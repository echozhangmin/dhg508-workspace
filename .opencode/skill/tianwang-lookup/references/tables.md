# tables.md — what each table holds

`taiping.db` — SQLite. `PRAGMA foreign_keys = ON`. Row counts as of the build
printed by `code/build_db.py`: documents 48, places 49, persons 33, titles 33,
name_variants 34, events 34, event_participants 71, date_conversions 15; total 317.

The one rule that holds everywhere: **every fact row carries `doc_id` (a
foreign key to `documents`) + `locator` (page/section) + `note`.**

## documents
The sources themselves. `doc_id` (PK, text like `wiki-hongxiuquan`,
`meadows1856`), `title, author, year, kind ∈ {primary,secondary,reference,image},
language ∈ {zh,en,other}, locator (URL/archive id), note`.

## places — 地名
`place_id` (PK), `name_zh` (UNIQUE with admin), `name_en, modern_name, admin,
kind, lat, lon, doc_id, locator, note`. Gazetteer of every place named in the
data. `modern_name` is the present-day form; `lat/lon` are approximate.

## persons — 人物
`person_id` (PK), `name_zh` UNIQUE (the form you should query), `name_en,
surname_zh, given_zh, role, faction ∈ {Taiping,Qing,Western,Other}, birth_raw,
birth_norm, death_raw, death_norm, death_place_id → places, origin_place_id →
places, doc_id, locator, note`.
`_raw` = the source's wording; `_norm` = machine form or `''`.

## titles — 封号/职官
`title_id` (PK), `person_id → persons`, `title_zh, title_en, kind, full_title,
rank_label, granted_raw, granted_norm, doc_id, locator, note`. One row per
person-title. `full_title` is the long form (which changes over time — e.g. 石达开's
is longer after 1860); `rank_label` carries things like 九千岁.

## name_variants — 异名
`variant_id` (PK), `person_id → persons`, `variant, script, kind, doc_id,
locator, note`. `kind` ∈ original / childhood / courtesy / epithet /
spelling-variant / taboo / transliteration. **Aliases live here, never as a
second `persons` row.**

## events — 事件
`event_id` (PK), `name_zh` UNIQUE, `name_en, date_raw, date_norm, date_system,
place_id → places, kind, summary, doc_id, locator, note`.
`date_system` ∈ gregorian / lunar-qing / taiping-era.

## event_participants — 参与（连接表）
`ep_id` (PK), `event_id → events`, `person_id → persons`, `role, doc_id,
locator, note`. UNIQUE(event_id, person_id, role). This is why a cross-table
question like "谁参与了天京事变" is one JOIN.

## date_conversions — 日期换算审计
`conv_id` (PK), `raw_date, from_calendar, norm_date, to_calendar, method,
doc_id, locator, note`. Every date normalisation is recorded here. `method` is
a closed set: `sxtwl 2.0.7 (＝lunar-python 1.4.8 cross-check)`, `per source`,
`not converted` (norm_date is `''` and `note` says why).
