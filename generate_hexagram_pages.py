#!/usr/bin/env python3
"""Generate 64 hexagram HTML pages for the YiWord site.

Each hexagram page lives at hexagram/hXX.html (e.g. h01.html).
Pages include trigram info, judgment (卦辭), six line texts (爻辭),
and (for H01/H02) a 用九/用六 section.

Run:  python3 generate_hexagram_pages.py
"""

import os
import sys

# -- locate yijing_data.py ---------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from yijing_data import HEXAGRAMS, TRIGRAMS  # noqa: E402

OUT_DIR = os.path.join(SCRIPT_DIR, "hexagram")

# -- trigram binary patterns (bottom-to-top, 1=yang 0=yin) -------------------
TRIGRAM_BITS = {
    "qian": "111",
    "dui":  "011",
    "li":   "101",
    "zhen": "001",
    "xun":  "110",
    "kan":  "010",
    "gen":  "100",
    "kun":  "000",
}

# -- line labels -------------------------------------------------------------
# Chinese numerals for positions 1-6
LINE_POS_LABELS = ["初", "二", "三", "四", "五", "上"]
# value char: 1 → 九, 0 → 六
def line_label(pos: int, is_yang: bool) -> str:
    """Return the traditional line label, e.g. 初九, 六二, 上九."""
    num = LINE_POS_LABELS[pos - 1]  # 1-based
    val = "九" if is_yang else "六"
    if pos == 1:
        return f"初{val}"
    elif pos == 6:
        return f"上{val}"
    else:
        return f"{val}{num}"


def hexagram_bits(hex_id: str, upper: str, lower: str) -> list[bool]:
    """Return 6 booleans for lines 1-6 (bottom-to-top).

    Lines 1-3 come from the lower trigram, lines 4-6 from the upper trigram.
    Within a trigram the pattern is bottom/middle/top = chars 0/1/2.
    """
    lower_bits = TRIGRAM_BITS[lower]
    upper_bits = TRIGRAM_BITS[upper]
    bits = []
    for i in range(3):
        bits.append(lower_bits[i] == "1")
    for i in range(3):
        bits.append(upper_bits[i] == "1")
    return bits


def generate_page(hx) -> str:
    """Build the full HTML for one hexagram tuple."""
    (
        hex_id,
        name_hant,
        name_hans,
        name_en,
        unicode_sym,
        upper_key,
        lower_key,
        judgment,
    ) = hx

    lower_id = hex_id.lower()  # h01, h02, ...
    upper_tr = TRIGRAMS[upper_key]
    lower_tr = TRIGRAMS[lower_key]

    bits = hexagram_bits(hex_id, upper_key, lower_key)

    # -- line unit_ids --------------------------------------------------------
    line_ids = []
    for i in range(6):
        pos = i + 1
        unit_id = f"{hex_id}-L0{pos}"
        line_ids.append(unit_id)
    if hex_id == "H01":
        yong_unit_id = f"{hex_id}-L07-YONG9"
    elif hex_id == "H02":
        yong_unit_id = f"{hex_id}-L07-YONG6"

    # -- build line sections --------------------------------------------------
    line_sections = []
    for i in range(6):
        pos = i + 1
        is_yang = bits[i]
        label = line_label(pos, is_yang)
        uid = line_ids[i]
        line_sections.append(f"""  <section class="line-section" id="{uid}">
    <h3>{label}</h3>
    <div class="cite-box">
      <p class="orig-text">[原文待補]</p>
      <p class="src">unit_id: {uid}</p>
    </div>
  </section>""")

    # -- 用九 / 用六 section --------------------------------------------------
    yong_section = ""
    if hex_id == "H01":
        yong_section = f"""  <section class="line-section" id="{yong_unit_id}">
    <h3>用九</h3>
    <div class="cite-box">
      <p class="orig-text">[原文待補]</p>
      <p class="src">unit_id: {yong_unit_id}</p>
    </div>
  </section>
"""
    elif hex_id == "H02":
        yong_section = f"""  <section class="line-section" id="{yong_unit_id}">
    <h3>用六</h3>
    <div class="cite-box">
      <p class="orig-text">[原文待補]</p>
      <p class="src">unit_id: {yong_unit_id}</p>
    </div>
  </section>
"""

    # -- unit_ids note --------------------------------------------------------
    all_unit_ids = [f"{hex_id}-JUDGMENT"] + line_ids
    if hex_id in ("H01", "H02"):
        all_unit_ids.append(yong_unit_id)
    unit_ids_str = ", ".join(all_unit_ids)

    # -- trigram descriptions -------------------------------------------------
    upper_desc = f"{upper_tr['name']}（{upper_tr['nature']}）"
    lower_desc = f"{lower_tr['name']}（{lower_tr['nature']}）"

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{unicode_sym} {name_hant}（{hex_id}）— YiWord 易理</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<header>
  <div class="brand">YiWord <span>易理</span></div>
  <div class="lang-switch">
    <a href="../hexagram/{lower_id}.html" class="active">繁中</a>
    <a href="../en/hexagram/{lower_id}.html">EN</a>
    <a href="../cn/hexagram/{lower_id}.html">简中</a>
  </div>
</header>
<nav>
  <ul>
    <li><a href="../index.html">首頁</a></li>
    <li><a href="../introduction.html">易經介紹</a></li>
    <li><a href="../hexagrams.html" class="active">六十四卦</a></li>
    <li><a href="../wings.html">易傳十翼</a></li>
    <li><a href="../terms.html">名詞索引</a></li>
    <li><a href="../search.html">搜尋</a></li>
    <li><a href="../about.html">關於</a></li>
  </ul>
</nav>
<main>
  <h1>{unicode_sym} {name_hant}</h1>

  <table class="hexagram-info">
    <tbody>
      <tr><th>卦名</th><td>{name_hant}（{name_hans}）· {name_en}</td></tr>
      <tr><th>Unicode符號</th><td>{unicode_sym} {hex_id}</td></tr>
      <tr><th>上卦</th><td>{upper_tr['symbol']} {upper_desc}</td></tr>
      <tr><th>下卦</th><td>{lower_tr['symbol']} {lower_desc}</td></tr>
    </tbody>
  </table>

  <section class="judgment-section" id="{hex_id}-JUDGMENT">
    <h2>卦辭</h2>
    <div class="cite-box">
      <p class="orig-text">{judgment}</p>
      <p class="src">unit_id: {hex_id}-JUDGMENT</p>
    </div>
  </section>

  <h2>爻辭</h2>
{chr(10).join(line_sections)}
{yong_section}  <div class="note">
    <p>固定 unit_ids：{unit_ids_str}</p>
  </div>
</main>
<footer>
  <p>© 2026 YiWord.com · <a href="../privacy.html">隱私權政策</a> · <a href="../terms.html">使用條款</a></p>
  <p class="small">固定 ID：H01-H64 · W01-W10 · text_version: yijing-introduction-1.0.0</p>
</footer>
</body>
</html>
"""
    return html


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    count = 0
    for hx in HEXAGRAMS:
        html = generate_page(hx)
        lower_id = hx[0].lower()
        path = os.path.join(OUT_DIR, f"{lower_id}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
    print(f"Generated {count} hexagram pages in {OUT_DIR}")

    # -- verify ---------------------------------------------------------------
    files = [
        f for f in os.listdir(OUT_DIR)
        if f.startswith("h") and f.endswith(".html")
    ]
    print(f"Verification: found {len(files)} h*.html files in {OUT_DIR}")
    assert len(files) == 64, f"Expected 64 files, found {len(files)}"
    print("All 64 hexagram pages verified.")


if __name__ == "__main__":
    main()
