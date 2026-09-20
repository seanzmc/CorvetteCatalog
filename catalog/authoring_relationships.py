"""Reviewed ownership edits for direct option inclusions in local authoring drafts."""
from datetime import datetime, timezone
import json

from catalog.consumers import ConsumerCatalog, digest, encode, validate_mappings
from catalog.evaluator import Evaluator, EvaluationError


def prepare(db):
    # Additive local history; old option workspaces need no reinitialization.
    with db:
        db.execute('''CREATE TABLE IF NOT EXISTS authoring_relationship_change (
            change_id INTEGER PRIMARY KEY, revision_id TEXT NOT NULL,
            acquisition_id TEXT NOT NULL, edit_version INTEGER NOT NULL,
            saved_at TEXT NOT NULL, reason TEXT NOT NULL,
            before_json TEXT NOT NULL, after_json TEXT NOT NULL,
            UNIQUE(revision_id,edit_version), FOREIGN KEY(revision_id,acquisition_id)
            REFERENCES acquisition(revision_id,id))''')


def relationships(db, revision):
    # Only one positive option member in one conjunctive clause is editable.
    return [dict(r) for r in db.execute('''SELECT a.*,s.id AS source_option_id,
        s.rpo AS source_rpo,s.name AS source_name,t.rpo AS target_rpo,t.name AS target_name
        FROM acquisition a JOIN condition c ON c.revision_id=a.revision_id AND c.id=a.condition_id
        JOIN condition_clause cc ON cc.revision_id=c.revision_id AND cc.condition_id=c.id
        JOIN condition_member cm ON cm.revision_id=cc.revision_id AND cm.condition_id=cc.condition_id AND cm.clause_id=cc.clause_id
        JOIN option s ON s.revision_id=cm.revision_id AND s.id=cm.option_id
        JOIN option t ON t.revision_id=a.revision_id AND t.id=a.target_option_id
        WHERE a.revision_id=? AND a.origin_kind='included' AND c.mode='conjunction'
        AND cc.mode='any_present' AND cm.state='resolved_selection'
        AND (SELECT count(*) FROM condition_clause x WHERE x.revision_id=c.revision_id AND x.condition_id=c.id)=1
        AND (SELECT count(*) FROM condition_member x WHERE x.revision_id=c.revision_id AND x.condition_id=c.id)=1
        ORDER BY s.name,t.name,a.id''', (revision,))]


def detail(db, revision, relationship):
    row = next((r for r in relationships(db, revision) if r['id'] == relationship), None)
    if row is None:
        raise ValueError('Choose an existing direct option inclusion')
    version, state = db.execute('SELECT edit_version,state FROM catalog_revision WHERE revision_id=?', (revision,)).fetchone()
    if state != 'draft':
        raise ValueError('Only draft revisions can be edited')
    ev = Evaluator(db, revision)
    scopes = [dict(r) for r in db.execute('''SELECT c.* FROM acquisition_configuration s
        JOIN configuration c ON c.revision_id=s.revision_id AND c.id=s.configuration_id
        WHERE s.revision_id=? AND s.acquisition_id=? ORDER BY c.chooser_order,c.id''', (revision, relationship))]
    if not scopes:
        raise ValueError('This relationship has no configuration scope')
    history = [dict(r) for r in db.execute('''SELECT edit_version,saved_at,reason,before_json,after_json
        FROM authoring_relationship_change WHERE revision_id=? AND acquisition_id=? ORDER BY change_id DESC''', (revision, relationship))]
    for h in history:
        h['before'] = json.loads(h.pop('before_json'))
        h['after'] = json.loads(h.pop('after_json'))
    evidence = [dict(r) for r in db.execute('''SELECT d.source_path,a.locator,a.fragment_key FROM evidence_member e
        JOIN source_anchor a USING(anchor_id) JOIN source_document d USING(document_id)
        WHERE e.set_id=? ORDER BY d.source_path,a.locator,a.fragment_key''', (row['evidence_set_id'],))]
    # Include executable dependencies, not just the changed row, for stale reviews.
    etag = digest(dict(row=row, version=version, rows=ev.rows, bases=ev.bases,
                       scopes={t: sorted(s) for t, s in ev.scopes.items()}))
    return dict(relationship=row, edit_version=version, configurations=scopes,
                history=history, evidence=evidence, etag=etag)


def outcomes(db, revision, row, scopes):
    catalog = ConsumerCatalog(db, revision)
    ev = catalog.ev
    result = []
    for cfg in scopes:
        try:
            initial = ev.state(cfg['id'])
            purchased = ev.transition(initial, 'select', row['target_option_id'])
            if row['target_option_id'] not in purchased.intent:
                raise EvaluationError('The included option must support independent purchase')
            selected = ev.transition(purchased, 'select', row['source_option_id'])
            if row['source_option_id'] not in selected.resolved or not any(
                    c.source_id == row['id'] and c.option_id == row['target_option_id'] for c in selected.causes):
                raise EvaluationError('The source and its included target must both be observed')
            removed = ev.transition(selected, 'remove', row['source_option_id'])
            result.append(dict(configuration_id=cfg['id'], body=cfg['body'], trim=cfg['trim'],
                               purchased=catalog.project(purchased, 'local-authoring'),
                               selected=catalog.project(selected, 'local-authoring'),
                               removed=catalog.project(removed, 'local-authoring')))
        except EvaluationError as error:
            raise ValueError(f"Cannot verify inclusion in {cfg['body']} {cfg['trim']}: {error}") from error
    return result


def preview(db, revision, relationship, etag, intent_policy, reason):
    current = detail(db, revision, relationship)
    if current['etag'] != etag:
        raise ValueError('Stale edit: reload this relationship and review again')
    if not isinstance(reason, str) or not 1 <= len(reason.strip()) <= 2000:
        raise ValueError('A change reason of 1–2000 characters is required')
    row = current['relationship']
    if intent_policy not in ('preserve_prior', 'absorb_prior'):
        raise ValueError('Choose preserve prior purchase or absorb prior purchase')
    if row['intent_policy'] == intent_policy:
        raise ValueError('No changes to save')
    before = dict(intent_policy=row['intent_policy'])
    after = dict(intent_policy=intent_policy)
    original = outcomes(db, revision, row, current['configurations'])
    # Exercise the actual evaluator, then discard the candidate even on failure.
    db.execute('SAVEPOINT relationship_preview')
    try:
        db.execute('UPDATE acquisition SET intent_policy=? WHERE revision_id=? AND id=?', (intent_policy, revision, relationship))
        candidate = outcomes(db, revision, row | {'intent_policy': intent_policy}, current['configurations'])
    finally:
        db.execute('ROLLBACK TO relationship_preview')
        db.execute('RELEASE relationship_preview')
    return dict(kind='relationship', revision_id=revision, acquisition_id=relationship, etag=etag,
                edit_version=current['edit_version'], reason=reason.strip(), before=before, after=after,
                source=dict(id=row['source_option_id'], rpo=row['source_rpo'], name=row['source_name']),
                target=dict(id=row['target_option_id'], rpo=row['target_rpo'], name=row['target_name']),
                before_outcomes=original, after_outcomes=candidate)


def save(db, change):
    if db.in_transaction:
        raise ValueError('Finish the current transaction before saving')
    with db:
        db.execute('BEGIN IMMEDIATE')
        reviewed = preview(db, change['revision_id'], change['acquisition_id'], change['etag'],
                           change['after']['intent_policy'], change['reason'])
        if reviewed != change:
            raise ValueError('Preview changed; reload and review again')
        db.execute('UPDATE acquisition SET intent_policy=? WHERE revision_id=? AND id=?',
                   (change['after']['intent_policy'], change['revision_id'], change['acquisition_id']))
        db.execute('UPDATE catalog_revision SET edit_version=edit_version+1 WHERE revision_id=?', (change['revision_id'],))
        validate_mappings(db)
        db.execute('''INSERT INTO authoring_relationship_change
            (revision_id,acquisition_id,edit_version,saved_at,reason,before_json,after_json) VALUES (?,?,?,?,?,?,?)''',
            (change['revision_id'], change['acquisition_id'], change['edit_version'] + 1,
             datetime.now(timezone.utc).isoformat(), change['reason'], encode(change['before']), encode(change['after'])))
    return detail(db, change['revision_id'], change['acquisition_id'])
