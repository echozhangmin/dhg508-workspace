# Answer — 太平天国运动最开始爆发的地方

**Question (pre-1950):** 太平天国运动最开始爆发的地方（和时间）在哪里？
*Where (and when) did the Taiping movement first break out as an armed uprising?*

**Answer (short):** The armed uprising first broke out at **金田村 (Jintian village), 桂平县
(Guiping county), 广西 (Guangxi province)** — today 广西贵港市桂平市金田镇 — on **11 January 1851
(清道光三十年十二月初十日)**, when Hong Xiuquan's God Worshipping Society rose in revolt and
proclaimed the Taiping Heavenly Kingdom (建号太平天国). This is the **金田起义 (Jintian Uprising)**.

Distinguish carefully (this is where "爆发" can mislead): the **God Worshipping Society (拜上帝会)**
was founded in **广东花县**, Hong's home district, in 1843; members were ordered to assemble at
**金田村** from July 1850 (团营); but the **armed uprising / outbreak** is Jintian, 11 Jan 1851.

## Evidence 1 — secondary (no OCR) — 中国国家博物馆, "金田起义"

> "1851年1月11日（道光三十年十二月十日），洪秀全和杨秀清、肖朝贵、冯云山、韦昌辉、石达开等人率众约
> 两万人在**广西桂平金田村**发动武装起义，建号太平天国。"
> https://www.chnmuseum.cn/zp/zpml/ysp/202012/t20201214_248369.shtml

Why reliable: a national museum's institutional account of the event; the Jintian site is a
protected national heritage site. Corroborated by Britannica ("formed among the impoverished
peasants of Guangxi province … he led them in rebellion"). It is secondary, so it is paired with
the contemporary source below.

## Evidence 2 — OCR'd contemporary source — Meadows (1856), p. 5

> "The province of Kwangse, in which the present religious movement took its rise, contains the
> most of these …"

- Thomas Taylor Meadows, *The Chinese and Their Rebellions* (London: Smith, Elder, 1856), printed
  p. 5. Public domain.
- OCR'd from the scan `sources/raw/meadows_n77.jpg` (leaf n77) → text in
  `sources/processed/page-05_vision-ocr.md`; comparison with IA machine OCR in
  `ocr/ocr_results_comparison.md`.

Why reliable: a contemporary (1856) account by a British consular interpreter in China, close to
the events; one of the foundational Western sources on the movement. Caveat: a British-imperial
vantage point; it names the **province** (Kwangse = Guangxi), not the village.

## Evidence 3 (added) — 第一手史料证明 1851 年

**See `projects/taiping-jintian/date-evidence-1851.md`** (full argument). In brief:

1. 《欽定剿平粵匪方略》卷首目錄 (Qing official compilation, 御制序 dated 同治十一年 = 1872): its
   own first 目录 page records **卷一至卷五 = 道光三十年五月庚戌至咸豐元年六月乙亥**, i.e. the
   official record brackets the uprising between 1850 and **咸豐元年 = 1851**. OCR'd from the scan
   (`sources/processed/qingfanglue-mulu_vision-ocr.md`).
2. A Qing memorial printed in the *Peking Gazette* (京报), quoted in Meadows (1856) p.155: "the Tae
   pings left their camp at **Kin teen** [金田] on the **4th March, 1851**." OCR'd
   (`sources/processed/page-155_vision-ocr.md`).
3. The Taipings' own era name **辛开元年 = 1851**.

Calendar rigour: 十二月初十日 = **1851年1月11日** 公历; by Qing reckoning it was still
**道光三十年**, because 咸豐元年正月 begins ~1851-02. So "1851" is correct on the Gregorian
calendar, and the official records straddle both 道光三十年 (1850 mobilisation) and 咸豐元年 (1851
suppression campaigns).

## How the OCR was done (one source needed OCR)

Tried the prescribed order (see `ocr/README_ocr_methods.md`):

1. **LLM API (OpenRouter/DeepSeek): not run** — no API key in this environment; ready-to-run
   `ocr/llm_ocr.py` provided.
2. **PaddleOCR: blocked** — `paddlepaddle` has no wheel for Python 3.14 (verified); no tesseract,
   no Docker.
3. **OpenCode vision (allowed last resort): used** — read the page scan and transcribed it.

**Verification:** the vision transcription was checked against the visible page and against Internet
Archive's machine OCR of the same page, which drops commas (→ `^`) and makes letter substitutions
(`fbur` for "four", `Th^y` for "They") and mislabels the printed page number (5→6). Both readings
agree on the sentence that matters, so the evidence is treated as reliable.

## Why the evidence supports the answer

- Evidence 2 (contemporary, OCR'd) independently establishes that the movement "took its rise" in
  **Kwangse / Guangxi**.
- Evidence 1 (institutional secondary) fixes the precise place and date: **金田村, 桂平县, 广西，
  1851年1月11日**.
- Together they locate the **first outbreak** at Jintian, Guiping, Guangxi, on 11 Jan 1851 — and
  they also let us separate the *organisation* (拜上帝会, 广东花县, 1843) from the *outbreak*.

## Bring-to-class ready

1. Question & answer — above.
2. Evidence: 中国国家博物馆 (secondary, precise place) + Meadows 1856 p.5 (contemporary, OCR'd).
3. OCR: vision method on the scan; original and OCR result; errors found in the machine OCR;
   unresolved: the Meadows "Kwei-ping district / Thistle mount" page still to be checked.
