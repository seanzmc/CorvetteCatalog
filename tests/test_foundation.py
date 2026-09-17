"""Structural rejection tests and independent six-lane source reconciliation."""

import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from uuid import UUID

from catalog import foundation as f
from catalog.foundation_schema import IDENTITY_RELATIONS, TRANSLATIONS, statements


def insert(connection, table, **values):
    connection.execute(f"INSERT INTO {table} ({', '.join(values)}) VALUES "
                       f"({', '.join('?' for _ in values)})", tuple(values.values()))


class FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = f.connect(":memory:")
        f.create_schema(cls.sample)
        f.import_samples(cls.sample)

    @classmethod
    def tearDownClass(cls):
        cls.sample.close()

    def setUp(self):
        self.db = f.connect(":memory:")
        self.sample.backup(self.db)
        self.addCleanup(self.db.close)
        self.revision = dict(self.db.execute("""
            SELECT r.* FROM catalog_revision r JOIN model_year y USING (model_year_id)
            JOIN model m USING (model_id) WHERE m.model_key = 'stingray'
        """).fetchone())
        self.r = self.revision["revision_id"]
        self.m = self.revision["model_year_id"]
        option = self.db.execute("SELECT * FROM option WHERE revision_id = ?", (self.r,)).fetchone()
        self.evidence = dict(evidence_set_id=option["evidence_set_id"], decision_set_id=None)

    def identity(self, relation, identifier, model_year=None, **extra):
        insert(self.db, relation + "_identity", model_year_id=model_year or self.m,
               id=identifier, **self.evidence, **extra)

    def version(self, relation, identifier, **payload):
        self.identity(relation, identifier)
        insert(self.db, relation, revision_id=self.r, model_year_id=self.m,
               id=identifier, **payload, **self.evidence)

    def test_all_18_typed_pairs_and_explicit_nonnullable_primary_keys(self):
        expected = {
            "configuration", "option", "interior", "component", "condition", "requirement",
            "acquisition", "conflict", "choice_group", "replacement_plan", "option_rate",
            "equipment_substitution", "content_aspect", "content_effect", "step", "section",
            "summary_section", "visual_scene",
        }
        tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        self.assertEqual({t.removesuffix("_identity") for t in tables if t.endswith("_identity")}, expected)
        self.assertTrue(expected <= tables)
        self.assertEqual({t for t in tables if t.endswith("_translation")}, {name + "_translation" for name in TRANSLATIONS})
        for table in tables:
            info = self.db.execute(f"PRAGMA table_info({table})").fetchall()
            primary = [r for r in info if r[5]]
            self.assertTrue(primary, table)
            self.assertTrue(all(r[3] for r in primary), table)
        ddl = "\n".join(statements()).lower()
        for forbidden in ("rowid", "trigger", "autoincrement", "pragma", "if not exists"):
            self.assertNotIn(forbidden, ddl)
        self.assertFalse(self.db.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'").fetchall())

    def test_every_connection_enforces_foreign_keys_including_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "foundation.sqlite"
            for attempt in range(2):
                db = f.connect(path)
                try:
                    if attempt == 0:
                        f.create_schema(db)
                    self.assertEqual(db.execute("PRAGMA foreign_keys").fetchone()[0], 1)
                    with self.assertRaises(sqlite3.IntegrityError):
                        insert(db, "evidence_member", set_id="missing", anchor_id="missing")
                finally:
                    db.close()

    def test_source_values_ids_and_exact_provenance_per_lane(self):
        expected_counts = {"stingray": 6, "grand_sport": 6, "grand_sport_x": 6,
                           "z06": 6, "zr1": 4, "zr1x": 4}
        for path in sorted((f.ROOT / "docs").glob("*-structured-records.json")):
            data = json.loads(path.read_bytes())
            rows = data["baseline_rows"]
            revision = self.db.execute("""
                SELECT r.revision_id FROM catalog_revision r JOIN model_year y USING (model_year_id)
                JOIN model m USING (model_id) WHERE m.model_key = ? AND y.year = ?
            """, (data["model_key"], data["model_year"])).fetchone()[0]
            configs = self.db.execute("SELECT id, body, trim, enabled, chooser_order FROM configuration "
                                      "WHERE revision_id = ? ORDER BY id", (revision,)).fetchall()
            self.assertEqual([tuple(r) for r in configs], sorted(
                (r["variant_id"], r["body_style"], r["trim_level"], int(r["active"]), r["display_order"])
                for r in rows["variant_master"]))
            self.assertEqual(len(configs), expected_counts[data["model_key"]])
            sample, = [r for r in rows[data["sheet_roles"]["options"]] if r["option_id"] == "opt_uvb_001"]
            actual, = self.db.execute("SELECT id, rpo, name, customer_selectable, lifecycle FROM option "
                                      "WHERE revision_id = ?", (revision,)).fetchall()
            self.assertEqual(tuple(actual), (sample["option_id"], sample["rpo"], sample["option_name"],
                                             int(sample["selectable"]), "active"))
            expected_availability = [r for r in rows[data["sheet_roles"]["availability"]]
                                     if r["option_id"] == "opt_uvb_001"]
            actual_availability = self.db.execute("SELECT option_id, configuration_id, status FROM option_configuration "
                                                   "WHERE revision_id = ? ORDER BY configuration_id", (revision,)).fetchall()
            self.assertEqual([tuple(r) for r in actual_availability], sorted(
                (r["option_id"], r["variant_id"], r["status"]) for r in expected_availability))
            for relation, sheet, source_rows, key in (
                ("configuration", "variant_master", rows["variant_master"], "variant_id"),
                ("option", data["sheet_roles"]["options"], [sample], "option_id"),
                ("option_configuration", data["sheet_roles"]["availability"], expected_availability, "variant_id"),
            ):
                links = self.db.execute(f"""
                    SELECT t.*, a.locator, a.fragment_key AS anchor_fragment, d.content_sha256, d.source_path
                    FROM {relation}_translation t JOIN source_anchor a USING (anchor_id)
                    JOIN source_document d USING (document_id) WHERE t.revision_id = ?
                """, (revision,)).fetchall()
                self.assertEqual(len(links), len(source_rows))
                for row in source_rows:
                    locator = f"baseline_rows/{sheet}/_row={row['_row']}"
                    link, = [r for r in links if r["locator"] == locator]
                    self.assertEqual(link["content_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
                    self.assertEqual(link["source_path"], f"docs/{path.name}")
                    self.assertEqual(link["fragment_key"], "")
                    self.assertEqual(link["anchor_fragment"], "")
                    self.assertEqual(link["option_id" if relation == "option" else "configuration_id"], row[key])
                    if relation == "option_configuration":
                        self.assertEqual(link["option_id"], row["option_id"])

    def test_allocate_once_reimport_survives_connection_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.sqlite"
            db = f.connect(path)
            self.sample.backup(db)
            before = list(db.iterdump())
            ids = [r[0] for r in db.execute("SELECT revision_id FROM catalog_revision")]
            for value in ids:
                self.assertEqual(str(UUID(value)), value)
            db.close()
            db = f.connect(path)
            try:
                f.import_samples(db)
                self.assertEqual(list(db.iterdump()), before)
            finally:
                db.close()

    def test_changed_source_is_rejected_without_refreshing_existing_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            for path in (f.ROOT / "docs").glob("*-structured-records.json"):
                Path(directory, path.name).write_bytes(path.read_bytes())
            path = Path(directory, "zr1x-structured-records.json")
            path.write_bytes(path.read_bytes() + b"\n")
            before = list(self.db.iterdump())
            with self.assertRaisesRegex(ValueError, "source changed"):
                f.import_samples(self.db, directory)
            self.assertEqual(list(self.db.iterdump()), before)

    def test_failed_last_lane_rolls_back_all_earlier_lanes(self):
        with tempfile.TemporaryDirectory() as directory:
            for path in (f.ROOT / "docs").glob("*-structured-records.json"):
                Path(directory, path.name).write_bytes(path.read_bytes())
            path = Path(directory, "zr1x-structured-records.json")
            data = json.loads(path.read_bytes())
            sheet = data["sheet_roles"]["availability"]
            data["baseline_rows"][sheet] = [r for r in data["baseline_rows"][sheet]
                                           if r["option_id"] != "opt_uvb_001"]
            path.write_text(json.dumps(data))
            db = f.connect(":memory:")
            try:
                f.create_schema(db)
                with self.assertRaisesRegex(ValueError, "applicability"):
                    f.import_samples(db, directory)
                self.assertEqual(db.execute("SELECT count(*) FROM model").fetchone()[0], 0)
                self.assertEqual(db.execute("SELECT count(*) FROM source_document").fetchone()[0], 0)
            finally:
                db.close()

    def test_model_master_ownership_mismatch_rolls_back_import(self):
        scratch = f.ROOT / ".local"
        scratch.mkdir(exist_ok=True)
        for lane in (f.LANES[0], f.LANES[-1]):
            for field, wrong in (("model_key", "wrong-model"), ("model_year", "2028")):
                with self.subTest(lane=lane, field=field), tempfile.TemporaryDirectory(dir=scratch) as directory:
                    for source_lane in f.LANES:
                        name = f"{source_lane}-structured-records.json"
                        Path(directory, name).write_bytes((f.ROOT / "docs" / name).read_bytes())
                    path = Path(directory, f"{lane}-structured-records.json")
                    data = json.loads(path.read_bytes())
                    # Configurations still agree with the header; only the cited
                    # model-master identity is stale.
                    data["baseline_rows"]["model_master"][0][field] = wrong
                    path.write_text(json.dumps(data))
                    db = f.connect(":memory:")
                    try:
                        f.create_schema(db)
                        before = list(db.iterdump())
                        with self.assertRaisesRegex(ValueError, f"model_master {field} mismatch: {lane}"):
                            f.import_samples(db, directory)
                        self.assertEqual(list(db.iterdump()), before)
                    finally:
                        db.close()

    def test_all_version_owners_reject_cross_model_and_cross_year(self):
        other_year = "stingray-2028-test"
        model = self.db.execute("SELECT model_id FROM model_year WHERE model_year_id = ?", (self.m,)).fetchone()[0]
        insert(self.db, "model_year", model_year_id=other_year, model_id=model, year=2028, **self.evidence)
        other_model = self.db.execute("SELECT model_year_id FROM catalog_revision WHERE revision_id <> ?", (self.r,)).fetchone()[0]
        self.version("condition", "always", mode="always")
        self.version("step", "step")
        self.version("content_aspect", "aspect", name="test aspect")
        payloads = {
            "configuration": dict(body="coupe", trim="test", enabled=1, chooser_order=1),
            "option": dict(rpo=None, name="test", customer_selectable=0, lifecycle="active"),
            "interior": dict(seat_option_id="opt_uvb_001"),
            "component": dict(kind="test", code="test"), "condition": dict(mode="always"),
            "requirement": dict(source_option_id="opt_uvb_001", activation_condition_id="always",
                                satisfaction_condition_id="always"),
            "acquisition": dict(condition_id="always", target_option_id="opt_uvb_001"),
            "conflict": dict(source_option_id="opt_uvb_001", activation_condition_id="always"),
            "choice_group": dict(minimum=0, maximum=1),
            "replacement_plan": dict(condition_id="always", requested_option_id="opt_uvb_001"),
            "option_rate": dict(condition_id="always", target_option_id="opt_uvb_001", priority=1),
            "equipment_substitution": dict(condition_id="always", removed_option_id="opt_uvb_001"),
            "content_effect": dict(condition_id="always", aspect_id="aspect"),
            "content_aspect": dict(name="test aspect"),
            "section": dict(step_id="step"),
        }
        for relation in IDENTITY_RELATIONS:
            # The same source ID may exist in several models/years; that must not
            # permit a version to claim the wrong revision/model-year pair.
            for owner in (other_model, other_year):
                self.identity(relation, "wrong-owner", owner)
                with self.subTest(relation=relation, owner=owner), self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
                    insert(self.db, relation, revision_id=self.r, model_year_id=owner, id="wrong-owner",
                           **payloads.get(relation, {}), **self.evidence)
            # A valid revision/model-year pair cannot borrow an identity from
            # another model/year either, even with the same unqualified ID.
            with self.subTest(relation=relation, missing_identity=True), self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
                insert(self.db, relation, revision_id=self.r, model_year_id=self.m, id="wrong-owner",
                       **payloads.get(relation, {}), **self.evidence)
            self.identity(relation, "wrong-owner")
            insert(self.db, relation, revision_id=self.r, model_year_id=self.m, id="wrong-owner",
                   **payloads.get(relation, {}), **self.evidence)

    def test_revision_parent_must_be_same_model_year(self):
        other = self.db.execute("SELECT revision_id FROM catalog_revision WHERE revision_id <> ?", (self.r,)).fetchone()[0]
        with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
            insert(self.db, "catalog_revision", **(self.revision | dict(revision_id="bad", revision_number=2, parent_revision_id=other)))
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "catalog_revision", **(self.revision | dict(revision_id="bad", revision_number=2)))
        insert(self.db, "catalog_revision", **(self.revision | dict(revision_id="good", revision_number=2, parent_revision_id=self.r)))
        f.validate(self.db)

    def test_full_composite_target_and_disposition_keys(self):
        self.version("option", "another-option", rpo="UVB", name="Duplicate RPO is permitted",
                     customer_selectable=0, lifecycle="active")
        link = dict(self.db.execute("SELECT * FROM option_configuration_translation WHERE revision_id = ?", (self.r,)).fetchone())
        with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
            insert(self.db, "option_configuration_translation", **(link | dict(option_id="another-option")))
        with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
            insert(self.db, "option_configuration_translation", **(link | dict(fragment_key="missing-fragment")))
        foreign_config = self.db.execute("SELECT id FROM configuration WHERE revision_id <> ?", (self.r,)).fetchone()[0]
        with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
            insert(self.db, "option_configuration", revision_id=self.r, option_id="opt_uvb_001",
                   configuration_id=foreign_config, status="standard", **self.evidence)

    def test_predecessor_rules_for_every_identity_family(self):
        current_model = self.db.execute("SELECT model_id FROM model_year WHERE model_year_id = ?", (self.m,)).fetchone()[0]
        other_model_year = self.db.execute("SELECT model_year_id FROM model_year WHERE model_id <> ?", (current_model,)).fetchone()[0]
        for year in (2026, 2028):
            insert(self.db, "model_year", model_year_id=f"year-{year}", model_id=current_model, year=year, **self.evidence)
        for relation in IDENTITY_RELATIONS:
            with self.subTest(relation=relation):
                self.identity(relation, "previous", "year-2026")
                self.identity(relation, "lineage", predecessor_model_year_id="year-2026", predecessor_id="previous")
                f.validate_predecessors(self.db)
                for invalid_year in (self.m, "year-2028", other_model_year):
                    self.identity(relation, "invalid-parent", invalid_year)
                    self.db.execute(f"UPDATE {relation}_identity SET predecessor_model_year_id = ?, predecessor_id = ? "
                                    "WHERE model_year_id = ? AND id = 'lineage'",
                                    (invalid_year, "invalid-parent", self.m))
                    with self.assertRaisesRegex(ValueError, "same model in an earlier year"):
                        f.validate_predecessors(self.db)
                self.db.execute(f"UPDATE {relation}_identity SET predecessor_model_year_id = 'year-2026', "
                                "predecessor_id = 'previous' WHERE model_year_id = ? AND id = 'lineage'", (self.m,))
                with self.assertRaises(sqlite3.IntegrityError):
                    self.identity(relation, "partial", predecessor_id="previous")
                with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
                    self.identity(relation, "missing", predecessor_model_year_id="year-2026", predecessor_id="absent")

    def group_fixture(self):
        self.version("choice_group", "group", minimum=0, maximum=1)
        self.version("condition", "group-condition", mode="conjunction")
        self.version("condition", "always", mode="always")
        insert(self.db, "condition_clause", revision_id=self.r, condition_id="group-condition",
               clause_id="c", mode="none_present", **self.evidence)
        insert(self.db, "condition_member", revision_id=self.r, condition_id="group-condition",
               clause_id="c", member_id="m", group_id="group", state="occupied", **self.evidence)
        insert(self.db, "choice_group_configuration", revision_id=self.r, group_id="group",
               configuration_id="1lt_c07", **self.evidence)

    def test_group_scope_subset_for_every_implemented_condition_consumer(self):
        self.group_fixture()
        self.version("content_aspect", "aspect", name="test aspect")
        parents = {
            "requirement": ("requirement_id", dict(source_option_id="opt_uvb_001", activation_condition_id="always",
                                                   satisfaction_condition_id="group-condition")),
            "acquisition": ("acquisition_id", dict(target_option_id="opt_uvb_001", condition_id="group-condition")),
            "conflict": ("conflict_id", dict(source_option_id="opt_uvb_001", activation_condition_id="group-condition")),
            "replacement_plan": ("plan_id", dict(requested_option_id="opt_uvb_001", condition_id="group-condition")),
            "option_rate": ("rate_id", dict(target_option_id="opt_uvb_001", condition_id="group-condition", priority=1)),
            "equipment_substitution": ("substitution_id", dict(removed_option_id="opt_uvb_001", condition_id="group-condition")),
            "content_effect": ("effect_id", dict(aspect_id="aspect", condition_id="group-condition")),
        }
        for relation, (owner, payload) in parents.items():
            with self.subTest(relation=relation):
                self.version(relation, "consumer", **payload)
                f.validate_group_scopes(self.db)  # empty scope applies nowhere
                insert(self.db, relation + "_configuration", revision_id=self.r, **{owner: "consumer"},
                       configuration_id="1lt_c07", **self.evidence)
                f.validate_group_scopes(self.db)
                insert(self.db, relation + "_configuration", revision_id=self.r, **{owner: "consumer"},
                       configuration_id="2lt_c07", **self.evidence)
                with self.assertRaisesRegex(ValueError, "not a subset"):
                    f.validate_group_scopes(self.db)
                self.db.execute(f"DELETE FROM {relation}_configuration WHERE configuration_id = '2lt_c07'")
        self.db.execute("UPDATE requirement SET activation_condition_id = 'group-condition', satisfaction_condition_id = 'always'")
        insert(self.db, "requirement_configuration", revision_id=self.r, requirement_id="consumer",
               configuration_id="3lt_c07", **self.evidence)
        with self.assertRaisesRegex(ValueError, "requirement.activation_condition_id"):
            f.validate_group_scopes(self.db)

    def test_condition_endpoint_xor_and_duplicate_uniqueness(self):
        self.group_fixture()
        member = dict(self.db.execute("SELECT * FROM condition_member").fetchone())
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "condition_member", **(member | dict(member_id="dup")))
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "condition_member", **(member | dict(member_id="xor", option_id="opt_uvb_001")))

    def test_group_scope_checks_every_clause_and_group_even_in_another_revision(self):
        self.group_fixture()
        self.version("choice_group", "second-group", minimum=0, maximum=1)
        insert(self.db, "condition_clause", revision_id=self.r, condition_id="group-condition",
               clause_id="second-clause", mode="any_present", **self.evidence)
        insert(self.db, "condition_member", revision_id=self.r, condition_id="group-condition",
               clause_id="second-clause", member_id="m", group_id="second-group", state="occupied", **self.evidence)
        self.version("acquisition", "consumer", condition_id="group-condition", target_option_id="opt_uvb_001")
        insert(self.db, "acquisition_configuration", revision_id=self.r, acquisition_id="consumer",
               configuration_id="1lt_c07", **self.evidence)
        with self.assertRaisesRegex(ValueError, "second-group"):
            f.validate_group_scopes(self.db)
        # Even a matching group/configuration ID in another revision cannot
        # supply the missing scope of the current revision.
        insert(self.db, "catalog_revision", **(self.revision | dict(revision_id="second", revision_number=2, parent_revision_id=self.r)))
        for relation, identifier in (("choice_group", "second-group"), ("configuration", "1lt_c07")):
            row = dict(self.db.execute(f"SELECT * FROM {relation} WHERE revision_id = ? AND id = ?", (self.r, identifier)).fetchone())
            insert(self.db, relation, **(row | dict(revision_id="second")))
        insert(self.db, "choice_group_configuration", revision_id="second", group_id="second-group",
               configuration_id="1lt_c07", **self.evidence)
        with self.assertRaisesRegex(ValueError, "second-group"):
            f.validate_group_scopes(self.db)
        insert(self.db, "choice_group_configuration", revision_id=self.r, group_id="second-group",
               configuration_id="1lt_c07", **self.evidence)
        f.validate_group_scopes(self.db)

    def test_declared_uniqueness_and_required_keys(self):
        cases = [
            ("source_document", "document_id"), ("source_anchor", "anchor_id"),
            ("model", "model_id"), ("model_year", "model_year_id"),
            ("catalog_revision", "revision_id"),
        ]
        for relation, primary in cases:
            row = dict(self.db.execute(f"SELECT * FROM {relation} LIMIT 1").fetchone())
            with self.subTest(relation=relation), self.assertRaises(sqlite3.IntegrityError):
                insert(self.db, relation, **(row | {primary: "different-id"}))
        self.identity("configuration", "duplicate-body-trim")
        row = dict(self.db.execute("SELECT * FROM configuration WHERE revision_id = ? LIMIT 1", (self.r,)).fetchone())
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "configuration", **(row | dict(id="duplicate-body-trim")))
        self.version("component", "component", kind="stitch", code="38S")
        self.identity("component", "duplicate-component")
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "component", revision_id=self.r, model_year_id=self.m,
                   id="duplicate-component", kind="stitch", code="38S", **self.evidence)
        self.version("condition", "always", mode="always")
        self.version("option_rate", "rate", condition_id="always", target_option_id="opt_uvb_001", priority=1)
        self.identity("option_rate", "duplicate-rate")
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "option_rate", revision_id=self.r, model_year_id=self.m, id="duplicate-rate",
                   condition_id="always", target_option_id="opt_uvb_001", priority=1, **self.evidence)
        with self.assertRaises(sqlite3.IntegrityError):
            insert(self.db, "step_identity", model_year_id=self.m, id=None, **self.evidence)

    def test_provenance_nonempty_sets_missing_evidence_and_decision_version(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
            self.db.execute("UPDATE option SET evidence_set_id = 'absent'")
        insert(self.db, "decision_set", set_id="decision")
        with self.assertRaisesRegex(ValueError, "empty decision_set"):
            f.validate(self.db)
        insert(self.db, "review_decision", decision_id="review", version=1,
               evidence_set_id=self.evidence["evidence_set_id"])
        with self.assertRaisesRegex(sqlite3.IntegrityError, "FOREIGN KEY"):
            insert(self.db, "decision_member", set_id="decision", decision_id="review", version=2)
        insert(self.db, "decision_member", set_id="decision", decision_id="review", version=1)
        f.validate(self.db)
        insert(self.db, "evidence_set", set_id="empty")
        with self.assertRaisesRegex(ValueError, "empty evidence_set"):
            f.validate(self.db)


if __name__ == "__main__":
    unittest.main()
