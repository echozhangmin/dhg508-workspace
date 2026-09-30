---
name: taiping-ingest
description: 向「天国掌故」数据库增长资料：新增出处、人物、事件、地点、封号或异名，走可重复管线并重建 taiping.db。Use when the user wants to add sources or rows to the Taiping database, when the data must keep growing, or when tianwang-lookup cannot answer for lack of data.
---

# 天国掌故 taiping-ingest

把新材料加进库。原则：**只增不改、每行带出处、重跑管线即可复现**。

## 最短流程（详见 `references/pipeline.md`）

1. 在 `data/documents.json` 加出处（给稳定的 `doc_id`；网页源加 `fetch` 字段）。
2. `python3 projects/taiping-jintian/code/fetch_sources.py` 缓存原文（幂等）。
3. 在 `data/*.json` 加行：`persons / places / titles / name_variants / events /
   event_participants / date_conversions`。每行必须有 `doc_id`、`locator`、`note`；
   日期/人名按 `references/row-templates.md` 保留原文于 `_raw`、机器形于 `_norm`。
4. `python3 projects/taiping-jintian/code/build_db.py` —— 先校验（外键、约束、出处齐全），
   通过才重建 `taiping.db`，并复制进 `tianwang-lookup` 技能目录。
5. `python3 .../code/check_random_rows.py --n 20` 抽查，把结果记进
   `research/verification-20-rows.md`。

## 边界

- 不确定的值写进 `note`，不要覆盖既有值；被后来资料推翻的行**不删**，
  在新 `doc_id` 里说明（旧换算留在 `date_conversions`）。
- 大文件、API key 不进 Git；库本身小且可重建。

## 加完后

**交回 `tianwang-lookup` 技能**，用新数据重新回答原问题，并给出 `[表:主键]`
与出处。改动原因与前后对照写进 `improvement-log.md`。
