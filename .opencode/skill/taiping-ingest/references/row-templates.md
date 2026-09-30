# row-templates.md — one template per table

Copy a line, fill it, keep `doc_id` / `locator` / `note` always. Ids are small
integers you choose (next free number).

## documents.json
```json
{"doc_id": "wiki-example", "title": "…", "author": "中文维基百科", "year": "2026",
 "kind": "reference", "language": "zh", "locator": "https://zh.wikipedia.org/wiki/…",
 "note": "", "fetch": {"lang": "zh", "title": "…"}}
```
`kind` ∈ primary/secondary/reference/image.

## places.json
```json
{"place_id": 50, "name_zh": "地名", "name_en": "", "modern_name": "今地名",
 "admin": "省", "kind": "city", "lat": null, "lon": null,
 "doc_id": "wiki-…", "locator": "首段", "note": ""}
```

## persons.json
```json
{"person_id": 34, "name_zh": "常用名", "name_en": "", "surname_zh": "姓", "given_zh": "名",
 "role": "身份", "faction": "Taiping", "birth_raw": "原文写法", "birth_norm": "",
 "death_raw": "原文写法", "death_norm": "", "death_place_id": null, "origin_place_id": null,
 "doc_id": "wiki-…", "locator": "首段", "note": "存疑处写这里"}
```
`faction` ∈ Taiping/Qing/Western/Other. `_norm` must match
`YYYY[-MM[-DD]][?]` or be `""`.

## titles.json
```json
{"title_id": 34, "person_id": 34, "title_zh": "封号", "title_en": "", "kind": "royal",
 "full_title": "全称", "rank_label": "九千岁", "granted_raw": "原文", "granted_norm": "",
 "doc_id": "wiki-…", "locator": "经过", "note": ""}
```

## name_variants.json
```json
{"variant_id": 36, "person_id": 1, "variant": "异名", "script": "hanzi",
 "kind": "original", "doc_id": "wiki-…", "locator": "首段", "note": ""}
```
`kind` ∈ original/childhood/courtesy/epithet/spelling-variant/taboo/transliteration.

## events.json
```json
{"event_id": 35, "name_zh": "事件", "name_en": "", "date_raw": "原文日期",
 "date_norm": "", "date_system": "lunar-qing", "place_id": null, "kind": "battle",
 "summary": "一句话", "doc_id": "wiki-…", "locator": "经过", "note": ""}
```
`date_system` ∈ gregorian/lunar-qing/taiping-era.

## event_participants.json
```json
{"ep_id": 72, "event_id": 35, "person_id": 1, "role": "角色",
 "doc_id": "wiki-…", "locator": "经过", "note": ""}
```

## date_conversions.json
```json
{"conv_id": 16, "raw_date": "原文日期", "from_calendar": "lunar-qing", "norm_date": "1851-01-11",
 "to_calendar": "gregorian", "method": "sxtwl 2.0.7 (＝lunar-python 1.4.8 cross-check)",
 "doc_id": "wiki-…", "locator": "经过", "note": ""}
```

## Date conversion

Add your raw date to the `ROWS` list in `code/normalize_dates.py` (with its
`lunar=[year,month,day,leap]`) and run `python3 code/normalize_dates.py`. The
two libraries must agree or the script stops. `method` is then filled in
automatically; for a date you deliberately do not convert, use
`method="not converted"`, `norm_date=""`, and explain in `note`.
