import pickle,json,sys
from PIL import Image, ImageDraw, ImageFont
rows=pickle.load(open('cellfeat.pkl','rb'))
ch={}
for p in json.load(open('char.json'))['pages']:
    for c in p['columns']:
        for x in c['cells']: ch[x['a']]=x.get('c','')
d=json.load(open('cord.json')); P={p['page']:p for p in d['pages']}
def walk(o,out):
    if isinstance(o,dict):
        if 'a' in o and 'box' in o: out[o['a']]=o['box']
        for v in o.values(): walk(v,out)
    elif isinstance(o,list):
        for v in o: walk(v,out)
B={}
for pg,p in P.items(): b={}; walk(p,b); B.update(b)
font=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',18)
imgs={}
def img(pg):
    if pg not in imgs:
        s=P[pg]['image']['sha256']; imgs[pg]=Image.open(f'/root/.cache/guji-data/sha256/{s[:2]}/{s}.png').convert('RGB')
    return imgs[pg]
def sheet(name,hits):
    n=len(hits); cols=10; S=Image.new('RGB',(cols*170,((n+cols-1)//cols)*200),'white'); dr=ImageDraw.Draw(S)
    for i,a in enumerate(hits):
        x,y,w,h=B[a]; m=40; t=img(int(a.split(':')[0])).crop((x-m,y-m,x+w+m,y+h+m)); ImageDraw.Draw(t).rectangle([m,m,m+w,m+h],outline=(255,0,0),width=3)
        t.thumbnail((160,160)); X,Y=(i%cols)*170,(i//cols)*200; S.paste(t,(X+5,Y+30)); dr.text((X+5,Y+2),f"{a} {ch.get(a,'?')}",fill=(0,0,0),font=font)
    S.save(name)
