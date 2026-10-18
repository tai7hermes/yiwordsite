#!/usr/bin/env python3
"""Extract political/military cases from 12 docx files and build 3 trilingual HTML pages."""
import os, re, html
from docx import Document

SRC = "/Users/tai7hermes/YiwordSite_MVP/docs/source-docs/AI-易經-A11-64掛與384爻-案例-3-202609"
OUT = "/Users/tai7hermes/YiwordSite_MVP"

FILES = {
    "A11": "A11-周易六十四卦_中華政治軍事史案例_重新撰寫故事與卦義短文_網站App_RWD.docx",
    "A12": "A12-周易六十四卦_歐美政治軍事史案例_故事與卦義短文_網站App_RWD.docx",
    "B11": "B11-易傳小象384爻_中華政治軍事故事與社群短文_重新編寫.docx",
    "B12": "B12-易傳小象384爻_歐美政治軍事故事與社群短文_重新編寫.docx",
    "C11": "C11-周易六十四卦_中华政治军事史案例_简体中文版_网站App_RWD.docx",
    "C12": "C12-周易六十四卦_欧美政治军事史案例_简体中文版_网站App_RWD.docx",
    "D11": "D11-易传小象384爻中华政治军事案例故事与历史对照_简体中文版.docx",
    "D12": "D12-易传小象384爻欧美政治军事案例故事与历史对照_简体中文版.docx",
    "E11": "E11_Zhouyi_64_Political_Military_Historical_Stories_English_Web_App_RWD.docx",
    "E12": "E12-Zhouyi_64_Europe_US_Political_Military_Rewritten_Stories_Analogy_English_Web_App_RWD.docx",
    "F11": "F11_Xiaoxiang_384_English_Complete_Working_Draft_H01-H64_Lines_001-384.docx",
    "F12": "F12-Yizhuan_384_Europe_US_Political_Military_Rewritten_English_Stories_Comparisons_Web_App_RWD.docx",
}

YAO_PAT = re.compile(r'^(初九|九二|九三|九四|九五|上九|初六|六二|六三|六四|六五|上六)[｜|]')
HEX_NUM_PAT = re.compile(r'^(\d{1,2})\s*[｜|\s]\s*\S')
HEX_NUM_PAT2 = re.compile(r'^(\d{1,2})\s+\S')
YAO_NUM_PAT = re.compile(r'^第(\d+)爻')


def load_doc(key):
    return Document(os.path.join(SRC, FILES[key]))


def extract_64_h2(doc, hex_pat):
    """Extract 64-hex cases where case title is Heading 2 starting with hex number."""
    cases = []
    current = None
    for p in doc.paragraphs:
        style = p.style.name if p.style else "None"
        text = p.text.strip()
        if not text:
            continue
        if style == "Heading 2":
            if hex_pat.match(text):
                if current:
                    cases.append(current)
                current = {"title": text, "meta": "", "paragraphs": []}
            else:
                if current:
                    cases.append(current)
                current = None
        elif style in ("Normal", "Caption", "Caption Small") and current is not None:
            if not current["meta"]:
                current["meta"] = text
            else:
                current["paragraphs"].append(text)
    if current:
        cases.append(current)
    return cases[:64]


def extract_64_h1(doc, hex_pat):
    """Extract 64-hex cases where case title is Heading 1 starting with hex number."""
    cases = []
    current = None
    for p in doc.paragraphs:
        style = p.style.name if p.style else "None"
        text = p.text.strip()
        if not text:
            continue
        if style == "Heading 1":
            if hex_pat.match(text):
                if current:
                    cases.append(current)
                current = {"title": text, "meta": "", "paragraphs": []}
            else:
                if current:
                    cases.append(current)
                current = None
        elif style in ("Heading 2", "Normal", "Caption", "Caption Small") and current is not None:
            if not current["meta"]:
                current["meta"] = text
            else:
                current["paragraphs"].append(text)
    if current:
        cases.append(current)
    return cases[:64]


def extract_384_yao_h2(doc):
    """Extract 384-yao cases where case title is Heading 2 starting with yao name (初九 etc)."""
    cases = []
    current = None
    for p in doc.paragraphs:
        style = p.style.name if p.style else "None"
        text = p.text.strip()
        if not text:
            continue
        if style == "Heading 2":
            if YAO_PAT.match(text) or YAO_NUM_PAT.match(text):
                if current:
                    cases.append(current)
                current = {"title": text, "meta": "", "paragraphs": []}
            else:
                if current:
                    cases.append(current)
                current = None
        elif style == "Heading 3" and current is not None:
            current["paragraphs"].append(text)
        elif style in ("Normal", "List Bullet") and current is not None:
            if not current["meta"]:
                current["meta"] = text
            else:
                current["paragraphs"].append(text)
    if current:
        cases.append(current)
    return cases[:384]


def extract_384_en_h3(doc):
    """Extract 384-yao cases from English F11/F12 where each case is a Heading 3 'Line N'."""
    cases = []
    current = None
    line_pat = re.compile(r'^Line\s+\d')
    for p in doc.paragraphs:
        style = p.style.name if p.style else "None"
        text = p.text.strip()
        if not text:
            continue
        if style == "Heading 3":
            if line_pat.match(text):
                if current:
                    cases.append(current)
                current = {"title": text, "meta": "", "paragraphs": []}
            else:
                if current:
                    cases.append(current)
                current = None
        elif style == "Heading 2":
            # Hexagram section heading - skip, but end current
            if current:
                cases.append(current)
            current = None
        elif style == "Normal" and current is not None:
            if not current["meta"]:
                current["meta"] = text
            else:
                current["paragraphs"].append(text)
    if current:
        cases.append(current)
    return cases[:384]


def extract_384_en_h2_lines(doc):
    """Extract 384-yao from English F11 which uses Heading 2 'NN.N — Line N'."""
    cases = []
    current = None
    line_pat = re.compile(r'^\d{1,2}\.\d\b')
    for p in doc.paragraphs:
        style = p.style.name if p.style else "None"
        text = p.text.strip()
        if not text:
            continue
        if style == "Heading 2":
            if line_pat.match(text):
                if current:
                    cases.append(current)
                current = {"title": text, "meta": "", "paragraphs": []}
            elif current is not None:
                current["paragraphs"].append(text)
        elif style == "Normal" and current is not None:
            if not current["meta"]:
                current["meta"] = text
            else:
                current["paragraphs"].append(text)
        elif style == "Heading 1":
            if current:
                cases.append(current)
            current = None
    if current:
        cases.append(current)
    return cases[:384]


def get_meta_64(meta):
    """Extract evidence tag (A/B) and the rest from meta line."""
    if not meta:
        return ("", "")
    # Look for A or B at start, or 'Evidence: A/B' or 'Evidence A/B'
    m = re.search(r'\b([AB])\b', meta)
    if m:
        tag = m.group(1)
        return (tag, meta)
    return ("", meta)


def case_to_html(case, is_yao, yao_num=None):
    title = html.escape(case["title"])
    if is_yao:
        tag = f"{yao_num:03d}爻"
        rest = case.get("meta", "")
    else:
        tag, rest = get_meta_64(case.get("meta", ""))
    parts = [f'<div class="case-entry">',
             f'  <h4>{title}</h4>']
    if rest:
        parts.append(f'  <div class="case-meta"><span class="case-tag">{html.escape(tag)}</span> {html.escape(rest)}</div>')
    elif tag:
        parts.append(f'  <div class="case-meta"><span class="case-tag">{html.escape(tag)}</span></div>')
    for para in case["paragraphs"]:
        parts.append(f'  <p>{html.escape(para)}</p>')
    parts.append('</div>')
    return "\n".join(parts)


def build_page(lang, hex_label, sec1_title, sec1_sub, sec2_title, sec2_sub,
               c64_zh, c64_eu, c384_zh, c384_eu, sub64_label, sub384_label):
    """Build one HTML page.
    Section 1 = 中華案例 (c64_zh + c384_zh)
    Section 2 = 歐美案例 (c64_eu + c384_eu)
    """
    if lang == "tw":
        lang_attr = "zh-Hant"
        title = "政治與軍事案例 — YiWord 易理"
        css_href = "style.css"
        nav = [("index.html","首頁"),("introduction.html","易經介紹"),("hexagrams.html","六十四卦"),
               ("wings.html","易傳十翼"),("cases.html","案例"),("divination.html","占卜"),
               ("terms.html","名詞索引"),("search.html","搜尋"),("about.html","關於")]
        lang_switch = '<a href="cn/case-political.html">简中</a> <a href="case-political.html" class="active">繁中</a> <a href="en/case-political.html">EN</a>'
        home_link = "index.html"
        home_label = "⌂ 首頁"
        back_label = "← 回上頁"
        footer_priv = "隱私權政策"
        footer_terms = "使用條款"
        privacy_href = "privacy.html"
        terms_href = "terms.html"
    elif lang == "cn":
        lang_attr = "zh-Hans"
        title = "政治与军事案例 — YiWord 易理"
        css_href = "../style.css"
        nav = [("index.html","首页"),("introduction.html","易经介绍"),("hexagrams.html","六十四卦"),
               ("wings.html","易传十翼"),("cases.html","案例"),("divination.html","占卜"),
               ("terms.html","名词索引"),("search.html","搜索"),("about.html","关于")]
        lang_switch = '<a href="../cn/case-political.html" class="active">简中</a> <a href="../case-political.html">繁中</a> <a href="../en/case-political.html">EN</a>'
        home_link = "../cn/index.html"
        home_label = "⌂ 首页"
        back_label = "← 回上页"
        footer_priv = "隐私权政策"
        footer_terms = "使用条款"
        privacy_href = "../privacy.html"
        terms_href = "../terms.html"
    else:
        lang_attr = "en"
        title = "Political and Military Cases — YiWord 易理"
        css_href = "../style.css"
        nav = [("index.html","Home"),("introduction.html","Introduction"),("hexagrams.html","64 Hexagrams"),
               ("wings.html","Ten Wings"),("cases.html","Cases"),("divination.html","Divination"),
               ("terms.html","Glossary"),("search.html","Search"),("about.html","About")]
        lang_switch = '<a href="../cn/case-political.html">简中</a> <a href="../case-political.html">繁中</a> <a href="../en/case-political.html" class="active">EN</a>'
        home_link = "../en/index.html"
        home_label = "⌂ Home"
        back_label = "← Back"
        footer_priv = "Privacy Policy"
        footer_terms = "Terms of Use"
        privacy_href = "../privacy.html"
        terms_href = "../terms.html"

    nav_html = ""
    for href, label in nav:
        full = f"../{lang}/{href}" if lang in ("cn", "en") else href
        cls = ' class="active"' if href == "cases.html" else ""
        nav_html += f'<li><a href="{full}"{cls}>{label}</a></li>'

    s1 = f'<h4 class="case-subhead">{html.escape(sub64_label)}</h4>\n'
    s1 += "\n".join(case_to_html(c, False) for c in c64_zh)
    s1 += f'\n<h4 class="case-subhead">{html.escape(sub384_label)}</h4>\n'
    s1 += "\n".join(case_to_html(c, True, i+1) for i, c in enumerate(c384_zh))
    s2 = f'<h4 class="case-subhead">{html.escape(sub64_label)}</h4>\n'
    s2 += "\n".join(case_to_html(c, False) for c in c64_eu)
    s2 += f'\n<h4 class="case-subhead">{html.escape(sub384_label)}</h4>\n'
    s2 += "\n".join(case_to_html(c, True, i+1) for i, c in enumerate(c384_eu))

    return f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{css_href}">
</head>
<body>
<header><div class="brand">YiWord <span>易理 = 處世之道</span></div><div class="lang-switch">{lang_switch}</div></header>
<nav><ul>{nav_html}</ul></nav>
<main>
<div class="back-nav"><a href="{home_link}">{home_label}</a><a href="javascript:history.back()">{back_label}</a></div>
<div class="hex-num-label">{html.escape(hex_label)}</div>
<div class="case-section">
<h3>{html.escape(sec1_title)}</h3>
<p>{html.escape(sec1_sub)}</p>
{s1}
</div>
<div class="case-section">
<h3>{html.escape(sec2_title)}</h3>
<p>{html.escape(sec2_sub)}</p>
{s2}
</div>
</main>
<footer><p>© 2026 YiWord.com · <a href="{privacy_href}">{html.escape(footer_priv)}</a> · <a href="{terms_href}">{html.escape(footer_terms)}</a></p></footer>
</body>
</html>"""


def main():
    print("=== Extracting 64-hex files ===")
    # A11/C11: H2 with "01 乾  ..." pattern
    a11 = extract_64_h2(load_doc("A11"), HEX_NUM_PAT2)
    c11 = extract_64_h2(load_doc("C11"), HEX_NUM_PAT2)
    # A12/C12: H2 with "01｜乾" pattern
    a12 = extract_64_h2(load_doc("A12"), HEX_NUM_PAT)
    c12 = extract_64_h2(load_doc("C12"), HEX_NUM_PAT)
    # E11: H1 with "01  乾  |" pattern
    e11 = extract_64_h1(load_doc("E11"), HEX_NUM_PAT2)
    # E12: H2 with "01  乾  |  Hexagram 01"
    e12 = extract_64_h2(load_doc("E12"), HEX_NUM_PAT2)
    print(f"  A11={len(a11)} A12={len(a12)} C11={len(c11)} C12={len(c12)} E11={len(e11)} E12={len(e12)}")

    print("=== Extracting 384-yao files ===")
    # B11/D11: H2 with "初九|..." yao pattern
    b11 = extract_384_yao_h2(load_doc("B11"))
    d11 = extract_384_yao_h2(load_doc("D11"))
    # B12: H2 with "第NNN爻..." pattern (full 384)
    b12 = extract_384_yao_h2(load_doc("B12"))
    # D12: only 96 cases (batch 4) - H2 with "第NNN爻..." pattern
    d12 = extract_384_yao_h2(load_doc("D12"))
    # F11: H2 with "NN.N — Line N" pattern
    f11 = extract_384_en_h2_lines(load_doc("F11"))
    # F12: H3 with "Line N" pattern under H2 hexagram sections
    f12 = extract_384_en_h3(load_doc("F12"))
    print(f"  B11={len(b11)} B12={len(b12)} D11={len(d11)} D12={len(d12)} F11={len(f11)} F12={len(f12)}")

    # Build pages
    tw = build_page("tw", "政治與軍事案例",
        "中華案例", "中華政治軍事歷史案例，含六十四卦 64 則與三百八十四爻 384 則。",
        "歐美案例", "歐美政治軍事歷史案例，含六十四卦 64 則與三百八十四爻 384 則。",
        a11, a12, b11, b12, "六十四卦案例", "三百八十四爻案例")
    with open(os.path.join(OUT, "case-political.html"), "w", encoding="utf-8") as f:
        f.write(tw)
    print(f"Wrote case-political.html ({len(tw)} bytes)")

    cn = build_page("cn", "政治与军事案例",
        "中华案例", "中华政治军事历史案例，含六十四卦 64 则与三百八十四爻 384 则。",
        "欧美案例", "欧美政治军事历史案例，含六十四卦 64 则与三百八十四爻 384 则。",
        c11, c12, d11, d12, "六十四卦案例", "三百八十四爻案例")
    with open(os.path.join(OUT, "cn", "case-political.html"), "w", encoding="utf-8") as f:
        f.write(cn)
    print(f"Wrote cn/case-political.html ({len(cn)} bytes)")

    en = build_page("en", "Political and Military Cases",
        "Chinese Cases", "Chinese political and military historical cases: 64 hexagram cases and 384 line cases.",
        "Western Cases", "European and American political and military historical cases: 64 hexagram cases and 384 line cases.",
        e11, e12, f11, f12, "64 Hexagram Cases", "384 Line Cases")
    with open(os.path.join(OUT, "en", "case-political.html"), "w", encoding="utf-8") as f:
        f.write(en)
    print(f"Wrote en/case-political.html ({len(en)} bytes)")

    total = (len(a11)+len(a12)+len(b11)+len(b12) +
             len(c11)+len(c12)+len(d11)+len(d12) +
             len(e11)+len(e12)+len(f11)+len(f12))
    print(f"\nTotal cases: {total}")
    print(f"Per page: tw={len(a11)+len(a12)+len(b11)+len(b12)} cn={len(c11)+len(c12)+len(d11)+len(d12)} en={len(e11)+len(e12)+len(f11)+len(f12)}")
    return total, len(a11)+len(a12)+len(b11)+len(b12), len(c11)+len(c12)+len(d11)+len(d12), len(e11)+len(e12)+len(f11)+len(f12)


if __name__ == "__main__":
    main()
