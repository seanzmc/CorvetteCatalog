"""Customer build form backed by one verified completed release.

Run locally:  python3 -m catalog.consumer_server --store PATH --release CONTENT_ID
Run publicly: CATALOG_BUILD_TOKEN_KEY=... python3 -m catalog.consumer_server \\
                --store PATH --release CONTENT_ID --host 0.0.0.0 --origin https://build.example.com

The server keeps no build state. Each response carries a signed build token
(release, model, configuration and confirmed actions); the server rebuilds the
build by replaying those actions. A preview returns a short-lived signed pending
token bound to that build and warning; confirmation re-derives the preview and
requires the same warning. Dealer payloads use the rebuilt server state. Live
dealer delivery is opt-in.
"""
import argparse
import base64
from contextlib import closing
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import sys
import time
from urllib.parse import urlsplit

from catalog import foundation as f
from catalog import dealer, artwork
from catalog.consumers import ConsumerCatalog, ConsumerSession, encode
from catalog.evaluator import EvaluationError
from catalog.releases import ReleaseStore, pins

MAX_HISTORY = 200          # confirmed actions carried in one build token
PENDING_SECONDS = 15 * 60  # how long a reviewed change can wait for confirmation
MAX_REQUEST = 65536
KEY_VARIABLE = 'CATALOG_BUILD_TOKEN_KEY'
UNAVAILABLE = 'This saved build can no longer be opened; start a new build'


def _b64(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode()


def _unb64(text):
    return base64.urlsafe_b64decode(text + '=' * (-len(text) % 4))


class Tokens:
    """HMAC-signed JSON. The kind field keeps build and pending tokens apart."""
    def __init__(self, key):
        self.key = key

    def _mac(self, body):
        return hmac.new(self.key, body.encode(), hashlib.sha256).digest()

    def sign(self, kind, payload):
        body = _b64(encode(dict(payload, k=kind, v=1)).encode())
        return body + '.' + _b64(self._mac(body))

    def verify(self, token, kind):
        try:
            body, mac = str(token).split('.')
            valid = hmac.compare_digest(_unb64(mac), self._mac(body))
            payload = json.loads(_unb64(body)) if valid else None
        except (ValueError, TypeError):
            payload = None
        if not isinstance(payload, dict) or payload.get('k') != kind or payload.get('v') != 1:
            raise ValueError('Missing, altered or foreign build' if kind == 'build'
                             else 'Missing, stale, foreign or altered confirmation')
        return payload


class Application:
    def __init__(self, store, identifier, dealer_submissions=False, token_key=None):
        self.store, self.identifier = store, identifier
        self.manifest = store.verify(identifier)
        if self.manifest['runtime'] != pins():
            raise ValueError('Use the runtime pinned in this release')
        self.artwork_root = store.completed / identifier / 'runtime/catalog/web/artwork'
        with closing(f.connect(store.completed / identifier / 'catalog.sqlite')) as db:
            self.catalogs = {m['model_key']: ConsumerCatalog(db, m['revision_id']) for m in self.manifest['models']}
        self.dealer_submissions = dealer_submissions
        # Without a configured key, tokens are valid only for this process.
        self.tokens = Tokens(token_key or secrets.token_bytes(32))

    def catalog(self):
        return dict(release_id=self.identifier, default_model=self.manifest['default_model'],
                    dealer=dict(enabled=self.dealer_submissions, endpoint=dealer.ENDPOINT if self.dealer_submissions else None,
                                site_key=dealer.SITE_KEY if self.dealer_submissions else None),
                    models={key: cat.contract() for key,cat in self.catalogs.items()})

    def response(self, build, session, notice=None):
        token = self.tokens.sign('build', dict(r=self.identifier, m=build['m'], c=build['c'], h=build['h']))
        result = dict(build_token=token, model=build['m'], configuration_id=build['c'],
                      **session.current(), cards=session.catalog.cards(session._session.state))
        return dict(result, notice=notice) if notice else result

    def rebuild(self, token):
        """Verify a build token and replay its confirmed actions on this release."""
        build = self.tokens.verify(token, 'build')
        catalog = self.catalogs.get(build.get('m'))
        history = build.get('h')
        if catalog is None or build.get('c') not in catalog.ev.configs or not isinstance(history, list) or len(history) > MAX_HISTORY:
            raise ValueError(UNAVAILABLE)
        session = ConsumerSession(catalog, build['c'], self.identifier)
        try:
            for action, target in history:
                step = session.preview(action, target, session.version)
                session.confirm(step['token'], step['warning_sha256'], session.version)
        except (EvaluationError, TypeError, ValueError):
            raise ValueError(UNAVAILABLE) from None
        return build, session

    def dispatch(self, path, body):
        if path == '/api/session':
            catalog = self.catalogs.get(body['model'])
            if catalog is None or body['configuration_id'] not in catalog.ev.configs:
                raise ValueError('Choose an available model and configuration')
            session = ConsumerSession(catalog, body['configuration_id'], self.identifier)
            return self.response(dict(m=body['model'], c=body['configuration_id'], h=[]), session)
        build, session = self.rebuild(body.get('build_token'))
        if path == '/api/restore':
            notice = None if build['r'] == self.identifier else \
                'The catalog was updated since this build was saved. Prices and availability reflect the current catalog.'
            return self.response(build, session, notice)
        if path == '/api/preview':
            if len(build['h']) >= MAX_HISTORY:
                raise ValueError('This build has reached its change limit; download it or start a new build')
            result = session.preview(body['action'], body.get('target'), body['version'])
            pending = self.tokens.sign('pending', dict(b=hashlib.sha256(body['build_token'].encode()).hexdigest(),
                a=body['action'], t=body.get('target'), w=result['warning_sha256'], x=int(time.time()) + PENDING_SECONDS))
            return dict(result, token=pending)
        if path == '/api/confirm':
            pending = self.tokens.verify(body.get('token'), 'pending')
            if (pending['b'] != hashlib.sha256(body['build_token'].encode()).hexdigest()
                    or pending['w'] != body.get('warning_sha256') or pending['x'] < time.time()):
                raise ValueError('Missing, stale, foreign or altered confirmation')
            session._version(body['version'])
            # Re-derive the change; it is applied only if the warning is identical.
            fresh = session.preview(pending['a'], pending['t'], session.version)
            if fresh['warning_sha256'] != pending['w']:
                raise ValueError('This change no longer matches what you reviewed; review it again')
            session.confirm(fresh['token'], fresh['warning_sha256'], session.version)
            return self.response(dict(build, h=build['h'] + [[pending['a'], pending['t']]]), session)
        if path == '/api/cancel':
            session._version(body['version'])
            return self.response(build, session)
        if path == '/api/order':
            return session.order()
        if path == '/api/dealer/review':
            return dealer.review(session, body['version'])
        if path == '/api/dealer/prepare':
            # The dealer contract accepts only contact details, version and security token.
            fields = {k: v for k, v in body.items() if k != 'build_token'}
            return dealer.prepare(session, fields, require_turnstile=self.dealer_submissions)
        raise ValueError('Unknown operation')


def handler(app, origins=None):
    """origins: allowed browser origins; None allows only this loopback port."""
    class Handler(BaseHTTPRequestHandler):
        def allowed_origins(self):
            return set(origins) if origins else {f'http://127.0.0.1:{self.server.server_port}'}

        def log_message(self, format, *args):
            # Request line and status only; client addresses are not recorded.
            sys.stderr.write(f'{self.log_date_time_string()} {format % args}\n')

        def send(self, status, payload, content_type='application/json'):
            raw = payload if isinstance(payload, bytes) else encode(payload).encode()
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            security = "default-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
            if app.dealer_submissions:
                security += "; script-src 'self' https://challenges.cloudflare.com; frame-src https://challenges.cloudflare.com; connect-src 'self' https://challenges.cloudflare.com https://stingraychevroletcorvette.com"
            else:
                security += "; script-src 'self'; connect-src 'self'"
            self.send_header('Content-Security-Policy', security)
            self.end_headers()
            self.wfile.write(raw)

        def allowed(self):
            allowed = self.allowed_origins()
            hosts = {urlsplit(origin).netloc for origin in allowed}
            origin = self.headers.get('Origin')
            return self.headers.get('Host') in hosts and (origin is None or origin in allowed)

        def do_GET(self):
            if self.path == '/healthz':
                # Platform health probes may not send the public Host header.
                return self.send(200, {'status': 'ok', 'release_id': app.identifier})
            if not self.allowed():
                return self.send(403, {'error': 'Wrong origin'})
            if self.path == '/api/catalog':
                return self.send(200, app.catalog())
            if self.path.startswith('/artwork/'):
                path = artwork.asset_path(self.path, root=app.artwork_root)
                if path is not None:
                    return self.send(200, path.read_bytes(), 'image/webp')
                return self.send(404, {'error':'Artwork not found'})
            files = {'/': ('index.html','text/html; charset=utf-8'), '/app.js': ('app.js','text/javascript'),
                     '/dealer.js': ('dealer.js','text/javascript'), '/artwork.js': ('artwork.js','text/javascript'), '/style.css': ('style.css','text/css')}
            if self.path not in files:
                return self.send(404, {'error':'Not found'})
            name, mime = files[self.path]
            return self.send(200, (Path(__file__).with_name('web') / name).read_bytes(), mime)

        def do_POST(self):
            if not self.allowed() or self.headers.get('Content-Type') != 'application/json':
                return self.send(403, {'error':'Wrong origin or content type'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= MAX_REQUEST:
                    raise ValueError('Invalid request size')
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError('Expected request object')
                result = app.dispatch(self.path, body)
                self.send(200, result)
            except (ValueError, KeyError, TypeError) as error:
                self.send(409, {'error': str(error)})
    return Handler


def token_key(host):
    """The signing key from the environment; required when serving beyond loopback."""
    value = os.environ.get(KEY_VARIABLE, '')
    if value and len(value) < 32:
        raise SystemExit(f'{KEY_VARIABLE} must be at least 32 characters')
    if not value and host not in ('127.0.0.1', 'localhost', '::1'):
        raise SystemExit(f'Set {KEY_VARIABLE} to serve on {host}; builds would not survive a restart without it')
    return value.encode() or None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--release', required=True)
    parser.add_argument('--host', default='127.0.0.1', help='Interface to listen on (default loopback only)')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--origin', action='append', default=[],
                        help='Allowed browser origin, e.g. https://build.example.com; repeat for several (default this loopback port)')
    parser.add_argument('--enable-dealer-submissions', action='store_true',
                        help='Enable the existing dealer endpoint and Turnstile; otherwise preview without sending')
    args = parser.parse_args()
    app = Application(ReleaseStore(args.store), args.release, args.enable_dealer_submissions, token_key(args.host))
    with ThreadingHTTPServer((args.host, args.port), handler(app, args.origin or None)) as server:
        print(f'Customer build form: http://{args.host}:{server.server_port}', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
