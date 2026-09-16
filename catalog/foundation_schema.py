"""Portable structural DDL for the disposable master-schema foundation.

This is a projection of the reviewed logical design, not a complete catalog.
Draft rows may omit payloads until translated. The bounded evaluator source
slice supplies prices and policies; presentation and releases remain absent.
Typed ownership and endpoint keys are concrete.
"""

IDENTITY_RELATIONS = (
    "configuration", "option", "interior", "component", "condition",
    "requirement", "acquisition", "conflict", "choice_group",
    "replacement_plan", "option_rate", "equipment_substitution",
    "content_aspect", "content_effect", "step", "section",
    "summary_section", "visual_scene",
)

# Parent relation -> scope owner column; visual bindings are outside this slice.
SCOPES = {
    "requirement": "requirement_id", "acquisition": "acquisition_id",
    "conflict": "conflict_id", "choice_group": "group_id",
    "replacement_plan": "plan_id", "option_rate": "rate_id",
    "equipment_substitution": "substitution_id", "content_effect": "effect_id",
}
TRANSLATIONS = {
    "configuration": ("configuration_id",), "option": ("option_id",),
    "option_configuration": ("option_id", "configuration_id"),
}

# Only families populated by the bounded source importer receive translation links.
TRANSLATIONS.update({
    "interior": ("interior_id",), "interior_configuration": ("interior_id", "configuration_id"),
    "condition": ("condition_id",), "condition_clause": ("condition_id", "clause_id"),
    "condition_member": ("condition_id", "clause_id", "member_id"),
    "acquisition": ("acquisition_id",), "requirement": ("requirement_id",),
    "choice_group": ("group_id",), "choice_group_member": ("group_id", "option_id"),
    "conflict": ("conflict_id",), "conflict_member": ("conflict_id", "member_id"),
    "replacement_plan": ("plan_id",), "replacement_action": ("plan_id", "position"),
    "option_rate": ("rate_id",), "equipment_substitution": ("substitution_id",),
    "interaction_policy": (), "configuration_policy": ("configuration_id",),
})
TRANSLATIONS.update({f"{parent}_configuration": (column, "configuration_id")
                     for parent, column in SCOPES.items() if parent != "content_effect"})


def money(column):
    # Integer minor units avoid SQLite NUMERIC's floating-point conversion.
    return [f"{column} BIGINT CHECK ({column} >= 0 AND {column} = CAST({column} AS BIGINT))", key("basis_id", True),
            fk("basis_id", "price_basis", "basis_id"),
            f"CHECK (({column} IS NULL AND basis_id IS NULL) OR "
            f"({column} IS NOT NULL AND basis_id IS NOT NULL))"]


def key(name, nullable=False):
    return f"{name} VARCHAR(255)" + ("" if nullable else " NOT NULL")


def fk(columns, table, targets):
    return f'FOREIGN KEY ({columns}) REFERENCES "{table}" ({targets})'


EVIDENCE = [
    key("evidence_set_id"), key("decision_set_id", True),
    fk("evidence_set_id", "evidence_set", "set_id"),
    fk("decision_set_id", "decision_set", "set_id"),
]


def table(name, fields):
    constraints = ("PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK")
    ordered = [f for f in fields if not f.startswith(constraints)]
    ordered += [f for f in fields if f.startswith(constraints)]
    return f'CREATE TABLE "{name}" (\n    ' + ",\n    ".join(ordered) + "\n);"


def endpoint(column, relation, nullable=False):
    return [key(column, nullable), fk(f"revision_id, {column}", relation, "revision_id, id")]


def source_endpoints():
    return (endpoint("source_option_id", "option", True)
            + endpoint("source_interior_id", "interior", True)
            + ["CHECK ((source_option_id IS NOT NULL AND source_interior_id IS NULL)"
               " OR (source_option_id IS NULL AND source_interior_id IS NOT NULL))"])


def statements():
    """Only standard CREATE TABLE, explicit keys, CHECKs and references."""
    yield table("source_document", [
        key("document_id"), "content_sha256 VARCHAR(64) NOT NULL UNIQUE",
        "source_path VARCHAR(2048) NOT NULL", "acquired_at VARCHAR(64) NOT NULL",
        "PRIMARY KEY (document_id)",
    ])
    yield table("source_anchor", [
        key("anchor_id"), key("document_id"), "locator VARCHAR(2048) NOT NULL",
        key("fragment_key"), "PRIMARY KEY (anchor_id)",
        "UNIQUE (document_id, locator, fragment_key)",
        fk("document_id", "source_document", "document_id"),
    ])
    yield table("evidence_set", [key("set_id"), "PRIMARY KEY (set_id)"])
    yield table("evidence_member", [
        key("set_id"), key("anchor_id"), "PRIMARY KEY (set_id, anchor_id)",
        fk("set_id", "evidence_set", "set_id"), fk("anchor_id", "source_anchor", "anchor_id"),
    ])
    yield table("review_decision", [
        key("decision_id"), "version INTEGER NOT NULL CHECK (version > 0)",
        key("evidence_set_id"), "PRIMARY KEY (decision_id, version)",
        fk("evidence_set_id", "evidence_set", "set_id"),
    ])
    yield table("decision_set", [key("set_id"), "PRIMARY KEY (set_id)"])
    yield table("decision_member", [
        key("set_id"), key("decision_id"), "version INTEGER NOT NULL",
        "PRIMARY KEY (set_id, decision_id, version)",
        fk("set_id", "decision_set", "set_id"),
        fk("decision_id, version", "review_decision", "decision_id, version"),
    ])
    yield table("model", [
        key("model_id"), "model_key VARCHAR(255) NOT NULL UNIQUE",
        "name VARCHAR(255) NOT NULL", "PRIMARY KEY (model_id)", *EVIDENCE,
    ])
    yield table("model_year", [
        key("model_year_id"), key("model_id"), "year INTEGER NOT NULL",
        "PRIMARY KEY (model_year_id)", "UNIQUE (model_id, year)",
        "UNIQUE (model_year_id, model_id, year)", fk("model_id", "model", "model_id"),
        *EVIDENCE,
    ])
    yield table("catalog_revision", [
        key("revision_id"), key("model_year_id"), key("parent_revision_id", True),
        "revision_number INTEGER NOT NULL CHECK (revision_number > 0)",
        "state VARCHAR(16) NOT NULL CHECK (state = 'draft')",
        "edit_version INTEGER NOT NULL CHECK (edit_version > 0)",
        "PRIMARY KEY (revision_id)", "UNIQUE (model_year_id, revision_number)",
        "UNIQUE (revision_id, model_year_id)",
        "CHECK ((revision_number = 1 AND parent_revision_id IS NULL) OR"
        " (revision_number > 1 AND parent_revision_id IS NOT NULL))",
        fk("model_year_id", "model_year", "model_year_id"),
        fk("parent_revision_id, model_year_id", "catalog_revision", "revision_id, model_year_id"),
    ])
    for relation in IDENTITY_RELATIONS:
        yield table(f"{relation}_identity", [
            key("model_year_id"), key("id"), key("predecessor_model_year_id", True),
            key("predecessor_id", True), "PRIMARY KEY (model_year_id, id)",
            "CHECK ((predecessor_model_year_id IS NULL AND predecessor_id IS NULL) OR"
            " (predecessor_model_year_id IS NOT NULL AND predecessor_id IS NOT NULL))",
            fk("model_year_id", "model_year", "model_year_id"),
            fk("predecessor_model_year_id, predecessor_id", f"{relation}_identity", "model_year_id, id"),
            *EVIDENCE,
        ])

    yield table("price_basis", [
        key("basis_id"), "currency VARCHAR(3) NOT NULL",
        "minor_units_per_unit INTEGER NOT NULL CHECK (minor_units_per_unit = 100)",
        "amount_meaning VARCHAR(64) NOT NULL CHECK (amount_meaning IN ('vehicle_destination_included', 'option_purchase'))",
        "resolution_state VARCHAR(32) NOT NULL CHECK (resolution_state = 'accepted')",
        "PRIMARY KEY (basis_id)", "UNIQUE (currency, amount_meaning)", *EVIDENCE,
    ])
    payloads = {
        "configuration": ["body VARCHAR(64) NOT NULL", "trim VARCHAR(64) NOT NULL",
                          "enabled INTEGER NOT NULL CHECK (enabled IN (0, 1))",
                          "chooser_order INTEGER NOT NULL", "UNIQUE (revision_id, body, trim)"],
        "option": ["rpo VARCHAR(255)", "name VARCHAR(2048) NOT NULL",
                   "customer_selectable INTEGER NOT NULL CHECK (customer_selectable IN (0, 1))",
                   "lifecycle VARCHAR(32) NOT NULL CHECK (lifecycle IN ('active', 'factory_unavailable', 'retired'))"],
        "interior": endpoint("seat_option_id", "option") + ["code VARCHAR(64)", "enabled INTEGER CHECK (enabled IN (0, 1))"],
        "component": [key("kind"), key("code"), "UNIQUE (revision_id, kind, code)"],
        "condition": ["mode VARCHAR(32) NOT NULL CHECK (mode IN ('always', 'conjunction'))"],
        "requirement": source_endpoints() + endpoint("activation_condition_id", "condition")
                       + endpoint("satisfaction_condition_id", "condition"),
        "acquisition": endpoint("condition_id", "condition") + endpoint("target_option_id", "option"),
        "conflict": source_endpoints() + endpoint("activation_condition_id", "condition"),
        "choice_group": ["minimum INTEGER NOT NULL CHECK (minimum >= 0)",
                         "maximum INTEGER NOT NULL CHECK (maximum >= minimum)"],
        "replacement_plan": endpoint("condition_id", "condition") + endpoint("requested_option_id", "option"),
        "option_rate": endpoint("condition_id", "condition") + endpoint("target_option_id", "option")
                       + ["priority INTEGER NOT NULL", "UNIQUE (revision_id, target_option_id, priority)"],
        "equipment_substitution": endpoint("condition_id", "condition")
                                  + endpoint("removed_option_id", "option")
                                  + endpoint("replacement_option_id", "option", True),
        "content_effect": endpoint("condition_id", "condition") + endpoint("aspect_id", "content_aspect"),
        "section": endpoint("step_id", "step"),
    }
    payloads["configuration"] += money("starting_amount_minor")
    payloads["option"] += money("purchase_amount_minor") + [
        "charge_mode VARCHAR(32) CHECK (charge_mode IN ('priced', 'no_separate_charge'))",
        "CHECK (charge_mode <> 'no_separate_charge' OR (purchase_amount_minor IS NULL AND basis_id IS NULL))",
    ]
    payloads["option_rate"] += money("amount_minor")
    payloads["acquisition"] += [
        "origin_kind VARCHAR(32) CHECK (origin_kind IN ('standard', 'default', 'included', 'dependency'))",
        "peer_policy VARCHAR(32) CHECK (peer_policy IN ('locked', 'yield_to_explicit'))",
        "intent_policy VARCHAR(32) CHECK (intent_policy IN ('absorb_prior', 'preserve_prior'))",
        "priority INTEGER CHECK (priority > 0)",
    ]
    payloads["requirement"] += [
        "source_state VARCHAR(32) CHECK (source_state IN ('resolved_selection', 'chosen'))",
        "CHECK ((source_option_id IS NOT NULL AND source_state = 'resolved_selection') OR "
        "(source_interior_id IS NOT NULL AND source_state = 'chosen'))",
        "loss_policy VARCHAR(64) CHECK (loss_policy = 'remove_source_with_notice_revert')",
    ]
    payloads["choice_group"] += ["peer_policy VARCHAR(32) CHECK (peer_policy = 'replace')"]
    for relation in IDENTITY_RELATIONS:
        yield table(relation, [
            key("revision_id"), key("model_year_id"), key("id"),
            "PRIMARY KEY (revision_id, id)",
            fk("revision_id, model_year_id", "catalog_revision", "revision_id, model_year_id"),
            fk("model_year_id, id", f"{relation}_identity", "model_year_id, id"),
            *payloads.get(relation, []), *EVIDENCE,
        ])
    yield table("option_configuration", [
        key("revision_id"), *endpoint("option_id", "option"),
        *endpoint("configuration_id", "configuration"),
        "status VARCHAR(32) NOT NULL CHECK (status IN ('standard', 'available', 'unavailable'))",
        "PRIMARY KEY (revision_id, option_id, configuration_id)", *EVIDENCE,
    ])
    yield table("interior_configuration", [
        key("revision_id"), *endpoint("interior_id", "interior"),
        *endpoint("configuration_id", "configuration"),
        "PRIMARY KEY (revision_id, interior_id, configuration_id)", *EVIDENCE,
    ])
    for parent, column in SCOPES.items():
        yield table(f"{parent}_configuration", [
            key("revision_id"), *endpoint(column, parent),
            *endpoint("configuration_id", "configuration"),
            f"PRIMARY KEY (revision_id, {column}, configuration_id)", *EVIDENCE,
        ])
    yield table("choice_group_member", [
        key("revision_id"), *endpoint("group_id", "choice_group"),
        *endpoint("option_id", "option"), "PRIMARY KEY (revision_id, group_id, option_id)", *EVIDENCE,
    ])
    yield table("condition_clause", [
        key("revision_id"), *endpoint("condition_id", "condition"), key("clause_id"),
        "mode VARCHAR(32) NOT NULL CHECK (mode IN ('any_present', 'none_present'))",
        "PRIMARY KEY (revision_id, condition_id, clause_id)", *EVIDENCE,
    ])
    yield table("condition_member", [
        key("revision_id"), key("condition_id"), key("clause_id"), key("member_id"),
        *endpoint("option_id", "option", True), *endpoint("interior_id", "interior", True),
        *endpoint("group_id", "choice_group", True), key("state"),
        "PRIMARY KEY (revision_id, condition_id, clause_id, member_id)",
        fk("revision_id, condition_id, clause_id", "condition_clause", "revision_id, condition_id, clause_id"),
        "CHECK ((option_id IS NOT NULL AND interior_id IS NULL AND group_id IS NULL"
        " AND state IN ('explicit_intent', 'resolved_selection')) OR"
        " (option_id IS NULL AND interior_id IS NOT NULL AND group_id IS NULL AND state = 'chosen') OR"
        " (option_id IS NULL AND interior_id IS NULL AND group_id IS NOT NULL AND state = 'occupied'))",
        *[f"UNIQUE (revision_id, condition_id, clause_id, {column}, state)"
          for column in ("option_id", "interior_id", "group_id")], *EVIDENCE,
    ])
    yield table("conflict_member", [
        key("revision_id"), *endpoint("conflict_id", "conflict"), key("member_id"),
        *endpoint("option_id", "option", True), *endpoint("interior_id", "interior", True),
        "PRIMARY KEY (revision_id, conflict_id, member_id)",
        "CHECK ((option_id IS NOT NULL AND interior_id IS NULL) OR (option_id IS NULL AND interior_id IS NOT NULL))",
        "UNIQUE (revision_id, conflict_id, option_id)", "UNIQUE (revision_id, conflict_id, interior_id)", *EVIDENCE,
    ])
    yield table("replacement_action", [
        key("revision_id"), *endpoint("plan_id", "replacement_plan"),
        "position INTEGER NOT NULL CHECK (position > 0)", *endpoint("option_id", "option"),
        "action VARCHAR(16) NOT NULL CHECK (action IN ('add', 'remove'))",
        "intent_effect VARCHAR(32)", "PRIMARY KEY (revision_id, plan_id, position)",
        "CHECK ((action = 'remove' AND intent_effect IS NULL) OR "
        "(action = 'add' AND intent_effect IS NOT NULL AND intent_effect = 'commit_purchase'))", *EVIDENCE,
    ])
    yield table("interaction_policy", [
        key("revision_id"), "PRIMARY KEY (revision_id)", fk("revision_id", "catalog_revision", "revision_id"),
        "conflict_action VARCHAR(32) NOT NULL CHECK (conflict_action = 'notice_confirm_cancel')",
        "direct_removal_action VARCHAR(64) NOT NULL CHECK (direct_removal_action = 'remove_requested_and_supporting_sources')",
        "cancel_action VARCHAR(32) NOT NULL CHECK (cancel_action = 'preserve_whole_state')",
        "revert_action VARCHAR(32) NOT NULL CHECK (revert_action = 'restore_whole_state')", *EVIDENCE,
    ])
    yield table("configuration_policy", [
        key("revision_id"), *endpoint("configuration_id", "configuration"),
        "PRIMARY KEY (revision_id, configuration_id)",
        "interior_minimum INTEGER NOT NULL CHECK (interior_minimum = 1)",
        "interior_maximum INTEGER NOT NULL CHECK (interior_maximum = 1)",
        "context_reset_policy VARCHAR(32) NOT NULL CHECK (context_reset_policy = 'clear_intent')",
        "invalid_interior_action VARCHAR(32) NOT NULL CHECK (invalid_interior_action = 'clear_with_notice_revert')", *EVIDENCE,
    ])
    yield table("source_disposition", [
        key("revision_id"), key("anchor_id"), key("fragment_key"),
        "disposition VARCHAR(32) NOT NULL CHECK (disposition IN ('baseline_sample', 'accepted_target'))",
        "PRIMARY KEY (revision_id, anchor_id, fragment_key)",
        fk("revision_id", "catalog_revision", "revision_id"),
        fk("anchor_id", "source_anchor", "anchor_id"), *EVIDENCE,
    ])
    for relation, columns in TRANSLATIONS.items():
        target_columns = ("id",) if relation in IDENTITY_RELATIONS else columns
        suffix = (", " + ", ".join(columns)) if columns else ""
        target_suffix = (", " + ", ".join(target_columns)) if target_columns else ""
        yield table(f"{relation}_translation", [
            key("revision_id"), key("anchor_id"), key("fragment_key"),
            *["position INTEGER NOT NULL" if column == "position" else key(column) for column in columns],
            f"PRIMARY KEY (revision_id, anchor_id, fragment_key{suffix})",
            fk("revision_id, anchor_id, fragment_key", "source_disposition", "revision_id, anchor_id, fragment_key"),
            fk("revision_id" + suffix, relation, "revision_id" + target_suffix),
            *EVIDENCE,
        ])
