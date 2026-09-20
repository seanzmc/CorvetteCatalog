"""Local authoring of a model-owned component rate shared by interior leaves."""
from datetime import datetime, timezone
import json
import re

from catalog.consumers import ConsumerCatalog, digest, encode, validate_mappings


def prepare(db):
    with db:
        db.execute('''CREATE TABLE IF NOT EXISTS authoring_component_change (
            change_id INTEGER PRIMARY KEY, revision_id TEXT NOT NULL,
            component_id TEXT NOT NULL, configuration_id TEXT NOT NULL,
            edit_version INTEGER NOT NULL, saved_at TEXT NOT NULL, reason TEXT NOT NULL,
            before_json TEXT NOT NULL, after_json TEXT NOT NULL,
            UNIQUE(revision_id,edit_version),
            FOREIGN KEY(revision_id,component_id,configuration_id)
            REFERENCES component_rate(revision_id,component_id,configuration_id))''')


def rates(db, revision):
    # Sharing is an actual interior_part FK in this exact configuration, not a
    # matching code in another lane or a shared source PriceRef label.
    return [dict(r) for r in db.execute('''SELECT cr.*,c.kind,c.code,cfg.body,cfg.trim,
        count(*) AS member_count FROM component_rate cr
        JOIN component c ON c.revision_id=cr.revision_id AND c.id=cr.component_id
        JOIN configuration cfg ON cfg.revision_id=cr.revision_id AND cfg.id=cr.configuration_id
        JOIN interior_part p ON p.revision_id=cr.revision_id AND p.component_id=cr.component_id
        JOIN interior_configuration ic ON ic.revision_id=p.revision_id AND ic.interior_id=p.interior_id
            AND ic.configuration_id=cr.configuration_id
        WHERE cr.revision_id=? GROUP BY cr.revision_id,cr.component_id,cr.configuration_id
        HAVING count(*)>1 ORDER BY c.kind,c.code,cfg.chooser_order,cfg.id''', (revision,))]


def detail(db, revision, component, configuration):
    rate = next((r for r in rates(db, revision) if r['component_id'] == component
                 and r['configuration_id'] == configuration), None)
    if rate is None:
        raise ValueError('Choose an existing component rate shared by at least two interiors')
    version, state = db.execute('SELECT edit_version,state FROM catalog_revision WHERE revision_id=?', (revision,)).fetchone()
    if state != 'draft':
        raise ValueError('Only draft revisions can be edited')
    consumer = ConsumerCatalog(db, revision)
    members = []
    for row in db.execute('''SELECT p.interior_id,p.role FROM interior_part p
        JOIN interior_configuration ic ON ic.revision_id=p.revision_id AND ic.interior_id=p.interior_id
        WHERE p.revision_id=? AND p.component_id=? AND ic.configuration_id=? ORDER BY p.interior_id''',
                          (revision,component,configuration)):
        presentation = consumer.maps['interior'][row['interior_id']]['hierarchy']
        members.append(dict(row) | dict(label=' · '.join(str(presentation[k]) for k in
            ('trim_level','interior_seat_label','interior_leaf_label'))))
    history = [dict(r) for r in db.execute('''SELECT edit_version,saved_at,reason,before_json,after_json
        FROM authoring_component_change WHERE revision_id=? AND component_id=? AND configuration_id=?
        ORDER BY change_id DESC''', (revision,component,configuration))]
    for change in history:
        change['before'] = json.loads(change.pop('before_json'))
        change['after'] = json.loads(change.pop('after_json'))
    evidence = [dict(r) for r in db.execute('''SELECT d.source_path,a.locator,a.fragment_key FROM evidence_member e
        JOIN source_anchor a USING(anchor_id) JOIN source_document d USING(document_id)
        WHERE e.set_id=? ORDER BY d.source_path,a.locator,a.fragment_key''', (rate['evidence_set_id'],))]
    ev = consumer.ev
    etag = digest(dict(rate=rate, version=version, members=members, rows=ev.rows, bases=ev.bases,
                       scopes={t: sorted(s) for t,s in ev.scopes.items()}))
    return dict(rate=rate, members=members, edit_version=version, history=history,
                evidence=evidence, currency=ev.bases[rate['basis_id']]['currency'], etag=etag)


def outcomes(db, revision, component, configuration, members):
    catalog = ConsumerCatalog(db, revision)
    ev = catalog.ev
    initial = ev.state(configuration)
    result = []
    for member in members:
        state = ev.transition(initial, 'interior', member['interior_id'])
        charges = [c for c in state.charges if c.owner_kind == 'component' and c.owner_id == component]
        if len(charges) != 1 or state.interior_id != member['interior_id']:
            raise ValueError('Cannot verify a single shared component charge for ' + member['interior_id'])
        result.append(dict(interior_id=member['interior_id'], label=member['label'],
                           amount_minor=charges[0].amount_minor, total_minor=state.total_minor,
                           resolved=sorted(state.resolved), installed=sorted(state.installed),
                           issues=list(state.issues)))
    return result


def preview(db, revision, component, configuration, etag, price, reason):
    current = detail(db, revision, component, configuration)
    if current['etag'] != etag:
        raise ValueError('Stale edit: reload this shared rate and review again')
    if not isinstance(price,str) or not re.fullmatch(r'\d{1,9}(?:\.\d{1,2})?',price):
        raise ValueError('Enter a nonnegative price with at most two decimal places')
    if not isinstance(reason,str) or not 1 <= len(reason.strip()) <= 2000:
        raise ValueError('A change reason of 1–2000 characters is required')
    whole, _, fraction = price.partition('.')
    amount = int(whole)*100 + int(fraction.ljust(2,'0'))
    before = dict(amount_minor=current['rate']['amount_minor'])
    after = dict(amount_minor=amount)
    if before == after:
        raise ValueError('No changes to save')
    original = outcomes(db,revision,component,configuration,current['members'])
    db.execute('SAVEPOINT component_preview')
    try:
        db.execute('UPDATE component_rate SET amount_minor=? WHERE revision_id=? AND component_id=? AND configuration_id=?',
                   (amount,revision,component,configuration))
        candidate = outcomes(db,revision,component,configuration,current['members'])
        delta = amount-before['amount_minor']
        for old, new in zip(original,candidate):
            if (new['total_minor']-old['total_minor'] != delta or new['amount_minor'] != amount
                    or any(new[k] != old[k] for k in ('interior_id','resolved','installed','issues'))):
                raise ValueError('Shared price edit changed more than its component charge')
    finally:
        db.execute('ROLLBACK TO component_preview')
        db.execute('RELEASE component_preview')
    return dict(kind='component',revision_id=revision,component_id=component,configuration_id=configuration,
                etag=etag,edit_version=current['edit_version'],reason=reason.strip(),before=before,after=after,
                currency=current['currency'],body=current['rate']['body'],trim=current['rate']['trim'],
                code=current['rate']['code'],component_kind=current['rate']['kind'],
                before_outcomes=original,after_outcomes=candidate)


def save(db, change):
    if db.in_transaction:
        raise ValueError('Finish the current transaction before saving')
    with db:
        db.execute('BEGIN IMMEDIATE')
        amount = change['after']['amount_minor']
        reviewed = preview(db,change['revision_id'],change['component_id'],change['configuration_id'],
                           change['etag'],f'{amount // 100}.{amount % 100:02d}',change['reason'])
        if reviewed != change:
            raise ValueError('Preview changed; reload and review again')
        db.execute('UPDATE component_rate SET amount_minor=? WHERE revision_id=? AND component_id=? AND configuration_id=?',
                   (amount,change['revision_id'],change['component_id'],change['configuration_id']))
        db.execute('UPDATE catalog_revision SET edit_version=edit_version+1 WHERE revision_id=?', (change['revision_id'],))
        validate_mappings(db)
        db.execute('''INSERT INTO authoring_component_change
            (revision_id,component_id,configuration_id,edit_version,saved_at,reason,before_json,after_json)
            VALUES (?,?,?,?,?,?,?,?)''',
            (change['revision_id'],change['component_id'],change['configuration_id'],change['edit_version']+1,
             datetime.now(timezone.utc).isoformat(),change['reason'],encode(change['before']),encode(change['after'])))
    return detail(db,change['revision_id'],change['component_id'],change['configuration_id'])
