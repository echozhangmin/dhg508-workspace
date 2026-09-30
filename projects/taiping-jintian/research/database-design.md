# Database design — 天国掌故 / Taiping relations

Week 4 challenge 1. The Week 3 database was a single flat table (`kings`, 6
rows). This one is relational: eight tables, six foreign keys, `NOT NULL`,
`CHECK`, `UNIQUE`, and `PRAGMA foreign_keys = ON`. It was designed so that
adding new material means **adding rows, never reshaping old ones**.

## The one non-negotiable rule: provenance

> **Every row carries `doc_id` + `locator` (document and page/section) and a
> `note`.**

`doc_id` is a foreign key to `documents`. `locator` is the page number for a
book, the section/URL fragment for a web article, or the leaf for a scan.
`note` is `''` only when there is genuinely nothing uncertain; otherwise it
records the doubt. The build script refuses to load a row whose `doc_id` is
not in `documents`.

## Tables

| Table | Rows are | Key link |
|---|---|---|
| `documents` | the sources (books, archive items, Wikipedia articles) | — |
| `places` | a gazetteer of places named in the story | → `documents` |
| `persons` | people (Taiping, Qing, Western) | → `documents`, → `places` (death/origin) |
| `titles` | a title a person held (东王, 忠王, 军师 …) | → `persons`, → `documents` |
| `name_variants` | alternative/earlier/transliterated names | → `persons`, → `documents` |
| `events` | dated happenings (起义, 封王, 天京事变 …) | → `places`, → `documents` |
| `event_participants` | who took part in an event, and how | → `events`, → `persons`, → `documents` |
| `date_conversions` | the audit trail of every date normalisation | → `documents` |

## Entity–relationship sketch

```
documents ──< places ──────────────┐
    │  │  │                        │
    │  │  └──< persons ──< titles  │
    │  │            │  └──< name_variants
    │  │            │
    │  └────────────┴──< event_participants >── events ──> places
    │                                             │
    └──< date_conversions                         └──> documents
```

## Foreign keys (six)

1. `places.doc_id → documents.doc_id`
2. `persons.doc_id → documents.doc_id`
3. `persons.death_place_id → places.place_id`
4. `persons.origin_place_id → places.place_id`
5. `titles.person_id → persons.person_id`
6. `titles.doc_id → documents.doc_id`
7. `name_variants.person_id → persons.person_id`
8. `name_variants.doc_id → documents.doc_id`
9. `events.place_id → places.place_id`
10. `events.doc_id → documents.doc_id`
11. `event_participants.event_id → events.event_id`
12. `event_participants.person_id → persons.person_id`
13. `event_participants.doc_id → documents.doc_id`
14. `date_conversions.doc_id → documents.doc_id`

(Fourteen FK columns, six distinct parent tables.)

## Deliberate constraints

- `documents.kind IN ('primary','secondary','reference','image')` — a CHECK so
  a typo cannot enter.
- `persons.faction IN ('Taiping','Qing','Western','Other')`.
- `UNIQUE(persons.name_zh)` — one row per person; aliases go in
  `name_variants`, not duplicate rows.
- `UNIQUE(event_participants.event_id, person_id, role)` — a person appears
  once per role in an event.
- All `doc_id`/`locator`/`note` columns exist on every fact table, so the
  provenance rule is enforced by shape, not by habit.

## Where normalised values live beside originals

The requirement "keep the original wording beside it and record how you
converted it" is met by paired columns plus the audit table:

- `persons.birth_raw` / `birth_norm`, `death_raw` / `death_norm`;
  `titles.granted_raw` / `granted_norm`; `events.date_raw` / `date_norm`.
  The `_raw` column keeps whatever the source said (e.g. `约1820（一说1826）`).
  The `_norm` column holds the machine form (`1820?` or `1851-01-11`) or
  NULL if no defensible conversion exists.
- `date_conversions` records, per date, the `raw_date`, the source calendar,
  the normalised result, the target calendar, and the **method** used
  (`"lunardate 0.2.2"`, `"per source"`, `"computed, leap-month checked"`).
  A NULL `date_norm` with a populated `date_conversions` row means "we saw the
  date but chose not to collapse it" — that is information too.

See `normalisation.md` for the rules.
