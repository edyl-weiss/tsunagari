import json,collections,re
from wordfreq import zipf_frequency
d=json.load(open('../build/aod.json'))['data']
d=[x for x in d if x['type'] in ('TV','MOVIE','ONA','OVA') and 'hentai' not in x.get('tags',[])]
urls={}
for i,x in enumerate(d):
    for u in x['sources']: urls[u]=i
def words(t): return [w for w in re.sub(r'[^a-z0-9 ]',' ',t.lower()).split() if w]
par=list(range(len(d)))
def f(a):
    while par[a]!=a: par[a]=par[par[a]]; a=par[a]
    return a
def related(a,b):
    wa,wb=words(a['title']),words(b['title'])
    if not wa or not wb: return False
    if wa[0]==wb[0] and len(wa[0])>=3: return True
    return False
for i,x in enumerate(d):
    for u in x.get('relatedAnime',[]):
        j=urls.get(u)
        if j is not None and related(x,d[j]): par[f(i)]=f(j)
groups=collections.defaultdict(list)
for i in range(len(d)): groups[f(i)].append(i)

def pop(x):
    s=(x.get('score') or {}).get('arithmeticGeometricMean') or 0
    p=min(len(x['synonyms']),30)+3*len(x['sources'])+s
    if {'short episodes','shorts'} & set(x.get('tags',[])): p-=15
    return p
ROMAJI=set('no wa ga wo ni to de na kun chan sama san sensei shoujo shounen koi ore boku watashi kimi hime tachi mo ka ya yo ne desu da naru suru shi mono monogatari kara made yuusha maou tensei seishun gakuen sekai kamisama'.split())
BAD=re.compile(r'(season|\bpart\b|\bmovie\b|special|\btv\b|\bova\b|\bona\b|\b\d+(st|nd|rd|th)\b|\bs\d+\b|\bvol\b|recap|picture drama|\bpv\b|\bcm\b)',re.I)
OTH=['fr','es','de','it','pt']
_ec={}
def is_en(w):
    if w in _ec: return _ec[w]
    if w.isdigit(): r=True
    elif w in ROMAJI: r=False
    else:
        e=zipf_frequency(w,'en'); o=max(zipf_frequency(w,l) for l in OTH)
        r= e>3.0 and e>=o-0.3
    _ec[w]=r; return r
def en_words(s): return [w for w in words(s) if is_en(w)]
def label_score(c):
    ws=words(c)
    if not ws or not c.isascii() or len(c)<3 or len(c)>70: return -9
    ew=en_words(c); frac=len(ew)/len(ws)
    sc=frac*2+min(len(ws),5)*0.12
    if BAD.search(c): sc-=1.5
    if len(c)<=5: sc-=2.0
    if len([w for w in ew if len(w)>=4])==0: sc-=1
    if c==c.lower(): sc-=0.8
    return sc
def clean(c):
    c=re.sub(r'\s*[\(\[][^)\]]*[\)\]]\s*$','',c)
    c=re.sub(r'[\s:-]*(season\s*\d+|\d+(st|nd|rd|th)\s*season|part\s*\d+|final season.*)$','',c,flags=re.I).strip(' :-')
    return c
out=[]
for g in groups.values():
    ents=[d[i] for i in g]
    tv=[e for e in ents if e['type'] in('TV','ONA')] or ents
    top=max(pop(e) for e in tv)
    near=[e for e in tv if pop(e)>=top-0.25*abs(top)] or tv
    best=min(near,key=lambda e:((e.get('animeSeason') or {}).get('year') or 9999, -pop(e)))
    fpop=max(pop(e) for e in ents)+1.5*min(len(ents),20)
    cands=[best['title']]+best['synonyms']
    pool=[p.lower() for e in ents for p in [e['title']]+e['synonyms'] if p.isascii()]
    scored=[]
    for c0 in set(cands):
        c=clean(c0)
        ls=label_score(c)
        if c0==best['title']: ls=max(ls,1.0)
        if ls<0.6: continue
        cons=sum(1 for p in pool if c.lower() in p)
        scored.append((cons*(0.3+1.2*min(ls,2.6)/2.6)+ls*0.8, c, cons, ls))
    scored.sort(reverse=True)
    label=scored[0][1] if scored else clean(best['title'])
    if scored:
        top=scored[0]
        longer=[x for x in scored if x[1].lower().startswith(top[1].lower()) and len(x[1])>len(top[1]) and x[3]>=1.0 and x[2]>=0.5*top[2] and not BAD.search(x[1])]
        if longer: label=min(longer,key=lambda x:len(x[1]))[1]
    if len(label)<2: label=best['title']
    tags=set(best.get('tags',[]))
    tc=collections.Counter(t for e in ents for t in e.get('tags',[]))
    tags|={t for t,c in tc.items() if c>=2}
    out.append(dict(title=best['title'],label=label,syn=[s for s in cands if s!=label][:12],year=(best.get('animeSeason') or {}).get('year'),
                    type=best['type'],pop=round(fpop,2),n=len(ents),tags=sorted(tags),studios=best.get('studios',[])))
merged={}
for x in out:
    k=re.sub(r'[^a-z0-9]','',x['label'].lower())
    if k in merged:
        m=merged[k]; m['tags']=sorted(set(m['tags'])|set(x['tags'])); m['syn']=list(dict.fromkeys(m['syn']+[x['title']]+x['syn']))[:14]
        if x['pop']>m['pop']: m['pop']=x['pop']
    else: merged[k]=x
out=list(merged.values())
out.sort(key=lambda x:-x['pop'])
def key2(t):
    w=words(t); return ' '.join(w[:2]) if len(w)>=2 else (w[0] if w else t)
byk={}; final=[]
for x in out:
    k=key2(x['title']); hit=None
    for y in byk.get(k,[]):
        a,b=set(x['tags']),set(y['tags'])
        if a and b and len(a&b)/len(a|b)>=0.35: hit=y; break
    if hit: hit['tags']=sorted(set(hit['tags'])|set(x['tags'])); hit['syn']=list(dict.fromkeys(hit['syn']+[x['label'],x['title']]))[:16]
    else: final.append(x); byk.setdefault(k,[]).append(x)
out=final
out.sort(key=lambda x:-x['pop'])
json.dump(out,open('../build/anime_franchises.json','w'),ensure_ascii=False)
print(len(out))
for x in out[:80]: print(round(x['pop']),x['n'],x['label'],'|',x['title'])
