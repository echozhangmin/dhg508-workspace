# 天国掌故 / Tianwang-Lookup — 太平天国开国六王小库

> **Week 4 起已被取代。** 本目录保留 week-3 的单表六库作为历史记录。
> 现行数据库是 `../data/*.json`（8 表、300+ 行、6 组外键），由
> `../code/build_db.py` 构建，见 `../research/`，并装载进
> `.opencode/skill/tianwang-lookup/taiping.db`。下面的 `SKILL.md` 仅供对照。

DHG508 week-3：来源 → 数据 → 小库 → 一个 skill。

## 文件

| 文件 | 是什么 |
|---|---|
| `records.json` | 6 条记录的源数据（建库用） |
| `build_db.py` | 用 Python 标准库 sqlite3 建库：`python3 build_db.py` |
| `taiping-kings.db` | SQLite，表 `kings`，6 行 |
| `SKILL.md` | 给 agent 的规矩：输入名字查资料 |

## 表结构

`kings(id, title, name, honorific, full_title, birth, death, death_place,
achievement, source, portrait_url, portrait_note, note)`

## 出处

- 生卒、封号、功绩：各人维基百科条目（见每行 `source`）。
- 画像：多为桂林太平天国纪念馆铜像或现代塑像，**非当时真容**（见 `portrait_note`）。

## 注意

- `.gitignore` 忽略 `*.db`；如需把库提交进 fork，用 `git add -f taiping-kings.db`，
  或只提交 `records.json` + `build_db.py` 由对方重建。
