# Master catalog schema proposal

September 13, 2026. Design baseline: `f07e9de0bbf4e31a0f38714fee5fdc6304f5f04c`
(the merged [six-model review](six-model-review.md)). **Logical proposal for review;
no DDL, populated target catalog, evaluator, application or cutover is implemented.**

Use one relational vocabulary with model-owned facts. Share source documents and
immutable media where appropriate; do not share product identities, relationship
sets or rates just because their codes match. This proposal supersedes the design
recommendations in the historical [Stingray plan](stingray-schema-plan.md) and
[earlier cross-model proposal](proposed-database-design.md). Their source observations
remain evidence. The [disposable schema](../catalog/schema.py) remains unchanged.

The design addresses review findings R1–R6: policy precedence, acquisition history,
conditional acquisition, single charge ownership, separate equipment projections,
and complete source translation. R7 was a repaired documentation link, with no
schema requirement. The six walkthroughs below test representability against the
reviewed evidence; they are not executions of the proposed system.

## 1. Authority, identity and value rules

Target translation composes frozen source facts and observed baseline behavior,
then the complete model owner overlay, then the final
[compatibility notice policy](compatibility-notice-policy.json). All 72 decisions
remain accepted; this proposal creates no new product-policy decisions. It does
not make earlier refusal UI, `retain_invalid` dependency behavior, unresolved
currency, or Z06's old block-or-switch alternative authoritative again.

**Revision convention.** `M` is a model-year identity; `R` is one complete snapshot
of M. Every domain row below has R in its primary key and every domain FK includes
R. Table entries abbreviate `(R, id)` as `id` only in prose. An association key
contains R and the referenced IDs; it has no additional ID unless another fact
must refer to that association. Listed non-key fields depend on the entire key.
Global tables are expressly identified. No rule may refer across model, year or
revision boundaries, including a condition or a member of a group.

Continuing configuration, option, interior, component, rule and presentation
identities have typed identity records keyed `(M, id)`. Their revision rows include
M and reference both `(R, M)` and `(M, id)`; R determines M. IDs persist across
revisions of the same M. A new year has new identities and optional reviewed,
typed predecessor links; it never inherits facts by fallback. A changed RPO does
not prove continuity. RPO is nullable and nonunique; names, source rows and hashes
are not product keys. DTC and DUW are different options. GS's two T0E source IDs
remain distinguishable even though one is retired in the target.

- Amounts are exact decimals with currency and price-basis references. Accepted
  target currency is USD; source evidence keeps its original unresolved fields.
  Zero means known zero; null means unresolved, never an automatic free choice.
- A nullable presentation or contextual lifecycle override means inherit; false
  explicitly overrides true.
  No other null acts as a wildcard. Empty applicability means nowhere.
- Body/trim applicability is an explicit configuration set. Scoped facts use
  the concrete per-family junctions defined below, not a polymorphic
  `family_configuration` table or an untyped `family_id`.
  “All” expands to the actual six or four configurations. Paint, interior and
  selected options are conditions, not new body/trim configurations.
- Source scope tokens, row order, dormant records and rich text remain evidence.
  Authoring does not interpret raw `*`, blank, pipe-delimited codes or RPO strings.
- Display ordering, rule priority, hierarchy order and source sequence have
  different owners. Deterministic ordering must not silently settle a business
  contradiction. Unknown or ambiguous executable facts block affected release
  paths, not preservation of their evidence.

### Typed configuration-scope junctions

Each row below defines a separate relation. Its primary key is
`(R, parent_id, configuration_id)`, using the concrete parent column shown;
`(R, parent_id)` references that row's named parent relation `(R, id)`
(`(R, binding_id)` for `visual_binding`), and `(R, configuration_id)` references
`configuration(R, id)`. All key columns are
non-null. Thus a scope cannot refer to a missing parent, another family, or a
configuration in another revision/model-year, even when families reuse an ID.

| Scope relation | Parent column | Parent relation |
|---|---|---|
| `requirement_configuration` | `requirement_id` | `requirement` |
| `acquisition_configuration` | `acquisition_id` | `acquisition` |
| `conflict_configuration` | `conflict_id` | `conflict` |
| `choice_group_configuration` | `group_id` | `choice_group` |
| `replacement_plan_configuration` | `plan_id` | `replacement_plan` |
| `option_rate_configuration` | `rate_id` | `option_rate` |
| `equipment_substitution_configuration` | `substitution_id` | `equipment_substitution` |
| `content_effect_configuration` | `effect_id` | `content_effect` |
| `visual_binding_configuration` | `binding_id` | `visual_binding` |

“Plus configurations”, “configuration scope”, “has scope” and the visual binding's
“explicit configurations” below refer to these junctions. Each row owns only
membership and its evidence/decision lineage (§7), not a copy of parent fields.
No membership rows means the parent applies nowhere; all-scope requires one row
per actual configuration. Conflict members and replacement actions inherit their
parent's scope rather than owning independent scope sets. For example, an
`acquisition_configuration` row cannot be justified by an `option_rate` with the
same ID: its parent FK must resolve to `acquisition` in R.

The already explicit `option_configuration`, `option_presentation_override`,
`interior_configuration` and `component_rate` keys include their configuration
and typed owner directly; they do not gain a second scope junction. Their owner
and configuration FKs also include R. The option status matrix remains complete,
including unavailable pairs; it is not reduced to positive scope memberships.

## 2. Foundation and ownership tables

| Relation | Grain / key | Owned fields and constraints |
|---|---|---|
| `model` (global) | `model_id`; unique model key | Lane identity and name. |
| `model_year` (global) | M; unique `(model_id, year)` and `(M, model_id, year)` | Model FK and year. No generated trim Cartesian product. |
| `price_basis` (global, immutable) | Basis ID | Currency, unit/amount meaning, source evidence and resolution state. Sharing a USD basis never shares the amounts or qualifiers of a model-owned rate. |
| `catalog_revision` (global) | R; unique `(M, revision_number)` and `(R, M)` | Parent revision in M, draft/frozen state, edit version. A frozen snapshot cannot be edited. |
| Typed identity families | `(M, id)` for each domain kind | Stable identity; optional typed predecessor and continuity rationale. A version cannot change kind or model-year. |
| `configuration` | `(R, id)`; unique `(R, body, trim)` | Enabled state, chooser order, vehicle starting amount, price basis, destination treatment. Current foundation is 32 configurations: 6/6/6/6/4/4. |
| `option` | `(R, id)` | RPO and identity kind (manufacturer code, reference code or uncoded), name/description, lifecycle (`active`, `factory_unavailable`, `retired`), disclosure, customer-selectable flag, charge mode (`priced`, `no_separate_charge`), default purchase amount/basis, presentation owned by `option_presentation`. Uncoded equipment and auto-only order codes retain identities. |
| `option_configuration` | `(R, option_id, configuration_id)` | Complete matrix: `standard`, `available`, `unavailable`; contextual lifecycle/disclosure override where source-qualified. Overrides cannot reactivate a retired identity. Status describes product applicability, not price, acquisition or visual state. |
| `option_presentation_override` | `(R, option_id, configuration_id)` | Nullable selectable/display-role/section/order overrides. Presentation cannot bypass lifecycle, scope or validity constraints; no price here. |
| `configuration_policy` | `(R, configuration_id)` | Required interior min/max, auto-select-sole-interior, invalid-interior action, context-reset policy, requirement label/detail and step FK. Current form requires exactly one interior. |
| `model_presentation`, `model_fact` | R; `(R, fact_id)` | Setup copy; independently ordered facts. Not product eligibility. |

A standard status supplies static trim information. Explicit standard/default
acquisition records (§4) decide what participates in configured equipment. Those
records must be translated with corrected latent rules before enabling previously
inactive equipment. A standard display-only UQT is not a paid purchase. Its
priced option identity can still carry the 1LT purchase amount in LT lanes.

The [complete relationship diagram and per-relation key/FK reference](master-schema-diagram.md)
cover all relations named in §§1–7, including typed identity/translation templates
and all nine scope junctions. Unspecified column sets and family expansions are
listed as open rather than invented; this remains a logical, not physical, design.

## 3. Interiors and charge components

| Relation | Grain / key | Owned fields and constraints |
|---|---|---|
| `interior` | `(R, id)` | Exact selectable leaf, interior code, typed seat-option FK, color/material attributes, enabled state. No editable stored total. |
| `interior_configuration` | `(R, interior_id, configuration_id)` | Explicit eligibility; the seat must be permitted. The 704 source leaves remain model-owned, not globally deduplicated. |
| `interior_part` | `(R, interior_id, part_key)` | Exactly one option FK or component FK, role, order, label override. Unique target per leaf; seat cannot be repeated as a part. Membership acquires the part once. |
| `component` | `(R, id)`; unique `(R, kind, code)` | A non-option extra with model-qualified meaning. A price reference alone does not establish a new physical part. |
| `component_rate` | `(R, component_id, configuration_id)` | One exact amount and basis for an applicable extra. Source trim/universal fallback is resolved into explicit configurations during translation; no runtime cross-model fallback. |
| `interior_node`, `interior_node_member` | `(R, node_id)`; `(R, node_id, interior_id)` | Acyclic navigation hierarchy with sibling/member order. Labels organize exact leaves, not a free combination generator. |

Seat and R6X are option charge owners. N26, stitching and TU7, where classified
as non-option extras, use component rates. LT versus LZ price-reference meanings
remain qualified by model and configuration. Every source membership is classified
as seat, option-backed part, non-option extra, identity attribute, or retained
nonexecuting evidence. A combined PriceRef amount and frozen stored interior sum
are reconciliation evidence, never additional editable charges or balancing deltas.
An equivalent source inclusion for a part is linked as corroborating evidence,
not executed a second time.

For example, Stingray `3LT_R6X_AE4_HXO_N26_38S` has AE4 595 + R6X 995 + N26 695
+ 38S 495 = **2,780**; its frozen 2,185 remains defect evidence. LZ examples have
model-qualified extras and reach 2,980 rather than inheriting that LT subtotal.
The selected seat can contribute a charge before an interior is chosen, but the
build remains incomplete. Interior selection supplies the same seat owner, not a
second line. Clearing the interior removes its part causes; valid independently
owned options follow their scoped retention policies.

## 4. Conditions, acquisition, requirements and replacement

A small typed condition structure is needed for AND/ANY tests. It replaces the
Stingray-only guard and combination tables without introducing stored scripts.
Conditions belong to R; identical conditions across models are not shared facts.

| Relation | Grain / key | Meaning and constraints |
|---|---|---|
| `condition` | `(R, id)` | Explicit `always` or conjunction mode. Non-always conditions require at least one clause; always has none. |
| `condition_clause` | `(R, condition_id, clause_id)` | Clauses are ANDed. Each clause is `any_present` or `none_present` over a nonempty member set. No recursive conditions. |
| `condition_member` | `(R, condition_id, clause_id, member_id)` | Exactly one typed option, interior or choice-group FK. State test is explicit intent or resolved selection for options, chosen for interior, occupied for group. `none_present` is evaluated over that same named state. Duplicate endpoint/state members prohibited. |
| `requirement` | `(R, id)` plus configurations | Source option OR interior FK, source state test, activation-condition FK, satisfaction-condition FK, loss policy and notice/revert copy. Satisfaction is checked after eligible acquisition; it does not itself add a choice. |
| `acquisition` | `(R, id)` plus configurations | Condition FK, target option FK, origin kind (`standard`, `default`, `included`, `dependency`), peer policy (`locked`, `yield_to_explicit`), intent policy (`absorb_prior`, `preserve_prior`), priority, disclosure. No amount. Standard/default roots and dependent additions have distinct origins. |
| `conflict`, `conflict_member` | `(R, id)` plus configurations; `(R, conflict_id, member_id)` | Typed source option OR interior FK, activation condition and nonempty incompatible member set. Each member has exactly one option OR interior FK in R, with duplicate typed endpoints prohibited. Option endpoints test resolved selection; interior endpoints test the chosen leaf. Both acquisition directions are constrained; historical directional effects are evidence. Option replacements use explicit plans; interior loss follows the cleanup/revert contract below. |
| `choice_group`, `choice_group_member` | `(R, id)` plus configurations; `(R, group_id, option_id)` | Min/max and peer policy over explicit option members only. No section FK or runtime section-derived membership. Configuration-qualified groups have explicit scope; different contextual member sets use separately scoped groups. |
| `replacement_plan`, `replacement_action` | `(R, id)` plus configurations; `(R, plan_id, position)` | Trigger request endpoint and condition FK; ordered add/remove option actions, acquisition origin for additions, disclosure. Interior changes are outside this action type and follow the dependency-loss/revert path below. Actions identify a permitted compatible solution; no arbitrary scripts or invented alternatives. |

A condition never tests a group outside that group's configuration scope. For
every condition referenced by a scoped parent (requirement, acquisition, conflict,
replacement plan, option rate, equipment substitution, content effect or visual
binding), the parent's configuration scope must be a subset of the scope of every
choice group named by any of its members; a revision violating this cannot be
frozen. `any_present` and `none_present` therefore keep their plain occupied/vacant
meaning over group endpoints, with no clause-wide prerequisite or out-of-scope
special case. When source group membership varies by configuration, translation
emits separately scoped groups and separately scoped conditions/parents. See the
[group scope constraint](master-schema-diagram.md#group-scope-constraint-for-conditions).

Section-based source groups are expanded during translation into explicit
`choice_group_member` rows. Each expanded member and group scope retains evidence
for the source group, effective section assignment/override and translation
rationale. Later presentation moves do not change group membership or cardinality;
a product-membership change requires an explicit, evidenced group edit. When
source section membership varies by configuration, translation emits separately
scoped groups with their corresponding explicit members.

Conflict members support option–option, option–interior and interior–option
endpoints directly; the source is not flipped to encode an otherwise unsupported
member. The same incompatibility is checked in either selection order. Typing a
conflict does not authorize choosing a replacement interior.

Replacement plans edit options only. If a proposed option transition invalidates
the chosen interior, the evaluator clears that leaf and its unsupported part
causes through dependency-loss cleanup. Compatibility-driven removals are disclosed
before confirmation under the common policy; cancel preserves the prior state.
After a committed transition, cleanup recalculates charges and alerts with an
option to revert the whole transition. It never picks another leaf through a
replacement plan. The resulting missing-interior state is incomplete and cannot
be submitted; independently owned options still follow their scoped validity and
retention policies. This is the same dependency-loss/revert path used when an
interior loses a prerequisite, not a silent interior substitution.

All these facts have evidence and decision lineage (§7). Acquisition priorities
are unique where competing sources select alternative defaults in the same group.
Different causes for the same target are retained, not discarded by priority.
Overlapping acquisitions with contradictory intent or peer policies require an
explicit scoped resolution; numeric ordering alone cannot decide ownership.
Conflicts and requirements are final validity constraints regardless of whether
an endpoint entered through user selection, a package, an interior or a default.
A locked package child cannot be displaced while leaving an invalid parent active.
The replacement plan can remove that parent when authorized by the common policy.

**Concrete translation of a condition.** In GS, a DMX roof acquisition has only
convertible configurations, clause 1 = resolved DMX, clause 2 = any resolved
G26/G4Z/GBK/GKZ/GPH, target D84, origin dependency, preserve-prior intent. DMV uses
that paint set, DMY uses G26/G4Z/GBK/GTR, DMW uses G26/G4Z/GBK; DMU has no such
acquisition. GSX owns independent corresponding records. These are the exact
17 stripe/paint requirements per lane in GS-R04 and GSX-R05. A satisfaction
requirement also ensures that removing D84 cannot leave the triggering stripe
and paint together. Prohibited stripe/paint pairs are separate conflicts.
D84 costs 1,295 through its option price, and its content effect omits the roof
stripe whether acquisition was automatic or independent.

Hash→Z15 and EL9→Z25 are acquisitions plus continuing requirements. An attempted
hash/interior is evaluated in tentative state so the package can be acquired
before validating satisfaction; a pre-acquisition gate would incorrectly reject
entry. Requiring ANY(FEB, FEY) is one alternative clause, not two AND requirements.
An interior + paint or belt condition supplying D30 uses the same condition and
acquisition family. Two satisfied causes still acquire and charge D30 once.

Source direct/group/default rows are translated by meaning, not copied one for
one. Four legacy default forms become explicit conditions including group vacancy.
Rule scopes must preserve effective observed scope unless an accepted decision
changes it: e.g. ST convertible BCP requires ZZ3; coupe BCP does not require B6P.
The five Z06 derived CBF replacement edges need individual source-code anchors and
explicit target records. No blanket includes-closure permission applies elsewhere.

### Runtime state and transaction contract

These are transient evaluator concepts, not additional authoring tables:

- `intent(option_id)` records a committed independent purchase and its acquisition
  sequence. A package-supplied item is not independent merely because it is visible
  or clicked while locked. Preserved intent keeps its original acquisition order.
- `cause(target, acquisition_or_part_id, source_instance)` distinguishes independent,
  standard, default, interior and relationship origins. A cause must be supported
  by a live root; an inclusion cycle cannot keep itself alive after all roots vanish.
- Resolved selections, suppressed default/installed equipment, chosen interior,
  charge lines and validation messages are derived from those roots and facts.
  Displaced intent is removed; it is not a stack of purchases to restore later.

On a proposed action, resolve a candidate build without modifying the committed
state. Reconcile acquisitions and requirements, incompatible sets, dependent loss
and eligible defaults; calculate final content and charges. A compatibility issue
shows the affected selections, additions, removals and price consequences before
confirmation. Cancel preserves the entire prior build, including intent and cause
history. Confirm commits one valid, disclosed transition. Dependency-loss cleanup
removes unsupported dependents and charges, alerts, and offers to revert the
triggering transition. Revert restores the prior state as a whole, not a guessed
subset. Body/trim/model change uses the recorded reset policy, not cross-model
intent carryover. Missing required interior/group selections leave an incomplete
build that cannot be submitted.

Positive acquisitions use rooted closure; default rules with absence tests run
against the reconciled candidate, followed by revalidation. The eventual evaluator
must detect repeated states/contradictions and fail the candidate transition
without committing partial changes. Source cycles may be meaningful and are not
all forbidden, but self-supporting cycles and ambiguous competing defaults cannot
be accepted as valid results. This algorithm contract needs implementation proof;
FKs alone cannot establish convergence or compatibility.

Intent policy runs on acquisition transitions, not repeatedly while recomputing
closure. It is explicit per acquisition, never one global restore flag:
Stingray's retained absorbing package cases consume prior child intent. Later
model scopes preserve their accepted independent purchases. PDV's paid cap peer
survives under ST-D06. ZR1/ZR1X retain TOM after ZTK only if independently acquired
before the package; package-only TOM disappears. A cover displaced by TOM/ZTK
stays deselected and uncharged after removal. An independently owned item still
must satisfy current compatibility and prerequisites.

## 5. Pricing and projections

| Owner | Resolution | Invariant |
|---|---|---|
| Configuration starting amount | Exactly one amount/basis in the selected configuration | Destination included once on the accepted baseline basis; do not also add a destination line. Preserve any source breakdown as evidence. |
| Option default purchase amount | One amount/basis on the model-owned option | `priced` requires a known applicable rate; `no_separate_charge` explicitly has no own monetary line. Null does not choose that mode. |
| `option_rate(R, id)` plus configurations | Target option, condition FK, explicit precedence, exact replacement amount/basis | First applicable priority wins, then default purchase amount. No additive discount stacking or specificity inference. Overlap must have documented precedence; duplicate priority for a target is rejected. |
| Non-option extra | `component_rate` for selected interior part and configuration | Charge once per component in the selected leaf; no seat/R6X duplication. |

Standard-only informational equipment is not a charge candidate. For acquired
priced options, context rates explicitly implement included zero or discounted
amounts. Acquisition alone does not imply free content: TOM is acquired by ZTK
but costs 12,995. SBT includes SC7 at zero in the accepted target, even when SC7
has preserved independent intent; after SBT removal, independently owned SC7 uses
its standalone price. This requires selection and cause origins to remain visible
to pricing eligibility, with model-qualified predicates, not a global rule that
all automatic options are free. `option_rate` conditions use the named selection
state; charge eligibility additionally distinguishes standard-only causes from
purchase and interior-part causes plus default, included and dependency causes.
Those non-standard causes make a priced option eligible for its applicable rate;
zero still requires an explicit rate, not an assumption about its origin.

Hash choices with null source rates require an explicit translated
`no_separate_charge` classification supported by the accepted Z15 ownership;
that does not convert every null source option into free content. A release cannot
publish an unresolved purchasable rate merely because its example build omits it.
Retired or factory-unavailable cards cannot acquire or charge. Source-qualified
prices, including wheel conditions and column-D qualifiers for column-E option
amounts, must be represented and reconciled before release.

The calculated charge key is `(R, option_id)` or `(R, selected_interior_id,
component_id)`. Displaying the seat under Interior does not change its owner.
The quote totals configuration base + option lines + non-option part lines.
No separately edited interior total, package residual or package credit exists.

| Output | Relations / state supplying it | Kept distinct from |
|---|---|---|
| Informational standard equipment | `option_configuration` standard statuses, effective lifecycle/display policy | The installed configuration after replacements. |
| Configured equipment and order codes | Rooted resolved build, `equipment_substitution`, emission policy | Click history and raw static statuses. |
| Purchases and line items | Independent/acquisition state plus charge owners/rates | Merely present hardware, labels and static equipment. |
| Physical supplied content | `content_effect` with typed conditions and aspect | A new purchasable SKU or inferred price. |
| Visualizer manifest | Resolved build plus asset bindings, pinned to release | Eligibility and price authority. |

`equipment_substitution(R, id)` has configuration scope, condition FK, removed
option FK and optional replacement option FK. It suppresses installed output;
it neither charges nor acquires the replacement. Replacement content must have
its own valid acquisition cause. `content_aspect(R, id)` owns a stable aspect key
and label. `content_effect(R, id)` has scope, condition FK,
`content_aspect` FK, additive/replacement mode, description and precedence. The
aspect is model-owned, with unique replacement precedence when effects overlap.
Examples include a second roof, second-set wheel hardware, body-specific carbon
surfaces and a wing-compatible cover. They do not invent manufacturer codes.

`emission_policy(R, option_id)` owns code-emission role, state projection
(`resolved_selection` or `installed_equipment`), summary destination and order.
Equipment emissions honor substitutions; purchase/order-only codes use resolved
selection as classified by their evidence. RPO is emitted only when that role and resolved state permit it; reference-only
CFX remains nonselectable. Duplicate RPOs are not silently collapsed to an arbitrary
identity. Any required consumer deduplication must have a reviewed mapping while
retaining contributing identities. ST T0A/ZF1 behavior follows ST-D04, including
the difference between wing and TVS deletion paths; a content description cannot
substitute for the explicit output-code effects.

## 6. Presentation and media

| Relation | Grain / key | Ownership |
|---|---|---|
| `step`, `section`, `summary_section` | `(R, id)` each | Labels, explicit order, navigable/display roles. Section has step FK; equipment-only buckets need not be navigable. |
| `option_presentation` | `(R, option_id)` | Section, placement, choice order, display role; no duplicate option name/price. |
| `step_summary` | `(R, step_id)` | Summary-section FK; emitted options use the appropriate route. |
| `context_control`, `context_copy` | `(R, axis)`; `(R, axis, value, configuration_id)` | Body/trim chooser and exact contextual tooltip/copy. Values must occur in configurations; expand source general/exact precedence before authoring. |
| `interaction_policy` | R | Compatibility notice/confirm/cancel and dependency-loss alert/revert semantics, disclosure templates and source-policy version. Product replacement plans remain model-owned. |
| `asset` (global), `asset_binding` | Asset ID; `(R, binding_id)` | Immutable media content/hash, media type/dimensions; binding has exactly one typed option/interior/configuration target, role, alt text, fit/position and precedence. |
| `visual_scene`, `visual_layer`, `visual_binding` | `(R, scene_id)`; `(R, scene_id, layer_key)`; `(R, binding_id)` | Scene/view, ordered layers; asset FK, explicit configurations and condition FK. Visual conditions additionally allow typed resolved-installed-equipment tests. Unique precedence per layer. |

Sections own presentation only; moving an option between sections cannot alter
choice-group membership, cardinality or validity (§4).

All mutable copy, ordering and bindings are revision-owned. Identical source media
can share an immutable asset without sharing option meaning. Shared asset-map
fallbacks are expanded into reviewed model-owned bindings; exact model assignments
win. A missing image produces a missing/fallback visual result and cannot change
selection eligibility. Current `.psb` artwork is uninspected: actual scenes,
renditions and coverage remain later visualizer work. No media processing or
front-end stack is selected by this logical proposal.

## 7. Evidence, translation, revisions and releases

| Relation | Grain / key | Meaning and integrity |
|---|---|---|
| `source_document`, `source_anchor` (global) | Document ID unique by content hash; anchor ID unique within document + locator + fragment | Original bytes/name and supplied revision/date if known; sheet/cell/range, rich text/value/type, or pinned code/observation locator. Acquisition metadata does not invent publication dates. |
| `evidence_set`, `evidence_member` (global) | Set ID; `(set_id, anchor_id)` | Real anchor FKs. Every authored fact row, including association and scope rows, references evidence; copied scope can cite its source plus translation rationale. |
| `review_decision`, `decision_set`, `decision_member` (global) | Decision ID/version; set ID; `(set_id, decision_id, version)` | Authority, date, state, text and evidence. Fact rows hold nullable decision-set FKs, permitting lane decisions plus the overriding common policy. Prior decision versions remain immutable. |
| `source_disposition` | `(R, anchor_id, fragment_key)` | Unchanged/added/changed/removed/ambiguous/conflicting/not-applicable classification, rationale and decision set. Source coverage, not an executable rule or price store. |
| Typed `*_translation` links | `(R, disposition_key, target_id)` per target kind | Composite FKs to disposition and concrete target row. Many-to-many mapping supports splits and corroboration; removed/evidence-only fragments may have no target with an explicit reason. No unenforced table-name/ID pointer. |
| Typed `legacy_*_mapping` | `(R, namespace, legacy_key)` per exported kind | Target FK; stable runtime option/interior/configuration IDs, aliases and relevant rule references. New additions need explicit new consumer IDs. |
| `release`, `release_model`, `release_artifact` (global) | Release ID; `(release_id, model_id)`; `(release_id, artifact_role, path)` | Declared model year; membership carries `year`, M and R with the composite FKs below enforcing the matching lane/year; one frozen revision per lane in that year, explicit membership/order/aliases, immutable artifact hashes and manifest. Release default-model FK targets membership; unique paths/aliases within release. |
| `publication_pointer` (global) | Channel key | FK to a completed release; compare-and-swap version. Publication and rollback change the pointer, never frozen catalog facts. |

Release membership is constrained through explicit composite keys:

- `release` has unique `(release_id, year)` in addition to its primary key.
- `release_model(release_id, model_id, year, M, R)` has primary key
  `(release_id, model_id)` and all five columns are non-null.
- Its `(release_id, year)` FK references `release(release_id, year)`.
- Its `(M, model_id, year)` FK references the corresponding unique key on
  `model_year`; M cannot stand for another lane or year.
- Its `(R, M)` FK references `catalog_revision(R, M)`; the pinned revision
  must belong to that exact model-year.

Together these FKs reject a revision from the wrong model or declared release
year. Frozen-state eligibility remains a release validation requirement; the
composite FKs enforce identity, not lifecycle state.

A draft copies a complete prior revision and uses an edit version for stale-edit
refusal. Related accepted changes are one transaction. Freezing validates the
snapshot; it does not deploy it. A release pins frozen revisions, evaluator/format
versions, compatibility-policy version and media references. All form, order and
visualizer outputs use that same manifest. Candidate generation and validation
precede atomic publication; failure leaves the last good pointer intact. An old
release remains reproducible even after rates, presentation or rules change.
The first complete target release must account for all six lanes; later partial
lane edits still publish a complete manifest with unchanged frozen revisions for
unaffected lanes. No cross-model product FKs are needed for atomic releases.

This is a lifecycle design, not an authoring API or deployment implementation.
Customer records and submitted orders do not belong in the product catalog. A
future configuration/order reference identifies its release and input identities;
consumer/server validation must resolve that release rather than accepting a
client-supplied total. External dealer approval, emissions/service ordering and
successful submission remain outside the accepted customer-form scope.

### Translation coverage and existing-code disposition

The [workbook translation blueprint](workbook-translation-blueprint.md#complete-source-family-map)
retains the complete 77-sheet source map. The proposed target destinations are:

| Source family | Proposed destination / disposition |
|---|---|
| Model/year, variant membership, registry | Model-year/revision, exact configurations and release membership; source routing stays provenance. |
| Options, availability, overrides | Model-owned options, complete status matrix, contextual lifecycle and presentation. Preserve inactive identities; apply additions/retirements explicitly. |
| LT/LZ interiors, scope, hierarchy, PriceRef, components | Exact model leaves, memberships, navigation and single-owner prices. Stored sums and combined rate rows remain comparison evidence. |
| Direct/group/exclusive/default/color rules, raw scopes | Typed conditions, requirements, acquisitions, conflicts, groups/defaults and explicit scope sets. One semantic relation may combine several source rows; no double execution. |
| Conditional price rules | Ordered model-qualified total overrides; expanded component contexts; preserve source order only where behavior gives it meaning. |
| Steps, sections, summaries, context copy, asset map | Revision-owned presentation and media bindings; code-supplied buckets retain code anchors. |
| Phrase map, empty exception sheet, omitted guide offerings | Evidence/disposition, not new executable rules or customer selections. |
| Code-owned semantics and five Z06 derived edges | Explicit acquisition, replacement, charge and emission policies with pinned code plus decision provenance. |
| Accepted overlays and common policy | Complete fact/relationship/copy/lifecycle corrections with decision sets; not just offering-level `retain` flags. |

Reuse the disposable importer's source-preservation and composite-FK principles,
not its physical schema as a starting migration. Keep `catalog/importer.py`,
`catalog/contracts.py`, `catalog/parity.py`, frozen archives and discovery probes
as baseline comparison tools. The old R6X adjustment, `requires_z25` consumer flag,
global interior/rate ownership, raw scope authoring and single-baseline lifecycle
are not the target architecture. No shim, renamed schema version or in-place
migration of disposable files is proposed. Future implementation starts in a new
bounded slice after design review.

Translation must classify all 1,379 baseline offerings, 7,448 availability pairs,
704 model-interior leaves, 783 direct source rules (35 filtered / 748 emitted),
and five additional Z06 derived edges. These are source inventories, not required
final target row counts. Additions, retirements, relationship splits and explicit
scope expansion change target counts for documented reasons. Exact identities,
values, memberships, qualifiers and consequences establish completeness.

## 8. Six-model connected design walkthroughs

These are paper traces from each [structured handoff](model-discovery.md#current-model-handoffs),
its accepted overlay and the common policy. B means the selected configuration's
starting amount including its accepted destination treatment. Totals below name
only the stated options/interior components unless a full context is supplied.
Baseline observations remain frozen. Each trace covers input, applicability,
selection/removal, charges/output and authority; none claims target execution.

### Stingray

[Handoff](stingray-structured.md), [decisions ST-D01–12](stingray-owner-decisions.json).
Six body/LT configurations and 130 leaves remain explicit.

| Path | Logical records and result |
|---|---|
| Choose 1LT UQT, then switch to 2LT | At 1LT, UQT has available status and a priced independent purchase amount of 1,495. At 2LT/3LT it has standard status and a scoped standard acquisition, whose standard-only cause is not charge eligible. The configuration reset removes the earlier purchase intent. No lingering purchase charge; missing interior still blocks submission. |
| Select `3LT_R6X_AE4_HXO_N26_38S` | Seat option + R6X part + two components give 2,780, exactly +595 versus frozen defect. No balancing rate or doubled seat; ST-D03. |
| G26/HUQ plus a D30-triggering belt, remove causes separately | Two conditions/acquisition causes, one D30 owner. Removing one retains the other; removing the last removes its charge. Valid belt defaults are resolved independently. |
| Independent VWE → PCU → remove PCU | ST-S05/ST-T16 retained absorption consumes the prior child intent; package-only child disappears. Contrast paid PDV cap: full 750 package plus paid cap, then cap survives package removal under ST-D06. No blanket later-lane retention imported. |
| PCX → attempt incompatible accessory wheel | Conflict plan discloses a compatible replacement, including removal of the conflicting package where needed; cancel preserves build. Cannot retain PCX with that paid wheel or invent a package credit. |
| Z51 + 5ZU; compare TVS + Z51; lose wing paint prerequisite | Explicit emission effects remove T0A without adding ZF1 for 5ZU; TVS path adds ZF1. Unsupported wing is removed with alert/revert, replacing historical retained-invalid behavior. RNX may use the accepted Z51+ZF1 path; unavailable 5ZZ stays inactive. ST-D04/07/09. |
| Add DTC/SAI, retire DUW; review standard versus installed view | New identities 1,295/295, exact guide conflicts including GTR / trim-qualified V8X; no DUW edge rename. Installed equipment follows substitutions; static trim view stays labeled. Omitted dealer/service offerings stay outside selection. |

### Grand Sport

[Handoff](grand-sport-structured.md), [decisions GS-D01–16](grand-sport-owner-decisions.json).
Six configurations and 132 exact leaves; no standard GSX brake assumptions.

| Path | Logical records and result |
|---|---|
| Convertible 2LT G26/97A → DMX | Two-clause dependency acquisition adds D84 1,295. GS-T06 full-context target 107,175 versus frozen 105,880; disclose roof-stripe omission. On loss, remove dependency-only D84; retain independent valid D84. Cancel/revert preserves prior state. |
| Select Heritage hash; separately select EL9 in its permitted context | Hash acquires Z15 995 with the exact accepted disclosure. EL9 separately acquires Z25 1,995, AH2 zero or AE4 +595, locked 3F9 zero; EL9/AE4 contribution 2,590. No hidden Z25 charge owner or orange-belt target. |
| FEB / FEY support J57, T0F and B4Z; remove a package | AND/ANY requirements and cause ownership keep remaining FEY-supported equipment, remove unsupported dependents/charges. B4Z only with FEB or FEY. J6A→J6D with J57; loss restores J6A from J6D/J6L, retaining other valid paid calipers; restore eligible wheels. GS-D06–08. |
| Four R6X/AE4 paths; independent package child round trip | Target component subtotals 2,085/1,590/2,780/2,285, each +595. Preserve independent intent under GS-D16; automatic causes alone do not become independent purchases. |
| Graphics conflict and unavailable-card attempts | Exact VPW/VPO sets use notice/confirm/cancel, superseding refusal prose. Factory lifecycle remains separate. Add DTC/SAI, retire DUW and only `opt_t0e_002`, retain `opt_t0e_001`; naming corrections do not merge identities. |

### Grand Sport X

[Handoff](grand-sport-x-structured.md), [decisions GSX-D01–14](grand-sport-x-owner-decisions.json).
Six configurations and 132 leaves with its own rates and equipment.

| Path | Logical records and result |
|---|---|
| EL9 with AE4, then change to a non-EL9 leaf | Acquisition emits Z25 and charges 1,995 plus seat 595, with locked zero 3F9. Cause removal drops unsupported Z25 content/charge; new leaf and belt validity resolve normally. Fixes missing output, not just arithmetic. |
| Convertible 2LT G26/97A → DMX → lose roof cause | GSX-T09 target 129,275 versus frozen 127,980. Own conditional sets add D84 1,295; independent valid D84 survives, automatic-only D84 goes. CM9 selection cannot leave an incompatible required-roof build. |
| Start standard J57/B4Z/FE5; add/remove FED | Standard acquisitions retain this lane's brakes; FED changes tires. Do not apply GS's FEB/FEY requirement to standard B4Z. |
| Convertible ZZ3 and configured engine output | Retire exactly GSX-D14's two LS6 edges (rows 51/82); keep standard LS6, ZZ3→BC7/SL9 and valid coupe lighting causes. HP1 uses the accepted axle-only copy, not combined output. |
| Interior/package/graphics and source-identity checks | Four seat corrections use LT subtotals; independent ownership follows GSX-D12. Existing DTC gets complete conflicts; add SAI, no DUW/T0E retirement invented. Retained 5ZB carries price-only guide evidence. Static/installed displays and factory-unavailable cards stay distinct. |

### Z06

[Handoff](z06-structured.md), [decisions Z06-D01–12](z06-owner-decisions.json).
Six LZ configurations, 130 leaves; wheel-qualified rates remain local.

| Path | Logical records and result |
|---|---|
| PDB selected → request Z07 | Named replacement plan offers PDD switch with disclosed changes and rates; cancel preserves PDB build. Confirm validates the resulting package/wheel state. Never allow PDB+Z07, silently choose PDF, or retain the rejected 9,000-premium path. Common policy overrides older alternatives. |
| J57/Z07/PDD/PDF and wheel changes | Scoped acquisitions restore gray J6D by default with compatible paid alternatives. Rates map the handoff's 54-state matrix, not a single package price; five CBF derived edges have explicit code provenance. R8E 2,600 becomes 3,000 with T0F/T0G. |
| PCZ and second-set wheels | Package 5,295 includes 5DK/SFZ/SHT/VPO at zero additional charge. Full local conflict sets and independent-child intent apply. Factory wheels remain; supplied nuts/locks/bronze caps are content without duplicate purchases. |
| SC7 → SBT → remove SBT; repeat package-only | SBT 2,525, SC7 zero while supplied; prior independent SC7 returns to standalone charge, package-only SC7 disappears. No frozen 2,720 target. |
| Four AE4/R6X leaves; N2Z at 3LZ | Add missing 595 once; preserve N2Z 895 and LZ extras. N2Z replaces N3W in installed equipment; static trim information remains distinct. |
| Stripe/paint, RXI/SLN, lifecycle and source corrections | All 15 stripe/paint pairs and full graphic/package sets use notices in both directions. SLN remains otherwise available in Z06, unlike some other lanes. DTC/SAI additions, DUW retirement and DUE naming follow local decisions. |

### ZR1

[Handoff](zr1-structured.md), [decisions ZR1-D01–09](zr1-owner-decisions.json).
Four 1LZ/3LZ configurations and 90 leaves; guide columns D:G.

| Path | Logical records and result |
|---|---|
| Independent TOM → ZTK → remove ZTK | TOM owner 12,995; ZTK owner 5,995. Combined contribution 18,990; removal retains prior TOM at 12,995. Fresh ZTK removal also removes its automatic TOM. |
| Cover → confirm ZTK displacement → remove ZTK | Cover intent is cleared, stays uncharged and deselected. No restoration stack. Any retained TOM still imposes its cover conflicts. |
| ZTK installed versus static equipment | Rooted acquisitions/substitutions show J59/FEJ/XFS instead of J58/FE8/XFR. Static trim view remains explicitly informational. Correct dormant CFC→GBA and EFR scope before standard promotion; restore appropriate DY0/CFV/FE8/N3W. |
| SBT, four R6X paths, UQT and R8E | SBT 2,525 with SC7 zero; independent children preserved. Four subtotals 1,590/2,085/2,485/2,980 include AE4 once. UQT standard; R8E 3,000. No ZR1X ZTK rate or Z06 recorder charge. |
| DTC groups, unavailable cards, DUW/SAI | Three complete local graphic groups; compatibility notice versus inactive factory cards. Retire DUW by owner decision despite guide presence, retain existing DTC; SAI with its V8X scope. Separate configured content, line items and order disclosures. |

### ZR1X

[Handoff](zr1x-structured.md), [decisions ZR1X-D01–09](zr1x-owner-decisions.json).
Four configurations and 90 leaves; guide H:K is independently sourced.

| Path | Logical records and result |
|---|---|
| TOM → ZTK → remove ZTK, and package-only control | TOM 12,995 + local ZTK 1,500 = 14,495; retain only pre-existing independent TOM. Package-only removal removes both charges. Displaced covers remain deselected. |
| ZTK and baseline restoration | J59 remains standard; configured build shows FEZ/XFS/TOM with ZTK, restores FEH when appropriate after removal. Do not install static XFR in the ZTK view. |
| Convertible standard roof with nonblack paint | Remove exact CFC→GBA rule at `zr1x_rule_mapping` row 5 before restoring standard content. Existing DY0/CFV static entries are retained, not treated as missing ZR1 entries. N2Z replaces 3LZ N3W. |
| SBT/SC7 and AE4/R6X | Package 2,525 plus zero included pouch; preserve prior independent ownership. Four corrected totals 1,590/2,085/2,485/2,980 match local component evidence, not a global interior rate. |
| Presentation, prices and lifecycle | R8E 2,600; UQT/J59 standard; E60 3LZ-only. Retain this lane's HP1 combined-with-LT7 copy; do not copy GSX's correction. Complete three DTC groups, add SAI 295, rename DUE, retire DUW while preserving source. Factory-unavailable PCQ/VWT/R88/SLN cannot acquire charges. |

### Decision coverage index

This maps every accepted decision to the proposal, without rewriting the overlays
or presenting a second editable decision authority.

| Lane | Decisions → sections |
|---|---|
| ST (12) | D01/02 → 1, 2, 7; D03 → 3, 5; D04/08/09 → 4, 5; D05 → 2, 6; D06/07 → 4; D10 → 5, 6; D11 → 7; D12 → 1, 5. |
| GS (16) | D01/02/10/13 → 1, 2, 7; D03/04/06/07/08/12/16 → 4; D05/09/14 → 3, 5; D11 → 2, 6; D15 → 5, 7. |
| GSX (14) | D01/04/06/12/14 → 4, 7; D02/03/05/10 → 3, 5; D07/08/13 → 1, 2, 7; D09 → 2, 6; D11 → 5, 7. |
| Z06 (12) | D01/02/03/04/05/07/11 → 4, 5; D06 → 4, 5; D08 → 3, 5; D09 → 1, 2, 7; D10 → 2, 5; D12 → 1, 5, 7. |
| ZR1 (9) | D01/09 → 2, 5; D02 → 2, 6; D03/04/08 → 3, 5, 7; D05/06 → 4; D07 → 1, 2, 7. |
| ZR1X (9) | D01/09 → 2, 5; D02 → 2, 6; D03/04/08 → 3, 5, 7; D05/06 → 4; D07 → 1, 2, 7. |

## 9. Review outcome and next bounded work

**The six lanes fit this logical model without a new business-policy choice.**
Recommended architectural choices are explicit revision snapshots, model-owned
interiors and rates, typed AND/ANY conditions, separate acquisition and continuing
requirements, one charge owner, and a release manifest that pins all consumers.
These choices are proposals to review, not a claim that the schema is approved or
that the corrected behavior exists. They avoid unproven shared-product indirection
and preserve the evidence-backed differences between lanes.

This documentation was checked for consistency with the consolidated review,
all six owner overlays, the common policy, the older schema's known limitations
and the cited handoff examples. Existing handoff validation remains a check on
inputs, not on hypothetical target FKs. No DDL or target evaluator was available
to run; walkthroughs do not establish constraint enforcement, convergence,
corrected-runtime parity, browser behavior or release/rollback reliability.

The [relationship diagram slice](master-schema-diagram.md) now inventories all
named relations and their keys/FKs, settles identity membership and the group
scope constraint, and lists remaining naming/allocation opens. Before implementation, the next separately
authorized design slice is representative populated tables with worked selection,
pricing, removal and build-output traces. These must demonstrate the keys and
constraints above, resolve the relevant opens and make the design's complexity
assessable. Only after that review should a separately
authorized disposable relational foundation cover revisions, identities,
configurations, options, applicability and typed provenance, with a six-lane
source translation sample and constraint tests. It should not begin the authoring UI or claim full
migration. Conditional rules, intent transitions and prices then need a bounded
evaluator slice with independent expected targets from the retained evidence.
Select physical storage/DDL and exact implementation scope in that task; SQLite,
API and front-end choices remain uncommitted here.

Implementation acceptance must distinguish:

1. Baseline parity: preserved source identities/values/behavior against the frozen
   workbook/runtime, including classified defects and inactive records.
2. Accepted corrections: a complete decision-linked delta across relationships,
   prices, lifecycle, copy and output; both selection orders, removal, notice
   confirmation/cancellation and revert require affected-flow verification.
3. Release proof: FK/model/year isolation, explicit scope coverage, exact rates,
   rooted acquisition and default convergence, required-interior rejection,
   deterministic output, atomic publication and recovery. Test these as their
   implementations arrive, without adding speculative enforcement now.

The current workbook remains canonical. This task stops at the logical proposal.
