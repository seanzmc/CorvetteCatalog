"""Local frozen snapshots, deterministic consumer releases and CAS publication.

No deployment or canonical authority switch. Product inputs and validation are
captured before completion; publication/rollback only move a local pointer.
"""
import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
from collections import Counter

from catalog import foundation as f
from catalog.behavior_sources import import_behavior
from catalog.consumers import ConsumerCatalog, TABLES, encode, digest, import_mappings, validate_mappings
from catalog.semantic_validation import Audit, findings

FORMAT = 'catalog-release-v1'
MODEL_KEYS = {lane.replace('-', '_') for lane in f.LANES}


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def database_hash(db):
    """All schema and rows, including edit versions; independent of page layout."""
    tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    state = {t: sorted((list(row) for row in db.execute(f'SELECT * FROM "{t}"')), key=encode) for t in tables}
    state['schema'] = [list(r) for r in db.execute("SELECT type,name,sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY type,name")]
    return digest(state)


def membership(db):
    rows = [dict(r) for r in db.execute('''SELECT m.model_id,m.model_key,y.model_year_id,y.year,r.revision_id,r.edit_version,
        c.registry_key,c.legacy_alias,c.display_order,c.is_default,c.source_sha256,c.policy_sha256
        FROM catalog_revision r JOIN model_year y USING(model_year_id) JOIN model m USING(model_id)
        JOIN consumer_model c USING(revision_id) ORDER BY c.display_order,m.model_key''')]
    if len(rows) != 6 or {r['model_key'] for r in rows} != MODEL_KEYS or len({r['year'] for r in rows}) != 1:
        raise ValueError('A complete release requires exactly six matching model/year revisions')
    if sum(r['is_default'] for r in rows) != 1:
        raise ValueError('A release needs exactly one member as default')
    aliases = [alias for r in rows for alias in {r['model_key'], r['registry_key'], r['legacy_alias']} if alias]
    if len(aliases) != len(set(aliases)):
        raise ValueError('Ambiguous model alias')
    return rows


def validate_translation(db):
    """Replay pinned importers into a copy; missing/changed facts cannot pass."""
    with closing(f.connect(':memory:')) as check:
        db.backup(check)
        before = database_hash(check)
        versions = list(check.execute('SELECT revision_id,edit_version FROM catalog_revision'))
        with check:
            check.execute('UPDATE catalog_revision SET edit_version=1')
        import_behavior(check)
        with check:
            for revision, version in versions:
                check.execute('UPDATE catalog_revision SET edit_version=? WHERE revision_id=?', (version, revision))
        # Regenerate only consumer mappings. Product IDs remain the pinned IDs.
        with check:
            for table in ('consumer_option_context', 'consumer_option', 'consumer_configuration', 'consumer_interior', 'consumer_model'):
                check.execute(f'DELETE FROM {table}')
        import_mappings(check)
        if before != database_hash(check):
            raise ValueError('Draft differs from complete pinned source translation')
        # Idempotent replay checks expected values and missing facts, but an
        # additive importer cannot detect extra authored rows. A fresh import
        # supplies the exact per-table cardinalities; UUID values may differ.
        with closing(f.connect(':memory:')) as fresh:
            f.create_schema(fresh)
            import_behavior(fresh)
            import_mappings(fresh)
            schema_query = 'SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name'
            if list(check.execute(schema_query)) != list(fresh.execute(schema_query)):
                raise ValueError('Unexpected source translation schema')
            for table, in fresh.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
                if check.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] != fresh.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]:
                    raise ValueError('Unexpected source translation rows: ' + table)


def validate_semantics(db):
    """Run the existing whole-revision audit on the actual release snapshot."""
    results = {}
    for model in membership(db):
        key = model['model_key']
        audit = Audit(db, model['revision_id'])
        entries = audit.run()
        overlap = audit.overlaps()
        problems = findings({'lanes': {key: {'inventory': entries, 'overlaps': overlap}}})
        if problems:
            raise ValueError('Semantic validation failed: ' + encode(problems[:5]))
        results[key] = dict(inventory=len(entries), checks=dict(Counter(c['status'] for e in entries for c in e['checks'])),
                            live_overlaps=len(overlap['interactions']), findings=[])
        print(key, results[key], flush=True)
        audit._disjoint.cache_clear()
    return results


def write_json(path, data):
    Path(path).write_text(encode(data) + '\n')


def read_json(path):
    return json.loads(Path(path).read_text())


def check_id(identifier):
    if len(identifier) != 64 or any(c not in '0123456789abcdef' for c in identifier):
        raise ValueError('Invalid content identifier')


def runtime_files():
    return sorted([*Path(__file__).parent.glob('*.py'), *Path(__file__).with_name('web').glob('*')])


def pins():
    return {str(p.relative_to(f.ROOT)): file_hash(p) for p in runtime_files() if p.is_file()}


def _seal(stage, root, record, name, verify_existing):
    """Publish a fully built immutable directory by rename on this filesystem."""
    identifier = digest(record)
    write_json(stage / name, record)
    destination = root / identifier
    if destination.exists():
        if read_json(destination / name) != record:
            raise ValueError('Existing content identity mismatch')
        verify_existing(identifier)
        shutil.rmtree(stage)
    else:
        os.rename(stage, destination)
    return identifier


class ReleaseStore:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.frozen = self.root / 'frozen'
        self.completed = self.root / 'completed'
        self.frozen.mkdir(parents=True, exist_ok=True)
        self.completed.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.root / 'publication.sqlite')) as db, db:
            db.execute('''CREATE TABLE IF NOT EXISTS publication_pointer (
                channel TEXT PRIMARY KEY, release_id TEXT NOT NULL, version INTEGER NOT NULL)''')
            db.execute('''CREATE TABLE IF NOT EXISTS publication_history (
                channel TEXT NOT NULL, version INTEGER NOT NULL, release_id TEXT NOT NULL,
                previous_release_id TEXT, PRIMARY KEY(channel,version))''')

    def freeze(self, db, expected_digest):
        if db.in_transaction:
            raise ValueError('Commit the draft before freeze')
        stage = Path(tempfile.mkdtemp(prefix='.building-', dir=self.frozen))
        try:
            with closing(f.connect(stage / 'catalog.sqlite')) as snapshot:
                db.backup(snapshot)
                if database_hash(snapshot) != expected_digest:
                    raise ValueError('Stale draft snapshot')
                validate_mappings(snapshot)
                models = membership(snapshot)
                validate_translation(snapshot)
                runtime_pins = pins()
                semantics = validate_semantics(snapshot)
                if runtime_pins != pins():
                    raise ValueError('Runtime changed during freeze')
                write_json(stage / 'validation.json', dict(semantic=semantics, translation='complete_pinned_replay', mappings='complete'))
                record = dict(format=FORMAT, state='frozen', draft_sha256=expected_digest,
                    models=models, runtime=runtime_pins, snapshot_sha256=file_hash(stage / 'catalog.sqlite'),
                    validation_sha256=file_hash(stage / 'validation.json'))
            # Hold the same draft snapshot while checking and recording the
            # transition. Raw writes without edit-version increments also fail.
            db.execute('BEGIN IMMEDIATE')
            try:
                if database_hash(db) != expected_digest:
                    raise ValueError('Draft changed during freeze')
                identifier = _seal(stage, self.frozen, record, 'freeze.json', self.frozen_record)
            finally:
                db.rollback()
            return identifier
        finally:
            if stage.exists():
                shutil.rmtree(stage)

    def frozen_record(self, identifier):
        check_id(identifier)
        path = self.frozen / identifier
        record = read_json(path / 'freeze.json')
        if digest(record) != identifier or record['state'] != 'frozen' or record['format'] != FORMAT:
            raise ValueError('Invalid frozen manifest')
        if file_hash(path / 'catalog.sqlite') != record['snapshot_sha256'] or file_hash(path / 'validation.json') != record['validation_sha256']:
            raise ValueError('Frozen snapshot or validation was altered')
        return path, record

    def complete(self, frozen_id):
        path, record = self.frozen_record(frozen_id)
        if record['runtime'] != pins():
            raise ValueError('Freeze runtime pins do not match generator')
        stage = Path(tempfile.mkdtemp(prefix='.building-', dir=self.completed))
        try:
            shutil.copyfile(path / 'catalog.sqlite', stage / 'catalog.sqlite')
            shutil.copyfile(path / 'validation.json', stage / 'validation.json')
            for rel in record['runtime']:
                target = stage / 'runtime' / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(f.ROOT / rel, target)
            with closing(f.connect(stage / 'catalog.sqlite')) as db:
                models = membership(db)
                if models != record['models']:
                    raise ValueError('Release model membership changed')
                for model in models:
                    catalog = ConsumerCatalog(db, model['revision_id'])
                    base = stage / model['model_key']
                    base.mkdir()
                    contract = catalog.contract()
                    write_json(base / 'form.json', contract)
                    write_json(base / 'order.json', dict(format='catalog-order-v1', revision_id=model['revision_id'],
                        option_mappings=catalog.maps['option'], configuration_mappings=catalog.maps['configuration'],
                        interior_mappings=catalog.maps['interior'], presentation=catalog.model['presentation'],
                        source='confirmed_server_state', duplicate_codes='retain_contributing_option_identities'))
                    write_json(base / 'visualizer.json', dict(format='catalog-visualizer-v1', revision_id=model['revision_id'],
                        source='confirmed_installed_equipment', configuration_ids=sorted(catalog.ev.configs),
                        assets=[], coverage='art_not_bound'))
                    # All 32 configured defaults exercise generation from this
                    # snapshot. Exact JSON roundtrip is the artifact boundary.
                    for cfg in catalog.ev.configs:
                        catalog.project(catalog.ev.state(cfg), frozen_id)
                    if read_json(base / 'form.json') != contract:
                        raise ValueError('Form artifact roundtrip failed')
            artifacts = {str(p.relative_to(stage)): file_hash(p) for p in sorted(stage.rglob('*')) if p.is_file()}
            manifest = dict(format=FORMAT, state='completed', frozen_id=frozen_id, freeze=record, models=record['models'],
                default_model=next(r['model_key'] for r in record['models'] if r['is_default']),
                runtime=record['runtime'], artifacts=artifacts, media={'assets': [], 'coverage': 'art_not_bound'},
                comparison={'migration_baseline':'baselines/2026-09-06',
                            'target':'pinned_handoffs_and_accepted_owner_overlays',
                            'manufacturer_reconciliation':'separate_source_dispositions'},
                scope='local_consumer_release_not_canonical_cutover')
            if pins() != record['runtime']:
                raise ValueError('Generator changed during completion')
            identifier = _seal(stage, self.completed, manifest, 'manifest.json', self.verify)
            self.verify(identifier)
            return identifier
        finally:
            if stage.exists():
                shutil.rmtree(stage)

    def verify(self, identifier):
        check_id(identifier)
        path = self.completed / identifier
        return self._verify_path(path, identifier)

    def _verify_path(self, path, identifier):
        record = read_json(path / 'manifest.json')
        if digest(record) != identifier or record['state'] != 'completed' or record['format'] != FORMAT:
            raise ValueError('Invalid completed release manifest')
        actual = {str(p.relative_to(path)): file_hash(p) for p in path.rglob('*') if p.is_file() and p != path / 'manifest.json'}
        if any(p.is_symlink() for p in path.rglob('*')) or actual != record['artifacts']:
            raise ValueError('Missing, altered or unexpected release artifacts')
        frozen = record['freeze']
        if digest(frozen) != record['frozen_id'] or frozen['state'] != 'frozen' or frozen['format'] != FORMAT:
            raise ValueError('Invalid frozen release input')
        if frozen['runtime'] != record['runtime'] or frozen['models'] != record['models']:
            raise ValueError('Frozen membership or runtime mismatch')
        required = {'catalog.sqlite', 'validation.json'} | {'runtime/' + rel for rel in record['runtime']}
        required.update(m['model_key'] + '/' + role + '.json' for m in record['models'] for role in ('form','order','visualizer'))
        if set(record['artifacts']) != required:
            raise ValueError('Missing required consumer artifact')
        if record['artifacts']['catalog.sqlite'] != frozen['snapshot_sha256'] or record['artifacts']['validation.json'] != frozen['validation_sha256']:
            raise ValueError('Frozen snapshot or validation mismatch')
        if record['default_model'] != next(m['model_key'] for m in record['models'] if m['is_default']):
            raise ValueError('Invalid default model')
        for model in record['models']:
            for role in ('form','order','visualizer'):
                artifact = read_json(path / model['model_key'] / (role + '.json'))
                if artifact['revision_id'] != model['revision_id']:
                    raise ValueError('Consumer artifact revision mismatch')
        for rel, expected in record['runtime'].items():
            if record['artifacts'].get('runtime/' + rel) != expected:
                raise ValueError('Runtime pin mismatch')
        with closing(f.connect(path / 'catalog.sqlite')) as db:
            if membership(db) != record['models']:
                raise ValueError('Release membership mismatch')
        return record

    def backup(self, identifier, destination):
        self.verify(identifier)
        destination = Path(destination)
        if destination.exists():
            raise ValueError('Backup destination already exists')
        destination.parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix='.backup-', dir=destination.parent))
        try:
            shutil.copytree(self.completed / identifier, stage, dirs_exist_ok=True)
            self._verify_path(stage, identifier)
            os.rename(stage, destination)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
        return identifier

    def restore(self, source):
        source = Path(source)
        identifier = digest(read_json(source / 'manifest.json'))
        self._verify_path(source, identifier)
        stage = Path(tempfile.mkdtemp(prefix='.restore-', dir=self.completed))
        try:
            shutil.copytree(source, stage, dirs_exist_ok=True)
            self._verify_path(stage, identifier)
            destination = self.completed / identifier
            if destination.exists():
                self.verify(identifier)
            else:
                os.rename(stage, destination)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
        return identifier

    def pointer(self, channel='local'):
        with closing(sqlite3.connect(self.root / 'publication.sqlite')) as db, db:
            row = db.execute('SELECT release_id,version FROM publication_pointer WHERE channel=?', (channel,)).fetchone()
        return dict(release_id=row[0], version=row[1]) if row else dict(release_id=None, version=0)

    def publish(self, identifier, expected_version, channel='local'):
        if type(expected_version) is not int:
            raise ValueError('Expected publication version is required')
        with closing(sqlite3.connect(self.root / 'publication.sqlite')) as db, db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT release_id,version FROM publication_pointer WHERE channel=?', (channel,)).fetchone()
            previous, version = row if row else (None, 0)
            if version != expected_version:
                raise ValueError('Stale publication pointer')
            self.verify(identifier)
            db.execute('INSERT INTO publication_pointer VALUES (?,?,?) ON CONFLICT(channel) DO UPDATE SET release_id=excluded.release_id,version=excluded.version',
                       (channel, identifier, version + 1))
            db.execute('INSERT INTO publication_history VALUES (?,?,?,?)', (channel, version + 1, identifier, previous))
        return self.pointer(channel)

    def rollback(self, expected_version, channel='local'):
        with closing(sqlite3.connect(self.root / 'publication.sqlite')) as db, db:
            row = db.execute('SELECT previous_release_id FROM publication_history WHERE channel=? AND version=?', (channel, expected_version)).fetchone()
        if not row or not row[0]:
            raise ValueError('No previous completed release')
        return self.publish(row[0], expected_version, channel)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, default=f.ROOT / '.local/releases')
    commands = parser.add_subparsers(dest='command', required=True)
    prepare = commands.add_parser('prepare')
    prepare.add_argument('database', type=Path)
    freeze = commands.add_parser('freeze')
    freeze.add_argument('database', type=Path)
    freeze.add_argument('--expected-digest', required=True)
    for name in ('complete', 'verify'):
        commands.add_parser(name).add_argument('identifier')
    backup = commands.add_parser('backup')
    backup.add_argument('identifier')
    backup.add_argument('destination', type=Path)
    commands.add_parser('restore').add_argument('source', type=Path)
    publish = commands.add_parser('publish')
    publish.add_argument('identifier')
    for command in (publish, commands.add_parser('rollback')):
        command.add_argument('--expected-version', type=int, required=True)
        command.add_argument('--channel', default='local')
    commands.add_parser('pointer').add_argument('--channel', default='local')
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.database.exists():
            raise ValueError('Draft already exists')
        args.database.parent.mkdir(parents=True, exist_ok=True)
        with closing(f.connect(args.database)) as db:
            f.create_schema(db)
            import_behavior(db)
            import_mappings(db)
            print(database_hash(db))
        return
    store = ReleaseStore(args.store)
    if args.command == 'freeze':
        with closing(f.connect(args.database)) as db:
            print(store.freeze(db, args.expected_digest))
    elif args.command == 'publish':
        print(encode(store.publish(args.identifier, args.expected_version, args.channel)))
    elif args.command == 'rollback':
        print(encode(store.rollback(args.expected_version, args.channel)))
    elif args.command == 'backup':
        print(store.backup(args.identifier, args.destination))
    elif args.command == 'restore':
        print(store.restore(args.source))
    elif args.command == 'pointer':
        print(encode(store.pointer(args.channel)))
    else:
        print(getattr(store, args.command)(args.identifier))


if __name__ == '__main__':
    main()
