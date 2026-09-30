# pipeline.md — the repeatable steps

Canonical, longer version: `projects/taiping-jintian/research/pipeline.md`.
This is the working copy.

## Files

```
projects/taiping-jintian/
  data/documents.json            # every source, with doc_id
  data/{places,persons,titles,name_variants,events,
        event_participants,date_conversions}.json
  code/fetch_sources.py          # cache web sources (idempotent)
  code/normalize_dates.py        # regenerate date_conversions.json (needs sxtwl)
  code/build_db.py               # validate + load + copy into the skill
  code/check_random_rows.py      # spot check
  sources/raw/web/<doc_id>.json  # cached source text
  artifacts/taiping.db           # generated
```

## Steps

```bash
cd projects/taiping-jintian
python3 code/fetch_sources.py            # 2. cache (skips already-cached)
# 3. edit data/*.json  — see row-templates.md
python3 code/build_db.py                 # 4. validate + build + copy to skill
python3 code/check_random_rows.py --n 20 --seed 508   # 5. spot check
```

`build_db.py` aborts before writing if: a `doc_id` is unknown; a foreign key
dangles; a required `doc_id`/`locator` is empty; a `_norm` date is malformed; a
`CHECK`/`UNIQUE` fails; a lunar-qing event has a norm date but no
`date_conversions` row; or the grand total drops under 200.

## Adding rows without breaking old ones

- New rows take new ids; nothing is renumbered.
- Aliases → `name_variants`; never edit the `persons` row.
- Doubt → `note`; never overwrite a value.
- A contradicted row stays, with its `note` pointing at the newer `doc_id`.
- Every conversion is a `date_conversions` row, so old judgements stay auditable.

## Where new sources come from

Primary sources stay in `sources/raw/` and are OCR'd into `sources/processed/`
(see the project's `ocr/README_ocr_methods.md`). Web references are cached to
`sources/raw/web/`. The database cites, it does not contain the source text.
