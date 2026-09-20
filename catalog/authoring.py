"""Bounded local option authoring in an explicit copy of a source-verified draft.

Authored drafts are deliberately outside the source-only release freeze contract.
No source imports, accepted overlays, workbook or release artifacts are modified.
"""
from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3

from catalog import foundation as f
from catalog.consumers import digest, encode, validate_mappings
from catalog.releases import database_hash, membership, validate_translation


def initialize(source, destination):
    """Validate a read-only source, then create a new, never-overwritten workspace."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    with closing(sqlite3.connect(source.as_uri() + '?mode=ro', uri=True)) as original:
        original.row_factory = sqlite3.Row
        original.execute('PRAGMA foreign_keys=ON')
        # Capture one consistent source snapshot before validating it.
        with closing(f.connect(':memory:')) as snapshot:
            original.backup(snapshot)
            validate_translation(snapshot)
            validate_mappings(snapshot)
            membership(snapshot)
            baseline = database_hash(snapshot)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb'):
                pass
            try:
                with closing(f.connect(destination)) as db:
                    snapshot.backup(db)
                    with db:
                        db.execute('''CREATE TABLE authoring_workspace (
                            singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                            baseline_sha256 TEXT NOT NULL, created_at TEXT NOT NULL)''')
                        db.execute('INSERT INTO authoring_workspace VALUES (1,?,?)',
                                   (baseline, datetime.now(timezone.utc).isoformat()))
                        db.execute('''CREATE TABLE authoring_change (
                            change_id INTEGER PRIMARY KEY, revision_id TEXT NOT NULL,
                            option_id TEXT NOT NULL, edit_version INTEGER NOT NULL,
                            saved_at TEXT NOT NULL, reason TEXT NOT NULL,
                            before_json TEXT NOT NULL, after_json TEXT NOT NULL,
                            UNIQUE(revision_id,edit_version),
                            FOREIGN KEY(revision_id,option_id) REFERENCES option(revision_id,id))''')
            except Exception:
                destination.unlink()
                raise
    return baseline


def open_workspace(path):
    path = Path(path).resolve()
    # mode=rw prevents a typo from creating an empty database.
    db = sqlite3.connect(path.as_uri() + '?mode=rw', uri=True)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        if not db.execute('SELECT 1 FROM authoring_workspace WHERE singleton=1').fetchone():
            raise ValueError('Not an initialized authoring workspace')
    except Exception:
        db.close()
        raise
    return db


def catalog(db):
    models = [dict(r) for r in db.execute('''SELECT m.model_key,m.name,r.revision_id,r.edit_version
        FROM model m JOIN model_year y USING(model_id) JOIN catalog_revision r USING(model_year_id)
        JOIN consumer_model c USING(revision_id) ORDER BY c.display_order''')]
    for model in models:
        model['options'] = [dict(r) for r in db.execute('''SELECT id,rpo,name,lifecycle FROM option
            WHERE revision_id=? ORDER BY name,id''', (model['revision_id'],))]
    return models


def detail(db, revision, option):
    row = db.execute('SELECT * FROM option WHERE revision_id=? AND id=?', (revision, option)).fetchone()
    mapping = db.execute('SELECT * FROM consumer_option WHERE revision_id=? AND option_id=?',
                         (revision, option)).fetchone()
    if row is None or mapping is None:
        raise ValueError('Unknown model-owned option')
    row, mapping = dict(row), dict(mapping)
    version, state = db.execute('SELECT edit_version,state FROM catalog_revision WHERE revision_id=?',
                               (revision,)).fetchone()
    if state != 'draft':
        raise ValueError('Only draft revisions can be edited')
    configurations = [dict(r) for r in db.execute('''SELECT c.id,c.body,c.trim,oc.status
        FROM option_configuration oc JOIN configuration c
        ON c.revision_id=oc.revision_id AND c.id=oc.configuration_id
        WHERE oc.revision_id=? AND oc.option_id=? ORDER BY c.chooser_order,c.id''', (revision, option))]
    rates = [dict(r) for r in db.execute('''SELECT r.id,r.condition_id,r.amount_minor,r.priority,s.configuration_id
        FROM option_rate r JOIN option_rate_configuration s
        ON s.revision_id=r.revision_id AND s.rate_id=r.id
        WHERE r.revision_id=? AND r.target_option_id=? ORDER BY r.priority,s.configuration_id''', (revision, option))]
    evidence = [dict(r) for r in db.execute('''SELECT d.source_path,a.locator,a.fragment_key
        FROM evidence_member e JOIN source_anchor a USING(anchor_id) JOIN source_document d USING(document_id)
        WHERE e.set_id=? ORDER BY d.source_path,a.locator,a.fragment_key''', (row['evidence_set_id'],))]
    history = [dict(r) for r in db.execute('''SELECT change_id,edit_version,saved_at,reason,before_json,after_json
        FROM authoring_change WHERE revision_id=? AND option_id=? ORDER BY change_id DESC''', (revision, option))]
    for change in history:
        change['before'] = json.loads(change.pop('before_json'))
        change['after'] = json.loads(change.pop('after_json'))
    basis = dict(db.execute('SELECT * FROM price_basis WHERE basis_id=?', (row['basis_id'],)).fetchone() or {})
    return dict(option=row, edit_version=version, configurations=configurations, contextual_rates=rates,
                evidence=evidence, history=history, currency=basis.get('currency'),
                etag=digest(dict(option=row, mapping=mapping, version=version)),
                price_editable=row['charge_mode'] == 'priced' and row['purchase_amount_minor'] is not None)


def preview(db, revision, option, etag, name, price, reason):
    current = detail(db, revision, option)
    if etag != current['etag']:
        raise ValueError('Stale edit: reload this option and review your changes again')
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 2048:
        raise ValueError('Name must contain 1–2048 characters')
    if not isinstance(reason, str) or not reason.strip() or len(reason.strip()) > 2000:
        raise ValueError('A change reason of 1–2000 characters is required')
    row = current['option']
    amount = row['purchase_amount_minor']
    if current['price_editable']:
        if not isinstance(price, str) or not re.fullmatch(r'\d{1,9}(?:\.\d{1,2})?', price):
            raise ValueError('Enter a nonnegative price with at most two decimal places')
        whole, _, fraction = price.partition('.')
        amount = int(whole) * 100 + int(fraction.ljust(2, '0'))
    elif price is not None:
        raise ValueError('This option has no editable base purchase price; charge semantics are preserved')
    before = dict(name=row['name'], purchase_amount_minor=row['purchase_amount_minor'])
    after = dict(name=name.strip(), purchase_amount_minor=amount)
    if before == after:
        raise ValueError('No changes to save')
    return dict(revision_id=revision, option_id=option, etag=etag, before=before, after=after,
                reason=reason.strip(), edit_version=current['edit_version'],
                configurations=current['configurations'], contextual_rates=current['contextual_rates'],
                currency=current['currency'])


def save(db, change):
    """Revalidate under the write lock; data, mapping, version and history are atomic."""
    if db.in_transaction:
        raise ValueError('Finish the current transaction before saving')
    with db:
        db.execute('BEGIN IMMEDIATE')
        amount = change['after']['purchase_amount_minor']
        price = None if amount is None else f'{amount // 100}.{amount % 100:02d}'
        reviewed = preview(db, change['revision_id'], change['option_id'], change['etag'],
                           change['after']['name'], price, change['reason'])
        if reviewed != change:
            raise ValueError('Preview changed; reload and review again')
        revision, option = change['revision_id'], change['option_id']
        db.execute('UPDATE option SET name=?,purchase_amount_minor=? WHERE revision_id=? AND id=?',
                   (change['after']['name'], amount, revision, option))
        mapping, = db.execute('SELECT presentation FROM consumer_option WHERE revision_id=? AND option_id=?',
                              (revision, option)).fetchone()
        presentation = json.loads(mapping)
        presentation['name'] = change['after']['name']
        db.execute('UPDATE consumer_option SET presentation=? WHERE revision_id=? AND option_id=?',
                   (encode(presentation), revision, option))
        db.execute('UPDATE catalog_revision SET edit_version=edit_version+1 WHERE revision_id=?', (revision,))
        validate_mappings(db)
        db.execute('''INSERT INTO authoring_change
            (revision_id,option_id,edit_version,saved_at,reason,before_json,after_json) VALUES (?,?,?,?,?,?,?)''',
            (revision, option, change['edit_version'] + 1, datetime.now(timezone.utc).isoformat(),
             change['reason'], encode(change['before']), encode(change['after'])))
    return detail(db, revision, option)
