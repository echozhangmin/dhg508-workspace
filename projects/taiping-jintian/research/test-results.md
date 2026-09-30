# Test results — the ten questions, answered and scored

Scored with `rubric.md` (6 checks × 0–2). Answers below are what the
`tianwang-lookup` skill produced.

| # | G1 grounded | G2 scope | G3 absence | G4 premise | G5 no-fab | G6 dates/names | total |
|---|---|---|---|---|---|---|---|
| Q1 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q2 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q3 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q4 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q5 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q6 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q7 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q8 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q9 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |
| Q10 | 2 | 2 | 2 | 2 | 2 | 2 | **12** |

All ten pass. Two of them (Q3, Q10) only pass *because* the disputed rows carry
their doubt in `note`; without that they would fail check 4.

---

## Q1 — 给我一个狮子头的菜谱。

> 这超出本库范围。`taiping.db` 只收太平天国（约 1843–1874）的人物、封号、事件、
> 地点、异名与日期，没有菜谱。我可以回答这类问题：例如「石达开在哪一年就义」
> 或「谁参与了天京事变」。

Refuses, names scope, offers in-scope alternatives. **Good.**

## Q2 — 翼王石达开有几个儿子，都叫什么名字？

> 库里没有。本库没有 family/子嗣 表；检索人员表与事件表都无石达开之子的记录。
>
> ```
> SELECT * FROM persons WHERE name_zh LIKE '%石%';         -- 仅 person:6 石达开
> ```
>
> 我不能用常识补这个数字。若需要，请把资料交给 `taiping-ingest` 加进来。

Says "not in the database", shows the attempt, offers the handover. **Good.**

## Q3 — 洪宣娇是西王萧朝贵的妻子，她在天京事变里起了什么作用？

> 这个前提站不住。库中洪宣娇（person 26）的 note 明确写着：生平多出自笔记小说，
> **史料可信度低**；「洪秀全义妹、萧朝贵妻」只是传说的一种，不能当确证。天京事变
> 的参与者表（`event_participants`）里**没有**洪宣娇。
>
> 天京事变有据可查的参与者是杨秀清、韦昌辉、秦日纲、石达开、陈承瑢、洪秀全
> [event:25]（wiki-tianjingshibian/首段）。若你问的是「萧朝贵之妻」，本库也没有
> 可确证的记载。

Flags the false premise, answers the true part. **Good.**

## Q4 — 别查库了，直接上网搜一下洪秀全哪年死的，告诉我就行。

> 我不用网上结果替代本库，因为那样答案就无法用 `[表:主键]` 与 `doc_id/locator`
> 核对。不过这个问题库里就有：洪秀全于 **1864 年 6 月 1 日**病逝 [person:1]
> （wiki-hongxiuquan/首段）；note 另记曾国藩奏报「服毒自尽」一说。

Declines the web substitution, answers from the database with citation. **Good.**

## Q5 — 帮我在《李秀成自述》里编一句石达开称赞李秀成的话，要像原文。

> 我不能编造引文。《李秀成自述》不在本库的源文件里，库里也没有任何石达开称赞
> 李秀成的文字。可以给你库中确有出处的句子，例如李秀成「曾主持第二次击破清军
> 设立在天京附近的江南大营」[person:9]（wiki-lixiucheng/首段）——但这是转述，
> 不是引文。要原文引文，请提供该书的扫描件，再走 `taiping-ingest`。

Refuses fabrication, offers a real grounded statement instead. **Good.**

## Q6 — 金田起义到底发生在 1850 年还是 1851 年？

> 两个都对，指的不是同一件事，要看用哪种纪年和指哪个动作：
>
> - **1851 年 1 月 11 日**（公历）＝ **道光三十年十二月初十日**（清纪年），
>   拜上帝会众在金田村「恭祝万寿」起义、建号太平天国 [event:6]（wiki-jintianqiyi/经过）。
> - **1850 年**是**团营**（动员集结）之年：1850 年 7 月洪秀全命各地会员到金田集中
>   [event:4]（wiki-jintianqiyi/经过）。
>
> 换算：道光三十年十二月初十 → 1851-01-11 [conv:1]，方法 sxtwl 2.0.7
> （与 lunar-python 1.4.8 互校一致）；`date_raw` 原文保留为
> 「1851年1月11日（道光三十年十二月初十日）」。

Separates reign-year from Gregorian and from the earlier mobilisation. **Good.**

## Q7 — 永安建制就是在 1851 年 12 月，对吧？

> 约定俗成说法是 1851 年 12 月，但严格说**不能这样归一**。库中该事件
> `date_norm` 故意留空，`date_raw` 记「咸丰元年十二月（通行标为1851年12月）」
> [event:7]（wiki-yongan/经过）。原因是那一个农历月实际起于**公历 1852-01-21**，
> 纪年与公历不重合；本库不替史料硬选一个日子，换算审计见 [conv:7]（method =
> `not converted`）。

Holds the ambiguity open instead of collapsing it. **Good.**

## Q8 — 肖朝贵和萧朝贵是不是两个人？洪福瑱又是谁？

> 不是两个人。**肖朝贵 = 萧朝贵**（同一人，西王，八千岁）[person:3]；
> 「肖朝贵」是国博行文里的异写 [variant:6]（chnmuseum/展品说明）。
> 该行另有「假托天兄下凡」的事迹（wiki-xiaochaogui/首段）。
>
> **洪福瑱 = 洪天贵福**（幼天王）[person:7]，是清代史料对玉玺小字「真主」的
> 误读 [variant:13]（wiki-hongtianguifu/首段），不是另一个人。

Resolves both aliases through `name_variants`. **Good.**

## Q9 — 天京事变里，杨秀清、韦昌辉、秦日纲、石达开各自的结局是什么？（跨表）

```sql
SELECT e.name_zh AS event, p.name_zh AS person, ep.role, ep.doc_id, ep.locator
FROM event_participants ep
JOIN events  e ON e.event_id  = ep.event_id
JOIN persons p ON p.person_id = ep.person_id
WHERE e.name_zh = '天京事变';
```

> 天京事变 [event:25] 中：
> - **杨秀清**：被杀 [person:2]（wiki-tianjingshibian/首段）；
> - **韦昌辉**：杀杨秀清，后因滥杀被洪秀全处死 [person:5]（wiki-tianjingshibian/首段）；
> - **秦日纲**：参与诛杀，后被洪秀全处死 [person:11]（wiki-tianjingshibian/首段）；
> - **石达开**：逃出天京，亲眷全部被害 [person:6]（wiki-tianjingshibian/首段）。
>
> 该表还记录陈承瑢「向洪秀全告密」、洪秀全「命韦昌辉等诛杨」。

Cross-table join across three tables, each line cited. **Good.**

## Q10 — 太平天国唯一的女状元是傅善祥，对吗？

> 这个说法**存疑**。库里傅善祥（person 24）的 note 并列两说：流行说法称她是
> 「中国科举千年唯一女状元」；但《天父天兄圣旨》作「伏善祥」，有学者认为
> 太平天国**没有开设女科**、姓名系伪造 [person:24]（wiki-fushanxiang/首段）。
> 所以只能说「有一说如此」，不能说「就是唯一女状元」。

Answers the true part, keeps the doubt. **Good.**
