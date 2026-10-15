#!/usr/bin/env python3
"""Generate trilingual hexagram HTML pages from extracted JSON data."""
import json, os, html

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SITE_DIR, 'docs')

LANGS = {
    'zh_hant': {'code': 'zh-Hant', 'dir': '', 'nav': ['首頁','易經介紹','六十四卦','易傳十翼','名詞索引','搜尋','關於'],
                'pages': ['index.html','introduction.html','hexagrams.html','wings.html','terms.html','search.html','about.html'],
                'label_orig': '原文', 'label_trans': '翻譯', 'label_judgment': '卦辭', 'label_lines': '爻辭',
                'label_trigram': '卦象', 'label_upper': '上卦', 'label_lower': '下卦',
                'note': '原文待校勘；翻譯陸續增修。', 'footer': '© 2026 YiWord.com'},
    'zh_hans': {'code': 'zh-Hans', 'dir': 'cn', 'nav': ['首页','易经介绍','六十四卦','易传十翼','名词索引','搜索','关于'],
                'pages': ['index.html','introduction.html','hexagrams.html','wings.html','terms.html','search.html','about.html'],
                'label_orig': '原文', 'label_trans': '翻译', 'label_judgment': '卦辞', 'label_lines': '爻辞',
                'label_trigram': '卦象', 'label_upper': '上卦', 'label_lower': '下卦',
                'note': '原文待校勘；翻译陆续增修。', 'footer': '© 2026 YiWord.com'},
    'en': {'code': 'en', 'dir': 'en', 'nav': ['Home','Introduction','64 Hexagrams','Ten Wings','Glossary','Search','About'],
                'pages': ['index.html','introduction.html','hexagrams.html','wings.html','terms.html','search.html','about.html'],
                'label_orig': 'Original', 'label_trans': 'Translation', 'label_judgment': 'Judgment', 'label_lines': 'Line Texts',
                'label_trigram': 'Trigram', 'label_upper': 'Upper', 'label_lower': 'Lower',
                'note': 'Original text pending collation; translations under continuous revision.', 'footer': '© 2026 YiWord.com'},
}

# Load all three language JSON files
data = {}
for lang in LANGS:
    fname = f'zhouyi_{lang}.json'
    fpath = os.path.join(DATA_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            data[lang] = json.load(f)
        print(f'Loaded {lang}: {len(data[lang])} hexagrams')
    else:
        print(f'WARNING: {fpath} not found!')

def esc(text):
    return html.escape(text) if text else ''

def generate_hexagram_page(lang, hex_id, h_data, all_data):
    L = LANGS[lang]
    d = L['dir']
    prefix = '../' if d else ''
    css_prefix = '../' if d else ''
    
    hex_name = h_data.get('name', '')
    uni = h_data.get('unicode', '')
    units = h_data.get('units', {})
    
    # Language switch
    lang_switch = ''
    for sl, slabel in [('zh_hant', '繁中'), ('zh_hans', '简中'), ('en', 'EN')]:
        sd = LANGS[sl]['dir']
        sp = '../' if sd else ''
        if sd == d:
            lang_switch += f'<a href="{sp}hexagram/{hex_id.lower()}.html" class="active">{slabel}</a> '
        else:
            lang_switch += f'<a href="{sp}hexagram/{hex_id.lower()}.html">{slabel}</a> '
    
    # Nav
    nav_items = ''
    for i, label in enumerate(L['nav']):
        page = L['pages'][i]
        if page == 'hexagrams.html':
            nav_items += f'<li><a href="{prefix}{page}" class="active">{label}</a></li>'
        else:
            nav_items += f'<li><a href="{prefix}{page}">{label}</a></li>'
    
    # Units HTML
    units_html = ''
    for uid in sorted(units.keys()):
        u = units[uid]
        orig = esc(u.get('original', ''))
        trans = esc(u.get('translation', ''))
        label = esc(u.get('label', ''))
        units_html += f'''<div class="card">
<h3>{label} <span class="small">{uid}</span></h3>
<div class="cite-box"><p><strong>{L["label_orig"]}：</strong>{orig}</p></div>
<p><strong>{L["label_trans"]}：</strong>{trans}</p>
</div>
'''
    
    page_html = f'''<!DOCTYPE html>
<html lang="{L["code"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{hex_name} {uni} — YiWord</title>
<link rel="stylesheet" href="{css_prefix}style.css">
</head>
<body>
<header>
  <div class="brand">YiWord <span>易理</span></div>
  <div class="lang-switch">{lang_switch}</div>
</header>
<nav><ul>{nav_items}</ul></nav>
<main>
<h1>{uni} {hex_name}</h1>
<p class="small">{L["note"]} · hexagram_id: {hex_id} · text_version: zhouyi-{lang}-1.0.0 · review_status: draft</p>
{units_html}
</main>
<footer><p>{L["footer"]} · <a href="{prefix}privacy.html">{'隱私權政策' if lang=='zh_hant' else '隐私政策' if lang=='zh_hans' else 'Privacy'}</a> · <a href="{prefix}terms.html">{'使用條款' if lang=='zh_hant' else '使用条款' if lang=='zh_hans' else 'Terms'}</a></p></footer>
</body>
</html>'''
    return page_html

# Generate pages for each language
total_generated = 0
for lang in LANGS:
    if lang not in data:
        continue
    L = LANGS[lang]
    hex_dir = os.path.join(SITE_DIR, L['dir'], 'hexagram') if L['dir'] else os.path.join(SITE_DIR, 'hexagram')
    os.makedirs(hex_dir, exist_ok=True)
    
    for hex_id in sorted(data[lang].keys()):
        h_data = data[lang][hex_id]
        page_html = generate_hexagram_page(lang, hex_id, h_data, data)
        out_path = os.path.join(hex_dir, f'{hex_id.lower()}.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
        total_generated += 1

print(f'\nTotal pages generated: {total_generated}')
print(f'zh-Hant: {len(os.listdir(os.path.join(SITE_DIR, "hexagram")))} files')
print(f'zh-Hans: {len(os.listdir(os.path.join(SITE_DIR, "cn", "hexagram")))} files')
print(f'English: {len(os.listdir(os.path.join(SITE_DIR, "en", "hexagram")))} files')
