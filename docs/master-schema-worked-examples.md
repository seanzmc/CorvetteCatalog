# Master-schema populated tables and worked traces

Design examples for [proposal §9](master-schema-proposal.md#9-review-outcome-and-next-bounded-work), using the merged [diagram keys](master-schema-diagram.md) and [Identity membership](master-schema-diagram.md#identity-membership). No DDL, importer, evaluator, canonical-data edit or runtime proof. These are representative logical rows, not a complete release candidate.

Baseline: current `origin/main` at `9cd811451d31eb1cc42d3a00ab729e0cc94a5fa0`. Frozen handoffs and accepted overlays are unchanged. The [common policy](compatibility-notice-policy.json) applies after each overlay, including its explicit ST and Z06 UI overrides. Older blocked-card descriptions are historical.

## Reading the populated rows

A dagger (`†`) is the diagram's existing notation alias, not a proposed column name. Unnamed payload is described as **logical facts**, never assigned new column names. M/R, `ex:` IDs, `USD-options`/`USD-base`, and `A:` anchor handles are example values: the handoffs do not allocate target revision/condition/substitution/plan IDs. Existing configuration, option, interior, rule and rate IDs below are copied exactly. No RPO serves as an FK. The design resolutions under Open O1/O2/O6 define allocation; the illustrative values here remain fixtures.

Each identity-bearing table row below explicitly displays **two records**: the continuing typed identity `(M, id)` and its version `(R, id)` carrying M, with owner FK `(R, M)`. The relation column determines the concrete kind; a condition and acquisition with the same spelling are not one identity. Configuration, option, interior use their named families; every other identity-bearing relation used here is in RULE_IDENTITY. No component or presentation identity-bearing relation is instantiated. There are no predecessor links in this one-year sample.

Association tables have their full diagram PK and **no identity row**. `c = a, b` expands to two rows with those literal configuration IDs, not an array, wildcard, implicit all-scope or omitted unavailable pair. R always means the lane's R below. All endpoint FKs have that same R. This finite expansion keeps the 32 configuration and sampled status/scope rows readable.

Every row's last cell gives its immutable evidence locator and governing decision(s). These are human-readable lineage, not newly allocated `evidence_set_id†`/`decision_set_id†` values. The evidence-set/decision-set containers are not instantiated; O2/O7 below specify their linkage and allocation; this sample does not populate them. Source JSON sheet locators mean `baseline_rows[sheet]` selected by `_row`, not JSON line numbers. Handoff identifiers such as GS-T06 and GS-P02 are searchable row IDs in the linked handoff. Amounts are exact USD; `USD-options` means accepted option purchase basis, `USD-base` means vehicle starting amount with destination once, excluding separately acquired R8E. Null source prices are preserved as evidence, never presumed free purchases.

## Lane ownership and configuration rows

The model key is the model_id example value. M and R are deliberately unique per lane; R is a proposed snapshot handle, not a frozen production revision. Each row supplies `model(model_id)`, `model_year(M, model_id, year)` and `catalog_revision(R, M)` with revision number 1, draft. Parent revision is null; none is freeze-certified.

| Lane | model_id | M | R | year | Evidence and decision |
|---|---|---|---|---:|---|
| ST | `stingray` | `M-ST-2027` | `R-ST-1` | 2027 | [stingray source model_key/model_year](stingray-structured-records.json); [ST-D06/10/12](stingray-owner-decisions.json) |
| GS | `grand_sport` | `M-GS-2027` | `R-GS-1` | 2027 | [grand-sport source model_key/model_year](grand-sport-structured-records.json); [GS-D03/04/05/14/15/16](grand-sport-owner-decisions.json) |
| GSX | `grand_sport_x` | `M-GSX-2027` | `R-GSX-1` | 2027 | [grand-sport-x source model_key/model_year](grand-sport-x-structured-records.json); [GSX-D10/11/12/14](grand-sport-x-owner-decisions.json) |
| Z06 | `z06` | `M-Z06-2027` | `R-Z06-1` | 2027 | [z06 source model_key/model_year](z06-structured-records.json); [Z06-D01/11/12](z06-owner-decisions.json) |
| ZR1 | `zr1` | `M-ZR1-2027` | `R-ZR1-1` | 2027 | [zr1 source model_key/model_year](zr1-structured-records.json); [ZR1-D01/06/08/09](zr1-owner-decisions.json) |
| ZR1X | `zr1x` | `M-ZR1X-2027` | `R-ZR1X-1` | 2027 | [zr1x source model_key/model_year](zr1x-structured-records.json); [ZR1X-D01/06/08/09](zr1x-owner-decisions.json) |

`M-ST`/`R-ST` below abbreviate `M-ST-2027`/`R-ST-1`, likewise each lane. They are value aliases only. Both price-basis handles have currency USD and resolved meaning above; their required evidence is the lane price-basis decision and handoff §3/§4, with global linkage specified in O7 below but not populated here.

| configuration | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts | Evidence and decision |
|---|---|---|---|---|
| ST | `(M-ST, 1lt_c07)` | `(R-ST, 1lt_c07)`; `(R-ST, M-ST)` | coupe, 1lt; enabled; USD 73,495.00; `basis_id†=USD-base` | [variant_master!2](stingray-structured-records.json); ST-D06/10/12 |
| ST | `(M-ST, 2lt_c07)` | `(R-ST, 2lt_c07)`; `(R-ST, M-ST)` | coupe, 2lt; enabled; USD 80,595.00; `basis_id†=USD-base` | [variant_master!3](stingray-structured-records.json); ST-D06/10/12 |
| ST | `(M-ST, 3lt_c07)` | `(R-ST, 3lt_c07)`; `(R-ST, M-ST)` | coupe, 3lt; enabled; USD 85,245.00; `basis_id†=USD-base` | [variant_master!4](stingray-structured-records.json); ST-D06/10/12 |
| ST | `(M-ST, 1lt_c67)` | `(R-ST, 1lt_c67)`; `(R-ST, M-ST)` | convertible, 1lt; enabled; USD 80,495.00; `basis_id†=USD-base` | [variant_master!5](stingray-structured-records.json); ST-D06/10/12 |
| ST | `(M-ST, 2lt_c67)` | `(R-ST, 2lt_c67)`; `(R-ST, M-ST)` | convertible, 2lt; enabled; USD 87,595.00; `basis_id†=USD-base` | [variant_master!6](stingray-structured-records.json); ST-D06/10/12 |
| ST | `(M-ST, 3lt_c67)` | `(R-ST, 3lt_c67)`; `(R-ST, M-ST)` | convertible, 3lt; enabled; USD 92,245.00; `basis_id†=USD-base` | [variant_master!7](stingray-structured-records.json); ST-D06/10/12 |
| GS | `(M-GS, 1lt_e07)` | `(R-GS, 1lt_e07)`; `(R-GS, M-GS)` | coupe, 1lt; enabled; USD 88,495.00; `basis_id†=USD-base` | [variant_master!8](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| GS | `(M-GS, 2lt_e07)` | `(R-GS, 2lt_e07)`; `(R-GS, M-GS)` | coupe, 2lt; enabled; USD 95,595.00; `basis_id†=USD-base` | [variant_master!9](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| GS | `(M-GS, 3lt_e07)` | `(R-GS, 3lt_e07)`; `(R-GS, M-GS)` | coupe, 3lt; enabled; USD 100,245.00; `basis_id†=USD-base` | [variant_master!10](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| GS | `(M-GS, 1lt_e67)` | `(R-GS, 1lt_e67)`; `(R-GS, M-GS)` | convertible, 1lt; enabled; USD 95,495.00; `basis_id†=USD-base` | [variant_master!11](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| GS | `(M-GS, 2lt_e67)` | `(R-GS, 2lt_e67)`; `(R-GS, M-GS)` | convertible, 2lt; enabled; USD 102,595.00; `basis_id†=USD-base` | [variant_master!12](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| GS | `(M-GS, 3lt_e67)` | `(R-GS, 3lt_e67)`; `(R-GS, M-GS)` | convertible, 3lt; enabled; USD 107,245.00; `basis_id†=USD-base` | [variant_master!13](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| GSX | `(M-GSX, 1lt_g07)` | `(R-GSX, 1lt_g07)`; `(R-GSX, M-GSX)` | coupe, 1lt; enabled; USD 112,195.00; `basis_id†=USD-base` | [variant_master!14](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| GSX | `(M-GSX, 2lt_g07)` | `(R-GSX, 2lt_g07)`; `(R-GSX, M-GSX)` | coupe, 2lt; enabled; USD 117,695.00; `basis_id†=USD-base` | [variant_master!15](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| GSX | `(M-GSX, 3lt_g07)` | `(R-GSX, 3lt_g07)`; `(R-GSX, M-GSX)` | coupe, 3lt; enabled; USD 122,845.00; `basis_id†=USD-base` | [variant_master!16](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| GSX | `(M-GSX, 1lt_g67)` | `(R-GSX, 1lt_g67)`; `(R-GSX, M-GSX)` | convertible, 1lt; enabled; USD 119,195.00; `basis_id†=USD-base` | [variant_master!17](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| GSX | `(M-GSX, 2lt_g67)` | `(R-GSX, 2lt_g67)`; `(R-GSX, M-GSX)` | convertible, 2lt; enabled; USD 124,695.00; `basis_id†=USD-base` | [variant_master!18](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| GSX | `(M-GSX, 3lt_g67)` | `(R-GSX, 3lt_g67)`; `(R-GSX, M-GSX)` | convertible, 3lt; enabled; USD 129,845.00; `basis_id†=USD-base` | [variant_master!19](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| Z06 | `(M-Z06, 1lz_h07)` | `(R-Z06, 1lz_h07)`; `(R-Z06, M-Z06)` | coupe, 1lz; enabled; USD 121,395.00; `basis_id†=USD-base` | [variant_master!20](z06-structured-records.json); Z06-D01/11/12 |
| Z06 | `(M-Z06, 2lz_h07)` | `(R-Z06, 2lz_h07)`; `(R-Z06, M-Z06)` | coupe, 2lz; enabled; USD 130,295.00; `basis_id†=USD-base` | [variant_master!21](z06-structured-records.json); Z06-D01/11/12 |
| Z06 | `(M-Z06, 3lz_h07)` | `(R-Z06, 3lz_h07)`; `(R-Z06, M-Z06)` | coupe, 3lz; enabled; USD 134,945.00; `basis_id†=USD-base` | [variant_master!22](z06-structured-records.json); Z06-D01/11/12 |
| Z06 | `(M-Z06, 1lz_h67)` | `(R-Z06, 1lz_h67)`; `(R-Z06, M-Z06)` | convertible, 1lz; enabled; USD 128,395.00; `basis_id†=USD-base` | [variant_master!23](z06-structured-records.json); Z06-D01/11/12 |
| Z06 | `(M-Z06, 2lz_h67)` | `(R-Z06, 2lz_h67)`; `(R-Z06, M-Z06)` | convertible, 2lz; enabled; USD 137,295.00; `basis_id†=USD-base` | [variant_master!24](z06-structured-records.json); Z06-D01/11/12 |
| Z06 | `(M-Z06, 3lz_h67)` | `(R-Z06, 3lz_h67)`; `(R-Z06, M-Z06)` | convertible, 3lz; enabled; USD 141,945.00; `basis_id†=USD-base` | [variant_master!25](z06-structured-records.json); Z06-D01/11/12 |
| ZR1 | `(M-ZR1, 1lz_r07)` | `(R-ZR1, 1lz_r07)`; `(R-ZR1, M-ZR1)` | coupe, 1lz; enabled; USD 197,195.00; `basis_id†=USD-base` | [variant_master!26](zr1-structured-records.json); ZR1-D01/06/08/09 |
| ZR1 | `(M-ZR1, 3lz_r07)` | `(R-ZR1, 3lz_r07)`; `(R-ZR1, M-ZR1)` | coupe, 3lz; enabled; USD 208,195.00; `basis_id†=USD-base` | [variant_master!27](zr1-structured-records.json); ZR1-D01/06/08/09 |
| ZR1 | `(M-ZR1, 1lz_r67)` | `(R-ZR1, 1lz_r67)`; `(R-ZR1, M-ZR1)` | convertible, 1lz; enabled; USD 207,195.00; `basis_id†=USD-base` | [variant_master!28](zr1-structured-records.json); ZR1-D01/06/08/09 |
| ZR1 | `(M-ZR1, 3lz_r67)` | `(R-ZR1, 3lz_r67)`; `(R-ZR1, M-ZR1)` | convertible, 3lz; enabled; USD 218,195.00; `basis_id†=USD-base` | [variant_master!29](zr1-structured-records.json); ZR1-D01/06/08/09 |
| ZR1X | `(M-ZR1X, 1lz_s07)` | `(R-ZR1X, 1lz_s07)`; `(R-ZR1X, M-ZR1X)` | coupe, 1lz; enabled; USD 227,395.00; `basis_id†=USD-base` | [variant_master!30](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| ZR1X | `(M-ZR1X, 3lz_s07)` | `(R-ZR1X, 3lz_s07)`; `(R-ZR1X, M-ZR1X)` | coupe, 3lz; enabled; USD 238,395.00; `basis_id†=USD-base` | [variant_master!31](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| ZR1X | `(M-ZR1X, 1lz_s67)` | `(R-ZR1X, 1lz_s67)`; `(R-ZR1X, M-ZR1X)` | convertible, 1lz; enabled; USD 237,395.00; `basis_id†=USD-base` | [variant_master!32](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| ZR1X | `(M-ZR1X, 3lz_s67)` | `(R-ZR1X, 3lz_s67)`; `(R-ZR1X, M-ZR1X)` | convertible, 3lz; enabled; USD 248,395.00; `basis_id†=USD-base` | [variant_master!33](zr1x-structured-records.json); ZR1X-D01/06/08/09 |

## ST populated relations

Authority: [ST handoff](stingray-structured.md), [owner overlay](stingray-owner-decisions.json), then [common compatibility policy](compatibility-notice-policy.json). Only the listed relationships are exemplified; unrelated full catalog rules still apply.

| Relation | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|---|
| `option` | `(M-ST, opt_uqt_002)` | `(R-ST, opt_uqt_002)`; `(R-ST, M-ST)` | RPO UQT; priced; default USD 1,495.00; `basis_id†=USD-options`; active target | [stingray_options!69](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_pcx_001)` | `(R-ST, opt_pcx_001)`; `(R-ST, M-ST)` | RPO PCX; priced; default USD 4,595.00; `basis_id†=USD-options`; active target | [stingray_options!74](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_5do_001)` | `(R-ST, opt_5do_001)`; `(R-ST, M-ST)` | RPO 5DO; priced; default USD 4,395.00; `basis_id†=USD-options`; active target | [stingray_options!114](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_5dg_001)` | `(R-ST, opt_5dg_001)`; `(R-ST, M-ST)` | RPO 5DG; priced; default USD 4,395.00; `basis_id†=USD-options`; active target | [stingray_options!115](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_sfz_001)` | `(R-ST, opt_sfz_001)`; `(R-ST, M-ST)` | RPO SFZ; priced; default USD 250.00; `basis_id†=USD-options`; active target | [stingray_options!78](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_sht_001)` | `(R-ST, opt_sht_001)`; `(R-ST, M-ST)` | RPO SHT; priced; default USD 495.00; `basis_id†=USD-options`; active target | [stingray_options!216](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_sng_001)` | `(R-ST, opt_sng_001)`; `(R-ST, M-ST)` | RPO SNG; priced; default USD 320.00; `basis_id†=USD-options`; active target | [stingray_options!58](stingray-structured-records.json); ST-D06/10/12 |
| `option` | `(M-ST, opt_qe6_001)` | `(R-ST, opt_qe6_001)`; `(R-ST, M-ST)` | RPO QE6; priced; default USD 1,095.00; `basis_id†=USD-options`; active target | [stingray_options!240](stingray-structured-records.json); ST-D06/10/12 |
| `condition` | `(M-ST, ex:always)` | `(R-ST, ex:always)`; `(R-ST, M-ST)` | always; no clauses | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `acquisition` | `(M-ST, ex:standard-uqt)` | `(R-ST, ex:standard-uqt)`; `(R-ST, M-ST)` | `condition_id†=ex:always`; `target_option_id†=opt_uqt_002`; standard, locked, preserve_prior; priority 1 | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `condition` | `(M-ST, ex:pcx)` | `(R-ST, ex:pcx)`; `(R-ST, M-ST)` | conjunction; clauses ANDed | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `acquisition` | `(M-ST, rule_opt_pcx_001_includes_opt_5dg_001)` | `(R-ST, rule_opt_pcx_001_includes_opt_5dg_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_5dg_001`; included, locked, absorb_prior; priority 1 | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate` | `(M-ST, pr_pcx5dg_001)` | `(R-ST, pr_pcx5dg_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_5dg_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [price_rules!11](stingray-structured-records.json); ST-D06/12 |
| `acquisition` | `(M-ST, rule_opt_pcx_001_includes_opt_sfz_001)` | `(R-ST, rule_opt_pcx_001_includes_opt_sfz_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_sfz_001`; included, locked, absorb_prior; priority 1 | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate` | `(M-ST, pr_pcxsfz_001)` | `(R-ST, pr_pcxsfz_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_sfz_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [price_rules!12](stingray-structured-records.json); ST-D06/12 |
| `acquisition` | `(M-ST, rule_opt_pcx_001_includes_opt_sht_001)` | `(R-ST, rule_opt_pcx_001_includes_opt_sht_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_sht_001`; included, locked, absorb_prior; priority 1 | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate` | `(M-ST, pr_pcxsht_001)` | `(R-ST, pr_pcxsht_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_sht_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [price_rules!13](stingray-structured-records.json); ST-D06/12 |
| `acquisition` | `(M-ST, rule_opt_pcx_001_includes_opt_sng_001)` | `(R-ST, rule_opt_pcx_001_includes_opt_sng_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_sng_001`; included, locked, absorb_prior; priority 1 | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate` | `(M-ST, pr_pcxsng_001)` | `(R-ST, pr_pcxsng_001)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `target_option_id†=opt_sng_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [price_rules!14](stingray-structured-records.json); ST-D06/12 |
| `conflict` | `(M-ST, ex:pcx-wheel)` | `(R-ST, ex:pcx-wheel)`; `(R-ST, M-ST)` | `source_option_id†=opt_pcx_001`; `source_interior_id†=null`; `activation_condition_id†=ex:always` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `replacement_plan` | `(M-ST, ex:pcx-to-5do)` | `(R-ST, ex:pcx-to-5do)`; `(R-ST, M-ST)` | `condition_id†=ex:pcx`; `requested_option_id=opt_5do_001` (O3); disclose package and child removal | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |

Revision-only associations (R = `R-ST`):

| Relation | Full primary key | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|
| `option_configuration` | `(R, opt_uqt_002, c)` | standard; c = `2lt_c07`, `3lt_c07`, `2lt_c67`, `3lt_c67` | [stingray_ovs!1113,1114,1116,1117](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_uqt_002, c)` | available; c = `1lt_c07`, `1lt_c67` | [stingray_ovs!1112,1115](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_pcx_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!680,681,682,683,684,685](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_5do_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!44,45,46,47,48,49](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_5dg_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!38,39,40,41,42,43](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_sfz_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!896,897,898,899,900,901](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_sht_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!908,909,910,911,912,913](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_sng_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!950,951,952,953,954,955](stingray-structured-records.json); ST-D06/10/12 |
| `option_configuration` | `(R, opt_qe6_001, c)` | available; c = `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [stingray_ovs!740,741,742,743,744,745](stingray-structured-records.json); ST-D06/10/12 |
| `acquisition_configuration` | `(R, ex:standard-uqt, c)` | `acquisition_id=ex:standard-uqt`; one row for each `c` in `2lt_c07`, `3lt_c07`, `2lt_c67`, `3lt_c67` | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `option_presentation_override` | `(R, opt_uqt_002, 2lt_c07)` | selectable false; display-only | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `option_presentation_override` | `(R, opt_uqt_002, 3lt_c07)` | selectable false; display-only | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `option_presentation_override` | `(R, opt_uqt_002, 2lt_c67)` | selectable false; display-only | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `option_presentation_override` | `(R, opt_uqt_002, 3lt_c67)` | selectable false; display-only | [stingray_variant_overrides!2–5](stingray-structured-records.json); ST-P03; ST-D10/12 |
| `condition_clause` | `(R, ex:pcx, 1)` | any_present | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `condition_member` | `(R, ex:pcx, 1, 1)` | `option_id†=opt_pcx_001`; resolved_selection; other typed endpoints null | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `acquisition_configuration` | `(R, rule_opt_pcx_001_includes_opt_5dg_001, c)` | `acquisition_id=rule_opt_pcx_001_includes_opt_5dg_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate_configuration` | `(R, pr_pcx5dg_001, c)` | `rate_id=pr_pcx5dg_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [price_rules!11](stingray-structured-records.json); ST-D06/12 |
| `acquisition_configuration` | `(R, rule_opt_pcx_001_includes_opt_sfz_001, c)` | `acquisition_id=rule_opt_pcx_001_includes_opt_sfz_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate_configuration` | `(R, pr_pcxsfz_001, c)` | `rate_id=pr_pcxsfz_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [price_rules!12](stingray-structured-records.json); ST-D06/12 |
| `acquisition_configuration` | `(R, rule_opt_pcx_001_includes_opt_sht_001, c)` | `acquisition_id=rule_opt_pcx_001_includes_opt_sht_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate_configuration` | `(R, pr_pcxsht_001, c)` | `rate_id=pr_pcxsht_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [price_rules!13](stingray-structured-records.json); ST-D06/12 |
| `acquisition_configuration` | `(R, rule_opt_pcx_001_includes_opt_sng_001, c)` | `acquisition_id=rule_opt_pcx_001_includes_opt_sng_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `option_rate_configuration` | `(R, pr_pcxsng_001, c)` | `rate_id=pr_pcxsng_001`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [price_rules!14](stingray-structured-records.json); ST-D06/12 |
| `conflict_configuration` | `(R, ex:pcx-wheel, c)` | `conflict_id=ex:pcx-wheel`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `conflict_member` | `(R, ex:pcx-wheel, 1)` | `option_id†=opt_5do_001`; `interior_id†=null` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `replacement_plan_configuration` | `(R, ex:pcx-to-5do, c)` | `plan_id=ex:pcx-to-5do`; one row for each `c` in `1lt_c07`, `2lt_c07`, `3lt_c07`, `1lt_c67`, `2lt_c67`, `3lt_c67` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `replacement_action` | `(R, ex:pcx-to-5do, 1)` | remove `option_id†=opt_pcx_001` | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `replacement_action` | `(R, ex:pcx-to-5do, 2)` | add `option_id†=opt_5do_001`; `intent_effect=commit_purchase` (N2) | [rule_mapping!75–78](stingray-structured-records.json); ST-D06; common policy model_overrides.stingray |
| `emission_policy` | `(R, opt_uqt_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!69](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_pcx_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!74](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_5do_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!114](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_5dg_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!115](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_sfz_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!78](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_sht_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!216](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_sng_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!58](stingray-structured-records.json); ST-D06/10/12 |
| `emission_policy` | `(R, opt_qe6_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [stingray_options!240](stingray-structured-records.json); ST-D06/10/12 |

## GS populated relations

Authority: [GS handoff](grand-sport-structured.md), [owner overlay](grand-sport-owner-decisions.json), then [common compatibility policy](compatibility-notice-policy.json). Only the listed relationships are exemplified; unrelated full catalog rules still apply.

| Relation | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|---|
| `option` | `(M-GS, opt_dmx_001)` | `(R-GS, opt_dmx_001)`; `(R-GS, M-GS)` | RPO DMX; priced; default USD 1,295.00; `basis_id†=USD-options`; active target | [grandSport_options!61](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_d84_001)` | `(R-GS, opt_d84_001)`; `(R-GS, M-GS)` | RPO D84; priced; default USD 1,295.00; `basis_id†=USD-options`; active target | [grandSport_options!142](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_g26_001)` | `(R-GS, opt_g26_001)`; `(R-GS, M-GS)` | RPO G26; priced; default USD 995.00; `basis_id†=USD-options`; active target | [grandSport_options!122](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_g4z_001)` | `(R-GS, opt_g4z_001)`; `(R-GS, M-GS)` | RPO G4Z; priced; default USD 500.00; `basis_id†=USD-options`; active target | [grandSport_options!121](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_gbk_001)` | `(R-GS, opt_gbk_001)`; `(R-GS, M-GS)` | RPO GBK; priced; default USD 995.00; `basis_id†=USD-options`; active target | [grandSport_options!117](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_gkz_001)` | `(R-GS, opt_gkz_001)`; `(R-GS, M-GS)` | RPO GKZ; priced; default USD 0.00; `basis_id†=USD-options`; active target | [grandSport_options!123](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_gph_001)` | `(R-GS, opt_gph_001)`; `(R-GS, M-GS)` | RPO GPH; priced; default USD 995.00; `basis_id†=USD-options`; active target | [grandSport_options!120](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_z25_001)` | `(R-GS, opt_z25_001)`; `(R-GS, M-GS)` | RPO Z25; priced; default USD 1,995.00; `basis_id†=USD-options`; active target; auto/standard content, not an independent purchase in this sample | [grandSport_options!167](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_ae4_002)` | `(R-GS, opt_ae4_002)`; `(R-GS, M-GS)` | RPO AE4; priced; default USD 1,095.00; `basis_id†=USD-options`; active target | [grandSport_options!165](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_ah2_001)` | `(R-GS, opt_ah2_001)`; `(R-GS, M-GS)` | RPO AH2; priced; default USD 0.00; `basis_id†=USD-options`; active target | [grandSport_options!164](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_3f9_001)` | `(R-GS, opt_3f9_001)`; `(R-GS, M-GS)` | RPO 3F9; priced; default USD 595.00; `basis_id†=USD-options`; active target | [grandSport_options!161](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_97a_001)` | `(R-GS, opt_97a_001)`; `(R-GS, M-GS)` | RPO 97A; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [grandSport_options!67](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option` | `(M-GS, opt_z15_001)` | `(R-GS, opt_z15_001)`; `(R-GS, M-GS)` | RPO Z15; priced; default USD 995.00; `basis_id†=USD-options`; active target | [grandSport_options!203](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `condition` | `(M-GS, ex:always)` | `(R-GS, ex:always)`; `(R-GS, M-GS)` | always; no clauses | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition` | `(M-GS, ex:dmx-paints)` | `(R-GS, ex:dmx-paints)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `acquisition` | `(M-GS, ex:dmx-d84)` | `(R-GS, ex:dmx-d84)`; `(R-GS, M-GS)` | `condition_id†=ex:dmx-paints`; `target_option_id†=opt_d84_001`; dependency, locked, preserve_prior; priority 1 | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition` | `(M-GS, ex:d84)` | `(R-GS, ex:d84)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `requirement` | `(M-GS, ex:dmx-needs-d84)` | `(R-GS, ex:dmx-needs-d84)`; `(R-GS, M-GS)` | `source_option_id†=opt_dmx_001`; other source null; source resolved_selection; `activation_condition_id†=ex:dmx-paints`; `satisfaction_condition_id†=ex:d84`; dependency loss removes unsupported source with notice/revert | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `content_aspect` | `(M-GS, ex:roof-stripe)` | `(R-GS, ex:roof-stripe)`; `(R-GS, M-GS)` | roof stripe supplied content | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `content_effect` | `(M-GS, ex:omit-roof-stripe)` | `(R-GS, ex:omit-roof-stripe)`; `(R-GS, M-GS)` | `condition_id†=ex:d84`; `aspect_id†=ex:roof-stripe`; replacement; roof stripe omitted; precedence 1 | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition` | `(M-GS, ex:97a)` | `(R-GS, ex:97a)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `acquisition` | `(M-GS, ex:97a-z15)` | `(R-GS, ex:97a-z15)`; `(R-GS, M-GS)` | `condition_id†=ex:97a`; `target_option_id†=opt_z15_001`; dependency, locked, preserve_prior; priority 1 | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `condition` | `(M-GS, ex:z15)` | `(R-GS, ex:z15)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `requirement` | `(M-GS, ex:97a-needs-z15)` | `(R-GS, ex:97a-needs-z15)`; `(R-GS, M-GS)` | `source_option_id†=opt_97a_001`; other source null; source resolved_selection; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:z15`; dependency loss removes unsupported source with notice/revert | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `requirement` | `(M-GS, gs_rule_opt_dmx_001_requires_opt_z15_001)` | `(R-GS, gs_rule_opt_dmx_001_requires_opt_z15_001)`; `(R-GS, M-GS)` | `source_option_id†=opt_dmx_001`; other source null; source resolved_selection; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:z15`; dependency loss removes unsupported source with notice/revert | [grandSport_rule_mapping!75](grand-sport-structured-records.json); GS-D03/04 |
| `interior` | `(M-GS, 3LT_AE4_EL9)` | `(R-GS, 3LT_AE4_EL9)`; `(R-GS, M-GS)` | EL9; `seat_option_id†=opt_ae4_002`; enabled; no stored total | [lt_interiors!47](grand-sport-structured-records.json); GS-D05 |
| `condition` | `(M-GS, ex:3LT_AE4_EL9)` | `(R-GS, ex:3LT_AE4_EL9)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition` | `(M-GS, gs_rule_3lt_ae4_el9_includes_opt_z25_001)` | `(R-GS, gs_rule_3lt_ae4_el9_includes_opt_z25_001)`; `(R-GS, M-GS)` | `condition_id†=ex:3LT_AE4_EL9`; `target_option_id†=opt_z25_001`; included, locked, preserve_prior; priority 1 | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition` | `(M-GS, gs_sb_include_3lt_ae4_el9_3f9)` | `(R-GS, gs_sb_include_3lt_ae4_el9_3f9)`; `(R-GS, M-GS)` | `condition_id†=ex:3LT_AE4_EL9`; `target_option_id†=opt_3f9_001`; included, locked, preserve_prior; priority 1 | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition` | `(M-GS, ex:z25-AE4)` | `(R-GS, ex:z25-AE4)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `requirement` | `(M-GS, ex:el9-needs-z25-AE4)` | `(R-GS, ex:el9-needs-z25-AE4)`; `(R-GS, M-GS)` | `source_interior_id†=3LT_AE4_EL9`; other source null; source chosen; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:z25-AE4`; dependency loss removes unsupported source with notice/revert | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `option_rate` | `(M-GS, ex:el9-belt-AE4)` | `(R-GS, ex:el9-belt-AE4)`; `(R-GS, M-GS)` | `condition_id†=ex:3LT_AE4_EL9`; `target_option_id†=opt_3f9_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `interior` | `(M-GS, 3LT_AH2_EL9)` | `(R-GS, 3LT_AH2_EL9)`; `(R-GS, M-GS)` | EL9; `seat_option_id†=opt_ah2_001`; enabled; no stored total | [lt_interiors!80](grand-sport-structured-records.json); GS-D05 |
| `condition` | `(M-GS, ex:3LT_AH2_EL9)` | `(R-GS, ex:3LT_AH2_EL9)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition` | `(M-GS, gs_rule_3lt_ah2_el9_includes_opt_z25_001)` | `(R-GS, gs_rule_3lt_ah2_el9_includes_opt_z25_001)`; `(R-GS, M-GS)` | `condition_id†=ex:3LT_AH2_EL9`; `target_option_id†=opt_z25_001`; included, locked, preserve_prior; priority 1 | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition` | `(M-GS, gs_sb_include_3lt_ah2_el9_3f9)` | `(R-GS, gs_sb_include_3lt_ah2_el9_3f9)`; `(R-GS, M-GS)` | `condition_id†=ex:3LT_AH2_EL9`; `target_option_id†=opt_3f9_001`; included, locked, preserve_prior; priority 1 | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition` | `(M-GS, ex:z25-AH2)` | `(R-GS, ex:z25-AH2)`; `(R-GS, M-GS)` | conjunction; clauses ANDed | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `requirement` | `(M-GS, ex:el9-needs-z25-AH2)` | `(R-GS, ex:el9-needs-z25-AH2)`; `(R-GS, M-GS)` | `source_interior_id†=3LT_AH2_EL9`; other source null; source chosen; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:z25-AH2`; dependency loss removes unsupported source with notice/revert | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `option_rate` | `(M-GS, ex:el9-belt-AH2)` | `(R-GS, ex:el9-belt-AH2)`; `(R-GS, M-GS)` | `condition_id†=ex:3LT_AH2_EL9`; `target_option_id†=opt_3f9_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 2 | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `option_rate` | `(M-GS, ex:ae4-3lt)` | `(R-GS, ex:ae4-3lt)`; `(R-GS, M-GS)` | `condition_id†=ex:always`; `target_option_id†=opt_ae4_002`; replacement USD 595.00; `basis_id†=USD-options`; priority 1 | [lt_interiors!47](grand-sport-structured-records.json); GS-P02; GS-D05 |

Revision-only associations (R = `R-GS`):

| Relation | Full primary key | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|
| `option_configuration` | `(R, opt_dmx_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!332,333,334,335,336,337](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_d84_001, c)` | available; c = `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!305,306,307](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_d84_001, c)` | unavailable; c = `1lt_e07`, `2lt_e07`, `3lt_e07` | [grandSport_ovs!302,303,304](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_g26_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!536,537,538,539,540,541](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_g4z_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!542,543,544,545,546,547](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_gbk_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!560,561,562,563,564,565](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_gkz_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!578,579,580,581,582,583](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_gph_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!584,585,586,587,588,589](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_z25_001, c)` | available; c = `3lt_e07`, `3lt_e67` | [grandSport_ovs!1240,1243](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_z25_001, c)` | unavailable; c = `1lt_e07`, `2lt_e07`, `1lt_e67`, `2lt_e67` | [grandSport_ovs!1238,1239,1241,1242](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_ae4_002, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!110,111,112,113,114,115](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_ah2_001, c)` | standard; c = `3lt_e07`, `3lt_e67` | [grandSport_ovs!118,121](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_ah2_001, c)` | available; c = `2lt_e07`, `2lt_e67` | [grandSport_ovs!117,120](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_ah2_001, c)` | unavailable; c = `1lt_e07`, `1lt_e67` | [grandSport_ovs!116,119](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_3f9_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!32,33,34,35,36,37](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_97a_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!92,93,94,95,96,97](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `option_configuration` | `(R, opt_z15_001, c)` | available; c = `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_ovs!1232,1233,1234,1235,1236,1237](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `condition_clause` | `(R, ex:dmx-paints, 1)` | any_present | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:dmx-paints, 1, 1)` | `option_id†=opt_dmx_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_clause` | `(R, ex:dmx-paints, 2)` | any_present | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:dmx-paints, 2, 1)` | `option_id†=opt_g26_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:dmx-paints, 2, 2)` | `option_id†=opt_g4z_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:dmx-paints, 2, 3)` | `option_id†=opt_gbk_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:dmx-paints, 2, 4)` | `option_id†=opt_gkz_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:dmx-paints, 2, 5)` | `option_id†=opt_gph_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `acquisition_configuration` | `(R, ex:dmx-d84, c)` | `acquisition_id=ex:dmx-d84`; one row for each `c` in `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_clause` | `(R, ex:d84, 1)` | any_present | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_member` | `(R, ex:d84, 1, 1)` | `option_id†=opt_d84_001`; resolved_selection; other typed endpoints null | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `requirement_configuration` | `(R, ex:dmx-needs-d84, c)` | `requirement_id=ex:dmx-needs-d84`; one row for each `c` in `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `content_effect_configuration` | `(R, ex:omit-roof-stripe, c)` | `effect_id=ex:omit-roof-stripe`; one row for each `c` in `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_options!61,142](grand-sport-structured-records.json); GS-R04; GS-D04 |
| `condition_clause` | `(R, ex:97a, 1)` | any_present | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `condition_member` | `(R, ex:97a, 1, 1)` | `option_id†=opt_97a_001`; resolved_selection; other typed endpoints null | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `acquisition_configuration` | `(R, ex:97a-z15, c)` | `acquisition_id=ex:97a-z15`; one row for each `c` in `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `condition_clause` | `(R, ex:z15, 1)` | any_present | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `condition_member` | `(R, ex:z15, 1, 1)` | `option_id†=opt_z15_001`; resolved_selection; other typed endpoints null | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `requirement_configuration` | `(R, ex:97a-needs-z15, c)` | `requirement_id=ex:97a-needs-z15`; one row for each `c` in `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_options!67,203](grand-sport-structured-records.json); GS-D03/04 |
| `requirement_configuration` | `(R, gs_rule_opt_dmx_001_requires_opt_z15_001, c)` | `requirement_id=gs_rule_opt_dmx_001_requires_opt_z15_001`; one row for each `c` in `1lt_e07`, `2lt_e07`, `3lt_e07`, `1lt_e67`, `2lt_e67`, `3lt_e67` | [grandSport_rule_mapping!75](grand-sport-structured-records.json); GS-D03/04 |
| `interior_configuration` | `(R, 3LT_AE4_EL9, 3lt_e07)` | eligible | [lt_interiors!47](grand-sport-structured-records.json); GS-D05 |
| `interior_configuration` | `(R, 3LT_AE4_EL9, 3lt_e67)` | eligible | [lt_interiors!47](grand-sport-structured-records.json); GS-D05 |
| `condition_clause` | `(R, ex:3LT_AE4_EL9, 1)` | any_present | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition_member` | `(R, ex:3LT_AE4_EL9, 1, 1)` | `interior_id†=3LT_AE4_EL9`; chosen; other typed endpoints null | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition_configuration` | `(R, gs_rule_3lt_ae4_el9_includes_opt_z25_001, c)` | `acquisition_id=gs_rule_3lt_ae4_el9_includes_opt_z25_001`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition_configuration` | `(R, gs_sb_include_3lt_ae4_el9_3f9, c)` | `acquisition_id=gs_sb_include_3lt_ae4_el9_3f9`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition_clause` | `(R, ex:z25-AE4, 1)` | any_present | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition_member` | `(R, ex:z25-AE4, 1, 1)` | `option_id†=opt_z25_001`; resolved_selection; other typed endpoints null | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `requirement_configuration` | `(R, ex:el9-needs-z25-AE4, c)` | `requirement_id=ex:el9-needs-z25-AE4`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `option_rate_configuration` | `(R, ex:el9-belt-AE4, c)` | `rate_id=ex:el9-belt-AE4`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `interior_configuration` | `(R, 3LT_AH2_EL9, 3lt_e07)` | eligible | [lt_interiors!80](grand-sport-structured-records.json); GS-D05 |
| `interior_configuration` | `(R, 3LT_AH2_EL9, 3lt_e67)` | eligible | [lt_interiors!80](grand-sport-structured-records.json); GS-D05 |
| `condition_clause` | `(R, ex:3LT_AH2_EL9, 1)` | any_present | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition_member` | `(R, ex:3LT_AH2_EL9, 1, 1)` | `interior_id†=3LT_AH2_EL9`; chosen; other typed endpoints null | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition_configuration` | `(R, gs_rule_3lt_ah2_el9_includes_opt_z25_001, c)` | `acquisition_id=gs_rule_3lt_ah2_el9_includes_opt_z25_001`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `acquisition_configuration` | `(R, gs_sb_include_3lt_ah2_el9_3f9, c)` | `acquisition_id=gs_sb_include_3lt_ah2_el9_3f9`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition_clause` | `(R, ex:z25-AH2, 1)` | any_present | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `condition_member` | `(R, ex:z25-AH2, 1, 1)` | `option_id†=opt_z25_001`; resolved_selection; other typed endpoints null | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `requirement_configuration` | `(R, ex:el9-needs-z25-AH2, c)` | `requirement_id=ex:el9-needs-z25-AH2`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `option_rate_configuration` | `(R, ex:el9-belt-AH2, c)` | `rate_id=ex:el9-belt-AH2`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47,80](grand-sport-structured-records.json); GS-D05 |
| `option_rate_configuration` | `(R, ex:ae4-3lt, c)` | `rate_id=ex:ae4-3lt`; one row for each `c` in `3lt_e07`, `3lt_e67` | [lt_interiors!47](grand-sport-structured-records.json); GS-P02; GS-D05 |
| `emission_policy` | `(R, opt_dmx_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!61](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_d84_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!142](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_g26_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!122](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_g4z_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!121](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_gbk_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!117](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_gkz_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!123](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_gph_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!120](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_z25_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!167](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_ae4_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!165](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_ah2_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!164](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_3f9_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!161](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_97a_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!67](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |
| `emission_policy` | `(R, opt_z15_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grandSport_options!203](grand-sport-structured-records.json); GS-D03/04/05/14/15/16 |

## GSX populated relations

Authority: [GSX handoff](grand-sport-x-structured.md), [owner overlay](grand-sport-x-owner-decisions.json), then [common compatibility policy](compatibility-notice-policy.json). Only the listed relationships are exemplified; unrelated full catalog rules still apply.

| Relation | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|---|
| `option` | `(M-GSX, opt_fed_001)` | `(R-GSX, opt_fed_001)`; `(R-GSX, M-GSX)` | RPO FED; priced; default USD 500.00; `basis_id†=USD-options`; active target | [grand_sport_x_options!129](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_j57_001)` | `(R-GSX, opt_j57_001)`; `(R-GSX, M-GSX)` | RPO J57; priced; default USD 0.00; `basis_id†=USD-options`; active target | [grand_sport_x_options!125](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_b4z_001)` | `(R-GSX, opt_b4z_001)`; `(R-GSX, M-GSX)` | RPO B4Z; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [grand_sport_x_options!177](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_fe5_001)` | `(R-GSX, opt_fe5_001)`; `(R-GSX, M-GSX)` | RPO FE5; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [grand_sport_x_options!159](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_xft_001)` | `(R-GSX, opt_xft_001)`; `(R-GSX, M-GSX)` | RPO XFT; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [grand_sport_x_options!178](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_xfr_001)` | `(R-GSX, opt_xfr_001)`; `(R-GSX, M-GSX)` | RPO XFR; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [grand_sport_x_options!73](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_ls6_001)` | `(R-GSX, opt_ls6_001)`; `(R-GSX, M-GSX)` | RPO LS6; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [grand_sport_x_options!171](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_zz3_001)` | `(R-GSX, opt_zz3_001)`; `(R-GSX, M-GSX)` | RPO ZZ3; priced; default USD 1,195.00; `basis_id†=USD-options`; active target | [grand_sport_x_options!44](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_bc7_001)` | `(R-GSX, opt_bc7_001)`; `(R-GSX, M-GSX)` | RPO BC7; priced; default USD 0.00; `basis_id†=USD-options`; active target | [grand_sport_x_options!47](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_sl9_001)` | `(R-GSX, opt_sl9_001)`; `(R-GSX, M-GSX)` | RPO SL9; priced; default USD 125.00; `basis_id†=USD-options`; active target | [grand_sport_x_options!46](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option` | `(M-GSX, opt_d3v_001)` | `(R-GSX, opt_d3v_001)`; `(R-GSX, M-GSX)` | RPO D3V; priced; default USD 195.00; `basis_id†=USD-options`; active target | [grand_sport_x_options!45](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `condition` | `(M-GSX, ex:always)` | `(R-GSX, ex:always)`; `(R-GSX, M-GSX)` | always; no clauses | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `condition` | `(M-GSX, ex:fed)` | `(R-GSX, ex:fed)`; `(R-GSX, M-GSX)` | conjunction; clauses ANDed | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `acquisition` | `(M-GSX, grand_sport_x_rule_fed_includes_xfr_21b9e0e9fa01)` | `(R-GSX, grand_sport_x_rule_fed_includes_xfr_21b9e0e9fa01)`; `(R-GSX, M-GSX)` | `condition_id†=ex:fed`; `target_option_id†=opt_xfr_001`; included, locked, preserve_prior; priority 1 | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `equipment_substitution` | `(M-GSX, ex:fed-tires)` | `(R-GSX, ex:fed-tires)`; `(R-GSX, M-GSX)` | `condition_id†=ex:fed`; `removed_option_id†=opt_xft_001`; `replacement_option_id†=opt_xfr_001`; installed output only | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `acquisition` | `(M-GSX, ex:standard-J57)` | `(R-GSX, ex:standard-J57)`; `(R-GSX, M-GSX)` | `condition_id†=ex:always`; `target_option_id†=opt_j57_001`; standard, locked, preserve_prior; priority 1 | [grand_sport_x_options!125](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition` | `(M-GSX, ex:standard-B4Z)` | `(R-GSX, ex:standard-B4Z)`; `(R-GSX, M-GSX)` | `condition_id†=ex:always`; `target_option_id†=opt_b4z_001`; standard, locked, preserve_prior; priority 1 | [grand_sport_x_options!177](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition` | `(M-GSX, ex:standard-FE5)` | `(R-GSX, ex:standard-FE5)`; `(R-GSX, M-GSX)` | `condition_id†=ex:always`; `target_option_id†=opt_fe5_001`; standard, locked, preserve_prior; priority 1 | [grand_sport_x_options!159](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition` | `(M-GSX, ex:standard-XFT)` | `(R-GSX, ex:standard-XFT)`; `(R-GSX, M-GSX)` | `condition_id†=ex:always`; `target_option_id†=opt_xft_001`; standard, locked, preserve_prior; priority 1 | [grand_sport_x_options!178](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition` | `(M-GSX, ex:standard-LS6)` | `(R-GSX, ex:standard-LS6)`; `(R-GSX, M-GSX)` | `condition_id†=ex:always`; `target_option_id†=opt_ls6_001`; standard, locked, preserve_prior; priority 1 | [grand_sport_x_options!171](grand-sport-x-structured-records.json); GSX-D11/14 |
| `condition` | `(M-GSX, ex:zz3)` | `(R-GSX, ex:zz3)`; `(R-GSX, M-GSX)` | conjunction; clauses ANDed | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `acquisition` | `(M-GSX, grand_sport_x_rule_zz3_includes_bc7_cee5698ba347)` | `(R-GSX, grand_sport_x_rule_zz3_includes_bc7_cee5698ba347)`; `(R-GSX, M-GSX)` | `condition_id†=ex:zz3`; `target_option_id†=opt_bc7_001`; included, locked, preserve_prior; priority 1 | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `acquisition` | `(M-GSX, grand_sport_x_rule_zz3_includes_sl9_92d15a5d1074)` | `(R-GSX, grand_sport_x_rule_zz3_includes_sl9_92d15a5d1074)`; `(R-GSX, M-GSX)` | `condition_id†=ex:zz3`; `target_option_id†=opt_sl9_001`; included, locked, preserve_prior; priority 1 | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `option_rate` | `(M-GSX, grand_sport_x_pr_zz3_sl9_ce51294f94f9)` | `(R-GSX, grand_sport_x_pr_zz3_sl9_ce51294f94f9)`; `(R-GSX, M-GSX)` | `condition_id†=ex:zz3`; `target_option_id†=opt_sl9_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [grand_sport_x_price_rules!26](grand-sport-x-structured-records.json); GSX-D14 |

Revision-only associations (R = `R-GSX`):

| Relation | Full primary key | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|
| `option_configuration` | `(R, opt_fed_001, c)` | available; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!518,519,520,521,522,523](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_j57_001, c)` | standard; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!608,609,610,611,612,613](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_b4z_001, c)` | standard; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!176,177,178,179,180,181](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_fe5_001, c)` | standard; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!512,513,514,515,516,517](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_xft_001, c)` | standard; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!1250,1251,1252,1253,1254,1255](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_xfr_001, c)` | available; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!1244,1245,1246,1247,1248,1249](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_ls6_001, c)` | standard; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!674,675,676,677,678,679](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_zz3_001, c)` | available; c = `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_ovs!1275,1277,1279](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_zz3_001, c)` | unavailable; c = `1lt_g07`, `2lt_g07`, `3lt_g07` | [grand_sport_x_ovs!1274,1276,1278](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_bc7_001, c)` | standard; c = `1lt_g07`, `2lt_g07`, `3lt_g07` | [grand_sport_x_ovs!200,202,204](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_bc7_001, c)` | available; c = `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_ovs!201,203,205](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_sl9_001, c)` | available; c = `1lt_g07`, `1lt_g67`, `2lt_g07`, `2lt_g67`, `3lt_g07`, `3lt_g67` | [grand_sport_x_ovs!908,909,910,911,912,913](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_d3v_001, c)` | available; c = `1lt_g07`, `2lt_g07`, `3lt_g07` | [grand_sport_x_ovs!296,298,300](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_configuration` | `(R, opt_d3v_001, c)` | unavailable; c = `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_ovs!297,299,301](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `condition_clause` | `(R, ex:fed, 1)` | any_present | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `condition_member` | `(R, ex:fed, 1, 1)` | `option_id†=opt_fed_001`; resolved_selection; other typed endpoints null | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `acquisition_configuration` | `(R, grand_sport_x_rule_fed_includes_xfr_21b9e0e9fa01, c)` | `acquisition_id=grand_sport_x_rule_fed_includes_xfr_21b9e0e9fa01`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `equipment_substitution_configuration` | `(R, ex:fed-tires, c)` | `substitution_id=ex:fed-tires`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_rule_mapping!49](grand-sport-x-structured-records.json); GSX-R11; GSX-D11/12 |
| `acquisition_configuration` | `(R, ex:standard-J57, c)` | `acquisition_id=ex:standard-J57`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_options!125](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition_configuration` | `(R, ex:standard-B4Z, c)` | `acquisition_id=ex:standard-B4Z`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_options!177](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition_configuration` | `(R, ex:standard-FE5, c)` | `acquisition_id=ex:standard-FE5`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_options!159](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition_configuration` | `(R, ex:standard-XFT, c)` | `acquisition_id=ex:standard-XFT`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_options!178](grand-sport-x-structured-records.json); GSX-D11/14 |
| `acquisition_configuration` | `(R, ex:standard-LS6, c)` | `acquisition_id=ex:standard-LS6`; one row for each `c` in `1lt_g07`, `2lt_g07`, `3lt_g07`, `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_options!171](grand-sport-x-structured-records.json); GSX-D11/14 |
| `condition_clause` | `(R, ex:zz3, 1)` | any_present | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `condition_member` | `(R, ex:zz3, 1, 1)` | `option_id†=opt_zz3_001`; resolved_selection; other typed endpoints null | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `acquisition_configuration` | `(R, grand_sport_x_rule_zz3_includes_bc7_cee5698ba347, c)` | `acquisition_id=grand_sport_x_rule_zz3_includes_bc7_cee5698ba347`; one row for each `c` in `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `acquisition_configuration` | `(R, grand_sport_x_rule_zz3_includes_sl9_92d15a5d1074, c)` | `acquisition_id=grand_sport_x_rule_zz3_includes_sl9_92d15a5d1074`; one row for each `c` in `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_rule_mapping!81,83](grand-sport-x-structured-records.json); GSX-D14 |
| `source_disposition` | `(R, A:GSX:grand_sport_x_rule_mapping:51, grand_sport_x_rule_ls6_includes_d3v_c7bc4b3df65b)` | retire executable relationship `opt_ls6_001` → `opt_d3v_001`; preserve source; zero active acquisition/translation targets | [grand_sport_x_rule_mapping!51](grand-sport-x-structured-records.json); GSX-D14 |
| `source_disposition` | `(R, A:GSX:grand_sport_x_rule_mapping:82, grand_sport_x_rule_zz3_includes_ls6_b15b51ebf396)` | retire executable relationship `opt_zz3_001` → `opt_ls6_001`; preserve source; zero active acquisition/translation targets | [grand_sport_x_rule_mapping!82](grand-sport-x-structured-records.json); GSX-D14 |
| `emission_policy` | `(R, opt_fed_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!129](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_j57_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!125](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_b4z_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!177](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_fe5_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!159](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_xft_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!178](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_xfr_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!73](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_ls6_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!171](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_zz3_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!44](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_bc7_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!47](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_sl9_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!46](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `emission_policy` | `(R, opt_d3v_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [grand_sport_x_options!45](grand-sport-x-structured-records.json); GSX-D10/11/12/14 |
| `option_rate_configuration` | `(R, grand_sport_x_pr_zz3_sl9_ce51294f94f9, c)` | `rate_id=grand_sport_x_pr_zz3_sl9_ce51294f94f9`; one row for each `c` in `1lt_g67`, `2lt_g67`, `3lt_g67` | [grand_sport_x_price_rules!26](grand-sport-x-structured-records.json); GSX-D14 |

## Z06 populated relations

Authority: [Z06 handoff](z06-structured.md), [owner overlay](z06-owner-decisions.json), then [common compatibility policy](compatibility-notice-policy.json). Only the listed relationships are exemplified; unrelated full catalog rules still apply.

| Relation | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|---|
| `option` | `(M-Z06, opt_pdb_001)` | `(R-Z06, opt_pdb_001)`; `(R-Z06, M-Z06)` | RPO PDB; priced; default USD 16,000.00; `basis_id†=USD-options`; active target | [z06_options!242](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_pdd_001)` | `(R-Z06, opt_pdd_001)`; `(R-Z06, M-Z06)` | RPO PDD; priced; default USD 25,495.00; `basis_id†=USD-options`; active target | [z06_options!243](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_z07_001)` | `(R-Z06, opt_z07_001)`; `(R-Z06, M-Z06)` | RPO Z07; priced; default USD 9,500.00; `basis_id†=USD-options`; active target | [z06_options!131](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_j57_001)` | `(R-Z06, opt_j57_001)`; `(R-Z06, M-Z06)` | RPO J57; priced; default USD 9,000.00; `basis_id†=USD-options`; active target | [z06_options!125](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_t0f_001)` | `(R-Z06, opt_t0f_001)`; `(R-Z06, M-Z06)` | RPO T0F; priced; default USD 8,995.00; `basis_id†=USD-options`; active target | [z06_options!122](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_t0g_001)` | `(R-Z06, opt_t0g_001)`; `(R-Z06, M-Z06)` | RPO T0G; priced; default USD 10,995.00; `basis_id†=USD-options`; active target | [z06_options!123](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_r8e_002)` | `(R-Z06, opt_r8e_002)`; `(R-Z06, M-Z06)` | RPO R8E; priced; default USD 2,600.00; `basis_id†=USD-options`; active target | [z06_options!60](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_j6d_001)` | `(R-Z06, opt_j6d_001)`; `(R-Z06, M-Z06)` | RPO J6D; priced; default USD 0.00; `basis_id†=USD-options`; active target | [z06_options!31](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_roy_001)` | `(R-Z06, opt_roy_001)`; `(R-Z06, M-Z06)` | RPO ROY; priced; default USD 11,995.00; `basis_id†=USD-options`; active target | [z06_options!239](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_roz_001)` | `(R-Z06, opt_roz_001)`; `(R-Z06, M-Z06)` | RPO ROZ; priced; default USD 13,995.00; `basis_id†=USD-options`; active target | [z06_options!240](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_stz_001)` | `(R-Z06, opt_stz_001)`; `(R-Z06, M-Z06)` | RPO STZ; priced; default USD 15,500.00; `basis_id†=USD-options`; active target | [z06_options!241](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_j56_001)` | `(R-Z06, opt_j56_001)`; `(R-Z06, M-Z06)` | RPO J56; priced; default USD 0.00; `basis_id†=USD-options`; active target | [z06_options!124](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_j6a_001)` | `(R-Z06, opt_j6a_001)`; `(R-Z06, M-Z06)` | RPO J6A; priced; default USD 0.00; `basis_id†=USD-options`; active target | [z06_options!29](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_soe_002)` | `(R-Z06, opt_soe_002)`; `(R-Z06, M-Z06)` | RPO SOE; priced; default USD 0.00; `basis_id†=USD-options`; active target | [z06_options!233](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_t0e_001)` | `(R-Z06, opt_t0e_001)`; `(R-Z06, M-Z06)` | RPO T0E; priced; default USD 0.00; `basis_id†=USD-options`; active target | [z06_options!121](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_cfz_001)` | `(R-Z06, opt_cfz_001)`; `(R-Z06, M-Z06)` | RPO CFZ; priced; default USD 3,495.00; `basis_id†=USD-options`; active target | [z06_options!128](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_fe6_002)` | `(R-Z06, opt_fe6_002)`; `(R-Z06, M-Z06)` | RPO FE6; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target | [z06_options!58](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_fe7_001)` | `(R-Z06, opt_fe7_001)`; `(R-Z06, M-Z06)` | RPO FE7; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target | [z06_options!59](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_xfr_001)` | `(R-Z06, opt_xfr_001)`; `(R-Z06, M-Z06)` | RPO XFR; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [z06_options!61](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_xfs_001)` | `(R-Z06, opt_xfs_001)`; `(R-Z06, M-Z06)` | RPO XFS; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [z06_options!65](z06-structured-records.json); Z06-D01/11/12 |
| `option` | `(M-Z06, opt_cbf_001)` | `(R-Z06, opt_cbf_001)`; `(R-Z06, M-Z06)` | RPO CBF; priced; default USD 495.00; `basis_id†=USD-options`; active target; auto/standard content, not an independent purchase in this sample | [z06_options!245](z06-structured-records.json); Z06-D01/11/12 |
| `condition` | `(M-Z06, ex:always)` | `(R-Z06, ex:always)`; `(R-Z06, M-Z06)` | always; no clauses | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:pdb)` | `(R-Z06, ex:pdb)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:pdd)` | `(R-Z06, ex:pdd)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:z07)` | `(R-Z06, ex:z07)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:t0f)` | `(R-Z06, ex:t0f)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:roy)` | `(R-Z06, ex:roy)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:roz)` | `(R-Z06, ex:roz)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:j57)` | `(R-Z06, ex:j57)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `choice_group` | `(M-Z06, z06_group_pdd_requires_carbon_wheel)` | `(R-Z06, z06_group_pdd_requires_carbon_wheel)`; `(R-Z06, M-Z06)` | optional occupancy min 0/max 1; replacement peer policy; PDD requirement enforces occupancy while active (N1 translation rationale below) | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition` | `(M-Z06, ex:carbon-wheel-occupied)` | `(R-Z06, ex:carbon-wheel-occupied)`; `(R-Z06, M-Z06)` | conjunction; clauses ANDed | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `requirement` | `(M-Z06, ex:pdd-needs-wheel)` | `(R-Z06, ex:pdd-needs-wheel)`; `(R-Z06, M-Z06)` | `source_option_id†=opt_pdd_001`; other source null; source resolved_selection; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:carbon-wheel-occupied`; dependency loss removes unsupported source with notice/revert | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdb_001_includes_opt_j57_001)` | `(R-Z06, z06_rule_opt_pdb_001_includes_opt_j57_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_j57_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!35](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdb_001_includes_opt_j6d_001)` | `(R-Z06, z06_rule_opt_pdb_001_includes_opt_j6d_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_j6d_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!36](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdb_001_includes_opt_roy_001)` | `(R-Z06, z06_rule_opt_pdb_001_includes_opt_roy_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_roy_001`; included, yield_to_explicit, preserve_prior; priority 1 | [z06_rule_mapping!51](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdd_001_includes_opt_z07_001)` | `(R-Z06, z06_rule_opt_pdd_001_includes_opt_z07_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_z07_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!37](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdd_001_includes_opt_t0f_001)` | `(R-Z06, z06_rule_opt_pdd_001_includes_opt_t0f_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_t0f_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!38](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdd_001_includes_opt_cfz_001)` | `(R-Z06, z06_rule_opt_pdd_001_includes_opt_cfz_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_cfz_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!39](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_pdd_001_includes_opt_roy_001)` | `(R-Z06, z06_rule_opt_pdd_001_includes_opt_roy_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_roy_001`; included, yield_to_explicit, preserve_prior; priority 1 | [z06_rule_mapping!52](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_z07_001_includes_opt_j57_001)` | `(R-Z06, z06_rule_opt_z07_001_includes_opt_j57_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:z07`; `target_option_id†=opt_j57_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!43](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_z07_001_includes_opt_fe7_001)` | `(R-Z06, z06_rule_opt_z07_001_includes_opt_fe7_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:z07`; `target_option_id†=opt_fe7_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!44](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, z06_rule_opt_z07_001_includes_opt_xfs_001)` | `(R-Z06, z06_rule_opt_z07_001_includes_opt_xfs_001)`; `(R-Z06, M-Z06)` | `condition_id†=ex:z07`; `target_option_id†=opt_xfs_001`; included, locked, preserve_prior; priority 1 | [z06_rule_mapping!45](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition` | `(M-Z06, ex:j57-j6d)` | `(R-Z06, ex:j57-j6d)`; `(R-Z06, M-Z06)` | `condition_id†=ex:j57`; `target_option_id†=opt_j6d_001`; default, yield_to_explicit, preserve_prior; priority 1 | [z06_rule_mapping!36](z06-structured-records.json); Z06-D01 corrects missing J57 default |
| `conflict` | `(M-Z06, ex:pdb-z07)` | `(R-Z06, ex:pdb-z07)`; `(R-Z06, M-Z06)` | `source_option_id†=opt_pdb_001`; `source_interior_id†=null`; `activation_condition_id†=ex:always` | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `replacement_plan` | `(M-Z06, ex:pdb-to-pdd)` | `(R-Z06, ex:pdb-to-pdd)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `requested_option_id=opt_z07_001` (O3); notice PDD switch; do not commit standalone Z07 intent | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `option_rate` | `(M-Z06, z06_pr_z07_j57_zero)` | `(R-Z06, z06_pr_z07_j57_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:z07`; `target_option_id†=opt_j57_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!6](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdb_j57_zero)` | `(R-Z06, z06_pr_pdb_j57_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_j57_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 2 | [z06_price_rules!7](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdb_j6d_zero)` | `(R-Z06, z06_pr_pdb_j6d_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_j6d_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!8](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdb_roy_zero)` | `(R-Z06, z06_pr_pdb_roy_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_roy_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!9](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdb_roz_zero)` | `(R-Z06, z06_pr_pdb_roz_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdb`; `target_option_id†=opt_roz_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!10](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdd_z07_zero)` | `(R-Z06, z06_pr_pdd_z07_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_z07_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!12](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdd_t0f_zero)` | `(R-Z06, z06_pr_pdd_t0f_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_t0f_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!14](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdd_roy_zero)` | `(R-Z06, z06_pr_pdd_roy_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_roy_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 2 | [z06_price_rules!16](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdd_roz_zero)` | `(R-Z06, z06_pr_pdd_roz_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_roz_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 2 | [z06_price_rules!17](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_roy_pdb_16000)` | `(R-Z06, z06_pr_roy_pdb_16000)`; `(R-Z06, M-Z06)` | `condition_id†=ex:roy`; `target_option_id†=opt_pdb_001`; replacement USD 16,000.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!26](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_roz_pdb_17000)` | `(R-Z06, z06_pr_roz_pdb_17000)`; `(R-Z06, M-Z06)` | `condition_id†=ex:roz`; `target_option_id†=opt_pdb_001`; replacement USD 17,000.00; `basis_id†=USD-options`; priority 2 | [z06_price_rules!27](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_roy_pdd_25495)` | `(R-Z06, z06_pr_roy_pdd_25495)`; `(R-Z06, M-Z06)` | `condition_id†=ex:roy`; `target_option_id†=opt_pdd_001`; replacement USD 25,495.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!29](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_roz_pdd_26495)` | `(R-Z06, z06_pr_roz_pdd_26495)`; `(R-Z06, M-Z06)` | `condition_id†=ex:roz`; `target_option_id†=opt_pdd_001`; replacement USD 26,495.00; `basis_id†=USD-options`; priority 2 | [z06_price_rules!30](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_t0f_r8e_tax_3000)` | `(R-Z06, z06_pr_t0f_r8e_tax_3000)`; `(R-Z06, M-Z06)` | `condition_id†=ex:t0f`; `target_option_id†=opt_r8e_002`; replacement USD 3,000.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!50](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_t0f_cfz_zero)` | `(R-Z06, z06_pr_t0f_cfz_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:t0f`; `target_option_id†=opt_cfz_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 1 | [z06_price_rules!4](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate` | `(M-Z06, z06_pr_pdd_cfz_zero)` | `(R-Z06, z06_pr_pdd_cfz_zero)`; `(R-Z06, M-Z06)` | `condition_id†=ex:pdd`; `target_option_id†=opt_cfz_001`; replacement USD 0.00; `basis_id†=USD-options`; priority 2 | [z06_price_rules!15](z06-structured-records.json); Z06-D01/11/12 |
| `equipment_substitution` | `(M-Z06, ex:J56-J57)` | `(R-Z06, ex:J56-J57)`; `(R-Z06, M-Z06)` | `condition_id†=ex:j57`; `removed_option_id†=opt_j56_001`; `replacement_option_id†=opt_j57_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution` | `(M-Z06, ex:J6A-J6D)` | `(R-Z06, ex:J6A-J6D)`; `(R-Z06, M-Z06)` | `condition_id†=ex:j57`; `removed_option_id†=opt_j6a_001`; `replacement_option_id†=opt_j6d_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution` | `(M-Z06, ex:SOE-ROY)` | `(R-Z06, ex:SOE-ROY)`; `(R-Z06, M-Z06)` | `condition_id†=ex:roy`; `removed_option_id†=opt_soe_002`; `replacement_option_id†=opt_roy_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution` | `(M-Z06, ex:SOE-ROZ)` | `(R-Z06, ex:SOE-ROZ)`; `(R-Z06, M-Z06)` | `condition_id†=ex:roz`; `removed_option_id†=opt_soe_002`; `replacement_option_id†=opt_roz_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution` | `(M-Z06, ex:T0E-T0F)` | `(R-Z06, ex:T0E-T0F)`; `(R-Z06, M-Z06)` | `condition_id†=ex:t0f`; `removed_option_id†=opt_t0e_001`; `replacement_option_id†=opt_t0f_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution` | `(M-Z06, ex:FE6-FE7)` | `(R-Z06, ex:FE6-FE7)`; `(R-Z06, M-Z06)` | `condition_id†=ex:z07`; `removed_option_id†=opt_fe6_002`; `replacement_option_id†=opt_fe7_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution` | `(M-Z06, ex:XFR-XFS)` | `(R-Z06, ex:XFR-XFS)`; `(R-Z06, M-Z06)` | `condition_id†=ex:z07`; `removed_option_id†=opt_xfr_001`; `replacement_option_id†=opt_xfs_001`; installed output only | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:standard-J56)` | `(R-Z06, ex:standard-J56)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_j56_001`; standard, yield_to_explicit, preserve_prior; priority 1 | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:standard-J6A)` | `(R-Z06, ex:standard-J6A)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_j6a_001`; standard, yield_to_explicit, preserve_prior; priority 1 | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:standard-SOE)` | `(R-Z06, ex:standard-SOE)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_soe_002`; standard, yield_to_explicit, preserve_prior; priority 1 | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:standard-T0E)` | `(R-Z06, ex:standard-T0E)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_t0e_001`; standard, yield_to_explicit, preserve_prior; priority 1 | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:standard-FE6)` | `(R-Z06, ex:standard-FE6)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_fe6_002`; standard, yield_to_explicit, preserve_prior; priority 1 | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:standard-XFR)` | `(R-Z06, ex:standard-XFR)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_xfr_001`; standard, yield_to_explicit, preserve_prior; priority 1 | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition` | `(M-Z06, ex:required-r8e)` | `(R-Z06, ex:required-r8e)`; `(R-Z06, M-Z06)` | `condition_id†=ex:always`; `target_option_id†=opt_r8e_002`; default, locked, preserve_prior; priority 1; required charge root, not standard-only | [initial R8E / foundation states](discovery/z06-runtime.json); Z06-D12 |

Revision-only associations (R = `R-Z06`):

| Relation | Full primary key | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|
| `option_configuration` | `(R, opt_pdb_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1304,1305,1306,1307,1308,1309](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_pdd_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1310,1311,1312,1313,1314,1315](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_z07_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!170,171,172,173,174,175](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_j57_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!260,261,262,263,264,265](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_t0f_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!302,303,304,305,306,307](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_t0g_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1406,1407,1408,1409,1410,1411](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_r8e_002, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1322,1323,1324,1325,1326,1327](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_j6d_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!200,201,202,203,204,205](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_roy_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!602,603,604,605,606,607](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_roz_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!692,693,694,695,696,697](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_stz_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!770,771,772,773,774,775](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_j56_001, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!116,117,118,119,120,121](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_j6a_001, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!122,123,124,125,126,127](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_soe_002, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1370,1371,1372,1373,1374,1375](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_t0e_001, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!152,153,154,155,156,157](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_cfz_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!476,477,478,479,480,481](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_fe6_002, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1256,1257,1258,1259,1260,1261](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_fe7_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1262,1263,1264,1265,1266,1267](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_xfr_001, c)` | standard; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!716,717,718,719,720,721](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_xfs_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!788,789,790,791,792,793](z06-structured-records.json); Z06-D01/11/12 |
| `option_configuration` | `(R, opt_cbf_001, c)` | available; c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_ovs!1460,1461,1462,1463,1464,1465](z06-structured-records.json); Z06-D01/11/12 |
| `condition_clause` | `(R, ex:pdb, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:pdb, 1, 1)` | `option_id†=opt_pdb_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:pdd, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:pdd, 1, 1)` | `option_id†=opt_pdd_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:z07, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:z07, 1, 1)` | `option_id†=opt_z07_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:t0f, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:t0f, 1, 1)` | `option_id†=opt_t0f_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:roy, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:roy, 1, 1)` | `option_id†=opt_roy_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:roz, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:roz, 1, 1)` | `option_id†=opt_roz_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:j57, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:j57, 1, 1)` | `option_id†=opt_j57_001`; resolved_selection; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `choice_group_configuration` | `(R, z06_group_pdd_requires_carbon_wheel, c)` | `group_id=z06_group_pdd_requires_carbon_wheel`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `choice_group_member` | `(R, z06_group_pdd_requires_carbon_wheel, opt_roy_001)` | explicit product member; independent of section | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `choice_group_member` | `(R, z06_group_pdd_requires_carbon_wheel, opt_roz_001)` | explicit product member; independent of section | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `choice_group_member` | `(R, z06_group_pdd_requires_carbon_wheel, opt_stz_001)` | explicit product member; independent of section | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_clause` | `(R, ex:carbon-wheel-occupied, 1)` | any_present | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `condition_member` | `(R, ex:carbon-wheel-occupied, 1, 1)` | `group_id†=z06_group_pdd_requires_carbon_wheel`; occupied; other typed endpoints null | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `requirement_configuration` | `(R, ex:pdd-needs-wheel, c)` | `requirement_id=ex:pdd-needs-wheel`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_groups!3–4](z06-structured-records.json); Z06-D01/11 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdb_001_includes_opt_j57_001, c)` | `acquisition_id=z06_rule_opt_pdb_001_includes_opt_j57_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdb_001_includes_opt_j6d_001, c)` | `acquisition_id=z06_rule_opt_pdb_001_includes_opt_j6d_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!36](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdb_001_includes_opt_roy_001, c)` | `acquisition_id=z06_rule_opt_pdb_001_includes_opt_roy_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!51](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdd_001_includes_opt_z07_001, c)` | `acquisition_id=z06_rule_opt_pdd_001_includes_opt_z07_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!37](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdd_001_includes_opt_t0f_001, c)` | `acquisition_id=z06_rule_opt_pdd_001_includes_opt_t0f_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!38](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdd_001_includes_opt_cfz_001, c)` | `acquisition_id=z06_rule_opt_pdd_001_includes_opt_cfz_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!39](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_pdd_001_includes_opt_roy_001, c)` | `acquisition_id=z06_rule_opt_pdd_001_includes_opt_roy_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!52](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_z07_001_includes_opt_j57_001, c)` | `acquisition_id=z06_rule_opt_z07_001_includes_opt_j57_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!43](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_z07_001_includes_opt_fe7_001, c)` | `acquisition_id=z06_rule_opt_z07_001_includes_opt_fe7_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!44](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, z06_rule_opt_z07_001_includes_opt_xfs_001, c)` | `acquisition_id=z06_rule_opt_z07_001_includes_opt_xfs_001`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!45](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, ex:j57-j6d, c)` | `acquisition_id=ex:j57-j6d`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!36](z06-structured-records.json); Z06-D01 corrects missing J57 default |
| `conflict_configuration` | `(R, ex:pdb-z07, c)` | `conflict_id=ex:pdb-z07`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `conflict_member` | `(R, ex:pdb-z07, 1)` | `option_id†=opt_z07_001`; `interior_id†=null` | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `replacement_plan_configuration` | `(R, ex:pdb-to-pdd, c)` | `plan_id=ex:pdb-to-pdd`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `replacement_action` | `(R, ex:pdb-to-pdd, 1)` | remove `option_id†=opt_pdb_001` | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `replacement_action` | `(R, ex:pdb-to-pdd, 2)` | add `option_id†=opt_pdd_001`; `intent_effect=commit_purchase` on PDD, consuming the Z07 request (N2) | [z06_options!242–243](z06-structured-records.json); Z06-D11; common policy model_overrides.z06 |
| `option_rate_configuration` | `(R, z06_pr_z07_j57_zero, c)` | `rate_id=z06_pr_z07_j57_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!6](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdb_j57_zero, c)` | `rate_id=z06_pr_pdb_j57_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!7](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdb_j6d_zero, c)` | `rate_id=z06_pr_pdb_j6d_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!8](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdb_roy_zero, c)` | `rate_id=z06_pr_pdb_roy_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!9](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdb_roz_zero, c)` | `rate_id=z06_pr_pdb_roz_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!10](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdd_z07_zero, c)` | `rate_id=z06_pr_pdd_z07_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!12](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdd_t0f_zero, c)` | `rate_id=z06_pr_pdd_t0f_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!14](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdd_roy_zero, c)` | `rate_id=z06_pr_pdd_roy_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!16](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdd_roz_zero, c)` | `rate_id=z06_pr_pdd_roz_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!17](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_roy_pdb_16000, c)` | `rate_id=z06_pr_roy_pdb_16000`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!26](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_roz_pdb_17000, c)` | `rate_id=z06_pr_roz_pdb_17000`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!27](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_roy_pdd_25495, c)` | `rate_id=z06_pr_roy_pdd_25495`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!29](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_roz_pdd_26495, c)` | `rate_id=z06_pr_roz_pdd_26495`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!30](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_t0f_r8e_tax_3000, c)` | `rate_id=z06_pr_t0f_r8e_tax_3000`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!50](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_t0f_cfz_zero, c)` | `rate_id=z06_pr_t0f_cfz_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!4](z06-structured-records.json); Z06-D01/11/12 |
| `option_rate_configuration` | `(R, z06_pr_pdd_cfz_zero, c)` | `rate_id=z06_pr_pdd_cfz_zero`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_price_rules!15](z06-structured-records.json); Z06-D01/11/12 |
| `equipment_substitution_configuration` | `(R, ex:J56-J57, c)` | `substitution_id=ex:J56-J57`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution_configuration` | `(R, ex:J6A-J6D, c)` | `substitution_id=ex:J6A-J6D`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution_configuration` | `(R, ex:SOE-ROY, c)` | `substitution_id=ex:SOE-ROY`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution_configuration` | `(R, ex:SOE-ROZ, c)` | `substitution_id=ex:SOE-ROZ`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution_configuration` | `(R, ex:T0E-T0F, c)` | `substitution_id=ex:T0E-T0F`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution_configuration` | `(R, ex:FE6-FE7, c)` | `substitution_id=ex:FE6-FE7`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `equipment_substitution_configuration` | `(R, ex:XFR-XFS, c)` | `substitution_id=ex:XFR-XFS`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [z06_rule_mapping!35–52](z06-structured-records.json); Z06-R02/04; Z06-D01 |
| `emission_policy` | `(R, opt_pdb_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!242](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_pdd_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!243](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_z07_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!131](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_j57_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!125](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_t0f_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!122](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_t0g_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!123](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_r8e_002)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!60](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_j6d_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!31](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_roy_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!239](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_roz_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!240](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_stz_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!241](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_j56_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!124](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_j6a_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!29](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_soe_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!233](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_t0e_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!121](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_cfz_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!128](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_fe6_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!58](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_fe7_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!59](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_xfr_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!61](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_xfs_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!65](z06-structured-records.json); Z06-D01/11/12 |
| `emission_policy` | `(R, opt_cbf_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [z06_options!245](z06-structured-records.json); Z06-D01/11/12 |
| `acquisition_configuration` | `(R, ex:standard-J56, c)` | `acquisition_id=ex:standard-J56`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition_configuration` | `(R, ex:standard-J6A, c)` | `acquisition_id=ex:standard-J6A`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition_configuration` | `(R, ex:standard-SOE, c)` | `acquisition_id=ex:standard-SOE`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition_configuration` | `(R, ex:standard-T0E, c)` | `acquisition_id=ex:standard-T0E`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition_configuration` | `(R, ex:standard-FE6, c)` | `acquisition_id=ex:standard-FE6`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition_configuration` | `(R, ex:standard-XFR, c)` | `acquisition_id=ex:standard-XFR`; one row for each `c` in `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [variant_master!20–25](z06-structured-records.json); Z06-R04; Z06-D01 |
| `acquisition_configuration` | `(R, ex:required-r8e, c)` | one row for c = `1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67` | [initial R8E / foundations](discovery/z06-runtime.json); Z06-D12 |

## ZR1 populated relations

Authority: [ZR1 handoff](zr1-structured.md), [owner overlay](zr1-owner-decisions.json), then [common compatibility policy](compatibility-notice-policy.json). Only the listed relationships are exemplified; unrelated full catalog rules still apply.

| Relation | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|---|
| `option` | `(M-ZR1, opt_ztk_001)` | `(R-ZR1, opt_ztk_001)`; `(R-ZR1, M-ZR1)` | RPO ZTK; priced; default USD 5,995.00; `basis_id†=USD-options`; active target | [zr1_options!114](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_tom_001)` | `(R-ZR1, opt_tom_001)`; `(R-ZR1, M-ZR1)` | RPO TOM; priced; default USD 12,995.00; `basis_id†=USD-options`; active target | [zr1_options!110](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_j58_002)` | `(R-ZR1, opt_j58_002)`; `(R-ZR1, M-ZR1)` | RPO J58; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1_options!111](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_j59_002)` | `(R-ZR1, opt_j59_002)`; `(R-ZR1, M-ZR1)` | RPO J59; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1_options!112](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_fe8_002)` | `(R-ZR1, opt_fe8_002)`; `(R-ZR1, M-ZR1)` | RPO FE8; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1_options!189](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_fej_001)` | `(R-ZR1, opt_fej_001)`; `(R-ZR1, M-ZR1)` | RPO FEJ; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1_options!190](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_xfr_001)` | `(R-ZR1, opt_xfr_001)`; `(R-ZR1, M-ZR1)` | RPO XFR; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [zr1_options!58](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_xfs_001)` | `(R-ZR1, opt_xfs_001)`; `(R-ZR1, M-ZR1)` | RPO XFS; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [zr1_options!59](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_t0e_001)` | `(R-ZR1, opt_t0e_001)`; `(R-ZR1, M-ZR1)` | RPO T0E; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1_options!109](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option` | `(M-ZR1, opt_r8e_002)` | `(R-ZR1, opt_r8e_002)`; `(R-ZR1, M-ZR1)` | RPO R8E; priced; default USD 3,000.00; `basis_id†=USD-options`; active target | [zr1_options!54](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition` | `(M-ZR1, ex:always)` | `(R-ZR1, ex:always)`; `(R-ZR1, M-ZR1)` | always; no clauses | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition` | `(M-ZR1, ex:ztk)` | `(R-ZR1, ex:ztk)`; `(R-ZR1, M-ZR1)` | conjunction; clauses ANDed | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, zr1_rule_ztk_includes_fej_e1474255bc72)` | `(R-ZR1, zr1_rule_ztk_includes_fej_e1474255bc72)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `target_option_id†=opt_fej_001`; included, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, zr1_rule_ztk_includes_xfs_14d43544e74a)` | `(R-ZR1, zr1_rule_ztk_includes_xfs_14d43544e74a)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `target_option_id†=opt_xfs_001`; included, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, zr1_rule_ztk_includes_tom_5b60f5523451)` | `(R-ZR1, zr1_rule_ztk_includes_tom_5b60f5523451)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `target_option_id†=opt_tom_001`; included, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, zr1_rule_ztk_includes_j59_c53c618e6bcb)` | `(R-ZR1, zr1_rule_ztk_includes_j59_c53c618e6bcb)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `target_option_id†=opt_j59_002`; included, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition` | `(M-ZR1, ex:tom)` | `(R-ZR1, ex:tom)`; `(R-ZR1, M-ZR1)` | conjunction; clauses ANDed | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `requirement` | `(M-ZR1, ex:ztk-needs-tom)` | `(R-ZR1, ex:ztk-needs-tom)`; `(R-ZR1, M-ZR1)` | `source_option_id†=opt_ztk_001`; other source null; source resolved_selection; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:tom`; dependency loss removes unsupported source with notice/revert | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, ex:standard-J58)` | `(R-ZR1, ex:standard-J58)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:always`; `target_option_id†=opt_j58_002`; standard, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, ex:standard-FE8)` | `(R-ZR1, ex:standard-FE8)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:always`; `target_option_id†=opt_fe8_002`; standard, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, ex:standard-XFR)` | `(R-ZR1, ex:standard-XFR)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:always`; `target_option_id†=opt_xfr_001`; standard, locked, preserve_prior; priority 1 | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1, ex:FE8-FEJ)` | `(R-ZR1, ex:FE8-FEJ)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `removed_option_id†=opt_fe8_002`; `replacement_option_id†=opt_fej_001`; installed output only | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1, ex:XFR-XFS)` | `(R-ZR1, ex:XFR-XFS)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `removed_option_id†=opt_xfr_001`; `replacement_option_id†=opt_xfs_001`; installed output only | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1, ex:J58-J59)` | `(R-ZR1, ex:J58-J59)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:ztk`; `removed_option_id†=opt_j58_002`; `replacement_option_id†=opt_j59_002`; installed output only | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1, ex:aero)` | `(R-ZR1, ex:aero)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:tom`; `removed_option_id†=opt_t0e_001`; `replacement_option_id†=opt_tom_001`; installed output only | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition` | `(M-ZR1, ex:required-r8e)` | `(R-ZR1, ex:required-r8e)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:always`; `target_option_id†=opt_r8e_002`; default, locked, preserve_prior; priority 1; required charge root, not standard-only | [initial R8E / foundation states](discovery/zr1-runtime.json); ZR1-D08 |
| `acquisition` | `(M-ZR1, ex:standard-T0E)` | `(R-ZR1, ex:standard-T0E)`; `(R-ZR1, M-ZR1)` | `condition_id†=ex:always`; `target_option_id†=opt_t0e_001`; standard, yield_to_explicit, preserve_prior; priority 1 | [initial T0E / foundations](discovery/zr1-runtime.json); ZR1-D09 |

Revision-only associations (R = `R-ZR1`):

| Relation | Full primary key | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|
| `option_configuration` | `(R, opt_ztk_001, c)` | available; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!102,103,104,105](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_tom_001, c)` | available; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!794,795,796,797](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_j58_002, c)` | standard; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!738,739,740,741](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_j59_002, c)` | available; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!742,743,744,745](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_fe8_002, c)` | standard; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!730,731,732,733](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_fej_001, c)` | available; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!734,735,736,737](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_xfr_001, c)` | standard; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!414,415,416,417](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_xfs_001, c)` | available; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!450,451,452,453](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_t0e_001, c)` | standard; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!90,91,92,93](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `option_configuration` | `(R, opt_r8e_002, c)` | standard; c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_ovs!766,767,768,769](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition_clause` | `(R, ex:ztk, 1)` | any_present | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition_member` | `(R, ex:ztk, 1, 1)` | `option_id†=opt_ztk_001`; resolved_selection; other typed endpoints null | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1_rule_ztk_includes_fej_e1474255bc72, c)` | `acquisition_id=zr1_rule_ztk_includes_fej_e1474255bc72`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1_rule_ztk_includes_xfs_14d43544e74a, c)` | `acquisition_id=zr1_rule_ztk_includes_xfs_14d43544e74a`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1_rule_ztk_includes_tom_5b60f5523451, c)` | `acquisition_id=zr1_rule_ztk_includes_tom_5b60f5523451`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1_rule_ztk_includes_j59_c53c618e6bcb, c)` | `acquisition_id=zr1_rule_ztk_includes_j59_c53c618e6bcb`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition_clause` | `(R, ex:tom, 1)` | any_present | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `condition_member` | `(R, ex:tom, 1, 1)` | `option_id†=opt_tom_001`; resolved_selection; other typed endpoints null | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `requirement_configuration` | `(R, ex:ztk-needs-tom, c)` | `requirement_id=ex:ztk-needs-tom`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-J58, c)` | `acquisition_id=ex:standard-J58`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-FE8, c)` | `acquisition_id=ex:standard-FE8`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-XFR, c)` | `acquisition_id=ex:standard-XFR`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:FE8-FEJ, c)` | `substitution_id=ex:FE8-FEJ`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:XFR-XFS, c)` | `substitution_id=ex:XFR-XFS`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:J58-J59, c)` | `substitution_id=ex:J58-J59`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:aero, c)` | `substitution_id=ex:aero`; one row for each `c` in `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [zr1_rule_mapping!39–45](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_ztk_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!114](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_tom_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!110](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_j58_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!111](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_j59_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!112](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_fe8_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!189](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_fej_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!190](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_xfr_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!58](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_xfs_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!59](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_t0e_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!109](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `emission_policy` | `(R, opt_r8e_002)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1_options!54](zr1-structured-records.json); ZR1-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:required-r8e, c)` | one row for c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [initial R8E / foundations](discovery/zr1-runtime.json); ZR1-D08 |
| `acquisition_configuration` | `(R, ex:standard-T0E, c)` | one row for c = `1lz_r07`, `3lz_r07`, `1lz_r67`, `3lz_r67` | [initial T0E / foundations](discovery/zr1-runtime.json); ZR1-D09 |

## ZR1X populated relations

Authority: [ZR1X handoff](zr1x-structured.md), [owner overlay](zr1x-owner-decisions.json), then [common compatibility policy](compatibility-notice-policy.json). Only the listed relationships are exemplified; unrelated full catalog rules still apply.

| Relation | Identity `(M, id)` | Version `(R, id)`; owner `(R, M)` | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|---|
| `option` | `(M-ZR1X, opt_ztk_001)` | `(R-ZR1X, opt_ztk_001)`; `(R-ZR1X, M-ZR1X)` | RPO ZTK; priced; default USD 1,500.00; `basis_id†=USD-options`; active target | [zr1x_options!109](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_tom_002)` | `(R-ZR1X, opt_tom_002)`; `(R-ZR1X, M-ZR1X)` | RPO TOM; priced; default USD 12,995.00; `basis_id†=USD-options`; active target | [zr1x_options!108](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_j59_002)` | `(R-ZR1X, opt_j59_002)`; `(R-ZR1X, M-ZR1X)` | RPO J59; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1x_options!169](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_feh_002)` | `(R-ZR1X, opt_feh_002)`; `(R-ZR1X, M-ZR1X)` | RPO FEH; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1x_options!188](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_fez_001)` | `(R-ZR1X, opt_fez_001)`; `(R-ZR1X, M-ZR1X)` | RPO FEZ; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1x_options!189](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_xfr_001)` | `(R-ZR1X, opt_xfr_001)`; `(R-ZR1X, M-ZR1X)` | RPO XFR; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [zr1x_options!58](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_xfs_001)` | `(R-ZR1X, opt_xfs_001)`; `(R-ZR1X, M-ZR1X)` | RPO XFS; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [zr1x_options!59](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_cfc_002)` | `(R-ZR1X, opt_cfc_002)`; `(R-ZR1X, M-ZR1X)` | RPO CFC; no_separate_charge in these evidenced equipment/hash roles; frozen amount null (not converted to a priced zero); active target; auto/standard content, not an independent purchase in this sample | [zr1x_options!165](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_gba_001)` | `(R-ZR1X, opt_gba_001)`; `(R-ZR1X, M-ZR1X)` | RPO GBA; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1x_options!96](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_g8g_001)` | `(R-ZR1X, opt_g8g_001)`; `(R-ZR1X, M-ZR1X)` | RPO G8G; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1x_options!95](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_t0e_001)` | `(R-ZR1X, opt_t0e_001)`; `(R-ZR1X, M-ZR1X)` | RPO T0E; priced; default USD 0.00; `basis_id†=USD-options`; active target | [zr1x_options!107](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option` | `(M-ZR1X, opt_r8e_002)` | `(R-ZR1X, opt_r8e_002)`; `(R-ZR1X, M-ZR1X)` | RPO R8E; priced; default USD 2,600.00; `basis_id†=USD-options`; active target | [zr1x_options!54](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition` | `(M-ZR1X, ex:always)` | `(R-ZR1X, ex:always)`; `(R-ZR1X, M-ZR1X)` | always; no clauses | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition` | `(M-ZR1X, ex:ztk)` | `(R-ZR1X, ex:ztk)`; `(R-ZR1X, M-ZR1X)` | conjunction; clauses ANDed | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, zr1x_rule_ztk_includes_fez_12881b414e44)` | `(R-ZR1X, zr1x_rule_ztk_includes_fez_12881b414e44)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:ztk`; `target_option_id†=opt_fez_001`; included, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, zr1x_rule_ztk_includes_xfs_14d43544e74a)` | `(R-ZR1X, zr1x_rule_ztk_includes_xfs_14d43544e74a)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:ztk`; `target_option_id†=opt_xfs_001`; included, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, zr1x_rule_ztk_includes_tom_5b60f5523451)` | `(R-ZR1X, zr1x_rule_ztk_includes_tom_5b60f5523451)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:ztk`; `target_option_id†=opt_tom_002`; included, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition` | `(M-ZR1X, ex:tom)` | `(R-ZR1X, ex:tom)`; `(R-ZR1X, M-ZR1X)` | conjunction; clauses ANDed | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `requirement` | `(M-ZR1X, ex:ztk-needs-tom)` | `(R-ZR1X, ex:ztk-needs-tom)`; `(R-ZR1X, M-ZR1X)` | `source_option_id†=opt_ztk_001`; other source null; source resolved_selection; `activation_condition_id†=ex:always`; `satisfaction_condition_id†=ex:tom`; dependency loss removes unsupported source with notice/revert | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, ex:standard-J59)` | `(R-ZR1X, ex:standard-J59)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:always`; `target_option_id†=opt_j59_002`; standard, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, ex:standard-FEH)` | `(R-ZR1X, ex:standard-FEH)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:always`; `target_option_id†=opt_feh_002`; standard, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, ex:standard-XFR)` | `(R-ZR1X, ex:standard-XFR)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:always`; `target_option_id†=opt_xfr_001`; standard, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1X, ex:FEH-FEZ)` | `(R-ZR1X, ex:FEH-FEZ)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:ztk`; `removed_option_id†=opt_feh_002`; `replacement_option_id†=opt_fez_001`; installed output only | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1X, ex:XFR-XFS)` | `(R-ZR1X, ex:XFR-XFS)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:ztk`; `removed_option_id†=opt_xfr_001`; `replacement_option_id†=opt_xfs_001`; installed output only | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `equipment_substitution` | `(M-ZR1X, ex:aero)` | `(R-ZR1X, ex:aero)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:tom`; `removed_option_id†=opt_t0e_001`; `replacement_option_id†=opt_tom_002`; installed output only | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition` | `(M-ZR1X, ex:standard-cfc)` | `(R-ZR1X, ex:standard-cfc)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:always`; `target_option_id†=opt_cfc_002`; standard, locked, preserve_prior; priority 1 | [zr1x_rule_mapping!5](zr1x-structured-records.json); ZR1X-D01/09 |
| `acquisition` | `(M-ZR1X, ex:required-r8e)` | `(R-ZR1X, ex:required-r8e)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:always`; `target_option_id†=opt_r8e_002`; default, locked, preserve_prior; priority 1; required charge root, not standard-only | [initial R8E / foundation states](discovery/zr1x-runtime.json); ZR1X-D08 |
| `acquisition` | `(M-ZR1X, ex:standard-T0E)` | `(R-ZR1X, ex:standard-T0E)`; `(R-ZR1X, M-ZR1X)` | `condition_id†=ex:always`; `target_option_id†=opt_t0e_001`; standard, yield_to_explicit, preserve_prior; priority 1 | [initial T0E / foundations](discovery/zr1x-runtime.json); ZR1X-D09 |

Revision-only associations (R = `R-ZR1X`):

| Relation | Full primary key | Logical facts / diagram FK aliases | Evidence and decision |
|---|---|---|---|
| `option_configuration` | `(R, opt_ztk_001, c)` | available; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!102,103,104,105](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_tom_002, c)` | available; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!790,791,792,793](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_j59_002, c)` | standard; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!738,739,740,741](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_feh_002, c)` | standard; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!726,727,728,729](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_fez_001, c)` | available; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!730,731,732,733](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_xfr_001, c)` | standard; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!414,415,416,417](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_xfs_001, c)` | available; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!450,451,452,453](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_cfc_002, c)` | standard; c = `1lz_s67`, `3lz_s67` | [zr1x_ovs!708,709](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_cfc_002, c)` | unavailable; c = `1lz_s07`, `3lz_s07` | [zr1x_ovs!706,707](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_gba_001, c)` | available; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!138,139,140,141](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_g8g_001, c)` | available; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!66,67,68,69](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_t0e_001, c)` | standard; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!90,91,92,93](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `option_configuration` | `(R, opt_r8e_002, c)` | standard; c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_ovs!762,763,764,765](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition_clause` | `(R, ex:ztk, 1)` | any_present | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition_member` | `(R, ex:ztk, 1, 1)` | `option_id†=opt_ztk_001`; resolved_selection; other typed endpoints null | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1x_rule_ztk_includes_fez_12881b414e44, c)` | `acquisition_id=zr1x_rule_ztk_includes_fez_12881b414e44`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1x_rule_ztk_includes_xfs_14d43544e74a, c)` | `acquisition_id=zr1x_rule_ztk_includes_xfs_14d43544e74a`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, zr1x_rule_ztk_includes_tom_5b60f5523451, c)` | `acquisition_id=zr1x_rule_ztk_includes_tom_5b60f5523451`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition_clause` | `(R, ex:tom, 1)` | any_present | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `condition_member` | `(R, ex:tom, 1, 1)` | `option_id†=opt_tom_002`; resolved_selection; other typed endpoints null | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `requirement_configuration` | `(R, ex:ztk-needs-tom, c)` | `requirement_id=ex:ztk-needs-tom`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-J59, c)` | `acquisition_id=ex:standard-J59`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-FEH, c)` | `acquisition_id=ex:standard-FEH`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-XFR, c)` | `acquisition_id=ex:standard-XFR`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:FEH-FEZ, c)` | `substitution_id=ex:FEH-FEZ`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:XFR-XFS, c)` | `substitution_id=ex:XFR-XFS`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `equipment_substitution_configuration` | `(R, ex:aero, c)` | `substitution_id=ex:aero`; one row for each `c` in `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!38–43](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:standard-cfc, c)` | `acquisition_id=ex:standard-cfc`; one row for each `c` in `1lz_s67`, `3lz_s67` | [zr1x_rule_mapping!5](zr1x-structured-records.json); ZR1X-D01/09 |
| `source_disposition` | `(R, A:ZR1X:zr1x_rule_mapping:5, zr1x_rule_cfc_includes_gba_dd934a80de02)` | retire executable relationship `opt_cfc_002` → `opt_gba_001`; preserve source; zero active acquisition/translation targets | [zr1x_rule_mapping!5](zr1x-structured-records.json); ZR1X-D01 |
| `emission_policy` | `(R, opt_ztk_001)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!109](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_tom_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!108](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_j59_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!169](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_feh_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!188](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_fez_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!189](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_xfr_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!58](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_xfs_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!59](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_cfc_002)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!165](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_gba_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!96](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_g8g_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!95](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_t0e_001)` | code role: RPO when installed_equipment; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!107](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `emission_policy` | `(R, opt_r8e_002)` | code role: RPO when resolved_selection; summary destination/order populated during presentation translation under O3/N3; no standard-only price implication | [zr1x_options!54](zr1x-structured-records.json); ZR1X-D01/06/08/09 |
| `acquisition_configuration` | `(R, ex:required-r8e, c)` | one row for c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [initial R8E / foundations](discovery/zr1x-runtime.json); ZR1X-D08 |
| `acquisition_configuration` | `(R, ex:standard-T0E, c)` | one row for c = `1lz_s07`, `3lz_s07`, `1lz_s67`, `3lz_s67` | [initial T0E / foundations](discovery/zr1x-runtime.json); ZR1X-D09 |

## Source disposition anchors

These global anchors complete the three disposition keys above. `document_id†`
uses the frozen workbook hash as an example handle, not a new document-ID policy.
The one `source_document` row has `document_id† =
3127e663b1531e366ce86b989b6190914108d40dfd15a33a258307a05d608e3c`, the same content
hash, evidenced by each linked records file's `sources.workbook_sha256`; decisions
GSX-D14 and ZR1X-D01 require preservation of these originals.

| source_anchor `anchor_id†` | `document_id†` | Locator and evidence | Decision |
|---|---|---|---|
| `A:GSX:grand_sport_x_rule_mapping:51` | workbook hash above | [grand_sport_x_rule_mapping row 51](grand-sport-x-structured-records.json) | GSX-D14 |
| `A:GSX:grand_sport_x_rule_mapping:82` | workbook hash above | [grand_sport_x_rule_mapping row 82](grand-sport-x-structured-records.json) | GSX-D14 |
| `A:ZR1X:zr1x_rule_mapping:5` | workbook hash above | [zr1x_rule_mapping row 5](zr1x-structured-records.json) | ZR1X-D01 |

The disposition fragment is the exact retained source rule ID. There is no target
acquisition for those fragments and no tombstone rule that can execute. This is
retirement of relationships, **not retirement of LS6, ZZ3, CFC or GBA options**.
A concrete translation family is unnecessary for a retired fragment with zero
targets; any eventual linkage to replacement associations must use their complete
composite keys (O6).

## Worked traces

All steps are paper evaluation against the populated rows and retained handoff
context. A dollar amount here is either a full named context total or an expressly
identified contribution. A context missing paint/interior remains incomplete;
previewing its output does not authorize an order. Output lists show the affected
codes, not the entire unchanged build or an implemented export format.

A candidate transaction never changes committed state before confirmation. Cancel
keeps intent, causes, selected interior, charges and output unchanged. Revert after
commit restores the whole prior transaction state, not merely its dollar total.
Removal drops unsupported causes; independently owned items survive only if still
valid. These are the proposal's runtime contract, not new persistent relations.

### ST: UQT ownership and PCX replacement

Use `R-ST`, first `1lt_c07`. [ST-T02 / ST-P03](stingray-structured.md) and
`stingray_options!69`, `stingray_variant_overrides!2:5` establish:

| Step | Row evaluation / intent | USD reconciliation | Affected output |
|---|---|---:|---|
| Select UQT at 1LT | Available `opt_uqt_002`; independent intent; default purchase rate | 73,495 + 1,495 = **74,990** | Installed/order UQT, one paid line; not static 1LT standard equipment |
| Switch to `2lt_c07` | Context reset clears old intent; `ex:standard-uqt` supplies a standard-only cause; display override disallows purchase | **80,595**, no UQT charge | Static standard and installed UQT; no purchase line |
| Return to `1lt_c07` | Standard acquisition out of scope; earlier intent is not restored | **73,495** | UQT no longer selected/emitted |

The full 74,990 → 80,595 → 73,495 sequence matches ST-T02; subtraction of the
1LT purchase on reset is not an option-rate discount at 2LT.

For PCX, start `2lt_c07` with independent QE6. [ST-T14 and ST-O26](stingray-structured.md)
and [the retained PCX sequence](stingray-behavior.md) give the 86,285 checkpoint.
The later [common policy's ST override](compatibility-notice-policy.json)
supersedes ST-D06's historical blocked-card interaction while preserving its
prohibited combination and no-credit rule.

| Step | Rows / candidate transaction | USD reconciliation | Affected output |
|---|---|---:|---|
| Select PCX | Four source-ID acquisitions add 5DG/SFZ/SHT/SNG; their four named rates are zero; QE6 retains independent intent | 80,595 + 1,095 + 4,595 + 0 + 0 + 0 + 0 = **86,285** | QE6 remains factory wheel; PCX order code and four included codes; 5DG is a supplied second set, not a factory-wheel substitution |
| Request 5DO | `ex:pcx-wheel` forbids retaining PCX with 5DO; `ex:pcx-to-5do` previews removal of PCX and its package-only children, then the paid wheel | Candidate 80,595 + 1,095 + 4,395 = **86,085**; committed **86,285** | Notice lists removals and second-set replacement; does not invent a PCX credit |
| Cancel | Discard candidate | **86,285** | PCX, 5DG/SFZ/SHT/SNG unchanged |
| Confirm on retry | Remove PCX intent; unsupported four children disappear; independently request 5DO; keep QE6 | **86,085** | QE6 + 5DO; no PCX or its package-only codes |
| Revert | Restore previous committed state and ownership | **86,285** | PCX and its four children restored; 5DO absent |
| Remove PCX without replacement | Remove only its unsupported causes | 80,595 + 1,095 = **81,690** | QE6 remains; static trim information unchanged |

The frozen **90,680 = 86,285 + 4,395** coexistence result is rejected evidence,
not the target. The new 86,085 replacement total is derived from ST-D06 plus the
later common policy and the exact retained charge owners; ST-T14's accepted PCX
checkpoint remains 86,285. No blanket independent-child retention from GS/ZR1
is imported into ST's PCX acquisitions.

### GS: two-clause roof dependency and EL9 charge owner

Use `R-GS`, `2lt_e67`. The actual paint option IDs in clause 2 are
`opt_g26_001`, `opt_g4z_001`, `opt_gbk_001`, `opt_gkz_001`, `opt_gph_001`.
Clause 1 tests resolved `opt_dmx_001`; clause 2 is ANY of those five paints.
The clauses are ANDed; this is neither DMX-or-paint nor five simultaneous paints.
All acquisition, requirement and roof-content scopes explicitly contain the
three convertible configurations, with no coupe fallback.

[GS-T06 / GS-O38 / GS-D04](grand-sport-structured.md) provide the full context:

| Step | Rows / ownership | USD reconciliation | Affected output |
|---|---|---:|---|
| G26 and 97A chosen | 97A has no separate charge; its dependency acquires Z15 once | 102,595 + 995 + 995 = **104,585** | G26, 97A, Z15; no D84 yet |
| Select DMX | Both clauses true; `ex:dmx-d84` adds D84; requirement satisfaction checked after acquisition | 104,585 + 1,295 + 1,295 = **107,175** | DMX and D84 emitted; content effect discloses omitted roof stripe, not a new order code |
| Cancel a proposed removal of DMX | Committed causes unchanged | **107,175** | Same output |
| Commit DMX removal | Clause 1 false; dependency-only D84 loses last cause | 107,175 − 1,295 − 1,295 = **104,585** | DMX/D84 absent; G26/97A/Z15 remain |
| Revert | Restore DMX and its rooted D84 cause | **107,175** | Restore both codes and roof-stripe disclosure |
| Repeat with D84 bought independently first | Same resolved D84, two causes, one price; removing DMX leaves valid independent D84 | 107,175 − 1,295 = **105,880** | D84 remains with G26/97A/Z15; no DMX |

The accepted correction is **105,880 frozen + 1,295 missing D84 = 107,175**.
The numerically identical 105,880 in the last row is a different, explicitly named
build (D84 without DMX), not reuse of the defective frozen selection set. Removing
D84 while DMX and a listed paint remain cannot leave the source valid: disclose
cleanup/revert under GS-D04/16. Static trim information is not rewritten by the
stripe selection, and the body-color roof baseline is not proof of installed
Carbon Flash roof treatment.

Separately use `3lt_e07` and `3LT_AE4_EL9` (also eligible at `3lt_e67`). The
`interior` seat FK owns AE4 once, `gs_rule_3lt_ae4_el9_includes_opt_z25_001`
acquires Z25, and `gs_sb_include_3lt_ae4_el9_3f9` acquires locked 3F9. Z25 is
**1,995**, AE4's scoped rate **595**, and 3F9's EL9 rate **0**: contribution
**2,590** under [GS-P02 / GS-D05](grand-sport-structured.md). With no other paid
content this is **100,245 + 2,590 = 102,835**, before any separately selected
paint or other conditional charges. It is a subtotal context, not a completed
paint/interior order. Choosing the AH2 EL9 leaf instead gives **1,995 + 0 + 0 =
1,995**, or **102,240** on that base.

Cancel a proposed leaf clear leaves AE4/Z25/3F9 and the 2,590 contribution intact.
Confirm clear removes the leaf's seat and relationship causes; absent independent
valid intent, its contribution becomes zero, and the missing-interior state cannot
submit. Revert restores the leaf and 2,590. Installed/order output contains AE4,
Z25 and 3F9 for the AE4 leaf; EL9 is the interior code, not a separate priced option.
Static trim information stays static. No 1,400 interior residual, doubled seat,
orange belt or auto-selected replacement interior is introduced.

### GSX: FED tires and exact LS6 relationship retirement

Use `R-GSX`, `1lt_g07`. [GSX-P07 / GSX-T03 / GSX-T24](grand-sport-x-structured.md)
and the [foundation records](grand-sport-x-foundations-records.json),
`observed_sequences[0].states`, supply the exact **112,195 → 112,695 → 112,195**
round trip. FED is `opt_fed_001` at 500; the actual acquisition ID is
`grand_sport_x_rule_fed_includes_xfr_21b9e0e9fa01`.

| Step | Selection and pricing | Static versus installed / order |
|---|---|---|
| Initial | Standard J57/B4Z/FE5/LS6/XFT; no FED charge; **112,195** | Static XFT; installed XFT, J57/B4Z/FE5/LS6 |
| Add FED | One independent 500 charge, XFR inclusion has no separate charge; **112,195 + 500 = 112,695** | Static XFT remains informational; `ex:fed-tires` suppresses installed XFT and emits installed XFR; FED is an order/purchase code |
| Cancel proposed FED removal | **112,695**, causes unchanged | XFR and FED remain |
| Confirm removal | **112,195**; XFR loses its FED cause | XFT restored; J57/B4Z/FE5/LS6 stay; no FED/XFR code |
| Revert | **112,695**, restore FED cause | XFR returns; no GS brake-package requirement |

The distinct GSX-D14 test uses a convertible, e.g. `1lt_g67`. Before and after
ZZ3, LS6 is supplied by `ex:standard-LS6`. The retired row-82 edge
`grand_sport_x_rule_zz3_includes_ls6_b15b51ebf396` cannot create LS6 ownership,
and retired row 51 `grand_sport_x_rule_ls6_includes_d3v_c7bc4b3df65b` cannot
create a D3V charge or code. Retained row-81/83 acquisitions still give BC7/SL9;
the named ZZ3→SL9 zero rate prevents an extra 125 charge. Contribution is
**1,195 + 0 + 0 = 1,195**, not 1,195 + 125 + 195. Cancel leaves the prior state;
removing ZZ3 drops its BC7/SL9 causes and 1,195, while standard LS6 remains;
revert restores those causes. This is the accepted GSX-D14 ownership target,
not an executed correction. Valid coupe lighting relationships outside this
sample remain preserved evidence; neither disposition retires D3V itself.

### Z06: PDB request replacement, wheel rate and scoped group

Use `R-Z06`, `2lz_h07`. [Z06-T04–06 / Z06-P01–04](z06-structured.md) give the
base **130,295**, separate R8E **2,600**, PDB/ROY **16,000**, PDD/ROY **25,495**,
and PDD/ROZ **26,495**. The common policy selects the noticed PDD switch from
Z06-D11's earlier alternatives. The exact source rate
`z06_pr_roz_pdd_26495` targets **PDD**, not ROZ; ROZ itself uses
`z06_pr_pdd_roz_zero`. Priority resolves replacement rates; there is no additive
1,000 wheel charge after the 26,495 package amount.

| Step | Rules / transaction | USD reconciliation | Affected installed / order output |
|---|---|---:|---|
| PDB with default ROY | PDB acquisitions J57/J6D/ROY; zero child rates; R8E default | 130,295 + 16,000 + 2,600 = **148,895** | PDB, J57/J6D/ROY; no Z07; static J56/J6A/SOE remain informational |
| Request Z07 | `ex:pdb-z07` forbids coexistence; `ex:pdb-to-pdd` removes PDB and adds PDD in candidate | Preview **158,790**; committed **148,895** | Disclose PDD, Z07/T0F, suspension/tires and rate changes |
| Cancel | Discard candidate | **148,895** | Original PDB causes and output intact |
| Confirm on retry | PDD owns purchase; Z07 is included, not independently retained; Z07 supplies J57/FE7/XFS; repaired default fills J6D; PDD supplies T0F/CFZ/ROY | 130,295 + 25,495 + 3,000 = **158,790** | PDD/Z07/T0F/CFZ/J57/J6D/FE7/XFS/ROY; no PDB, installed J56/J6A/SOE/T0E/FE6/XFR suppressed |
| Choose ROZ | Explicit peer displaces ROY; group stays occupied; full PDD rate becomes 26,495 and ROZ line stays zero | 130,295 + 26,495 + 3,000 = **159,790** | ROZ replaces ROY; rest unchanged |
| Revert that wheel change | Restore prior wheel intent/causes | **158,790** | ROY restored |
| Remove PDD (ROY package-only run) | Unsupported Z07/aero/brake/wheel causes go; R8E returns to 2,600; eligible defaults restore | 130,295 + 2,600 = **132,895** | J56/J6A/SOE/T0E/FE6/XFR; no PDD/Z07/T0F or package-only wheel codes |

The rejected frozen coexistence is **167,790**, exactly **9,000 above 158,790**.
The accepted 159,790 ROZ checkpoint also matches Z06-T04. The missing J6D repair
changes output correctness, not these amounts. A prior independent wheel is a
separate validity case; the last row explicitly has no such independent cause.
The five derived CBF edges are retained source requirements outside this populated
subset; no generic transitive replacement permission is inferred (Open N3).

For the scoped condition, `ex:pdd-needs-wheel` references
`ex:carbon-wheel-occupied`, whose clause 1 has one group endpoint
`z06_group_pdd_requires_carbon_wheel`, state **occupied**. Its explicit members
are `opt_roy_001`, `opt_roz_001`, `opt_stz_001`. The populated scope rows expand to:

- Parent scope = {`1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67`}.
- Group scope = {`1lz_h07`, `2lz_h07`, `3lz_h07`, `1lz_h67`, `2lz_h67`, `3lz_h67`}.
- Parent scope ⊆ group scope, so the subset check passes on paper. In `2lz_h07`,
  ROY makes it occupied; ROZ replacement keeps it occupied; an empty candidate
  fails PDD's requirement until eligible default acquisition fills it.

Deleting only the group's `2lz_h67` membership would fail freeze even though this
coupe trace still passes. Conversely, a separately scoped parent limited to
`2lz_h07` also satisfies the constraint. Neither `none_present` nor `any_present`
is given an out-of-scope fallback. No source-varying member set is merged into
this group; the three inspected carbon-wheel members are the same in all six
configurations. This checks the [diagram's freeze-time subset rule](master-schema-diagram.md#group-scope-constraint-for-conditions),
not ordinary FK enforcement or a new runtime scope interpretation.

### ZR1: independent TOM survives ZTK

Use `R-ZR1`, `1lz_r07`, with the [ZR1-D06/D08 targets](zr1-owner-decisions.json)
and [handoff ZTK/TOM pricing](zr1-structured.md). The real TOM key is
`opt_tom_001`, unlike ZR1X's `opt_tom_002`. Base 197,195 plus R8E 3,000 gives
starting context **200,195**. Unspecified paint/interior remain missing.

| Step | Intent / charge reconciliation | USD total | Output |
|---|---|---:|---|
| Buy TOM independently | TOM 12,995, independent intent recorded first | **213,190** | TOM installed/order, one line |
| Add ZTK | `zr1_rule_ztk_includes_tom_5b60f5523451` preserves prior TOM intent and adds a second cause; TOM still charges once, not zero | 200,195 + 5,995 + 12,995 = **219,185** | ZTK/TOM, installed J59/FEJ/XFS; static J58/FE8/XFR retained as information |
| Cancel proposed ZTK removal | No committed change | **219,185** | Same causes/output |
| Confirm removal | Drop 5,995 and ZTK causes; valid prior TOM remains at 12,995 | **213,190** | TOM remains; J58/FE8/XFR restore; J59/FEJ/XFS package-only output goes |
| Revert | Restore ZTK and its causes without duplicating TOM intent | **219,185** | Installed ZTK equipment returns |
| Fresh ZTK-only control, then remove | No prior TOM intent; both charges and dependent causes disappear | **219,185 → 200,195** | Neither ZTK nor TOM remains; baseline equipment returns |

The accepted package contribution is **5,995 + 12,995 = 18,990**. Clicking a
locked included TOM does not manufacture independent intent. After independent
TOM survives, its own aero substitution still suppresses installed T0E; static
trim copy does not become an extra order code or a price. A displaced cover, if
present in a fuller trace, is not a package child and does not auto-restore.

### ZR1X: local rate and CFC disposition

Use `R-ZR1X`, `1lz_s07`, with [ZR1X-D06/D08/D09](zr1x-owner-decisions.json)
and the [ZR1X handoff](zr1x-structured.md). Base **227,395** plus local R8E
**2,600** gives **229,995**. Buy `opt_tom_002` first, then ZTK at **1,500**:

| Step | Intent / pricing | USD total | Static versus installed / order |
|---|---|---:|---|
| TOM first | Independent 12,995 | **242,990** | TOM installed/order |
| Add ZTK | Same TOM price owner plus local 1,500 | 229,995 + 12,995 + 1,500 = **244,490** | J59 stays standard/installed; FEZ/XFS replace installed FEH/XFR; ZTK/TOM emitted |
| Cancel removal | Preserve both causes and intent | **244,490** | Unchanged |
| Confirm ZTK removal | Preserve prior independent TOM; remove package-only suspension/tire causes | **242,990** | J59 stays; FEH/XFR restore, TOM remains |
| Revert | Restore ZTK cause, no duplicate TOM charge | **244,490** | FEZ/XFS return |
| Fresh ZTK-only control, then remove | No independent TOM survives | **244,490 → 229,995** | ZTK/TOM absent; J59/FEH/XFR installed |

This reconciles exactly to **1,500 + 12,995 = 14,495**, not ZR1's 18,990.
Static XFR is never sufficient to emit installed XFR alongside XFS. There is no
ZR1 J58→J59 brake change in this lane.

In convertible `1lz_s67`, retain nonblack `opt_g8g_001` paint and acquire standard
`opt_cfc_002` using `ex:standard-cfc`. The row-5 disposition has fragment
`zr1x_rule_cfc_includes_gba_dd934a80de02`; there is **no active acquisition** to
`opt_gba_001`. Therefore CFC neither selects GBA nor changes the customer's paint
or its charge. Cancel any unrelated candidate keeps that state; reset/revert
reapplies the same source-retirement rule, never revives the frozen edge.
CFC is standard/installed content without an independent purchase line; the
order paint remains G8G, not GBA. This is precisely ZR1X-D01's accepted qualitative
target, with **zero additional CFC/GBA charge**; no new accepted full-build total
is claimed for this formerly dormant path.

## Open

September 14 design resolution of O1–O8 and N1–N3. The specifications below
replace the earlier unchosen alternatives in this document and the diagram's
historical Open inventory. They are proposed design decisions for review, not
new owner business decisions, implemented constraints, or approval to build the
database. Existing example IDs remain readable fixtures. Naming a field does
not allocate its real records or turn this subset into a complete catalog.

| Item | Design disposition | Remaining execution evidence |
|---|---|---|
| O1 | Concrete typed identities and ownership names specified below. | DDL FK and predecessor tests. |
| O2 | Column naming, ID allocation and nullability conventions specified below. | Allocate actual global records and validate all mandatory links. |
| O3 | Request, hierarchy, context, visual and emission endpoints specified below. | Populate presentation destinations/order from each lane; check constraints. |
| O4 | Exact uniqueness scopes and precedence validation responsibilities specified below. | Full-catalog overlap checks and database rejection tests. |
| O5 | Installed-equipment state restricted to visual consumers. | Positive visual and negative nonvisual condition tests. |
| O6 | Typed translation expansion and consumer mapping contract specified below. | Complete source-to-target mapping and consumer inventory. |
| O7 | Acyclic global evidence and decision linkage specified below. | Populate evidence containers; test missing evidence rejection. |
| O8 | Freeze, completion and publication eligibility specified below. | Execute whole-revision and release validation. |
| N1 | Optional wheel group plus conditional PDD requirement retained. | Exercise all three wheels across all six Z06 configurations. |
| N2 | Replacement confirmation commits purchase intent on the accepted option. | Exercise confirm/cancel/revert and last-root removal. |
| N3 | Representative examples remain partial; full output has an explicit completion contract. | Translate the missing rows and verify complete outputs before release. |

### O1 and O2 — keys, identity and nullability

Use one concrete `<relation>_identity` table for each of the 18 relations in the
[identity membership table](master-schema-diagram.md#identity-membership).
This keeps ordinary typed FKs and avoids a shared kind-discriminator table.
A condition and acquisition with the same source ID remain distinct identities.
The physical database engine remains a separate implementation choice.

Use `model_year_id` for M and `revision_id` for R everywhere. Continuing identity
PKs are `(model_year_id, id)`; version PKs are `(revision_id, id)`, with both owner
FKs already specified by the diagram. Identity rows have nullable paired
`predecessor_model_year_id`/`predecessor_id` referencing their own concrete identity
table. Both are null or both set. A predecessor must belong to the same model in
an earlier year; it is a reviewed lineage link, never an automatic RPO match.
Revision parent uses `parent_revision_id`, nullable only for a first revision,
and must belong to the same model-year. Revision-only rows use `revision_id` and
the diagram's full association key; no extra continuing identity is introduced.
Every revision-only row has a direct revision FK or a mandatory parent FK that
already proves revision ownership; do not duplicate it merely for consistency.

Drop daggers from the named aliases (`basis_id`, `asset_id`, `document_id`,
`anchor_id`, `set_id`, `channel_key` and role-specific endpoint names).
`review_decision` uses `(decision_id, version)`; `decision_member` carries that
complete key. These are immutable record versions, not versions inferred from
a file timestamp. Evidence and decision sets are immutable membership sets:
changed membership gets a new `set_id`, not a mutable version column.

New target IDs are allocated once and retained in typed translation/mapping
records; they do not depend on row order, RPO, current price or mutable labels.
Existing source IDs may be retained within their concrete model-owned kind after
collision checking. New IDs use an opaque UUID string; a split source fact gets
one identity per distinct target meaning. Re-import reuses the stored mapping,
not a fresh UUID. Draft copies retain identities. New global IDs use the same
allocate-once rule; `USD-options`, `A:` and `ex:` remain paper aliases, not a claim
that those allocations have happened. Source-document hash is a unique content
attribute, not a requirement that its ID equal the hash.

Keys and FKs are non-null by default. Exceptions are nullable decision sets,
paired predecessors/first revision parent, unused XOR endpoints, an optional
replacement option, removal-action intent_effect, hierarchy roots, and a summary destination/order pair when
no summary output is emitted. A missing price in source evidence remains missing;
it never becomes a zero purchase amount. An active purchasable target must have
an evidenced price basis and complete applicable price before freeze.

### O3 and N2 — requests, transactions and presentation endpoints

`replacement_plan.requested_option_id` is a required same-revision option FK.
Plans here handle option selection requests; they do not generalize interior or
configuration reset into option replacements. Preconditions remain the separate
`condition_id`. Plan scope, exact request and precondition must all match.
More than one eligible plan for the same request is a validation error; source
row order never chooses the winner.

`replacement_action` retains `(revision_id, plan_id, position)` and its typed
option FK. Add actions carry `intent_effect=commit_purchase`; remove actions
carry no add intent effect. Included/dependent children are acquired by the
existing acquisition rules, not by duplicate add actions. This deliberately
limits replacement plans to explicit purchase transfers; no persistent purchase
intent table or catch-all action-origin enum is added to the catalog.

| Plan | Request FK | Confirmed root change | Derived children |
|---|---|---|---|
| ST `ex:pcx-to-5do` | `opt_5do_001` | Remove PCX ownership; commit independent 5DO ownership. | Remove unsupported PCX children under the existing absorbing policy. |
| Z06 `ex:pdb-to-pdd` | `opt_z07_001` | Remove PDB ownership; commit independent PDD ownership. Consume the request without committing independent Z07. | PDD acquires Z07/T0F and their children through rooted rules. |

The accepted addition receives the transaction's acquisition sequence; an already
valid independent purchase retains its original sequence. Reconciliation removes
obsolete causes, retains valid independent causes under each lane's policy, and
charges each option owner once. Cancel changes no root or sequence. Revert
restores the previous complete state. Removing PDD in the second example removes
package-only Z07; any genuinely pre-existing independent Z07 is handled by its
existing validity/retention rules, not fabricated by the replacement request.
These are refinements of the [transaction contract](master-schema-proposal.md#runtime-state-and-transaction-contract)
and common policy, with no change to the accepted example totals.

The remaining O3 endpoint allocations are:

- `interior_node.parent_node_id` is a nullable same-revision node FK; null is a
  root. Freeze validation rejects cycles and unreachable/invalid leaf mappings.
- `context_copy.axis` is `body` or `trim`; `value` must equal that axis on its
  referenced configuration. Check this cross-row constraint during validation;
  no new body/trim lookup hierarchy is needed.
- `visual_layer` owns scene FK, layer key and display order. `visual_binding`
  owns the full layer FK, asset FK, condition FK and precedence; its existing
  configuration junction owns scope. Binding precedence is separate from layer order.
- `emission_policy.summary_section_id` is a same-revision summary-section FK;
  `summary_order` is explicit. Both are required for summary-emitting rows and
  both null otherwise. Code emission and summary emission remain distinct roles.
  Populate destinations and ordering from each lane's retained presentation
  evidence; never route all example options to a newly invented common section.
  Equal display orders use stable option ID as a display tie-break only.

### O4 — uniqueness and competing rules

Ordinary unique keys: `model(model_key)`; `source_document(content_sha256)`;
`source_anchor(document_id, locator, fragment_key)` using preserved canonical
locator/fragment strings; `option_rate(revision_id, target_option_id, priority)`;
`visual_binding(revision_id, scene_id, layer_key, precedence)`.
The source anchor's fragment key may be the empty string for a whole locator,
never SQL null. This does not merge differing source documents or facts.

Typed duplicate checks use the parent plus populated endpoint: interior parts
use `(revision_id, interior_id, option_id)` or the component equivalent;
condition members use `(revision_id, condition_id, clause_id, endpoint, state)`
for each concrete endpoint kind; conflict members use `(revision_id, conflict_id,
endpoint)` for each kind. Enforce XOR first and unique non-null endpoints with
filtered indexes or equivalent constraints in the chosen engine. Endpoint state
is part of condition identity; different legitimate tests are not duplicates.

For acquisitions, validate unique priority per target **where scopes and
conditions overlap**. Retain all supported causes; priority cannot erase package
ownership. Contradictory peer/intent policies need an explicit evidenced resolution,
otherwise freeze fails. Content replacement effects require distinct precedence
per aspect where scopes/conditions overlap. Additive effects do not compete as
replacements. These cross-row predicates require semantic validation, not a claim
that an ordinary UNIQUE constraint proves overlap safety. Finite configuration
scopes and the typed condition language define the inputs to that validation.

Lower numeric priority wins, as in the existing examples. Source order is never
business precedence. PDB/Z07 zero J57 rates can retain their distinct sample
priorities because the accepted target forbids coexistence; zero amounts do not
excuse conflicting nonzero rules elsewhere. Full-catalog priority allocation must
preserve all evidenced winners and reject unexplained competing outcomes.

### O5 — installed state is a visual input

Allow `installed_equipment` in an option condition member only when every consumer
of that condition is a visual binding. Option intent/resolved-selection, interior
chosen and group occupied states keep their existing meanings. A condition shared
with a rule/rate/content consumer cannot contain an installed-equipment test;
create a separate typed condition if needed. Evaluate visual conditions after
root resolution and equipment substitution, so they cannot feed back into price
or selection. For example, ZR1 with ZTK shows XFS installed and XFR absent;
after removal without another supporting root, XFR returns. A missing asset
reports missing/fallback imagery without changing that state. No actual artwork
or rendering coverage is asserted by this design test.

### O6 and O7 — translation, consumer IDs and evidence

For every revision-owned authored target relation in the diagram, use a concrete
`<relation>_translation` when that relation is populated from source. Exclude
translation/mapping links themselves: do not recursively translate provenance.
Each link's PK is `(revision_id, anchor_id, fragment_key, <target PK without R>)`;
its two FKs reference the complete disposition and complete typed target keys.
This expansion includes identities' version rows, every scope junction, singleton
facts and associations. No scalar `target_id` substitutes for a composite key.
For example:

| Family | Full link PK; both FKs include revision_id |
|---|---|
| `acquisition_translation` | `(revision_id, anchor_id, fragment_key, acquisition_id)` |
| `acquisition_configuration_translation` | `(revision_id, anchor_id, fragment_key, acquisition_id, configuration_id)` |
| `condition_member_translation` | `(revision_id, anchor_id, fragment_key, condition_id, clause_id, member_id)` |
| `interaction_policy_translation` | `(revision_id, anchor_id, fragment_key)` |

This rule closes the family/key design without requiring unused tables in the
first implementation slice. A source split can link to several concrete families;
corroborating anchors can link to the same target. The three retired fragments
above keep zero executable translations. Continuing identity lineage is recorded
on its identity evidence, not by treating a revision disposition as a global FK.

Use `legacy_configuration_mapping`, `legacy_option_mapping` and
`legacy_interior_mapping` for those exported kinds. Other exported reference
kinds get their concrete `legacy_<relation>_mapping` only when consumer inventory
shows they are needed, including each exported rule family. Each has PK
`(revision_id, namespace, legacy_key)` and the target's complete same-revision FK.
Multiple aliases are separate mapping rows; they cannot ambiguously map one key
to two targets within the same kind/namespace. New consumer keys are allocated
once in that namespace and collision-checked. Release model aliases use
`release_model_alias(release_id, alias, model_id)`, PK `(release_id, alias)`, with
FK `(release_id, model_id)` to membership. It is a release association with no
continuing identity. No new runtime ID format or consumer interface is adopted
before that consumer's mapping is inspected and tested.

Every authored domain/version/association/identity row, including model and
model_year, has non-null
`evidence_set_id` and nullable `decision_set_id`. An identity's evidence records
its creation/lineage; version evidence records the changing facts. Price basis
and asset metadata also carry these links. `review_decision(decision_id, version)`
has a required evidence-set FK; it does not require a decision about itself.
Evidence sets contain one or more anchored source fragments. Decision sets contain
one or more immutable decision versions; absence of a governing decision uses a
null FK, not an empty set. Common-policy authority is a versioned decision member
alongside the lane decisions; its explicit override precedence remains intact.

Provenance terminates at immutable source documents/anchors. Those records own
source hash, locator and acquisition metadata; they do not require evidence about
themselves. Evidence/decision containers and their membership rows derive lineage
from their members, not self-referencing evidence sets. Revision/release metadata
records its pinned inputs and manifest; it is not a new product fact requiring
recursive source translation. Design-authored structure cites the reviewed design
revision plus the relevant source/owner decision. Do not label the September 14
design as an accepted owner decision until review actually accepts it.

### N1 — conditional factory-wheel requirement

Retain `z06_group_pdd_requires_carbon_wheel` as a model-owned optional 0/1 group
with ROY, ROZ and STZ and all six retained scopes. PDD activates the separate
occupied-group requirement. The source `requires_any` establishes that activated
requirement; the factory-wheel peer semantics establish maximum one. Outside PDD,
this requirement does not impose minimum one globally. Other applicable package
requirements continue to apply. Verify PDD with each member passes, PDD with none
fails, and any two members fail the peer constraint. Presentation sections do not
own this cardinality.

### N3 and O8 — full output and release completion

The representative examples do not become a release by resolving design choices.
The missing Z06 CBF relationships are explicitly these five frozen IDs in
[runtime_derived_relationships.records](z06-structured-records.json), each targeting
`opt_cbf_001`:

| Exact source fragment | Source option |
|---|---|
| `derived_opt_pdd_001_replaces_opt_cbf_001` | `opt_pdd_001` |
| `derived_opt_pdf_001_replaces_opt_cbf_001` | `opt_pdf_001` |
| `derived_opt_t0f_001_replaces_opt_cbf_001` | `opt_t0f_001` |
| `derived_opt_t0g_001_replaces_opt_cbf_001` | `opt_t0g_001` |
| `derived_opt_z07_001_replaces_opt_cbf_001` | `opt_z07_001` |

Translate each into an individually evidenced conflict under the common policy,
preserving effective configuration scope and any more specific accepted exception.
Selecting one of these sources against CBF removes incompatible CBF ownership
after confirmation; these are not equipment-substitution-only rows. Individual
source accounting does **not** require a separate replacement plan per fragment.
Use the O6 full-key links for each fragment's condition, conflict/member and scope,
and for the plans/actions implementing its request directions. Several fragments
may link to the same combined plan/action records; retain every contributing
anchor rather than duplicating executable behavior.

For a CBF request against an existing package build, allocate plans by the complete
disclosed removal transaction, not by each resolved incompatible endpoint. PDD
resolves PDD/Z07/T0F; PDF resolves PDF/Z07/T0G (retained
`z06_rule_mapping` rows 37–42). Their nested conflicts must participate in one
eligible plan for that request, not three. Where different removal sets need
separate plans, their preconditions must be mutually exclusive using explicit
intent `any_present`/`none_present` clauses and applicable scope. Include all
independently owned incompatible roots in that partition: merely testing PDD
intent does not exclude an additional retained Z07 or aero purchase. Remove the
roots needed to eliminate every conflicting cause, commit CBF once, and reconcile
unsupported children through the existing rooted rules. Never remove only a
locked child while retaining its incompatible parent.

Before freeze, check CBF requests against PDD and PDF, standalone Z07 with either
aero, standalone T0F/T0G, and valid retained-independent-root combinations in every
effective configuration. Require exactly one eligible complete plan when a
replacement is needed, no remaining incompatible cause after confirmation, and
unchanged prior ownership/charges on cancel or whole-state restoration on revert.
Check the reverse source requests against CBF as well. These are target-population
and validation obligations, not executed transition results. The pinned source-code
and frozen emitted anchors are both required; the table above identifies the
fragments but does not claim those target rows are populated. No general
inclusion-closure algorithm is authorized to invent further edges.

A full translated revision must account for every source disposition, complete
applicability matrix, defaults, rules and charge owners, interior requirements,
presentation destinations/order, code-emission classification and consumer keys.
Full outputs must be checked against independently evidenced expected builds,
including the unchanged portions omitted from these traces. Source discrepancies
remain accepted departures or explicit unresolved blockers. This is required
translation/verification work, not another open business decision.

`release.default_model_id` is nullable while drafting and mandatory for a completed
release; `(release_id, default_model_id)` references release membership. Release
aliases use the O6 association; artifact paths are unique on `(release_id, path)`.
A manifest pins immutable evaluator and format identifiers with content digests,
the exact compatibility decision/version, and every referenced asset ID/hash.
Store these pins as manifest data validated against the inputs/artifacts; no
mutable external version registry or redundant product FK is needed. A human
version label without immutable content identification is insufficient.

Freeze validates the whole revision's keys, typed endpoints, evidence, scopes,
prices, precedence, rooted rules and complete consumer mappings. Completion checks
all six model memberships, matching years, frozen revisions, default membership,
unique aliases/paths, generated artifacts and matching manifest/version/media pins.
Validate and commit each state transition against the same immutable snapshot;
concurrent draft edits invalidate the attempt. A publication pointer can reference
only a completed release and changes through compare-and-swap after generation
and validation succeed. FK existence alone never proves these predicates.

The remaining work is now explicit: populate the omitted translation/evidence/
presentation records, implement the constraints/evaluator, and execute full-output
and release checks in separately authorized slices. The design resolutions do not
claim those obligations passed or authorize implementation, publication or cutover.

## Validation boundary

Document review checks references, source IDs/locators, typed identity ownership,
finite scope expansion, sample priority uniqueness and arithmetic against retained
handoffs. The new design is checked for consistency with those examples and the
proposal; the five CBF IDs are compared with the frozen derived relationship list.
`python3 scripts/validate_handoffs.py` checks the unchanged input contract;
`git diff --check` checks the final documentation diff. No target evaluator,
physical FK enforcement, browser behavior, complete export or freeze/publication
transition is executed by these checks.
