# 太平天国 / 金田起义 — Week 2 project

Research question: **Where (and when) did the Taiping movement first break out as an armed
uprising?** Answer: **金田村, 桂平县, 广西 (Jintian village, Guiping, Guangxi), 11 January 1851**
(the 金田起义 / Jintian Uprising).

## Layout

```
sources/
  raw/        original source scans, unchanged (meadows_n77.jpg = printed p.5, etc.)
  processed/  OCR text produced from the scans
  README_sources.md     provenance + reliability of each source
ocr/
  llm_ocr.py              LLM API OCR script (OpenRouter / DeepSeek) — method 1, needs a key
  README_ocr_methods.md   what was tried, in order, and what happened
  ocr_results_comparison.md  vision OCR vs Internet Archive machine OCR
  chineseandtheir01meadgoog.txt  IA machine text (for comparison)
questions.md              unresolved questions
```

Related assignment deliverable: `../../assignments/week-02/answer-taiping.md`.

## Where things stand

- Two sources: 中国国家博物馆 (secondary, precise place) + Meadows 1856 p.5 (contemporary, OCR'd).
- OCR done via the allowed last-resort method (OpenCode vision); method 1 had no key, method 2
  (PaddleOCR) has no Python 3.14 wheels.
- OCR output verified against the scan and against IA's machine OCR (which had comma/letter errors
  and a wrong page number).
