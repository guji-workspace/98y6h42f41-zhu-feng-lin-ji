"""明别集丛刊版面 OCR（bbox.html）→ 不分行参校本语料（只留汉字，一块一行）。
用法：python3 clean_mbj_ocr.py <bbox.html> <起始标题> <终止标题> <输出.txt>
去掉：Page-Header（丛刊书眉）、Page-Footer（丛刊页码）、Image；版心文字（书名/卷次/叶码）；标点等非汉字。
"""
import html, re, sys, unicodedata
src, start_title, end_title, out = sys.argv[1:5]
raw = open(src, encoding='utf-8').read()
secs = re.findall(r'<section data-page="(\d+)"[^>]*>(.*?)</section>', raw, re.S)
NUM = '一二三四五六七八九十百'
BANXIN = re.compile(rf'^(朱楓林集?[{NUM}]*(序|目[錄録])?[{NUM}]*|朱楓林集?[{NUM}]*(卷之[{NUM}]*)?[{NUM}]*|／?卷之[{NUM}]*|目[錄録]|序|[{NUM}]{{1,4}})$')
EDITION_LINES = {'明萬曆歙邑朱氏刻本'}
def han(s):
    return ''.join(ch for ch in s if unicodedata.category(ch) == 'Lo' or 0x2E80 <= ord(ch) <= 0x2FDF)
started = False; lines = []; pages = []; drop = {'banxin': 0, 'header': 0, 'footer': 0, 'image': 0}
for pg, body in secs:
    blocks = re.findall(r'<div data-label="([^"]+)" data-bbox="([^"]+)">(.*?)</div>', body, re.S)
    pw = None
    m = re.search(r'data-page-box="(\d+) (\d+)"', raw[raw.find(f'data-page="{pg}"'):][:80])
    pw = int(m.group(1)) if m else 1273
    for label, bbox, txt in blocks:
        x0, y0, x1, y1 = map(int, bbox.split())
        center = abs((x0 + x1) / 2 - pw / 2) < 60 and (x1 - x0) < 80
        t = html.unescape(re.sub(r'<br/>', '\n', re.sub(r'<(?!br/)[^>]+>', '', txt)))
        flat = re.sub(r'\s+', '', t)
        if not started:
            if label == 'Section-Header' and flat == start_title: started = True; pages.append(int(pg))
            continue
        if label == 'Section-Header' and flat == end_title:
            started = None; break
        if re.match(r'^[（(]?明[)）]?\S{2,4}[著撰]$', flat):   # 丛刊下一种的题署页
            drop.setdefault('next_title', 0); drop['next_title'] += 1; continue
        if label == 'Page-Header': drop['header'] += 1; continue
        if label == 'Page-Footer': drop['footer'] += 1; continue
        if label == 'Image': drop['image'] += 1; continue
        if BANXIN.match(flat) and (label == 'Text' or center): drop['banxin'] += 1; continue
        if flat in EDITION_LINES: drop.setdefault('edition', 0); drop['edition'] += 1; continue
        h = han(flat)
        if h: lines.append(h)
    if started is None: pages.append(int(pg)); break
# 正文里粘进来的版心（「…田孫朱楓林集卷之三十四氏居焉…」）：行中出现的书名＋卷次＋叶码一律删
GLUED = re.compile(rf'(?<=.)朱楓林集(卷之[{NUM}]+)?[{NUM}]*(?!終)')
seen = set(); clean = []
for h in lines:
    h2 = GLUED.sub('', h) if len(h) > 8 else h
    if h2 != h: drop.setdefault('glued_banxin', 0); drop['glued_banxin'] += 1
    # 卷端题「朱楓林集卷之N」只出现一次，再出现是版心
    if re.fullmatch(rf'朱楓林集卷之[{NUM}]+', h2):
        if h2 in seen: drop['banxin'] += 1; continue
        seen.add(h2)
    if h2: clean.append(h2)
lines = clean
with open(out, 'w', encoding='utf-8') as f:
    f.write(f'# 朱楓林集十卷 參校本：明別集叢刊第一輯第一冊（黃山書社 2013 影印）版面 OCR 清理稿。不分行（line_is_column: false）。'
            f'丛刊页 {pages[0]}–{pages[-1]}；去书眉、页码、图片、版心文字与标点；只留汉字，一块一行。抽 3 页校得约 98%。\n')
    f.write('\n'.join(lines) + '\n')
print('pages', pages, 'lines', len(lines), 'chars', sum(map(len, lines)), 'dropped', drop)
