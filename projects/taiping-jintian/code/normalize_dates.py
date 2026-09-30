#!/usr/bin/env python3
"""Regenerate data/date_conversions.json (the date-normalisation audit trail).

Two kinds of rows:
  * computed   — a lunar-qing date converted with sxtwl 2.0.7 and cross-checked
                 against lunar-python 1.4.8 (both must agree, else we stop).
  * per source — the source itself gives both forms, no computation.
  * not converted — a raw date was seen but no defensible normal form was made
                 (norm_date '').

Requires: sxtwl, lunar-python  (pip install sxtwl lunar-python)
The committed output is what build_db.py reads, so building the database needs
neither library.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
OUT = PROJECT / "data" / "date_conversions.json"

# (raw_date, from_calendar, norm_date, to_calendar, method, doc_id, locator, note)
# For computed rows, norm_date is filled in below; put None here.
ROWS = [
    ("道光三十年十二月初十日", "lunar-qing", None, "gregorian", "computed", "wiki-jintianqiyi", "经过", "金田起义；公历1851-01-11。", (1850, 12, 10, False)),
    ("咸丰六年八月初四日", "lunar-qing", None, "gregorian", "computed", "wiki-yangxiuqing", "首段", "杨秀清在天京事变中被杀之日。", (1856, 8, 4, False)),
    ("同治三年四月二十七日", "lunar-qing", None, "gregorian", "computed", "wiki-hongxiuquan", "首段", "洪秀全病逝之日。", (1864, 4, 27, False)),
    ("同治三年六月十六日", "lunar-qing", None, "gregorian", "computed", "en-taiping-rebellion", "lead", "天京陷落之日。", (1864, 6, 16, False)),
    ("咸丰元年（1851年）", "lunar-qing", "1851", "gregorian", "per source", "wiki-yongan", "经过", "清帝纪年：咸丰元年＝1851年。", None),
    ("道光三十年（1850年）", "lunar-qing", "1850", "gregorian", "per source", "wiki-jintianqiyi", "经过", "清帝纪年：道光三十年＝1850年（其十二月已入公历1851）。", None),
    ("咸丰元年十二月（永安建制）", "lunar-qing", "", "gregorian", "not converted", "wiki-yongan", "经过", "通行系于1851年12月，但该农历月起于公历1852-01-21，纪年与公历不重合，不强行归一。", None),
    ("约1820年（一说1826年）", "gregorian", "1820?", "gregorian", "per source", "wiki-xiaochaogui", "首段", "萧朝贵生年两说，保留存疑标记。", None),
    ("1823年或1826年", "gregorian", "1823?", "gregorian", "per source", "wiki-weichanghui", "首段", "韦昌辉生年两说，保留存疑标记。", None),
    ("1831年？", "gregorian", "1831?", "gregorian", "per source", "wiki-zengshuiyuan", "首段", "曾水源生年原文存疑。",None),
    ("1848年", "gregorian", "1848", "gregorian", "per source", "wiki-xiaochaogui", "生平", "天父/天兄下凡之年（本条未给月日）。", None),
    ("道光二十三年（1843年）", "lunar-qing", "1843", "gregorian", "per source", "wiki-jintianqiyi", "经过", "拜上帝会创立；原文并给年号与公历。", None),
    ("道光二十四年（1844年）春", "lunar-qing", "1844", "gregorian", "per source", "wiki-jintianqiyi", "经过", "紫荆山立会；原文并给年号与公历。", None),
    ("咸丰二年（1852年）", "lunar-qing", "1852", "gregorian", "per source", "wiki-wulantai", "生平", "永安突围之年。", None),
    ("咸丰六年（1856年）", "lunar-qing", "1856", "gregorian", "per source", "wiki-tianjingshibian", "首段", "天京事变之年。", None),
]

CHECK = "sxtwl 2.0.7 (＝lunar-python 1.4.8 cross-check)"


def main() -> int:
    import sxtwl  # noqa: PLC0415
    from lunar_python import Lunar  # noqa: PLC0415

    out = []
    for i, (raw, frm, norm, to, method, doc, loc, note, lunar) in enumerate(ROWS, start=1):
        if lunar is not None:
            y, m, d, leap = lunar
            x = sxtwl.fromLunar(y, m, d, leap)
            a = f"{x.getSolarYear():04d}-{x.getSolarMonth():02d}-{x.getSolarDay():02d}"
            sol = Lunar.fromYmd(y, m, d).getSolar()
            b = f"{sol.getYear():04d}-{sol.getMonth():02d}-{sol.getDay():02d}"
            if a != b:
                raise SystemExit(f"converter disagreement for {raw}: {a} vs {b}")
            norm, method = a, CHECK
        out.append({
            "conv_id": i, "raw_date": raw, "from_calendar": frm, "norm_date": norm,
            "to_calendar": to, "method": method, "doc_id": doc, "locator": loc, "note": note,
        })
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({len(out)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
