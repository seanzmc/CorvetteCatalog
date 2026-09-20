"""Loopback, single-user option authoring. Run with --help for workspace setup."""
import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
from urllib.parse import parse_qs, urlsplit

from catalog import authoring
from catalog.consumers import encode


class Application:
    def __init__(self, database):
        self.database = Path(database)
        self.pending = {}
        with closing(authoring.open_workspace(self.database)):
            pass

    def read(self, path):
        url = urlsplit(path)
        with closing(authoring.open_workspace(self.database)) as db:
            if url.path == '/api/catalog':
                return {'models': authoring.catalog(db)}
            if url.path == '/api/option':
                query = parse_qs(url.query)
                return authoring.detail(db, query['revision'][0], query['option'][0])
        raise ValueError('Unknown operation')

    def dispatch(self, path, body):
        if path == '/api/cancel':
            self.pending.pop(body['token'], None)
            return {'cancelled': True}
        with closing(authoring.open_workspace(self.database)) as db:
            if path == '/api/preview':
                previous = body.get('previous_token')
                if previous is not None:
                    self.pending.pop(previous, None)
                change = authoring.preview(db, body['revision_id'], body['option_id'], body['etag'],
                                           body['name'], body['price'], body['reason'])
                if len(self.pending) >= 128:
                    self.pending.pop(next(iter(self.pending)))
                token = secrets.token_urlsafe(32)
                self.pending[token] = change
                return dict(token=token, **change)
            if path == '/api/save':
                change = self.pending.pop(body['token'], None)
                if change is None:
                    raise ValueError('Preview expired; review your changes again')
                return authoring.save(db, change)
        raise ValueError('Unknown operation')


def handler(app):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, payload, content_type='application/json'):
            raw = payload if isinstance(payload, bytes) else encode(payload).encode()
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def allowed(self):
            authority = f'127.0.0.1:{self.server.server_port}'
            return self.headers.get('Host') == authority and self.headers.get('Origin', 'http://' + authority) == 'http://' + authority

        def do_GET(self):
            if not self.allowed():
                return self.send(403, {'error': 'Wrong origin'})
            files = {'/': ('index.html', 'text/html; charset=utf-8'),
                     '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
            if self.path in files:
                filename, mime = files[self.path]
                return self.send(200, (Path(__file__).with_name('authoring_web') / filename).read_bytes(), mime)
            try:
                self.send(200, app.read(self.path))
            except (ValueError, KeyError, IndexError, TypeError) as error:
                self.send(400, {'error': str(error)})

        def do_POST(self):
            if not self.allowed() or self.headers.get('Content-Type') != 'application/json':
                return self.send(403, {'error': 'Wrong origin or content type'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 16384:
                    raise ValueError('Invalid request size')
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError('Expected request object')
                self.send(200, app.dispatch(self.path, body))
            except (ValueError, KeyError, TypeError, sqlite3.Error) as error:
                self.send(409, {'error': str(error)})
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True, help='Separate local authoring database')
    parser.add_argument('--initialize-from', type=Path, help='Create a new workspace from a source-verified draft; then exit')
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()
    if args.initialize_from:
        print('Created authoring workspace from baseline', authoring.initialize(args.initialize_from, args.database))
        return
    with HTTPServer(('127.0.0.1', args.port), handler(Application(args.database))) as server:
        print(f'Local catalog authoring: http://127.0.0.1:{server.server_port}', flush=True)
        server.serve_forever()


if __name__ == '__main__':
    main()
