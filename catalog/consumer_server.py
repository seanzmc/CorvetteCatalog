"""Customer build form backed by one verified completed release.

Run locally:  python3 -m catalog.consumer_server --store PATH --release CONTENT_ID
Run publicly: CATALOG_BUILD_TOKEN_KEY=... python3 -m catalog.consumer_server \\
                --store PATH --release CONTENT_ID --host 0.0.0.0 --origin https://build.example.com

The server keeps no build state beyond a one-build replay cache: each response
carries a signed build token and the build is rebuilt from it (catalog.builds).
Live dealer delivery is opt-in.
"""
import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import sys
import threading
import time
from urllib.parse import urlsplit

from catalog import foundation as f
from catalog import artwork
from catalog.builds import Builds, Tokens, description
from catalog.consumers import ConsumerCatalog, encode
from catalog.releases import ReleaseStore, pins

MAX_REQUEST = 65536
KEY_VARIABLE = 'CATALOG_BUILD_TOKEN_KEY'


class Application(Builds):
    def __init__(self, store, identifier, dealer_submissions=False, token_key=None):
        self.store = store
        self.manifest = store.verify(identifier)
        if self.manifest['runtime'] != pins():
            raise ValueError('Use the runtime pinned in this release')
        self.artwork_root = store.completed / identifier / 'runtime/catalog/web/artwork'
        with closing(f.connect(store.completed / identifier / 'catalog.sqlite')) as db:
            catalogs = {m['model_key']: ConsumerCatalog(db, m['revision_id']) for m in self.manifest['models']}
        # Without a configured key, tokens are valid only for this process.
        super().__init__(identifier, catalogs, Tokens(token_key or secrets.token_bytes(32)), dealer_submissions)
        # Evaluators rebuild shared indexes on every call, so evaluation runs one
        # request at a time. Threads still keep pages, artwork and health checks
        # responsive; capacity comes from more instances, which tokens allow.
        self.evaluation = threading.Lock()

    def catalog(self):
        return description(self.identifier, self.manifest['default_model'], self.catalogs, self.dealer_submissions)

    def dispatch(self, path, body):
        with self.evaluation:
            return self._dispatch(path, body)

    def _dispatch(self, path, body):
        return Builds.dispatch(self, path, body)


class ChannelApp:
    """Serve whatever a channel names and follow it when it moves.

    A release pinned to different code cannot run in this process. The server
    then keeps its current release and reports that a restart is required.
    """
    def __init__(self, store, channel, dealer_submissions=False, token_key=None, interval=5.0):
        self.store, self.channel, self.interval = store, channel, interval
        self.dealer_submissions = dealer_submissions
        # One key for every release this process serves keeps saved builds valid.
        self.key = token_key or secrets.token_bytes(32)
        self.lock = threading.Lock()
        self.checked, self.restart_required = time.monotonic(), None
        release = store.pointer(channel)['release_id']
        if not release:
            raise ValueError(f'Nothing is published to the {channel} channel')
        self.current = Application(store, release, dealer_submissions, self.key)

    def refresh(self):
        with self.lock:
            if time.monotonic() - self.checked < self.interval:
                return self.current
            self.checked = time.monotonic()
            named = self.store.pointer(self.channel)['release_id']
            if named and named != self.current.identifier:
                try:
                    self.current = Application(self.store, named, self.dealer_submissions, self.key)
                    self.restart_required = None
                    print(f'Now serving release {named} from the {self.channel} channel', file=sys.stderr, flush=True)
                except ValueError as error:
                    if self.restart_required != named:
                        print(f'Restart to serve release {named}: {error}', file=sys.stderr, flush=True)
                    self.restart_required = named
            return self.current

    @property
    def identifier(self):
        return self.refresh().identifier

    @property
    def artwork_root(self):
        return self.refresh().artwork_root

    def catalog(self):
        return self.refresh().catalog()

    def dispatch(self, path, body):
        return self.refresh().dispatch(path, body)


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
            # Dealership-hosted images (favicon, catalog card photos) as in the existing form.
            security = "default-src 'self'; img-src 'self' https://stingraychevroletcorvette.com; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
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
                health = {'status': 'ok', 'release_id': app.identifier}
                if getattr(app, 'restart_required', None):
                    health['restart_required_for'] = app.restart_required
                return self.send(200, health)
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
                     '/dealer.js': ('dealer.js','text/javascript'), '/engine.js': ('engine.js','text/javascript'), '/artwork.js': ('artwork.js','text/javascript'), '/style.css': ('style.css','text/css'),
                     '/brand/crossflags-white.png': ('brand/crossflags-white.png','image/png'),
                     '/brand/stingray-wordmark-white.png': ('brand/stingray-wordmark-white.png','image/png')}
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
    chosen = parser.add_mutually_exclusive_group(required=True)
    chosen.add_argument('--release', help='Completed release ID to serve')
    chosen.add_argument('--channel', help='Serve the release a channel names, e.g. production')
    parser.add_argument('--host', default='127.0.0.1', help='Interface to listen on (default loopback only)')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--origin', action='append', default=[],
                        help='Allowed browser origin, e.g. https://build.example.com; repeat for several (default this loopback port)')
    parser.add_argument('--enable-dealer-submissions', action='store_true',
                        help='Enable the existing dealer endpoint and Turnstile; otherwise preview without sending')
    args = parser.parse_args()
    store = ReleaseStore(args.store)
    if args.release:
        app = Application(store, args.release, args.enable_dealer_submissions, token_key(args.host))
    else:
        try:
            app = ChannelApp(store, args.channel, args.enable_dealer_submissions, token_key(args.host))
        except ValueError as error:
            raise SystemExit(f'{error} in {args.store}') from None
    with ThreadingHTTPServer((args.host, args.port), handler(app, args.origin or None)) as server:
        print(f'Customer build form: http://{args.host}:{server.server_port}', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
