# OCR results comparison — page 39

Two independent readings of the same printed page were compared: **my OpenCode-vision
transcription** (`sources/processed/page-39_vision-ocr.md`) and **Internet Archive's retro-OCR**
(`ocr/fulltext.txt`, from `boxerrebellionpo66clemuoft_djvu.txt`). The image is the arbiter.

## Differences found

| Word (printed) | Retro-OCR (IA `_djvu.txt`) | Vision (from image) | Verdict |
|---|---|---|---|
| foreign | "loreign . influence" | "foreign influence" | IA error: letter confusion (f→l) + stray period |
| policy | "poHcy" | "policy" | IA error: cap-H artifact from old "li" ligature |
| indemnities | "indernnjties" | "indemnities" | IA error: substituted letters (nn→nj) |
| category. | "cate- gory." then "gory." | "category." | IA split/duplicated the word across lines |
| comity | "comity" | "comity" | agreement |

## What this shows

- Internet Archive's machine OCR is serviceable but produces character substitutions
  (f→l, p→H, nn→nj). None of these changes the meaning of this passage, but on names,
  numbers, or dates such substitutions would be serious.
- The vision transcription, read against the visible page, reproduces the printed text
  accurately; where the two readings disagreed, the page image resolves the question.

## Consequence for the research claim

For this passage both readings support the same reading: Clements attributes the rising
anti-foreign mood to the "mad scramble for land" and to demands consisting "mainly of
religious and commercial concessions, railway grants, and heavy indemnities." Because the
two readings are independent and agree, I treat the transcribed passage as reliable evidence.

## Remaining uncertainty

- The footnote marker "7" after "ethics." points to a citation note; the footnote text sits at
  the foot of the adjacent page and is not fully legible in this crop, so it was not checked.
- This is one 1915 American author's framing; it emphasizes the "scramble for concessions"
  interpretation of causation. It should be read alongside the ecological/missionary accounts
  quoted in `assignments/week-02/answer.md`.
