#!/usr/bin/env python3
"""Build a self-contained HTML checklist (work/review/checklist.html) of the unresolved close calls
listed in tools/review_items.json, with an image crop at each spot. Needs Pillow
(~/.venvs/lds-transcribe/bin/python). The page stores decisions in the browser (localStorage) and can
export them as text.

Each crop is located by an estimate (where the quoted text falls in the page's text), so the mark can
be a few lines above or below the middle of the crop: use the whole-page link when in doubt.
"""
import base64, io, json, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ITEMS = json.loads((ROOT / 'tools' / 'review_items.json').read_text(encoding='utf-8'))
OUT = ROOT / 'work' / 'review'
OUT.mkdir(parents=True, exist_ok=True)


def body_text(p):
    t = (ROOT / 'book-of-mormon-1837-pages' / f'page-{p:03d}.md').read_text(encoding='utf-8')
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'\n---\n.*', '', t, flags=re.S)
    lines = [l for l in t.split('\n') if l.strip() and not l.startswith(('**Header', '#', 'Footer'))]
    return re.sub(r'\s+', ' ', ' '.join(lines)).replace('*', '')


def crop(p, needle):
    im = Image.open(ROOT / 'source' / f'{p:03d}.jpg').convert('L')
    w, h = im.size
    body = body_text(p)
    key = re.sub(r'\s+', ' ', needle.replace('*', ''))
    i = body.find(key) if key else -1
    frac = (i + len(key) / 2) / max(1, len(body)) if i >= 0 else 0.5
    cy = int(h * (0.10 + 0.80 * frac))
    half = 300
    top, bot = max(0, cy - half), min(h, cy + half)
    c = im.crop((0, top, w, bot))
    c = c.resize((int(c.width * 1.25), int(c.height * 1.25)), Image.LANCZOS)
    b = io.BytesIO(); c.save(b, 'JPEG', quality=68)
    return base64.b64encode(b.getvalue()).decode(), i >= 0


rows = []
for k, it in enumerate(ITEMS):
    data, found = crop(it['p'], it['n'])
    ctx = ''
    if it['n']:
        body = body_text(it['p']); key = re.sub(r'\s+', ' ', it['n'].replace('*', ''))
        i = body.find(key)
        ctx = body[max(0, i - 60): i + len(key) + 60] if i >= 0 else '(text not found in page file)'
    rows.append(f'''<section class="item" id="i{k}" data-k="{k}">
<h2>#{k+1} &middot; image {it['p']} <a href="../../source/{it['p']:03d}.jpg" target="_blank">whole page</a></h2>
<p class="q">{it['q']}</p>
<p class="ctx">file reads: <code>&hellip;{ctx}&hellip;</code> (current: <b>{it['cur']}</b>, other reading: <b>{it['alt']}</b>)</p>
<img src="data:image/jpeg;base64,{data}" alt="crop of image {it['p']}">
<p class="btn"><label><input type="radio" name="d{k}" value="keep"> keep ({it['cur']})</label>
<label><input type="radio" name="d{k}" value="change"> change to ({it['alt']})</label>
<label><input type="radio" name="d{k}" value="unsure"> can't tell</label>
<input type="text" name="n{k}" placeholder="note (optional)" size="40"></p></section>''')

html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Close calls review</title><style>
:root{--bg:#fff;--fg:#1c1c1c;--mu:#666;--bd:#ccc;--ac:#0b57d0}
@media (prefers-color-scheme: dark){:root{--bg:#161616;--fg:#e8e8e8;--mu:#999;--bd:#444;--ac:#8ab4f8}}
body{background:var(--bg);color:var(--fg);font:16px/1.45 system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:0 16px 80px}
.item{border-top:1px solid var(--bd);padding:12px 0}img{max-width:100%;height:auto;border:1px solid var(--bd);background:#fff}
.q{font-weight:600;margin:.2em 0}.ctx{color:var(--mu);margin:.2em 0}code{background:rgba(127,127,127,.15);padding:0 3px}
label{margin-right:16px}a{color:var(--ac)}.top{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--bd)}
button{font:inherit;padding:4px 12px}textarea{width:100%;height:160px;margin-top:8px}
</style></head><body>
<div class="top"><b>Close calls</b> &mdash; <span id="cnt"></span> decided
<button onclick="exp()">Export decisions</button></div>
<p>Pick what the original shows. The crop is centred on an <i>estimate</i> of where the mark is, a few lines either way; open the whole page if you do not see it. Colon: two round, equal dots. Semicolon: the lower dot has a tail.</p>
<textarea id="out" placeholder="exported decisions appear here (copy them back into the chat)"></textarea>
''' + '\n'.join(rows) + '''
<script>
const items=''' + json.dumps([{'p':i['p'],'n':i['n'],'cur':i['cur'],'alt':i['alt']} for i in ITEMS]) + ''';
const KEY="close-calls-1837";let s={};try{s=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}cnt()}
function cnt(){document.getElementById("cnt").textContent=Object.keys(s).filter(k=>s[k].d).length+" of "+items.length}
document.querySelectorAll(".item").forEach(sec=>{const k=sec.dataset.k;s[k]=s[k]||{};
 sec.querySelectorAll("input[type=radio]").forEach(r=>{if(s[k].d===r.value)r.checked=true;r.onchange=()=>{s[k].d=r.value;save()}});
 const t=sec.querySelector("input[type=text]");t.value=s[k].n||"";t.oninput=()=>{s[k].n=t.value;save()}});
cnt();
function exp(){const L=[];items.forEach((it,k)=>{const d=(s[k]||{}).d||"undecided";L.push("#"+(k+1)+" image "+it.p+" \\""+it.n+"\\": "+(d==="change"?"CHANGE to "+it.alt:d==="keep"?"keep "+it.cur:d)+((s[k]||{}).n?" ["+s[k].n+"]":""))});
 document.getElementById("out").value=L.join("\\n")}
</script></body></html>'''
(OUT / 'checklist.html').write_text(html, encoding='utf-8')
print(f'{len(ITEMS)} items -> {OUT / "checklist.html"}  ({(OUT / "checklist.html").stat().st_size // 1024} KB)')
