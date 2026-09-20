"""Loopback, single-user option authoring. Run with --help for workspace setup."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from multiprocessing import get_context
from pathlib import Path
import secrets
import sqlite3
from urllib.parse import parse_qs, urlsplit

from catalog import authoring
from catalog import authoring_records as records, authoring_acceptance as acceptance
from catalog import authoring_relationships as relationships
from catalog import authoring_components as components
from catalog.consumers import encode


class Application:
    def __init__(self, database):
        self.database = Path(database)
        self.pending = {}
        self.release_jobs = {}
        # The audit is CPU-bound. A separate process keeps SQLite-backed editor
        # reads responsive instead of competing with its thread for the GIL.
        self.release_worker = ProcessPoolExecutor(max_workers=1, mp_context=get_context('spawn'))
        with closing(authoring.open_workspace(self.database)) as db:
            relationships.prepare(db)
            components.prepare(db)
            records.prepare(db)
            acceptance.prepare(db)

    def read(self, path):
        url = urlsplit(path)
        with closing(authoring.open_workspace(self.database)) as db:
            if url.path == '/api/release/status':
                query = parse_qs(url.query)
                future = self.release_jobs.get(query['job'][0])
                if future is None:
                    raise ValueError('Unknown release job')
                if not future.done():
                    return {'state': 'running', 'message': 'Validating source replay and all six model lanes, then generating the release.'}
                try:
                    return dict(state='completed', **future.result())
                except Exception as error:
                    return dict(state='failed', error=str(error))
            if url.path == '/api/editors':
                return {'editors': [records.schema(db,t) for t in records.FIELDS]}
            if url.path == '/api/records':
                query = parse_qs(url.query)
                return records.listing(db, query['revision'][0], query['table'][0])
            if url.path == '/api/acceptance':
                return acceptance.review(db)
            if url.path == '/api/component-rates':
                query = parse_qs(url.query)
                return {'rates': components.rates(db, query['revision'][0])}
            if url.path == '/api/component-rate':
                query = parse_qs(url.query)
                return components.detail(db, query['revision'][0], query['component'][0], query['configuration'][0])
            if url.path == '/api/catalog':
                return {'models': authoring.catalog(db)}
            if url.path == '/api/option':
                query = parse_qs(url.query)
                return authoring.detail(db, query['revision'][0], query['option'][0])
            if url.path == '/api/relationships':
                query = parse_qs(url.query)
                return {'relationships': relationships.relationships(db, query['revision'][0])}
            if url.path == '/api/relationship':
                query = parse_qs(url.query)
                return relationships.detail(db, query['revision'][0], query['relationship'][0])
        raise ValueError('Unknown operation')

    def dispatch(self, path, body):
        if path == '/api/release/create':
            if any(not f.done() for f in self.release_jobs.values()):
                raise ValueError('A release is already being built')
            job = secrets.token_urlsafe(24)
            self.release_jobs[job] = self.release_worker.submit(build_release, self.database, body['etag'])
            return {'job': job}
        if path == '/api/cancel':
            self.pending.pop(body['token'], None)
            return {'cancelled': True}
        with closing(authoring.open_workspace(self.database)) as db:
            if path in ('/api/records/preview','/api/acceptance/preview'):
                self.pending.pop(body.get('previous_token'), None)
                if path == '/api/records/preview':
                    change = records.preview(db, body['revision_id'], body['etag'], body['requests'], body['reason'], body.get('scenarios'))
                else:
                    change = acceptance.preview(db, body['etag'], body['reviewer'], body['reason'], body.get('intake_decisions'))
                if len(self.pending) >= 128:
                    self.pending.pop(next(iter(self.pending)))
                token = secrets.token_urlsafe(32)
                self.pending[token] = change
                return dict(token=token, **change)
            if path in ('/api/records/save','/api/acceptance/save'):
                kind = 'records' if path == '/api/records/save' else 'acceptance'
                change = self.pending.pop(body['token'], None)
                if change is None or change.get('kind') != kind:
                    raise ValueError('Preview expired; review again')
                return records.save(db, change) if kind == 'records' else acceptance.accept(db, change)
            if path == '/api/intake/stage':
                return acceptance.stage(db, body['payload'])
            if path == '/api/intake/disposition':
                return acceptance.disposition(db, body['intake_id'], body['decision'], body['reviewer'], body['reason'])
            if path == '/api/relationship/preview':
                self.pending.pop(body.get('previous_token'), None)
                change = relationships.preview(db, body['revision_id'], body['acquisition_id'],
                                               body['etag'], body['intent_policy'], body['reason'])
                if len(self.pending) >= 128:
                    self.pending.pop(next(iter(self.pending)))
                token = secrets.token_urlsafe(32)
                self.pending[token] = change
                return dict(token=token, **change)
            if path == '/api/relationship/save':
                change = self.pending.pop(body['token'], None)
                if change is None or change.get('kind') != 'relationship':
                    raise ValueError('Preview expired; review your relationship again')
                return relationships.save(db, change)
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
            if path == '/api/component-rate/preview':
                self.pending.pop(body.get('previous_token'), None)
                change = components.preview(db, body['revision_id'], body['component_id'], body['configuration_id'],
                                            body['etag'], body['price'], body['reason'])
                if len(self.pending) >= 128:
                    self.pending.pop(next(iter(self.pending)))
                token = secrets.token_urlsafe(32)
                self.pending[token] = change
                return dict(token=token, **change)
            if path == '/api/component-rate/save':
                change = self.pending.pop(body['token'], None)
                if change is None or change.get('kind') != 'component':
                    raise ValueError('Preview expired; review your shared rate again')
                return components.save(db, change)
        raise ValueError('Unknown operation')


def build_release(database, expected_digest):
    from catalog.releases import ReleaseStore
    store = ReleaseStore(Path(database).resolve().parent / 'releases')
    with closing(authoring.open_workspace(database)) as db:
        frozen = store.freeze(db, expected_digest)
    release = store.complete(frozen)
    manifest = store.verify(release)
    return dict(release_id=release, frozen_id=frozen, artifact_count=len(manifest['artifacts']),
                store=str(store.root), evidence=str(store.completed / release / 'reviewed-edits.json'))


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
            files = {'/records': ('records.html', 'text/html; charset=utf-8'),
                     '/records.js': ('records.js', 'text/javascript'),
                     '/acceptance': ('acceptance.html', 'text/html; charset=utf-8'),
                     '/acceptance.js': ('acceptance.js', 'text/javascript'),
                     '/relationships': ('relationships.html', 'text/html; charset=utf-8'),
                     '/relationships.js': ('relationships.js', 'text/javascript'),
                     '/': ('index.html', 'text/html; charset=utf-8'),
                     '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
            files.update({'/components': ('components.html', 'text/html; charset=utf-8'),
                          '/components.js': ('components.js', 'text/javascript')})
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
                if not 0 < length <= 1048576:
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
