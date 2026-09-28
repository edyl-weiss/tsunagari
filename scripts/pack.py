import json
g = json.load(open('../build/final_graph.json')); pools = json.load(open('../build/pools.json'))
T = g['titles']; CATS = g['cats']
tl = sorted({tr for t in T for tr in t['traits']}); ti = {t: i for i, t in enumerate(tl)}
CC = {'mechanic': 0, 'theme': 1, 'setting': 2, 'trope': 3, 'icon': 4, 'story': 5}
import re
TH = json.load(open('../build/thumbs.json'))
# movie titles whose accents were lost in the IMDb CSV, plus a couple of truncated game names
FIX = {'Lon': 'Léon: The Professional', 'WALLE': 'WALL·E', 'Amlie': 'Amélie', 'Lt den rtte komma in': 'Let the Right One In',
  "La vie d'Adle": 'Blue Is the Warmest Colour', 'Kkaku Kidtai': 'Ghost in the Shell (1995)', 'Y tu mam tambin': 'Y Tu Mamá También',
  'Bhubali: The Beginning': 'Baahubali: The Beginning', 'Un prophte': 'A Prophet', ' bout de souffle': 'Breathless',
  'Un long dimanche de fianailles': 'A Very Long Engagement', 'Das weie Band - Eine deutsche Kindergeschichte': 'The White Ribbon',
  'Capharnam': 'Capernaum', '4 luni, 3 saptamni si 2 zile': '4 Months, 3 Weeks and 2 Days',
  'Shin seiki Evangelion Gekij-ban: Air/Magokoro wo, kimi ni': 'The End of Evangelion', 'Hvnen': 'In a Better World',
  'Le dner de cons': 'The Dinner Game', 'La montaa sagrada': 'The Holy Mountain', 'Jb ninpch': 'Ninja Scroll',
  'Omoide no Mn': 'When Marnie Was There', 'Tky goddofzzu': 'Tokyo Godfathers', 'D hng denglong gaogao gu': 'Raise the Red Lantern',
  'Death Note: Desu nto': 'Death Note (2006)', 'Joyeux Nol': 'Joyeux Noël', 'Hstsonaten': 'Autumn Sonata',
  'La rgle du jeu': 'The Rules of the Game', 'La plante sauvage': 'Fantastic Planet', 'Adams bler': "Adam's Apples",
  'La double vie de Vronique': 'The Double Life of Véronique', 'Grand Theft Auto IV: The': 'Grand Theft Auto IV', 'Nioh 2 – The': 'Nioh 2'}
out_t = []; H = {}
for i, t in enumerate(T):
    lab = FIX.get(t['label'], t['label'])
    al = [a for a in t.get('aliases', []) if a and a != t['label'] and a != lab and '\x1a' not in a and a not in FIX][:4]
    if lab != t['label'] and t['media'] == 'movie' and len(al) < 4: al.append(t['label'])   # keep the original spelling searchable
    out_t.append([lab, {'anime': 0, 'game': 1, 'movie': 2}[t['media']], t.get('year') or 0, [ti[x] for x in t['traits']], al, t['franchise'], t['pop'], TH[i]])
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
