# Week 4 — a real database, a progressive skill

Project: [`projects/taiping-jintian`](../../projects/taiping-jintian).
Everything was done through opencode; the build, the checks and the skills are
all re-runnable.

## The database (challenge 1)

`data/*.json` → `python3 code/build_db.py` → `artifacts/taiping.db`, copied into
the `tianwang-lookup` skill.

- **8 tables, 14 foreign-key columns**, `NOT NULL`/`CHECK`/`UNIQUE`,
  `PRAGMA foreign_keys = ON`. **317 rows** (challenge asked ≥3 tables, ≥2 FKs,
  ≥200 rows).
- Every fact row has `doc_id` + `locator` + `note`; the build refuses to load a
  row without them.
- Dates/names keep the original wording (`*_raw`) beside the machine form
  (`*_norm`); every conversion is auditable in `date_conversions`
  (`non converted` is a recorded decision, not a blank).
- Growth steps are written down in
  [`research/pipeline.md`](../../projects/taiping-jintian/research/pipeline.md);
  rows are only ever added.

## Check it (challenge 2)

[`research/verification-20-rows.md`](../../projects/taiping-jintian/research/verification-20-rows.md):
20 random rows compared with originals. 16 clean, **4 fixed** —
two content errors (乌兰泰's death; the 全州 date) and two bad locators.

## A progressive skill (challenge 3)

- `tianwang-lookup`: short `SKILL.md` (what the DB is, when to use it, how to
  cite `[table:pk]` + `doc_id/locator`, what to do when data is absent) pointing
  to `references/{tables,queries,rules-dates-names,citation,corner-cases}.md`,
  read only when needed.
- `taiping-ingest`: how to add a source/row and rebuild; hands back to the
  lookup skill.

## Test it (challenge 4)

- [`research/rubric.md`](../../projects/taiping-jintian/research/rubric.md) — six
  checks, good vs bad.
- [`research/test-questions.md`](../../projects/taiping-jintian/research/test-questions.md)
  — 10 questions incl. off-topic, no-data, false premise, "look online", invent a
  quotation, date and name traps.
- [`research/test-results.md`](../../projects/taiping-jintian/research/test-results.md)
  — each answer scored (all pass).

## Improve, and log it (challenge 5)

[`improvement-log.md`](../../projects/taiping-jintian/improvement-log.md) — 4
entries, each before/change/after.

---

## Bring to class (5 minutes)

### 1. One question across tables — Q9
「天京事变里，杨秀清、韦昌辉、秦日纲、石达开各自的结局是什么？」

```sql
SELECT e.name_zh AS event, p.name_zh AS person, ep.role, ep.doc_id, ep.locator
FROM event_participants ep
JOIN events  e ON e.event_id  = ep.event_id
JOIN persons p ON p.person_id = ep.person_id
WHERE e.name_zh = '天京事变';
```

Answer: 杨秀清被杀；韦昌辉杀杨后因滥杀被处死；秦日纲参与诛杀后被处死；石达开逃出、
亲眷被害 — each cited `[person:…]` + `wiki-tianjingshibian/首段`.

### 2. Two corner cases handled well
- **Q3 false premise:** 洪宣娇 as a fact — the row's `note` flags the doubt, the
  answer refuses the premise.
- **Q7 date trap:** 永安建制 "1851年12月" — `date_norm` deliberately empty,
  because the lunar month begins 1852-01-21; the answer explains instead of
  collapsing.

### 3. Rubric
`research/rubric.md` (six checks; ≥10/12 good).

### 4. One improvement-log entry
乌兰泰's death (entry 1): before "攻永安阵亡" → fixed to "追击中中炮卒于军中" →
after answer cites `wiki-wulantai/戰歿`.
