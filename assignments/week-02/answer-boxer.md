# Answer — 义和团运动爆发的原因 / Causes of the Boxer Movement

**Question (pre-1950):** 义和团运动为什么在 1898–1900 年在华北（山东、直隶）迅速兴起？
*Why did the Yihetuan (Boxer) movement arise and spread so rapidly in North China, 1898–1900?*

**Answer (short):** The movement grew out of a convergence of two pressures, with a third enabling
condition supplied by the Qing court. First, an **ecological and economic crisis**: the 1898 Yellow
River flood followed by the 1899–1900 drought and locusts, on top of the collapse of northern
Shandong's cotton economy against imported foreign cotton and the decline of Grand Canal trade.
Second, a **foreign presence that the population blamed for that crisis**: the post-1895 "scramble
for concessions" (Germany's occupation of Jiaozhou Bay after the 1897 deaths of two missionaries,
German railroads and telegraphs that tore up burial grounds and were defended with gunfire), and
above all the missionaries, whose converts were protected by officials and whose churches peasants
believed were "blocking the sky [and] stopping the rain." A third, enabling factor: the Qing court's
indecision between suppressing and appeasing the Boxers (the 剿抚 debate — Yuan Shikai vs. Yuxian)
allowed the movement a semi-official status and let it spread from Shandong into Zhili and Beijing.

## Evidence 1 — secondary (no OCR) — Britannica, "Boxer Rebellion"

> "In the late 19th century, because of growing economic impoverishment, a series of unfortunate
> natural calamities, and unbridled foreign aggression in the area, the Boxers began to increase
> their strength in the provinces of North China." — plus "Christian missionary activities helped
> provoke the Boxers."
> https://www.britannica.com/event/Boxer-Rebellion

Why reliable: authoritative reference encyclopedia synthesising modern scholarship.
Why *not* sufficient alone: it is a tertiary summary. It frames the causes; it does not by itself
prove them, so it is paired with the contemporary study below (as the assignment requires —
"evaluate the evidence, not just the website").

## Evidence 2 — OCR'd primary/contemporary source — Clements (1915), p. 39

> "The Powers, in their mad scramble for land, did not take into account the rights of the Chinese …
> the united opinion of Europe was that China would soon disappear as a sovereign entity,
> dismembered and divided … the European demands had been comparatively easy of realization.
> Besides acquisitions of territory, there were numberless other demands … consisting mainly of
> religious and commercial concessions, railway grants, and heavy indemnities."

- Paul H. Clements, *The Boxer Rebellion: A Political and Diplomatic Review* (Columbia University,
  1915), "Causes of the Rebellion," printed p. 39. Public domain.
- OCR'd from the scan `sources/raw/ia_42.jpg` (leaf n42) → text in
  `sources/processed/page-39_vision-ocr.md`; comparison with IA retro-OCR in
  `ocr/ocr_results_comparison.md`.

Why reliable: Columbia University Press scholarly series; author a Columbia Fellow in
International Law; written close to the events (1915) and grounded in the published US diplomatic
record (he cites *U.S. Foreign Relations* and **China No. 1 / China No. 3**). Caveat: a 1915
American "scramble-for-concessions" interpretation; paired with Evidence 1 it gives the
economic/ecological dimension as well.

## How the OCR was done (one source needed OCR)

Tried the prescribed order (see `ocr/README_ocr_methods.md`):

1. **LLM API (OpenRouter/DeepSeek): not run** — no API key in this environment. A ready-to-run
   script `ocr/llm_ocr.py` is prepared (reads key from env; no key stored in Git).
2. **PaddleOCR: blocked** — `paddlepaddle` has no wheel for Python 3.14 (verified:
   "No matching distribution found for paddlepaddle"); no tesseract, no Docker.
3. **OpenCode vision (allowed last resort): used.** Read the page scan directly and transcribed it.

**Verification:** the vision transcription matches the visible page; compared to Internet Archive's
retro-OCR of the same page, which contains character-substitution errors ("loreign" for "foreign",
"poHcy" for "policy", "indernnjties" for "indemnities"). Both independent readings agree on the
substance, so I treat the passage as reliable for the claim.

## Why the evidence supports the answer

- Evidence 2 proves the existence and intensity of the **foreign-aggression / concession** cause in
  the words of a contemporary scholar using diplomatic records ("mad scramble for land", "religious
  and commercial concessions", "heavy indemnities").
- Evidence 1 independently names the **ecological and missionary** causes that Evidence 2 under-
  emphasises ("economic impoverishment, natural calamities … foreign aggression"; "missionary
  activities helped provoke the Boxers").
- Together, and reinforcing the placard text quoted in `sources/README_sources.md`, they show the
  uprising as the convergence of economic hardship, imperialist pressure, and a foreign religious
  presence that the population held responsible for the hardship.

## Bring-to-class ready

1. Question & answer — see above.
2. Evidence: Britannica (secondary) + Clements 1915 p.39 (primary/contemporary; OCR'd).
3. OCR: vision method on the scan; original and OCR result; errors found in the machine OCR;
   unresolved: the footnote "7" text, and the placard text still needs verification.
