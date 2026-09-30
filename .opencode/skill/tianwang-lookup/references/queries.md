# queries.md — ready example queries

Run these with Python's stdlib `sqlite3`. `taiping.db` sits next to `SKILL.md`.
Always select the `doc_id` and `locator` columns so you can cite.

```python
import sqlite3, pathlib
con = sqlite3.connect(pathlib.Path(__file__).with_name("taiping.db"))  # or the SKILL.md dir
con.row_factory = sqlite3.Row
```

## 1. One person, with title, death-place, and citation (cross-table)

```sql
SELECT p.name_zh, t.title_zh, t.full_title, t.rank_label,
       p.birth_raw, p.birth_norm, p.death_raw, p.death_norm,
       pl.name_zh AS death_place,
       p.doc_id AS p_doc, p.locator AS p_loc
FROM persons p
LEFT JOIN titles t  ON t.person_id  = p.person_id
LEFT JOIN places pl ON pl.place_id  = p.death_place_id
WHERE p.name_zh = :name;
```

## 2. Who took part in an event, and in what role

```sql
SELECT e.name_zh AS event, p.name_zh AS person, ep.role,
       ep.doc_id, ep.locator
FROM event_participants ep
JOIN events  e ON e.event_id  = ep.event_id
JOIN persons p ON p.person_id = ep.person_id
WHERE e.name_zh = :event
ORDER BY ep.ep_id;
```

## 3. One person's aliases (never confuse these with separate people)

```sql
SELECT v.variant, v.kind, v.doc_id, v.locator
FROM name_variants v JOIN persons p ON p.person_id = v.person_id
WHERE p.name_zh = :name;
```

## 4. Events at a place, oldest first (place join + nullable date)

```sql
SELECT e.name_zh, e.date_raw, e.date_norm, e.kind
FROM events e JOIN places pl ON pl.place_id = e.place_id
WHERE pl.name_zh = :place
ORDER BY COALESCE(NULLIF(e.date_norm,''), '9999');
```

## 5. The date audit trail for a raw date (provenance of a normalisation)

```sql
SELECT raw_date, from_calendar, norm_date, to_calendar, method, doc_id, locator, note
FROM date_conversions
WHERE raw_date LIKE :fragment;
```

## 6. Everything known about a person in one pass (alias + title + events)

```sql
SELECT 'variant' AS kind, v.variant AS value, v.doc_id, v.locator
  FROM name_variants v JOIN persons p ON p.person_id=v.person_id WHERE p.name_zh=:name
UNION ALL
SELECT 'title', t.title_zh, t.doc_id, t.locator
  FROM titles t JOIN persons p ON p.person_id=t.person_id WHERE p.name_zh=:name
UNION ALL
SELECT 'event', e.name_zh, ep.doc_id, ep.locator
  FROM event_participants ep JOIN events e ON e.event_id=ep.event_id
  JOIN persons p ON p.person_id=ep.person_id WHERE p.name_zh=:name;
```

## 7. Counting / coverage checks

```sql
SELECT faction, COUNT(*) FROM persons GROUP BY faction;
SELECT kind,   COUNT(*) FROM documents GROUP BY kind;
```

## Rules of thumb

- Query by `name_zh` first; if empty, search `name_variants.variant` before
  saying "not in the database".
- A NULL/empty `date_norm` is intentional (see `rules-dates-names.md`); show
  `date_raw` instead of inventing a Gregorian date.
- No result is an answer: say so, with the query you ran.
