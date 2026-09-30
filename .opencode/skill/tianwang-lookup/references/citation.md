# citation.md — how to cite

Every factual sentence ends with two things:

1. an **id tag** in square brackets, `[table:pk]`, pointing at the exact row;
2. a **source** `doc_id / locator`, pointing at the exact place in the source.

Example:

> 石达开于 1863 年 6 月 27 日在成都受审后就义，年三十二 [person:6]
> （wiki-shidakai / 首段）。他小名亚达，绰号石敢当 [variant:10]
> （wiki-shidakai / 首段）。

Rules:

- Use the table's real key: `[person:6]`, `[title:6]`, `[event:25]`,
  `[place:23]`, `[variant:10]`, `[conv:1]`, `[doc:meadows1856]`.
- Always add `doc_id / locator`. An id without its source is a claim without a
  citation.
- When two rows disagree (a value and its `note`, or two sources), cite **both**
  and state the disagreement — do not average them.
- Prefer the primary source where it exists: `meadows1856` has page-level
  locators (`printed p.155 (vision-checked)`); reference articles use their
  section (`首段`, `生平`, `经过`).
- To expose every citation behind one answer, list them at the end:

  ```
  出处：wiki-shidakai/首段；wiki-shidakai/生平；meadows1856/p.5
  ```
