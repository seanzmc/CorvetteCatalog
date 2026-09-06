"""Explicit typed relations for the first disposable workbook import.

Declarations create ordinary SQLite STRICT tables, not property/value storage.
IDs are separate from source locations. Reference columns use typed, model-owned
foreign keys. Evidence and reconciliation metadata are the only JSON storage.
"""
import sqlite3

# Field types: text, integer, boolean, exact decimal, or a typed reference.
TABLES = {
    "model": ("model_key:t registry_key:t label:t year:i active:b expected_variant_count:i default_model:b", "model_key"),
    "model_presentation": ("dataset_name:t export_slug:t setup_card_subtitle:t setup_eyebrow:t setup_title:t setup_description:t", "model_id"),
    "model_fact": ("position:i text:t", "model_id,position"),
    "publication": ("registry_key:t promoted_to_runtime:b default_model:b artifact_path:t artifact_type:t legacy_alias:t active:b display_order:i", "model_id"),
    "section": ("section_key:t name:t selection_mode:t is_required:b display_order:i standard_behavior:t step_key:t", "section_key"),
    "variant": ("legacy_id:t trim_level:t body_style:t display_name:t base_price:d display_order:i active:b membership_order:i membership_active:b", "model_id,legacy_id"),
    "option_definition": ("intrinsic_name:t description:t", ""),
    "offering": ("legacy_id:t definition_id:@option_definition active:b", "model_id,legacy_id"),
    "offering_code": ("offering_id:@offering code:t role:t", "offering_id,code,role"),
    "offering_policy": ("offering_id:@offering selectable:b display_behavior:t", "offering_id"),
    "offering_presentation": ("offering_id:@offering section_id:@section label:t description:t display_order:i", "offering_id"),
    "offering_price": ("offering_id:@offering amount:d basis:t currency:t", "offering_id"),
    "availability": ("offering_id:@offering variant_id:@variant status:t", "offering_id,variant_id"),
    "variant_override": ("offering_id:@offering variant_id:@variant selectable:b display_behavior:t section_id:@section active:b", "offering_id,variant_id"),
    "interior_definition": ("legacy_id:t name:t material:t stored_price:d price_trim:t seat:t interior_code:t suede:t stitch:t two_tone:t section_id:@section active_for_stingray:b requires_r6x:b included_legacy_id:t", "legacy_id"),
    "model_interior": ("legacy_id:t definition_id:@interior_definition trim_level:t active:b requires_offering_id:@offering included_offering_id:@offering", "model_id,legacy_id,trim_level"),
    "interior_presentation": ("interior_id:@model_interior seat_label:t color_family:t material_family:t variant_label:t group_display_order:i material_display_order:i choice_display_order:i parent_group_label:t leaf_label:t reference_order:i", "interior_id"),
    "hierarchy_node": ("parent_id:@hierarchy_node label:t position:i", ""),
    "interior_hierarchy_member": ("interior_id:@model_interior node_id:@hierarchy_node position:i", "interior_id,position"),
    "component_rate": ("component_type:t code:t trim_scope:t amount:d basis:t currency:t", "component_type,code,trim_scope"),
    "interior_component": ("interior_id:@model_interior code:t component_type:t label:t rate_type:t rate_code:t rate_trim:t rate_id:@component_rate display_order:i active:b", "interior_id,component_type,code"),
    "direct_rule": ("legacy_id:t source_id:@entity target_id:@entity effect:t runtime_action:t explanation:t", "model_id,legacy_id"),
    "group_rule": ("legacy_id:t display_label:t effect:t source_id:@entity explanation:t active:b", "model_id,legacy_id"),
    "group_member": ("group_id:@group_rule target_id:@entity display_order:i active:b", "group_id,target_id"),
    "exclusive_group": ("legacy_id:t display_label:t selection_mode:t active:b", "model_id,legacy_id"),
    "exclusive_member": ("group_id:@exclusive_group offering_id:@offering display_order:i active:b", "group_id,offering_id"),
    "price_rule": ("legacy_id:t condition_id:@entity target_id:@offering effect:t amount:d basis:t currency:t", "model_id,legacy_id"),
    "default_rule": ("legacy_id:t target_id:@offering condition_kind:t condition_code:t condition_section_id:@section condition_offering_id:@offering target_section_mode:t priority:i display_behavior:t active:b", "model_id,legacy_id"),
    "color_rule": ("interior_id:@model_interior condition_id:@offering added_id:@offering effect:t", "model_id,interior_id,condition_id,added_id"),
    "scope_axis": ("owner_id:@entity axis:t mode:t", "owner_id,axis"),
    "scope_member": ("scope_id:@scope_axis token:t variant_id:@variant", "scope_id,token"),
    "context_section": ("context_type:t section_key:t name:t selection_mode:t choice_mode:t is_required:b standard_behavior:t display_order:i step_key:t step_label:t active:b", "model_id,context_type"),
    "section_presentation": ("section_id:@section display_label:t step_key:t display_behavior:t display_order:i standard_equipment_bucket:b standard_equipment_group_type:t auto_added_bucket:b active:b", "model_id,section_id"),
    "runtime_step": ("step_key:t label:t runtime_order:i active:b navigable:b", "model_id,step_key"),
    "context_copy": ("context_type:t value:t body_scope:t info_tooltip:t active:b", "model_id,context_type,value,body_scope"),
    "context_choice": ("context_type:t value:t", "model_id,context_type,value"),
    "summary_section": ("section_key:t label:t display_order:i active:b", "model_id,section_key"),
    "step_summary": ("step_id:@runtime_step section_id:@summary_section active:b", "step_id"),
    "asset_assignment": ("target_id:@entity source_scope:t image_url:t image_alt:t image_fit:t image_position:t hover_image_url:t hover_image_alt:t hover_image_position:t active:b", "model_id,target_id,source_scope"),
    "derivation_permission": ("source_id:@offering target_id:@offering method:t", "source_id,target_id,method"),
}

GLOBAL = {"model", "section", "interior_definition", "component_rate"}
CHECKS = {
    "availability": "status IN ('standard','available','unavailable') AND status IS NOT NULL",
    "direct_rule": "effect IN ('requires','includes','excludes') AND (runtime_action IS NULL OR runtime_action='replace')",
    "group_rule": "effect IN ('requires_any','excludes_any')",
    "exclusive_group": "selection_mode IN ('at_most_one','exactly_one')",
    "price_rule": "effect='override'",
    "color_rule": "effect='requires'",
    "scope_axis": "axis IN ('body','trim','variant') AND mode IN ('all','members')",
    "default_rule": """(condition_kind='always' AND condition_code IS NULL AND condition_section_id IS NULL AND condition_offering_id IS NULL)
        OR (condition_kind='unless_selected_rpo' AND condition_code IS NOT NULL AND condition_section_id IS NULL AND condition_offering_id IS NULL)
        OR (condition_kind='unless_selected_section' AND condition_code IS NULL AND condition_section_id IS NOT NULL AND condition_offering_id IS NULL)
        OR (condition_kind='when_selected_unless_selected_section' AND condition_code IS NULL AND condition_section_id IS NULL AND condition_offering_id IS NOT NULL AND target_section_mode='resolved_target_section')""",
}

OPTIONAL_REFS = {("variant_override", "section_id"), ("model_interior", "requires_offering_id"),
                 ("model_interior", "included_offering_id"), ("hierarchy_node", "parent_id"),
                 ("interior_component", "rate_id"), ("default_rule", "condition_section_id"),
                 ("default_rule", "condition_offering_id"), ("scope_member", "variant_id")}


def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


def create(db):
    db.executescript("""
        CREATE TABLE import_metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL) STRICT;
        CREATE TABLE source_sheet(name TEXT PRIMARY KEY, ordinal INTEGER NOT NULL,
          headers TEXT NOT NULL, row_count INTEGER NOT NULL) STRICT;
        CREATE TABLE source_row(id TEXT PRIMARY KEY, sheet TEXT NOT NULL REFERENCES source_sheet(name),
          ordinal INTEGER NOT NULL, cells TEXT NOT NULL, UNIQUE(sheet,ordinal)) STRICT;
        CREATE TABLE entity(id TEXT PRIMARY KEY, kind TEXT NOT NULL, model_id TEXT NOT NULL,
          UNIQUE(id,model_id)) STRICT;
        CREATE TABLE legacy_mapping(namespace TEXT NOT NULL, model_id TEXT NOT NULL,
          kind TEXT NOT NULL, legacy_id TEXT NOT NULL, entity_id TEXT NOT NULL,
          PRIMARY KEY(namespace,model_id,kind,legacy_id),
          FOREIGN KEY(entity_id,model_id) REFERENCES entity(id,model_id)) STRICT;
        CREATE TABLE evidence_link(source_id TEXT NOT NULL REFERENCES source_row(id),
          entity_id TEXT NOT NULL REFERENCES entity(id), PRIMARY KEY(source_id,entity_id)) STRICT;
        CREATE TABLE source_disposition(source_id TEXT NOT NULL REFERENCES source_row(id),
          model_key TEXT NOT NULL, disposition TEXT NOT NULL, reason TEXT NOT NULL,
          PRIMARY KEY(source_id,model_key,disposition)) STRICT;
        CREATE TABLE code_evidence(path TEXT NOT NULL, revision TEXT NOT NULL,
          symbol TEXT NOT NULL, classification TEXT NOT NULL, description TEXT NOT NULL,
          PRIMARY KEY(path,symbol)) STRICT;
    """)
    for table, (spec, key) in TABLES.items():
        columns = ["id TEXT PRIMARY KEY REFERENCES entity(id)", "model_id TEXT NOT NULL",
                   "sequence INTEGER NOT NULL", "UNIQUE(id,model_id)"]
        if table not in GLOBAL:
            columns.append("FOREIGN KEY(model_id) REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED")
        fields, constraints = [], []
        for item in spec.split():
            field, typ = item.split(":")
            sqltype = "INTEGER" if typ in {"i", "b"} else "TEXT"
            required = field in key.split(",") or (typ.startswith("@") and (table, field) not in OPTIONAL_REFS)
            required = required or field in {"effect", "axis", "mode", "condition_kind"}
            fields.append(f"{field} {sqltype}" + (" NOT NULL" if required else ""))
            if typ == "b":
                constraints.append(f"CHECK ({field} IN (0,1))")
            if typ == "d":
                constraints.append(f"""CHECK ({field} IS NULL OR
                    ({field} NOT GLOB '*[^0-9.-]*' AND {field} GLOB '*[0-9]*'
                    AND instr(substr({field},2),'-')=0
                    AND length({field})-length(replace({field},'.',''))<=1))""")
            if typ.startswith("@"):
                target = typ[1:]
                if target in GLOBAL:
                    constraints.append(f"FOREIGN KEY({field}) REFERENCES {target}(id) DEFERRABLE INITIALLY DEFERRED")
                else:
                    constraints.append(f"FOREIGN KEY({field},model_id) REFERENCES {target}(id,model_id) DEFERRABLE INITIALLY DEFERRED")
        # Put table constraints after all field declarations.
        definitions = columns[:3] + fields + columns[3:] + constraints
        if key:
            definitions.append(f"UNIQUE({key})")
        if table in CHECKS:
            definitions.append(f"CHECK ({CHECKS[table]})")
        db.execute(f"CREATE TABLE {table} ({','.join(definitions)}) STRICT")
        for action in ("INSERT", "UPDATE"):
            db.execute(f"""CREATE TRIGGER {table}_{action.lower()}_identity BEFORE {action} ON {table}
                BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM entity
                  WHERE id=NEW.id AND kind='{table}' AND model_id=NEW.model_id)
                  THEN RAISE(ABORT,'Entity subtype or model mismatch') END; END""")
    # Only offering/interior identities are valid polymorphic product rule ends.
    for table, fields in {"direct_rule": ["source_id", "target_id"],
                          "group_rule": ["source_id"], "group_member": ["target_id"],
                          "price_rule": ["condition_id"]}.items():
        for action in ("INSERT", "UPDATE"):
            condition = " OR ".join(f"(SELECT kind FROM entity WHERE id=NEW.{f}) NOT IN ('offering','model_interior')" for f in fields)
            db.execute(f"""CREATE TRIGGER {table}_{action.lower()}_ends BEFORE {action} ON {table}
                WHEN {condition} BEGIN SELECT RAISE(ABORT,'Invalid rule endpoint type'); END""")
    db.execute("""CREATE TRIGGER entity_identity_immutable BEFORE UPDATE ON entity
        BEGIN SELECT RAISE(ABORT,'Candidate entity identities are immutable'); END""")
