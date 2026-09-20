"""Explicit draft acceptance and exact source-plus-edit replay for local releases."""
from contextlib import closing
from datetime import datetime, timezone
import json
import hashlib
from uuid import uuid4

from catalog import foundation as f
from catalog.consumers import digest, encode, validate_mappings
from catalog.releases import database_hash, validate_translation
from catalog import authoring_records as records

HISTORY = ('authoring_change','authoring_relationship_change','authoring_component_change','authoring_record_change')
METADATA = (*HISTORY,'authoring_intake','authoring_acceptance','authoring_workspace')


def prepare(db):
    with db:
        db.execute('''CREATE TABLE IF NOT EXISTS authoring_intake (
            intake_id TEXT PRIMARY KEY, saved_at TEXT NOT NULL, payload_json TEXT NOT NULL,
            disposition TEXT NOT NULL CHECK(disposition IN ('pending','rejected','deferred','accepted')),
            reviewer TEXT, reason TEXT, accepted_change_ids_json TEXT)''')
        db.execute('''CREATE TABLE IF NOT EXISTS authoring_acceptance (
            acceptance_id TEXT PRIMARY KEY, accepted_at TEXT NOT NULL, reviewer TEXT NOT NULL,
            reason TEXT NOT NULL, history_sha256 TEXT NOT NULL, product_sha256 TEXT NOT NULL,
            evidence_json TEXT NOT NULL, intake_ids_json TEXT NOT NULL)''')


def tables(db):
    return {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def events(db):
    result=[]
    for table in HISTORY:
        if table not in tables(db): continue
        for row in db.execute(f'SELECT * FROM "{table}"'):
            item=dict(row)
            result.append(dict(table=table,event=item,change_ref=table+':'+item['revision_id']+':'+str(item['edit_version'])))
    return sorted(result,key=lambda x:(x['event']['revision_id'],x['event']['edit_version'],x['table']))


def product_copy(db):
    copy=f.connect(':memory:')
    # Call only outside a write transaction. SQLite backup waits on a writer,
    # including the same connection; locked callers use serialization instead.
    copy.deserialize(db.serialize())
    copy.execute('PRAGMA foreign_keys=OFF')
    with copy:
        for table in METADATA:
            copy.execute(f'DROP TABLE IF EXISTS "{table}"')
    copy.execute('PRAGMA foreign_keys=ON')
    return copy


def product_hash(db):
    with closing(product_copy(db)) as copy:
        return database_hash(copy)


def legacy_operations(db,item,reverse=False):
    row=item['event'];table=item['table'];rev=row['revision_id']
    before=json.loads(row['before_json']);after=json.loads(row['after_json'])
    if table=='authoring_change':
        target='option';key=dict(revision_id=rev,id=row['option_id'])
    elif table=='authoring_relationship_change':
        target='acquisition';key=dict(revision_id=rev,id=row['acquisition_id'])
    else:
        target='component_rate';key=dict(revision_id=rev,component_id=row['component_id'],configuration_id=row['configuration_id'])
    current=records.lookup(db,target,key)
    expected=after if reverse else before
    if current is None or any(current[k]!=v for k,v in expected.items()):
        raise ValueError('Legacy history does not match '+target)
    ops=[dict(table=target,key=key,before=current|before,after=current|after)]
    if table=='authoring_change':
        mapping_key=dict(revision_id=rev,option_id=row['option_id'])
        mapping=records.lookup(db,'consumer_option',mapping_key)
        payload=json.loads(mapping['presentation'])
        if payload['name']!=expected['name']: raise ValueError('Legacy presentation history differs')
        ops.append(dict(table='consumer_option',key=mapping_key,
                        before=mapping|dict(presentation=encode(payload|dict(name=before['name']))),
                        after=mapping|dict(presentation=encode(payload|dict(name=after['name'])))))
    return ops


def validate_history_schema(db):
    from catalog import authoring, authoring_relationships, authoring_components
    def objects(connection):
        return {r['name']:(r['type'], ' '.join((r['sql'] or '').split())) for r in connection.execute(
            "SELECT type,name,sql FROM sqlite_master WHERE tbl_name LIKE 'authoring_%'")}
    with closing(f.connect(':memory:')) as expected:
        authoring.prepare(expected, 'schema-check')
        authoring_relationships.prepare(expected)
        authoring_components.prepare(expected)
        records.prepare(expected)
        prepare(expected)
        actual=objects(db);allowed=objects(expected)
        if any(name not in allowed or value!=allowed[name] for name,value in actual.items()):
            raise ValueError('Unexpected authoring schema')


def replay(db,require_acceptance=True):
    """Undo every logged edit, verify the pinned baseline, then replay in order.

    Raw row changes, missing/reordered history, schema changes and dangling
    evidence fail. Nothing is discarded from the actual draft or snapshot.
    """
    present=tables(db)
    validate_history_schema(db)
    if 'authoring_workspace' not in present: raise ValueError('Not an authoring workspace')
    unknown={t for t in present if t.startswith('authoring_')}-set(METADATA)
    if unknown: raise ValueError('Unknown authoring schema')
    history=events(db)
    expected_product=product_hash(db)
    accepted=None
    if require_acceptance:
        accepted=next((dict(r) for r in db.execute('SELECT * FROM authoring_acceptance ORDER BY accepted_at DESC,acceptance_id')
                       if r['history_sha256']==digest(history) and r['product_sha256']==expected_product),None)
        if accepted is None: raise ValueError('Unaccepted edits: review and accept the current draft before release')
    with closing(product_copy(db)) as check:
        check.execute('PRAGMA defer_foreign_keys=ON')
        normalized=[]
        for item in reversed(history):
            row=item['event'];revision=row['revision_id'];version=row['edit_version']
            current=check.execute('SELECT edit_version FROM catalog_revision WHERE revision_id=?',(revision,)).fetchone()
            if not current or current[0]!=version: raise ValueError('Missing or duplicate edit history')
            ops=json.loads(row['operations_json']) if item['table']=='authoring_record_change' else legacy_operations(check,item,True)
            for op in reversed(ops): records.patch_row(check,op,reverse=True)
            check.execute('UPDATE catalog_revision SET edit_version=edit_version-1 WHERE revision_id=?',(revision,))
            normalized.append(dict(**item,operations=ops))
        check.commit()
        baseline=db.execute('SELECT baseline_sha256 FROM authoring_workspace WHERE singleton=1').fetchone()[0]
        if database_hash(check)!=baseline: raise ValueError('Unrecorded changes or history drift from source baseline')
        validate_translation(check)
        for item in reversed(normalized):
            check.execute('PRAGMA defer_foreign_keys=ON')
            for op in item['operations']: records.patch_row(check,op)
            check.execute('UPDATE catalog_revision SET edit_version=edit_version+1 WHERE revision_id=?',(item['event']['revision_id'],))
            check.commit()
        validate_mappings(check)
        if database_hash(check)!=expected_product: raise ValueError('Accepted edits did not reproduce the catalog')
    intakes=[dict(r) for r in db.execute('SELECT * FROM authoring_intake ORDER BY intake_id')] if 'authoring_intake' in present else []
    for item in intakes:
        if digest(json.loads(item['payload_json']))!=item['intake_id']:
            raise ValueError('Intake evidence changed')
    history_by_ref={i['change_ref']:i for i in history}
    for receipt in db.execute('SELECT * FROM authoring_acceptance'):
        pinned=json.loads(receipt['evidence_json'])
        if digest(pinned['history'])!=receipt['history_sha256'] or any(history_by_ref.get(i['change_ref'])!=i for i in pinned['history']):
            raise ValueError('Previously accepted edit history changed')
        for source in pinned['intake']:
            if source!=next((i for i in intakes if i['intake_id']==source['intake_id']),None):
                raise ValueError('Previously accepted intake decision changed')
    if accepted:
        if json.loads(accepted['evidence_json'])['history']!=history:
            raise ValueError('Accepted history evidence changed')
        pinned_intakes=json.loads(accepted['evidence_json'])['intake']
        for iid in json.loads(accepted['intake_ids_json']):
            intake=next((i for i in intakes if i['intake_id']==iid),None)
            if intake is None or intake['disposition']!='accepted' or digest(json.loads(intake['payload_json']))!=iid:
                raise ValueError('Accepted intake evidence changed')
            if intake!=next((i for i in pinned_intakes if i['intake_id']==iid),None):
                raise ValueError('Accepted intake decision changed')
    return dict(format='catalog-reviewed-edits-v1',baseline_sha256=baseline,product_sha256=expected_product,
                history_sha256=digest(history),history=history,acceptance=accepted,intake=intakes)


def review(db):
    history=events(db)
    accepted=[dict(r) for r in db.execute('SELECT * FROM authoring_acceptance ORDER BY accepted_at DESC')]
    return dict(etag=database_hash(db),history=history,acceptances=accepted,
                intake=[dict(r) for r in db.execute('SELECT * FROM authoring_intake ORDER BY saved_at,intake_id')])


def text(value,label):
    if not isinstance(value,str) or not 1<=len(value.strip())<=4000:
        raise ValueError(label+' is required')
    return value.strip()


def stage(db,payload):
    """Stage one explicit interpreted assertion, preserving its exact evidence.

    Parsing a full guide remains separate: this input must state its scope and
    ambiguity. Staging never changes a product fact or accepts a correction.
    """
    if not isinstance(payload,dict) or set(payload)!={'source_sha256','source_path','locator','assertion','scope','comparison','ambiguity','coverage'}:
        raise ValueError('Intake requires a source hash/path, exact locator, assertion, scope, comparison, ambiguity and coverage')
    for key in payload: text(payload[key],key)
    sha=payload['source_sha256']
    if len(sha)!=64 or any(c not in '0123456789abcdef' for c in sha): raise ValueError('Source SHA-256 is required')
    if payload['comparison'] not in ('unchanged','added','changed','removed','ambiguous','conflicting'):
        raise ValueError('Unknown comparison classification')
    source=(f.ROOT / payload['source_path']).resolve()
    if not source.is_relative_to(f.ROOT) or not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=sha:
        raise ValueError('Source path must identify preserved repository evidence with the supplied hash')
    identifier=digest(payload)
    with db:
        db.execute('INSERT OR IGNORE INTO authoring_intake VALUES (?,?,?,\'pending\',NULL,NULL,NULL)',
                   (identifier,datetime.now(timezone.utc).isoformat(),encode(payload)))
    return dict(intake_id=identifier)


def disposition(db,identifier,decision,reviewer,reason):
    if decision not in ('rejected','deferred','pending'): raise ValueError('Accept an assertion with the reviewed catalog edit')
    reviewer=text(reviewer,'Reviewer');reason=text(reason,'Decision reason')
    with db:
        result=db.execute('UPDATE authoring_intake SET disposition=?,reviewer=?,reason=? WHERE intake_id=? AND disposition<>\'accepted\'',
                          (decision,reviewer,reason,identifier))
        if result.rowcount!=1: raise ValueError('Unknown or already accepted assertion')
    return review(db)


def preview(db,etag,reviewer,reason,intake_decisions=None):
    if database_hash(db)!=etag: raise ValueError('Stale acceptance: reload and review again')
    reviewer=text(reviewer,'Reviewer');reason=text(reason,'Acceptance reason')
    decisions=intake_decisions or []
    if not isinstance(decisions,list) or len(decisions)>100: raise ValueError('Too many intake decisions')
    report=replay(db,False)
    history=report['history']
    if not history: raise ValueError('No saved edits to accept')
    if any(r['history_sha256']==report['history_sha256'] and r['product_sha256']==report['product_sha256']
           for r in db.execute('SELECT * FROM authoring_acceptance')):
        raise ValueError('This exact draft has already been accepted')
    identifiers=set()
    for decision in decisions:
        iid=decision['intake_id']
        if iid in identifiers: raise ValueError('Duplicate intake decision')
        identifiers.add(iid)
        row=db.execute('SELECT * FROM authoring_intake WHERE intake_id=?',(iid,)).fetchone()
        if not row or row['disposition'] not in ('pending','deferred'): raise ValueError('Intake is unavailable for acceptance')
        text(decision['resolution'],'Evidence and ambiguity resolution')
        payload=json.loads(row['payload_json'])
        if digest(payload)!=iid: raise ValueError('Intake evidence hash changed')
        source=(f.ROOT/payload['source_path']).resolve()
        if not source.is_relative_to(f.ROOT) or not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=payload['source_sha256']:
            raise ValueError('Preserved intake source no longer matches its hash')
        if payload['comparison']=='removed' and payload['coverage']!='complete':
            raise ValueError('Removal requires complete relevant source coverage')
        change_ids={i['change_ref'] for i in history}
        if not decision.get('change_ids') or not set(decision['change_ids'])<=change_ids:
            raise ValueError('Link the intake assertion to its exact saved edit IDs')
    return dict(kind='acceptance',etag=etag,reviewer=reviewer,reason=reason,intake_decisions=decisions,
                report=report)


def accept(db,change):
    if db.in_transaction: raise ValueError('Finish the current transaction before acceptance')
    with db:
        db.execute('BEGIN IMMEDIATE')
        checked=preview(db,change['etag'],change['reviewer'],change['reason'],change['intake_decisions'])
        if checked!=change: raise ValueError('Acceptance changed; review again')
        report=change['report'];identifier=str(uuid4())
        for decision in change['intake_decisions']:
            db.execute('UPDATE authoring_intake SET disposition=\'accepted\',reviewer=?,reason=?,accepted_change_ids_json=? WHERE intake_id=?',
                       (change['reviewer'],decision['resolution'],encode(decision['change_ids']),decision['intake_id']))
        db.execute('INSERT INTO authoring_acceptance VALUES (?,?,?,?,?,?,?,?)',
                   (identifier,datetime.now(timezone.utc).isoformat(),change['reviewer'],change['reason'],
                    report['history_sha256'],report['product_sha256'],encode(dict(history=report['history'],intake=[dict(r) for r in db.execute("SELECT * FROM authoring_intake WHERE disposition='accepted' ORDER BY intake_id")])),
                    encode([r[0] for r in db.execute("SELECT intake_id FROM authoring_intake WHERE disposition='accepted' ORDER BY intake_id")])))
    return dict(accepted=True,acceptance_id=identifier,etag=database_hash(db))
