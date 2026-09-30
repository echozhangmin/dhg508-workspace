# corner-cases.md — what to do when the request is awkward

The database is the source of record. Skill is not "answer at any cost".

## Off-topic request
(e.g. "给我一个狮子头的菜谱")
Say plainly that this is outside the database's scope (太平天国 1843–1874), and
offer a Taiping question instead. Do **not** answer the off-topic request "as a
favour" and do not mix it with database output.

## The data cannot answer it
Say "库里没有". Show the query/key you tried (person name → `name_variants`;
event name → `events`). Never fill the gap from general knowledge silently. If
the user insists, mark any outside content as **「以下不是库里的内容」**.

## A false premise
Check the premise against the tables before answering the question built on it.
Examples the database can catch:
- "洪宣娇作为西王娘做了 X" → **洪宣娇的史料可信度低**（person 26 note）；西王萧朝贵之妻
  另有说法，不能当作确证前提。
- "太平天国唯一的女状元傅善祥…" → the 女状元 story is **disputed** (person 24
  note); the DB does not assert it.
State which part of the premise fails, then answer the true part.

## "Just look it up online"
Decline to substitute the open web for this database. Explain: the answers must
be traceable to the rows here (`[table:pk]` + `doc_id/locator`); an online answer
is not auditable by this skill. If the point is that the database is thin, say
so and hand over to `taiping-ingest` to add a source.

## A request to invent a quotation
Refuse. You may quote a passage that is actually in a source
(`sources/processed/*` or the cached `doc_id`), with page/section. If no such
passage exists, say "no such quotation is in the database" rather than composing
one that sounds right.

## A date-or-name trap
Use `rules-dates-names.md`. Show `date_raw` beside `date_norm`; if `date_norm`
is empty, explain the ambiguity instead of guessing. For names, resolve through
`name_variants` before answering, and never treat an alias as a new person.

## When the right move is to add data
If the question is legitimate but simply absent, answer "not in the database",
then hand over to **`taiping-ingest`** so the source can be added through the
pipeline and the question re-run.
