"""Disposable evaluator for E01–E08 behavior and complete interior price owners.

No authoring writes, full-catalog validity, rendering, or submission API. All
amounts are integer minor units. A Session previews and commits whole states.
"""
from collections import defaultdict
from dataclasses import dataclass

from catalog.foundation_schema import SCOPES


class EvaluationError(ValueError):
    """An unsupported request or contradictory candidate; nothing was committed."""


@dataclass(frozen=True)
class Cause:
    option_id: str
    origin: str
    source_id: str
    roots: frozenset[str]
    peer_policy: str = 'locked'


@dataclass(frozen=True)
class Charge:
    owner_kind: str
    owner_id: str
    amount_minor: int
    basis_id: str
    rate_id: str | None = None


@dataclass(frozen=True)
class State:
    revision_id: str
    configuration_id: str
    intent: tuple[str, ...]
    interior_id: str | None
    causes: tuple[Cause, ...]
    resolved: frozenset[str]
    installed: frozenset[str]
    standard: frozenset[str]
    charges: tuple[Charge, ...]
    issues: tuple[str, ...]

    @property
    def total_minor(self):
        return sum(line.amount_minor for line in self.charges)


@dataclass(frozen=True)
class Preview:
    before: State
    candidate: State
    added: frozenset[str]
    removed: frozenset[str]
    removed_intent: frozenset[str]
    interior_changed: bool


class Evaluator:
    """Read one revision into a private snapshot; requests use retained IDs."""

    def __init__(self, db, revision_id):
        self.revision_id = revision_id
        tables = ('configuration', 'option', 'interior', 'interior_part', 'component_rate',
                  'option_presentation_override', 'condition',
                  'condition_clause', 'condition_member', 'option_configuration',
                  'interior_configuration', 'choice_group_member', 'conflict_member',
                  'replacement_action', 'configuration_policy', 'interaction_policy',
                  *[t for t in SCOPES if t != 'content_effect'])
        self.rows = {t: [dict(r) for r in db.execute(
            f'SELECT * FROM "{t}" WHERE revision_id = ?', (revision_id,))] for t in tables}
        self.scopes = {t: {(r[0], r[1]) for r in db.execute(
            f'SELECT {key}, configuration_id FROM {t}_configuration WHERE revision_id = ?',
            (revision_id,))} for t, key in SCOPES.items() if t != 'content_effect'}
        self.options = {r['id']: r for r in self.rows['option']}
        self.configs = {r['id']: r for r in self.rows['configuration']}
        self.interiors = {r['id']: r for r in self.rows['interior']}
        self.conditions = {r['id']: r for r in self.rows['condition']}
        self.bases = {r['basis_id']: dict(r) for r in db.execute('SELECT * FROM price_basis')}
        self.statuses = {(r['option_id'], r['configuration_id']): r['status']
                         for r in self.rows['option_configuration']}
        self.interior_scopes = {(r['interior_id'], r['configuration_id']) for r in self.rows['interior_configuration']}
        self.members = defaultdict(set)
        for r in self.rows['choice_group_member']:
            self.members[r['group_id']].add(r['option_id'])
        if len(self.rows['interaction_policy']) != 1 or not self.configs:
            raise EvaluationError('Missing revision interaction policy or configurations')
        policy = self.rows['interaction_policy'][0]
        expected = dict(conflict_action='notice_confirm_cancel',
                        direct_removal_action='remove_requested_and_supporting_sources',
                        cancel_action='preserve_whole_state', revert_action='restore_whole_state')
        if any(policy[k] != v for k, v in expected.items()):
            raise EvaluationError('Unsupported interaction policy')

    def scoped(self, table, config):
        return [r for r in self.rows[table] if (r['id'], config) in self.scopes[table]]

    def eligible(self, option, config):
        row = self.options.get(option)
        return bool(row and row['lifecycle'] == 'active' and
                    self.statuses.get((option, config)) in ('available', 'standard'))

    def condition(self, identifier, config, intent, interior, roots):
        """Return truth and supporting live roots; absence contributes no roots."""
        condition = self.conditions[identifier]
        clauses = [r for r in self.rows['condition_clause'] if r['condition_id'] == identifier]
        if condition['mode'] == 'always':
            if clauses:
                raise EvaluationError('Always condition has clauses')
            return True, frozenset()
        if not clauses:
            raise EvaluationError('Empty conjunction')
        support = set()
        for clause in clauses:
            members = [r for r in self.rows['condition_member']
                       if r['condition_id'] == identifier and r['clause_id'] == clause['clause_id']]
            if not members:
                raise EvaluationError('Empty condition clause')
            hits = []
            for m in members:
                if m['option_id'] is not None:
                    oid = m['option_id']
                    hits.append(({oid} if oid in intent else set()) if m['state'] == 'explicit_intent'
                                else roots.get(oid, set()))
                elif m['interior_id'] is not None:
                    hits.append({'interior:' + interior} if interior == m['interior_id'] else set())
                else:
                    gid = m['group_id']
                    if (gid, config) not in self.scopes['choice_group']:
                        raise EvaluationError('Condition references out-of-scope group')
                    hits.append(set().union(*(roots.get(o, set()) for o in self.members[gid])))
            present = any(hits)
            if clause['mode'] == 'any_present':
                if not present:
                    return False, frozenset()
                support.update(set().union(*hits))
            elif clause['mode'] == 'none_present':
                if present:
                    return False, frozenset()
            else:
                raise EvaluationError('Unsupported condition clause')
        return True, frozenset(support)

    @staticmethod
    def roots(causes):
        roots = defaultdict(set)
        for cause in causes:
            roots[cause.option_id].update(cause.roots)
        return roots

    def closure(self, config, intent, interior, blocked=frozenset()):
        base = [Cause(o, 'independent', o, frozenset({o})) for o in intent if o not in blocked]
        if interior:
            seat = self.interiors[interior]['seat_option_id']
            if seat not in blocked:
                base.append(Cause(seat, 'interior', interior, frozenset({'interior:' + interior})))
            for part in self.rows['interior_part']:
                if part['interior_id'] == interior and part['option_id'] and part['option_id'] not in blocked:
                    base.append(Cause(part['option_id'], 'interior', interior, frozenset({'interior:' + interior})))
        if any(not self.eligible(c.option_id, config) for c in base):
            raise EvaluationError('Interior or intent targets ineligible option')
        causes, seen = tuple(base), set()
        for _ in range(256):
            signature = frozenset(causes)
            if signature in seen:
                raise EvaluationError('Repeated acquisition state / nonconvergence')
            seen.add(signature)
            roots = self.roots(causes)
            active = []
            for row in self.scoped('acquisition', config):
                truth, support = self.condition(row['condition_id'], config, intent, interior, roots)
                if truth:
                    if not self.eligible(row['target_option_id'], config):
                        raise EvaluationError('Acquisition targets ineligible option')
                    if not support:
                        support = frozenset({'configuration:' + row['id']})
                    active.append((row, support))
            # Multiple causes are retained. Conflicting policies cannot be resolved
            # by whichever row happens to come first in a SQL result.
            policies = defaultdict(set)
            for row, _ in active:
                policies[row['target_option_id']].add((row['peer_policy'], row['intent_policy']))
            if any(len(p) > 1 for p in policies.values()):
                raise EvaluationError('Contradictory acquisition ownership policies')
            suppressed = set()
            for group in self.scoped('choice_group', config):
                members = self.members[group['id']]
                explicit = members.intersection(intent)
                if len(explicit) > group['maximum']:
                    raise EvaluationError('Conflicting explicit group intent')
                offers = [(row, support) for row, support in active if row['target_option_id'] in members]
                locked = {r['target_option_id'] for r, _ in offers if r['peer_policy'] == 'locked'}
                winners = explicit | locked
                if len(winners) > group['maximum']:
                    raise EvaluationError('Locked group conflict')
                if not winners and offers:
                    priority = min(r['priority'] for r, _ in offers)
                    winners = {r['target_option_id'] for r, _ in offers if r['priority'] == priority}
                    if len(winners) > group['maximum']:
                        raise EvaluationError('Ambiguous competing defaults')
                suppressed.update(members - winners)
            next_causes = list(base)
            for row, support in active:
                target = row['target_option_id']
                if target not in blocked and target not in suppressed:
                    next_causes.append(Cause(target, row['origin_kind'], row['id'], support, row['peer_policy']))
            next_causes = tuple(sorted(set(next_causes), key=lambda c: (c.option_id, c.origin, c.source_id, sorted(c.roots))))
            if frozenset(next_causes) == signature:
                return next_causes, active
            causes = next_causes
        raise EvaluationError('Acquisition iteration limit exceeded')

    def _money(self, amount, basis, meaning):
        b = self.bases.get(basis)
        if type(amount) is not int or amount < 0 or not b or b['currency'] != 'USD' or b['minor_units_per_unit'] != 100 or b['amount_meaning'] != meaning:
            raise EvaluationError('Missing or incompatible exact price/basis')
        return amount

    def state(self, config, intent=(), interior=None):
        configuration = self.configs.get(config)
        if not configuration or not configuration['enabled']:
            raise EvaluationError('Unknown or disabled configuration in this revision')
        if len(set(intent)) != len(intent):
            raise EvaluationError('Duplicate independent intent')
        if any(not self.eligible(o, config) or not self.options[o]['customer_selectable'] for o in intent):
            raise EvaluationError('Ineligible or cross-revision intent')
        if any(r['configuration_id'] == config and r['option_id'] in intent and not r['customer_selectable']
               for r in self.rows['option_presentation_override']):
            raise EvaluationError('Context makes option nonselectable')
        if interior and (interior not in self.interiors or not self.interiors[interior]['enabled'] or (interior, config) not in self.interior_scopes):
            raise EvaluationError('Ineligible interior')
        causes, _ = self.closure(config, intent, interior)
        if any(c.option_id in intent and c.origin == 'standard' and c.peer_policy == 'locked' for c in causes):
            raise EvaluationError('Standard-only equipment cannot carry purchase intent')
        roots = self.roots(causes)
        test = lambda cid: self.condition(cid, config, intent, interior, roots)[0]
        for r in self.scoped('requirement', config):
            present = r['source_option_id'] in roots if r['source_option_id'] else r['source_interior_id'] == interior
            if present and test(r['activation_condition_id']) and not test(r['satisfaction_condition_id']):
                raise EvaluationError('Unsatisfied continuing requirement: ' + r['id'])
        if self.conflicts(config, intent, interior, causes):
            raise EvaluationError('Unresolved incompatibility')
        issues = ['partial_catalog_not_submission_ready']
        policies = [r for r in self.rows['configuration_policy'] if r['configuration_id'] == config]
        if len(policies) != 1:
            raise EvaluationError('Missing configuration policy')
        if not interior and policies[0]['interior_minimum']:
            issues.append('missing_required_interior')
        for group in self.scoped('choice_group', config):
            count = len(self.members[group['id']].intersection(roots))
            if count > group['maximum']:
                raise EvaluationError('Group cardinality exceeded')
            if count < group['minimum']:
                issues.append('missing_group:' + group['id'])
        installed = set(roots)
        for r in self.scoped('equipment_substitution', config):
            if test(r['condition_id']):
                installed.discard(r['removed_option_id'])
                replacement = r['replacement_option_id']
                if replacement and replacement not in roots:
                    raise EvaluationError('Substitution has no rooted replacement')
        charges = [Charge('configuration', config, self._money(configuration['starting_amount_minor'], configuration['basis_id'], 'vehicle_destination_included'), configuration['basis_id'])]
        for oid in sorted(roots):
            if not any(c.option_id == oid and c.origin != 'standard' for c in causes):
                continue
            option = self.options[oid]
            if option['charge_mode'] == 'no_separate_charge':
                continue
            if option['charge_mode'] != 'priced':
                raise EvaluationError('Unclassified purchase price')
            rates = [r for r in self.scoped('option_rate', config) if r['target_option_id'] == oid and test(r['condition_id'])]
            if len({r['priority'] for r in rates}) != len(rates):
                raise EvaluationError('Ambiguous applicable rates')
            rate = min(rates, key=lambda r: r['priority']) if rates else None
            amount, basis = (rate['amount_minor'], rate['basis_id']) if rate else (option['purchase_amount_minor'], option['basis_id'])
            charges.append(Charge('option', oid, self._money(amount, basis, 'option_purchase'), basis, rate['id'] if rate else None))
        for part in self.rows['interior_part']:
            if part['interior_id'] != interior or not part['component_id']:
                continue
            rates = [r for r in self.rows['component_rate']
                     if r['component_id'] == part['component_id'] and r['configuration_id'] == config]
            if len(rates) != 1:
                raise EvaluationError('Missing or ambiguous interior component rate')
            rate = rates[0]
            charges.append(Charge('component', part['component_id'],
                self._money(rate['amount_minor'], rate['basis_id'], 'option_purchase'), rate['basis_id']))
        standard = frozenset(o for (o, c), status in self.statuses.items() if c == config and status == 'standard')
        return State(self.revision_id, config, tuple(intent), interior, causes, frozenset(roots), frozenset(installed), standard, tuple(charges), tuple(issues))

    def conflicts(self, config, intent, interior, causes):
        roots = self.roots(causes)
        found = []
        for r in self.scoped('conflict', config):
            source = r['source_option_id'] or ('interior:' + r['source_interior_id'])
            present = source in roots or source == 'interior:' + (interior or '')
            if not present or not self.condition(r['activation_condition_id'], config, intent, interior, roots)[0]:
                continue
            for member in self.rows['conflict_member']:
                if member['conflict_id'] == r['id']:
                    target = member['option_id'] or ('interior:' + member['interior_id'])
                    if target in roots or target == 'interior:' + (interior or ''):
                        found.append((source, target))
        return found

    def transition(self, before, action, target=None):
        if before.revision_id != self.revision_id:
            raise EvaluationError('State belongs to another revision')
        config, intent, interior = before.configuration_id, list(before.intent), before.interior_id
        if action == 'configure':
            if target == config:
                return before
            policy, = [r for r in self.rows['configuration_policy'] if r['configuration_id'] == config]
            if policy['context_reset_policy'] != 'clear_intent':
                raise EvaluationError('Unsupported context reset policy')
            return self.state(target)
        if action == 'interior':
            interior = target
            # Check scope before any closure dereferences the leaf.
            if interior and (interior, config) not in self.interior_scopes:
                raise EvaluationError('Ineligible interior')
        elif action in ('select', 'remove'):
            if not self.eligible(target, config) or not self.options[target]['customer_selectable']:
                raise EvaluationError('Option is not customer selectable in this context')
            target_causes = [c for c in before.causes if c.option_id == target]
            if any(c.origin == 'standard' and c.peer_policy == 'locked' for c in target_causes):
                raise EvaluationError('Standard-only equipment cannot be purchased or removed')
            if action == 'select':
                if target in before.resolved and any(c.peer_policy == 'locked' and c.origin != 'independent' for c in target_causes):
                    return before  # A click on a supplied child never invents intent.
                plans = [r for r in self.scoped('replacement_plan', config)
                         if r['requested_option_id'] == target and self.condition(r['condition_id'], config, intent, interior, self.roots(before.causes))[0]]
                if len(plans) > 1:
                    raise EvaluationError('Ambiguous applicable replacements')
                if plans:
                    for row in sorted((r for r in self.rows['replacement_action'] if r['plan_id'] == plans[0]['id']), key=lambda r: r['position']):
                        if row['action'] == 'remove':
                            intent, interior = self.remove_roots(row['option_id'], intent, interior, before.causes)
                        elif row['intent_effect'] == 'commit_purchase':
                            if not self.eligible(row['option_id'], config):
                                raise EvaluationError('Replacement purchase is ineligible')
                            if row['option_id'] not in intent:
                                intent.append(row['option_id'])
                elif target not in intent:
                    # Explicit group peers replace displaced intent permanently.
                    peers = set().union(*(self.members[g['id']] for g in self.scoped('choice_group', config) if target in self.members[g['id']]))
                    intent = [o for o in intent if o not in peers]
                    intent.append(target)
            else:
                intent = [o for o in intent if o != target]
        else:
            raise EvaluationError('Unknown action')
        blocked = {target} if action == 'remove' else set()
        seen = set()
        for _ in range(256):
            signature = (tuple(intent), interior)
            if signature in seen:
                raise EvaluationError('Repeated transition cleanup state')
            seen.add(signature)
            causes, active = self.closure(config, intent, interior, blocked)
            roots = self.roots(causes)
            changed = False
            for r in self.scoped('requirement', config):
                source = r['source_option_id'] or ('interior:' + r['source_interior_id'])
                present = source in roots or source == 'interior:' + (interior or '')
                if present and self.condition(r['activation_condition_id'], config, intent, interior, roots)[0] and not self.condition(r['satisfaction_condition_id'], config, intent, interior, roots)[0]:
                    intent, interior = self.remove_roots(source, intent, interior, causes)
                    changed = True
                    break
            if changed:
                continue
            for row, support in active:
                if row['target_option_id'] in blocked:
                    intent, interior = self.drop_support(support, intent, interior)
                    changed = True
                    break
            if changed:
                continue
            conflicts = self.conflicts(config, intent, interior, causes)
            if conflicts:
                left, right = conflicts[0]
                # A removal requests nothing, so neither conflict side is preferred.
                requested_roots = ({target} if action == 'select' else
                                   {'interior:' + (target or '')} if action == 'interior' else set())
                left_roots = roots.get(left, {left})
                right_roots = roots.get(right, {right})
                if requested_roots.intersection(left_roots) and not requested_roots.intersection(right_roots):
                    loser = right
                elif requested_roots.intersection(right_roots) and not requested_roots.intersection(left_roots):
                    loser = left
                else:
                    raise EvaluationError('No unambiguous permitted conflict removal')
                intent, interior = self.remove_roots(loser, intent, interior, causes)
                continue
            # Absorption is a transition effect, never part of pure evaluation.
            old_acquisitions = {c.source_id for c in before.causes}
            absorbed = {r['target_option_id'] for r, _ in active
                        if r['intent_policy'] == 'absorb_prior' and r['id'] not in old_acquisitions}
            if absorbed.intersection(intent):
                intent = [o for o in intent if o not in absorbed]
                continue
            return self.state(config, intent, interior)
        raise EvaluationError('Transition iteration limit exceeded')

    def remove_roots(self, option, intent, interior, causes):
        support = {option} if option.startswith('interior:') else self.roots(causes).get(option, {option})
        return self.drop_support(support, intent, interior)

    @staticmethod
    def drop_support(support, intent, interior):
        if any(root.startswith('configuration:') for root in support):
            raise EvaluationError('Cannot remove mandatory configuration equipment')
        return [o for o in intent if o not in support], (None if 'interior:' + (interior or '') in support else interior)


class Session:
    """One pending preview and one undo state. Cancel/failed previews are inert."""

    def __init__(self, evaluator, configuration_id):
        self.evaluator = evaluator
        self.state = evaluator.state(configuration_id)
        self._pending = None
        self._previous = None

    def preview(self, action, target=None):
        self._pending = None
        candidate = self.evaluator.transition(self.state, action, target)
        self._pending = Preview(self.state, candidate, candidate.resolved - self.state.resolved,
                                self.state.resolved - candidate.resolved,
                                frozenset(self.state.intent) - frozenset(candidate.intent),
                                self.state.interior_id != candidate.interior_id)
        return self._pending

    def confirm(self, preview):
        if preview is not self._pending or preview.before is not self.state:
            raise EvaluationError('Stale or foreign preview')
        if preview.candidate != self.state:
            self._previous, self.state = self.state, preview.candidate
        self._pending = None
        return self.state

    def cancel(self):
        self._pending = None
        return self.state

    def revert(self):
        if self._previous is None:
            raise EvaluationError('No committed transition to revert')
        self.state, self._previous = self._previous, None
        self._pending = None
        return self.state
