#!/usr/bin/env python3
"""Build all markdown files for song_history from the wikisource cache."""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wikisource_to_md import (convert_page, extract_header_notes, make_md,
                              safe_name)

CACHE = "/tmp/opencode/ws_cache"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "sources", "raw")


def read_wiki(title):
    with open(os.path.join(CACHE, safe_name(title) + ".wikitext")) as f:
        return f.read()


def write(rel, display, body, ntype, title_for_url):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(make_md(title_for_url, display, body, ntype))
    print("wrote", rel)


def sec_lines(page_title, sections):
    """Extract named sections from a ProofreadPage djvu page as line lists."""
    t = read_wiki(page_title)
    out = []
    for sec in sections:
        m = re.search(r'<section begin="%s"\s*/>(.*?)<section end="%s"\s*/>'
                      % (sec, sec), t, flags=re.S)
        if not m:
            raise RuntimeError(f"section {sec} not found in {page_title}")
        out += m.group(1).replace("<br>", "\n").split("\n")
    return out


def sku_body(lines, drop_prefixes=(), drop_equals=()):
    """Turn djvu column lines into flowing 四庫 text: drop furniture, join
    consecutive content lines, keep signature lines as their own paragraphs."""
    paras, buf = [], []
    for ln in lines:
        s = convert_page(ln).strip()
        if not s:
            continue
        if any(s.startswith(p) for p in drop_prefixes) or s in drop_equals:
            continue
        if s.startswith(("總纂官", "總校官")):
            if buf:
                paras.append("".join(buf))
                buf = []
            paras.append(s)
            continue
        buf.append(s)
    if buf:
        paras.append("".join(buf))
    return "\n\n".join(paras)


# ---- 1. 四書章句集註: combined files & 提要 -------------------------------
W = "四書章句集註"
write(f"{W}/大學章句.md", "大學章句（含序）",
      "## 大學章句序\n\n" + convert_page(read_wiki(f"{W}/大學章句序")).strip()
      + "\n\n## 大學章句\n\n" + convert_page(read_wiki(f"{W}/大學章句")).strip(),
      "punct", f"{W}/大學章句")

write(f"{W}/中庸章句.md", "中庸章句（含序）",
      "## 中庸章句序\n\n" + convert_page(read_wiki(f"{W}/中庸章句序")).strip()
      + "\n\n## 中庸章句\n\n" + convert_page(read_wiki(f"{W}/中庸章句")).strip(),
      "punct", f"{W}/中庸章句")

write(f"{W}/論語序說.md", "論語序說（含讀論語孟子法）",
      "## 論語序說\n\n" + convert_page(read_wiki(f"{W}/論語序說")).strip()
      + "\n\n## 讀論語孟子法\n\n" + convert_page(read_wiki(f"{W}/讀論語孟子法")).strip(),
      "punct", f"{W}/論語序說")

write(f"{W}/附考.md", "附考（四書章句附考序·定本辨）",
      "## 四書章句附考序\n\n" + convert_page(read_wiki(f"{W}/四書章句附考序")).strip()
      + "\n\n## 四書章句集註定本辨\n\n" + convert_page(read_wiki(f"{W}/四書章句集註定本辨")).strip(),
      "punct", f"{W}/四書章句附考序")

write(f"{W}/提要（四庫總目）.md", "四書章句集註·提要（四庫總目）",
      convert_page(extract_header_notes(read_wiki(W))), "punct", W)

# ---- 2. 二程集 component 提要 (from Header notes of main pages) -----------
for main, comp in [("二程遺書", "河南程氏遺書"), ("二程外書", "河南程氏外書"),
                   ("二程粹言", "河南程氏粹言")]:
    write(f"二程集/{comp}/提要（四庫總目）.md", f"{comp}·提要（四庫總目）",
          convert_page(extract_header_notes(read_wiki(main))), "punct", main)

# ---- 3. per-juan manifest files -------------------------------------------
subprocess.run([sys.executable,
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "wikisource_to_md.py"),
                CACHE, "/tmp/opencode/manifest4.tsv", OUT], check=True)

# ---- 4. 易傳 序與提要 (from djvu proofread pages) ---------------------------
write("二程集/周易程氏傳/伊川易傳序.md", "伊川易傳序（四庫本）",
      sku_body(sec_lines("Page:文淵閣四庫全書_0009冊.djvu/162", ["葉628a", "葉628b"]),
               drop_equals=("伊川易傳序",)),
      "sku", "Page:文淵閣四庫全書_0009冊.djvu/162")

write("二程集/周易程氏傳/四庫提要.md", "周易程氏傳（伊川易傳）·四庫提要",
      "## 提要\n\n" + sku_body(sec_lines("Page:文淵閣四庫全書_0009冊.djvu/161",
                                          ["葉624a", "葉624b", "葉625a", "葉625b"]),
                                    drop_prefixes=("欽定四庫全書", "伊川易傳"),
                                    drop_equals=("提要",)),
      "sku", "Page:文淵閣四庫全書_0009冊.djvu/161")


# ---- 5. 合訂本 -------------------------------------------------------------
def demote(body):
    return re.sub(r"^(#{1,5}) ", lambda m: m.group(1) + "# ", body, flags=re.M)


def book_md(intro, parts):
    """parts: list of (heading, list of (subheading, body))."""
    out = [intro.strip(), "", "---", ""]
    for h, subs in parts:
        out.append(f"## {h}")
        out.append("")
        for sub, body in subs:
            if sub:
                out.append(f"### {sub}")
                out.append("")
            out.append(demote(body.strip()))
            out.append("")
    return "\n".join(out).rstrip() + "\n"


W = "四書章句集註"
sishu_intro = ("朱熹撰，南宋淳熙年間成書。文本轉錄自[維基文庫]"
               "(https://zh.wikisource.org/wiki/四書章句集註)（[CC BY-SA 4.0]"
               "(https://creativecommons.org/licenses/by-sa/4.0/)），取用日期 2026-11-10。"
               "朱熹集注等小字注以（）標示；〔校：…〕為維基文庫校勘注。")
sishu_parts = [
    ("提要（四庫總目）", [("", convert_page(extract_header_notes(read_wiki(W))))]),
    ("大學章句", [("大學章句序", convert_page(read_wiki(f"{W}/大學章句序"))),
                 ("大學章句", convert_page(read_wiki(f"{W}/大學章句")))]),
    ("中庸章句", [("中庸章句序", convert_page(read_wiki(f"{W}/中庸章句序"))),
                 ("中庸章句", convert_page(read_wiki(f"{W}/中庸章句")))]),
    ("論語集注", [("論語序說", convert_page(read_wiki(f"{W}/論語序說"))),
                 ("讀論語孟子法", convert_page(read_wiki(f"{W}/讀論語孟子法")))] +
                [(f"論語集注卷{c}", convert_page(read_wiki(f"{W}/論語集注卷{c}")))
                 for c in "一二三四五六七八九十"]),
    ("孟子集注", [("孟子序說", convert_page(read_wiki(f"{W}/孟子序說")))] +
                [(f"孟子集注卷{c}", convert_page(read_wiki(f"{W}/孟子集注卷{c}")))
                 for c in list("一二三四五六七八九十") + [f"十{x}" for x in "一二三四"]]),
    ("附錄", [("四書章句附考序", convert_page(read_wiki(f"{W}/四書章句附考序"))),
              ("四書章句集註定本辨", convert_page(read_wiki(f"{W}/四書章句集註定本辨")))]),
]
write(f"{W}/{W}.md", W + "（合訂本）", book_md(sishu_intro, sishu_parts), "punct", W)

EC = "二程集"
ercheng_intro = ("程顥、程頤著述總集（對應中華書局點校本《二程集》諸成分），文本轉錄自[維基文庫]"
                 "(https://zh.wikisource.org/wiki/二程全書)（[CC BY-SA 4.0]"
                 "(https://creativecommons.org/licenses/by-sa/4.0/)），取用日期 2026-11-10。"
                 "遺書、外書、粹言、易傳取自維基文庫標點錄排版；文集、經說、易傳序及各提要取自"
                 "四庫全書掃描錄文（無標點，（）為小字注，□為掃描造字）。")
ercheng_parts = [
    ("河南程氏遺書",
     [("提要（四庫總目）", convert_page(extract_header_notes(read_wiki("二程遺書"))))] +
     [(f"卷{i:02d}", convert_page(read_wiki(f"二程遺書/卷{i:02d}"))) for i in range(1, 26)] +
     [("附錄（四庫本）", convert_page(read_wiki("二程遺書 (四庫全書本)/附録")))]),
    ("河南程氏外書",
     [("提要（四庫總目）", convert_page(extract_header_notes(read_wiki("二程外書"))))] +
     [(f"卷{i:02d}", convert_page(read_wiki(f"二程外書/卷{i:02d}"))) for i in range(1, 13)]),
    ("河南程氏粹言",
     [("提要（四庫總目）", convert_page(extract_header_notes(read_wiki("二程粹言"))))] +
     [(f"卷{c}", convert_page(read_wiki(f"二程粹言/卷{c}"))) for c in "一二"]),
    ("河南程氏文集（四庫本）",
     [("四庫提要", convert_page(read_wiki("二程文集 (四庫全書本)")))] +
     [(f"卷{i:02d}", convert_page(read_wiki(f"二程文集 (四庫全書本)/卷{i:02d}"))) for i in range(1, 14)] +
     [("附錄上", convert_page(read_wiki("二程文集 (四庫全書本)/卷上"))),
      ("附錄下", convert_page(read_wiki("二程文集 (四庫全書本)/卷下")))]),
    ("周易程氏傳",
     [("四庫提要", "## 提要\n\n" + sku_body(sec_lines("Page:文淵閣四庫全書_0009冊.djvu/161",
                                                      ["葉624a", "葉624b", "葉625a", "葉625b"]),
                                                drop_prefixes=("欽定四庫全書", "伊川易傳"),
                                                drop_equals=("提要",))),
      ("伊川易傳序", sku_body(sec_lines("Page:文淵閣四庫全書_0009冊.djvu/162", ["葉628a", "葉628b"]),
                              drop_equals=("伊川易傳序",))),
      ("周易程氏傳（卷一至卷四）", convert_page(read_wiki("伊川易傳")))]),
    ("河南程氏經說（四庫本）",
     [("四庫提要", convert_page(read_wiki("程氏經説 (四庫全書本)")))] +
     [(f"卷{i}", convert_page(read_wiki(f"程氏經説 (四庫全書本)/卷{i}"))) for i in range(1, 8)]),
]
write(f"{EC}/{EC}.md", EC + "（合訂本）", book_md(ercheng_intro, ercheng_parts), "punct", "二程全書")
print("ALL DONE")
