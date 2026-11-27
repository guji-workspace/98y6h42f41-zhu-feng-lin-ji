"""格高合理性检查（实验版）：按页格高 period、页参考列宽 ref_w 判明显不合理的字框。"""
import json,glob,sys,collections
P=sys.argv[1] if len(sys.argv)>1 else '_packs/rev-001-r0/01/'
pend={c['cell']:c['pending_reason'] for c in json.load(open('reports/01/_publish/001-r0/001.pending.json'))['cells']}
votes={json.loads(l)['id'].split(':',1)[1]:json.loads(l)['v'] for l in open('/tmp/claude-0/votes01/drafts.jsonl')}
hits=[]
for f in sorted(glob.glob(P+'cell_shrink/p*.json')):
    pg=int(f[-9:-5]); g=json.load(open(P+f'cut_gate/p{pg:04d}.json'))['gate_manifest']
    per,rw=g.get('period'),g.get('ref_w')
    if not per: continue
    for c in json.load(open(f))['char_index']['columns']:
        ch=[x for x in c['chars'] if x.get('cell_type')=='char']
        main=[x for x in ch if not x.get('sub')]
        for i,x in enumerate(ch):
            h,w=x['height']/per,x['width']/rw; why=[]
            if x.get('sub'):  # 双行小注半格只查极端
                if h>1.6: why.append('tall')
            else:
                if h<0.12 and w>=0.6: why.append('frame_line')       # 扁长一条：框线/界行残段
                elif h<0.25 and w<0.25: why.append('speck')          # 又矮又窄：墨点
                if h>1.6: why.append('tall')                         # 一框超过 1.6 格高：两字并一框或污渍
                if 0.12<=h<0.62 and w<0.85:                           # 半截字：与上/下邻框合起来像一个字
                    j=main.index(x) if x in main else -1
                    for k in (j-1,j+1):
                        if 0<=k<len(main) and j>=0:
                            y=main[k]; top=min(x['bbox_page'][1],y['bbox_page'][1]); bot=max(x['bbox_page'][3],y['bbox_page'][3])
                            if y['height']/per<0.9 and (bot-top)/per<1.25: why.append('split_pair'); break
            if why: hits.append((pg,x['id'].split(':',1)[1],why,round(h,2),round(w,2)))
cnt=collections.Counter()
for pg,cid,why,h,w in hits:
    k=(why[0], 'pending' if cid in pend else 'AUTO', 'voted:'+votes.get(cid,'-'))
    cnt[k]+=1
for k,v in sorted(cnt.items()): print(k,v)
print('--- 自动放行里被判的：')
for pg,cid,why,h,w in hits:
    if cid not in pend: print(cid,why,h,w)
print('--- 网站标了切坏/非字、本检查没抓到：')
hit_ids={h[1] for h in hits}
for cid,v in votes.items():
    if v in('seg_defect','not_a_char') and cid not in hit_ids: print(cid,v,pend.get(cid))
