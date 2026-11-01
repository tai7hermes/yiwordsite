#!/usr/bin/env python3
"""Build accordion sections for terms.html (3 languages) with original text from docx + JSON."""

import json
import re
from html import escape
from docx import Document

BASE = '/Users/tai7hermes/YiwordSite_MVP/'
SRC = BASE + 'docs/source-docs/AI-易經-A00-周易與易傳原文-202611/'
LABEL_PATTERN = re.compile(r'^([A-Z][A-Z]*(?:-[A-Z])?-\d+-\d+)')

ARROW = '\u25b6'  # ▶

# ============================================================
# DATA EXTRACTION
# ============================================================

def extract_zhouyi_hant():
    """Extract 周易繁中 from docx: 450 units."""
    doc = Document(SRC + '周易原文_64卦450單元_網站App_RWD工程版.docx')
    data = []
    current_hx_no = None
    current_hx_name = None
    started = False
    for p in doc.paragraphs:
        style = p.style.name
        text = p.text.strip()
        if not started:
            if style == 'Heading 1' and '五' in text and '周易' in text:
                started = True
            continue
        if style == 'Heading 2':
            m = re.match(r'第\s*(\d+)\s*卦\s*\u3000?(.+)', text)
            if m:
                current_hx_no = int(m.group(1))
                current_hx_name = m.group(2).strip()
            continue
        if style == 'Normal' and text and current_hx_no:
            if text.startswith('卦辭'):
                line_pos = '卦辭'
                original = text.replace('卦辭', '', 1).lstrip('\u3000').strip()
            else:
                idx = text.find('：')
                if idx > 0 and idx <= 4:
                    line_pos = text[:idx]
                    original = text
                else:
                    idx = text.find('，')
                    if idx > 0 and idx <= 4:
                        line_pos = text[:idx]
                        original = text
                    else:
                        continue
            if original:
                data.append((current_hx_no, current_hx_name, line_pos, original))
    return data

def extract_zhouyi_hans():
    """Extract 周易简中 from docx: 450 units."""
    doc = Document(SRC + '周易原文_简体中文版_64卦450单元_网站App_RWD工程版.docx')
    data = []
    current_hx_no = None
    current_hx_name = None
    started = False
    for p in doc.paragraphs:
        style = p.style.name
        text = p.text.strip()
        if not started:
            if style == 'Heading 1' and '四' in text and '周易原文' in text:
                started = True
            continue
        if style == 'Heading 2':
            m = re.match(r'(\d+)\s+(\S+)\s*\S*', text)
            if m:
                current_hx_no = int(m.group(1))
                current_hx_name = m.group(2).strip()
            continue
        if style == 'Normal' and text and current_hx_no:
            uid_match = re.search(r'\[(H\d+-(JUDGMENT|L\d|USE))\]', text)
            if not uid_match:
                continue
            uid = uid_match.group(1)
            text_clean = re.sub(r'\s*\[.*?\]\s*$', '', text).strip()
            if not text_clean:
                continue
            if uid.endswith('-JUDGMENT'):
                line_pos = '卦辞'
            elif uid.endswith('-USE'):
                line_pos = '用九' if current_hx_no == 1 else '用六'
            else:
                idx = text_clean.find('：')
                if idx > 0:
                    line_pos = text_clean[:idx]
                else:
                    line_pos = ''
                data.append((current_hx_no, current_hx_name, line_pos, text_clean))
                continue
            data.append((current_hx_no, current_hx_name, line_pos, text_clean))
    return data

def extract_zhouyi_en():
    """Extract 周易EN from JSON: 450 units."""
    with open(BASE + 'docs/zhouyi_en.json', 'r', encoding='utf-8') as f:
        zy = json.load(f)
    data = []
    for hx_no in range(1, 65):
        key = 'H%02d' % hx_no
        if key not in zy:
            continue
        hx = zy[key]
        units = hx.get('units', {})
        j = units.get('H%02d-JUDGMENT' % hx_no, {})
        j_orig = j.get('original', '')
        idx = j_orig.find('：')
        hx_name = j_orig[:idx] if idx > 0 else ''
        for uid_suffix in ['JUDGMENT'] + ['L%d' % i for i in range(1, 7)] + ['USE']:
            full_uid = 'H%02d-%s' % (hx_no, uid_suffix)
            if full_uid not in units:
                continue
            u = units[full_uid]
            orig = u.get('original', '')
            if uid_suffix == 'JUDGMENT':
                line_pos = 'Judgment'
            elif uid_suffix == 'USE':
                line_pos = 'Use of Nine' if hx_no == 1 else 'Use of Six'
            else:
                idx2 = orig.find('：')
                line_pos = orig[:idx2] if idx2 > 0 else u.get('label', '')
            data.append((hx_no, hx_name, line_pos, orig))
    return data

def clean_wing_name(name):
    """Extract wing name from '第N翼｜彖傳上' or '第N翼　彖传上'."""
    m = re.match(r'第\d+翼[｜\u3000]\s*(.+)', name)
    return m.group(1).strip() if m else name

def extract_wings_hant():
    """Extract 十翼繁中 from docx: 750 units."""
    doc = Document(SRC + '易傳十翼_十翼750單元_繁體原文_網站App_RWD完整總檔.docx')
    data = []
    current_wing = None
    in_body = False
    pending_uid = None
    for p in doc.paragraphs:
        style = p.style.name
        text = p.text.strip()
        if style == 'Heading 1' and '原文正文' in text:
            in_body = True
            continue
        if not in_body:
            continue
        if style == 'Heading 2':
            current_wing = clean_wing_name(text)
            pending_uid = None
            continue
        if not text or not current_wing:
            continue
        if style == 'Normal':
            m = LABEL_PATTERN.match(text)
            if m:
                pending_uid = m.group(1)
                continue
            if pending_uid:
                data.append((current_wing, pending_uid, text))
                pending_uid = None
    return data

def extract_wings_hans():
    """Extract 十翼简中 from docx: 750 units."""
    doc = Document(SRC + '易传十翼_十翼750单元_简体原文_网站App_RWD完整总档.docx')
    data = []
    current_wing = None
    pending_uid = None
    in_body = False
    for p in doc.paragraphs:
        style = p.style.name
        text = p.text.strip()
        if not in_body:
            if style == 'Heading 1' and '第1翼' in text:
                in_body = True
                current_wing = clean_wing_name(text)
            continue
        if style == 'Heading 1' and '第' in text and '翼' in text:
            current_wing = clean_wing_name(text)
            pending_uid = None
            continue
        if style == 'Heading 2':
            pending_uid = text
            continue
        if style == 'Normal' and text and current_wing and pending_uid:
            data.append((current_wing, pending_uid, text))
            pending_uid = None
    return data

def extract_wings_en():
    """Extract 十翼EN from JSON: 750 units."""
    with open(BASE + 'docs/wings_en_new.json', 'r', encoding='utf-8') as f:
        wg = json.load(f)
    wing_names = {
        'TUAN-U': 'Tuan Commentary I', 'TUAN-L': 'Tuan Commentary II',
        'XIANG-U': 'Image Commentary I', 'XIANG-L': 'Image Commentary II',
        'WENYAN': 'Words on the Lines',
        'XICI-U': 'Appended Statements I', 'XICI-L': 'Appended Statements II',
        'SHUOGUA': 'Explaining the Trigrams', 'XUGUA': 'Sequence of the Hexagrams',
        'ZAGUA': 'Miscellaneous Hexagrams',
    }
    data = []
    for wk in ['TUAN-U','TUAN-L','XIANG-U','XIANG-L','WENYAN','XICI-U','XICI-L','SHUOGUA','XUGUA','ZAGUA']:
        w = wg[wk]
        units = w.get('units', {})
        wname = wing_names.get(wk, wk)
        for uid in sorted(units.keys()):
            u = units[uid]
            orig = u.get('original', '')
            if orig:
                data.append((wname, uid, orig))
    return data

# ============================================================
# HTML GENERATION
# ============================================================

ACCORDION_JS = """<script>
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('.acc-header').forEach(function(h){
    h.addEventListener('click',function(){this.parentElement.classList.toggle('open');});
  });
});
</script>"""

TITLES_ZHOUYI = {
    'hant': '周易六十四卦 原文',
    'hans': '周易六十四卦 原文',
    'en': 'Original Text of the 64 Hexagrams',
}
TITLES_WINGS = {
    'hant': '易傳十翼 原文',
    'hans': '易传十翼 原文',
    'en': 'Original Text of the Ten Wings',
}

def build_zhouyi_table(data, lang):
    """Build HTML table for 周易六十四卦原文."""
    if lang == 'hant':
        headers = ['卦號', '卦名', '爻位', '原文']
    elif lang == 'hans':
        headers = ['卦号', '卦名', '爻位', '原文']
    else:
        headers = ['Hexagram', 'Name', 'Line', 'Original Text']
    
    rows = []
    for hx_no, hx_name, line_pos, original in data:
        rows.append('    <tr><td>%02d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            hx_no, escape(str(hx_name)), escape(str(line_pos)), escape(str(original))
        ))
    body = '\n'.join(rows)
    title = escape(TITLES_ZHOUYI[lang])
    return '  <div class="acc-item">\n    <div class="acc-header"><span>%s</span><span class="acc-arrow">%s</span></div>\n    <div class="acc-body">\n  <table class="hex-table">\n    <thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead>\n    <tbody>\n%s\n    </tbody>\n  </table>\n    </div>\n  </div>' % (
        title, ARROW, headers[0], headers[1], headers[2], headers[3], body
    )

def build_wings_table(data, lang):
    """Build HTML table for 易傳十翼原文."""
    if lang == 'hant':
        headers = ['翼名', '單元編號', '原文']
    elif lang == 'hans':
        headers = ['翼名', '单元编号', '原文']
    else:
        headers = ['Wing', 'Unit ID', 'Original Text']
    
    rows = []
    for wing_name, unit_id, original in data:
        rows.append('    <tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            escape(str(wing_name)), escape(str(unit_id)), escape(str(original))
        ))
    body = '\n'.join(rows)
    title = escape(TITLES_WINGS[lang])
    return '  <div class="acc-item">\n    <div class="acc-header"><span>%s</span><span class="acc-arrow">%s</span></div>\n    <div class="acc-body">\n  <table class="hex-table">\n    <thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>\n    <tbody>\n%s\n    </tbody>\n  </table>\n    </div>\n  </div>' % (
        title, ARROW, headers[0], headers[1], headers[2], body
    )

def build_and_patch(lang, zhouyi_data, wings_data):
    """Build accordion HTML and patch the corresponding terms.html."""
    if lang == 'hant':
        path = BASE + 'terms.html'
    elif lang == 'hans':
        path = BASE + 'cn/terms.html'
    else:
        path = BASE + 'en/terms.html'
    
    zhouyi_html = build_zhouyi_table(zhouyi_data, lang)
    wings_html = build_wings_table(wings_data, lang)
    
    accordion_block = '<div class="acc-list">\n%s\n%s\n</div>\n%s' % (
        zhouyi_html, wings_html, ACCORDION_JS
    )
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    marker = '</table>\n  <p class="small">'
    if marker not in content:
        print("ERROR: Could not find insertion marker in %s" % path)
        return 0
    
    new_content = content.replace(
        marker,
        '</table>\n  ' + accordion_block + '\n  <p class="small">'
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    total_rows = len(zhouyi_data) + len(wings_data)
    print("  %s: %d 周易 + %d 十翼 = %d rows" % (path, len(zhouyi_data), len(wings_data), total_rows))
    return total_rows

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("Extracting data...")
    zy_hant = extract_zhouyi_hant()
    zy_hans = extract_zhouyi_hans()
    zy_en = extract_zhouyi_en()
    wg_hant = extract_wings_hant()
    wg_hans = extract_wings_hans()
    wg_en = extract_wings_en()
    
    print("  周易 繁中: %d, 简中: %d, EN: %d" % (len(zy_hant), len(zy_hans), len(zy_en)))
    print("  十翼 繁中: %d, 简中: %d, EN: %d" % (len(wg_hant), len(wg_hans), len(wg_en)))
    
    assert len(zy_hant) == 450, "周易繁中: expected 450, got %d" % len(zy_hant)
    assert len(zy_hans) == 450, "周易简中: expected 450, got %d" % len(zy_hans)
    assert len(zy_en) == 450, "周易EN: expected 450, got %d" % len(zy_en)
    assert len(wg_hant) == 750, "十翼繁中: expected 750, got %d" % len(wg_hant)
    assert len(wg_hans) == 750, "十翼简中: expected 750, got %d" % len(wg_hans)
    assert len(wg_en) == 750, "十翼EN: expected 750, got %d" % len(wg_en)
    print("  All counts verified: 450 + 750 = 1200 per language")
    
    print("\nPatching terms.html files...")
    total = 0
    total += build_and_patch('hant', zy_hant, wg_hant)
    total += build_and_patch('hans', zy_hans, wg_hans)
    total += build_and_patch('en', zy_en, wg_en)
    print("\nTotal rows across all 3 files: %d" % total)
    print("Files modified: 3")
