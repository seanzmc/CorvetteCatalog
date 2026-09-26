"""The customer form's engine inside the browser (Pyodide, in a Web Worker).

The page's worker copies a static bundle's files into Pyodide's file system and
calls Form.call with the same paths and bodies the server accepts; the answers
come from the same catalog.builds code. Each model's trimmed catalog is loaded
the first time a build uses it.
"""
import gzip
import json
from pathlib import Path
import sqlite3

from catalog.builds import Builds, Tokens, _unb64
from catalog.consumers import ConsumerCatalog, encode
from catalog.evaluator import EvaluationError

# The build token is kept in the shopper's own browser and every replayed action
# is re-evaluated, so its signature has no security role here: a fixed key lets a
# reload reopen the build. The dealer's receiver checks what it is sent.
KEY = b'catalog-browser-build'


def _catalog_bytes(raw):
    # A host may already have removed the gzip layer (Content-Encoding).
    return gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw


class Form:
    def __init__(self, root):
        self.root = Path(root)
        self.bundle = json.loads((self.root / 'bundle.json').read_text())
        self.manifest = json.loads((self.root / self.bundle['artwork_manifest']).read_text())
        self.models = {m['model_key']: m for m in self.bundle['models']}
        self.builds = Builds(self.bundle['release_id'], {}, Tokens(KEY))

    def model_for(self, path, body):
        if path == '/api/session':
            return body.get('model')
        try:
            return json.loads(_unb64(str(body.get('build_token')).split('.')[0])).get('m')
        except (ValueError, TypeError, AttributeError):
            return None

    def needs(self, path, text):
        """The bundle file of a model catalog this request needs and is not loaded yet;
        the worker fetches it into the file system before calling."""
        try:
            key = self.model_for(path, json.loads(text))
            if key in self.models and key not in self.builds.catalogs:
                return self.models[key]['catalog']
        except (ValueError, TypeError, AttributeError):
            pass  # call() reports the request's own error
        return None

    def load(self, key):
        if key in self.builds.catalogs or key not in self.models:
            return
        model = self.models[key]
        db = sqlite3.connect(':memory:')
        db.deserialize(_catalog_bytes((self.root / model['catalog']).read_bytes()))
        db.row_factory = sqlite3.Row
        self.builds.catalogs[key] = ConsumerCatalog(db, model['revision_id'], artwork_manifest=self.manifest)

    def call(self, path, text):
        """One request as JSON text; answers {status, result} like the server's statuses."""
        try:
            body = json.loads(text)
            if not isinstance(body, dict):
                raise ValueError('Expected request object')
            self.load(self.model_for(path, body))
            return encode(dict(status=200, result=self.builds.dispatch(path, body)))
        except (EvaluationError, ValueError, KeyError, TypeError) as error:
            return encode(dict(status=409, result=dict(error=str(error))))
