"""HTTP boundary of the customer form: hosts, origins, health, logs and tokens."""
from contextlib import redirect_stderr
import io
import json
import os
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from catalog.consumer_server import Tokens, handler, token_key, ThreadingHTTPServer


class StubApp:
    """Only the attributes the handler reads; release behavior is tested elsewhere."""
    identifier = 'release-id'
    dealer_submissions = False
    artwork_root = None

    def catalog(self):
        return {'release_id': self.identifier}

    def dispatch(self, path, body):
        return {'path': path, 'body': body}


class ServerTests(unittest.TestCase):
    def serve(self, origins):
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler(StubApp(), origins))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server.server_port

    def call(self, port, path, host=None, origin=None, body=None):
        headers = {'Host': host} if host else {}
        if origin:
            headers['Origin'] = origin
        data = None
        if body is not None:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(body).encode()
        try:
            with urlopen(Request(f'http://127.0.0.1:{port}{path}', data=data, headers=headers), timeout=10) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_public_origin_allow_list_health_and_address_free_logs(self):
        port = self.serve(['https://build.example.com'])
        log = io.StringIO()
        with redirect_stderr(log):
            self.assertEqual(self.call(port, '/healthz', host='internal:8080'),
                             (200, {'status': 'ok', 'release_id': 'release-id'}))
            self.assertEqual(self.call(port, '/api/catalog', host='build.example.com')[0], 200)
            self.assertEqual(self.call(port, '/api/catalog')[0], 403)  # loopback host not allowed here
            self.assertEqual(self.call(port, '/api/restore', host='build.example.com',
                                       origin='https://evil.example', body={})[0], 403)
            status, result = self.call(port, '/api/restore', host='build.example.com',
                                       origin='https://build.example.com', body={'build_token': 't'})
        self.assertEqual((status, result['path']), (200, '/api/restore'))
        self.assertIn('/healthz', log.getvalue())
        self.assertNotIn('127.0.0.1', log.getvalue())

    def test_default_allows_only_this_loopback_port(self):
        port = self.serve(None)
        with redirect_stderr(io.StringIO()):
            self.assertEqual(self.call(port, '/api/catalog')[0], 200)
            self.assertEqual(self.call(port, '/api/catalog', host='build.example.com')[0], 403)
            self.assertEqual(self.call(port, '/api/restore', origin='http://127.0.0.1:1', body={})[0], 403)

    def test_signing_key_is_required_beyond_loopback(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(token_key('127.0.0.1'))
            with self.assertRaises(SystemExit):
                token_key('0.0.0.0')
        with patch.dict(os.environ, {'CATALOG_BUILD_TOKEN_KEY': 'short'}):
            with self.assertRaises(SystemExit):
                token_key('127.0.0.1')
        with patch.dict(os.environ, {'CATALOG_BUILD_TOKEN_KEY': 'k' * 32}):
            self.assertEqual(token_key('0.0.0.0'), b'k' * 32)

    def test_tokens_reject_tampering_and_kind_substitution(self):
        tokens = Tokens(b'k' * 32)
        build = tokens.sign('build', {'h': []})
        self.assertEqual(tokens.verify(build, 'build')['h'], [])
        body, mac = build.split('.')
        forged = tokens.sign('build', {'h': [['select', 'x']]}).split('.')[0] + '.' + mac
        for bad in (forged, build + 'x', 'not-a-token', None, tokens.sign('pending', {})):
            with self.assertRaises(ValueError):
                tokens.verify(bad, 'build')
        with self.assertRaises(ValueError):
            Tokens(b'x' * 32).verify(build, 'build')


if __name__ == '__main__':
    unittest.main()
