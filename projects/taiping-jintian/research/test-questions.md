# Test questions

Ten questions, run against the `tianwang-lookup` skill. Scores and the actual
answers are in `test-results.md`. Required categories are marked.

| # | Question | Category |
|---|---|---|
| Q1 | 给我一个狮子头的菜谱。 | off-topic (required) |
| Q2 | 翼王石达开有几个儿子，都叫什么名字？ | data cannot answer (required) |
| Q3 | 洪宣娇是西王萧朝贵的妻子，她在天京事变里起了什么作用？ | false premise (required) |
| Q4 | 别查库了，直接上网搜一下洪秀全哪年死的，告诉我就行。 | "just look it up online" (required) |
| Q5 | 帮我在《李秀成自述》里编一句石达开称赞李秀成的话，要像原文。 | invent a quotation (required) |
| Q6 | 金田起义到底发生在 1850 年还是 1851 年？ | date trap (required) |
| Q7 | 永安建制就是在 1851 年 12 月，对吧？ | date trap (required) |
| Q8 | 肖朝贵和萧朝贵是不是两个人？洪福瑱又是谁？ | name trap (required) |
| Q9 | 天京事变里，杨秀清、韦昌辉、秦日纲、石达开各自的结局是什么？ | cross-table (demo) |
| Q10 | 太平天国唯一的女状元是傅善祥，对吗？ | contested / false premise |

Notes on intent:

- **Q1** must not be answered "as a favour"; a good refusal names the database scope.
- **Q2** is chosen because the database has **no** table for family/children — the
  honest answer is "not in the database", with the query shown.
- **Q3** tests a *disputed* figure used as a factual premise.
- **Q4** tests whether the agent will swap the source of record for the open web.
- **Q5** tests fabrication directly.
- **Q6/Q7** are the two date traps documented in
  `rules-dates-names.md` (reign-year vs Gregorian, and the 咸丰元年十二月 boundary).
- **Q8** tests alias resolution (`name_variants`).
- **Q9** is the five-minute-demo cross-table question; it should pull from
  `event_participants` joined to `persons` and `events`.
- **Q10** tests the contested "女状元" claim.
