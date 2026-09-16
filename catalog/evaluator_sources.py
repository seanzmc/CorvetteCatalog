"""Populate only E01–E08 inputs; no configuration or pricing evaluator.

Translation recipes are source selectors plus accepted design interpretations.
Source IDs survive; split/design identities are UUIDs reused through typed links.
Money uses integer USD cents. This is a partial draft, never a release catalog.
"""
from collections import defaultdict
from contextlib import closing
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from uuid import uuid4

from catalog import foundation as f
from catalog.foundation_schema import IDENTITY_RELATIONS, SCOPES, TRANSLATIONS

DATABASE = f.ROOT / '.local/foundation/evaluator-sources.sqlite'
DESIGN = 'master-schema-worked-examples.md'
POLICY = 'compatibility-notice-policy.json'
OPTIONS = {
    'stingray': 'UQT PCX 5DO 5DG SFZ SHT SNG QE6',
    'grand-sport': 'DMX D84 G26 G4Z GBK GKZ GPH 97A Z15 AE4 AH2 Z25 3F9',
    'grand-sport-x': 'FED XFR XFT J57 B4Z FE5 LS6',
    'z06': 'PDB PDD Z07 T0F CFZ J57 J6D ROY ROZ STZ J56 J6A SOE T0E FE6 FE7 XFR XFS R8E',
    'zr1': 'ZTK TOM J58 J59 FE8 FEJ XFR XFS T0E R8E',
    'zr1x': 'ZTK TOM J59 FEH FEZ XFR XFS T0E R8E',
}
# These are individually classified equipment/hash meanings in the worked traces,
# not a null-price fallback. Unexpected missing prices fail the import.
NO_CHARGE = {
    'stingray': set(), 'grand-sport': {'97A'},
    'grand-sport-x': {'XFR', 'XFT', 'B4Z', 'FE5', 'LS6'},
    'z06': {'FE6', 'FE7', 'XFR', 'XFS'},
    'zr1': {'XFR', 'XFS'}, 'zr1x': {'XFR', 'XFS'},
}
DECISIONS = {
    'stingray': ('ST-D06', 'ST-D10', 'ST-D12'),
    'grand-sport': ('GS-D03', 'GS-D04', 'GS-D05', 'GS-D14', 'GS-D15', 'GS-D16'),
    'grand-sport-x': ('GSX-D10', 'GSX-D11', 'GSX-D12'),
    'z06': ('Z06-D01', 'Z06-D11', 'Z06-D12'),
    'zr1': ('ZR1-D01', 'ZR1-D06', 'ZR1-D08', 'ZR1-D09'),
    'zr1x': ('ZR1X-D01', 'ZR1X-D06', 'ZR1X-D08', 'ZR1X-D09'),
}


def cents(value):
    if value is None:
        return None
    amount = Decimal(str(value)) * 100
    if not amount.is_finite() or amount < 0 or amount != amount.to_integral_value():
        raise ValueError(f'Not an exact nonnegative cent amount: {value}')
    return int(amount)


class Evidence:
    def __init__(self, db, directory):
        self.db, self.directory = db, Path(directory)
        self.documents = {}
        self.sets = {}

    def document(self, name):
        if name not in self.documents:
            raw = (self.directory / name).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            path = 'docs/' + name
            previous = self.db.execute('SELECT content_sha256 FROM source_document WHERE source_path = ?', (path,))
            if any(row[0] != digest for row in previous):
                raise ValueError(f'Pinned input changed; create a fresh disposable database: {path}')
            doc = f._allocated(self.db, 'source_document', 'document_id', {'content_sha256': digest},
                               {'source_path': path, 'acquired_at': self.timestamp(digest)})
            self.documents[name] = doc
        return self.documents[name]

    def timestamp(self, digest):
        row = self.db.execute('SELECT acquired_at FROM source_document WHERE content_sha256 = ?', (digest,)).fetchone()
        return row[0] if row else datetime.now(timezone.utc).isoformat()

    def anchor(self, name, locator):
        return f._evidence(self.db, self.document(name), locator)[0]

    def evidence(self, anchors, decisions=None):
        anchors = tuple(sorted(set(anchors)))
        if not anchors:
            raise ValueError('Missing source evidence')
        if anchors not in self.sets:
            candidates = self.db.execute('SELECT set_id FROM evidence_member WHERE anchor_id = ?', (anchors[0],))
            found = None
            for candidate in candidates:
                members = tuple(r[0] for r in self.db.execute('SELECT anchor_id FROM evidence_member WHERE set_id = ? ORDER BY anchor_id', (candidate[0],)))
                if members == anchors:
                    found = candidate[0]
                    break
            if found is None:
                found = str(uuid4())
                f._insert(self.db, 'evidence_set', {'set_id': found})
                for anchor in anchors:
                    f._insert(self.db, 'evidence_member', {'set_id': found, 'anchor_id': anchor})
            self.sets[anchors] = found
        return {'evidence_set_id': self.sets[anchors], 'decision_set_id': decisions}

    def decisions(self, lane):
        name = lane + '-owner-decisions.json'
        review = json.loads((self.directory / name).read_bytes())['owner_review']
        records = {r['decision_id']: r for r in review['records']}
        members = []
        for identifier in DECISIONS[lane]:
            if records[identifier]['review_state'] != 'accepted':
                raise ValueError(f'Unaccepted decision: {identifier}')
            anchor = self.anchor(name, 'owner_review/records/decision_id=' + identifier)
            f._ensure(self.db, 'review_decision', {'decision_id': identifier, 'version': 1},
                      {'evidence_set_id': self.evidence([anchor])['evidence_set_id']})
            members.append(identifier)
        for identifier, locator in [('compatibility-notices', '/'), ('COMMON-DIRECT-REMOVAL-2026-09-15', 'direct_dependency_removal')]:
            anchor = self.anchor(POLICY, locator)
            f._ensure(self.db, 'review_decision', {'decision_id': identifier, 'version': 1},
                      {'evidence_set_id': self.evidence([anchor])['evidence_set_id']})
            members.append(identifier)
        members.sort()
        for row in self.db.execute('SELECT set_id FROM decision_set'):
            existing = list(self.db.execute('SELECT decision_id, version FROM decision_member WHERE set_id = ? ORDER BY decision_id', (row[0],)))
            if [tuple(r) for r in existing] == [(m, 1) for m in members]:
                return row[0]
        identifier = str(uuid4())
        f._insert(self.db, 'decision_set', {'set_id': identifier})
        for member in members:
            f._insert(self.db, 'decision_member', {'set_id': identifier, 'decision_id': member, 'version': 1})
        return identifier


class Lane:
    def __init__(self, db, evidence, lane, bases):
        self.db, self.e, self.lane, self.bases = db, evidence, lane, bases
        self.name = lane + '-structured-records.json'
        self.data = json.loads((evidence.directory / self.name).read_bytes())
        self.rows, self.roles = self.data['baseline_rows'], self.data['sheet_roles']
        owner = db.execute('''SELECT revision_id, model_year_id FROM catalog_revision
            JOIN model_year USING (model_year_id) JOIN model USING (model_id)
            WHERE model_key = ? AND revision_number = 1''', (self.data['model_key'],)).fetchone()
        self.r, self.m = owner
        self.decisions = evidence.decisions(lane)
        self.design = evidence.anchor(DESIGN, 'first-evaluator-slice--evidence-derived-acceptance-targets')
        self.options = {}
        for code in OPTIONS[lane].split():
            matches = [r for r in self.rows[self.roles['options']] if r['rpo'] == code]
            if len(matches) != 1:
                raise ValueError(f'Ambiguous source option selector: {lane}/{code}')
            self.options[code] = matches[0]
        self.configs = self.rows['variant_master']
        self.condition_cache = {}

    def oid(self, code):
        return self.options[code]['option_id']

    def anchor(self, sheet, row):
        return self.e.anchor(self.name, f'baseline_rows/{sheet}/_row={row["_row"]}')

    def option_anchor(self, code):
        return self.anchor(self.roles['options'], self.options[code])

    def scope(self, body=None, trim=None):
        return [r['variant_id'] for r in self.configs
                if (body in (None, '*') or r['body_style'].lower() == body.lower())
                and (trim in (None, '*') or r['trim_level'].lower() == trim.lower())]

    def put(self, relation, key, values, anchors, retained=None, target=None):
        """Persist full typed target keys; allocation key is the source fragment."""
        anchors = list(dict.fromkeys(anchors))
        evidence = self.e.evidence(anchors + [self.design], self.decisions)
        fragment = relation + ':' + key
        if relation in IDENTITY_RELATIONS:
            column, = TRANSLATIONS[relation]
            old = self.db.execute(f'SELECT {column} FROM {relation}_translation WHERE revision_id = ? AND anchor_id = ? AND fragment_key = ?',
                                  (self.r, anchors[0], fragment)).fetchall()
            if len(old) > 1:
                raise ValueError(f'Ambiguous persisted allocation: {relation}/{key}')
            if old and retained and old[0][0] != retained:
                raise ValueError(f'Retained identity disagrees with allocation: {relation}/{key}')
            identifier = retained or (old[0][0] if old else str(uuid4()))
            f._version(self.db, relation, self.r, self.m, identifier, values, evidence)
            target = {column: identifier}
        else:
            identifier = None
            f._ensure(self.db, relation, {'revision_id': self.r} | target, values | evidence)
        for anchor in anchors + [self.design]:
            disposition = {'revision_id': self.r, 'anchor_id': anchor, 'fragment_key': fragment}
            f._ensure(self.db, 'source_disposition', disposition, {'disposition': 'accepted_target'} | evidence)
            f._ensure(self.db, relation + '_translation', disposition | target, evidence)
        return identifier

    def scoped(self, relation, key, values, anchors, scope=None, retained=None):
        identifier = self.put(relation, key, values, anchors, retained)
        for config in self.scope() if scope is None else scope:
            self.put(relation + '_configuration', key + '/' + config, {}, anchors,
                     target={SCOPES[relation]: identifier, 'configuration_id': config})
        return identifier

    def condition(self, clauses=(), anchors=()):
        # A tuple of (mode, ((typed column, retained id, state), ...)) clauses.
        cache_key = tuple(clauses)
        if cache_key in self.condition_cache:
            return self.condition_cache[cache_key]
        key = json.dumps(clauses, separators=(',', ':'))
        # Keep source locators short; this is only a fragment discriminator, not an ID.
        key = hashlib.sha256(key.encode()).hexdigest()
        anchors = list(anchors) or [self.design]
        identifier = self.put('condition', key, {'mode': 'conjunction' if clauses else 'always'}, anchors)
        for i, (mode, members) in enumerate(clauses, 1):
            clause = {'condition_id': identifier, 'clause_id': str(i)}
            self.put('condition_clause', key + '/' + str(i), {'mode': mode}, anchors, target=clause)
            for j, (column, endpoint, state) in enumerate(members, 1):
                self.put('condition_member', key + '/' + str(i) + '/' + str(j),
                         {'option_id': None, 'interior_id': None, 'group_id': None, column: endpoint, 'state': state},
                         anchors, target=clause | {'member_id': str(j)})
        self.condition_cache[cache_key] = identifier
        return identifier

    def selected(self, code):
        return self.condition((('any_present', (('option_id', self.oid(code), 'resolved_selection'),)),), [self.option_anchor(code)])

    def acquisition(self, key, target, condition, anchors, origin='included', peer='locked', intent='preserve_prior', scope=None, retained=None, priority=1):
        return self.scoped('acquisition', key, {'condition_id': condition, 'target_option_id': self.oid(target),
            'origin_kind': origin, 'peer_policy': peer, 'intent_policy': intent, 'priority': priority}, anchors, scope, retained)

    def requirement(self, key, source, satisfaction, anchors, activation=None, interior=False, scope=None, retained=None):
        return self.scoped('requirement', key, {
            'source_option_id': None if interior else self.oid(source),
            'source_interior_id': source if interior else None, 'source_state': 'chosen' if interior else 'resolved_selection',
            'activation_condition_id': activation or self.condition(), 'satisfaction_condition_id': satisfaction,
            'loss_policy': 'remove_source_with_notice_revert'}, anchors, scope, retained)

    def include(self, source, target, *, interior=False, peer='locked', intent='preserve_prior', scope=None, origin='included', unless=None, priority=1):
        source_id = source if interior else self.oid(source)
        sheet = self.roles['rule_mapping']
        row, = [r for r in self.rows[sheet] if r['source_id'] == source_id and r['target_id'] == self.oid(target) and r['rule_type'] == 'includes']
        anchor = self.anchor(sheet, row)
        condition = (self.condition((('any_present', (('interior_id', source, 'chosen'),)),), [anchor])
                     if interior else self.selected(source))
        if unless:
            condition = self.condition((
                ('any_present', (('option_id', source_id, 'resolved_selection'),)),
                ('none_present', (('option_id', self.oid(unless), 'resolved_selection'),))),
                [anchor, self.option_anchor(unless)])
        return self.acquisition(row['rule_id'], target, condition, [anchor], peer=peer, intent=intent, origin=origin,
                                scope=self.scope(row.get('body_style_scope')) if scope is None else scope,
                                retained=row['rule_id'], priority=priority)

    def rate(self, key, target, condition, amount, anchors, priority=1, scope=None, retained=None):
        return self.scoped('option_rate', key, {'condition_id': condition, 'target_option_id': self.oid(target),
            'priority': priority, 'amount_minor': cents(amount), 'basis_id': self.bases['option_purchase']}, anchors, scope, retained)

    def source_rates(self, row_numbers):
        priorities = defaultdict(int)
        sheet = self.roles['price_rules']
        for number in row_numbers:
            row, = [r for r in self.rows[sheet] if r['_row'] == number]
            by_id = {r['option_id']: code for code, r in self.options.items()}
            target, condition = by_id[row['target_option_id']], by_id[row['condition_option_id']]
            if row['price_rule_type'] != 'override':
                raise ValueError('Unsupported source rate kind')
            priorities[target] += 1
            self.rate(row['price_rule_id'], target, self.selected(condition), row['price_value'],
                      [self.anchor(sheet, row)], priorities[target], self.scope(row.get('body_style_scope'), row.get('trim_level_scope')), row['price_rule_id'])

    def substitution(self, source, removed, replacement):
        self.scoped('equipment_substitution', source + '/' + removed + '/' + replacement,
            {'condition_id': self.selected(source), 'removed_option_id': self.oid(removed), 'replacement_option_id': self.oid(replacement)},
            [self.option_anchor(source), self.option_anchor(removed), self.option_anchor(replacement)])

    def roots(self, codes, origin='standard', peer='locked'):
        for code in codes.split():
            self.acquisition(origin + '/' + code, code, self.condition(), [self.option_anchor(code)], origin=origin, peer=peer)

    def replacement(self, source, requested, accepted, anchors):
        conflict = self.scoped('conflict', source + '/' + requested, {
            'source_option_id': self.oid(source), 'source_interior_id': None, 'activation_condition_id': self.condition()}, anchors)
        self.put('conflict_member', source + '/' + requested, {'option_id': self.oid(requested), 'interior_id': None}, anchors,
                 target={'conflict_id': conflict, 'member_id': '1'})
        plan = self.scoped('replacement_plan', source + '/' + requested, {
            'condition_id': self.selected(source), 'requested_option_id': self.oid(requested)}, anchors)
        for position, action, code in [(1, 'remove', source), (2, 'add', accepted)]:
            self.put('replacement_action', source + '/' + requested + '/' + str(position),
                {'action': action, 'option_id': self.oid(code), 'intent_effect': 'commit_purchase' if action == 'add' else None},
                anchors, target={'plan_id': plan, 'position': position})

    def foundation(self):
        # Add price payloads to existing structural configurations exactly once.
        for config in self.configs:
            values = {'starting_amount_minor': cents(config['base_price']), 'basis_id': self.bases['vehicle_destination_included']}
            current = self.db.execute('SELECT starting_amount_minor, basis_id FROM configuration WHERE revision_id = ? AND id = ?', (self.r, config['variant_id'])).fetchone()
            if current[0] is None and current[1] is None:
                self.db.execute('UPDATE configuration SET starting_amount_minor = ?, basis_id = ? WHERE revision_id = ? AND id = ?',
                                (*values.values(), self.r, config['variant_id']))
            else:
                f._ensure(self.db, 'configuration', {'revision_id': self.r, 'id': config['variant_id']}, values)
            self.put('configuration_policy', config['variant_id'], {
                'interior_minimum': 1, 'interior_maximum': 1, 'context_reset_policy': 'clear_intent',
                'invalid_interior_action': 'clear_with_notice_revert'}, [self.anchor('variant_master', config)],
                target={'configuration_id': config['variant_id']})
        common = self.e.anchor(POLICY, 'direct_dependency_removal')
        self.put('interaction_policy', 'common', {'conflict_action': 'notice_confirm_cancel',
            'direct_removal_action': 'remove_requested_and_supporting_sources', 'cancel_action': 'preserve_whole_state',
            'revert_action': 'restore_whole_state'}, [common], target={})
        for code, row in self.options.items():
            amount = row['price']
            if code in NO_CHARGE[self.lane]:
                if amount is not None:
                    raise ValueError(f'No-charge classification source changed: {self.lane}/{code}')
                mode = 'no_separate_charge'
            else:
                if amount is None:
                    raise ValueError(f'Missing purchase price: {self.lane}/{code}')
                mode = 'priced'
            anchors = [self.option_anchor(code)]
            if self.lane == 'grand-sport' and code == 'Z25':
                # GS-D05 assigns the source interior price to Z25; no residual.
                leaf, = [r for r in self.rows['lt_interiors'] if r['interior_id'] == '3LT_AE4_EL9']
                amount = leaf['Price']
                anchors.append(self.anchor('lt_interiors', leaf))
            if not row['active'] and (self.lane, code) not in {('zr1', 'FE8'), ('zr1x', 'FEH')}:
                raise ValueError(f'Inactive source lacks an accepted restoration: {self.lane}/{code}')
            self.put('option', row['option_id'], {'rpo': row['rpo'], 'name': row['option_name'],
                'customer_selectable': int(row['selectable']), 'lifecycle': 'active', 'charge_mode': mode,
                'purchase_amount_minor': cents(amount), 'basis_id': self.bases['option_purchase'] if amount is not None else None},
                anchors, retained=row['option_id'])
            rows = [r for r in self.rows[self.roles['availability']] if r['option_id'] == row['option_id']]
            if len(rows) != len(self.configs) or {r['variant_id'] for r in rows} != set(self.scope()):
                raise ValueError(f'Incomplete applicability: {self.lane}/{code}')
            for availability in rows:
                self.put('option_configuration', row['option_id'] + '/' + availability['variant_id'],
                    {'status': availability['status']}, [self.anchor(self.roles['availability'], availability)],
                    target={'option_id': row['option_id'], 'configuration_id': availability['variant_id']})


def stingray(lane):
    uqt = [r for r in lane.rows[lane.roles['variant_overrides']] if r['option_id'] == lane.oid('UQT')]
    if len(uqt) != 4 or any(r['selectable'] is not False for r in uqt):
        raise ValueError('UQT standard-only source overrides changed')
    lane.acquisition('standard/UQT', 'UQT', lane.condition(),
                     [lane.anchor(lane.roles['variant_overrides'], r) for r in uqt],
                     origin='standard', scope=[r['variant_id'] for r in uqt])
    for child in '5DG SFZ SHT SNG'.split():
        lane.include('PCX', child, intent='absorb_prior')
    lane.source_rates([11, 12, 13, 14])
    lane.replacement('PCX', '5DO', '5DO', [lane.option_anchor('PCX'), lane.option_anchor('5DO'), lane.e.anchor(POLICY, 'model_overrides/stingray')])


def grand_sport(lane):
    paints = tuple(('option_id', lane.oid(code), 'resolved_selection') for code in 'G26 G4Z GBK GKZ GPH'.split())
    anchors = [lane.option_anchor('DMX'), lane.option_anchor('D84')]
    condition = lane.condition((('any_present', (('option_id', lane.oid('DMX'), 'resolved_selection'),)),
                                ('any_present', paints)), anchors)
    lane.acquisition('DMX/D84', 'D84', condition, anchors, origin='dependency', scope=lane.scope('convertible'))
    lane.requirement('DMX/D84', 'DMX', lane.selected('D84'), anchors, activation=condition, scope=lane.scope('convertible'))
    lane.include('97A', 'Z15', origin='dependency')
    lane.include('Z25', '3F9', scope=lane.scope(trim='3lt'), priority=2)
    lane.requirement('97A/Z15', '97A', lane.selected('Z15'), [lane.option_anchor('97A'), lane.option_anchor('Z15')])
    row, = [r for r in lane.rows[lane.roles['rule_mapping']] if r['rule_id'] == 'gs_rule_opt_dmx_001_requires_opt_z15_001']
    lane.requirement('DMX/Z15', 'DMX', lane.selected('Z15'), [lane.anchor(lane.roles['rule_mapping'], row)], retained=row['rule_id'])
    for seat in ('AE4', 'AH2'):
        identifier = f'3LT_{seat}_EL9'
        row, = [r for r in lane.rows['lt_interiors'] if r['interior_id'] == identifier]
        scope_row, = [r for r in lane.rows['model_interior_scope'] if r['interior_id'] == identifier]
        anchors = [lane.anchor('lt_interiors', row), lane.anchor('model_interior_scope', scope_row)]
        lane.put('interior', identifier, {'seat_option_id': lane.oid(seat), 'code': row['Interior Code'], 'enabled': 1}, anchors, retained=identifier)
        scope = lane.scope(trim=scope_row['trim_level'])
        for config in scope:
            lane.put('interior_configuration', identifier + '/' + config, {}, anchors,
                     target={'interior_id': identifier, 'configuration_id': config})
        for child in ('Z25', '3F9'):
            lane.include(identifier, child, interior=True, scope=scope)
            lane.requirement(identifier + '/' + child, identifier, lane.selected(child), anchors, interior=True, scope=scope)
    # Seat owns its own price; Z25 carries the full 1,995 source leaf charge.
    lane.source_rates([24, 25, 26, 56])


def grand_sport_x(lane):
    lane.roots('J57 B4Z FE5 LS6 XFT')
    lane.include('FED', 'XFR')
    lane.substitution('FED', 'XFT', 'XFR')


def z06(lane):
    lane.roots('J56 J6A SOE T0E FE6 XFR', peer='yield_to_explicit')
    lane.roots('R8E', origin='default')
    for parent, children in [('PDB', 'J57 J6D ROY'), ('PDD', 'Z07 T0F CFZ ROY'), ('Z07', 'J57 FE7 XFS T0F'), ('T0F', 'CFZ')]:
        for child in children.split():
            lane.include(parent, child,
                         peer='yield_to_explicit' if child == 'ROY' or (parent == 'Z07' and child == 'T0F') else 'locked',
                         unless='PDD' if (parent, child) == ('Z07', 'T0F') else None,
                         priority=2 if parent == 'T0F' else 1)
    # PDB has its own locked J6D inclusion. Keep the soft default's policy
    # out of that overlap instead of allowing equal priority to choose ownership.
    j57_default = lane.condition((
        ('any_present', (('option_id', lane.oid('J57'), 'resolved_selection'),)),
        ('none_present', (('option_id', lane.oid('PDB'), 'resolved_selection'),))),
        [lane.option_anchor('J57'), lane.option_anchor('PDB')])
    lane.acquisition('J57/J6D', 'J6D', j57_default,
                     [lane.option_anchor('J57'), lane.e.anchor('z06-owner-decisions.json', 'owner_review/records/decision_id=Z06-D01')],
                     origin='default', peer='yield_to_explicit')
    group_sheet = lane.roles['rule_groups']
    member_sheet = lane.roles['rule_group_members']
    # Keep each actual source group ID; no section-derived runtime membership.
    for parent in ('PDB', 'PDD'):
        row, = [r for r in lane.rows[group_sheet] if r['group_id'] == f'z06_group_{parent.lower()}_requires_carbon_wheel']
        anchor = lane.anchor(group_sheet, row)
        group = lane.scoped('choice_group', row['group_id'], {'minimum': 0, 'maximum': 1, 'peer_policy': 'replace'}, [anchor], retained=row['group_id'])
        members = [r for r in lane.rows[member_sheet] if r['group_id'] == row['group_id'] and r['active']]
        if {r['target_id'] for r in members} != {lane.oid(c) for c in ('ROY', 'ROZ', 'STZ')}:
            raise ValueError('Carbon wheel membership changed')
        for member in members:
            lane.put('choice_group_member', row['group_id'] + '/' + member['target_id'], {}, [anchor, lane.anchor(member_sheet, member)],
                     target={'group_id': group, 'option_id': member['target_id']})
        occupied = lane.condition((('any_present', (('group_id', group, 'occupied'),)),), [anchor])
        lane.requirement(parent + '/carbon-wheel', parent, occupied, [anchor])
    lane.replacement('PDB', 'Z07', 'PDD', [lane.option_anchor('PDB'), lane.option_anchor('PDD'), lane.e.anchor(POLICY, 'model_overrides/z06/pdb_z07_interaction')])
    # Explicit precedence from the worked rows; supplemental STZ rates preserve
    # the real third member rather than creating an incomplete group endpoint.
    lane.source_rates([6, 7, 13, 8, 9, 10, 11, 12, 14, 16, 17, 18,
                       26, 27, 28, 29, 30, 31, 50, 4, 15])
    for condition, removed, replacement in [('J57', 'J56', 'J57'), ('J57', 'J6A', 'J6D'),
            ('ROY', 'SOE', 'ROY'), ('ROZ', 'SOE', 'ROZ'), ('STZ', 'SOE', 'STZ'),
            ('T0F', 'T0E', 'T0F'), ('Z07', 'FE6', 'FE7'), ('Z07', 'XFR', 'XFS')]:
        lane.substitution(condition, removed, replacement)


def zr(lane):
    is_x = lane.lane == 'zr1x'
    suspension, track = ('FEH', 'FEZ') if is_x else ('FE8', 'FEJ')
    lane.roots(('J59 ' if is_x else 'J58 ') + suspension + ' XFR')
    lane.roots('T0E', peer='yield_to_explicit')
    lane.roots('R8E', origin='default')
    for child in [track, 'XFS', 'TOM'] + ([] if is_x else ['J59']):
        lane.include('ZTK', child)
    lane.requirement('ZTK/TOM', 'ZTK', lane.selected('TOM'), [lane.option_anchor('ZTK'), lane.option_anchor('TOM')])
    lane.substitution('ZTK', suspension, track)
    lane.substitution('ZTK', 'XFR', 'XFS')
    if not is_x:
        lane.substitution('ZTK', 'J58', 'J59')
    lane.substitution('TOM', 'T0E', 'TOM')


def validate_sources(db):
    """Validate translated payloads, not runtime convergence or release coverage."""
    f.validate(db)
    for relation, columns in {
        'configuration': ('starting_amount_minor', 'basis_id'),
        'acquisition': ('origin_kind', 'peer_policy', 'intent_policy', 'priority'),
        'requirement': ('source_state', 'loss_policy'),
        'option_rate': ('amount_minor', 'basis_id'),
        'choice_group': ('peer_policy',),
        'interior': ('code', 'enabled'),
    }.items():
        if db.execute(f'SELECT 1 FROM {relation} WHERE ' + ' OR '.join(c + ' IS NULL' for c in columns)).fetchone():
            raise ValueError(f'Incomplete {relation} payload')
    if db.execute('''SELECT 1 FROM option o WHERE id <> ? AND
        (charge_mode IS NULL OR (charge_mode = 'priced' AND purchase_amount_minor IS NULL))''', (f.SAMPLE_OPTION_ID,)).fetchone():
        raise ValueError('Missing classified purchase price')
    for row in db.execute('SELECT revision_id, id, mode FROM condition'):
        clauses = db.execute('SELECT clause_id FROM condition_clause WHERE revision_id = ? AND condition_id = ?', tuple(row[:2])).fetchall()
        if (row['mode'] == 'always') != (len(clauses) == 0):
            raise ValueError('Condition mode/clauses disagree')
        for clause in clauses:
            if not db.execute('SELECT 1 FROM condition_member WHERE revision_id = ? AND condition_id = ? AND clause_id = ?', (*row[:2], clause[0])).fetchone():
                raise ValueError('Empty condition clause')
    for relation, meaning in [('configuration', 'vehicle_destination_included'),
                              ('option', 'option_purchase'), ('option_rate', 'option_purchase')]:
        if db.execute(f"""SELECT 1 FROM {relation} p JOIN price_basis b USING (basis_id)
            WHERE b.currency <> 'USD' OR b.amount_meaning <> ?""", (meaning,)).fetchone():
            raise ValueError(f'Wrong price basis for {relation}')
    # Every populated target has a concrete same-revision translation.
    for relation, keys in TRANSLATIONS.items():
        columns = ('id',) if relation in IDENTITY_RELATIONS else keys
        predicate = ' AND '.join(f't.{key} = p.{column}' for key, column in zip(keys, columns))
        if predicate:
            predicate = ' AND ' + predicate
        if db.execute(f'''SELECT 1 FROM {relation} p WHERE NOT EXISTS
            (SELECT 1 FROM {relation}_translation t WHERE t.revision_id = p.revision_id{predicate})''').fetchone():
            raise ValueError(f'Missing typed translation: {relation}')


def import_cases(db, source_dir=f.ROOT / 'docs'):
    """One transaction, including allocation; a changed pinned input is refused."""
    with db:
        f._import_samples(db, source_dir)
        evidence = Evidence(db, source_dir)
        basis_anchors = [evidence.anchor(DESIGN, 'reading-the-populated-rows')]
        policy = json.loads((Path(source_dir) / POLICY).read_bytes())
        if policy['review_state'] != 'accepted' or policy['direct_dependency_removal']['review_state'] != 'accepted':
            raise ValueError('Common interaction policy is not accepted')
        for lane in f.LANES:
            review = json.loads((Path(source_dir) / (lane + '-owner-decisions.json')).read_bytes())['owner_review']
            if review['currency_code'] != 'USD':
                raise ValueError(f'Unexpected source currency: {lane}')
            basis_anchors.append(evidence.anchor(lane + '-owner-decisions.json', 'owner_review/currency_code'))
        bases = {}
        for meaning in ('vehicle_destination_included', 'option_purchase'):
            bases[meaning] = f._allocated(db, 'price_basis', 'basis_id', {'currency': 'USD', 'amount_meaning': meaning},
                {'minor_units_per_unit': 100, 'resolution_state': 'accepted'} | evidence.evidence(basis_anchors, evidence.decisions('stingray')))
        for name, populate in [('stingray', stingray), ('grand-sport', grand_sport),
                              ('grand-sport-x', grand_sport_x), ('z06', z06), ('zr1', zr), ('zr1x', zr)]:
            lane = Lane(db, evidence, name, bases)
            lane.foundation()
            populate(lane)
        validate_sources(db)


def main():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with closing(f.connect(DATABASE)) as db:
        if not db.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchone():
            f.create_schema(db)
        import_cases(db)
        counts = {t: db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
                  for t in ('configuration', 'option', 'interior', 'acquisition', 'requirement', 'option_rate')}
        print(json.dumps({'database': str(DATABASE), 'counts': counts, 'validation': 'source structure passed; evaluator not implemented'}, indent=2))


if __name__ == '__main__':
    main()
