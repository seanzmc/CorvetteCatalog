#!/usr/bin/env python3
"""Open the current checked-in catalog without managing release IDs by hand."""
import argparse
from contextlib import closing
from http.server import HTTPServer
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from catalog import authoring, foundation as f
from catalog.behavior_sources import import_behavior
from catalog.consumers import import_mappings
from catalog.consumer_server import Application, handler
from catalog.releases import ReleaseStore, MODEL_KEYS, database_hash, file_hash, pins


def matches_checkout(bundle, manifest, runtime):
    """Only reuse source releases with current code, inputs and a full audit."""
    if manifest['runtime'] != runtime or 'reviewed_edits_sha256' in manifest['freeze']:
        return False
    validation = json.loads((bundle / 'validation.json').read_text())
    lanes = validation.get('semantic', {})
    if (validation.get('translation') != 'complete_pinned_replay'
            or set(lanes) != MODEL_KEYS
            or any(not isinstance(lane, dict) or lane.get('findings') != [] for lane in lanes.values())):
        return False
    with closing(sqlite3.connect((bundle / 'catalog.sqlite').resolve().as_uri() + '?mode=ro', uri=True)) as db:
        sources = db.execute('SELECT source_path,content_sha256 FROM source_document').fetchall()
    return bool(sources) and all(
        (ROOT / path).is_file() and file_hash(ROOT / path) == expected
        for path, expected in sources
    )


def find_release(local):
    runtime = pins()
    # Existing qualified bundles may live in a previous local review store.
    # Inspect metadata first; fully verify any matching bundle before using it.
    for path in sorted(local.glob('**/completed/*/manifest.json')):
        try:
            manifest = json.loads(path.read_text())
            if not matches_checkout(path.parent, manifest, runtime):
                continue
            store = ReleaseStore(path.parents[2])
            store.verify(path.parent.name)
            return store, path.parent.name
        except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as error:
            print(f'Skipping unusable local release {path.parent.name}: {error}', flush=True)
    return None


def build_release(local):
    store = ReleaseStore(local / 'preview' / 'releases')
    print('Preparing the current catalog…', flush=True)
    # A private temporary source draft leaves all editing workspaces untouched.
    with tempfile.TemporaryDirectory(prefix='source-', dir=store.root) as scratch:
        with closing(f.connect(Path(scratch) / 'catalog.sqlite')) as db:
            f.create_schema(db)
            import_behavior(db)
            import_mappings(db)
            print('Checking all six models. The first launch can take several minutes…', flush=True)
            frozen = store.freeze(db, database_hash(db))
        print('Preparing the form and artwork…', flush=True)
        release = store.complete(frozen)
    return store, release


def draft_release(database):
    """Reuse or build the release of an accepted editing draft, beside that draft."""
    store = ReleaseStore(Path(database).resolve().parent / 'releases')
    with closing(authoring.open_workspace(database)) as db:
        digest = database_hash(db)
    runtime = pins()
    for path in sorted(store.completed.glob('*/manifest.json')):
        manifest = json.loads(path.read_text())
        if manifest['freeze']['draft_sha256'] == digest and manifest['runtime'] == runtime:
            store.verify(path.parent.name)
            print('Reusing the release of this exact draft.', flush=True)
            return store, path.parent.name
    print('Building a release of your accepted draft. This can take several minutes…', flush=True)
    with closing(authoring.open_workspace(database)) as db:
        frozen = store.freeze(db, digest)
    return store, store.complete(frozen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--draft', type=Path, help='Preview an accepted editing draft instead of the checked-in catalog')
    parser.add_argument('--no-browser', action='store_true', help='Print the URL without opening a browser')
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('Port must be between 1 and 65535')
    # Reserve the port before doing expensive preparation; never stop another app.
    try:
        server = HTTPServer(('127.0.0.1', args.port), None)
    except OSError as error:
        parser.exit(1, f'Cannot open port {args.port}: {error}. Try --port {8767 if args.port != 8767 else 8768}.\n')
    with server:
        try:
            if args.draft:
                store, release = draft_release(args.draft)
            else:
                print('Looking for a verified release matching this checkout…', flush=True)
                local = ROOT / '.local'
                result = find_release(local)
                if result:
                    print('Reusing the current verified build.', flush=True)
                store, release = result or build_release(local)
            # Application verifies the bundle again and keeps live delivery off.
            server.RequestHandlerClass = handler(Application(store, release))
            url = f'http://127.0.0.1:{args.port}'
            print(f'CorvetteCatalog is ready: {url}\nLeave this terminal open. Press Ctrl+C to stop.', flush=True)
            if not args.no_browser:
                webbrowser.open(url)
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nPreview stopped.', flush=True)
        except (OSError, ValueError, sqlite3.Error) as error:
            parser.exit(1, f'Could not start the preview: {error}\n')


if __name__ == '__main__':
    main()
