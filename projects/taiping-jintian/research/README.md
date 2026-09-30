# research/ — how this project works

Week 4 turned the Week 3 `kings-db` (one table, six rows) into a relational
database plus a two-skill setup. These files record how, so the work can be
repeated and grown.

| File | What it is |
|---|---|
| `database-design.md` | The schema: eight tables, six foreign keys, the provenance rule. |
| `pipeline.md` | The exact, repeatable steps from a new source to fresh rows. |
| `normalisation.md` | Rules for converting dates and names, and where the original wording is kept. |
| `verification-20-rows.md` | Twenty random rows checked against their originals, with errors, causes, fixes. |
| `rubric.md` | What makes an answer good or bad, per question. |
| `test-questions.md` / `test-results.md` | The ten test questions and their scored answers. |

The database itself is generated into `../artifacts/taiping.db` and copied into
the `tianwang-lookup` skill folder. Both are rebuildable with
`python3 ../code/build_db.py` — see `pipeline.md`.
