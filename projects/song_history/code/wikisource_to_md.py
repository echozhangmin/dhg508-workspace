#!/usr/bin/env python3
"""Convert Wikisource wikitext (cached) to markdown for song_history project.

Usage: python3 wikisource_to_md.py <cache_dir> <titles_file> <output_dir>
Each line of titles_file: <wiki title>\t<output relative path>\t<display title>\t<note type>
Note type: punct (punctuated transcription) or sku (四庫全書 scan transcription).
"""
import json
import os
import re
import sys
import urllib.parse

TODAY = "2026-11-10"
WS_URL = "https://zh.wikisource.org/wiki/"

DROP_TEMPLATES = {
    "novel", "header", "skqs header", "skqs footer", "footer", "pd-old", "pd",
    "textquality", "search", "检索", "wikipedia", "sk list", "transclude pages",
    "pagequality", "left-right", "gap", "annotate link", "dl",
}


def safe_name(title):
    return title.replace("/", "__").replace(" ", "_")


def find_matching(text, i):
    """i points at '{{'; return index just past the matching '}}'."""
    depth, j = 0, i
    while j < len(text):
        if text.startswith("{{", j):
            depth += 1
            j += 2
        elif text.startswith("}}", j):
            depth -= 1
            j += 2
            if depth == 0:
                return j
        else:
            j += 1
    return -1


def split_args(s):
    """Split template body on top-level pipes, respecting nested {{ }} and [[ ]]."""
    parts, cur, tdepth, ldepth = [], [], 0, 0
    i = 0
    while i < len(s):
        if s.startswith("{{", i):
            tdepth += 1
            cur.append("{{")
            i += 2
        elif s.startswith("}}", i):
            tdepth -= 1
            cur.append("}}")
            i += 2
        elif s.startswith("[[", i):
            ldepth += 1
            cur.append("[[")
            i += 2
        elif s.startswith("]]", i):
            ldepth -= 1
            cur.append("]]")
            i += 2
        elif s[i] == "|" and tdepth == 0 and ldepth == 0:
            parts.append("".join(cur))
            cur = []
            i += 1
        else:
            cur.append(s[i])
            i += 1
    parts.append("".join(cur))
    return parts


def expand_templates(text):
    while True:
        i = text.find("{{")
        if i < 0:
            return text
        end = find_matching(text, i)
        if end < 0:
            text = text[:i] + text[i + 2:]
            continue
        inner = text[i + 2:end - 2]
        parts = split_args(inner)
        name = parts[0].strip().lower()
        args = parts[1:]
        if name in DROP_TEMPLATES:
            repl = ""
        elif name == "annotate":
            repl = "（%s）" % expand_templates(args[0]).strip() if args else ""
        elif name == "sk notes":
            repl = "（%s）" % expand_templates(args[0]).strip() if args else ""
        elif name in ("skchar",):
            repl = "□"
        elif name.startswith("gap"):
            repl = ""
        elif name in ("propernoun", "proper noun", "yl", "sk", "sk anchor", "pua"):
            repl = expand_templates(args[0]) if args else ""
        else:
            repl = expand_templates(args[0]) if args else ""
        text = text[:i] + repl + text[end:]


def strip_links(text):
    def repl(m):
        inner = m.group(1)
        return inner.split("|")[-1].strip()
    return re.sub(r"\[\[([^\[\]]+)\]\]", repl, text)


def convert_page(wikitext):
    t = re.sub(r"<!--.*?-->", "", wikitext, flags=re.S)
    t = re.sub(r"<noinclude>.*?</noinclude>", "", t, flags=re.S)
    t = t.replace("<onlyinclude>", "").replace("</onlyinclude>", "")
    t = re.sub(r"==\s*全覽\s*==\n(?:\*[^\n]*\n?\n?)+", "", t)
    t = expand_templates(t)
    t = re.sub(r"\[\[Category:[^\]]+\]\]", "", t)
    t = re.sub(r"\[\[Wikisource:[^\]]+\]\]", "", t)
    t = strip_links(t)
    t = re.sub(r"-\{([^{}]*)\}-", r"\1", t)
    t = t.replace("'''", "").replace("''", "")
    t = re.sub(r"<ref[^>]*/>", "", t)
    t = re.sub(r"<ref[^>]*>(.*?)</ref>", r"〔校：\1〕", t, flags=re.S)
    t = re.sub(r"</?poem[^>]*/?>", "", t)
    t = re.sub(r"</?br\s*/?>", "\n", t)
    t = re.sub(r"</?[a-zA-Z][^>]*>", "", t)
    t = re.sub(r"^(={2,6})\s*(.*?)\s*\1\s*$",
               lambda m: "#" * len(m.group(1)) + " " + m.group(2).strip(),
               t, flags=re.M)
    lines = [ln.strip(" \t\u3000") for ln in t.split("\n")]
    paras = [ln for ln in lines if ln]
    return "\n\n".join(paras)


def extract_header_notes(wikitext):
    """Extract notes= named arg from the {{Header}}/{{header}} template."""
    m = re.search(r"\{\{[Hh]eader\b", wikitext)
    if not m:
        return ""
    end = find_matching(wikitext, m.start())
    if end < 0:
        return ""
    parts = split_args(wikitext[m.start() + 2:end - 2])
    for p in parts[1:]:
        if p.strip().startswith("notes"):
            val = p.split("=", 1)[1] if "=" in p else ""
            return val.strip()
    return ""


NOTES = {
    "punct": "> 體例：朱熹集注等小字注以（）標示；〔校：…〕為維基文庫校勘注；□為無法顯示之字。",
    "sku": "> 體例：四庫全書掃描錄文，無標點；（）為小字注或出處注；□為掃描本造字（維基文庫 PUA 字符）。",
}


def make_md(title, display, body, note_type):
    url = WS_URL + urllib.parse.quote(title.replace(" ", "_"), safe="/:")
    header = f"# {display}\n\n"
    src = (f"> 來源：[維基文庫「{title}」]({url}) · 取用 {TODAY} · "
           f"[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)\n")
    note = NOTES[note_type]
    return header + src + note + "\n\n---\n\n" + body.strip() + "\n"


def main(cache_dir, titles_file, out_dir):
    count = 0
    for line in open(titles_file):
        line = line.rstrip("\n")
        if not line:
            continue
        title, rel, display, ntype = line.split("\t")
        path = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        src = os.path.join(cache_dir, safe_name(title) + ".wikitext")
        body = convert_page(open(src).read())
        with open(path, "w") as f:
            f.write(make_md(title, display, body, ntype))
        count += 1
        print("wrote", rel)
    print(count, "files")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
