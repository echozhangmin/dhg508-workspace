# OCR result — 《欽定剿平粵匪方略》卷首·目錄 (FIRST-HAND Qing official source)

**Method:** OpenCode vision. Machine OCR of this woodblock volume is unusable (see below).
**Input scan:** `sources/raw/qingfanglue_mulu_leaf30.jpg` (first page of 目錄).
**Item:** Internet Archive `02080988.cn` — 欽定剿平粵匪方略(一), 北京大學圖書館藏本.
**Provenance:** 御制序 (leaf n12) ends "同治十有一年歲次壬申季秋月吉" = **autumn 1872** ( imperial brush, 御筆); compiled by 奕訢 et al.

## Transcription (right-to-left woodblock layout)

```
欽定剿平粵匪方略目錄   [卷首]

聖製一卷

卷一至卷五：道光三十年五月庚戌 至 咸豐元年六月乙亥

卷六至卷十：……亥（接次頁）
```

<span style="opacity:.7">*Binding-edge marginal title (OCR-noisy): 剿平粵匪方略目録.*</span>

## Why this matters for the 1851 date

The Qing court's official war chronicle organises all 255 volumes by date. Its own first pages of
the **目錄** state that **卷一至卷五 covers 道光三十年五月庚戌 → 咸豐元年六月乙亥** — i.e. **June 1850
through June 1851 (咸豐元年 = 1851)**. The 金田 events (道光三十年十二月 = Jan 1851 Gregorian) must
therefore fall inside this range: the official record itself brackets the uprising within
1850–1851, and uses 咸豐元年 for 1851.

## OCR notes

- IA's tesseract `_djvu.txt` of the scan is unrecoverable noise; its Chinese chOCR contains **zero**
  hits for 金田/桂平/洪秀全/咸豐元年/道光三十年/粵匪 (grep-verified). Reading required vision.
- Follow-ups logged in `questions.md`: the actual memorials of 卷一–卷五 are in the sibling items
  (卷二 = `02080989.cn`, 卷三 = `02080990.cn`); this volume contains 卷首+目錄.
