"""Static files that let the customer form run in the browser (Pyodide).

Run: python -m catalog.static_bundle build --store STORE --release RELEASE_ID --output DIR
     python -m catalog.static_bundle verify DIR

A bundle is made from one verified completed release and is a complete static
site: open index.html from any folder. It holds:
- the release's own form page (index.html, scripts, styles, brand images), which
  runs the engine in a Web Worker through Pyodide (catalog.browser);
- catalog.json.gz: every model's contract, so the first screen needs no Python;
- catalog/<model>.sqlite.gz: only the tables the engine reads for that model,
  observed while loading it, so a shopper downloads one small model;
- engine/catalog/*.py: the release's own engine code;
- artwork/...: the release's verified artwork images, plus artwork-manifest.json;
- bundle.json: release identity, models and the SHA-256 of every file.
Building checks that every trimmed model gives the same contract and option
cards as the full release. Output is reproducible for a given release.
"""
import argparse
from contextlib import closing
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile

from catalog import artwork
from catalog import builds
from catalog.consumers import ConsumerCatalog, encode
from catalog.releases import ReleaseStore, pins

FORMAT = 'catalog-static-bundle-v1'
# The browser runtime the bundle was measured with; the page loads this version.
PYODIDE_VERSION = '314.0.7'
# The import closure of catalog.browser (checked by a test).
ENGINE = ('__init__', 'artwork', 'browser', 'builds', 'consumers', 'dealer', 'evaluator', 'foundation', 'foundation_schema')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_tables(db, revision, manifest):
    """Load one model the way the form does and record every table it reads."""
    seen = set()
    def authorize(action, table, *_):
        if action == sqlite3.SQLITE_READ:
            seen.add(table)
        return sqlite3.SQLITE_OK
    db.set_authorizer(authorize)
    try:
        catalog = ConsumerCatalog(db, revision, artwork_manifest=manifest)
    finally:
        db.set_authorizer(None)
    return catalog, sorted(seen)


def trim(db, revision, tables):
    """A new database holding only these tables, limited to this revision where they carry one."""
    out = sqlite3.connect(':memory:')
    for table in tables:
        sql, = db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
        out.execute(sql)
        columns = [c[1] for c in db.execute(f'PRAGMA table_info("{table}")')]
        where, args = (' WHERE revision_id=? ORDER BY rowid', (revision,)) if 'revision_id' in columns else (' ORDER BY rowid', ())
        rows = db.execute(f'SELECT * FROM "{table}"' + where, args).fetchall()
        out.executemany(f'INSERT INTO "{table}" VALUES ({",".join("?" * len(columns))})', [tuple(r) for r in rows])
    out.commit()
    return out


def trimmed_catalog(db, revision, tables, manifest):
    """Trim, adding any table a load still needs. SQLite's read hook does not report
    tables used only as join keys (model_year), so a failed load names them."""
    tables = list(tables)
    for _ in range(10):
        small = trim(db, revision, tables)
        small.row_factory = sqlite3.Row
        try:
            ConsumerCatalog(small, revision, artwork_manifest=manifest)
            return small, sorted(tables)
        except sqlite3.OperationalError as error:
            small.close()
            missing = str(error).removeprefix('no such table: ')
            if missing == str(error) or missing in tables:
                raise
            tables.append(missing)
    raise ValueError('Could not find the tables the engine needs')


def same_behavior(full, trimmed):
    """The trimmed catalog must give the same contract and starting cards everywhere."""
    if encode(full.contract()) != encode(trimmed.contract()):
        return False
    return all(encode(full.cards(full.ev.state(c))) == encode(trimmed.cards(trimmed.ev.state(c)))
               for c in sorted(full.ev.configs))


def gzip_bytes(raw):
    buffer = io.BytesIO()
    # A fixed timestamp and no file name keep the output reproducible.
    with gzip.GzipFile(filename='', mode='wb', fileobj=buffer, mtime=0, compresslevel=9) as out:
        out.write(raw)
    return buffer.getvalue()


def build(store, release, destination):
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Bundle destination already exists')
    record = store.verify(release)
    if record['runtime'] != pins():
        raise ValueError('Use the runtime pinned in this release')
    bundle = store.completed / release
    runtime = bundle / 'runtime/catalog'
    manifest = artwork.load_collection(runtime / 'web/artwork')
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.bundle-', dir=destination.parent))
    try:
        models, contracts = [], {}
        (stage / 'catalog').mkdir()
        with closing(sqlite3.connect(':memory:')) as db:
            with closing(sqlite3.connect((bundle / 'catalog.sqlite').resolve().as_uri() + '?mode=ro', uri=True)) as source:
                source.backup(db)
            db.row_factory = sqlite3.Row
            for model in sorted(record['models'], key=lambda m: m['display_order']):
                full, tables = read_tables(db, model['revision_id'], manifest)
                contracts[model['model_key']] = full
                small, tables = trimmed_catalog(db, model['revision_id'], tables, manifest)
                with closing(small):
                    if not same_behavior(full, ConsumerCatalog(small, model['revision_id'], artwork_manifest=manifest)):
                        raise ValueError('Trimmed catalog differs from the release: ' + model['model_key'])
                    with tempfile.TemporaryDirectory() as scratch:
                        path = Path(scratch) / 'model.sqlite'
                        with closing(sqlite3.connect(path)) as disk:
                            small.backup(disk)
                            disk.execute('VACUUM')
                        raw = path.read_bytes()
                name = f'catalog/{model["model_key"]}.sqlite.gz'
                (stage / name).write_bytes(gzip_bytes(raw))
                models.append(dict(model_key=model['model_key'], registry_key=model['registry_key'],
                                   display_order=model['display_order'], revision_id=model['revision_id'],
                                   catalog=name, tables=tables, uncompressed_bytes=len(raw)))
        # Dealer delivery from the browser is not enabled yet: the page previews it.
        form = builds.description(release, record['default_model'], contracts)
        (stage / 'catalog.json.gz').write_bytes(gzip_bytes(encode(form).encode()))
        web = runtime / 'web'
        for source in sorted(web.rglob('*')):
            if source.is_file() and not source.relative_to(web).parts[0] == 'artwork':
                target = stage / source.relative_to(web)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        for name in ENGINE:
            target = stage / 'engine/catalog' / (name + '.py')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(runtime / (name + '.py'), target)
        prefix = 'runtime/catalog/web/artwork/'
        for asset in record['media'].get('assets', []):
            target = stage / 'artwork' / asset['path'].removeprefix(prefix)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(bundle / asset['path'], target)
        (stage / 'artwork-manifest.json').write_text(encode(manifest) + '\n')
        files = {str(p.relative_to(stage)): sha256(p) for p in sorted(stage.rglob('*')) if p.is_file()}
        description = dict(format=FORMAT, release_id=release, default_model=record['default_model'],
                           pyodide=PYODIDE_VERSION, contract='catalog.json.gz', engine=[f'engine/catalog/{n}.py' for n in ENGINE],
                           artwork_manifest='artwork-manifest.json', models=models, files=files)
        (stage / 'bundle.json').write_text(json.dumps(description, indent=2, sort_keys=True) + '\n')
        verify(stage)
        os.rename(stage, destination)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return destination


def verify(path):
    """Every listed file is present with its hash, and nothing else is."""
    path = Path(path)
    description = json.loads((path / 'bundle.json').read_text())
    if description.get('format') != FORMAT:
        raise ValueError('Not a catalog static bundle')
    # A bundle is self-contained: links could point outside it or hide entries.
    if any(p.is_symlink() for p in path.rglob('*')):
        raise ValueError('Bundles may not contain symbolic links')
    manifest = path / 'bundle.json'
    actual = {str(p.relative_to(path)): sha256(p) for p in sorted(path.rglob('*'))
              if p.is_file() and p != manifest}
    if actual != description['files']:
        raise ValueError('Missing, altered or unexpected bundle files')
    return description


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    make = commands.add_parser('build', help='Write a static bundle for one completed release')
    make.add_argument('--store', type=Path, required=True)
    make.add_argument('--release', required=True)
    make.add_argument('--output', type=Path, required=True)
    commands.add_parser('verify', help='Check a bundle against its bundle.json').add_argument('path', type=Path)
    args = parser.parse_args()
    if args.command == 'build':
        print(build(ReleaseStore(args.store), args.release, args.output))
    else:
        description = verify(args.path)
        print(f'Bundle for release {description["release_id"]}: {len(description["files"])} files verified')


if __name__ == '__main__':
    main()
