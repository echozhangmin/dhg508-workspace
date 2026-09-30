#!/usr/bin/env python3
"""Build the 天国掌故 relational database from data/*.json.

Standard library only. Validates before writing anything:

  * every doc_id referenced is a real document;
  * every person_id / place_id / event_id foreign key resolves;
  * provenance columns (doc_id, locator, note) exist and doc_id/locator are
    non-empty on every fact row;
  * normal-forms match the ISO-ish pattern, and a lunar-qing normal form has a
    matching row in date_conversions;
  * UNIQUE / CHECK constraints hold (enforced by SQLite on insert).

On success writes artifacts/taiping.db and copies it into the tianwang-lookup
skill folder. Re-running always rebuilds from scratch, so old rows are never
half-mutated.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]  # .../dhg508-workspace
DATA = PROJECT / "data"
ARTIFACT = PROJECT / "artifacts" / "taiping.db"
SKILL_DB = ROOT / ".opencode" / "skill" / "tianwang-lookup" / "taiping.db"

DATE_RE = re.compile(r"^$|^\d{3,4}(-\d{2}(-\d{2})?)?\??$")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE documents (
  doc_id   TEXT PRIMARY KEY,
  title    TEXT NOT NULL,
  author   TEXT,
  year     TEXT,
  kind     TEXT NOT NULL CHECK (kind IN ('primary','secondary','reference','image')),
  language TEXT CHECK (language IN ('zh','en','other')),
  locator  TEXT NOT NULL,
  note     TEXT NOT NULL DEFAULT ''
);

CREATE TABLE places (
  place_id    INTEGER PRIMARY KEY,
  name_zh     TEXT NOT NULL,
  name_en     TEXT,
  modern_name TEXT,
  admin       TEXT,
  kind        TEXT,
  lat         REAL,
  lon         REAL,
  doc_id      TEXT NOT NULL REFERENCES documents(doc_id),
  locator     TEXT NOT NULL,
  note        TEXT NOT NULL DEFAULT '',
  UNIQUE(name_zh, admin)
);

CREATE TABLE persons (
  person_id       INTEGER PRIMARY KEY,
  name_zh         TEXT NOT NULL UNIQUE,
  name_en         TEXT,
  surname_zh      TEXT,
  given_zh        TEXT,
  role            TEXT,
  faction         TEXT NOT NULL CHECK (faction IN ('Taiping','Qing','Western','Other')),
  birth_raw       TEXT,
  birth_norm      TEXT,
  death_raw       TEXT,
  death_norm      TEXT,
  death_place_id  INTEGER REFERENCES places(place_id),
  origin_place_id INTEGER REFERENCES places(place_id),
  doc_id          TEXT NOT NULL REFERENCES documents(doc_id),
  locator         TEXT NOT NULL,
  note            TEXT NOT NULL DEFAULT ''
);

CREATE TABLE titles (
  title_id    INTEGER PRIMARY KEY,
  person_id   INTEGER NOT NULL REFERENCES persons(person_id),
  title_zh    TEXT NOT NULL,
  title_en    TEXT,
  kind        TEXT,
  full_title  TEXT,
  rank_label  TEXT,
  granted_raw TEXT,
  granted_norm TEXT,
  doc_id      TEXT NOT NULL REFERENCES documents(doc_id),
  locator     TEXT NOT NULL,
  note        TEXT NOT NULL DEFAULT '',
  UNIQUE(person_id, title_zh, full_title)
);

CREATE TABLE name_variants (
  variant_id INTEGER PRIMARY KEY,
  person_id  INTEGER NOT NULL REFERENCES persons(person_id),
  variant    TEXT NOT NULL,
  script     TEXT,
  kind       TEXT,
  doc_id     TEXT NOT NULL REFERENCES documents(doc_id),
  locator    TEXT NOT NULL,
  note       TEXT NOT NULL DEFAULT '',
  UNIQUE(person_id, variant)
);

CREATE TABLE events (
  event_id    INTEGER PRIMARY KEY,
  name_zh     TEXT NOT NULL UNIQUE,
  name_en     TEXT,
  date_raw    TEXT,
  date_norm   TEXT,
  date_system TEXT,
  place_id    INTEGER REFERENCES places(place_id),
  kind        TEXT,
  summary     TEXT,
  doc_id      TEXT NOT NULL REFERENCES documents(doc_id),
  locator     TEXT NOT NULL,
  note        TEXT NOT NULL DEFAULT ''
);

CREATE TABLE event_participants (
  ep_id     INTEGER PRIMARY KEY,
  event_id  INTEGER NOT NULL REFERENCES events(event_id),
  person_id INTEGER NOT NULL REFERENCES persons(person_id),
  role      TEXT,
  doc_id    TEXT NOT NULL REFERENCES documents(doc_id),
  locator   TEXT NOT NULL,
  note      TEXT NOT NULL DEFAULT '',
  UNIQUE(event_id, person_id, role)
);

CREATE TABLE date_conversions (
  conv_id       INTEGER PRIMARY KEY,
  raw_date      TEXT NOT NULL,
  from_calendar TEXT NOT NULL,
  norm_date     TEXT,
  to_calendar   TEXT NOT NULL,
  method        TEXT NOT NULL,
  doc_id        TEXT NOT NULL REFERENCES documents(doc_id),
  locator       TEXT NOT NULL,
  note          TEXT NOT NULL DEFAULT ''
);
"""

TABLES = [
    ("documents", "doc_id"), ("places", "place_id"), ("persons", "person_id"),
    ("titles", "title_id"), ("name_variants", "variant_id"), ("events", "event_id"),
    ("event_participants", "ep_id"), ("date_conversions", "conv_id"),
]


def load(name: str) -> list[dict]:
    path = DATA / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def fail(msg: str) -> None:
    raise SystemExit("BUILD FAILED: " + msg)


def validate(d: dict) -> None:
    docs = {r["doc_id"] for r in d["documents"]}
    places = {r["place_id"] for r in d["places"]}
    persons = {r["person_id"] for r in d["persons"]}
    events = {r["event_id"] for r in d["events"]}

    def need_doc(table, row):
        if row.get("doc_id") not in docs:
            fail(f"{table} row {row.get('id', row)} references missing doc_id {row.get('doc_id')!r}")
        if not str(row.get("locator", "")).strip():
            fail(f"{table} row {row} has empty locator")
        if "note" not in row:
            fail(f"{table} row {row} has no note field")

    for r in d["places"]:
        need_doc("places", r)
    for r in d["persons"]:
        need_doc("persons", r)
        for fk in ("death_place_id", "origin_place_id"):
            if r.get(fk) is not None and r[fk] not in places:
                fail(f"persons {r['name_zh']} {fk}={r[fk]} not a place")
        for f in ("birth_norm", "death_norm"):
            if r.get(f) and not DATE_RE.match(r[f]):
                fail(f"persons {r['name_zh']} {f}={r[f]!r} not a valid norm form")
    for r in d["titles"]:
        need_doc("titles", r)
        if r["person_id"] not in persons:
            fail(f"titles {r['title_zh']} person_id {r['person_id']} missing")
        if r.get("granted_norm") and not DATE_RE.match(r["granted_norm"]):
            fail(f"titles {r['title_zh']} granted_norm={r['granted_norm']!r} invalid")
    for r in d["name_variants"]:
        need_doc("name_variants", r)
        if r["person_id"] not in persons:
            fail(f"name_variants {r['variant']} person_id {r['person_id']} missing")
    for r in d["events"]:
        need_doc("events", r)
        if r.get("place_id") is not None and r["place_id"] not in places:
            fail(f"events {r['name_zh']} place_id {r['place_id']} missing")
        if r.get("date_norm") and not DATE_RE.match(r["date_norm"]):
            fail(f"events {r['name_zh']} date_norm={r['date_norm']!r} invalid")
    for r in d["event_participants"]:
        need_doc("event_participants", r)
        if r["event_id"] not in events or r["person_id"] not in persons:
            fail(f"event_participants ep_id {r['ep_id']} dangling FK")

    # Cross-table date rule: a lunar-qing event with a norm form must have a
    # matching date_conversions row.
    conv_norms = {r["norm_date"] for r in d["date_conversions"] if r.get("norm_date")}
    for r in d["events"]:
        if r.get("date_system") == "lunar-qing" and r.get("date_norm") and r["date_norm"] not in conv_norms:
            fail(f"events {r['name_zh']} date_norm {r['date_norm']} has no date_conversions row")
    for r in d["date_conversions"]:
        need_doc("date_conversions", r)
        if r.get("method", "").startswith("computed") and not r.get("norm_date"):
            fail(f"date_conversions {r['conv_id']} computed but empty norm_date")

    total = sum(len(v) for k, v in d.items())
    if total < 200:
        fail(f"only {total} rows; challenge requires at least 200")


def build(d: dict, out: Path) -> sqlite3.Connection:
    if out.exists():
        out.unlink()
    out.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(out)
    con.executescript(SCHEMA)
    for table, _ in TABLES:
        rows = d[table]
        if not rows:
            continue
        cols = list(rows[0].keys())
        q = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join(':'+c for c in cols)})"
        con.executemany(q, rows)
    con.commit()
    return con


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-copy", action="store_true", help="do not copy into the skill")
    args = ap.parse_args()

    d = {t: load(t) for t in ("documents", "places", "persons", "titles", "name_variants",
                              "events", "event_participants", "date_conversions")}
    validate(d)
    con = build(d, ARTIFACT)
    fk_bad = con.execute("PRAGMA foreign_key_check").fetchall()
    if fk_bad:
        fail(f"foreign_key_check reported: {fk_bad}")

    print(f"built {ARTIFACT}")
    grand = 0
    for table, _ in TABLES:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        grand += n
        print(f"  {table:<20} {n:>4}")
    print(f"  {'TOTAL':<20} {grand:>4}")
    con.close()

    if not args.no_copy:
        SKILL_DB.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ARTIFACT, SKILL_DB)
        print(f"copied -> {SKILL_DB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
