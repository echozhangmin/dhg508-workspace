# Pipeline — from a new source to fresh rows

This is the "adding new material means running the same steps again" promise,
written down. Every step is a command you can re-run; nothing is edited by
hand inside the database.

## The files that matter

```
projects/taiping-jintian/
├── data/
│   ├── documents.json          # every source, with its id
│   ├── places.json             # gazetteer rows
│   ├── persons.json            # person rows
│   ├── titles.json             # titles held (→ persons)
│   ├── name_variants.json      # aliases (→ persons)
│   ├── events.json             # event rows
│   ├── event_participants.json # who did what (→ events, persons)
│   └── date_conversions.json   # normalisation audit trail
├── code/
│   ├── fetch_sources.py        # cache web sources (idempotent)
│   ├── build_db.py             # validate + load + copy into the skill
│   └── check_random_rows.py    # the 20-row spot check
├── sources/raw/web/            # cached fetched text (one file per doc_id)
└── artifacts/taiping.db        # generated (gitignored)
```

## The steps

### Step 1 — add the source to `documents.json`

Give it a short stable `doc_id` (e.g. `meadows1856`, `wiki-lixiucheng`). Fill
`kind`, `year`, `locator` (URL / archive id). If it is a web article, add
`fetch` (lang + title) so Step 2 can cache it.

### Step 2 — cache the source text

```bash
cd projects/taiping-jintian
python3 code/fetch_sources.py            # fetches only what is not cached
python3 code/fetch_sources.py --refetch  # force refresh
```

Idempotent: a cached file is skipped. The cache lives in `sources/raw/web/`,
one `<doc_id>.json` per fetched document, holding the plain text and the
canonical URL that `locator` should point at.

### Step 3 — add rows

Add records to the per-table JSON files. Every record needs `doc_id`,
`locator`, `note`. `person_id`/`place_id`/`event_id` are small integers you
choose; the next step checks they exist. Use `_raw` for the source wording and
`_norm` for the machine form (see `normalisation.md`); add the matching row to
`date_conversions.json` for each date you convert.

### Step 4 — build (validates, then loads)

```bash
python3 code/build_db.py
```

It fails loudly, before writing anything, if:

- a `doc_id` or a foreign key is dangling,
- a `CHECK`/`UNIQUE` would be violated,
- a required provenance column is empty,
- a `_norm` date has no `date_conversions` row.

On success it writes `artifacts/taiping.db`, prints the row count per table,
and copies the database next to `.opencode/skill/tianwang-lookup/`.

### Step 5 — spot-check

```bash
python3 code/check_random_rows.py --n 20 --seed 508
```

Prints N random rows with their source and asks you to compare against the
cached original. Record the result in `research/verification-20-rows.md`.

## Why adding rows cannot break old rows

- New rows get new ids; nothing is renumbered.
- Aliases go into `name_variants`, never by editing a `persons` row.
- Uncertainty goes into `note`, never by overwriting a value.
- A row that is contradicted later is **not deleted**: its `note` records the
  contradiction and points at the newer `doc_id`. The `date_conversions` table
  keeps the old conversion beside the new one.

That last rule is the reason `date_conversions` is a table and not a function:
it makes every past judgement reviewable.
