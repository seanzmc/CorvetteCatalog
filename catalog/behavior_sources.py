"""Translate six retained model lanes into executable draft behavior.

The case and offering importers remain independently usable. This importer adds
source-owned behavior and accepted corrections, never release/publication state.
"""
import argparse
from collections import defaultdict
from contextlib import closing
import json
from pathlib import Path

from catalog import foundation as f
from catalog import evaluator_sources as s

DATABASE = f.ROOT / '.local/foundation/catalog-behavior.sqlite'
FAMILIES = ('rule_mapping', 'rule_groups', 'rule_group_members', 'exclusive_groups',
            'exclusive_group_members', 'color_overrides')


def active(value):
    return str(value).lower() == 'true'


class BehaviorLane(s.OfferingLane):
    def __init__(self, *args):
        super().__init__(*args)
        self.design = self.e.anchor('master-schema-proposal.md', '4-conditions-acquisition-requirements-and-replacement')
        self.groups = {}
        self.accounted = set()
        self.code_ids = {}
        self.sections = {r['section_id']: r for r in self.rows['section_master']}
        self.availability = {(r['option_id'], r['variant_id']): r['status']
                             for r in self.rows[self.roles['availability']]}
        self.overrides = {(r['option_id'], r['variant_id']): r
                          for r in self.rows[self.roles['variant_overrides']] if active(r['active'])}

    def oid(self, code):
        if code in self.code_ids:
            return self.code_ids[code]
        if code in self.code_ids.values():
            return code
        return super().oid(code)

    def option_anchor(self, code):
        oid = self.oid(code)
        if oid in self.offerings:
            return super().option_anchor(oid)
        addition, = [r for r in self.review['accepted_additions'] if self.oid(r['rpo']) == oid]
        return self.review_anchor('accepted_additions', addition['record_id'])

    def foundation(self):
        super().foundation()
        self.code_ids = {r['rpo']: r['id'] for r in self.db.execute(
            "SELECT id, rpo FROM option WHERE revision_id = ? AND lifecycle <> 'retired' AND rpo IS NOT NULL", (self.r,))}
        for oid, row in self.offerings.items():
            for cid in self.scope():
                if row['selectable'] and not self.effective(oid, cid)[2] and (oid, cid) not in self.overrides:
                    self.put('option_presentation_override', 'behavior/' + oid + '/' + cid,
                             {'customer_selectable': 0}, [self.option_anchor(oid)],
                             target={'option_id': oid, 'configuration_id': cid})

    def decision(self, identifier):
        return self.e.anchor(self.review_name, 'owner_review/records/decision_id=' + identifier)

    def availability_target(self, row, availability):
        status, anchors = super().availability_target(row, availability)
        if self.lane == 'grand-sport' and row['rpo'] == 'B4Z':
            return 'available', anchors + [self.decision('GS-D08')]
        return status, anchors

    def account(self, sheet, row, reason='Translated to typed behavior', disposition='translated'):
        key = (sheet, row['_row'])
        if key in self.accounted:
            raise ValueError(f'Duplicate behavior accounting: {self.lane}/{key}')
        anchor = self.anchor(sheet, row)
        f._ensure(self.db, 'source_disposition',
                  {'revision_id': self.r, 'anchor_id': anchor, 'fragment_key': 'behavior'},
                  {'disposition': disposition, 'reason': reason} | self.e.evidence([anchor], self.decisions))
        self.accounted.add(key)

    def canonical(self, oid):
        if self.lane == 'grand-sport' and oid == 'opt_t0e_002':
            return 'opt_t0e_001'
        return oid

    def live(self, oid):
        return oid in self.interior_rows or bool(self.db.execute(
            "SELECT 1 FROM option WHERE revision_id=? AND id=? AND lifecycle <> 'retired'",
            (self.r, oid)).fetchone())

    def usable(self, oid, config):
        return bool(self.db.execute("""SELECT 1 FROM option o JOIN option_configuration c
            ON c.revision_id=o.revision_id AND c.option_id=o.id
            WHERE o.revision_id=? AND o.id=? AND o.lifecycle='active'
            AND c.configuration_id=? AND c.status<>'unavailable'""", (self.r, oid, config)).fetchone())

    def row_scope(self, row, endpoints=()):
        def match(raw, value):
            return raw in (None, '', '*') or value in str(raw).split('|')
        configs = [c['variant_id'] for c in self.configs
                   if match(row.get('body_style_scope'), c['body_style'])
                   and match(row.get('trim_level_scope'), c['trim_level'])
                   and match(row.get('variant_scope'), c['variant_id'])]
        for endpoint in endpoints:
            if endpoint in self.interior_rows:
                configs = [c for c in configs if self.db.execute(
                    'SELECT 1 FROM interior_configuration WHERE revision_id=? AND interior_id=? AND configuration_id=?',
                    (self.r, endpoint, c)).fetchone()]
            else:
                # Keep lifecycle-disabled relationships for their applicable
                # contexts. Lifecycle decides acquisition, not rule existence.
                configs = [c for c in configs if self.availability.get((endpoint, c), 'available') != 'unavailable']
        return configs

    def member(self, oid, state=None):
        oid = self.canonical(oid)
        return ('interior_id', oid, 'chosen') if oid in self.interior_rows else ('option_id', oid, state or 'resolved_selection')

    def when(self, *sets, absent=(), anchors=()):
        clauses = [('any_present', tuple(self.member(o) for o in members)) for members in sets]
        if absent:
            clauses.append(('none_present', tuple(self.member(o) for o in absent)))
        return self.condition(tuple(clauses), anchors)

    def group(self, key, members, anchors, scope, minimum=0, retained=None):
        members = tuple(sorted(set(members)))
        identifier = self.scoped('choice_group', key, {'minimum': minimum, 'maximum': 1, 'peer_policy': 'replace'}, anchors, scope, retained)
        for oid in members:
            self.put('choice_group_member', key + '/' + oid, {}, anchors + [self.option_anchor(oid)],
                     target={'group_id': identifier, 'option_id': oid})
        self.groups[key] = (identifier, members, scope)
        return identifier

    def conflict(self, key, source, targets, anchors, scope=None, activation=None):
        source = self.canonical(source)
        interior = source in self.interior_rows
        identifier = self.scoped('conflict', key, {
            'source_option_id': None if interior else source,
            'source_interior_id': source if interior else None,
            'activation_condition_id': activation or self.condition()}, anchors, self.row_scope({}, (source,)) if scope is None else scope)
        for index, target in enumerate(dict.fromkeys(self.canonical(t) for t in targets), 1):
            self.put('conflict_member', key + '/' + str(index), {
                'option_id': None if target in self.interior_rows else target,
                'interior_id': target if target in self.interior_rows else None}, anchors,
                target={'conflict_id': identifier, 'member_id': str(index)})
        return identifier

    def effective(self, oid, config):
        row = self.offerings[oid]
        override = self.overrides.get((oid, config), {})
        section = override.get('section_id') or row['section_id']
        display = override.get('display_behavior') or row.get('display_behavior')
        selectable = override.get('selectable')
        if selectable is None:
            selectable = row['selectable']
        if display in ('auto_only', 'display_only', 'hidden'):
            selectable = False
        if self.lane == 'z06' and row['rpo'] in ('CFX', 'DRG', 'TR7', 'XFS'):
            selectable = False  # Included-only disclosure rows, no purchase owner.
        return section, display, bool(selectable)

    def substitution(self, source, removed, replacement):
        anchors = [self.option_anchor(c) for c in (source, removed, replacement)]
        self.scoped('equipment_substitution', source + '/' + removed + '/' + replacement,
                    {'condition_id': self.when([self.oid(source)], [self.oid(replacement)], anchors=anchors),
                     'removed_option_id': self.oid(removed), 'replacement_option_id': self.oid(replacement)}, anchors)

    def choices(self):
        # Expand source sections now. Evaluation never reads presentation sections.
        for config in self.configs:
            cid = config['variant_id']
            groups = defaultdict(list)
            for oid in self.offerings:
                section, _, selectable = self.effective(oid, cid)
                if self.live(oid) and self.availability[(oid, cid)] != 'unavailable' and selectable:
                    groups[section].append(oid)
            # Seats belong to the chosen interior; they still participate in the
            # explicit group, but no arbitrary leaf is chosen to satisfy it.
            for sid, members in groups.items():
                section = self.sections[sid]
                if section['selection_mode'] in ('single_select_req', 'single_select_opt'):
                    self.group('section/' + cid + '/' + sid, members,
                               [self.anchor('section_master', section)] +
                               [self.anchor(self.roles['variant_overrides'], self.overrides[o, cid])
                                for o in members if (o, cid) in self.overrides], [cid],
                               int(section['selection_mode'] == 'single_select_req'))
        sheet, ms = self.roles['exclusive_groups'], self.roles['exclusive_group_members']
        for row in self.rows[sheet]:
            if row['selection_mode'] not in ('single_within_group', 'required_single_within_group'):
                raise ValueError('Unknown exclusive group mode')
            members = [r for r in self.rows[ms] if r['group_id'] == row['group_id']]
            targets = [self.canonical(r['option_id']) for r in members if active(r['active']) and self.live(self.canonical(r['option_id']))]
            if active(row['active']) and targets:
                self.group(row['group_id'], targets, [self.anchor(sheet, row)] + [self.anchor(ms, r) for r in members],
                           self.scope(), int(row['selection_mode'] == 'required_single_within_group'))
                self.account(sheet, row)
            else:
                self.account(sheet, row, 'Inactive or no retained members', 'inactive')
            for member in members:
                self.account(ms, member, 'Explicit exclusive membership' if active(member['active']) and self.live(self.canonical(member['option_id'])) else 'Inactive/retired membership',
                             'translated' if active(member['active']) and self.live(self.canonical(member['option_id'])) else 'inactive')
        # DTC additions join the concrete stripe choice group (not DUW edges).
        if 'DTC' in self.code_ids and self.oid('DTC') not in self.offerings:
            oid = self.oid('DTC')
            for key, (group, members, _) in self.groups.items():
                if key.startswith('section/') and key.endswith('/sec_stri_001'):
                    self.put('choice_group_member', key + '/DTC', {}, [self.option_anchor(oid)],
                             target={'group_id': group, 'option_id': oid})

    def relationships(self):
        group_sheet, member_sheet = self.roles['rule_groups'], self.roles['rule_group_members']
        grouped = set()
        for row in self.rows[group_sheet]:
            members = [r for r in self.rows[member_sheet] if r['group_id'] == row['group_id']]
            source = self.canonical(row['source_id'])
            targets = [self.canonical(r['target_id']) for r in members if active(r['active']) and self.live(self.canonical(r['target_id']))]
            if not active(row['active']) or not self.live(source) or not targets:
                self.account(group_sheet, row, 'Inactive or retired group endpoint', 'inactive')
                for m in members:
                    self.account(member_sheet, m, 'Inactive or retired group', 'inactive')
                continue
            anchors = [self.anchor(group_sheet, row)] + [self.anchor(member_sheet, r) for r in members]
            if self.lane == 'stingray' and row['group_id'] == 'grp_5v7_spoiler_requirement':
                targets.append(self.oid('5ZW'))
                anchors.append(self.decision('ST-D08'))
            if row['group_type'] == 'requires_any':
                grouped.update((source, t) for t in targets)
                scope = self.row_scope(row, (source,))
                # Each current alternative set is a source-owned wheel,
                # package, paint or spoiler peer set; retain its identity.
                group = self.group(row['group_id'], targets, anchors, scope, retained=row['group_id'])
                occupied = self.condition((('any_present', (('group_id', group, 'occupied'),)),), anchors)
                self.requirement(row['group_id'], source, occupied, anchors,
                                 interior=source in self.interior_rows, scope=scope)
            elif row['group_type'] == 'excludes_any':
                self.conflict(row['group_id'], source, targets, anchors, self.row_scope(row, (source,)))
            else:
                raise ValueError('Unknown grouped rule type')
            self.account(group_sheet, row)
            for member in members:
                self.account(member_sheet, member, 'Grouped typed endpoint' if active(member['active']) and self.live(self.canonical(member['target_id'])) else 'Inactive or retired endpoint',
                             'translated' if active(member['active']) and self.live(self.canonical(member['target_id'])) else 'inactive')
        removed = {r['rule_id'] for decision in self.review['records'] for r in decision.get('target_rule_removals', [])}
        sheet = self.roles['rule_mapping']
        for row in self.rows[sheet]:
            source, target = (self.canonical(row[k]) for k in ('source_id', 'target_id'))
            reason = None
            if not self.live(source) or not self.live(target):
                reason = 'Retired offering; original endpoint is not renamed'
            elif row['rule_id'] in removed:
                reason = 'GSX-D14 explicitly retires LS6 rule'
            elif row['rule_type'] == 'requires' and (source, target) in grouped:
                reason = 'Superseded by source requires-any group'
            elif self.lane == 'stingray' and target == self.oid('ZF1') and source in [self.oid(c) for c in ('5ZU', '5ZZ')]:
                reason = 'ST-D04: high wings remove T0A without acquiring ZF1'
            elif self.lane in ('zr1', 'zr1x') and source == self.oid('CFC') and target == self.oid('GBA'):
                reason = 'D01: convertible standard CFC does not force black paint'
            if reason:
                self.account(sheet, row, reason, 'superseded')
                continue
            anchors = [self.anchor(sheet, row)]
            scope = self.row_scope(row, (source,))
            # Convertible engine-cover requirements do not prohibit the coupe
            # purchase; coupe lighting inclusions do not acquire unavailable D3V.
            if row['rule_type'] == 'requires' and target == self.code_ids.get('ZZ3'):
                scope = [c for c in scope if c in self.scope('convertible')]
            if row['rule_type'] == 'includes':
                if source in self.interior_rows:
                    # Already owned by OfferingLane.interiors; retain its cause.
                    self.account(sheet, row, 'Interior-owned inclusion populated with offering')
                    continue
                scope = [c for c in scope if c in self.row_scope({}, (target,))]
                peer = 'locked'
                if target in [self.code_ids.get(c) for c in ('BC7', 'VWD', 'ROY')]:
                    peer = 'yield_to_explicit'
                if self.lane == 'grand-sport' and source == self.oid('FEB') and target == self.oid('J56'):
                    peer = 'yield_to_explicit'
                if self.lane == 'stingray' and source == self.oid('Z51') and target == self.oid('T0A'):
                    peer = 'yield_to_explicit'
                if self.lane == 'z06' and source == self.oid('PDB') and target == self.oid('J6D'):
                    peer = 'yield_to_explicit'  # Z06-D01 permits compatible paid calipers.
                if self.lane == 'grand-sport-x' and source == self.oid('J57') and target == self.oid('J6D'):
                    peer = 'yield_to_explicit'
                condition = self.when([source], anchors=anchors)
                if self.lane == 'z06' and source == self.oid('Z07') and target == self.oid('T0F'):
                    peer = 'yield_to_explicit'
                    condition = self.when([source], absent=[self.oid('PDD'), self.oid('PDF')], anchors=anchors)
                if self.lane == 'stingray' and source == self.oid('Z51') and target == self.oid('FE3'):
                    peer = 'yield_to_explicit'
                intent = 'absorb_prior' if self.lane == 'stingray' and source == self.oid('PCX') else 'preserve_prior'
                self.acquisition(row['rule_id'], target, condition, anchors, peer=peer, intent=intent,
                                 scope=scope, retained=row['rule_id'], priority=10)
                if peer == 'locked':
                    self.requirement(row['rule_id'] + '/child', source, self.when([target], anchors=anchors), anchors, scope=scope)
            elif row['rule_type'] == 'requires':
                self.requirement(row['rule_id'], source, self.when([target], anchors=anchors), anchors,
                                 interior=source in self.interior_rows, scope=scope, retained=row['rule_id'])
            elif row['rule_type'] == 'excludes':
                # ST-D09 explicitly permits RNX under Z51+ZF1.
                activation = None
                if self.lane == 'stingray' and {source, target} == {self.oid('RNX'), self.oid('Z51')}:
                    activation = self.when(absent=[self.oid('ZF1')], anchors=anchors + [self.decision('ST-D09')])
                self.conflict(row['rule_id'], source, [target], anchors, scope, activation)
            else:
                raise ValueError('Unknown direct rule kind')
            self.account(sheet, row)

    def defaults(self):
        rows = self.rows['default_selection_rules']
        explicit_targets = {r['target_option_id'] for r in rows if active(r['active'])}
        for row in rows:
            oid = self.canonical(row['target_option_id'])
            if not active(row['active']) or not self.live(oid):
                self.account('default_selection_rules', row, 'Inactive default', 'inactive')
                continue
            anchor = self.anchor('default_selection_rules', row)
            for config in self.row_scope(row, (oid,)):
                if not self.usable(oid, config):
                    continue
                kind = row['condition_type']
                condition = self.condition()
                if kind == 'unless_selected_rpo':
                    condition = self.when(absent=[self.oid(row['condition_id'])], anchors=[anchor])
                elif kind == 'when_selected_unless_selected_section':
                    condition = self.when([row['condition_id']], anchors=[anchor])
                elif kind not in ('always', 'unless_selected_section'):
                    raise ValueError(f'Unknown default condition: {kind}')
                # Explicit membership resolves section vacancy and peer yielding.
                sid = row['condition_id'] if kind == 'unless_selected_section' else self.effective(oid, config)[0]
                members = [o for o in self.offerings if self.effective(o, config)[0] == sid
                           and self.live(o) and self.availability[(o, config)] != 'unavailable']
                if kind in ('unless_selected_section', 'when_selected_unless_selected_section') and len(members) > 1:
                    # Vacancy is a predicate, not an exclusivity constraint on
                    # a multi-select source section (e.g. EDU plus CBF).
                    trigger = [[row['condition_id']]] if kind == 'when_selected_unless_selected_section' else []
                    condition = self.when(*trigger, absent=[o for o in members if o != oid], anchors=[anchor])
                peer = 'locked' if oid == self.code_ids.get('R8E') else 'yield_to_explicit'
                self.acquisition(row['rule_id'] + '/' + config, oid, condition, [anchor], origin='default', peer=peer,
                                 priority=int(row['priority']), scope=[config])
            self.account('default_selection_rules', row)
        for config in self.configs:
            cid = config['variant_id']
            for oid, row in self.offerings.items():
                if not self.usable(oid, cid):
                    continue
                section, display, selectable = self.effective(oid, cid)
                status = self.availability[oid, cid]
                anchor = self.option_anchor(oid)
                default = display == 'default_selected'
                if selectable and status == 'standard' and self.sections[section]['selection_mode'] == 'single_select_req':
                    standards = [o for o in self.offerings if self.effective(o, cid)[0] == section
                                 and self.effective(o, cid)[2] and self.usable(o, cid) and self.availability[o, cid] == 'standard']
                    default |= len(standards) == 1
                # Workbook default_selected restoration is independent of a
                # generated default's section-vacancy predicate (frozen
                # addWorkbookDefaultChoices). For example CBF must not leave
                # the EFR/EDU/EFY required accent group empty.
                if oid in explicit_targets and not default:
                    continue
                # B4Z is conditional in GS even when the baseline marks it standard.
                if self.lane == 'grand-sport' and oid == self.oid('B4Z'):
                    continue
                if not selectable and status == 'standard' and display != 'auto_only':
                    self.acquisition('standard/' + cid + '/' + oid, oid, self.condition(), [anchor], origin='standard',
                                     peer='yield_to_explicit', priority=1000, scope=[cid])
                elif default and row['rpo'] not in ('AQ9', 'AH2', 'AE4'):
                    self.acquisition('default/' + cid + '/' + oid, oid, self.condition(), [anchor], origin='default',
                                     peer='yield_to_explicit', priority=1000, scope=[cid])

    def interior_conditions(self):
        for row in self.rows['model_interior_scope']:
            if row.get('requires_option_id'):
                source, target = row['interior_id'], self.canonical(row['requires_option_id'])
                anchor = self.anchor('model_interior_scope', row)
                self.requirement('interior/' + source, source, self.when([target], anchors=[anchor]), [anchor],
                                 interior=True, scope=self.row_scope({}, (source,)))
        sheet = self.roles['color_overrides']
        for row in self.rows[sheet]:
            interior, option, target = row['interior_id'], row['option_id'], row['adds_rpo']
            if interior not in self.interior_rows:
                raise ValueError('Foreign interior color condition')
            anchor = self.anchor(sheet, row)
            condition = self.when([interior], [option], anchors=[anchor])
            self.acquisition('color/' + str(row['_row']), target, condition, [anchor], origin='dependency',
                             scope=self.row_scope({}, (interior, option, target)), priority=10000 + row['_row'])
            self.account(sheet, row)

    def corrections(self):
        """Accepted targets; original workbook rules remain immutable evidence."""
        lane = self.lane
        def conflict(source, targets, decision, scope=None, policy_anchors=()):
            anchor = self.decision(decision)
            self.conflict('accepted/' + source + '/' + decision, self.oid(source), [self.oid(t) for t in targets.split()],
                          [anchor, self.option_anchor(source), *policy_anchors], scope)
        def include(source, target, decision, peer='locked', origin='included', scope=None):
            anchors = [self.decision(decision), self.option_anchor(source), self.option_anchor(target)]
            self.acquisition('accepted/' + source + '/' + target, target, self.when([self.oid(source)], anchors=anchors),
                             anchors, peer=peer, origin=origin, scope=scope, priority=5)
        dtc_decision = {'stingray': 'ST-D01', 'grand-sport': 'GS-D01', 'grand-sport-x': 'GSX-D01',
                        'z06': 'Z06-D09', 'zr1': 'ZR1-D05', 'zr1x': 'ZR1X-D05'}[lane]
        # Each set is selected from that lane's retained guide mentions; these
        # are not mechanically renamed DUW relationships.
        dtc_peers = {
            'stingray': 'PDV PCX SFZ R88 SHT SB7 CF8',
            'grand-sport': 'PDA SFZ R88 VPW VPO SNE SHT CF8 Z15',
            'grand-sport-x': 'PDA SFZ R88 VPW VPO SNE SHT CF8 Z15',
            'z06': 'PDA PCZ SFZ R88 VPW VPO SNE SHT CF8',
            'zr1': 'SFZ R88 SB9', 'zr1x': 'SFZ R88 SB9',
        }
        conflict('DTC', 'GTR ' + dtc_peers[lane], dtc_decision)
        sai_decision = {'stingray': 'ST-D02', 'grand-sport': 'GS-D02', 'grand-sport-x': 'GSX-D07',
                        'z06': 'Z06-D09', 'zr1': 'ZR1-D07', 'zr1x': 'ZR1X-D07'}[lane]
        conflict('SAI', 'V8X', sai_decision, self.scope(trim='3lt' if lane in ('stingray', 'grand-sport', 'grand-sport-x') else '3lz'))
        if lane in ('grand-sport', 'grand-sport-x', 'z06'):
            stripes = 'DPB DPC DPG DPL DPT DSY DSZ DT0 DTC DTH DUB DUE DUK DZU DZV DZX'
            decision = {'grand-sport': 'GS-D12', 'grand-sport-x': 'GSX-D06', 'z06': 'Z06-D05'}[lane]
            # These decisions retain the exclusions, but their refusal UI was
            # superseded on September 11. Stripes, badges and packages all use
            # notice/confirm/cancel; confirmation must never permit coexistence.
            policy = [self.e.anchor(s.POLICY, 'precedence'),
                      self.e.anchor(s.POLICY, 'model_overrides/' + self.data['model_key'])]
            conflict('VPW', stripes + (' SHT VPO Z15' if lane != 'z06' else ' PCZ SHT VPO'), decision, policy_anchors=policy)
            conflict('VPO', stripes + (' PDA SNE VPW Z15' if lane != 'z06' else ' EYK PDA SNE VPW'), decision, policy_anchors=policy)
        if lane in ('grand-sport', 'grand-sport-x'):
            decision = 'GS-D04' if lane == 'grand-sport' else 'GSX-D04'
            for stripe, paints in [('DMX', 'G26 G4Z GBK GKZ GPH'), ('DMV', 'G26 G4Z GBK GKZ GPH'),
                                  ('DMY', 'G26 G4Z GBK GTR'), ('DMW', 'G26 G4Z GBK')]:
                anchors = [self.decision(decision), self.option_anchor(stripe)]
                condition = self.when([self.oid(stripe)], [self.oid(p) for p in paints.split()], anchors=anchors)
                self.acquisition('accepted/' + stripe + '/D84', 'D84', condition, anchors,
                                 origin='dependency', scope=self.scope('convertible'), priority=5)
                self.requirement('accepted/' + stripe + '/D84', stripe, self.selected('D84'), anchors,
                                 activation=condition, scope=self.scope('convertible'))
            for hash_code in '17A 20A 55A 75A 97A DX4'.split():
                self.requirement('hash/' + hash_code, hash_code, self.selected('Z15'), [self.option_anchor(hash_code)])
        if lane == 'stingray':
            anchors = [self.decision('ST-D04')]
            condition = self.when([self.oid('TVS')], [self.oid('Z51')], anchors=anchors)
            self.acquisition('accepted/TVS/ZF1', 'ZF1', condition, anchors, origin='dependency', priority=5)
            for code in ('5ZU', '5ZZ', 'ZF1', 'TVS'):
                self.scoped('equipment_substitution', 'accepted/' + code + '/T0A', {
                    'condition_id': self.selected(code), 'removed_option_id': self.oid('T0A'), 'replacement_option_id': self.oid(code)},
                    anchors, self.scope())
        if lane == 'grand-sport':
            anchors = [self.decision('GS-D08')]
            self.acquisition('accepted/B4Z', 'B4Z', self.when([self.oid('FEB'), self.oid('FEY')], anchors=anchors), anchors, priority=5)
            self.requirement('accepted/B4Z', 'B4Z', self.when([self.oid('FEB'), self.oid('FEY')], anchors=anchors), anchors)
        if lane in ('grand-sport', 'z06'):
            decision = 'GS-D07' if lane == 'grand-sport' else 'Z06-D01'
            # Explicit gray/red standard calipers cannot survive losing the
            # ceramic brake requirement; the section default restores J6A.
            conflict('J57', 'J6A', decision)
            if lane == 'z06':
                anchors = [self.decision(decision)]
                self.acquisition('accepted/J57/J6D', 'J6D', self.when([self.oid('J57')], absent=[self.oid('PDB')], anchors=anchors),
                                 anchors, origin='default', peer='yield_to_explicit', priority=5)
        if lane == 'z06':
            for code in ('5DH', '5DK'):
                conflict(code, 'R8C SPZ SFE SPY S47 ROY ROZ STZ', 'Z06-D03')
            for stripes, paints in [('DUE DPB', 'GTR'), ('DUK DPL DSZ DZX', 'GKZ GPH'),
                                    ('DPC DT0 DZU', 'GBK'), ('DPG DSY', 'G26')]:
                for stripe in stripes.split():
                    conflict(stripe, paints, 'Z06-D04')
            for target in ('5DK', 'SFZ', 'SHT', 'VPO'):
                include('PCZ', target, 'Z06-D02')
                self.rate('accepted/PCZ/' + target, target, self.selected('PCZ'), 0,
                          [self.decision('Z06-D02')], priority=10000)
            conflict('PCZ', 'R8C SPZ SFE SPY S47 ROY ROZ STZ EYK PDA SNE VPW DPB DPC DPG DPL DPT DSY DSZ DT0 DTC DTH DUB DUE DUK DZU DZV DZX', 'Z06-D02')
            conflict('RXI', 'SLN', 'Z06-D07')
            self.replacement('PDB', 'Z07', 'PDD', [self.decision('Z06-D11'), self.e.anchor(s.POLICY, 'model_overrides/z06/pdb_z07_interaction')])
            derived_anchors = []
            derived = self.data['runtime_derived_relationships']['records']
            expected = {('derived_opt_' + c + '_001_replaces_opt_cbf_001', 'opt_' + c + '_001', 'excludes', 'opt_cbf_001')
                        for c in ('pdd', 'pdf', 'z07', 't0f', 't0g')}
            if len(derived) != 5 or {(r['rule_id'], r['source_id'], r['rule_type'], r['target_id']) for r in derived} != expected:
                raise ValueError('Unexpected derived replacement permission')
            for row in derived:
                anchor = self.e.anchor(self.name, 'runtime_derived_relationships/records/rule_id=' + row['rule_id'])
                anchors = [anchor, self.e.anchor(self.name, 'sources/runtime_commit'),
                           self.e.anchor(s.DESIGN, 'n3-and-o8--full-output-and-release-completion')]
                derived_anchors.extend(anchors)
                self.conflict(row['rule_id'], row['source_id'], [row['target_id']], anchors)
            # One complete plan removes every live incompatible cause; absent
            # endpoints are inert. This avoids overlapping per-child plans for
            # PDD/PDF -> Z07 -> aero while retaining independent aero roots.
            targets = ['PDD', 'PDF', 'Z07', 'T0F', 'T0G', 'CFZ', 'CFV']
            plan = self.scoped('replacement_plan', 'CBF/complete', {
                'requested_option_id': self.oid('CBF'),
                'condition_id': self.when([self.oid(c) for c in targets], anchors=derived_anchors)}, derived_anchors)
            for position, code in enumerate(targets + ['CBF'], 1):
                self.put('replacement_action', 'CBF/complete/' + code,
                         {'option_id': self.oid(code), 'action': 'add' if code == 'CBF' else 'remove',
                          'intent_effect': 'commit_purchase' if code == 'CBF' else None}, derived_anchors,
                         target={'plan_id': plan, 'position': position})
        if lane in ('z06', 'zr1', 'zr1x'):
            leaves = [r['interior_id'] for r in self.rows['interior_components'] if r['rpo'] == 'N2Z']
            anchors = [self.anchor('interior_components', r) for r in self.rows['interior_components'] if r['rpo'] == 'N2Z']
            self.scoped('equipment_substitution', 'N2Z/N3W', {
                'condition_id': self.when(leaves, anchors=anchors), 'removed_option_id': self.oid('N3W'),
                'replacement_option_id': None}, anchors)
        substitutions = {
            'stingray': [('Z51', 'JL9', 'J55'), ('Z51', 'M1L', 'M1N'), ('Z51', 'G0J', 'G0K'), ('Z51', 'XFN', 'QTU'), ('FE4', 'FE3', 'FE4')],
            'grand-sport': [('FEB', 'JX6', 'J56'), ('FEY', 'JX6', 'J57'), ('FEY', 'J56', 'J57'), ('FEB', 'XFT', 'XFR'), ('FEY', 'XFT', 'XFS')],
            'grand-sport-x': [('FED', 'XFT', 'XFR')],
            'z06': [('Z07', 'FE6', 'FE7'), ('Z07', 'XFR', 'XFS')],
            'zr1': [('ZTK', 'J58', 'J59'), ('ZTK', 'FE8', 'FEJ'), ('ZTK', 'XFR', 'XFS')],
            'zr1x': [('ZTK', 'FEH', 'FEZ'), ('ZTK', 'XFR', 'XFS')],
        }
        for source, old, new in substitutions[lane]:
            self.substitution(source, old, new)

    def content(self):
        """Supplied physical content has no invented purchasable option/charge."""
        aspects = {}
        def effect(name, key, value, sets, codes, scope=None, precedence=1, kind='replace', extra=()):
            anchors = [self.option_anchor(c) for c in codes] + list(extra)
            if name not in aspects:
                aspects[name] = self.put('content_aspect', name, {'name': name}, [self.design])
            self.scoped('content_effect', key, {
                'aspect_id': aspects[name], 'condition_id': self.when(*[[self.oid(c) for c in group] for group in sets], anchors=anchors),
                'effect_kind': kind, 'value': value, 'precedence': precedence}, anchors, scope)
        wings = {'stingray': ['5ZU', '5ZZ', '5ZW'], 'grand-sport': ['5ZV', 'T0F'],
                 'grand-sport-x': ['5ZV'], 'z06': ['5V5', '5ZV', 'T0F', 'T0G']}
        # Z06's WKR disclosure also mentions 5ZW, which is not a Z06 offering.
        # Preserve that text as evidence; do not invent a selectable identity.
        if self.lane in wings:
            effect('car_cover_version', 'WKR/high-wing', 'high-wing version', [['WKR'], wings[self.lane]], ['WKR'])
        if self.lane in ('grand-sport', 'grand-sport-x'):
            effect('roof_stripe', 'D84/stripe', 'center stripe omitted from roof',
                   [['D84'], ['DMU', 'DMV', 'DMW', 'DMX', 'DMY']],
                   ['D84', 'DMU', 'DMV', 'DMW', 'DMX', 'DMY'], self.scope('convertible'))
        if self.lane in ('grand-sport', 'grand-sport-x', 'z06'):
            effect('rocker_splitter_finish', 'EFR/CFV', 'visible carbon fiber replaces Carbon Flash on rockers and splitter',
                   [['EFR'], ['CFV']], ['EFR', 'CFV'])
            for precedence, ground in enumerate(('CFV', 'CFZ'), 1):
                effect('splitter_finish', 'EDU/' + ground, 'ground-effects finish replaces body-color splitter',
                       [['EDU'], [ground]], ['EDU', ground], precedence=precedence)
                if self.lane == 'z06':
                    effect('rocker_finish', 'EFY/' + ground, 'ground-effects finish replaces body-color rockers',
                           [['EFY'], [ground]], ['EFY', ground], precedence=precedence)
        if self.lane == 'z06':
            for wheel in ('5DH', '5DK'):
                effect('second_wheel_set_hardware', wheel + '/hardware', 'black lug nuts and locks supplied with second wheel set',
                       [[wheel]], [wheel], extra=[self.decision('Z06-D03')])
            effect('second_wheel_set_caps', '5DK/caps', 'Tech Bronze center caps supplied with second wheel set',
                   [['5DK']], ['5DK'], extra=[self.decision('Z06-D03')])
        effect('additional_roof_panel', 'SBT/panel', 'additional transparent removable roof panel', [['SBT']], ['SBT'], self.scope('coupe'))
        if self.lane in ('zr1', 'zr1x'):
            effect('convertible_roof_trim', 'CFC/default', 'Carbon Flash nacelles, A-pillars and header',
                   [['CFC']], ['CFC'], self.scope('convertible'), precedence=2,
                   extra=[self.e.anchor(self.name, 'guide_rows/Exterior 5!A9:K9')])
            effect('convertible_roof_trim', 'CFC/black', 'body-color nacelles, A-pillars and header with black exterior paint',
                   [['CFC'], ['GBA']], ['CFC', 'GBA'], self.scope('convertible'),
                   extra=[self.decision('ZR1-D01' if self.lane == 'zr1' else 'ZR1X-D01'),
                          self.e.anchor(self.name, 'guide_rows/Exterior 5!A9:K9')])
            effect('exterior_accents', 'EFR/scope', 'Carbon Flash side vents and front/rear grille accents',
                   [['EFR']], ['EFR'], extra=[self.e.anchor(self.name, 'guide_rows/Exterior 5!A13:K13')])
            effect('tonneau_grille', 'EFR/tonneau', 'Carbon Flash tonneau grille', [['EFR']], ['EFR'], self.scope('convertible'))

    def translate(self):
        self.foundation()
        self.interiors(case_recipes=False)
        self.choices()
        self.relationships()
        self.defaults()
        self.interior_conditions()
        # Distinct amounts are configuration-disjoint or mutually exclusive
        # wheel conditions; equal-amount causes share one charge. Source row
        # order is not business precedence in the complete behavior import.
        self.all_rates(source_order=False)
        self.corrections()
        self.content()
        expected = {(self.roles[role], r['_row']) for role in FAMILIES for r in self.rows[self.roles[role]]}
        expected |= {('default_selection_rules', r['_row']) for r in self.rows['default_selection_rules']}
        if self.accounted != expected:
            raise ValueError(f'Unaccounted behavior rows: {expected ^ self.accounted}')


def import_behavior(db, source_dir=f.ROOT / 'docs'):
    with db:
        if db.execute('SELECT 1 FROM acquisition').fetchone() and not db.execute(
                "SELECT 1 FROM source_disposition WHERE fragment_key='behavior'").fetchone():
            raise ValueError('Different projection; create a fresh behavior database')
        f._import_samples(db, source_dir, include_sample_option=False)
        evidence = s.Evidence(db, source_dir, complete=True)
        policy = json.loads((Path(source_dir) / s.POLICY).read_text())
        if policy['review_state'] != 'accepted' or policy['direct_dependency_removal']['review_state'] != 'accepted':
            raise ValueError('Unaccepted common interaction policy')
        bases = {}
        for meaning in ('vehicle_destination_included', 'option_purchase'):
            anchors = [evidence.anchor(s.DESIGN, 'reading-the-populated-rows')]
            for lane in f.LANES:
                review = json.loads((Path(source_dir) / (lane + '-owner-decisions.json')).read_text())['owner_review']
                if review['currency_code'] != 'USD':
                    raise ValueError('Unexpected source currency')
                anchors.append(evidence.anchor(lane + '-owner-decisions.json', 'owner_review/currency_code'))
            bases[meaning] = f._allocated(db, 'price_basis', 'basis_id', {'currency': 'USD', 'amount_meaning': meaning},
                {'minor_units_per_unit': 100, 'resolution_state': 'accepted'} | evidence.evidence(anchors, evidence.decisions('stingray')))
        for lane in f.LANES:
            BehaviorLane(db, evidence, lane, bases).translate()
        s.validate_sources(db, allow_sample_option=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=DATABASE)
    args = parser.parse_args()
    args.database.parent.mkdir(parents=True, exist_ok=True)
    with closing(f.connect(args.database)) as db:
        if not db.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchone():
            f.create_schema(db)
        import_behavior(db)
        print(json.dumps({'database': str(args.database), 'source_accounting':
            dict(db.execute("SELECT disposition, COUNT(*) FROM source_disposition WHERE fragment_key='behavior' GROUP BY disposition")),
            'boundary': 'draft behavior; semantic overlap and release validation remain separate'}, indent=2))


if __name__ == '__main__':
    main()
