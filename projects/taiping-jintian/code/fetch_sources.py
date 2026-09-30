#!/usr/bin/env python3
"""Cache the web sources listed in data/documents.json.

Idempotent: a document that is already cached is skipped unless --refetch.
Writes one file per document into sources/raw/web/<doc_id>.json. The cached
plain text is what build_db.py's locators are checked against by hand.

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DOCS = PROJECT / "data" / "documents.json"
CACHE = PROJECT / "sources" / "raw" / "web"
UA = "dhg508-taiping-research/1.0 (coursework; contact via GitHub echozhangmin)"


def api_url(lang: str, title: str) -> str:
    base = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": "1",
        "redirects": "1",
        "converttitles": "1",
        "titles": title,
    }
    return base + "?" + urllib.parse.urlencode(params)


def fetch(lang: str, title: str, retries: int = 4) -> dict:
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(api_url(lang, title), headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = 3 * (2 ** attempt)
                print(f"  {exc.code} on {title}; retry in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    else:
        raise last  # type: ignore[misc]
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        raise RuntimeError("no pages in response")
    page = next(iter(pages.values()))
    if "missing" in page:
        raise RuntimeError(f"page not found: [{lang}] {title}")
    return {
        "canonical_title": page.get("title"),
        "pageid": page.get("pageid"),
        "url": f"https://{lang}.wikipedia.org/wiki/"
        + urllib.parse.quote(page.get("title", title).replace(" ", "_")),
        "extract": page.get("extract", ""),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true", help="refresh cached files")
    ap.add_argument("--delay", type=float, default=1.5, help="seconds between requests")
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    docs = json.loads(DOCS.read_text(encoding="utf-8"))

    fetched = skipped = failed = 0
    for doc in docs:
        spec = doc.get("fetch")
        if not spec:
            continue
        out = CACHE / f"{doc['doc_id']}.json"
        if out.exists() and not args.refetch:
            skipped += 1
            continue
        try:
            payload = fetch(spec["lang"], spec["title"])
        except Exception as exc:  # noqa: BLE001 - report, keep going
            print(f"FAIL {doc['doc_id']}: {exc}", file=sys.stderr)
            failed += 1
            continue
        payload.update(
            {
                "doc_id": doc["doc_id"],
                "requested_lang": spec["lang"],
                "requested_title": spec["title"],
                "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        )
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        chars = len(payload["extract"])
        print(f"ok   {doc['doc_id']:<26} {chars:>7} chars  {payload['canonical_title']}")
        fetched += 1
        time.sleep(args.delay)

    print(f"\nfetched={fetched} skipped={skipped} failed={failed} -> {CACHE}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
