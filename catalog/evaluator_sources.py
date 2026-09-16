"""Populate complete offerings or the preserved E01–E08 source fixture.

Translation recipes are source selectors plus accepted design interpretations.
Source IDs survive; split/design identities are UUIDs reused through typed links.
Money uses integer USD cents. This is a partial draft, never a release catalog.
"""
from collections import defaultdict
import argparse
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
CATALOG_DATABASE = f.ROOT / '.local/foundation/catalog-offerings.sqlite'
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
# Inspected null-price equipment identities. This is a classification, never a
# fallback for an unexpectedly missing purchasable price. Uncoded equipment is
# separately classified by the handoff offering disposition.
EQUIPMENT_NO_CHARGE = {
    'stingray': set('UVB UQS K7A DWK UV6 UQH UVA UFG K7B UG1 KI3 KQV AL9 AT9 AHE AHH AQA AP9 DYX UFT UTJ UTV UTU IWE DRG TR7 CFX J55 V08 G96 QTU M1N G0K B4Z AJ7 UHY UEU UKT TQ5 UHX DRZ UD7 TDM CJ2 JL9 U80 G0J NPP T4L LS6 A2X A7K N38 XFN M1L VHM NK4 U5G IVE UE1 U2K VV4 PPW'.split()),
    'grand-sport': set('UVB UQS K7A DWK UV6 UQH UVA UFG K7B UG1 KI3 KQV AL9 AT9 AHE AHH AQA AP9 DYX UFT UTJ UTV UTU IWE DRG TR7 CFX XFR XFS AJ7 UHY UEU UKT TQ5 UHX DRZ UD7 TDM CJ2 U80 NPP T4L LS6 A2X A7K N38 VHM V08 M1N G0K B4Z XFT NK4 FEA IVE PPW'.split()),
    'grand-sport-x': set('UVB UQS K7A DWK UV6 UQH UVA UFG K7B UG1 KI3 KQV AL9 AT9 AHE AHH AQA AP9 DYX UFT UTJ UTV UTU IWE DRG TR7 CFX XFR AJ7 UHY UEU UKT TQ5 UHX DRZ UD7 TDM FE5 MLG HP1 CJ2 U80 NPP T4L LS6 A2X A7K N38 VHM G0K B4Z XFT NK4 U2K UE1 VV4 U5G IVE PPW'.split()),
    'z06': set('DWK K7A UQS UV6 UVB AHE AHH AL9 AP9 AQA AT9 DYX K7B KI3 KQV UFG UFT UG1 UQH UTJ UTU UTV UVA IWE FE6 FE7 XFR N3W AJ7 DRZ TDM TQ5 UD7 UEU UHX UHY UKT A2X A7K B4Z CJ2 G0K LT6 M1M N38 NPP T4L U80 VHM WUB NK4 IVE PPW U2K U5G UE1 VV4'.split()),
    'zr1': set('UV6 UVB UQS K7A DWK UQH UVA UFG K7B UG1 KI3 KQV AL9 AT9 AHE AHH AQA AP9 DYX UFT UTJ UTV UTU IWE DRG TR7 CFX XFR XFS UQT AJ7 UHY UEU UKT TQ5 UHX DRZ UD7 TDM CJ2 U80 WUB NPP T4L A2X A7K N38 VHM G0K B4Z LT7 M1K NK4 IVE PPW U2K U5G UE1 VV4'.split()),
    'zr1x': set('UV6 UVB UQS K7A DWK UQH UVA UFG K7B UG1 KI3 KQV AL9 AT9 AHE AHH AQA AP9 DYX UFT UTJ UTV UTU IWE DRG TR7 CFX XFR XFS UQT AJ7 UHY UEU UKT TQ5 UHX DRZ UD7 TDM CJ2 U80 WUB NPP T4L A2X A7K N38 VHM G0K B4Z CFC HP1 LT7 MLP NK4 IVE PPW U2K U5G UE1 VV4'.split()),
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
    def __init__(self, db, directory, *, complete=False):
        self.db, self.directory = db, Path(directory)
        self.complete = complete
        self.documents = {}
        self.anchors = {}
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
        key = (name, locator)
        if key not in self.anchors:
            self.anchors[key] = f._evidence(self.db, self.document(name), locator)[0]
        return self.anchors[key]

    def evidence(self, anchors, decisions=None):
        anchors = tuple(sorted(set(anchors)))
        if not anchors:
            raise ValueError('Missing source evidence')
        if anchors not in self.sets:
            # The common design anchor belongs to thousands of sets. Start at
            # the most selective source anchor rather than random UUID order.
            first = min(anchors, key=lambda anchor: self.db.execute(
                'SELECT COUNT(*) FROM evidence_member WHERE anchor_id = ?', (anchor,)).fetchone()[0])
            candidates = self.db.execute('SELECT set_id FROM evidence_member WHERE anchor_id = ?', (first,))
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
        for identifier in records if self.complete else DECISIONS[lane]:
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

    def configuration_foundation(self):
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

    def foundation(self):
        self.configuration_foundation()
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


class OfferingLane(Lane):
    """Complete offering data; relationship execution is still the case slice.

    Keep source identities, including uncoded and retired rows. RPO lookup is
    only for the existing recipes; it cannot collapse duplicate source rows.
    """

    def __init__(self, db, evidence, lane, bases):
        super().__init__(db, evidence, lane, bases)
        self.design = evidence.anchor(DESIGN, 'reading-the-populated-rows')
        self.review_name = lane + '-owner-decisions.json'
        self.review = json.loads((evidence.directory / self.review_name).read_bytes())['owner_review']
        self.offerings = {r['option_id']: r for r in self.rows[self.roles['options']]}
        if len(self.offerings) != len(self.rows[self.roles['options']]):
            raise ValueError(f'Duplicate source option identity: {lane}')
        self.targets = {r['record_id']: r for r in self.review['offering_targets']}
        expected = {self.data['model_key'] + ':' + oid for oid in self.offerings}
        if set(self.targets) != expected or len(self.targets) != len(self.review['offering_targets']):
            raise ValueError(f'Incomplete offering decision accounting: {lane}')
        self.options = {}
        for row in self.offerings.values():
            code = row['rpo']
            if not code or self.target(row)['target_disposition'] == 'retire_duplicate':
                continue
            if code in self.options:
                raise ValueError(f'Ambiguous source option selector: {lane}/{code}')
            self.options[code] = row
        self.interior_rows = {r['interior_id']: r for r in self.rows[self.roles['interiors']]}
        self.rate_order = []

    def target(self, row):
        return self.targets[self.data['model_key'] + ':' + row['option_id']]

    def review_anchor(self, collection, identifier):
        return self.e.anchor(self.review_name, f'owner_review/{collection}/record_id={identifier}')

    def oid(self, code):
        return code if code in self.offerings else super().oid(code)

    def option_anchor(self, code):
        return self.anchor(self.roles['options'], self.offerings[self.oid(code)])

    def availability_target(self, row, availability):
        return availability['status'], [self.anchor(self.roles['availability'], availability)]

    def foundation(self):
        self.configuration_foundation()
        dispositions = {r['record_id']: r for r in self.data['offering_dispositions']}
        restorations = {
            'z06': {'N3W'}, 'zr1': {'N3W', 'DY0', 'CFV', 'CFC', 'FE8'},
            'zr1x': {'N3W', 'FEH'},
        }
        hashes = {'17A', '20A', '55A', '75A', '97A', 'DX4'} if self.lane in ('grand-sport', 'grand-sport-x') else set()
        for oid, row in self.offerings.items():
            target = self.target(row)
            disposition = target['target_disposition']
            if disposition not in {'retain_subject_to_decision_overlay', 'rename', 'retire', 'retire_duplicate', 'visible_unavailable'}:
                raise ValueError(f'Unsupported offering disposition: {disposition}')
            lifecycle = ('retired' if disposition in ('retire', 'retire_duplicate') else
                         'factory_unavailable' if disposition == 'visible_unavailable' else 'active')
            if not row['active'] and lifecycle == 'active' and row['rpo'] not in restorations.get(self.lane, set()):
                raise ValueError(f'Inactive source lacks accepted restoration: {self.lane}/{oid}')
            amount = row['price']
            classification = dispositions[self.data['model_key'] + ':' + oid]['source_classification']
            # Z06's included-only disclosure rows retain a true workbook
            # selectable flag; the flag is not evidence of a purchase price.
            included_only = self.lane == 'z06' and row['rpo'] in {'CFX', 'DRG', 'TR7', 'XFS'}
            no_charge = row['rpo'] in EQUIPMENT_NO_CHARGE[self.lane] or row['rpo'] in hashes or included_only or classification == 'uncoded_equipment_match'
            if no_charge:
                if amount is not None:
                    raise ValueError(f'No-charge classification source changed: {self.lane}/{row["rpo"] or oid}')
                mode = 'no_separate_charge'
            elif amount is not None:
                mode = 'priced'
            elif lifecycle != 'active':
                # A disabled historical offering may have an unknown purchase
                # rate. It is neither free nor eligible for acquisition.
                mode = None
            else:
                raise ValueError(f'Missing purchase price: {self.lane}/{oid}')
            anchors = [self.option_anchor(oid), self.review_anchor('offering_targets', target['record_id'])]
            name = row['option_name']
            if target.get('target_name') and target['target_name'] != 'Royal Blue':
                name = target['target_name']
            elif row['rpo'] == 'DUE' and self.lane != 'stingray':
                # GSX-D07/Z06-D09 carry the rename in their decision records,
                # although their per-offering target still says retain.
                name = name.replace('Santorini Blue', 'Royal Blue')
            if row['rpo'] == 'Z25' and self.lane in ('grand-sport', 'grand-sport-x'):
                leaf = self.interior_rows['3LT_AE4_EL9']
                amount = leaf['Price']
                anchors.append(self.anchor(self.roles['interiors'], leaf))
            self.put('option', oid, {'rpo': row['rpo'], 'name': name,
                'customer_selectable': int(row['selectable']), 'lifecycle': lifecycle, 'charge_mode': mode,
                'purchase_amount_minor': cents(amount), 'basis_id': self.bases['option_purchase'] if amount is not None else None}, anchors, retained=oid)
            matrix = [r for r in self.rows[self.roles['availability']] if r['option_id'] == oid]
            if len(matrix) != len(self.configs) or {r['variant_id'] for r in matrix} != set(self.scope()):
                raise ValueError(f'Incomplete applicability: {self.lane}/{oid}')
            for availability in matrix:
                status, status_anchors = self.availability_target(row, availability)
                self.put('option_configuration', oid + '/' + availability['variant_id'],
                    {'status': status}, status_anchors,
                    target={'option_id': oid, 'configuration_id': availability['variant_id']})
        for addition in self.review['accepted_additions']:
            if addition['currency'] != 'USD' or addition['target_disposition'] != 'add' or addition['rpo'] in self.options:
                raise ValueError(f'Invalid or duplicate accepted addition: {addition["record_id"]}')
            if set(addition['configuration_ids']) != set(self.scope()):
                raise ValueError(f'Incomplete accepted addition scope: {addition["record_id"]}')
            anchor = self.review_anchor('accepted_additions', addition['record_id'])
            oid = self.put('option', addition['record_id'], {
                'rpo': addition['rpo'], 'name': addition['guide_disclosure'].split('\n')[0].removeprefix('NEW!').strip(),
                'customer_selectable': 1, 'lifecycle': 'active', 'charge_mode': 'priced',
                'purchase_amount_minor': cents(addition['price']), 'basis_id': self.bases['option_purchase']}, [anchor])
            for config in self.scope():
                self.put('option_configuration', addition['record_id'] + '/' + config,
                    {'status': 'available'}, [anchor], target={'option_id': oid, 'configuration_id': config})
        for row in self.rows[self.roles['variant_overrides']]:
            if row['active']:
                self.put('option_presentation_override', row['option_id'] + '/' + row['variant_id'],
                    {'customer_selectable': int(row['selectable'])}, [self.anchor(self.roles['variant_overrides'], row)],
                    target={'option_id': row['option_id'], 'configuration_id': row['variant_id']})

    def interiors(self, *, case_recipes=True):
        """Translate seats once, option-backed parts, and model-owned extras.

        The frozen leaf Price is never a balancing amount. AE4 is always owned
        by its seat option, including the four defective R6X source paths.
        """
        scopes = {r['interior_id']: r for r in self.rows['model_interior_scope']}
        if set(scopes) != set(self.interior_rows) or len(scopes) != len(self.rows['model_interior_scope']):
            raise ValueError(f'Incomplete interior scope accounting: {self.lane}')
        components = {}
        for identifier, row in self.interior_rows.items():
            sr = scopes[identifier]
            if sr['model_key'] != self.data['model_key'] or row['Trim'].split('_')[0].lower() != sr['trim_level'].lower():
                raise ValueError(f'Wrong interior lane or trim: {identifier}')
            anchors = [self.anchor(self.roles['interiors'], row), self.anchor('model_interior_scope', sr)]
            self.put('interior', identifier, {'seat_option_id': self.oid(row['Seat']), 'code': row['Interior Code'],
                'enabled': int(str(sr['active']).lower() == 'true')}, anchors, retained=identifier)
            for config in self.scope(trim=sr['trim_level']):
                self.put('interior_configuration', identifier + '/' + config, {}, anchors,
                    target={'interior_id': identifier, 'configuration_id': config})
        for row in self.rows['interior_components']:
            if str(row['active']).lower() != 'true':
                continue
            identifier = row['interior_id']
            leaf = self.interior_rows[identifier]
            if row['model_key'] != self.data['model_key']:
                raise ValueError('Cross-model interior part')
            if row['component_type'] == 'seat':
                if row['rpo'] != leaf['Seat']:
                    raise ValueError('Interior seat component disagrees with leaf')
                continue  # Seat FK already owns this part and charge.
            anchors = [self.anchor('interior_components', row)]
            option, component = None, None
            if row['rpo'] in self.options:
                option = self.oid(row['rpo'])
            else:
                key = (row['component_type'], row['rpo'])
                if key not in components:
                    # Use the complete membership evidence, so shared components
                    # do not depend on the first encountered leaf's identity.
                    members = [r for r in self.rows['interior_components']
                               if (r['component_type'], r['rpo']) == key and str(r['active']).lower() == 'true']
                    component = self.put('component', '/'.join(key), {'kind': key[0], 'code': key[1]},
                        [self.anchor('interior_components', r) for r in members])
                    components[key] = component
                    for config in self.configs:
                        used = [r for r in members if scopes[r['interior_id']]['trim_level'].lower() == config['trim_level'].lower()]
                        if not used:
                            continue
                        rates = [r for r in self.rows['PriceRef'] if r['Code'] == key[1]
                                 and str(r['OptionType']).lower().replace('_', '') == row['price_ref_type'].lower().replace('_', '')
                                 and (r['Trim'] is None or r['Trim'].lower() == config['trim_level'].lower())]
                        specific = [r for r in rates if r['Trim'] is not None]
                        rate, = specific or rates
                        self.put('component_rate', '/'.join(key) + '/' + config['variant_id'],
                            {'amount_minor': cents(rate['Price']), 'basis_id': self.bases['option_purchase']},
                            [self.anchor('PriceRef', rate)] + [self.anchor('interior_components', r) for r in used],
                            target={'component_id': component, 'configuration_id': config['variant_id']})
                component = components[key]
            self.put('interior_part', identifier + '/' + row['rpo'], {
                'option_id': option, 'component_id': component, 'role': row['component_type'],
                'display_order': int(row['display_order'])}, anchors,
                target={'interior_id': identifier, 'part_key': row['rpo']})
        # Interior-owned belts and launch-edition content are part of the
        # offering's price closure. Keep their source inclusion identities;
        # broader option-to-option behavior is still outside this import.
        for row in self.rows[self.roles['rule_mapping']]:
            if row['source_id'] not in self.interior_rows or row['rule_type'] != 'includes':
                continue
            if case_recipes and self.lane == 'grand-sport' and row['source_id'] in ('3LT_AE4_EL9', '3LT_AH2_EL9'):
                continue  # Already translated by the GS E04 recipe.
            self.include(row['source_id'], row['target_id'], interior=True,
                         scope=self.scope(trim=scopes[row['source_id']]['trim_level']))
        if self.lane == 'grand-sport-x':
            # GSX-D02 corrects the absent Z25 inclusion without inventing an
            # interior residual. The leaf retains its independently owned seat.
            for seat in ('AE4', 'AH2'):
                identifier = f'3LT_{seat}_EL9'
                leaf = self.interior_rows[identifier]
                anchor = self.anchor(self.roles['interiors'], leaf)
                condition = self.condition((('any_present', (('interior_id', identifier, 'chosen'),)),), [anchor])
                self.acquisition(identifier + '/Z25', 'Z25', condition, [anchor], scope=self.scope(trim='3lt'))

    def source_rates(self, row_numbers):
        # Preserve the case slice's documented precedence before filling the
        # remaining source rates in workbook order. This is draft precedence;
        # general overlap/release validation remains a separate checkpoint.
        self.rate_order.extend(row_numbers)

    def all_rates(self, *, source_order=True):
        sheet = self.roles['price_rules']
        rows = {r['_row']: r for r in self.rows[sheet]}
        priorities = defaultdict(int)
        order = dict.fromkeys(self.rate_order + list(rows)) if source_order else sorted(rows, key=lambda n: rows[n]['price_rule_id'])
        for number in order:
            row = rows[number]
            if row['price_rule_type'] != 'override':
                raise ValueError('Unsupported source rate kind')
            anchor = self.anchor(sheet, row)
            endpoint = row['condition_option_id']
            if endpoint in self.offerings:
                condition = self.selected(endpoint)
            elif endpoint in self.interior_rows:
                condition = self.condition((('any_present', (('interior_id', endpoint, 'chosen'),)),), [anchor])
            else:
                raise ValueError(f'Unknown price condition endpoint: {endpoint}')
            target = row['target_option_id']
            priorities[target] += 1
            self.rate(row['price_rule_id'], target, condition, row['price_value'], [anchor], priorities[target],
                      self.scope(row.get('body_style_scope'), row.get('trim_level_scope')), row['price_rule_id'])
        decision = {'z06': 'Z06-D06', 'zr1': 'ZR1-D03', 'zr1x': 'ZR1X-D03'}.get(self.lane)
        if decision:
            # The other three lanes already contain this zero rate. These
            # accepted corrections add the missing rate, not a package credit.
            target = self.oid('SC7')
            priorities[target] += 1
            anchor = self.e.anchor(self.review_name, 'owner_review/records/decision_id=' + decision)
            self.rate('accepted/SBT/SC7', 'SC7', self.selected('SBT'), 0,
                      [anchor, self.option_anchor('SC7')], priorities[target], self.scope(body='coupe'))


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


def validate_sources(db, *, allow_sample_option=True):
    """Validate translated payloads, not runtime convergence or release coverage."""
    f.validate(db)
    for relation, columns in {
        'configuration': ('starting_amount_minor', 'basis_id'),
        'acquisition': ('origin_kind', 'peer_policy', 'intent_policy', 'priority'),
        'requirement': ('source_state', 'loss_policy'),
        'option_rate': ('amount_minor', 'basis_id'),
        'choice_group': ('peer_policy',),
        'interior': ('code', 'enabled'),
        'content_aspect': ('name',),
        'content_effect': ('effect_kind', 'value', 'precedence'),
    }.items():
        if db.execute(f'SELECT 1 FROM {relation} WHERE ' + ' OR '.join(c + ' IS NULL' for c in columns)).fetchone():
            raise ValueError(f'Incomplete {relation} payload')
    if db.execute('''SELECT 1 FROM option o WHERE id <> ? AND lifecycle = 'active' AND
        (charge_mode IS NULL OR (charge_mode = 'priced' AND purchase_amount_minor IS NULL))''', (f.SAMPLE_OPTION_ID,)).fetchone():
        raise ValueError('Missing classified purchase price')
    if not allow_sample_option and db.execute("SELECT 1 FROM option WHERE lifecycle = 'active' AND charge_mode IS NULL").fetchone():
        raise ValueError('Missing classified purchase price')
    if db.execute('''SELECT 1 FROM interior_part p JOIN interior i
        ON i.revision_id = p.revision_id AND i.id = p.interior_id
        WHERE p.option_id = i.seat_option_id''').fetchone():
        raise ValueError('Interior part repeats its seat owner')
    if db.execute('''SELECT 1 FROM interior_part p JOIN interior_configuration s
        ON s.revision_id = p.revision_id AND s.interior_id = p.interior_id
        WHERE p.component_id IS NOT NULL AND NOT EXISTS
        (SELECT 1 FROM component_rate r WHERE r.revision_id = p.revision_id
         AND r.component_id = p.component_id AND r.configuration_id = s.configuration_id)''').fetchone():
        raise ValueError('Missing scoped interior component rate')
    for row in db.execute('SELECT revision_id, id, mode FROM condition'):
        clauses = db.execute('SELECT clause_id FROM condition_clause WHERE revision_id = ? AND condition_id = ?', tuple(row[:2])).fetchall()
        if (row['mode'] == 'always') != (len(clauses) == 0):
            raise ValueError('Condition mode/clauses disagree')
        for clause in clauses:
            if not db.execute('SELECT 1 FROM condition_member WHERE revision_id = ? AND condition_id = ? AND clause_id = ?', (*row[:2], clause[0])).fetchone():
                raise ValueError('Empty condition clause')
    for relation, meaning in [('configuration', 'vehicle_destination_included'),
                              ('option', 'option_purchase'), ('option_rate', 'option_purchase'),
                              ('component_rate', 'option_purchase')]:
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
    """Preserved E01–E08 fixture, independently usable for regression checks."""
    _import(db, source_dir, complete=False)


def import_catalog(db, source_dir=f.ROOT / 'docs'):
    """Complete offering data with the bounded behavior recipes; not a release."""
    _import(db, source_dir, complete=True)


def _import(db, source_dir, *, complete):
    """One transaction, including allocation; a changed pinned input is refused."""
    with db:
        f._import_samples(db, source_dir, include_sample_option=not complete)
        evidence = Evidence(db, source_dir, complete=complete)
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
            lane = (OfferingLane if complete else Lane)(db, evidence, name, bases)
            lane.foundation()
            populate(lane)
            if complete:
                lane.interiors()
                lane.all_rates()
        validate_sources(db, allow_sample_option=not complete)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', action='store_true', help='Populate only the original E01–E08 fixture')
    parser.add_argument('--database', type=Path, help='Fresh disposable SQLite path (existing matching imports may be reopened)')
    args = parser.parse_args()
    database = args.database or (DATABASE if args.cases else CATALOG_DATABASE)
    database.parent.mkdir(parents=True, exist_ok=True)
    with closing(f.connect(database)) as db:
        if not db.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchone():
            f.create_schema(db)
        (import_cases if args.cases else import_catalog)(db)
        counts = {t: db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
                  for t in ('configuration', 'option', 'interior', 'interior_part', 'component', 'component_rate',
                            'option_configuration', 'acquisition', 'requirement', 'option_rate')}
        print(json.dumps({'database': str(database), 'counts': counts,
                          'validation': 'source structure passed; general option behavior remains E01–E08; not submission ready'}, indent=2))


if __name__ == '__main__':
    main()
