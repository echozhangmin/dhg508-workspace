## Added — Meadows (1856), printed p.155 (leaf n229)

Vision transcription vs IA machine OCR (`chineseandtheir01meadgoog.txt`):

| Printed (image) | Machine OCR (IA) | Verdict |
|---|---|---|
| "Eastern village" | "Eastern **Tillage**" | IA letter confusion (v→T) |
| "Peking Gazette" (footnote) | "Peking **Ghizette**" | IA substitution |
| "affairs" | "aflTairs" | ligature artifact (ffl→fT) |
| "attempted" | "attcmptcd" | IA letter confusion (te→tc) |
| "…left **their** camp…" | "left **the** camp" (p.234 variant) | minor |

Both readings agree on the decisive sentence — "the Tae pings left their camp at Kin teen on the
4th March, 1851" — so the footnote is treated as reliable evidence for the 1851 date.

## Added — 《欽定剿平粵匪方略》卷首目錄 (woodblock Chinese)

Machine OCR is unusable on this volume: IA's tesseract `_djvu.txt` is noise, and the AI Chinese
chOCR returns **zero** grep hits for 金田/桂平/洪秀全/咸豐元年/道光三十年/粵匪. Vision reading was
required and succeeded (`sources/processed/qingfanglue-mulu_vision-ocr.md`), yielding the dated
range 卷一至卷五 = 道光三十年五月庚戌至咸豐元年六月乙亥.

## Original comparison (Meadows p.5)

Two independent readings of the same printed page: **my OpenCode-vision transcription**
(`sources/processed/page-05_vision-ocr.md`) and **Internet Archive's machine OCR**
(`ocr/chineseandtheir01meadgoog.txt`, the `_djvu.txt`). The page image is the arbiter.

## Differences found

| Printed (image) | Machine OCR (IA) | Vision (from image) | Verdict |
|---|---|---|---|
| page number **5** | `POLITICAL GEOGRAPHY. 6` | page number **5** | IA mislabels the page number (5→6) |
| "colonists, exercise" | "colonists^ exercise" | "colonists, exercise" | IA rendered comma as caret `^` |
| "space, as" | "space^ as" | "space, as" | IA rendered comma as caret `^` |
| "more exact, all" | "more exacts all" | "more exact, all" | IA read comma as `s` |
| "four provinces" | "fbur provinces" | "four provinces" | IA letter confusion (o→b) |
| "They have" | "Th^y have" | "They have" | IA lost the `e` (→ caret) |
| "settlers, who" | "settlers^ who" | "settlers, who" | IA rendered comma as caret `^` |

## What this shows

- Internet Archive's machine OCR of this Google-digitised volume is broadly readable but drops
  punctuation (comma → `^`) and makes letter substitutions (`fbur` for "four", `Th^y` for "They"),
  and it even reports the wrong printed page number (6 instead of 5).
- None of these errors changes the *sense* of this passage, but they show why the OCR text must be
  checked against the page image. On a name or a date such errors would be serious.
- The vision reading, checked against the visible page, reproduces the printed text faithfully,
  including the printed page number 5 that the machine OCR got wrong.

## Consequence for the research claim

Both readings agree on the sentence that matters for the question:
> "The province of Kwangse, in which the present religious movement took its rise, contains the most of these …"

Because the two independent readings agree on this sentence, I treat it as reliable evidence that
Meadows (1856) located the movement's origin in **Kwangse (Guangxi)**.

## Remaining uncertainty

- Meadows gives the **province** (Guangxi). The precise village (Jintian, Guiping county) comes from
  the secondary source; see `sources/README_sources.md`.
- A further Meadows passage names "Thistle mount in the Kwei ping district" (Guiping county). It is
  visible in the machine text but I have not yet located and checked the page image for it — logged
  in `questions.md`.
