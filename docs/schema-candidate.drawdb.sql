-- CorvetteCatalog: CURRENT DISPOSABLE CANDIDATE
-- Not the final authoring/release design; visualization only.
-- Generated from catalog.schema.create; do not edit or apply as a migration.
-- Refresh: python3 -m catalog.export_drawdb
-- Import into a new SQLite diagram in drawDB. See docs/drawdb.md.
-- CHECK constraints and triggers are comments because drawDB cannot model them.
-- Deferred FK timing is omitted; STRICT remains SQL-only diagram metadata.

CREATE TABLE import_metadata(
  key TEXT PRIMARY KEY NOT NULL,
  value TEXT NOT NULL
) STRICT;

CREATE TABLE source_sheet(
  name TEXT PRIMARY KEY NOT NULL,
  ordinal INTEGER NOT NULL,
  headers TEXT NOT NULL,
  row_count INTEGER NOT NULL
) STRICT;

CREATE TABLE entity(
  id TEXT PRIMARY KEY NOT NULL,
  kind TEXT NOT NULL,
  model_id TEXT NOT NULL,
  UNIQUE(id,model_id)
) STRICT;

CREATE TABLE code_evidence(
  path TEXT NOT NULL,
  revision TEXT NOT NULL,
  symbol TEXT NOT NULL,
  classification TEXT NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY(path,symbol)
) STRICT;

CREATE TABLE source_row(
  id TEXT PRIMARY KEY NOT NULL,
  sheet TEXT NOT NULL REFERENCES source_sheet(name),
  ordinal INTEGER NOT NULL,
  cells TEXT NOT NULL,
  UNIQUE(sheet,ordinal)
) STRICT;

CREATE TABLE legacy_mapping(
  namespace TEXT NOT NULL,
  model_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  legacy_id TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  PRIMARY KEY(namespace,model_id,kind,legacy_id),
  FOREIGN KEY(entity_id,model_id) REFERENCES entity(id,model_id)
) STRICT;

CREATE TABLE model (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  model_key TEXT NOT NULL,
  registry_key TEXT,
  label TEXT,
  year INTEGER,
  active INTEGER,
  expected_variant_count INTEGER,
  default_model INTEGER,
  UNIQUE(id,model_id),
  UNIQUE(model_key)
) STRICT;
-- CHECK (active IN (0,1))
-- CHECK (default_model IN (0,1))

CREATE TABLE section (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  section_key TEXT NOT NULL,
  name TEXT,
  selection_mode TEXT,
  is_required INTEGER,
  display_order INTEGER,
  standard_behavior TEXT,
  step_key TEXT,
  UNIQUE(id,model_id),
  UNIQUE(section_key)
) STRICT;
-- CHECK (is_required IN (0,1))

CREATE TABLE component_rate (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  component_type TEXT NOT NULL,
  code TEXT NOT NULL,
  trim_scope TEXT NOT NULL,
  amount TEXT,
  basis TEXT,
  currency TEXT,
  UNIQUE(id,model_id),
  UNIQUE(component_type,code,trim_scope)
) STRICT;
-- CHECK (amount IS NULL OR
--                     (amount NOT GLOB '*[^0-9.-]*' AND amount GLOB '*[0-9]*'
--                     AND instr(substr(amount,2),'-')=0
--                     AND length(amount)-length(replace(amount,'.',''))<=1))

CREATE TABLE evidence_link(
  source_id TEXT NOT NULL REFERENCES source_row(id),
  entity_id TEXT NOT NULL REFERENCES entity(id),
  PRIMARY KEY(source_id,entity_id)
) STRICT;

CREATE TABLE source_disposition(
  source_id TEXT NOT NULL REFERENCES source_row(id),
  model_key TEXT NOT NULL,
  disposition TEXT NOT NULL,
  reason TEXT NOT NULL,
  PRIMARY KEY(source_id,model_key,disposition)
) STRICT;

CREATE TABLE model_presentation (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  source_workbook TEXT,
  source_option_sheet TEXT,
  rule_mapping_sheet TEXT,
  price_rules_sheet TEXT,
  color_overrides_sheet TEXT,
  interior_source_sheet TEXT,
  dataset_name TEXT,
  export_slug TEXT,
  setup_card_subtitle TEXT,
  setup_eyebrow TEXT,
  setup_title TEXT,
  setup_description TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE model_fact (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  position INTEGER NOT NULL,
  text TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,position)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE publication (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  registry_key TEXT,
  promoted_to_runtime INTEGER,
  default_model INTEGER,
  artifact_path TEXT,
  artifact_type TEXT,
  legacy_alias TEXT,
  active INTEGER,
  display_order INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (promoted_to_runtime IN (0,1))
-- CHECK (default_model IN (0,1))
-- CHECK (active IN (0,1))

CREATE TABLE variant (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  legacy_id TEXT NOT NULL,
  trim_level TEXT,
  body_style TEXT,
  display_name TEXT,
  base_price TEXT,
  display_order INTEGER,
  active INTEGER,
  membership_order INTEGER,
  membership_active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (base_price IS NULL OR
--                     (base_price NOT GLOB '*[^0-9.-]*' AND base_price GLOB '*[0-9]*'
--                     AND instr(substr(base_price,2),'-')=0
--                     AND length(base_price)-length(replace(base_price,'.',''))<=1))
-- CHECK (active IN (0,1))
-- CHECK (membership_active IN (0,1))

CREATE TABLE hierarchy_node (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  parent_id TEXT,
  label TEXT,
  position INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(parent_id,model_id) REFERENCES hierarchy_node(id,model_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(parent_id,model_id) REFERENCES hierarchy_node(id,model_id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE direct_rule (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  source_note TEXT,
  legacy_id TEXT NOT NULL,
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  effect TEXT NOT NULL,
  runtime_action TEXT,
  explanation TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(source_id,model_id) REFERENCES entity(id,model_id),
  FOREIGN KEY(target_id,model_id) REFERENCES entity(id,model_id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(source_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(target_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (effect IN ('requires','includes','excludes') AND (runtime_action IS NULL OR runtime_action='replace'))

CREATE TABLE group_rule (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  notes TEXT,
  legacy_id TEXT NOT NULL,
  display_label TEXT,
  effect TEXT NOT NULL,
  source_id TEXT NOT NULL,
  explanation TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(source_id,model_id) REFERENCES entity(id,model_id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(source_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))
-- CHECK (effect IN ('requires_any','excludes_any'))

CREATE TABLE exclusive_group (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  notes TEXT,
  legacy_id TEXT NOT NULL,
  display_label TEXT,
  selection_mode TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))
-- CHECK (selection_mode IN ('at_most_one','exactly_one'))

CREATE TABLE scope_axis (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  all_token TEXT,
  owner_id TEXT NOT NULL,
  axis TEXT NOT NULL,
  mode TEXT NOT NULL,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(owner_id,model_id) REFERENCES entity(id,model_id),
  UNIQUE(owner_id,axis)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(owner_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (axis IN ('body','trim','variant') AND mode IN ('all','members'))

CREATE TABLE context_section (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  context_type TEXT NOT NULL,
  section_key TEXT,
  name TEXT,
  selection_mode TEXT,
  choice_mode TEXT,
  is_required INTEGER,
  standard_behavior TEXT,
  display_order INTEGER,
  step_key TEXT,
  step_label TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,context_type)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (is_required IN (0,1))
-- CHECK (active IN (0,1))

CREATE TABLE runtime_step (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  source TEXT,
  step_key TEXT NOT NULL,
  label TEXT,
  runtime_order INTEGER,
  active INTEGER,
  navigable INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,step_key)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))
-- CHECK (navigable IN (0,1))

CREATE TABLE context_copy (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  context_type TEXT NOT NULL,
  value TEXT NOT NULL,
  body_scope TEXT NOT NULL,
  info_tooltip TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,context_type,value,body_scope)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE context_choice (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  context_type TEXT NOT NULL,
  value TEXT NOT NULL,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,context_type,value)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE summary_section (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  notes TEXT,
  section_key TEXT NOT NULL,
  label TEXT,
  display_order INTEGER,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  UNIQUE(model_id,section_key)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE asset_assignment (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  target_id TEXT NOT NULL,
  source_scope TEXT NOT NULL,
  image_url TEXT,
  image_alt TEXT,
  image_fit TEXT,
  image_position TEXT,
  hover_image_url TEXT,
  hover_image_alt TEXT,
  hover_image_position TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(target_id,model_id) REFERENCES entity(id,model_id),
  UNIQUE(model_id,target_id,source_scope)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(target_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE option (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  legacy_id TEXT NOT NULL,
  rpo TEXT,
  rpo_role TEXT,
  name TEXT,
  description TEXT,
  base_price TEXT,
  price_basis TEXT,
  currency TEXT,
  section_id TEXT NOT NULL,
  selectable INTEGER,
  display_behavior TEXT,
  display_order INTEGER,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(section_id) REFERENCES section(id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (base_price IS NULL OR
--                     (base_price NOT GLOB '*[^0-9.-]*' AND base_price GLOB '*[0-9]*'
--                     AND instr(substr(base_price,2),'-')=0
--                     AND length(base_price)-length(replace(base_price,'.',''))<=1))
-- Deferred in source: FOREIGN KEY(section_id) REFERENCES section(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (selectable IN (0,1))
-- CHECK (active IN (0,1))

CREATE TABLE interior_definition (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  source_note TEXT,
  color_overrides_raw TEXT,
  legacy_id TEXT NOT NULL,
  name TEXT,
  material TEXT,
  stored_price TEXT,
  price_trim TEXT,
  seat TEXT,
  interior_code TEXT,
  suede TEXT,
  stitch TEXT,
  two_tone TEXT,
  section_id TEXT NOT NULL,
  active_for_stingray INTEGER,
  requires_r6x INTEGER,
  included_legacy_id TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(section_id) REFERENCES section(id),
  UNIQUE(legacy_id)
) STRICT;
-- CHECK (stored_price IS NULL OR
--                     (stored_price NOT GLOB '*[^0-9.-]*' AND stored_price GLOB '*[0-9]*'
--                     AND instr(substr(stored_price,2),'-')=0
--                     AND length(stored_price)-length(replace(stored_price,'.',''))<=1))
-- Deferred in source: FOREIGN KEY(section_id) REFERENCES section(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active_for_stingray IN (0,1))
-- CHECK (requires_r6x IN (0,1))

CREATE TABLE section_presentation (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  section_id TEXT NOT NULL,
  display_label TEXT,
  step_key TEXT,
  display_behavior TEXT,
  display_order INTEGER,
  standard_equipment_bucket INTEGER,
  standard_equipment_group_type TEXT,
  auto_added_bucket INTEGER,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(section_id) REFERENCES section(id),
  UNIQUE(model_id,section_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(section_id) REFERENCES section(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (standard_equipment_bucket IN (0,1))
-- CHECK (auto_added_bucket IN (0,1))
-- CHECK (active IN (0,1))

CREATE TABLE group_member (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  group_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  display_order INTEGER,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(group_id,model_id) REFERENCES group_rule(id,model_id),
  FOREIGN KEY(target_id,model_id) REFERENCES entity(id,model_id),
  UNIQUE(group_id,target_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(group_id,model_id) REFERENCES group_rule(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(target_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE scope_member (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  position INTEGER,
  scope_id TEXT NOT NULL,
  token TEXT NOT NULL,
  variant_id TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(scope_id,model_id) REFERENCES scope_axis(id,model_id),
  FOREIGN KEY(variant_id,model_id) REFERENCES variant(id,model_id),
  UNIQUE(scope_id,token)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(scope_id,model_id) REFERENCES scope_axis(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(variant_id,model_id) REFERENCES variant(id,model_id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE step_summary (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  step_id TEXT NOT NULL,
  section_id TEXT NOT NULL,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(step_id,model_id) REFERENCES runtime_step(id,model_id),
  FOREIGN KEY(section_id,model_id) REFERENCES summary_section(id,model_id),
  UNIQUE(step_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(step_id,model_id) REFERENCES runtime_step(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(section_id,model_id) REFERENCES summary_section(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE availability (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  option_id TEXT NOT NULL,
  variant_id TEXT NOT NULL,
  status TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(option_id,model_id) REFERENCES option(id,model_id),
  FOREIGN KEY(variant_id,model_id) REFERENCES variant(id,model_id),
  UNIQUE(option_id,variant_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(option_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(variant_id,model_id) REFERENCES variant(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (status IN ('standard','available','unavailable') AND status IS NOT NULL)

CREATE TABLE variant_override (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  option_id TEXT NOT NULL,
  variant_id TEXT NOT NULL,
  selectable INTEGER,
  display_behavior TEXT,
  section_id TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(option_id,model_id) REFERENCES option(id,model_id),
  FOREIGN KEY(variant_id,model_id) REFERENCES variant(id,model_id),
  FOREIGN KEY(section_id) REFERENCES section(id),
  UNIQUE(option_id,variant_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(option_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(variant_id,model_id) REFERENCES variant(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (selectable IN (0,1))
-- Deferred in source: FOREIGN KEY(section_id) REFERENCES section(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE exclusive_member (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  group_id TEXT NOT NULL,
  option_id TEXT NOT NULL,
  display_order INTEGER,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(group_id,model_id) REFERENCES exclusive_group(id,model_id),
  FOREIGN KEY(option_id,model_id) REFERENCES option(id,model_id),
  UNIQUE(group_id,option_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(group_id,model_id) REFERENCES exclusive_group(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(option_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE price_rule (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  notes TEXT,
  legacy_id TEXT NOT NULL,
  condition_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  effect TEXT NOT NULL,
  amount TEXT,
  basis TEXT,
  currency TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(condition_id,model_id) REFERENCES entity(id,model_id),
  FOREIGN KEY(target_id,model_id) REFERENCES option(id,model_id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(condition_id,model_id) REFERENCES entity(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(target_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (amount IS NULL OR
--                     (amount NOT GLOB '*[^0-9.-]*' AND amount GLOB '*[0-9]*'
--                     AND instr(substr(amount,2),'-')=0
--                     AND length(amount)-length(replace(amount,'.',''))<=1))
-- CHECK (effect='override')

CREATE TABLE default_rule (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  notes TEXT,
  legacy_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  condition_kind TEXT NOT NULL,
  condition_code TEXT,
  condition_section_id TEXT,
  condition_option_id TEXT,
  target_section_mode TEXT,
  priority INTEGER,
  display_behavior TEXT,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(target_id,model_id) REFERENCES option(id,model_id),
  FOREIGN KEY(condition_section_id) REFERENCES section(id),
  FOREIGN KEY(condition_option_id,model_id) REFERENCES option(id,model_id),
  UNIQUE(model_id,legacy_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(target_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(condition_section_id) REFERENCES section(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(condition_option_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))
-- CHECK ((condition_kind='always' AND condition_code IS NULL AND condition_section_id IS NULL AND condition_option_id IS NULL)
--         OR (condition_kind='unless_selected_rpo' AND condition_code IS NOT NULL AND condition_section_id IS NULL AND condition_option_id IS NULL)
--         OR (condition_kind='unless_selected_section' AND condition_code IS NULL AND condition_section_id IS NOT NULL AND condition_option_id IS NULL)
--         OR (condition_kind='when_selected_unless_selected_section' AND condition_code IS NULL AND condition_section_id IS NULL AND condition_option_id IS NOT NULL AND target_section_mode='resolved_target_section'))

CREATE TABLE derivation_permission (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  target_id TEXT NOT NULL,
  method TEXT NOT NULL,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(source_id,model_id) REFERENCES option(id,model_id),
  FOREIGN KEY(target_id,model_id) REFERENCES option(id,model_id),
  UNIQUE(source_id,target_id,method)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(source_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(target_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE model_interior (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  legacy_id TEXT NOT NULL,
  definition_id TEXT NOT NULL,
  trim_level TEXT NOT NULL,
  active INTEGER,
  requires_option_id TEXT,
  included_option_id TEXT,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(definition_id) REFERENCES interior_definition(id),
  FOREIGN KEY(requires_option_id,model_id) REFERENCES option(id,model_id),
  FOREIGN KEY(included_option_id,model_id) REFERENCES option(id,model_id),
  UNIQUE(model_id,legacy_id,trim_level)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(definition_id) REFERENCES interior_definition(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))
-- Deferred in source: FOREIGN KEY(requires_option_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(included_option_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE interior_presentation (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  interior_id TEXT NOT NULL,
  seat_label TEXT,
  color_family TEXT,
  material_family TEXT,
  variant_label TEXT,
  group_display_order INTEGER,
  material_display_order INTEGER,
  choice_display_order INTEGER,
  parent_group_label TEXT,
  leaf_label TEXT,
  reference_order INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id),
  UNIQUE(interior_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE interior_hierarchy_member (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  interior_id TEXT NOT NULL,
  node_id TEXT NOT NULL,
  position INTEGER NOT NULL,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id),
  FOREIGN KEY(node_id,model_id) REFERENCES hierarchy_node(id,model_id),
  UNIQUE(interior_id,position)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(node_id,model_id) REFERENCES hierarchy_node(id,model_id) DEFERRABLE INITIALLY DEFERRED

CREATE TABLE interior_component (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  interior_id TEXT NOT NULL,
  code TEXT NOT NULL,
  component_type TEXT NOT NULL,
  label TEXT,
  rate_type TEXT,
  rate_code TEXT,
  rate_trim TEXT,
  rate_id TEXT,
  display_order INTEGER,
  active INTEGER,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id),
  FOREIGN KEY(rate_id) REFERENCES component_rate(id),
  UNIQUE(interior_id,component_type,code)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(rate_id) REFERENCES component_rate(id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (active IN (0,1))

CREATE TABLE color_rule (
  id TEXT PRIMARY KEY REFERENCES entity(id) NOT NULL,
  model_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  interior_id TEXT NOT NULL,
  condition_id TEXT NOT NULL,
  added_id TEXT NOT NULL,
  effect TEXT NOT NULL,
  UNIQUE(id,model_id),
  FOREIGN KEY(model_id) REFERENCES model(id),
  FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id),
  FOREIGN KEY(condition_id,model_id) REFERENCES option(id,model_id),
  FOREIGN KEY(added_id,model_id) REFERENCES option(id,model_id),
  UNIQUE(model_id,interior_id,condition_id,added_id)
) STRICT;
-- Deferred in source: FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(interior_id,model_id) REFERENCES model_interior(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(condition_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- Deferred in source: FOREIGN KEY(added_id,model_id) REFERENCES option(id,model_id) DEFERRABLE INITIALLY DEFERRED
-- CHECK (effect='requires')

-- Trigger DDL retained as reference comments only; not imported by drawDB.
-- CREATE TRIGGER asset_assignment_insert_identity BEFORE INSERT ON asset_assignment
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='asset_assignment' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER asset_assignment_update_identity BEFORE UPDATE ON asset_assignment
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='asset_assignment' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER availability_insert_identity BEFORE INSERT ON availability
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='availability' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER availability_update_identity BEFORE UPDATE ON availability
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='availability' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER color_rule_insert_identity BEFORE INSERT ON color_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='color_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER color_rule_update_identity BEFORE UPDATE ON color_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='color_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER component_rate_insert_identity BEFORE INSERT ON component_rate
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='component_rate' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER component_rate_update_identity BEFORE UPDATE ON component_rate
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='component_rate' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER context_choice_insert_identity BEFORE INSERT ON context_choice
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='context_choice' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER context_choice_update_identity BEFORE UPDATE ON context_choice
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='context_choice' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER context_copy_insert_identity BEFORE INSERT ON context_copy
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='context_copy' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER context_copy_update_identity BEFORE UPDATE ON context_copy
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='context_copy' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER context_section_insert_identity BEFORE INSERT ON context_section
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='context_section' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER context_section_update_identity BEFORE UPDATE ON context_section
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='context_section' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER default_rule_insert_identity BEFORE INSERT ON default_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='default_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER default_rule_update_identity BEFORE UPDATE ON default_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='default_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER derivation_permission_insert_identity BEFORE INSERT ON derivation_permission
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='derivation_permission' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER derivation_permission_update_identity BEFORE UPDATE ON derivation_permission
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='derivation_permission' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER direct_rule_insert_ends BEFORE INSERT ON direct_rule
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.source_id) NOT IN ('option','model_interior') OR (SELECT kind FROM entity WHERE id=NEW.target_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER direct_rule_insert_identity BEFORE INSERT ON direct_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='direct_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER direct_rule_update_ends BEFORE UPDATE ON direct_rule
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.source_id) NOT IN ('option','model_interior') OR (SELECT kind FROM entity WHERE id=NEW.target_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER direct_rule_update_identity BEFORE UPDATE ON direct_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='direct_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER entity_identity_immutable BEFORE UPDATE ON entity
--         BEGIN SELECT RAISE(ABORT,'Candidate entity identities are immutable'); END;
-- CREATE TRIGGER exclusive_group_insert_identity BEFORE INSERT ON exclusive_group
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='exclusive_group' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER exclusive_group_update_identity BEFORE UPDATE ON exclusive_group
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='exclusive_group' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER exclusive_member_insert_identity BEFORE INSERT ON exclusive_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='exclusive_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER exclusive_member_update_identity BEFORE UPDATE ON exclusive_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='exclusive_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER group_member_insert_ends BEFORE INSERT ON group_member
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.target_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER group_member_insert_identity BEFORE INSERT ON group_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='group_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER group_member_update_ends BEFORE UPDATE ON group_member
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.target_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER group_member_update_identity BEFORE UPDATE ON group_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='group_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER group_rule_insert_ends BEFORE INSERT ON group_rule
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.source_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER group_rule_insert_identity BEFORE INSERT ON group_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='group_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER group_rule_update_ends BEFORE UPDATE ON group_rule
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.source_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER group_rule_update_identity BEFORE UPDATE ON group_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='group_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER hierarchy_node_insert_identity BEFORE INSERT ON hierarchy_node
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='hierarchy_node' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER hierarchy_node_update_identity BEFORE UPDATE ON hierarchy_node
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='hierarchy_node' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_component_insert_identity BEFORE INSERT ON interior_component
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_component' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_component_update_identity BEFORE UPDATE ON interior_component
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_component' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_definition_insert_identity BEFORE INSERT ON interior_definition
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_definition' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_definition_update_identity BEFORE UPDATE ON interior_definition
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_definition' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_hierarchy_member_insert_identity BEFORE INSERT ON interior_hierarchy_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_hierarchy_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_hierarchy_member_update_identity BEFORE UPDATE ON interior_hierarchy_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_hierarchy_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_presentation_insert_identity BEFORE INSERT ON interior_presentation
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_presentation' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER interior_presentation_update_identity BEFORE UPDATE ON interior_presentation
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='interior_presentation' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_fact_insert_identity BEFORE INSERT ON model_fact
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model_fact' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_fact_update_identity BEFORE UPDATE ON model_fact
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model_fact' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_insert_identity BEFORE INSERT ON model
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_interior_insert_identity BEFORE INSERT ON model_interior
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model_interior' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_interior_update_identity BEFORE UPDATE ON model_interior
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model_interior' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_presentation_insert_identity BEFORE INSERT ON model_presentation
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model_presentation' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_presentation_update_identity BEFORE UPDATE ON model_presentation
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model_presentation' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER model_update_identity BEFORE UPDATE ON model
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='model' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER option_insert_identity BEFORE INSERT ON option
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='option' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER option_update_identity BEFORE UPDATE ON option
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='option' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER price_rule_insert_ends BEFORE INSERT ON price_rule
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.condition_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER price_rule_insert_identity BEFORE INSERT ON price_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='price_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER price_rule_update_ends BEFORE UPDATE ON price_rule
--                 WHEN (SELECT kind FROM entity WHERE id=NEW.condition_id) NOT IN ('option','model_interior') BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END;
-- CREATE TRIGGER price_rule_update_identity BEFORE UPDATE ON price_rule
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='price_rule' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER publication_insert_identity BEFORE INSERT ON publication
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='publication' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER publication_update_identity BEFORE UPDATE ON publication
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='publication' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER runtime_step_insert_identity BEFORE INSERT ON runtime_step
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='runtime_step' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER runtime_step_update_identity BEFORE UPDATE ON runtime_step
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='runtime_step' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER scope_axis_insert_identity BEFORE INSERT ON scope_axis
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='scope_axis' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER scope_axis_update_identity BEFORE UPDATE ON scope_axis
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='scope_axis' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER scope_member_insert_identity BEFORE INSERT ON scope_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='scope_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER scope_member_update_identity BEFORE UPDATE ON scope_member
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='scope_member' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER section_insert_identity BEFORE INSERT ON section
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='section' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER section_presentation_insert_identity BEFORE INSERT ON section_presentation
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='section_presentation' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER section_presentation_update_identity BEFORE UPDATE ON section_presentation
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='section_presentation' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER section_update_identity BEFORE UPDATE ON section
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='section' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER step_summary_insert_identity BEFORE INSERT ON step_summary
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='step_summary' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER step_summary_update_identity BEFORE UPDATE ON step_summary
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='step_summary' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER summary_section_insert_identity BEFORE INSERT ON summary_section
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='summary_section' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER summary_section_update_identity BEFORE UPDATE ON summary_section
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='summary_section' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER variant_insert_identity BEFORE INSERT ON variant
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='variant' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER variant_override_insert_identity BEFORE INSERT ON variant_override
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='variant_override' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER variant_override_update_identity BEFORE UPDATE ON variant_override
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='variant_override' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
-- CREATE TRIGGER variant_update_identity BEFORE UPDATE ON variant
--                 BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
--                   WHERE id=NEW.id AND kind='variant' AND model_id=NEW.model_id)
--                   THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END;
