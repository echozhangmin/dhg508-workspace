# improvement-log

Each entry: the question, the answer that was wrong, what was wrong, what I
changed, and the answer after. Changes are in `data/*.json`; rebuild with
`python3 code/build_db.py`.

---

## 1 — 乌兰泰是怎么死的？

- **Answer before:** 「清将乌兰泰在**攻永安一役中**阵亡」[event:8]。
- **What was wrong:** content error. The source distinguishes the siege of
  Yong'an from the later pursuit toward Guilin. 乌兰泰 was ambushed at 昭平山中,
  中炮 at the 将军桥, and died 20 days later in camp — not at the siege.
- **Change:** rewrote `event:8` summary; moved `person:29.death_place_id` from
  永安州 to a new place 阳朔 (#49); `locator` from 首段 to 戰歿; kept the old
  wording in `note`. (Found in the 20-row spot check, E1.)
- **Answer after:** 「太平军趁雨夜弃永安北上；清将乌兰泰追至昭平山中遭伏大败，
  后于将军桥中炮，退屯阳朔，二十日后卒于军中」[person:29]（wiki-wulantai/戰歿）。

## 2 — 全州之战发生在 1852 年的哪个月？

- **Answer before:** 「1852 年 **6 月**太平军路过全州」[event:9] / [place:11]。
- **What was wrong:** date error. 5 月 24 日 the army passed 全州 and the city
  was taken 6 月 3 日; the 6 月 10 日 date belongs to the separate 蓑衣渡 battle.
- **Change:** `event:9` `date_raw/date_norm` → 1852-05-24（6月3日城破）; rewrote
  `place:11` note; kept 蓑衣渡 as its own `event:10`. (Spot check, E2.)
- **Answer after:** 「1852 年 5 月 24 日太平军路经全州，6 月 3 日攻克；冯云山
  6 月 10 日在城外蓑衣渡中炮阵亡」[event:9]（wiki-fengyunshan/生平）。

## 3 — 永安建制是在 1851 年 12 月吗？

- **Answer before:** the database stored `date_norm = "1851-12"`, so the skill
  answered a flat yes.
- **What was wrong:** the Qing lunar month 咸丰元年十二月 begins on **1852-01-21**
  Gregorian. Writing `1851-12` silently equated the reign-year label with a
  Gregorian month — the exact trap the assignment warns about.
- **Change:** set `event:7.date_norm = ""`; added a `date_conversions` row with
  `method = "not converted"` and the reason [conv:7]; the raw wording
  「咸丰元年十二月（通行标为1851年12月）」is kept.
- **Answer after:** 「约定俗成作 1851 年 12 月，但严格说不能归一：该农历月起于
  公历 1852-01-21，本库故意不换算」[event:7]（wiki-yongan/经过）。

## 4 — 洪宣娇作为西王娘，在天京事变里做了什么？

- **Answer before:** the name existed in a persons table with no caveat, so a
  lookup returned her "biography" as fact.
- **What was wrong:** the premise treats a disputed, novel-laden figure as a
  confirmed historical actor; the database (correctly) has no record of her at
  the Tianjing Incident.
- **Change:** kept `person:26` but wrote the doubt into its `note`
  (史料可信度低); added `references/corner-cases.md` to the lookup skill
  ("check the premise before answering"); added it as test question Q3.
- **Answer after:** 「前提站不住：洪宣娇史料可信度低，只是传说；天京事变的
  参与者表里没有她」[person:26] + [event:25]（wiki-hongxuanjiao/首段）；
  有据的参与者另列。
