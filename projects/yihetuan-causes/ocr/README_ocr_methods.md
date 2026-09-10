# OCR methods tried (Week 2 hierarchy) — 义和团运动爆发的原因

Assignment order: **(1) LLM API → (2) PaddleOCR → (3) OpenCode vision**. You only keep
going if the previous method fails or is unusable. Record of what actually happened here.

## Machine / environment (checked 2026-09-10)

- macOS (darwin), zsh
- Python 3.14.7, pip 26.2.1
- git 2.50.1; **no** `gh`, `node`, `docker`, `podman`, `tesseract`
- No `OPENROUTER_API_KEY` / `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` in the environment

## Method 1 — LLM API (OpenRouter / DeepSeek): not run (no key)

The official multimodal guides were used to write `llm_ocr.py`:

- OpenRouter image-understanding guide
- DeepSeek vision guide

**Result:** Could not run — no API key is present in this environment. The script reads the key
from the environment (`OPENROUTER_API_KEY` or `DEEPSEEK_API_KEY`) and performs the request with
urllib (no third-party dependency); it is ready to run once a key is supplied. A secret is never
stored in the repo.

## Method 2 — PaddleOCR: blocked by the environment

PaddleOCR depends on `paddlepaddle`. Attempted install and queried the package indices:

```
$ python3 -m pip index versions paddlepaddle
ERROR: No matching distribution found for paddlepaddle
$ python3 -m pip download --no-deps --dest /tmp/pptest paddlepaddle
ERROR: Could not find a version that satisfies the requirement paddlepaddle
ERROR: No matching distribution found for paddlepaddle
```

**Result:** `paddlepaddle` publishes no wheel for CPython 3.14 yet. There is also no `tesseract`
binary and no Docker/Podman, so there is no packaged OCR alternative available on this machine.
PaddleOCR is therefore unusable here without installing a Python 3.12 environment or an
image-based tool.

## Method 3 — OpenCode vision (last resort, allowed): used

**Result:** Read the page scan `sources/raw/ia_42.jpg` directly with OpenCode's vision and
produced `sources/processed/page-39_vision-ocr.md`. The transcription matches the visible page.

## Verification

The vision transcription was compared against Internet Archive's retro-OCR of the same page
(`ocr/fulltext.txt`, `_djvu.txt`). The retro-OCR contains character-substitution errors
(e.g. "loreign" for "foreign", "poHcy" for "policy", "indernnjties" for "indemnities") that the
vision reading and the page image both resolve. Logged in `ocr/ocr_results_comparison.md`.

**Conclusion:** Method 1 and 2 were blocked for environment reasons (no key; no compatible
PaddleOCR wheels), so the allowed method 3 was used, and the output was checked against the
original image. If a key is added later, `llm_ocr.py` re-runs the task, and the new result can be
compared to this one.

## Next check

- Obtain an OpenRouter or DeepSeek key and re-run method 1; compare to the vision reading.
- Install Python 3.12 to attempt PaddleOCR; compare character-accuracy on the same page.
