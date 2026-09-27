import json
g = json.load(open('../build/final_graph.json')); pools = json.load(open('../build/pools.json'))
T = g['titles']; CATS = g['cats']
tl = sorted({tr for t in T for tr in t['traits']}); ti = {t: i for i, t in enumerate(tl)}
CC = {'mechanic': 0, 'theme': 1, 'setting': 2, 'trope': 3, 'icon': 4, 'story': 5}
out_t = []; H = {}
for i, t in enumerate(T):
    al = [a for a in t.get('aliases', []) if a and a != t['label']][:4]
    out_t.append([t['label'], {'anime': 0, 'game': 1, 'movie': 2}[t['media']], t.get('year') or 0, [ti[x] for x in t['traits']], al, t['franchise'], t['pop']])
    for tr, d in (t.get('hand') or {}).items():
        if d and tr in ti: H[f"{i},{ti[tr]}"] = d
P = {}
for k, lst in pools.items():
    seen = set(); keep = []
    for p in lst:
        key = frozenset((p[0], p[-1]))
        if key in seen: continue
        seen.add(key); keep.append(p)
    if k in ('hard', 'expert'):
        keep.sort(key=lambda p: max(T[p[0]]['pop'], T[p[-1]]['pop']) - 0.001 * (len(T[p[0]]['traits']) + len(T[p[-1]]['traits'])))
    P[k] = keep
data = dict(t=out_t, r=tl, c=[CC.get(CATS.get(x, 'trope'), 3) for x in tl], h=H, p=P)
s = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
open('../data/pack.json', 'w').write(s)
print(len(out_t), 'titles', len(tl), 'traits', {k: len(v) for k, v in P.items()}, round(len(s.encode()) / 1e6, 2), 'MB')
