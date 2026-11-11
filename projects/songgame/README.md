# songgame · 北宋赶考记研究项目

为单文件 HTML 游戏《北宋赶考记 · 嘉祐二年》提供史料与学术依据的研究项目。

- 游戏仓库：<https://github.com/echozhangmin/songgame>
- 游戏概要：临川举子正月初十启程，三十日后在汴京应嘉祐二年（1057）省试、殿试；
  管理智力／精力／人缘／盘缠四属性，含题诗、行卷、山匪水匪、欧阳修苏轼等真实人物、
  54 条带史料的词条。题库 150 道来自姊妹项目 `history-quiz`。

## 研究重点

- 省试／殿试制度（三场试卷、糊名誊录、殿试不黜落）
- 嘉祐二年人物与贡举（欧阳修、梅尧臣、苏轼等）
- 举子赴京手续（投状、解状、寄应／冒贯）
- 举子生活与科举文学（诗赋规范、应试生态）

## 当前成果（Week 8 · 历史模拟）

- 作业答卷：[`assignments/week-08/answer.md`](../../assignments/week-08/answer.md)
  （含 evidenced／inferred／invented 证据分级表）
- 幻灯片：[`research/outputs/presentation.html`](research/outputs/presentation.html)
  （浏览器打开，方向键翻页，⌘P 可导出 PDF）
- 讲稿：[`research/outputs/presentation_script.md`](research/outputs/presentation_script.md)
- 未解问题：[`questions.md`](questions.md)

## Layout

```text
projects/songgame/
├── README.md
├── research/
│   ├── design/design_doc.md
│   ├── journal/research_journal.md
│   ├── notes/
│   ├── drafts/
│   ├── outputs/
│   └── references/          ← 书目与检索日志（bibliography.md, search_log.md）
├── sources/
│   ├── raw/
│   └── processed/
├── artifacts/
└── code/
```

## Use

- 书目、引用与检索日志在 `research/references/`。
- 阅读笔记（含页码定位）在 `research/notes/`，研究决策与进展在 `research/journal/`。
- 原始史料放 `sources/raw/`；OCR、整理后的放 `sources/processed/`。
- 大型产物放 `artifacts/`，不提交 git（除非明说）。

## Large Files

提交小而有长期价值的文件；大批 PDF、生成物、索引、数据库不入 git，
在 `artifacts/README.md` 或日志里登记外部或忽略的材料。
