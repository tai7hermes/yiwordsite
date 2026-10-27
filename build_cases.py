#!/usr/bin/env python3
"""Build all 36 case sub-pages from V4.3 source .docx files."""
import os, re
from docx import Document
from html import escape

BASE = "/Users/tai7hermes/YiwordSite_MVP"
SRC = os.path.join(BASE, "docs/source-docs/AI-易經-A11-64掛與384爻-案例(新)-202610")

HEX_TW = ['乾','坤','屯','蒙','需','訟','師','比','小畜','履','泰','否','同人','大有',
           '謙','豫','隨','蠱','臨','觀','噬嗑','賁','剝','復','无妄','大畜','頤','大過',
           '坎','離','咸','恆','遯','大壯','晉','明夷','家人','睽','蹇','解','損','益',
           '夬','姤','萃','升','困','井','革','鼎','震','艮','漸','歸妹','豐','旅',
           '巽','兌','渙','節','中孚','小過','既濟','未濟']
HEX_HS = ['干','坤','屯','蒙','需','讼','师','比','小畜','履','泰','否','同人','大有',
           '谦','豫','随','蛊','临','观','噬嗑','贲','剥','复','无妄','大畜','颐','大过',
           '坎','离','咸','恒','遯','大壮','晋','明夷','家人','睽','蹇','解','损','益',
           '夬','姤','萃','升','困','井','革','鼎','震','艮','渐','归妹','丰','旅',
           '巽','兑','涣','节','中孚','小过','既济','未济']
HEX_EN = ['Qian','Kun','Zhun','Meng','Xu','Song','Shi','Bi','Xiao Xu','Lu','Tai','Pi',
           'Tong Ren','Da You','Qian','Yu','Sui','Gu','Lin','Guan','Shi He','Bi','Bo','Fu',
           'Wu Wang','Da Xu','Yi','Da Guo','Kan','Li','Xian','Heng','Dun','Da Zhuang',
           'Jin','Ming Yi','Jia Ren','Kui','Jian','Jie','Sun','Yi','Guai','Gou','Cui',
           'Sheng','Kun','Jing','Ge','Ding','Zhen','Gen','Jian','Gui Mei','Feng','Lu',
           'Xun','Dui','Huan','Jie','Zhong Fu','Xiao Guo','Ji Ji','Wei Ji']
LINE_POS = ['初九','九二','九三','九四','九五','上九']
DOMAIN_MAP = {'political':'PM','economic':'EF','workplace':'WL'}

def sp(n, folder, fn):
    return os.path.join(SRC, "AI-易經-A11-64掛與384爻-案例-" + str(n) + "-" + folder + "-202610", fn)

SRC_64 = {
    'cn': {
        'zhTW': {
            'PM': sp(4,'中華64卦','周易64卦_中華PM_01-64卦_繁體中文版_四批整合_適切性修訂_V4.3.docx'),
            'EF': sp(4,'中華64卦','周易64卦_中華EF_01-64卦_繁體中文版_四批整合_適切性修訂_V4.3.docx'),
            'WL': sp(4,'中華64卦','周易64卦_中華WL_01-64卦_繁體中文版_四批整合_適切性修訂_V4.3.docx'),
        },
        'zhHS': {
            'PM': sp(4,'中華64卦','周易64卦_中华政治军事PM_第01-64卦_简体中文版_V4.3_完整总档_网站App_RWD.docx'),
            'EF': sp(4,'中華64卦','周易64卦_中华经济财经EF_第01-64卦_简体中文版_V4.3_完整总档_网站App_RWD.docx'),
            'WL': sp(4,'中華64卦','周易64卦_中华职场生活WL_第01-64卦_简体中文版_V4.3_完整总档_网站App_RWD.docx'),
        },
        'en': {
            'PM': sp(4,'中華64卦','Zhouyi_Chinese_English_PM_H01-H64_V4.3_Without_Traditional_Reference.docx'),
            'EF': sp(4,'中華64卦','Zhouyi_Chinese_English_EF_H01-H64_V4.3_Only_Evidence_Limitations.docx'),
            'WL': sp(4,'中華64卦','Zhouyi_Chinese_English_WL_H01-H64_V4.3_Complete_Web_App_RWD.docx'),
        },
    },
    'eu': {
        'zhTW': {
            'PM': sp(5,'歐美64卦','Zhouyi_64_Traditional_Chinese_H01-PM_V4.3_Integrated_Web_App_RWD.docx'),
            'EF': sp(5,'歐美64卦','Zhouyi_64_Traditional_Chinese_H01-EF_V4.3_Integrated_Web_App_RWD.docx'),
            'WL': sp(5,'歐美64卦','Zhouyi_64_Traditional_Chinese_H01-WL_V4.3_H49-64_Full_Revised.docx'),
        },
        'zhHS': {
            'PM': sp(5,'歐美64卦','Zhouyi_64_Simplified_Chinese_PM_H01-V4.3_Integrated_Web_App_RWD.docx'),
            'EF': sp(5,'歐美64卦','Zhouyi_64_Simplified_Chinese_EF_H01-V4.3_Integrated_Web_App_RWD.docx'),
            'WL': sp(5,'歐美64卦','Zhouyi_64_Simplified_Chinese_WL_H01-_V4.3_Integrated_Web_App_RWD.docx'),
        },
        'en': {
            'PM': sp(5,'歐美64卦','Zhouyi_64_English_EN-PM_V4.3_Integrated_Web_App_RWD.docx'),
            'EF': sp(5,'歐美64卦','Zhouyi_64_English_EF_EN-V4.3_Integrated_Web_App_RWD.docx'),
            'WL': sp(5,'歐美64卦','Zhouyi_64_English_EN-WL_V4.3_Integrated_Web_App_RWD.docx'),
        },
    },
}

SRC_384 = {
    'cn': {
        'zhTW': {
            'PM': sp(6,'中華384爻','易傳小象_中華_繁體中文版_PM_全64卦384篇_V4.3.3_逐爻可辨識短標題與384筆目錄_網站App_RWD工程版.docx'),
            'EF': sp(6,'中華384爻','易傳小象_中華_繁體中文版_EF_全64卦384篇_V4.3.3_逐爻可辨識短標題與384筆目錄_網站App_RWD工程版.docx'),
            'WL': sp(6,'中華384爻','易傳小象_中華_繁體中文版_WL_全64卦384篇_V4.3.3_逐爻可辨識短標題與384筆目錄_網站App_RWD工程版.docx'),
        },
        'zhHS': {
            'PM': sp(6,'中華384爻','易傳小象_中華_简体中文版_PM_全64卦384篇_V4.3.2_简短标题与目录_网站App_RWD工程版.docx'),
            'EF': sp(6,'中華384爻','易傳小象_中華_简体中文版_EF_全64卦384篇_V4.3.2_简短标题与目录_网站App_RWD工程版.docx'),
            'WL': sp(6,'中華384爻','易傳小象_中華_简体中文版_WL_全64卦384篇_V4.3.2_简短标题与目录_网站App_RWD工程版.docx'),
        },
        'en': {
            'PM': sp(6,'中華384爻','Zhouyi_384_PM_384_English_V433.docx'),
            'EF': sp(6,'中華384爻','Zhouyi_384_EF_384_English_Unified_Working_Master_V4.3.4.docx'),
            'WL': sp(6,'中華384爻','Zhouyi_384_WL_64Hexagrams_384_English_Working_Master_V4.3.4_Web_App_RWD.docx'),
        },
    },
    'eu': {
        'zhTW': {
            'PM': sp(7,'歐美384爻','Yijing_V4.3_ZH_TW_PM_Corrected.docx'),
            'EF': sp(7,'歐美384爻','Yijing_V4.3_ZH_TW_EF_Corrected.docx'),
            'WL': sp(7,'歐美384爻','Yijing_V4.3_ZH_TW_WL_Corrected.docx'),
        },
        'zhHS': {
            'PM': sp(7,'歐美384爻','Yijing_V4.3_ZH_CN_PM_384_Editable.docx'),
            'EF': sp(7,'歐美384爻','Yijing_V4.3_ZH_CN_EF_384_Editable.docx'),
            'WL': sp(7,'歐美384爻','Yijing_V4.3_ZH_CN_WL_384_Editable.docx'),
        },
        'en': {
            'PM': sp(7,'歐美384爻','Yijing_V4.3_EN_PM_Corrected.docx'),
            'EF': sp(7,'歐美384爻','Yijing_V4.3_EN_EF_Corrected.docx'),
            'WL': sp(7,'歐美384爻','Yijing_V4.3_EN_WL_Corrected.docx'),
        },
    },
}

LABELS = {}
DOMAIN_NAMES = {'political': {'zhTW':'政治與軍事','zhHS':'政治与军事','en':'Political & Military'},
                'economic': {'zhTW':'經濟與財經','zhHS':'经济与财经','en':'Economic & Financial'},
                'workplace': {'zhTW':'職場與生活','zhHS':'职场与生活','en':'Workplace & Life'}}
REGION_NAMES = {'cn': {'zhTW':'中華','zhHS':'中华','en':'Chinese'},
                'eu': {'zhTW':'歐美','zhHS':'欧美','en':'Western'}}
for domain in ['political', 'economic', 'workplace']:
    for region in ['cn', 'eu']:
        for dtype, tt, th, te in [('64','64卦','64卦','64 Hexagrams'),('384','384爻','384爻','384 Lines')]:
            LABELS[(domain,region,dtype)] = {
                'zhTW': REGION_NAMES[region]['zhTW'] + DOMAIN_NAMES[domain]['zhTW'] + '案例 — ' + tt,
                'zhHS': REGION_NAMES[region]['zhHS'] + DOMAIN_NAMES[domain]['zhHS'] + '案例 — ' + th,
                'en':   REGION_NAMES[region]['en'] + ' ' + DOMAIN_NAMES[domain]['en'] + ' Cases — ' + te,
            }

JS_CODE = """<script>
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('.acc-header').forEach(function(h){
    h.addEventListener('click',function(){this.parentElement.classList.toggle('open');});
  });
});
</script>"""

# ── Parsers ──

def parse_64_cn_zh(doc, lang):
    """CN 64 zhTW/zhHS: Heading 2 = case heading 'NN 卦名...'"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 2' and re.match(r'^\d{2}\s', text):
            if current:
                cases.append(current)
            current = {'title': text, 'meta': '', 'tag': '', 'content': []}
        elif current and style == 'Normal':
            if text.startswith('【V4.'):
                continue
            if not current['meta'] and re.match(r'^[A-C][\s]', text):
                current['meta'] = text
                current['tag'] = text[0]
            elif not current['meta'] and ('｜' in text or '-H' in text):
                current['meta'] = text
                m = re.match(r'^([A-C])', text)
                if m:
                    current['tag'] = m.group(1)
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_64_cn_zhs_wl(doc):
    """CN 64 zhHS WL: All Normal, case heading 'NN 卦名　...' after TOC"""
    cases = []
    current = None
    in_cases = False
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        # Detect transition from TOC to cases: TOC entries are 'NN 卦名 ...' on Normal
        # Real case content also starts with 'NN 卦名　...' but has meta lines after
        if style == 'Normal' and re.match(r'^\d{2}\s', text):
            # Check if next non-empty para is a meta line (contains ｜ and case ID)
            if current:
                cases.append(current)
            current = {'title': text, 'meta': '', 'tag': '', 'content': []}
        elif current and style == 'Normal':
            if text.startswith('【V4.'):
                continue
            if not current['meta']:
                current['meta'] = text
                m = re.match(r'^([A-C])[\s｜]', text)
                if m:
                    current['tag'] = m.group(1)
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    # Filter: only keep entries that have content (meta + content)
    # TOC entries will have meta='' and empty content
    return [c for c in cases if c['content'] or c['meta']]

def parse_64_cn_en(doc):
    """CN 64 English: Heading 1 = case heading 'NN  卦名 · Title'"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 1' and re.match(r'^\d{2}\s', text):
            if current:
                cases.append(current)
            current = {'title': text, 'meta': '', 'tag': '', 'content': []}
        elif current and style == 'Normal':
            if not current['meta']:
                current['meta'] = text
                m = re.search(r'evidence_class\s*=\s*([A-C])', text)
                if m:
                    current['tag'] = m.group(1)
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_64_eu_cn(doc, lang):
    """EU 64 zhTW/zhHS: Heading 1 = '第NN卦　卦名｜title' or 'NN  卦名｜title' or 'NN｜卦名｜title'"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        is_case = False
        if style == 'Heading 1':
            if re.match(r'^第\d+卦', text) or re.match(r'^\d{2}｜', text) or re.match(r'^\d{2}\s', text):
                is_case = True
        if is_case:
            if current:
                cases.append(current)
            title = re.sub(r'^第\d+卦[\s　]+', '', text)
            current = {'title': title, 'meta': '', 'tag': '', 'content': []}
        elif current:
            if style == 'Heading 2':
                continue
            if style == 'Normal':
                if not current['meta']:
                    current['meta'] = text
                    m = re.search(r'評級[：:]\s*([A-C])', text) or re.search(r'评级[：:]\s*([A-C])', text)
                    if m:
                        current['tag'] = m.group(1)
                else:
                    current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_64_eu_cn_wl(doc):
    """EU 64 zhHS WL: Heading 1 = 'NN  卦名｜title' (two spaces)"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 1' and re.match(r'^\d{2}\s', text):
            if current:
                cases.append(current)
            current = {'title': text, 'meta': '', 'tag': '', 'content': []}
        elif current:
            if style == 'Heading 2':
                continue
            if style == 'Normal':
                if not current['meta']:
                    current['meta'] = text
                    m = re.search(r'評級[：:]\s*([A-C])', text) or re.search(r'评级[：:]\s*([A-C])', text)
                    if m:
                        current['tag'] = m.group(1)
                else:
                    current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_64_eu_en(doc):
    """EU 64 English: Heading 2 = 'NN  卦名  |  Hexagram NN'"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 2' and re.match(r'^\d{2}\s', text):
            if current:
                cases.append(current)
            current = {'title': text, 'meta': '', 'tag': '', 'content': []}
        elif current:
            if style == 'Caption Small':
                if not current['meta']:
                    current['meta'] = text
                else:
                    current['content'].append(text)
            elif style == 'Normal':
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_384_cn_zhtw(doc):
    """CN 384 zhTW: Heading 3 = 'XCASE-HNN-LX｜...', Heading 4 = '爻位｜short_title'"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 3' and re.match(r'^X(CASE|FIN|LIFE)-H\d', text):
            if current:
                cases.append(current)
            m = re.match(r'^X(?:CASE|FIN|LIFE)-H(\d{2})-L(\d)', text)
            hex_no = int(m.group(1)) if m else 0
            line_no = int(m.group(2)) if m else 0
            current = {'hex_no': hex_no, 'line_no': line_no,
                       'line_pos': '', 'short_title': '', 'full_title': '',
                       'meta': '', 'content': [], 'story': '', 'comparison': ''}
        elif current and style == 'Heading 4':
            parts = text.split('｜', 1)
            current['line_pos'] = parts[0].strip()
            if len(parts) > 1:
                rest = parts[1].strip()
                current['full_title'] = rest
                segs = rest.rsplit(' ', 1)
                current['short_title'] = segs[-1] if len(segs) > 1 else rest
            else:
                current['short_title'] = text
                current['full_title'] = text
        elif current and style == 'Normal':
            if text.startswith('案例 '):
                current['meta'] = text
            elif text.startswith('歷史故事全文') or text.startswith('历史故事全文'):
                if '｜' in text:
                    current['story'] = text.split('｜', 1)[1].strip()
            elif text.startswith('歷史對照') or text.startswith('历史对照'):
                if '｜' in text:
                    current['comparison'] = text.split('｜', 1)[1].strip()
            elif text.startswith('《小象》原文') or text.startswith('既有繁體中文譯文') or text.startswith('原事件與來源'):
                current['content'].append(text)
            elif text.startswith('本輪適切性') or text.startswith('內容狀態') or text.startswith('職場生活提醒') or text.startswith('V4.3') or text.startswith('替換') or text.startswith('史實故事') or text.startswith('逐爻對照（正式'):
                if text.startswith('史實故事'):
                    if '｜' in text:
                        current['story'] = text.split('｜', 1)[1].strip()
                    else:
                        current['story'] = text
                elif text.startswith('逐爻對照（正式'):
                    if '｜' in text:
                        current['comparison'] = text.split('｜', 1)[1].strip()
                    else:
                        current['comparison'] = text
                # else skip
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_384_cn_zhs(doc):
    """CN 384 zhHS: Heading 2 = hexagram group or XCASE-HNN-LX; Heading 3 = yao entry"""
    cases = []
    current = None
    current_hex = 0
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        # Hexagram group heading: '第NN卦｜...' or '第NN–MM卦｜...'
        if style == 'Heading 2' and re.match(r'^第\d+[–-]', text):
            m = re.match(r'^第(\d+)', text)
            current_hex = int(m.group(1)) if m else 0
        # Case ID heading (PM domain): 'XCASE-HNN-LX｜...' — use as context, don't create new case
        elif style == 'Heading 2' and re.match(r'^X(CASE|FIN|LIFE)-H\d', text):
            m = re.match(r'^X(?:CASE|FIN|LIFE)-H(\d{2})-L(\d)', text)
            hex_no = int(m.group(1)) if m else 0
            line_no = int(m.group(2)) if m else 0
            if current:
                current['hex_no'] = hex_no
                current['line_no'] = line_no
                if not current['meta']:
                    current['meta'] = text
        # Yao entry heading (EF/WL domains): '初九｜title' etc. in Heading 3
        elif style == 'Heading 3' and re.match(r'^(初九|九二|九三|九四|九五|上九|初六|六二|六三|六四|六五|上六)', text):
            if current:
                cases.append(current)
            line_no_map = {'初九':1,'九二':2,'九三':3,'九四':4,'九五':5,'上九':6,
                           '初六':1,'六二':2,'六三':3,'六四':4,'六五':5,'上六':6}
            parts = text.split('｜', 1)
            line_pos = parts[0].strip()
            line_no = line_no_map.get(line_pos, 1)
            hex_no = current_hex
            rest = parts[1].strip() if len(parts) > 1 else text
            segs = rest.rsplit(' ', 1)
            short_title = segs[-1] if len(segs) > 1 else rest
            current = {'hex_no': hex_no, 'line_no': line_no,
                       'line_pos': line_pos, 'short_title': short_title, 'full_title': rest,
                       'meta': '', 'content': [], 'story': '', 'comparison': ''}
        # PM domain H3 with XCASE: 'XCASE-HNN-LX｜最终X级' or 'XCASE-HNN-LX｜爻位｜title｜复查X'
        elif style == 'Heading 3' and re.match(r'^X(CASE|FIN|LIFE)-H\d', text):
            parts = text.split('｜')
            m = re.match(r'^X(?:CASE|FIN|LIFE)-H(\d{2})-L(\d)', text)
            hex_no = int(m.group(1)) if m else 0
            line_no = int(m.group(2)) if m else 0
            if len(parts) >= 4:
                # Detailed entry: 'XCASE-HNN-LX｜NN卦｜爻位｜title｜复查X'
                if current:
                    cases.append(current)
                line_pos = parts[2].strip()
                full_title = parts[3].strip()
                segs = full_title.rsplit(' ', 1)
                short_title = segs[-1] if len(segs) > 1 else full_title
                current = {'hex_no': hex_no, 'line_no': line_no,
                           'line_pos': line_pos, 'short_title': short_title, 'full_title': full_title,
                           'meta': text, 'content': [], 'story': '', 'comparison': ''}
            else:
                # Grade-only entry: 'XCASE-HNN-LX｜最终X级' — update current case's metadata
                if current:
                    if not current['meta']:
                        current['meta'] = text
                else:
                    current = {'hex_no': hex_no, 'line_no': line_no,
                               'line_pos': '', 'short_title': '', 'full_title': '',
                               'meta': text, 'content': [], 'story': '', 'comparison': ''}
        # PM domain: Heading 4 with title for the case
        elif current and style == 'Heading 4':
            parts = text.split('｜', 1)
            current['line_pos'] = parts[0].strip()
            if len(parts) > 1:
                rest = parts[1].strip()
                current['full_title'] = rest
                segs = rest.rsplit(' ', 1)
                current['short_title'] = segs[-1] if len(segs) > 1 else rest
            else:
                current['short_title'] = text
                current['full_title'] = text
        elif current and style == 'Normal':
            if text.startswith('案例 ') or text.startswith('case_id：') or text.startswith('case_id:'):
                if not current['meta']:
                    current['meta'] = text
                else:
                    current['content'].append(text)
            elif text.startswith('历史故事全文') or text.startswith('歷史故事全文'):
                if '｜' in text:
                    current['story'] = text.split('｜', 1)[1].strip()
            elif text.startswith('历史对照') or text.startswith('歷史對照'):
                if '｜' in text:
                    current['comparison'] = text.split('｜', 1)[1].strip()
            elif text.startswith('《小象》') or text.startswith('古籍原文') or text.startswith('简体中文译文') or text.startswith('既有繁體') or text.startswith('既有简体') or text.startswith('原事件與來源') or text.startswith('原事件与来源'):
                current['content'].append(text)
            elif text.startswith('适切性审查') or text.startswith('內容狀態') or text.startswith('内容状态') or text.startswith('publish_status') or text.startswith('本轮适切性') or text.startswith('本輪適切性'):
                pass
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_384_cn_en(doc):
    """CN 384 English: multiple formats — Heading 2 with 'NNN · ...' or 'Nth line | ...'"""
    cases = []
    current = None
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        # Format 1: Heading 2 'Nth line | ...' (PM)
        # Format 2: Heading 2 'NNN · Hexagram NN · Line N · Title' (EF)
        # Format 3: Heading 2 'NNN · XCASE/XLIFE-HNN-LX · Title' (WL)
        if style == 'Heading 2' and re.match(r'^\d{3}[\s·|]', text):
            if current:
                cases.append(current)
            m = re.match(r'^(\d{3})\s*[·|]\s*(.+)', text)
            if m:
                line_num = int(m.group(1))
                title = m.group(2).strip()
            else:
                line_num = 0
                title = text
            current = {'title': title, 'meta': '', 'tag': '', 'content': [],
                       'story_paras': [], 'comparison': '', 'hex_no': 0, 'line_no': 0,
                       'line_num': line_num}
        elif style == 'Heading 2':
            # Catch all remaining Heading 2 entries as case titles
            if current:
                cases.append(current)
            current = {'title': text, 'meta': '', 'tag': '', 'content': [],
                       'story_paras': [], 'comparison': '', 'hex_no': 0, 'line_no': 0,
                       'line_num': 0}
        elif current and style == 'Normal':
            if 'case_id' in text and ('XCASE' in text or 'XFIN' in text or 'XLIFE' in text):
                m = re.search(r'X(?:CASE|FIN|LIFE)-H(\d{2})-L(\d)', text)
                if m:
                    current['hex_no'] = int(m.group(1))
                    current['line_no'] = int(m.group(2))
                if not current['meta']:
                    current['meta'] = text
                else:
                    current['content'].append(text)
            elif 'case_id' in text.lower() and 'grade' in text.lower():
                if not current['meta']:
                    current['meta'] = text
            elif re.match(r'^E\d{2}\s', text):
                current['story_paras'].append(text)
            elif text.startswith('Line-specific comparison'):
                current['comparison'] = text.split('comparison', 1)[-1].strip(' :|') if 'comparison' in text.lower() else text
                current['content'].append(text)
            elif text.startswith('Selected historical event') or text.startswith('The Lesser Image') or text.startswith('Source coverage') or text.startswith('Source trace') or text.startswith('Editorial flags') or text.startswith('Fidelity') or text.startswith('source_trace') or text.startswith('source_batch'):
                pass
            else:
                current['content'].append(text)
        elif current and style == 'Heading 3':
            current['content'].append(text)
        elif current and style == 'Heading 1':
            # Skip section headers like 'Hexagram 01 · Six line cases'
            pass
    if current:
        cases.append(current)
    return cases

def parse_384_eu_zhtw(doc):
    """EU 384 zhTW: Heading 2 = '第N卦...', Heading 3 = 'NNN｜title'"""
    cases = []
    current = None
    current_hex = 0
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 2' and re.match(r'^第\d+卦', text):
            m = re.match(r'^第(\d+)卦', text)
            current_hex = int(m.group(1)) if m else 0
        elif style == 'Heading 3' and re.match(r'^\d{3}｜', text):
            if current:
                cases.append(current)
            m2 = re.match(r'^(\d{3})｜(.+)', text)
            line_num = int(m2.group(1)) if m2 else 0
            title = m2.group(2) if m2 else text
            current = {'line_num': line_num, 'hex_no': current_hex, 'title': title,
                       'meta': '', 'tag': '', 'content': [],
                       'story': '', 'comparison': ''}
        elif current and style == 'Normal':
            if text.startswith('案例識別碼') or text.startswith('案例编号'):
                current['meta'] = text
            elif text.startswith('歷史故事') or text.startswith('历史事件'):
                if '｜' in text:
                    current['story'] = text.split('｜', 1)[1].strip()
                else:
                    current['story'] = text
            elif text.startswith('逐爻對照') or text.startswith('逐爻对照'):
                if '｜' in text:
                    current['comparison'] = text.split('｜', 1)[1].strip()
                else:
                    current['comparison'] = text
            elif text.startswith('原評級') or text.startswith('原评级') or text.startswith('地點') or text.startswith('地点') or text.startswith('──') or text.startswith('爻辭') or text.startswith('爻辞') or text.startswith('小象'):
                pass
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_384_eu_zhs(doc):
    """EU 384 zhHS: Heading 1 = '第N卦...', Heading 2 = 'NNN｜title'"""
    cases = []
    current = None
    current_hex = 0
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 1' and re.match(r'^第\d+卦', text):
            m = re.match(r'^第(\d+)卦', text)
            current_hex = int(m.group(1)) if m else 0
        elif style == 'Heading 2' and re.match(r'^\d{3}｜', text):
            if current:
                cases.append(current)
            m2 = re.match(r'^(\d{3})｜(.+)', text)
            line_num = int(m2.group(1)) if m2 else 0
            title = m2.group(2) if m2 else text
            current = {'line_num': line_num, 'hex_no': current_hex, 'title': title,
                       'meta': '', 'tag': '', 'content': [],
                       'story': '', 'comparison': ''}
        elif current and style == 'Normal':
            if text.startswith('案例编号') or text.startswith('案例識別碼'):
                current['meta'] = text
            elif text.startswith('历史事件') or text.startswith('歷史故事'):
                if '｜' in text:
                    current['story'] = text.split('｜', 1)[1].strip()
                else:
                    current['story'] = text
            elif text.startswith('逐爻对照') or text.startswith('逐爻對照'):
                if '｜' in text:
                    current['comparison'] = text.split('｜', 1)[1].strip()
                else:
                    current['comparison'] = text
            elif text.startswith('原评级') or text.startswith('原評級') or text.startswith('──') or text.startswith('爻辞') or text.startswith('爻辭') or text.startswith('小象'):
                pass
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

def parse_384_eu_en(doc):
    """EU 384 English: Heading 2 = 'Hexagram N', Heading 3 = 'NNN｜title'"""
    cases = []
    current = None
    current_hex = 0
    for p in doc.paragraphs:
        text = p.text.strip()
        style = p.style.name
        if not text:
            continue
        if style == 'Heading 2' and re.match(r'^Hexagram\s+\d+', text):
            m = re.match(r'^Hexagram\s+(\d+)', text)
            current_hex = int(m.group(1)) if m else 0
        elif style == 'Heading 3' and re.match(r'^\d{3}｜', text):
            if current:
                cases.append(current)
            m2 = re.match(r'^(\d{3})｜(.+)', text)
            line_num = int(m2.group(1)) if m2 else 0
            title = m2.group(2) if m2 else text
            current = {'line_num': line_num, 'hex_no': current_hex, 'title': title,
                       'meta': '', 'tag': '', 'content': [],
                       'story': '', 'comparison': ''}
        elif current and style == 'Normal':
            if text.startswith('Case ID'):
                current['meta'] = text
            elif text.startswith('Historical Event'):
                if '｜' in text:
                    current['story'] = text.split('｜', 1)[1].strip()
                else:
                    current['story'] = text.replace('Historical Event', '').strip(' |')
            elif text.startswith('Line-Specific Comparison'):
                if '｜' in text:
                    current['comparison'] = text.split('｜', 1)[1].strip()
                else:
                    current['comparison'] = text.replace('Line-Specific Comparison', '').strip(' |')
            elif text.startswith('Line') or text.startswith('Xiaoxiang') or text.startswith('Location') or text.startswith('Prior Grade') or text.startswith('──'):
                pass
            else:
                current['content'].append(text)
    if current:
        cases.append(current)
    return cases

# ── HTML generation ──

def gen_64_accordion(cases, region, lang):
    data_cat = region + "-64"
    items = []
    for c in cases:
        title = escape(c['title'])
        tag = escape(c.get('tag', '') or '')
        meta = escape(c.get('meta', ''))
        content_paras = '\n  '.join('<p>' + escape(p) + '</p>' for p in c['content'])
        item = '<div class="acc-item" data-cat="' + data_cat + '"><div class="acc-header"><span>' + title + '</span><span class="acc-arrow">▶</span></div><div class="acc-body"><div class="case-entry">\n  <h4>' + title + '</h4>\n  <div class="case-meta"><span class="case-tag">' + tag + '</span> ' + meta + '</div>\n  ' + content_paras + '\n</div></div></div>'
        items.append(item)
    return '\n'.join(items)

def gen_384_accordion(cases, region, lang):
    data_cat = region + "-384"
    hex_names = {'zhTW': HEX_TW, 'zhHS': HEX_HS, 'en': HEX_EN}
    hn = hex_names.get(lang, HEX_TW)
    items = []
    for c in cases:
        if 'line_num' in c and c['line_num']:
            line_num = c['line_num']
            hex_no = c['hex_no']
            hex_name = hn[hex_no - 1] if 0 < hex_no <= 64 else ''
            line_pos = c.get('line_pos', '') or LINE_POS[c.get('line_no', 1) - 1] if c.get('line_no', 0) else ''
            short_title = c.get('title', '') or c.get('short_title', '')
            if lang == 'en':
                header_title = '%03d Line  H%02d %s  %s' % (line_num, hex_no, hex_name, short_title)
            else:
                header_title = '第%03d爻  %02d %s  %s  %s' % (line_num, hex_no, hex_name, line_pos, short_title)
            h4_title = (line_pos + '｜' + short_title) if line_pos else short_title
            tag = '%03d爻' % line_num if lang in ('zhTW', 'zhHS') else '%03d' % line_num
            meta = escape(c.get('meta', ''))
            content_parts = []
            story = c.get('story', '')
            if story:
                for para in story.split('\n\n'):
                    para = para.strip()
                    if para:
                        content_parts.append('<p>' + escape(para) + '</p>')
            comparison = c.get('comparison', '')
            if comparison:
                content_parts.append('<p>' + escape(comparison) + '</p>')
            for p in c.get('content', []):
                content_parts.append('<p>' + escape(p) + '</p>')
            content_html = '\n  '.join(content_parts)
        elif 'hex_no' in c and c['hex_no']:
            hex_no = c['hex_no']
            line_no = c['line_no']
            line_num = (hex_no - 1) * 6 + line_no
            hex_name = hn[hex_no - 1] if 0 < hex_no <= 64 else ''
            line_pos = c.get('line_pos', '') or LINE_POS[line_no - 1] if line_no else ''
            short_title = c.get('short_title', '') or c.get('full_title', '')
            if lang == 'en':
                header_title = '%03d Line  H%02d %s  %s' % (line_num, hex_no, hex_name, short_title)
            else:
                header_title = '第%03d爻  %02d %s  %s  %s' % (line_num, hex_no, hex_name, line_pos, short_title)
            h4_title = (line_pos + '｜' + short_title) if line_pos else short_title
            tag = '%03d爻' % line_num if lang in ('zhTW', 'zhHS') else '%03d' % line_num
            meta = escape(c.get('meta', ''))
            content_parts = []
            story = c.get('story', '')
            if story:
                for para in story.split('\n\n'):
                    para = para.strip()
                    if para:
                        content_parts.append('<p>' + escape(para) + '</p>')
            comparison = c.get('comparison', '')
            if comparison:
                content_parts.append('<p>' + escape(comparison) + '</p>')
            for p in c.get('content', []):
                content_parts.append('<p>' + escape(p) + '</p>')
            content_html = '\n  '.join(content_parts)
        else:
            title = escape(c.get('title', ''))
            tag = escape(c.get('tag', '') or '')
            meta = escape(c.get('meta', ''))
            content_parts = []
            for sp_ in c.get('story_paras', []):
                content_parts.append('<p>' + escape(sp_) + '</p>')
            if c.get('comparison'):
                content_parts.append('<p>' + escape(c['comparison']) + '</p>')
            for p in c.get('content', []):
                content_parts.append('<p>' + escape(p) + '</p>')
            content_html = '\n  '.join(content_parts)
            header_title = title
            h4_title = title
        item = '<div class="acc-item" data-cat="' + data_cat + '"><div class="acc-header"><span>' + escape(header_title) + '</span><span class="acc-arrow">▶</span></div><div class="acc-body"><div class="case-entry">\n  <h4>' + escape(h4_title) + '</h4>\n  <div class="case-meta"><span class="case-tag">' + escape(tag) + '</span> ' + meta + '</div>\n  ' + content_html + '\n</div></div></div>'
        items.append(item)
    return '\n'.join(items)

def gen_page(domain, region, dtype, lang, accordion_html):
    filename = 'case-' + domain + '-' + region + '-' + dtype + '.html'
    labels = LABELS[(domain, region, dtype)]
    label = labels[lang]
    title = label + ' — YiWord 易理'
    if lang == 'zhTW':
        html_lang = 'zh-Hant'
        css_href = 'style.css'
        lang_switch = '<a href="cn/' + filename + '">简中</a> <a href="' + filename + '" class="active">繁中</a> <a href="en/' + filename + '">EN</a>'
        nav_items = [('index.html','首頁'),('introduction.html','易經介紹'),('hexagrams.html','六十四卦'),
            ('wings.html','易傳十翼'),('cases.html','案例'),('divination.html','占卜'),
            ('terms.html','名詞索引'),('search.html','搜尋'),('about.html','關於')]
        back_home = '⌂ 首頁'
        back_text = '← 回上頁'
        footer_links = '<a href="privacy.html">隱私權政策</a> · <a href="terms-of-use.html">使用條款</a>'
        home_link = 'index.html'
    elif lang == 'zhHS':
        html_lang = 'zh-Hans'
        css_href = '../style.css'
        lang_switch = '<a href="' + filename + '" class="active">简中</a> <a href="../' + filename + '">繁中</a> <a href="../en/' + filename + '">EN</a>'
        nav_items = [('../cn/index.html','首页'),('../cn/introduction.html','易经介绍'),('../cn/hexagrams.html','六十四卦'),
            ('../cn/wings.html','易传十翼'),('../cn/cases.html','案例'),('../cn/divination.html','占卜'),
            ('../cn/terms.html','名词索引'),('../cn/search.html','搜索'),('../cn/about.html','关于')]
        back_home = '⌂ 首页'
        back_text = '← 回上页'
        footer_links = '<a href="../cn/privacy.html">隐私权政策</a> · <a href="../cn/terms-of-use.html">使用条款</a>'
        home_link = '../cn/index.html'
    else:
        html_lang = 'en'
        css_href = '../style.css'
        lang_switch = '<a href="../cn/' + filename + '">简中</a> <a href="../' + filename + '">繁中</a> <a href="' + filename + '" class="active">EN</a>'
        nav_items = [('../cn/index.html','Home'),('../cn/introduction.html','Introduction'),('../cn/hexagrams.html','64 Hexagrams'),
            ('../cn/wings.html','Ten Wings'),('../cn/cases.html','Cases'),('../cn/divination.html','Divination'),
            ('../cn/terms.html','Glossary'),('../cn/search.html','Search'),('../cn/about.html','About')]
        back_home = '⌂ Home'
        back_text = '← Back'
        footer_links = '<a href="../cn/privacy.html">Privacy Policy</a> · <a href="../cn/terms-of-use.html">Terms of Use</a>'
        home_link = '../cn/index.html'

    nav_html = '\n'.join(
        '<li><a href="{}"{}>{}</a></li>'.format(u, ' class="active"' if t in ('案例','Cases') else '', t)
        for u, t in nav_items
    )

    html = '<!DOCTYPE html>\n<html lang="' + html_lang + '">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>' + escape(title) + '</title>\n<link rel="stylesheet" href="' + css_href + '">\n</head>\n<body>\n'
    html += '<header><div class="brand">YiWord <span>易理 = 處世之道</span></div><div class="lang-switch">' + lang_switch + '</div></header>\n'
    html += '<nav><ul>\n' + nav_html + '\n</ul></nav>\n'
    html += '<main>\n'
    html += '<div class="back-nav"><a href="' + home_link + '">' + back_home + '</a><a href="javascript:history.back()">' + back_text + '</a></div>\n'
    html += '<div class="hex-num-label">' + escape(label) + '</div>\n'
    html += '<div class="acc-list">\n' + accordion_html + '\n</div>\n'
    html += JS_CODE + '\n</main>\n'
    html += '<footer><p>© 2026 YiWord.com · ' + footer_links + '</p></footer>\n'
    html += '</body>\n</html>'
    return html

def build_all():
    files_built = []
    total_cases = 0
    for domain in ['political', 'economic', 'workplace']:
        for region in ['cn', 'eu']:
            for dtype in ['64', '384']:
                filename = 'case-' + domain + '-' + region + '-' + dtype + '.html'
                for lang in ['zhTW', 'zhHS', 'en']:
                    src_map = SRC_64 if dtype == '64' else SRC_384
                    src_file = src_map[region][lang][DOMAIN_MAP[domain]]
                    if not os.path.exists(src_file):
                        print('  WARNING: Missing: ' + src_file)
                        continue
                    doc = Document(src_file)
                    if dtype == '64':
                        if region == 'cn':
                            if lang in ('zhTW', 'zhHS'):
                                if DOMAIN_MAP[domain] == 'WL' and lang == 'zhHS':
                                    cases = parse_64_cn_zhs_wl(doc)
                                else:
                                    cases = parse_64_cn_zh(doc, lang)
                            else:
                                cases = parse_64_cn_en(doc)
                        else:
                            if lang in ('zhTW', 'zhHS'):
                                cases = parse_64_eu_cn(doc, lang)
                            else:
                                cases = parse_64_eu_en(doc)
                        accordion = gen_64_accordion(cases, region, lang)
                    else:
                        if region == 'cn':
                            if lang == 'zhTW':
                                cases = parse_384_cn_zhtw(doc)
                            elif lang == 'zhHS':
                                cases = parse_384_cn_zhs(doc)
                            else:
                                cases = parse_384_cn_en(doc)
                        else:
                            if lang == 'zhTW':
                                cases = parse_384_eu_zhtw(doc)
                            elif lang == 'zhHS':
                                cases = parse_384_eu_zhs(doc)
                            else:
                                cases = parse_384_eu_en(doc)
                        accordion = gen_384_accordion(cases, region, lang)
                    html = gen_page(domain, region, dtype, lang, accordion)
                    if lang == 'zhTW':
                        out_path = os.path.join(BASE, filename)
                    elif lang == 'zhHS':
                        out_path = os.path.join(BASE, 'cn', filename)
                    else:
                        out_path = os.path.join(BASE, 'en', filename)
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(html)
                    files_built.append(out_path)
                    n = len(cases) if cases else 0
                    total_cases += n
                    print('  ✓ ' + lang + ' ' + filename + ': ' + str(n) + ' cases')
    return files_built, total_cases

if __name__ == '__main__':
    print('Building all 36 case sub-pages from V4.3 sources...')
    files, total = build_all()
    print('\nDone: ' + str(len(files)) + ' files built, ' + str(total) + ' total cases')
