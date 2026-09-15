"""Disposable SQLite foundation; run with ``python3 -m catalog.foundation``."""

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from uuid import uuid4

from catalog.foundation_schema import IDENTITY_RELATIONS, SCOPES, statements

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / ".local/foundation/catalog.sqlite"
LANES = ("stingray", "grand-sport", "grand-sport-x", "z06", "zr1", "zr1x")
SAMPLE_OPTION_ID = "opt_uvb_001"


def connect(path=DATABASE):
    """The sole foundation connection factory; FK enforcement is per connection."""
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        connection.close()
        raise RuntimeError("SQLite foreign key enforcement is unavailable")
    return connection


def create_schema(connection):
    """Initialize an empty database atomically; never migrate the old candidate."""
    with connection:
        connection.execute("BEGIN")
        for statement in statements():
            connection.execute(statement)


def validate_predecessors(connection):
    for relation in IDENTITY_RELATIONS:
        invalid = connection.execute(f"""
            SELECT i.model_year_id, i.id FROM {relation}_identity i
            JOIN model_year current_year ON current_year.model_year_id = i.model_year_id
            JOIN model_year previous_year ON previous_year.model_year_id = i.predecessor_model_year_id
            WHERE current_year.model_id <> previous_year.model_id
               OR previous_year.year >= current_year.year
        """).fetchone()
        if invalid:
            raise ValueError(f"{relation} predecessor must belong to the same model in an earlier year: {tuple(invalid)}")


def validate_group_scopes(connection):
    """Every named group must cover every configuration of each consuming parent.

    Checks both requirement conditions and every clause, including none_present.
    Empty parent scope is the empty set, never implicit all-scope. Visual bindings
    are not implemented in this foundation and must join this check when added.
    """
    for parent, owner in SCOPES.items():
        if parent == "choice_group":
            continue
        conditions = {
            "requirement": ("activation_condition_id", "satisfaction_condition_id"),
            "conflict": ("activation_condition_id",),
        }.get(parent, ("condition_id",))
        for condition in conditions:
            invalid = connection.execute(f"""
                SELECT p.revision_id, p.id, m.group_id, s.configuration_id
                FROM {parent} p
                JOIN {parent}_configuration s
                  ON s.revision_id = p.revision_id AND s.{owner} = p.id
                JOIN condition_member m
                  ON m.revision_id = p.revision_id AND m.condition_id = p.{condition}
                WHERE m.group_id IS NOT NULL AND NOT EXISTS (
                    SELECT 1 FROM choice_group_configuration g
                    WHERE g.revision_id = p.revision_id AND g.group_id = m.group_id
                      AND g.configuration_id = s.configuration_id
                )
            """).fetchone()
            if invalid:
                raise ValueError(f"{parent}.{condition} scope is not a subset of group scope: {tuple(invalid)}")


def validate(connection):
    """Structural checks only; this does not establish release eligibility."""
    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        raise ValueError("foreign key enforcement is disabled")
    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    if violations:
        raise ValueError(f"foreign key violations: {[tuple(r) for r in violations]}")
    validate_predecessors(connection)
    validate_group_scopes(connection)
    for container, member in (("evidence_set", "evidence_member"), ("decision_set", "decision_member")):
        if connection.execute(f"SELECT set_id FROM {container} c WHERE NOT EXISTS "
                              f"(SELECT 1 FROM {member} m WHERE m.set_id = c.set_id)").fetchone():
            raise ValueError(f"empty {container}")
    if connection.execute("""
        SELECT c.revision_id FROM catalog_revision c JOIN catalog_revision p
        ON p.revision_id = c.parent_revision_id
        WHERE p.revision_number >= c.revision_number
    """).fetchone():
        raise ValueError("parent revision must precede its child")


def _insert(connection, table, values):
    columns = ", ".join(values)
    placeholders = ", ".join("?" for _ in values)
    connection.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(values.values()))


def _ensure(connection, table, keys, values):
    """Insert once; reject changed facts instead of replacing recorded evidence."""
    where = " AND ".join(f"{column} = ?" for column in keys)
    existing = connection.execute(f"SELECT * FROM {table} WHERE {where}", tuple(keys.values())).fetchone()
    expected = keys | values
    if existing is None:
        _insert(connection, table, expected)
    elif any(existing[column] != value for column, value in expected.items()):
        raise ValueError(f"recorded {table} differs from sample: {keys}")


def _allocated(connection, table, id_column, keys, values):
    """Global UUIDs are persisted once under their declared natural unique key."""
    where = " AND ".join(f"{column} = ?" for column in keys)
    existing = connection.execute(f"SELECT {id_column} FROM {table} WHERE {where}", tuple(keys.values())).fetchone()
    allocated_id = existing[0] if existing else str(uuid4())
    _ensure(connection, table, keys, values | {id_column: allocated_id})
    return allocated_id


def _evidence(connection, document_id, locator):
    anchor_id = _allocated(connection, "source_anchor", "anchor_id",
                           dict(document_id=document_id, locator=locator, fragment_key=""), {})
    # Reuse an immutable singleton set; do not mutate membership on re-import.
    existing = connection.execute("""
        SELECT e.set_id FROM evidence_member e WHERE e.anchor_id = ?
        AND NOT EXISTS (SELECT 1 FROM evidence_member other
                        WHERE other.set_id = e.set_id AND other.anchor_id <> e.anchor_id)
        ORDER BY e.set_id
    """, (anchor_id,)).fetchone()
    if existing:
        set_id = existing[0]
    else:
        set_id = str(uuid4())
        _insert(connection, "evidence_set", dict(set_id=set_id))
        _insert(connection, "evidence_member", dict(set_id=set_id, anchor_id=anchor_id))
    return anchor_id, dict(evidence_set_id=set_id, decision_set_id=None)


def _translate(connection, relation, revision_id, anchor_id, target, evidence):
    disposition = dict(revision_id=revision_id, anchor_id=anchor_id, fragment_key="")
    _ensure(connection, "source_disposition", disposition,
            dict(disposition="baseline_sample") | evidence)
    _ensure(connection, f"{relation}_translation", disposition | target, evidence)


def _version(connection, relation, revision_id, model_year_id, retained_id, values, evidence):
    _ensure(connection, f"{relation}_identity", dict(model_year_id=model_year_id, id=retained_id),
            dict(predecessor_model_year_id=None, predecessor_id=None) | evidence)
    _ensure(connection, relation, dict(revision_id=revision_id, id=retained_id),
            dict(model_year_id=model_year_id) | values | evidence)


def import_samples(connection, source_dir=ROOT / "docs"):
    """Atomically translate the UVB applicability sample independently in six lanes.

    Sources are the tracked handoff documents, with workbook sheet/row locators
    preserved inside them. Their SHA256 is not misrepresented as a raw-workbook
    hash. All source prices, frozen evidence and accepted overlays stay untouched.
    """
    with connection:
        for lane in LANES:
            path = Path(source_dir) / f"{lane}-structured-records.json"
            raw = path.read_bytes()
            data = json.loads(raw)
            source_path = f"docs/{path.name}"
            digest = hashlib.sha256(raw).hexdigest()
            old = connection.execute("SELECT content_sha256 FROM source_document WHERE source_path = ?",
                                     (source_path,)).fetchall()
            if any(row[0] != digest for row in old):
                raise ValueError(f"source changed; do not refresh the existing sample: {source_path}")
            document = connection.execute("SELECT document_id FROM source_document WHERE content_sha256 = ?",
                                          (digest,)).fetchone()
            if document:
                document_id = document[0]
            else:
                document_id = str(uuid4())
                _insert(connection, "source_document", dict(document_id=document_id, content_sha256=digest,
                        source_path=source_path, acquired_at=datetime.now(timezone.utc).isoformat()))
            rows = data["baseline_rows"]
            model_row, = rows["model_master"]
            _, evidence = _evidence(connection, document_id, f"baseline_rows/model_master/_row={model_row['_row']}")
            model_id = _allocated(connection, "model", "model_id", dict(model_key=data["model_key"]),
                                  dict(name=model_row["model_label"]) | evidence)
            model_year_id = _allocated(connection, "model_year", "model_year_id",
                                       dict(model_id=model_id, year=data["model_year"]), evidence)
            revision_id = _allocated(connection, "catalog_revision", "revision_id",
                                     dict(model_year_id=model_year_id, revision_number=1),
                                     dict(parent_revision_id=None, state="draft", edit_version=1))
            configurations = rows["variant_master"]
            if len({r["variant_id"] for r in configurations}) != len(configurations):
                raise ValueError(f"duplicate configuration IDs: {lane}")
            for row in configurations:
                if row["model_year"] != data["model_year"]:
                    raise ValueError(f"configuration model-year mismatch: {lane}")
                anchor, evidence = _evidence(connection, document_id, f"baseline_rows/variant_master/_row={row['_row']}")
                _version(connection, "configuration", revision_id, model_year_id, row["variant_id"],
                         dict(body=row["body_style"], trim=row["trim_level"],
                              enabled=int(row["active"]), chooser_order=row["display_order"]), evidence)
                _translate(connection, "configuration", revision_id, anchor,
                           dict(configuration_id=row["variant_id"]), evidence)
            option_sheet = data["sheet_roles"]["options"]
            option, = [r for r in rows[option_sheet] if r["option_id"] == SAMPLE_OPTION_ID]
            if option["active"] is not True:
                raise ValueError(f"sample no longer active: {lane}")
            anchor, evidence = _evidence(connection, document_id, f"baseline_rows/{option_sheet}/_row={option['_row']}")
            _version(connection, "option", revision_id, model_year_id, option["option_id"],
                     dict(rpo=option["rpo"], name=option["option_name"],
                          customer_selectable=int(option["selectable"]), lifecycle="active"), evidence)
            _translate(connection, "option", revision_id, anchor, dict(option_id=option["option_id"]), evidence)
            availability_sheet = data["sheet_roles"]["availability"]
            availability = [r for r in rows[availability_sheet] if r["option_id"] == SAMPLE_OPTION_ID]
            if (len(availability) != len(configurations) or
                {r["variant_id"] for r in availability} != {r["variant_id"] for r in configurations}):
                raise ValueError(f"incomplete or duplicate sample applicability: {lane}")
            for row in availability:
                anchor, evidence = _evidence(connection, document_id, f"baseline_rows/{availability_sheet}/_row={row['_row']}")
                target = dict(option_id=row["option_id"], configuration_id=row["variant_id"])
                _ensure(connection, "option_configuration", dict(revision_id=revision_id) | target,
                        dict(status=row["status"]) | evidence)
                _translate(connection, "option_configuration", revision_id, anchor, target, evidence)
        validate(connection)


def main():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with closing(connect()) as connection:
        if not connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchone():
            create_schema(connection)
        import_samples(connection)
        counts = {table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                  for table in ("model", "configuration", "option", "option_configuration")}
        print(json.dumps(dict(database=str(DATABASE), counts=counts, validation="passed"), indent=2))


if __name__ == "__main__":
    main()
