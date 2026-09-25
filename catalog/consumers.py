"""Revision-owned consumer mappings and confirmation-gated build sessions.

Consumers never evaluate client totals or commit client-supplied candidates.
Retained IDs remain lane-local. New offering keys use their accepted record ID.
"""
import hashlib
import json
import secrets
from dataclasses import asdict

from catalog import foundation as f
from catalog import artwork
from catalog.evaluator import Evaluator, EvaluationError, Preview, Session

FORMAT = 'catalog-consumers-v1'
TABLES = ('consumer_model', 'consumer_option', 'consumer_option_context',
          'consumer_configuration', 'consumer_interior')


# One reusable encoder: identical output to json.dumps with these arguments,
# without constructing a new encoder on every call.
encode = json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def plain(value):
    if isinstance(value, (set, frozenset)):
        return sorted(plain(x) for x in value)
    if isinstance(value, (tuple, list)):
        return [plain(x) for x in value]
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    return value


def active(value):
    return str(value).lower() == 'true'


def create_schema(db):
    # Source presentation is retained as named fields in each typed mapping.
    # JSON payloads contain copy/order/hierarchy, never executable product rules.
    db.execute('''CREATE TABLE IF NOT EXISTS consumer_model (
        revision_id TEXT PRIMARY KEY REFERENCES catalog_revision(revision_id),
        registry_key TEXT NOT NULL, legacy_alias TEXT,
        display_order INTEGER NOT NULL, is_default INTEGER NOT NULL,
        presentation TEXT NOT NULL, source_sha256 TEXT NOT NULL, policy_sha256 TEXT NOT NULL)''')
    for kind in ('option', 'configuration', 'interior'):
        db.execute(f'''CREATE TABLE IF NOT EXISTS consumer_{kind} (
            revision_id TEXT NOT NULL, {kind}_id TEXT NOT NULL, consumer_key TEXT NOT NULL,
            presentation TEXT NOT NULL, source_locator TEXT NOT NULL,
            PRIMARY KEY(revision_id, {kind}_id), UNIQUE(revision_id, consumer_key),
            FOREIGN KEY(revision_id, {kind}_id) REFERENCES "{kind}"(revision_id,id))''')
    db.execute('''CREATE TABLE IF NOT EXISTS consumer_option_context (
        revision_id TEXT NOT NULL, option_id TEXT NOT NULL, configuration_id TEXT NOT NULL,
        presentation TEXT NOT NULL, PRIMARY KEY(revision_id,option_id,configuration_id),
        FOREIGN KEY(revision_id,option_id) REFERENCES consumer_option(revision_id,option_id),
        FOREIGN KEY(revision_id,configuration_id) REFERENCES consumer_configuration(revision_id,configuration_id))''')


def import_mappings(db, source_dir=f.ROOT / 'docs'):
    """Populate mappings atomically from pinned lane handoffs and accepted overlays."""
    with db:
        create_schema(db)
        for lane in f.LANES:
            path = source_dir / (lane + '-structured-records.json')
            raw = path.read_bytes()
            data = json.loads(raw)
            rows, roles = data['baseline_rows'], data['sheet_roles']
            review_path = source_dir / (lane + '-owner-decisions.json')
            review = json.loads(review_path.read_bytes())['owner_review']
            for input_path in (path, review_path, source_dir / 'compatibility-notice-policy.json'):
                pinned = db.execute('SELECT content_sha256 FROM source_document WHERE source_path=?',
                                    ('docs/' + input_path.name,)).fetchone()
                if not pinned or pinned[0] != hashlib.sha256(input_path.read_bytes()).hexdigest():
                    raise ValueError('Unpinned mapping input: ' + input_path.name)
            revision, = db.execute('''SELECT revision_id FROM catalog_revision JOIN model_year USING(model_year_id)
                JOIN model USING(model_id) WHERE model_key=?''', (data['model_key'],)).fetchone()
            if db.execute('SELECT 1 FROM consumer_model WHERE revision_id=?', (revision,)).fetchone():
                raise ValueError('Mappings already populated; create a fresh draft')
            promotion, = rows['model_registry_promotion']
            meta = {k: rows[k] for k in ('model_master', 'runtime_steps', 'section_master', 'section_presentation',
                    'order_summary_sections', 'step_order_summary_map', 'context_section_master', 'context_choice_copy')}
            # Card photos (model, body style, option) are presentation only; a
            # missing image never changes availability or price.
            meta['asset_map'] = [r for r in rows['asset_map'] if active(r['active'])]
            policy_hash = hashlib.sha256((source_dir / 'compatibility-notice-policy.json').read_bytes()).hexdigest()
            db.execute('INSERT INTO consumer_model VALUES (?,?,?,?,?,?,?,?)',
                       (revision, promotion['registry_key'], promotion['legacy_alias'], promotion['display_order'],
                        int(active(promotion['default_model'])), encode(meta), hashlib.sha256(raw).hexdigest(), policy_hash))
            for cfg in rows['variant_master']:
                db.execute('INSERT INTO consumer_configuration VALUES (?,?,?,?,?)',
                           (revision, cfg['variant_id'], cfg['variant_id'], encode(cfg),
                            f'baseline_rows/variant_master/_row={cfg["_row"]}'))
            scopes = {r['interior_id']: r for r in rows['model_interior_scope']}
            for interior in rows[roles['interiors']]:
                iid = interior['interior_id']
                if db.execute('SELECT 1 FROM interior WHERE revision_id=? AND id=?', (revision, iid)).fetchone():
                    payload = {'source': interior, 'hierarchy': scopes[iid],
                               'components': [r for r in rows['interior_components'] if r['interior_id'] == iid]}
                    db.execute('INSERT INTO consumer_interior VALUES (?,?,?,?,?)',
                               (revision, iid, iid, encode(payload), f'baseline_rows/{roles["interiors"]}/_row={interior["_row"]}'))
            originals = {r['option_id']: r for r in rows[roles['options']]}
            additions = {r['rpo']: r for r in review['accepted_additions']}
            sections = {r['section_id']: r for r in rows['section_master']}
            views = {r['section_id']: r for r in rows['section_presentation'] if active(r['active'])}
            summary = {r['step_key']: r['section_key'] for r in rows['step_order_summary_map'] if active(r['active'])}
            overrides = {(r['option_id'], r['variant_id']): r for r in rows[roles['variant_overrides']] if active(r['active'])}
            equipment = {r[0] for r in db.execute('SELECT option_id FROM option_configuration WHERE revision_id=? AND status="standard"', (revision,))}
            for removed, replacement in db.execute('SELECT removed_option_id,replacement_option_id FROM equipment_substitution WHERE revision_id=?', (revision,)):
                equipment.update((removed, replacement))
            for opt in db.execute('SELECT * FROM option WHERE revision_id=? ORDER BY id', (revision,)).fetchall():
                oid, code = opt['id'], opt['rpo']
                if oid in originals:
                    source = originals[oid]
                    key = oid
                    locator = f'baseline_rows/{roles["options"]}/_row={source["_row"]}'
                else:
                    addition = additions[code]
                    # These destinations are evidenced by the accepted product
                    # family and existing lane-specific stripe/interior sections.
                    sid = {'DTC': 'sec_stri_001', 'SAI': 'sec_lpoi_001'}[code]
                    if sid not in sections:
                        raise ValueError('Missing accepted-addition destination: ' + lane + '/' + code)
                    source = dict(section_id=sid, display_order=0, description=addition['guide_disclosure'], detail_raw=None, display_behavior=None)
                    key = addition['record_id']
                    locator = 'owner_review/accepted_additions/record_id=' + key
                payload = {k: source.get(k) for k in ('section_id', 'display_order', 'description', 'detail_raw', 'display_behavior')}
                payload.update(name=opt['name'], rpo=code,
                               projection='installed_equipment' if oid in equipment else 'resolved_selection',
                               emit_code=bool(code and code != 'CFX' and opt['lifecycle'] != 'retired'))
                if lane == 'grand-sport-x' and code == 'HP1':
                    target = review['model_policies']['hp1_target']
                    payload.update(name=target['title'], description=target['description'], detail_raw=None)
                db.execute('INSERT INTO consumer_option VALUES (?,?,?,?,?)', (revision, oid, key, encode(payload), locator))
                for cfg in rows['variant_master']:
                    cid = cfg['variant_id']
                    override = overrides.get((oid, cid), {})
                    sid = override.get('section_id') or source['section_id']
                    section, view = sections[sid], views.get(sid, {})
                    step = view.get('step_key') or section['step_key']
                    context = dict(section_id=sid, section_label=view.get('display_label') or section['section_name'],
                        section_order=view.get('section_display_order') if view.get('section_display_order') is not None else section['display_order'],
                        step_key=step, summary_section_id=summary.get(step),
                        display_behavior=override.get('display_behavior') or source.get('display_behavior'),
                        standard_equipment_group_type=view.get('standard_equipment_group_type'))
                    if step != 'standard_equipment' and context['summary_section_id'] is None:
                        raise ValueError('Unmapped summary route: ' + lane + '/' + sid)
                    db.execute('INSERT INTO consumer_option_context VALUES (?,?,?,?)', (revision, oid, cid, encode(context)))
        validate_mappings(db)


def validate_mappings(db):
    f.validate(db)
    for kind in ('option', 'configuration', 'interior'):
        missing = db.execute(f'''SELECT revision_id,id FROM "{kind}" EXCEPT
            SELECT revision_id,{kind}_id FROM consumer_{kind}''').fetchone()
        if missing:
            raise ValueError('Missing consumer mapping: ' + str(tuple(missing)))
    missing = db.execute('''SELECT revision_id,option_id,configuration_id FROM option_configuration EXCEPT
        SELECT revision_id,option_id,configuration_id FROM consumer_option_context''').fetchone()
    if missing:
        raise ValueError('Missing option context mapping')
    for rev, in db.execute('SELECT revision_id FROM catalog_revision'):
        contract = ConsumerCatalog(db, rev).contract()
        summary = {r['section_key'] for r in contract['presentation']['order_summary_sections'] if active(r['active'])}
        for item in contract['option_contexts']:
            if item['summary_section_id'] is not None and item['summary_section_id'] not in summary:
                raise ValueError('Invalid summary destination')
        Evaluator(db, rev)  # Also checks the supported common transaction policy.


class ConsumerCatalog:
    def __init__(self, db, revision, artwork_manifest=None):
        self.revision = revision
        self.ev = Evaluator(db, revision)
        self.model = dict(db.execute('SELECT * FROM consumer_model WHERE revision_id=?', (revision,)).fetchone())
        self.model['presentation'] = json.loads(self.model['presentation'])
        self.model_key = db.execute('''SELECT model_key FROM catalog_revision
            JOIN model_year USING(model_year_id) JOIN model USING(model_id) WHERE revision_id=?''', (revision,)).fetchone()[0]
        self.maps = {}
        for kind in ('option', 'configuration', 'interior'):
            self.maps[kind] = {r[kind + '_id']: dict(key=r['consumer_key'], **json.loads(r['presentation']))
                               for r in db.execute(f'SELECT * FROM consumer_{kind} WHERE revision_id=?', (revision,))}
        self.components = {r['id']: dict(r) for r in db.execute('SELECT * FROM component WHERE revision_id=?', (revision,))}
        self.contexts = {(r['option_id'], r['configuration_id']): json.loads(r['presentation'])
                         for r in db.execute('SELECT * FROM consumer_option_context WHERE revision_id=?', (revision,))}
        self.artwork = artwork.catalog_contract(self, artwork_manifest if artwork_manifest is not None else artwork.load_collection())

    def contract(self):
        return dict(format=FORMAT, revision_id=self.revision, registry_key=self.model['registry_key'],
            display_order=self.model['display_order'],
            presentation=self.model['presentation'], configurations=self.maps['configuration'], interiors=self.maps['interior'],
            options={oid: {**self.maps['option'][oid], 'lifecycle': row['lifecycle'], 'customer_selectable': bool(row['customer_selectable'])}
                     for oid, row in self.ev.options.items()},
            option_contexts=[dict(option_id=oid, configuration_id=cid, status=self.ev.statuses[oid,cid], **data)
                             for (oid, cid), data in sorted(self.contexts.items())])

    def option(self, oid):
        row = self.maps['option'][oid]
        return dict(option_id=oid, consumer_key=row['key'], rpo=row['rpo'], label=row['name'])

    def issue_label(self, issue, configuration):
        if issue == 'missing_required_interior':
            return 'Choose an interior'
        if issue.startswith('missing_group:'):
            gid = issue.split(':', 1)[1]
            labels = sorted({self.contexts[oid, configuration]['section_label'] for oid in self.ev.members[gid]})
            return 'Choose an option in ' + ', '.join(labels)
        return issue

    def owner_label(self, charge):
        kind, identifier = charge['owner_kind'], charge['owner_id']
        if kind == 'option':
            return self.option(identifier)['label']
        if kind == 'configuration':
            return self.maps['configuration'][identifier]['display_name']
        component = self.components[identifier]
        return component['kind'].replace('_', ' ').title() + ' ' + component['code']

    def project(self, state, release_id):
        def options(ids):
            return [self.option(oid) for oid in sorted(ids)]
        codes, items = [], []
        for oid in sorted(state.resolved):
            mapped = self.maps['option'][oid]
            if mapped['projection'] == 'installed_equipment' and oid not in state.installed:
                continue
            item = {**self.option(oid), **self.contexts[oid, state.configuration_id]}
            if item['summary_section_id'] is not None:
                items.append(item)
            if mapped['emit_code']:
                codes.append(self.option(oid))
        items.sort(key=lambda r: (r['section_order'] or 0, r['section_id'], self.maps['option'][r['option_id']]['display_order'] or 0, r['consumer_key']))
        interior = self.maps['interior'].get(state.interior_id)
        if interior is not None:
            owned = self.ev.interiors[state.interior_id]
            parts = [p for p in self.ev.rows['interior_part'] if p['interior_id']==state.interior_id]
            interior = dict(interior, configured_code=owned['code'], seat_option=self.option(owned['seat_option_id']),
                configured_components=[dict(role=p['role'], option=self.option(p['option_id']) if p['option_id'] else None,
                    component=self.components[p['component_id']] if p['component_id'] else None)
                    for p in sorted(parts,key=lambda p:(p['display_order'],p['part_key']))])
        common = dict(release_id=release_id, revision_id=self.revision, configuration_id=state.configuration_id)
        return dict(**common, intent=list(state.intent), interior_id=state.interior_id,
            selected_interior=interior,
            resolved=options(state.resolved), installed_equipment=options(state.installed),
            informational_standard_equipment=options(state.standard), order_codes=codes, summary_items=items,
            charges=[dict(**asdict(c), label=self.owner_label(asdict(c))) for c in state.charges], total_minor=state.total_minor,
            missing_requirements=[self.issue_label(i, state.configuration_id) for i in state.issues if i != 'partial_catalog_not_submission_ready'],
            content=[asdict(c) for c in state.content], issues=list(state.issues),
            visualizer=dict(**common, installed_option_ids=sorted(state.installed), interior_id=state.interior_id,
                            content=[asdict(c) for c in state.content], **artwork.project(self, state)))

    def cards(self, state):
        cards = []
        for oid, opt in self.ev.options.items():
            if opt['lifecycle'] == 'retired':
                continue
            if self.contexts[oid, state.configuration_id]['display_behavior'] in ('hidden', 'auto_only'):
                continue
            selected = oid in state.resolved
            reason, conflict, delta_minor = '', False, None
            try:
                candidate = self.ev.transition(state, 'remove' if selected else 'select', oid)
                delta_minor = candidate.total_minor - state.total_minor
                conflict = bool(state.resolved - candidate.resolved or set(state.intent) - set(candidate.intent)
                                or state.interior_id != candidate.interior_id)
            except EvaluationError as error:
                reason = 'Unavailable at this time' if opt['lifecycle'] == 'factory_unavailable' else str(error)
            view = self.maps['option'][oid]
            cards.append(dict(**self.option(oid), **self.contexts[oid, state.configuration_id],
                              description=view['description'], detail_raw=view['detail_raw'],
                              selected=selected, selectable=not bool(reason), conflict=conflict, reason=reason, delta_minor=delta_minor,
                              display_order=view['display_order'] or 0))
        cards.sort(key=lambda r: (r['section_order'] or 0, r['section_id'], r['display_order'], r['consumer_key']))
        interiors = [dict(interior_id=iid, label=' › '.join(json.loads(
                         self.maps['interior'][iid]['hierarchy']['interior_hierarchy_levels'])))
                     for iid in self.ev.interiors if self.ev.interiors[iid]['enabled'] and (iid, state.configuration_id) in self.ev.interior_scopes]
        return dict(options=cards, interiors=interiors)

    def warning(self, preview, release_id, action, target):
        before, after = preview.before, preview.candidate
        def names(ids):
            return [self.option(oid) for oid in sorted(ids)]
        charges_before = {(c.owner_kind, c.owner_id): asdict(c) for c in before.charges}
        charges_after = {(c.owner_kind, c.owner_id): asdict(c) for c in after.charges}
        def causes(state):
            return {encode(plain(asdict(c))): plain(asdict(c)) for c in state.causes}
        cb, ca = causes(before), causes(after)
        changes = dict(added=names(preview.added), removed=names(preview.removed),
            removed_independent_ownership=names(preview.removed_intent),
            added_independent_ownership=names(set(after.intent)-set(before.intent)),
            interior={'before': before.interior_id, 'after': after.interior_id},
            installed_removed=names(before.installed-after.installed), installed_added=names(after.installed-before.installed),
            causes_removed=[cb[k] for k in sorted(cb.keys()-ca.keys())], causes_added=[ca[k] for k in sorted(ca.keys()-cb.keys())],
            charge_changes=[{'before': charges_before.get(k), 'after': charges_after.get(k)}
                            for k in sorted(charges_before.keys() | charges_after.keys()) if charges_before.get(k) != charges_after.get(k)],
            content_before=[asdict(c) for c in before.content], content_after=[asdict(c) for c in after.content],
            total_before_minor=before.total_minor, total_after_minor=after.total_minor,
            delta_minor=after.total_minor-before.total_minor, issues=list(after.issues))
        lines = []
        for field, label in (('removed','Remove'), ('added','Add'), ('removed_independent_ownership','End independent ownership'),
                             ('added_independent_ownership','Add independent ownership'),
                             ('installed_removed','No longer installed'), ('installed_added','Now installed')):
            for item in changes[field]:
                lines.append(f'{label}: {item["rpo"] or item["consumer_key"]} — {item["label"]}')
        if preview.interior_changed:
            lines.append(f'Interior: {before.interior_id or "None"} → {after.interior_id or "None"}')
        for change in changes['charge_changes']:
            charge = change['after'] or change['before']
            owner = self.owner_label(charge)
            old, new = change['before'], change['after']
            lines.append(f'Charge: {owner}: {money(old["amount_minor"]) if old else "None"} → {money(new["amount_minor"]) if new else "None"}')
        # Every supporting cause is exposed even if an item or net charge stays.
        for field, label in (('causes_removed','End supplying relationship'), ('causes_added','Add supplying relationship')):
            for cause in changes[field]:
                roots = [self.option(root)['label'] if root in self.ev.options else ('Interior ' + root.removeprefix('interior:') if root.startswith('interior:') else 'Configuration ' + root.removeprefix('configuration:')) for root in cause['roots']]
                lines.append(f'{label}: {self.option(cause["option_id"])["label"]}; {cause["origin"]}; owners: {", ".join(roots)}')
        if before.content != after.content:
            lines.extend('Content before: ' + c.value for c in before.content)
            lines.extend('Content after: ' + c.value for c in after.content)
        lines.append(f'Total: {money(before.total_minor)} → {money(after.total_minor)}')
        lines.extend('Incomplete: ' + self.issue_label(issue, after.configuration_id) for issue in after.issues if issue != 'partial_catalog_not_submission_ready')
        # Exact accepted hash-first disclosure, in addition to all automatic deltas.
        codes = {self.ev.options[o]['rpo'] for o in preview.added}
        if self.model['registry_key'] in ('grandSport', 'grand_sport_x') and 'Z15' in codes and target in self.ev.options and self.maps['option'][target]['section_id'] == 'sec_gsha_001':
            lines.insert(0, 'Selecting this hash mark adds the Grand Sport Heritage Package (Z15) for $995.')
        return dict(release_id=release_id, revision_id=self.revision, action=action, target=target,
                    changes=changes, lines=lines, candidate=self.project(after, release_id))


def money(amount):
    return f'${amount / 100:,.2f}'


class ConsumerSession:
    """Transport boundary: opaque single-use tokens authorize only held previews."""
    def __init__(self, catalog, configuration_id, release_id):
        self.catalog, self.release_id = catalog, release_id
        self._session = Session(catalog.ev, configuration_id)
        self._pending = None
        self.version = 0

    def current(self):
        return dict(version=self.version, build=self.catalog.project(self._session.state, self.release_id),
                    pending=self._pending is not None, revertible=self._session._previous is not None)

    def _version(self, version):
        if type(version) is not int or version != self.version:
            raise EvaluationError('Stale build version')

    def preview(self, action, target, version):
        self._version(version)
        self._pending = None
        if action == 'revert':
            self._session.cancel()
            before, candidate = self._session.state, self._session._previous
            if candidate is None:
                raise EvaluationError('No committed transition to revert')
            p = Preview(before, candidate, candidate.resolved-before.resolved, before.resolved-candidate.resolved,
                        frozenset(before.intent)-frozenset(candidate.intent), before.interior_id != candidate.interior_id)
        else:
            p = self._session.preview(action, target)
        warning = self.catalog.warning(p, self.release_id, action, target)
        token = secrets.token_urlsafe(32)
        warning_hash = digest(warning)
        self._pending = (token, warning_hash, p, action)
        return dict(token=token, warning_sha256=warning_hash, version=self.version, warning=warning)

    def confirm(self, token, warning_sha256, version):
        self._version(version)
        if not self._pending or not secrets.compare_digest(self._pending[0], str(token)) or self._pending[1] != warning_sha256:
            raise EvaluationError('Missing, stale, foreign or altered confirmation')
        if self._pending[3] == 'revert':
            self._session.revert()
        else:
            self._session.confirm(self._pending[2])
        self._pending = None
        self.version += 1
        return self.current()

    def cancel(self, version):
        self._version(version)
        self._session.cancel()
        self._pending = None
        return self.current()

    def order(self):
        if self._pending:
            raise EvaluationError('Confirm or cancel the pending change before export')
        remaining = [i for i in self._session.state.issues if i != 'partial_catalog_not_submission_ready']
        if remaining:
            raise EvaluationError('Complete required selections before export: ' + ', '.join(remaining))
        build = self.current()['build']
        build['issues'] = remaining
        build['validation_scope'] = 'local_catalog_build_not_dealer_submission'
        return build
