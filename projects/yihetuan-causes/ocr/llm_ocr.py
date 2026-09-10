#!/usr/bin/env python3
"""LLM-based OCR via OpenRouter or DeepSeek (multimodal image input).

This is method #1 in the Week 2 hierarchy (LLM API first). It is ready to run but
needs an API key. No key was present in this environment, so we fell back to
method #3 (OpenCode vision); see `README_ocr_methods.md`.

Usage:
    export OPENROUTER_API_KEY=sk-...      # OR
    export DEEPSEEK_API_KEY=sk-...

    python3 llm_ocr.py --image ../sources/raw/ia_42.jpg \
        --provider openrouter --model google/gemini-2.0-flash \
        --prompt "Transcribe all visible text, preserving line breaks. Do not correct the text."

Notes:
    - Model must accept images. OpenRouter multimodal guide:
      https://openrouter.ai/docs/guides/overview/multimodal/image-understanding
    - DeepSeek vision guide: https://api-docs.deepseek.com/guides/vision/
    - No keys are stored in this repo.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request


def read_image_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def build_request(body: dict, key: str) -> urllib.request.Request:
    req = urllib.request.Request(
        body["url"],
        data=json.dumps(body["payload"]).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    return req


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--provider", choices=["openrouter", "deepseek"], default="openrouter")
    ap.add_argument("--model", default="google/gemini-2.0-flash")
    ap.add_argument("--prompt", default="Transcribe all visible printed text exactly, preserving line breaks.")
    args = ap.parse_args()

    if args.provider == "openrouter":
        key = os.environ.get("OPENROUTER_API_KEY")
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = args.model
    else:
        key = os.environ.get("DEEPSEEK_API_KEY")
        url = "https://api.deepseek.com/chat/completions"
        model = args.model

    if not key:
        print("ERROR: missing API key. Set OPENROUTER_API_KEY or DEEPSEEK_API_KEY.", file=sys.stderr)
        return 1

    data_uri = "data:image/jpeg;base64," + read_image_b64(args.image)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": args.prompt},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ],
    }

    body = {"url": url, "payload": payload}
    try:
        with urllib.request.urlopen(build_request(body, key), timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        return 2
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}", file=sys.stderr)
        return 3

    try:
        print(data["choices"][0]["message"]["content"])
    except (KeyError, IndexError):
        print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
