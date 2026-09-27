import json, collections, random, time
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import shortest_path
g = json.load(open('../build/final_graph.json')); T = g['titles']; CATS = g['cats']
tl = sorted({tr for t in T for tr in t['traits']}); ti = {t: i for i, t in enumerate(tl)}
rows, cols = [], []
for i, t in enumerate(T):
    for tr in t['traits']: rows.append(i); cols.append(ti[tr])
M = sparse.csr_matrix((np.ones(len(rows), dtype=np.int32), (rows, cols)), shape=(len(T), len(tl)))
C = (M @ M.T).tocsr(); C.setdiag(0); C.eliminate_zeros()
E = (C >= 2).astype(np.int8); E.eliminate_zeros()
print('titles', len(T), 'edges', E.nnz // 2)
order = sorted(range(len(T)), key=lambda i: (T[i]['pop'], T[i]['media']))
T1 = set(order[:1800]); T2 = order[:4000]; SRC = order[:8000]; T3 = set(order[:8000])
want = {3: 'easy', 4: 'medium', 5: 'hard', 6: 'expert'}
cand = collections.defaultdict(list)
t0 = time.time()
T1a = np.zeros(len(T), bool); T1a[list(T1)] = True
T2a = np.zeros(len(T), bool); T2a[T2] = True
T3a = np.zeros(len(T), bool); T3a[list(T3)] = True
fr = np.array([hash(t['franchise']) for t in T])
prs = random.Random(3)
CAPPER = {'easy': 4, 'medium': 20, 'hard': 10**6, 'expert': 10**6}
for b in range(0, len(SRC), 500):
    src = SRC[b:b + 500]
    D, pred = shortest_path(E, unweighted=True, directed=False, indices=src, return_predecessors=True)
    for k, s in enumerate(src):
        row = D[k]
        for d, name in want.items():
            if b >= 4000 and name != 'expert': continue
            mask = (row == d) & (fr != fr[s])
            if name in ('easy', 'medium'):
                if not T1a[s]: continue
                mask &= T1a
            elif name == 'hard':
                mask &= T2a
                if not T1a[s]: mask &= T1a
            else:
                mask &= T3a
            ts = np.flatnonzero(mask)
            if len(ts) > CAPPER[name]: ts = prs.sample(list(ts), CAPPER[name])
            for t in ts:
                t = int(t); p = [t]
                while p[-1] != s: p.append(int(pred[k, p[-1]]))
                cand[name].append((p[::-1], int(T1a[s]) + int(T1a[t])))
    print(b, {k: len(v) for k, v in cand.items()}, round(time.time() - t0), 's', flush=True)
rng = random.Random(11); out = {}
LIM = {'easy': 1500, 'medium': 1500, 'hard': 1200, 'expert': 900}
for name, lst in cand.items():
    rng.shuffle(lst); lst.sort(key=lambda x: -x[1])   # prefer puzzles with popular endpoints
    res = []; seen = set(); per = collections.Counter()
    for p, pri in lst:
        key = frozenset((p[0], p[-1]))
        if key in seen: continue
        media = {T[i]['media'] for i in p}; fr = {T[i]['franchise'] for i in p}
        if name in ('hard', 'expert') and len(media) < 2: continue
        lim = {'easy': 5, 'medium': 10}.get(name, 25)
        if per[p[0]] >= lim or per[p[-1]] >= lim: continue
        seen.add(key); per[p[0]] += 1; per[p[-1]] += 1; res.append(p)
        if len(res) >= LIM[name]: break
    out[name] = res
    print(name, 'kept', len(res), 'with 2 popular ends', sum(1 for p in res if p[0] in T1 and p[-1] in T1))
json.dump(out, open('../build/pools.json', 'w'))
