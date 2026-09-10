# OCR methods tried (Week 2 hierarchy) — 太平天国 / 金田起义

Assignment order: **(1) LLM API → (2) PaddleOCR → (3) OpenCode vision**. Record of what actually
happened on this machine.

## Environment (checked 2026-09-10)

- macOS (darwin), zsh; Python 3.14.7, pip 26.2.1
- No `tesseract`, no `docker`/`podman`; no `OPENROUTER_API_KEY` / `DEEPSEEK_API_KEY` in the env

## Method 1 — LLM API (OpenRouter / DeepSeek): attempted, blocked by an invalid key

`llm_ocr.py` (same script as the 义和团 project) implements the request for OpenRouter's
image-understanding endpoint or DeepSeek's vision endpoint, reading the key from the environment.
A DeepSeek key was later supplied (2026-09-10). A minimal text-only request against the official
endpoint (`api.deepseek.com/chat/completions`, model `deepseek-flash`) was rejected: 
`"Your api key: ****GRtE is invalid"`. The key's format (67 chars, `sk-` + 64 alphanumerics)
matches neither official DeepSeek nor OpenRouter keys, so it likely belongs to a third-party relay;
OpenRouter requests never reach its auth layer from this network (even intentionally fake keys
return the same 401), so that provider is unusable here. **Method 1 could not be checked in
production;** a working key is all that is needed to run `llm_ocr.py` (no secret is stored in the
repo).

## Method 2 — PaddleOCR: blocked by the environment

`paddlepaddle` (PaddleOCR's engine) publishes no wheel for CPython 3.14:

```
$ python3 -m pip index versions paddlepaddle
ERROR: No matching distribution found for paddlepaddle
```

No `tesseract` binary and no Docker/Podman are available either. PaddleOCR is unusable here without
a Python 3.12 environment or a container.

## Method 3 — OpenCode vision (last resort, allowed): used

Read the scan `sources/raw/meadows_n77.jpg` (Meadows 1856, printed p.5) with OpenCode's vision and
produced `sources/processed/page-05_vision-ocr.md`.

## Verification

Compared against Internet Archive's machine OCR of the same page and against the page image. The
machine OCR has comma/letter errors and mislabels the printed page number (5→6); the vision reading
resolves these against the image. See `ocr/ocr_results_comparison.md`.

**Conclusion:** methods 1 and 2 were blocked for environment reasons; the allowed method 3 was used
and checked against the original scan.
