#!/usr/bin/env python3
"""Pull N random fact rows from the database with their source context.

Prints, for each row, the stored value and a window from the cached source, so
a human can compare the two and log any error in research/verification-20-rows.md.

    python3 check_random_rows.py --n 20 --seed 508
"""
from __future__ import annotations

import argparse
import json
import random
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DB = PROJECT / "artifacts" / "taiping.db"
CACHE = PROJECT / "sources" / "raw" / "web"

# table, id column, label expression, fields to show, keyword to search
SOURCES = {
    "persons": ("person_id", "name_zh",
                ["name_zh", "birth_raw", "birth_norm", "death_raw", "death_norm", "note"], "name_zh"),
    "titles": ("title_id", "title_zh",
               ["title_zh", "full_title", "rank_label", "granted_raw", "note"], "title_zh"),
    "name_variants": ("variant_id", "variant",
                      ["variant", "kind", "note"], "variant"),
    "events": ("event_id", "name_zh",
               ["name_zh", "date_raw", "date_norm", "summary", "note"], "name_zh"),
    "places": ("place_id", "name_zh",
               ["name_zh", "modern_name", "admin", "note"], "name_zh"),
}


def window(text: str, needle: str, width: int = 220) -> str:
    text = " ".join(text.split())
    i = text.find(needle) if needle else -1
    if i < 0:
        return text[:width] + ("…" if len(text) > width else "")
    a, b = max(0, i - width // 2), min(len(text), i + width // 2)
    return ("…" if a else "") + text[a:b] + ("…" if b < len(text) else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=508)
    args = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    pool = []
    for table, (idc, label, fields, kw) in SOURCES.items():
        for r in con.execute(f"SELECT * FROM {table}"):
            pool.append((table, idc, label, fields, kw, r))
    rng = random.Random(args.seed)
    sample = rng.sample(pool, args.n)

    for i, (table, idc, label, fields, kw, r) in enumerate(sample, 1):
        doc = r["doc_id"]
        loc = r["locator"]
        print(f"\n### {i:>2}. {table} #{r[idc]}  —  {label}: {r[label]}")
        for f in fields:
            val = r[f]
            if val not in (None, ""):
                print(f"     {f}: {val}")
        print(f"     source: {doc} [{loc}]")
        cache_file = CACHE / f"{doc}.json"
        if cache_file.exists():
            text = json.loads(cache_file.read_text(encoding="utf-8")).get("extract", "")
            print(f"     source-text: {window(text, str(r[kw]))}")
        else:
            print(f"     source-text: (no web cache for {doc}; see sources/processed or ocr/)")
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
