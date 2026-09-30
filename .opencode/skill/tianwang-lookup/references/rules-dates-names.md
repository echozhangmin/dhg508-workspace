# rules-dates-names.md — dates, names, and the known traps

## Dates

Pairs are deliberate: `*_raw` keeps the source's wording, `*_norm` is the
machine form (or `''`). **Never silently replace one with the other.**

| date_norm stored | means |
|---|---|
| `1851-01-11` | exact day, Gregorian, defensible |
| `1852-06` | month known, day not |
| `1851` | year only |
| `1820?` | the source itself is uncertain ("约…，一说…") |
| `''` (empty) | a raw date exists but no defensible conversion was made |

Every non-`per source` conversion has a row in `date_conversions` naming the
method. Methods are a closed set: `sxtwl 2.0.7 (＝lunar-python 1.4.8
cross-check)`, `per source`, `not converted`.

### Traps to expect

- **金田起义 = 1851-01-11 = 道光三十年十二月初十日.** The Gregorian year is
  1851 but the Qing reign-year is still 道光三十年. Both are correct for
  different calendars; do not "correct" one into the other.
- **永安建制 (event 7) has `date_norm = ''`.** Sources date it to 咸丰元年十二月,
  conventionally called "1851年12月", but that lunar month actually begins
  1852-01-21 Gregorian. This is a deliberate non-conversion — say why.
- **天京陷落 = 同治三年六月十六 = 1864-07-19**, not 同治三年就可推 December.
- Year-only norms like `1820?` are not typos: `question about 萧朝贵's birth year`
  should surface the raw "约1820年（一说1826年）", not pick one.

## Names

- Query by `persons.name_zh` (the common form). On miss, search
  `name_variants.variant` before concluding the person is absent.
- Aliases are rows in `name_variants`, so **never** treat 洪仁坤, 杨嗣龙,
  韦正, 石亚达 as separate people, and never treat 肖朝贵 / 萧朝贵 as two.
- Transcriptions are kept as-is with their source (`kind='transliteration'`),
  because a reader following a citation needs the exact spelling on the page.

### Contested rows (answer with the doubt, not over it)

- **洪宣娇 (person 26):** popular as 洪秀全's 义妹 / 萧朝贵's wife, but the
  biography rests on notes and novels; the row is flagged. Do not assert her as
  a certain historical person.
- **傅善祥 (person 24):** the "唯一女状元" story is disputed; the row records
  both the popular account and the scholarly objection.
- **洪天贵福 (person 7):** Qing sources call him 洪福瑱 — that is a misreading
  of the seal, recorded as a `spelling-variant`, not a second person.
