---
name: tianwang-lookup
description: 查询「天国掌故」关系型数据库（太平天国 1843–1874 的人物、封号、事件、地点、异名、日期换算），带出处作答。Use when the user asks about Taiping Heavenly Kingdom kings, generals, titles, events, places, dates, or their sources — by name in Chinese (洪秀全/石达开/天京事变…) or English.
---

# 天国掌故 tianwang-lookup

回答太平天国（约1843–1874）的问题。数据在本目录的关系型 SQLite 库
`taiping.db`（8 张表，317 行，6 组外键），不是凭记忆，也不是上网现查。

## 最短上手

- 库文件与本文件同目录：`taiping.db`。用 Python 标准库 `sqlite3` 自写小查询。
- 先想清楚问的是哪张表，再写 SQL；跨表用主键连接（见 `references/queries.md`）。
- **引用格式**：每条事实后写 `[表:主键]`，并给出处 `doc_id / locator`。
  例：`石达开于1863年6月27日在成都受审后就义 [person:6]（wiki-shidakai/首段）`。
- **查不到就说没有**：库里没有的人/事，直接答「库里没有」，不要用常识补；
  若确需补充，必须明说「以下不是库里的内容」。

## 细节按需读取（不要一次全读）

| 需要什么 | 读哪个 |
|---|---|
| 每张表存什么、字段含义、行数 | `references/tables.md` |
| 可直接改用的示例查询（含跨表） | `references/queries.md` |
| 日期与人名的转换规则、已知陷阱 | `references/rules-dates-names.md` |
| 引用与出处怎么写 | `references/citation.md` |
| 没资料／跑题／错前提／要编引文时怎么办 | `references/corner-cases.md` |

## 要往库里加东西时

本库只增不改。若问题缺资料、或用户想加入新人物/事件/出处，**转交给
`taiping-ingest` 技能**（同目录同级）：它负责走管线、重建 `taiping.db`，
再交回本技能作答。
