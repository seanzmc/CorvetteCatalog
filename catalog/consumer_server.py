"""Loopback review form backed by one verified completed local release.

Run: python3 -m catalog.consumer_server --store PATH --release CONTENT_ID
Dealer payloads use confirmed server state. Live browser delivery is opt-in.
"""
import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets

from catalog import foundation as f
from catalog import dealer
from catalog.consumers import ConsumerCatalog, ConsumerSession, encode
from catalog.releases import ReleaseStore, pins


class Application:
    def __init__(self, store, identifier, dealer_submissions=False):
        self.store, self.identifier = store, identifier
        self.manifest = store.verify(identifier)
        if self.manifest['runtime'] != pins():
            raise ValueError('Use the runtime pinned in this release')
        with closing(f.connect(store.completed / identifier / 'catalog.sqlite')) as db:
            self.catalogs = {m['model_key']: ConsumerCatalog(db, m['revision_id']) for m in self.manifest['models']}
        self.sessions = {}
        self.dealer_submissions = dealer_submissions

    def catalog(self):
        return dict(release_id=self.identifier, default_model=self.manifest['default_model'],
                    dealer=dict(enabled=self.dealer_submissions, endpoint=dealer.ENDPOINT if self.dealer_submissions else None,
                                site_key=dealer.SITE_KEY if self.dealer_submissions else None),
                    models={key: cat.contract() for key,cat in self.catalogs.items()})

    def response(self, session):
        return dict(**session.current(), cards=session.catalog.cards(session._session.state))

    def dispatch(self, path, body, session_id=None):
        if path == '/api/session':
            if len(self.sessions) >= 256:
                raise ValueError('Local session limit reached; restart the review server')
            catalog = self.catalogs[body['model']]
            session = ConsumerSession(catalog, body['configuration_id'], self.identifier)
            identifier = secrets.token_urlsafe(32)
            self.sessions[identifier] = session
            return dict(session_id=identifier, **self.response(session))
        if session_id not in self.sessions:
            raise ValueError('Unknown session')
        session = self.sessions[session_id]
        if path == '/api/preview':
            return session.preview(body['action'], body.get('target'), body['version'])
        if path == '/api/confirm':
            session.confirm(body['token'], body['warning_sha256'], body['version'])
        elif path == '/api/cancel':
            session.cancel(body['version'])
        elif path == '/api/order':
            return session.order()
        elif path == '/api/dealer/review':
            return dealer.review(session, body['version'])
        elif path == '/api/dealer/prepare':
            return dealer.prepare(session, body, require_turnstile=self.dealer_submissions)
        else:
            raise ValueError('Unknown operation')
        return self.response(session)


def handler(app):
    class Handler(BaseHTTPRequestHandler):
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
            authority = f'127.0.0.1:{self.server.server_port}'
            return self.headers.get('Host') == authority and self.headers.get('Origin', 'http://' + authority) == 'http://' + authority

        def do_GET(self):
            if not self.allowed():
                return self.send(403, {'error': 'Wrong origin'})
            if self.path == '/api/catalog':
                return self.send(200, app.catalog())
            files = {'/': ('index.html','text/html; charset=utf-8'), '/app.js': ('app.js','text/javascript'),
                     '/dealer.js': ('dealer.js','text/javascript'), '/style.css': ('style.css','text/css')}
            if self.path not in files:
                return self.send(404, {'error':'Not found'})
            name, mime = files[self.path]
            return self.send(200, (Path(__file__).with_name('web') / name).read_bytes(), mime)

        def do_POST(self):
            if not self.allowed() or self.headers.get('Content-Type') != 'application/json':
                return self.send(403, {'error':'Wrong origin or content type'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 16384:
                    raise ValueError('Invalid request size')
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError('Expected request object')
                result = app.dispatch(self.path, body, self.headers.get('X-Catalog-Session'))
                self.send(200, result)
            except (ValueError, KeyError, TypeError) as error:
                self.send(409, {'error': str(error)})
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--release', required=True)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--enable-dealer-submissions', action='store_true',
                        help='Enable the existing dealer endpoint and Turnstile; otherwise preview without sending')
    args = parser.parse_args()
    app = Application(ReleaseStore(args.store), args.release, args.enable_dealer_submissions)
    with HTTPServer(('127.0.0.1', args.port), handler(app)) as server:
        print(f'Local consumer review: http://127.0.0.1:{server.server_port}', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
