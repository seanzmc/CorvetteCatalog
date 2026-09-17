"""Finite, model-scoped behavior audit; no release or publication authority.

Witnesses come from typed conditions, never from a recorded evaluator output.
Every unsuccessful witness is reported for review, not counted as a passing test.
"""
import argparse
from collections import Counter
from itertools import combinations, product
from functools import lru_cache
import json
import hashlib
from pathlib import Path

from catalog import foundation as f
from catalog.behavior_sources import import_behavior
from catalog.evaluator import Evaluator, EvaluationError, Session
from catalog.foundation_schema import SCOPES


def endpoint(row, prefix='source_'):
    return row.get(prefix + 'option_id') or 'interior:' + row[prefix + 'interior_id']


def present(state, item):
    return state.interior_id == item[9:] if item.startswith('interior:') else item in state.resolved


class Audit:
    def __init__(self, db, revision):
        self.ev = Evaluator(db, revision)
        self.db = db
        self.witnesses = {}
        self.witness_reasons = {}
        self.transactions = {}
        self.errors = Counter()
        e = self.ev
        self.scope_configs = {table: {row['id']: {c for rid,c in e.scopes[table] if rid == row['id']} for row in e.rows[table]} for table in SCOPES}
        self.reverse_implications = {}
        self.interior_only_sources = {}
        self.implications = {}
        for config in e.configs:
            rows = []
            for row in e.scoped('acquisition', config):
                target = row['target_option_id']
                if row['peer_policy'] != 'locked' and (e.clauses[row['condition_id']] or
                        any(target in e.members[g['id']] and len(e.members[g['id']]) > 1 for g in e.scoped('choice_group', config)) or
                        any(endpoint(r) == target for r in e.scoped('conflict', config)) or
                        any(m['option_id'] == target for m in e.rows['conflict_member'])):
                    continue
                rows.append((target, tuple(self.recipes(row['condition_id']))))
            self.implications[config] = rows
            reverse = []
            interior_sources = {}
            for oid in e.options:
                if self.selectable(config, oid):
                    continue
                ways = [yes for row in e.scoped('acquisition', config) if row['target_option_id'] == oid
                        for yes, no in self.recipes(row['condition_id'])]
                ways.extend(frozenset({'interior:' + leaf}) for leaf, c in e.interior_scopes if c == config and
                            (e.interiors[leaf]['seat_option_id'] == oid or any(
                                p['interior_id'] == leaf and p['option_id'] == oid for p in e.rows['interior_part'])))
                if ways:
                    leaves = [{x for x in way if x.startswith('interior:')} for way in ways]
                    if all(leaves):
                        interior_sources[oid] = set().union(*leaves)
                    common = frozenset.intersection(*ways)
                    if common:
                        reverse.append((oid, common))
            self.reverse_implications[config] = reverse
            self.interior_only_sources[config] = interior_sources

    def selectable(self, config, oid):
        e = self.ev
        return (e.eligible(oid, config) and e.options[oid]['customer_selectable'] and
                not any(r['configuration_id'] == config and r['option_id'] == oid and not r['customer_selectable']
                        for r in e.rows['option_presentation_override']))

    def recipes(self, cid, truth=True):
        """DNF choices for all/any/none predicates, including explicit groups."""
        e = self.ev
        clauses = e.clauses[cid]
        if not clauses:
            if truth:
                yield frozenset(), frozenset()
            return
        terms = []
        for clause in clauses:
            members = []
            for m in e.condition_members[cid, clause['clause_id']]:
                members.extend(sorted(e.members[m['group_id']]) if m['group_id'] else [endpoint(m, '')])
            positive = clause['mode'] == 'any_present'
            terms.append([(frozenset({x}), frozenset()) for x in members] if positive else
                         [(frozenset(), frozenset(members))])
        if truth:
            for parts in product(*terms):
                yield frozenset().union(*(p[0] for p in parts)), frozenset().union(*(p[1] for p in parts))
        else:
            # NOT(all clauses): falsifying any one clause suffices.
            for clause in clauses:
                members = []
                for m in e.condition_members[cid, clause['clause_id']]:
                    members.extend(sorted(e.members[m['group_id']]) if m['group_id'] else [endpoint(m, '')])
                if clause['mode'] == 'any_present':
                    yield frozenset(), frozenset(members)
                else:
                    for x in members:
                        yield frozenset({x}), frozenset()

    def witness(self, config, wanted=(), absent=()):
        key = config, frozenset(wanted), frozenset(absent)
        if key in self.witnesses:
            return self.witnesses[key]
        e = self.ev
        seen = set()
        reasons = Counter()

        def search(want, no, intent=(), interior=None):
            signature = want, no, intent, interior
            if signature in seen:
                return None
            seen.add(signature)
            proof = self.disjoint(config, want, no)
            if proof:
                reasons[proof] += 1
                return None
            leaves = {x[9:] for x in want if x.startswith('interior:')}
            if len(leaves) > 1:
                reasons['mutually exclusive interiors'] += 1
                return None
            if leaves:
                interior = next(iter(leaves))
                if (interior, config) not in e.interior_scopes:
                    reasons['interior out of scope'] += 1
                    return None
            try:
                causes, _ = e.closure(config, intent, interior, resolving=True)
            except EvaluationError as exc:
                reasons[str(exc)] += 1
                return None
            roots = e.roots(causes)
            has = set(roots) | ({'interior:' + interior} if interior else set())
            missing = sorted(want - has, key=lambda x: (not self.selectable(config, x), x))
            if missing:
                oid = missing[0]
                if oid.startswith('interior:'):
                    return None
                if self.selectable(config, oid) and oid not in intent:
                    result = search(want, no, tuple(sorted((*intent, oid))), interior)
                    if result:
                        return result
                for row in e.scoped('acquisition', config):
                    if row['target_option_id'] == oid:
                        for yes, nots in self.recipes(row['condition_id']):
                            if yes.issubset(want) and nots.issubset(no):
                                continue
                            result = search(want | yes, no | nots, intent, interior)
                            if result:
                                return result
                # Seats/belts/trim parts can be acquired through their actual leaf.
                for leaf in sorted(e.interiors):
                    if (leaf, config) not in e.interior_scopes or interior:
                        continue
                    if e.interiors[leaf]['seat_option_id'] == oid or any(
                            r['interior_id'] == leaf and r['option_id'] == oid for r in e.rows['interior_part']):
                        result = search(want | {'interior:' + leaf}, no, intent, leaf)
                        if result:
                            return result
                reasons['no eligible acquisition for ' + oid] += 1
                return None
            for r in e.scoped('requirement', config):
                if endpoint(r) in has and e.condition(r['activation_condition_id'], config, intent, interior, roots)[0] and not e.condition(r['satisfaction_condition_id'], config, intent, interior, roots)[0]:
                    for yes, nots in self.recipes(r['satisfaction_condition_id']):
                        result = search(want | yes, no | nots, intent, interior)
                        if result:
                            return result
                    reasons['unsatisfied requirement ' + r['id']] += 1
                    return None
            if has & no:
                oid = sorted(has & no)[0]
                # A conditional default can disappear by deactivating its
                # predicate, even when it has no exclusive-group peer (ZR1
                # EFR is supplied unless ZYC is selected).
                for row in e.scoped('acquisition', config):
                    if row['target_option_id'] != oid:
                        continue
                    for yes, nots in self.recipes(row['condition_id'], False):
                        if yes.issubset(want) and nots.issubset(no):
                            continue
                        result = search(want | yes, no | nots, intent, interior)
                        if result:
                            return result
                peers = set().union(*(e.members[g['id']] for g in e.scoped('choice_group', config) if oid in e.members[g['id']]))
                for peer in sorted(peers - no - want):
                    if self.selectable(config, peer):
                        result = search(want | {peer}, no, intent, interior)
                        if result:
                            return result
                reasons['forbidden endpoint acquired'] += 1
                return None
            try:
                return e.state(config, intent, interior)
            except EvaluationError as exc:
                reasons[str(exc)] += 1
                return None

        state = search(key[1], key[2])
        self.witnesses[key] = state
        self.witness_reasons[key] = dict(reasons)
        if state is None:
            self.errors.update(reasons)
        return state

    def conditioned(self, config, cid, wanted=(), truth=True):
        for yes, no in self.recipes(cid, truth):
            state = self.witness(config, set(wanted) | yes, no)
            if state is not None:
                actual, _ = self.ev.condition(cid, config, state.intent, state.interior_id, self.ev.roots(state.causes))
                assert actual == truth, 'Condition witness does not match requested truth'
                yield state

    def unavailable_witness(self, config, cid, wanted=(), truth=True):
        proofs = []
        reasons = Counter()
        for yes, no in self.recipes(cid, truth):
            yes = yes | frozenset(wanted)
            proofs.append(self.disjoint(config, yes, no))
            reasons.update(self.witness_reasons.get((config, yes, no), {}))
        return {'status': 'inapplicable' if all(proofs) else 'unresolved',
                'reason': '; '.join(sorted(set(p for p in proofs if p))) or 'No valid witness constructed',
                'search_reasons': dict(reasons)}

    def transaction(self, before, action, target):
        try:
            return self._transaction(before, action, target)
        except (AssertionError, EvaluationError) as exc:
            # Keep a contextual failure and finish the other rows; a broken
            # reverse-order preview must not prevent writing the inventory.
            result = ('failed', type(exc).__name__ + ': ' + str(exc), None)
            self.transactions[before, action, target] = result
            return result

    def _transaction(self, before, action, target):
        key = before, action, target
        if key in self.transactions:
            return self.transactions[key]
        session = Session(self.ev, before.configuration_id)
        session.state = before
        try:
            preview = session.preview(action, target)
        except EvaluationError as exc:
            assert session.state is before and session._pending is None
            result = ('refused', str(exc), None)
        else:
            assert session.state is before
            after = preview.candidate
            assert preview.added == after.resolved - before.resolved
            assert preview.removed == before.resolved - after.resolved
            assert preview.removed_intent == set(before.intent) - set(after.intent)
            assert preview.interior_changed == (before.interior_id != after.interior_id)
            owners = [(c.owner_kind, c.owner_id) for c in after.charges]
            assert len(owners) == len(set(owners)), 'Duplicate charge owner'
            assert all(c.owner_id in after.resolved for c in after.charges if c.owner_kind == 'option'), 'Charge for removed option'
            if action == 'interior' and target is not None:
                assert after.interior_id == target, 'Requested interior silently discarded'
            assert session.cancel() is before
            try:
                session.confirm(preview)
            except EvaluationError:
                pass
            else:
                raise AssertionError('Canceled preview accepted')
            # SQL/source row order must not select a business winner. Reuse
            # the required second preview to challenge every interaction in
            # reverse acquisition/conflict/requirement/price/plan order.
            tables = ('acquisition', 'conflict', 'conflict_member', 'requirement',
                      'choice_group', 'option_rate', 'replacement_plan', 'replacement_action', 'content_effect')
            original = {t: self.ev.rows[t] for t in tables}
            try:
                for table in tables:
                    self.ev.rows[table] = list(reversed(original[table]))
                again = session.preview(action, target)
                assert again == preview, 'Transaction depends on source row order'
            finally:
                self.ev.rows.update(original)
                self.ev._index()
            assert session.confirm(again) == after
            if after != before:
                assert session.revert() == before
            result = ('passed', None, after)
        self.transactions[key] = result
        return result

    def probe(self, before, action, target, *, absent=(), retained=()):
        if before is None:
            return {'status': 'no_witness'}
        status, reason, after = self.transaction(before, action, target)
        result = {'status': status, 'before_intent': list(before.intent), 'before_interior': before.interior_id,
                  'action': action, 'target': target}
        if reason:
            result['reason'] = reason
        if after:
            bad = [x for x in absent if present(after, x)] + [x for x in retained if not present(after, x)]
            if bad:
                result.update(status='failed', reason='Postcondition: ' + ','.join(bad))
            result.update(removed=sorted(before.resolved - after.resolved),
                          removed_intent=sorted(set(before.intent) - set(after.intent)),
                          added=sorted(after.resolved - before.resolved),
                          before_total_minor=before.total_minor, after_total_minor=after.total_minor)
        return result

    def ownership(self, config, row, before):
        e = self.ev
        target = row['target_option_id']
        causes = [c for c in before.causes if c.source_id == row['id']]
        support = set().union(*(c.roots for c in causes))
        results = []
        for root in sorted(support):
            if root.startswith('configuration:'):
                continue
            action, request = ('interior', None) if root.startswith('interior:') else ('remove', root)
            if action == 'remove' and not self.selectable(config, request):
                continue
            results.append(dict(kind='source_remove', source=root, **self.probe(before, action, request)))
        if not self.selectable(config, target) or target in before.intent or not support or any(x.startswith('configuration:') for x in support):
            return results
        try:
            independent = e.state(config, (target,))
        except EvaluationError:
            return results
        # Actual transition order matters: a pure state cannot test absorption.
        after = independent
        try:
            for oid in before.intent:
                after = e.transition(after, 'select', oid)
            if before.interior_id:
                after = e.transition(after, 'interior', before.interior_id)
        except EvaluationError as exc:
            results.append(dict(kind='independent_before_source', status='unresolved', reason=str(exc)))
            return results
        if not any(c.source_id == row['id'] for c in after.causes):
            results.append(dict(kind='independent_before_source', status='yielded', reason='Independent peer prevents this acquisition'))
            return results
        owned = target in after.intent
        expected = row['intent_policy'] == 'preserve_prior'
        results.append(dict(kind='independent_before_source', status='passed' if owned == expected else 'failed',
                            target=target, expected_intent_policy=row['intent_policy']))
        # Selecting a locked supplied child afterward must not create ownership.
        if row['peer_policy'] == 'locked':
            result = self.probe(before, 'select', target)
            _, _, candidate = self.transaction(before, 'select', target)
            if candidate is not None and candidate.intent != before.intent:
                result.update(status='failed', reason='Supplied child click invented independent ownership')
            results.append(dict(kind='source_before_child', **result))
        if owned:
            for root in sorted(support):
                if root.startswith('configuration:'):
                    continue
                action, request = ('interior', None) if root.startswith('interior:') else ('remove', root)
                if action == 'remove' and not self.selectable(config, request):
                    continue
                # Continuing prerequisites are still authoritative; the generic
                # transaction checks validate them. Literal lane cases assert
                # the independently supported child and exact retained charge.
                results.append(dict(kind='independent_source_remove', source=root, **self.probe(after, action, request)))
            results.append(dict(kind='independent_child_remove', **self.probe(after, 'remove', target, absent=[target])))
        return results

    def disjoint(self, config, yes, no):
        """Small sound proofs; a failed search alone is never a proof."""
        return self._disjoint(config, frozenset(yes), frozenset(no))

    @lru_cache(maxsize=100000)
    def _disjoint(self, config, yes, no):
        e = self.ev
        if len([x for x in yes if x.startswith('interior:')]) > 1:
            return 'distinct chosen interiors'
        yes = set(yes)
        for x in list(yes):
            if x.startswith('interior:') and x[9:] in e.interiors:
                yes.add(e.interiors[x[9:]]['seat_option_id'])
                yes.update(r['option_id'] for r in e.rows['interior_part'] if r['interior_id'] == x[9:] and r['option_id'])
        changed = True
        while changed:
            prior = set(yes)
            for target, recipes in self.implications[config]:
                if any(a.issubset(yes) and b.issubset(no) for a, b in recipes):
                    yes.add(target)
            for target, required in self.reverse_implications[config]:
                if target in yes:
                    yes.update(required)
            changed = yes != prior
        if yes & no:
            return 'required or unconditionally acquired endpoint also required absent'
        leaves = {x for x in yes if x.startswith('interior:')}
        if len(leaves) > 1:
            return 'distinct chosen interiors'
        if leaves:
            for target, allowed in self.interior_only_sources[config].items():
                if target in yes and not leaves.intersection(allowed):
                    return 'nonselectable option requires a different interior: ' + target
        for x in yes:
            if x.startswith('interior:'):
                if (x[9:], config) not in e.interior_scopes:
                    return 'interior outside configuration'
            elif not e.eligible(x, config):
                return 'inactive or inapplicable option ' + x
        for group in e.scoped('choice_group', config):
            if len(yes & e.members[group['id']]) > group['maximum']:
                return 'exclusive group ' + group['id']
        for conflict in e.scoped('conflict', config):
            if endpoint(conflict) not in yes or e.conditions[conflict['activation_condition_id']]['mode'] != 'always':
                continue
            if any(m['conflict_id'] == conflict['id'] and endpoint(m, '') in yes for m in e.rows['conflict_member']):
                return 'unconditional exclusion ' + conflict['id']
        return None

    def overlaps(self):
        e = self.ev
        results = []
        disjoint_counts = Counter()
        for table, target in (('acquisition', 'target_option_id'), ('option_rate', 'target_option_id'),
                              ('replacement_plan', 'requested_option_id'), ('content_effect', 'aspect_id')):
            for left, right in combinations(e.rows[table], 2):
                if left[target] != right[target]:
                    continue
                if table == 'content_effect' and 'add' in (left['effect_kind'], right['effect_kind']):
                    continue
                configs = sorted(self.scope_configs[table][left['id']] & self.scope_configs[table][right['id']])
                for config in configs:
                    proofs = set()
                    unresolved = False
                    witness = None
                    for (a, b), (c, d) in product(self.recipes(left['condition_id']), self.recipes(right['condition_id'])):
                        yes, no = a | c, b | d
                        proof = self.disjoint(config, yes, no)
                        if proof:
                            proofs.add(proof)
                            continue
                        witness = self.witness(config, yes, no)
                        if witness:
                            break
                        unresolved = True
                    item = dict(table=table, left=left['id'], right=right['id'], configuration=config)
                    if witness:
                        item.update(status='overlap', intent=list(witness.intent), interior=witness.interior_id)
                        if table == 'acquisition':
                            same = (left['peer_policy'], left['intent_policy']) == (right['peer_policy'], right['intent_policy'])
                            if not same and 'standard' not in (left['origin_kind'], right['origin_kind']):
                                item.update(status='failed', reason='Contradictory ownership')
                            item['precedence'] = [left['priority'], right['priority']]
                            actual_causes = {c.source_id for c in witness.causes if c.option_id == left[target]}
                            if left['peer_policy'] == right['peer_policy'] == 'locked' and not {left['id'], right['id']}.issubset(actual_causes):
                                item.update(status='failed', reason='Overlapping locked cause lost')
                            if self.selectable(config, left[target]) and {left['id'], right['id']}.issubset(actual_causes):
                                item['removal'] = self.probe(witness, 'remove', left[target], absent=[left[target]])
                        elif table == 'replacement_plan':
                            item.update(status='failed', reason='Competing replacements')
                        else:
                            rank = 'priority' if table == 'option_rate' else 'precedence'
                            item['precedence'] = [left[rank], right[rank]]
                            if left[rank] == right[rank]:
                                item.update(status='failed', reason='Ambiguous precedence')
                    else:
                        item.update(status='unresolved' if unresolved else 'disjoint', proofs=sorted(proofs))
                    if item['status'] == 'disjoint':
                        disjoint_counts[table] += 1
                    else:
                        results.append(item)
        return {'disjoint_pairs': dict(disjoint_counts), 'interactions': results}

    def inventory(self):
        e = self.ev
        entries = []
        for table in SCOPES:
            for row in e.rows[table]:
                evidence = [dict(r) for r in self.db.execute('''SELECT d.source_path,a.locator FROM evidence_member m
                    JOIN source_anchor a USING(anchor_id) JOIN source_document d USING(document_id)
                    WHERE m.set_id=? ORDER BY d.source_path,a.locator''', (row['evidence_set_id'],))]
                conditions = {key: {'row': e.conditions[value], 'clauses': [dict(c, members=e.condition_members[value,c['clause_id']]) for c in e.clauses[value]]}
                              for key, value in row.items() if key.endswith('condition_id')}
                entry = {'table': table, 'id': row['id'], 'rule': row, 'conditions': conditions, 'evidence': evidence,
                         'configurations': sorted(c for rid, c in e.scopes[table] if rid == row['id'])}
                if table == 'conflict':
                    entry['members'] = [endpoint(m, '') for m in e.rows['conflict_member'] if m['conflict_id'] == row['id']]
                elif table == 'choice_group':
                    entry['members'] = sorted(e.members[row['id']])
                elif table == 'replacement_plan':
                    entry['actions'] = [r for r in e.rows['replacement_action'] if r['plan_id'] == row['id']]
                entries.append(entry)
        for leaf, row in e.interiors.items():
            evidence = [dict(r) for r in self.db.execute("""SELECT d.source_path,a.locator FROM evidence_member m
                JOIN source_anchor a USING(anchor_id) JOIN source_document d USING(document_id)
                WHERE m.set_id=? ORDER BY d.source_path,a.locator""", (row['evidence_set_id'],))]
            entries.append({'table': 'interior_ownership', 'id': leaf, 'rule': row, 'conditions': {},
                            'evidence': evidence, 'parts': [r for r in e.rows['interior_part'] if r['interior_id'] == leaf],
                            'configurations': sorted(c for i,c in e.interior_scopes if i == leaf)})
        return entries

    def run(self, tables=None):
        entries = self.inventory()
        for entry in entries:
            table, row = entry['table'], entry['rule']
            if tables and table not in tables:
                continue
            checks = []
            for config in entry['configurations']:
                def add(kind, result, **extra):
                    checks.append(dict(configuration=config, kind=kind, **extra, **result))
                if table == 'interior_ownership':
                    leaf = row['id']
                    members = [row['seat_option_id']] + [p['option_id'] for p in entry['parts'] if p['option_id']]
                    before = self.ev.state(config)
                    add('choose_interior', self.probe(before, 'interior', leaf, retained=['interior:' + leaf, *members]))
                    after = self.transaction(before, 'interior', leaf)[2]
                    if after is not None:
                        add('clear_interior', self.probe(after, 'interior', None, absent=['interior:' + leaf]))
                        for child in sorted(set(members)):
                            if self.selectable(config, child):
                                add('interior_child_remove', self.probe(after, 'remove', child, absent=[child]))
                elif table == 'conflict':
                    source = endpoint(row)
                    for target in entry['members']:
                        for first, second in ((source, target), (target, source)):
                            before = next(self.conditioned(config, row['activation_condition_id'], [first]), None)
                            action, request = ('interior', second[9:]) if second.startswith('interior:') else ('select', second)
                            result = self.probe(before, action, request, absent=[first]) if before else self.unavailable_witness(config, row['activation_condition_id'], [first])
                            add('exclude', result, first=first, second=second)
                elif table == 'choice_group':
                    if len(entry['members']) < 2:
                        state = self.witness(config, entry['members'])
                        add('single_member_group', {'status': 'active' if state else 'unresolved',
                            'reason': 'No distinct peer pair; cardinality checked in state evaluation'})
                    for first, second in combinations(entry['members'], 2):
                        for a, b in ((first, second), (second, first)):
                            before = self.witness(config, [a])
                            result = self.probe(before, 'select', b, absent=[a])
                            if before is None:
                                result = dict(status='inapplicable' if self.disjoint(config, {a}, set()) else 'unresolved',
                                              reason=self.disjoint(config, {a}, set()) or 'No valid peer witness')
                            add('peer', result, first=a, second=b)
                elif table == 'requirement':
                    source = endpoint(row)
                    found = False
                    for yes, no in self.recipes(row['satisfaction_condition_id']):
                        for before in self.conditioned(config, row['activation_condition_id'], {source} | yes):
                            if any(present(before, x) for x in no):
                                continue
                            found = True
                            for target in sorted(yes):
                                if present(before, target) and not target.startswith('interior:'):
                                    add('dependency_remove', self.probe(before, 'remove', target, absent=[target]), source=source)
                            break
                    if not found:
                        add('dependency_remove', self.unavailable_witness(config, row['activation_condition_id'], [source]), source=source)
                elif table == 'acquisition':
                    target = row['target_option_id']
                    found = False
                    for before in self.conditioned(config, row['condition_id']):
                        found = True
                        active = any(c.source_id == row['id'] for c in before.causes)
                        add('acquire', {'status': 'active' if active else 'yielded', 'intent': list(before.intent), 'interior': before.interior_id})
                        if active and self.selectable(config, target):
                            add('child_remove', self.probe(before, 'remove', target, absent=[target]))
                        if active:
                            for result in self.ownership(config, row, before):
                                kind = result.pop('kind')
                                add(kind, result)
                    if not found:
                        add('acquire', self.unavailable_witness(config, row['condition_id']))
                elif table == 'replacement_plan':
                    found = False
                    for before in self.conditioned(config, row['condition_id']):
                        found = True
                        removed = [a['option_id'] for a in entry['actions'] if a['action'] == 'remove']
                        added = [a['option_id'] for a in entry['actions'] if a['action'] == 'add']
                        add('replacement', self.probe(before, 'select', row['requested_option_id'], absent=removed, retained=added))
                    if not found:
                        add('replacement', self.unavailable_witness(config, row['condition_id']))
                else:
                    before = next(self.conditioned(config, row['condition_id']), None)
                    add('condition', {'status': 'active'} if before else self.unavailable_witness(config, row['condition_id']))
                for key, cid in row.items():
                    if key.endswith('condition_id') and self.ev.clauses[cid]:
                        negative = next(self.conditioned(config, cid, truth=False), None)
                        if negative and table == 'acquisition':
                            assert all(c.source_id != row['id'] for c in negative.causes), 'Inactive acquisition retained cause'
                        add(key + '_false', {'status': 'inactive', 'intent': list(negative.intent), 'interior': negative.interior_id}
                            if negative else self.unavailable_witness(config, cid, truth=False))
            entry['checks'] = checks

        return entries


def run(tables=None, models=None):
    db = f.connect(':memory:')
    try:
        f.create_schema(db)
        import_behavior(db)
        report = {'format': 'semantic-overlap-v1', 'release_ready': False, 'requested_tables': tables, 'requested_models': models, 'lanes': {},
                  'implementation': {name: hashlib.sha256((f.ROOT / name).read_bytes()).hexdigest() for name in (
                      'catalog/evaluator.py', 'catalog/behavior_sources.py', 'catalog/evaluator_sources.py', 'catalog/semantic_validation.py')},
                  'policy': json.loads((f.ROOT / 'docs/compatibility-notice-policy.json').read_text())}
        for model, revision in db.execute('''SELECT model_key,revision_id FROM catalog_revision
            JOIN model_year USING(model_year_id) JOIN model USING(model_id) ORDER BY model_key'''):
            if models and model not in models:
                continue
            audit = Audit(db, revision)
            entries = audit.run(tables)
            counts = Counter(c['status'] for e in entries for c in e.get('checks', []))
            print(model, dict(counts), 'unique transactions', len(audit.transactions), flush=True)
            overlaps = audit.overlaps()
            print(model, 'overlap analysis complete', len(overlaps['interactions']), flush=True)
            report['lanes'][model] = {'revision_id': revision, 'inventory': entries, 'counts': dict(counts),
                'options': {oid: {'rpo': row['rpo'], 'name': row['name'], 'lifecycle': row['lifecycle'],
                                  'customer_selectable': row['customer_selectable'],
                                  'configurations': {c: status for (o,c), status in audit.ev.statuses.items() if o == oid}}
                            for oid,row in audit.ev.options.items()},
                'source_dispositions': [dict(row) for row in db.execute("""SELECT d.source_path,a.locator,s.disposition,s.reason
                    FROM source_disposition s JOIN source_anchor a USING(anchor_id) JOIN source_document d USING(document_id)
                    WHERE s.revision_id=? AND s.fragment_key='behavior' ORDER BY d.source_path,a.locator""", (revision,))],
                'witness_failures': dict(audit.errors), 'overlaps': overlaps}
            problems = findings({'lanes': {model: report['lanes'][model]}})
            for problem in problems[:10]:
                print('FINDING', json.dumps(problem), flush=True)
            audit._disjoint.cache_clear()
        return report
    finally:
        db.close()



def findings(report):
    allowed_refusals = {
        'Option is not customer selectable in this context', 'Context makes option nonselectable',
        'Ineligible interior', 'Requested option cannot satisfy its prerequisites',
        'Standard-only equipment cannot be purchased or removed', 'Cannot remove mandatory configuration equipment',
    }
    found = []
    def walk(value, location):
        if isinstance(value, dict):
            if value.get('status') in ('failed', 'unresolved', 'no_witness') or (value.get('status') == 'refused' and value.get('reason') not in allowed_refusals):
                found.append({'location': location, **value})
            for key, child in value.items():
                walk(child, location + '/' + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, location + '/' + str(index))
    walk(report['lanes'], 'lanes')
    return found


def compact(report):
    """Normalize repeated conditions and checks; keep every inventory entry."""
    omit = {'revision_id', 'model_year_id', 'evidence_set_id', 'decision_set_id'}
    def clean(value):
        if isinstance(value, dict):
            return {k: clean(v) for k,v in value.items() if k not in omit and v is not None}
        if isinstance(value, list):
            return [clean(x) for x in value]
        return value
    for lane in report['lanes'].values():
        conditions = {}
        checks = []
        check_ids = {}
        for entry in lane['inventory']:
            for condition in entry.pop('conditions').values():
                cid = condition['row']['id']
                conditions[cid] = {'mode': condition['row']['mode'], 'clauses': [
                    {'mode': c['mode'], 'members': [{k:v for k,v in m.items() if k in ('option_id','interior_id','group_id','state') and v is not None}
                                                  for m in c['members']]} for c in condition['clauses']]}
            entry['rule'] = clean(entry['rule'])
            if 'parts' in entry:
                entry['parts'] = clean(entry['parts'])
            ids = []
            for check in entry.get('checks', []):
                key = json.dumps(check, sort_keys=True)
                if key not in check_ids:
                    check_ids[key] = len(checks)
                    checks.append(check)
                ids.append(check_ids[key])
            entry['checks'] = ids
        lane['conditions'] = conditions
        lane['checks'] = checks
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--tables', nargs='+', choices=(*SCOPES, 'interior_ownership'))
    parser.add_argument('--models', nargs='+')
    args = parser.parse_args()
    report = run(args.tables, args.models)
    problems = findings(report)
    report['findings'] = problems
    report['complete'] = not problems and not args.tables and not args.models
    args.output.write_text(json.dumps(compact(report), separators=(',', ':')) + '\n')
    print('Findings:', len(problems), flush=True)
    if problems:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
