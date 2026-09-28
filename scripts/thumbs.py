"""Attach an official thumbnail reference to every title in final_graph.json.
Anime: MyAnimeList key art (anime-offline-database). Games: Steam header capsule (steamdb dump).
Movies: IMDb poster (IMDb top 1000 CSV). Output: thumbs.json, a list aligned with titles,
using short codes the page expands:  aNNN/NNN = MAL,  sNNN = Steam appid,  iMV5B... = IMDb,  full URL otherwise."""
import json, gzip, re, csv
def norm(s): return re.sub(r'[^a-z0-9]+', ' ', (s or '').lower().replace('×', 'x')).strip()
T = json.load(open('../build/final_graph.json'))['titles']

# anime
aod = json.load(open('../build/aod.json'))['data']
A = {}
for e in aod:
    pic = e.get('picture') or ''
    if not pic or 'no_pic' in pic or 'noimage' in pic.lower(): continue
    yr = (e.get('animeSeason') or {}).get('year') or 0
    score = {'TV': 0, 'MOVIE': 1, 'OVA': 2, 'ONA': 2}.get(e.get('type'), 3)
    for n in [e['title']] + e.get('synonyms', []):
        k = norm(n)
        if k: A.setdefault(k, []).append((score, yr, pic))
def anime_pic(t):
    yr = t.get('year') or 0
    for n in [t['label']] + t.get('aliases', []):
        c = A.get(norm(n))
        if not c: continue
        c = sorted(c, key=lambda x: (0 if (not yr or not x[1] or abs(x[1] - yr) <= 1) else 1, x[0]))
        return c[0][2]
    return ''

# games
S = {}
for e in json.load(gzip.open('../build/steamdb.min.json.gz')):
    k = norm(e['name']); n = int(e['steam_reviews_count']) if str(e.get('steam_reviews_count', '')).isdigit() else 0
    ref = ('s' + str(e['steam_appid'])) if e.get('steam_appid') not in (None, 'None', '') else (e.get('image') or '')
    if ref and (k not in S or n > S[k][0]): S[k] = (n, ref)
EDITION = set('complete definitive enhanced edition goty game of the year remastered remaster anniversary special deluxe gold ultimate director s cut classic retired collection intergrade royal hd'.split())
# well-known titles whose Steam release has a different name (appids checked against the steamdb dump)
MANUAL = {'Final Fantasy VII Remake': 's1462040', 'Persona 5': 's1687950', 'Catherine': 's893180', 'Ni no Kuni: Wrath of the White Witch': 's798460',
          'Dark Souls': 's570940', 'Halo: Combat Evolved': 's976730', 'The Last of Us': 's1888930', 'Ghost of Tsushima': 's2215430',
          'Kingdom Hearts III': 's2552450'}
SK = sorted(S)
import bisect
def game_pic(t):
    if t['label'] in MANUAL: return MANUAL[t['label']]
    names = [t['label']] + t.get('aliases', [])
    for n in names:
        v = S.get(norm(n))
        if v: return v[1]
    # same title plus only edition words ("... Definitive Edition", "... GOTY")
    for n in names:
        k = norm(re.sub(r'\s*[:–-]?\s*The$', '', n)); best = None
        i = bisect.bisect_left(SK, k + ' ')
        while i < len(SK) and SK[i].startswith(k + ' '):
            rest = SK[i][len(k) + 1:].split()
            if all(w in EDITION or w.isdigit() for w in rest) and (best is None or S[SK[i]][0] > best[0]): best = S[SK[i]]
            i += 1
        if best: return best[1]
    return ''

# movies
M = {}
for r in csv.DictReader(open('../build/movies/imdb_top_1000.csv', encoding='utf-8')):
    m = re.match(r'https://m\.media-amazon\.com/images/M/([^.]+)\.', r['Poster_Link'] or '')
    if m: M.setdefault(norm(r['Series_Title'].replace('\x1a', '')), []).append((int(r['Released_Year']) if r['Released_Year'].isdigit() else 0, 'i' + m.group(1)))
def movie_pic(t):
    yr = t.get('year') or 0
    for n in [t['label']] + t.get('aliases', []):
        c = M.get(norm(n))
        if c: return sorted(c, key=lambda x: abs(x[0] - yr) if yr and x[0] else 0)[0][1]
    return ''

out = []
for t in T:
    p = {'anime': anime_pic, 'game': game_pic, 'movie': movie_pic}[t['media']](t)
    m = re.match(r'https://cdn\.myanimelist\.net/images/anime/(\d+/\d+)\.jpg$', p)
    out.append('a' + m.group(1) if m else p)
json.dump(out, open('../build/thumbs.json', 'w'), separators=(',', ':'))
from collections import Counter
have = Counter(t['media'] for t, o in zip(T, out) if o); tot = Counter(t['media'] for t in T)
print({k: f"{have[k]}/{tot[k]}" for k in tot})
top = [t['label'] for t, o in zip(T, out) if not o and t['pop'] <= 300]
print('missing among popular:', len(top), top[:40])
