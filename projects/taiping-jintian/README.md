# 太平天国 / 金田起义 — Weeks 2–4 project

Research question: **Where (and when) did the Taiping movement first break out as an armed
uprising?** Answer: **金田村, 桂平县, 广西 (Jintian village, Guiping, Guangxi), 11 January 1851**
(金田起义).

From Week 3 the project grew a small database and a skill; Week 4 made the database
**relational and checkable** and the skill **progressive**.

## Layout

```
sources/
  raw/            original scans, unchanged; raw/web/ = cached fetched references
  processed/      OCR text produced from the scans
  README_sources.md     provenance + reliability of each source
ocr/                OCR method record (llm_ocr.py, comparisons, machine text)
data/               the database source of truth (8 JSON files)
code/
  fetch_sources.py    cache web sources (idempotent)
  normalize_dates.py  regenerate data/date_conversions.json
  build_db.py         validate + load + copy into the skill
  check_random_rows.py  the 20-row spot check
research/           design, pipeline, normalisation rules, verification, rubric, tests
kings-db/           Week-3 single-table DB + skill, kept as history (superseded)
artifacts/taiping.db  generated database (gitignored; rebuild with build_db.py)
improvement-log.md  before/change/after entries
questions.md        unresolved questions
```

## Week 4 database

`data/*.json` → `code/build_db.py` → `artifacts/taiping.db` → copied into
`.opencode/skill/tianwang-lookup/taiping.db`.

- **8 tables, 14 foreign-key columns** (documents, places, persons, titles,
  name_variants, events, event_participants, date_conversions).
- **317 rows** at the last build; every fact row carries `doc_id` + `locator` +
  `note`.
- Dates and names keep the source wording in `*_raw` beside the machine form in
  `*_norm`; every conversion is audited in `date_conversions`.
- Rebuild: `python3 code/build_db.py`. Add material: see `research/pipeline.md`.

## Skills

- `.opencode/skill/tianwang-lookup/` — answers, progressively: a short
  `SKILL.md` plus `references/{tables,queries,rules-dates-names,citation,corner-cases}.md`.
- `.opencode/skill/taiping-ingest/` — adds data through the pipeline and hands
  back to the lookup skill.

## Where things stand

- Week 2: two sources (中国国家博物馆 + Meadows 1856 p.5, OCR'd) answer the
  place-and-date question; first-hand 1851 evidence in `date-evidence-1851.md`.
- Week 3: 六王单表小库 + one skill.
- Week 4: relational DB, 20-row verification (4 fixes), progressive two-skill
  setup, rubric + 10 test questions, `improvement-log.md`.

Deliverables: `research/rubric.md`, `research/test-questions.md`,
`research/test-results.md`, `improvement-log.md`; demo notes in
`../../assignments/week-04/`.
