# Normalisation — dates, names, and how the original is kept

Rules, then examples. The principle: **never overwrite the source's wording;
put the machine form in a second column and an audit row beside it.**

## Dates

Each dated field is paired:

| Column | Holds | Example |
|---|---|---|
| `date_raw` (or `birth_raw`, `death_raw`, `granted_raw`) | exactly what the source said, including "about" and "one theory says" | `约1820（一说1826）` |
| `date_norm` (or `birth_norm`, …) | a machine form, or NULL if none is defensible | `1820?` |
| `date_system` | which calendar the raw wording uses | `lunar-qing`, `gregorian`, `taiping-era` |

Every non-NULL `_norm` has a matching row in `date_conversions`:

```
conv_id, raw_date, from_calendar, norm_date, to_calendar, method, doc_id, locator, note
```

### Method values (closed set)

- `per source` — the source itself gives both forms; no computation.
- `sxtwl 2.0.7` — computed with the 寿星天文历 library, then cross-checked
  against `lunar-python 1.4.8`; both agreed. This is the method for the Qing
  lunar → Gregorian conversions below.
- `not converted` — a raw date exists but no defensible conversion was made.
  `norm_date` is then `''` and the reason is in `note`. Leaving a value blank
  on purpose is recorded, not hidden.

### Worked examples

| raw_date | from | norm_date | method |
|---|---|---|---|
| `道光三十年十二月初十日` | lunar-qing | `1851-01-11` | sxtwl 2.0.7 (＝lunar-python 1.4.8) |
| `同治三年四月二十七日` | lunar-qing | `1864-06-01` | sxtwl 2.0.7 |
| `同治三年六月十六日` | lunar-qing | `1864-07-19` | sxtwl 2.0.7 |
| `咸丰六年八月初四日` | lunar-qing | `1856-09-02` | sxtwl 2.0.7 |
| `约1820（一说1826）` | gregorian | `1820?` | per source |
| `道光三十年` | lunar-qing | `1850` | per source (a reign-year, not a day) |

To regenerate the conversions:

```bash
python3 code/normalize_dates.py        # reads data/date_inputs.json, prints rows
```

The result is committed as `data/date_conversions.json`, so `build_db.py` needs
no third-party library.

## Names

A person's `name_zh` in `persons` is the single most-used form (the one the
user will type: 洪秀全, 石达开). **Everything else is a row in
`name_variants`**, never a duplicate person and never an overwrite.

`name_variants.kind` values:

- `original` — birth/former name kept beside the adopted name:
  `洪仁坤 → 洪秀全`, `杨嗣龙 → 杨秀清`, `韦正 → 韦昌辉`.
- `courtesy` / `childhood` — 小名、字、号: `火秀`, `亚达`, `石敢当`.
- `transliteration` — a foreign rendering with its source's spelling:
  `Hung Seu-tsuen`, `Yang Sew-tsing` (Meadows 1856).
- `spelling-variant` — 肖朝贵/萧朝贵, 胡以晄/胡以晃: the same name written
  differently in different printing traditions.
- `taboo` — 太平天国避讳改字, recorded as such rather than silently applied.

`persons.surname_zh` and `given_zh` split the display name only when the split
is uncontroversial; otherwise they are left empty and the name lives whole in
`name_zh`. The original spelling from a foreign source is *always* kept in
`name_variants`, because the English sources spell the names differently and a
reader following a citation needs to find the right page.
