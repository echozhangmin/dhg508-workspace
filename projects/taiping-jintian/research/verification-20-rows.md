# Spot check — 20 random rows against the originals

Method: `python3 code/check_random_rows.py --n 20 --seed 508` draws 20 rows,
prints each stored value beside a window of the cached source text, and I
compare them by hand against `sources/raw/web/<doc_id>.json` (or the processed
scan for the book sources). The seed makes the draw repeatable.

## Result of this run

| # | row | verdict |
|---|---|---|
| 1 | place #5 紫荆山 | fixed (locator) |
| 2 | place #36 平南县 | ok |
| 3 | event #8 永安突围 | **error, fixed** |
| 4 | event #27 二破江南大营 | ok |
| 5 | person #18 赖汉英 | ok |
| 6 | person #26 洪宣娇 | ok |
| 7 | name_variant #1 洪仁坤 | ok |
| 8 | name_variant #29 阿七 | ok |
| 9 | place #37 南昌 | ok |
| 10 | person #21 蒙得恩 | ok |
| 11 | place #44 湘乡 | ok |
| 12 | place #29 成都 | ok |
| 13 | place #2 官禄㘵 | fixed (locator) |
| 14 | name_variant #30 七麻子 | ok |
| 15 | place #32 饶州 | ok |
| 16 | event #26 石达开出走 | ok |
| 17 | place #11 全州 | **error, fixed** |
| 18 | place #19 湖口 | ok |
| 19 | name_variant #25 陈作镕 | ok |
| 20 | person #24 傅善祥 | ok |

16 rows matched the source exactly; 4 needed a fix.

## Errors found

### E1 — event #8 永安突围: wrong cause of 乌兰泰's death (content error)

- **Stored (before):** "清将乌兰泰在**攻永安一役中**阵亡。"
- **Original (wiki-wulantai, §戰歿):** "太平軍趁雨夜棄永安州北犯桂林。烏蘭泰率兵急追至昭平山中，因山路險滑遭太平軍埋伏，清軍大敗……烏蘭泰隨後趕到，在南門外將軍橋激戰時，右腿中砲受傷嚴重，退屯陽朔。二十日後，卒於軍中。"
- **Cause:** I collapsed two separate events (the siege of Yong'an and the pursuit
  toward Guilin) into one, and gave the death the wrong place.
- **Fix:** summary rewritten to the pursuit-ambush-death sequence; the `person 29`
  row's `death_place_id` moved from 永安州 to a new place 阳朔 (#49); `locator`
  corrected from 首段 to 戰歿. The old wording is kept in `note`.

### E2 — event #9 全州之战 / place #11 全州: date off by a month (content error)

- **Stored (before):** "1852年6月太平军路过全州".
- **Original (wiki-fengyunshan, §生平):** "1852年**5月24日**太平军路經全州時……6月3日攻克。6月10日太平军在全州蓑衣渡遭到清军伏击。"
- **Cause:** I merged the start of the Quanzhou fighting with the later
  Suoyidu battle (6 June 10) and dated the whole thing to June.
- **Fix:** event #9 `date_raw/date_norm` = 1852-05-24 (城破 6月3日); place #11
  note rewritten; the separate 蓑衣渡 battle stays as event #10 (1852-06-10).

### E3 — place #5 紫荆山: locator pointed at the wrong article (provenance error)

- **Stored:** `doc_id=wiki-jintianqiyi`, which names 紫荆山 but **not** the
  modern place name I stored.
- **Fix:** switched to `wiki-fengyunshan`, which contains
  "廣西紫荆（今廣西桂平市紫荊鎮）"; the note now says where the modern form came from.

### E4 — place #2 官禄㘵: same locator problem

- **Stored:** `doc_id=wiki-hongxiuquan`, which does not name 官禄㘵 or the
  modern village.
- **Fix:** switched to `wiki-fengyunshan` ("洪秀全故里的官禄㘵和他的故里禾落地村
  今均属秀全街道大㘵村").

## What the process showed

- The two content errors (E1, E2) were **date/place conflations** — exactly the
  failure the challenge warns about. Both arose because the same article
  describes several nearby events in one paragraph.
- The two provenance errors (E3, E4) were rows where the *value* was right but
  the *locator* did not contain it. A correct fact with an uncheckable citation
  is not a checkable fact; the build now lets me spot this by printing the
  source window beside every row.
- 16/20 (80%) were clean. The four fixes only added or amended rows; no old row
  was renumbered or deleted, per `pipeline.md`.
