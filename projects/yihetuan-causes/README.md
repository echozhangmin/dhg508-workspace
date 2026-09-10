# 义和团运动爆发的原因 — Week 2 project

Research question: **Why did the Yihetuan (Boxer) movement arise and spread so rapidly in North
China, 1898–1900?** (义和团运动为什么在 1898–1900 年在华北迅速兴起?)

Supersedes the broad "Causes of the Boxer Rebellion" into an answerable claim about the emergence
in Shandong/Zhili, answerable with two independent pieces of evidence, one of which is OCR'd.

## Layout

```
sources/
  raw/            original source scans, unchanged (IA leaf n42 = printed p.39, etc.)
  processed/      OCR text produced from the scans
  README_sources.md   provenance + reliability of each source
ocr/
  llm_ocr.py      LLM API OCR script (OpenRouter / DeepSeek) — method 1, needs a key
  README_ocr_methods.md   what was tried, in order, and what happened
  ocr_results_comparison.md  vision OCR vs Internet Archive retro-OCR
  fulltext.txt    IA retro-OCR full text (for comparison)
questions.md      unresolved questions
```

Related assignment deliverable: `../../assignments/week-02/answer.md`.

## Where things stand

- Two sources identified (anonymous comment: Britannica + Clements 1915 p.39).
- OCR done via the allowed last-resort method (OpenCode vision) because method 1 had no key and
  method 2 (PaddleOCR) has no Python 3.14 wheels.
- OCR output verified against the scan and compared against IA's machine OCR.
- To push: keep the scans in `sources/raw/`, the transcriptions in `sources/processed/`, and
  leave API keys out of Git.
