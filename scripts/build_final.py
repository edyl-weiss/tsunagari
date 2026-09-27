"""Build the large Tsunagatteru graph.
Rule: two titles are one hop apart when they share at least TWO traits."""
import json, re, collections, sys
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components, shortest_path
sys.path.insert(0, '.')
from vocab import V, BLOCK_ANIME, BLOCK_STEAM, NON_GAME_STEAM
from connectors import text_traits

N_ANIME = int(sys.argv[1]); N_GAME = int(sys.argv[2]); CAP = int(sys.argv[3]); NEED = 2
MINF = 5

A2T = collections.defaultdict(list); S2T = collections.defaultdict(list)
for lab, (cat, at, st) in V.items():
    for t in at: A2T[t].append(lab)
    for t in st: S2T[t].append(lab)
CATS = {lab: cat for lab, (cat, _, _) in V.items()}

ANIME_STOP = set("""japanese production comedy action drama adventure fantasy present place time earth asia japan based on a manga
male protagonist female protagonist manga novel original work shounen seinen shoujo josei kids tropes speculative fiction sci-fi science fiction
science-fiction sci fi slice of life romance cgi 3d cg animation full cgi cg animation cg-anime chinese animation chinese production korean animation
south korean production short episodes shorts episodic plot continuity new season sequel ending stand-alone movie narration storytelling stereotypes
heterosexual ecchi nudity large breasts pantsu skimpy clothing gainax bounce fanservice lingerie small breasts boobs in your face sexual humour sex
swimsuit wardrobe malfunction sudden naked girl appearance flat chest jokes tentacle bdsm trap reverse trap femboy loli boys' love shounen ai
shounen-ai bl boys love girls love shoujo ai yuri lgbtq+ themes lgbtqia+ bisexual transgender tv censoring preaired episodes staff missing
remastered version available adapted into other media adapted into japanese movie adapted into jdrama crunchyroll co-production only on netflix
noitamina newtype anime award award winning awards ed variety weekly shounen jump promotional product placement canon filler half-length episodes
multi-segment episodes slide show animation black and white achromatic watercolour style experimental animation mixed media live-action imagery
faceless background characters walls of text talking is a free action mina call my name cgdct moe bishounen bishoujo suicide sexual abuse rape
child abuse animal abuse torture prostitution drugs psychoactive drugs racism incest sexual fantasies sexual abuse -- to be split and deleted
dark-skinned girl tanned skin gyaru age gap age difference romance primarily female cast primarily male cast primarily teen cast primarily adult cast
primarily child cast predominantly female cast predominantly male cast predominantly adult cast ensemble cast family friendly kodomo past future
fictional location real-world location foreign alternative world alternate universe alternative present alternative past world music the arts
violence tragedy slapstick school school life high school middle school elementary school college university magic super power supernatural
contemporary fantasy urban fantasy urban daily life family life historical game crime war death disaster monster monsters animals anthropomorphic
anthropomorphism non-human protagonists animal protagonists primarily animal cast 4-koma manga based on a 4-koma manga based on a light novel
based on a novel based on a web novel based on a video game based on a mobile game in medias res flashback open-ended time skip plot twists
character driven dialogue driven slow-paced fast-paced tone changes happy ending everybody dies achronological order classic literature
multi-anime projects show within a show running gag catchphrase funny expressions facial distortion chibi super deformed engrish wordplay
verbal comedy gag gag humor nonsense-comedy toilet humour randomness absurdist humour surreal comedy black humour parody satire self-parody
action comedy action drama romantic comedy romantic drama sentimental drama melodrama slice of life drama supernatural drama psychological drama
heart-warming iyashikei iyashi-kei season spring summer autumn winter hanami europe americas united states united kingdom france china old asia
ancient china feudal japan tokyo boy meets girl first love love triangle love polygon unrequited love slow when it comes to love forbidden love
multiple couples cohabitation under one roof female harem male harem harem reverse harem harem""".replace('\n', ' ').split(' '))
# multiword stop entries
ANIME_STOP_PHRASES = {s.strip() for s in re.split(r'\s{2,}|\n', "")}
BAD_PAT = re.compile(r'(breast|boob|panty|pantsu|nud|sex|erot|porn|hentai|fetish|incest|rape|abuse|suicide|self-harm|loli|shota|yaoi|yuri|ecchi|bdsm|genital|harem|lewd|masturb|virgin|pregnan|bust|butt|oppai|lingerie|underwear|bath)', re.I)

def norm(s): return re.sub(r'[^a-z0-9]+', ' ', s.lower().replace('×', 'x')).strip()
def fkey(s):
    s = norm(re.split(r'[:\-–(]', s)[0])
    s = re.sub(r'\b(\d+|ii|iii|iv|v|vi|vii|viii|ix|x|remastered|remake|definitive|edition|hd|deluxe|the)\b', '', s)
    return re.sub(r'\s+', ' ', s).strip()

titles = []
# ---------- anime ----------
anime = json.load(open('../build/anime_franchises.json'))
pool = []
for x in anime:
    tags = set(x['tags'])
    if tags & BLOCK_ANIME: continue
    if BAD_PAT.search(x['label']): continue
    pool.append(x)
    if len(pool) >= N_ANIME: break
afreq = collections.Counter(t for x in pool for t in x['tags'])
def multiword_stop(t):
    return t in STOPSET
STOPSET = set()
for phrase in ["japanese production", "based on a manga", "male protagonist", "female protagonist", "original work", "speculative fiction",
               "science fiction", "sci fi", "slice of life", "3d cg animation", "full cgi", "cg animation", "chinese animation", "chinese production",
               "korean animation", "south korean production", "short episodes", "plot continuity", "stand-alone movie", "large breasts",
               "skimpy clothing", "gainax bounce", "small breasts", "boobs in your face", "sexual humour", "wardrobe malfunction",
               "sudden naked girl appearance", "flat chest jokes", "reverse trap", "boys' love", "shounen ai", "boys love", "girls love",
               "shoujo ai", "lgbtq+ themes", "tv censoring", "preaired episodes", "staff missing", "remastered version available",
               "adapted into other media", "adapted into japanese movie", "adapted into jdrama", "crunchyroll co-production", "only on netflix",
               "newtype anime award", "award winning", "ed variety", "weekly shounen jump", "product placement", "canon filler",
               "half-length episodes", "multi-segment episodes", "slide show animation", "black and white", "watercolour style",
               "experimental animation", "mixed media", "live-action imagery", "faceless background characters", "walls of text",
               "talking is a free action", "call my name", "sexual abuse", "child abuse", "animal abuse", "psychoactive drugs",
               "sexual fantasies", "dark-skinned girl", "tanned skin", "age gap", "age difference romance", "primarily female cast",
               "primarily male cast", "primarily teen cast", "primarily adult cast", "primarily child cast", "predominantly female cast",
               "predominantly male cast", "predominantly adult cast", "ensemble cast", "family friendly", "fictional location",
               "real-world location", "alternative world", "alternate universe", "alternative present", "alternative past", "the arts",
               "school life", "high school", "middle school", "elementary school", "super power", "contemporary fantasy", "urban fantasy",
               "daily life", "family life", "non-human protagonists", "animal protagonists", "primarily animal cast", "4-koma manga",
               "based on a 4-koma manga", "based on a light novel", "based on a novel", "based on a web novel", "based on a video game",
               "based on a mobile game", "in medias res", "time skip", "plot twists", "character driven", "dialogue driven", "tone changes",
               "happy ending", "everybody dies", "achronological order", "classic literature", "multi-anime projects", "show within a show",
               "running gag", "funny expressions", "facial distortion", "super deformed", "verbal comedy", "gag humor", "toilet humour",
               "absurdist humour", "surreal comedy", "black humour", "action comedy", "action drama", "romantic comedy", "romantic drama",
               "sentimental drama", "slice of life drama", "supernatural drama", "psychological drama", "old asia", "boy meets girl",
               "first love", "love triangle", "love polygon", "unrequited love", "slow when it comes to love", "forbidden love",
               "multiple couples", "under one roof", "female harem", "male harem", "reverse harem", "cute girls doing cute things",
               "cute boys doing cute things", "strong female lead", "strong male lead", "hero of strong character", "heroine of strong character",
               "hero of weak character", "calling your attacks", "visible aura", "collateral damage", "open-ended", "coming of age",
               "sexual abuse -- to be split and deleted", "idols (female)", "adult cast", "adult audience only", "japanese mythology"]:
    STOPSET.add(phrase)
for w in ANIME_STOP: STOPSET.add(w)
AUTO = {}
for t, c in afreq.items():
    if t in A2T or t in STOPSET or BAD_PAT.search(t) or c < MINF: continue
    lab = t[:1].upper() + t[1:]
    AUTO[t] = lab
for x in pool:
    tr = {lab for t in x['tags'] for lab in A2T.get(t, [])} | {AUTO[t] for t in x['tags'] if t in AUTO}
    titles.append(dict(label=x['label'], media='anime', year=x.get('year'), aliases=[x['title']] + [s for s in x['syn'] if s.isascii() and not BAD_PAT.search(s)][:5],
                       pop=0, traits=tr, franchise='a:' + fkey(x['label'])))
for i, t in enumerate(titles): t['pop'] = i + 1
na = len(titles)
# ---------- games ----------
STEAM_META = set(['Singleplayer','Multiplayer','Indie','Action','Adventure','Casual','Simulation','Strategy','RPG','2D','3D','2.5D','Pixel Graphics',
 'Great Soundtrack','Atmospheric','Story Rich','Funny','Cute','Colorful','Beautiful','Stylized','Cartoony','Cartoon','Realistic','Controller',
 'Early Access','Free to Play','Co-op','Online Co-Op','Local Co-Op','Local Multiplayer','Split Screen','4 Player Local','PvP','PvE','Competitive',
 'e-sports','Moddable','Mod','Level Editor','Replay Value','Addictive','Classic','Cult Classic','Old School','Remake','Sequel','Short',
 'Linear','Nonlinear','Epic','Masterpiece','Kickstarter','Crowdfunded','Touch-Friendly','Mouse only','TrackIR','3D Vision','VR','FPP','TPP',
 'First-Person','Third Person','Top-Down','Isometric','Side Scroller','Difficult','Unforgiving','Fast-Paced','Minimalist','Abstract','Experimental',
 'Immersive','Cinematic','Hand-drawn','Anime','Female Protagonist','LGBTQ+','Sexual Content','Nudity','Mature','Violent','Dynamic Narration',
 'Narration','Conversation','Text-Based','Tutorial','Soundtrack','Movie','Documentary','Episodic','Asynchronous Multiplayer','Inventory Management',
 'Character Customization','Gun Customization','Combat','Action-Adventure','Action RPG','Role-playing','Shooter','Exploration',
 'Well-Written','Intentionally Awkward Controls','Quick-Time Events','Time Attack','Family Friendly','Comedy','Drama',
 'Fantasy','Sci-fi','Futuristic','Modern','Historical','Dark','Lore-Rich','Beautiful','Nostalgia','1990\'s','1980s','Experience','Foreign',
 'Instrumental Music','Electronic Music','Rock Music','Faith','Real-Time','Real-time','Real-Time with Pause','Massively Multiplayer',
 'Spectacle fighter','Puzzle','Adventure','Interactive Fiction','Choose Your Own Adventure','Emotional','Relaxing','Wholesome','Cozy',
 'Colony Sim','RPGMaker','GameMaker','Voxel','Hex Grid','Games Workshop','Warhammer 40K','LEGO','Based On A Novel','Crime','Supernatural',
 'Thriller','Mystery','Horror','Gore','Blood','Psychological','Dystopian','Magic','War','Military','Violent','Memes','Illuminati'])
games = json.load(open('../build/steam_small.json'))
games.sort(key=lambda g: -g['reviews'])
seen = set(); ng = 0
SKIP = re.compile(r'(soundtrack|\bdemo\b|playtest|dedicated server|\bsdk\b|\bdlc\b|season pass|test server|\bbeta\b|wallpaper|benchmark)', re.I)
for g in games:
    tags = g['tags']
    if set(tags) & BLOCK_STEAM or set(tags) & NON_GAME_STEAM: continue
    if 'Sexual Content' in tags[:8] or 'Nudity' in tags[:6]: continue
    name = re.sub(r'[™®©]', '', g['name']).strip()
    name = re.sub(r'\s*[-–:]?\s*(Complete|Definitive|Game of the Year|GOTY|Enhanced|Deluxe|Anniversary|Ultimate|Gold|Special|Legendary|Royal)\s+Edition\b.*$', '', name, flags=re.I).strip()
    if SKIP.search(name) or BAD_PAT.search(name): continue
    k = norm(name)
    if not k or k in seen: continue
    seen.add(k)
    tr = []
    for t in tags[:20]:
        for lab in S2T.get(t, []):
            if lab not in tr: tr.append(lab)
        if t not in S2T and t not in STEAM_META and not BAD_PAT.search(t) and t not in tr: tr.append(t)
    ng += 1
    if ng > N_GAME: break
    yr = int(g['date'][:4]) if g.get('date') else None
    tr = set(tr) | text_traits(g.get('desc', ''))
    titles.append(dict(label=name, media='game', year=yr, aliases=[], pop=ng, traits=tr, franchise='g:' + fkey(name)))

# ---------- movies (IMDb Top 1000) ----------
from movies import load_movies
MOV = load_movies()
anime_ix = {}
for i, t in enumerate(titles):
    if t['media'] == 'anime':
        for s_ in [t['label']] + t['aliases']: anime_ix.setdefault(norm(s_), i)
nm_merged = 0
for m in MOV:
    j = anime_ix.get(norm(m['label']))
    if j is None:
        for a_ in m['aliases']: j = j if j is not None else anime_ix.get(norm(a_))
    if j is not None and 'Animation' in m['genres'] and m['year'] and titles[j].get('year') and abs(titles[j]['year'] - m['year']) <= 1:
        # same work already in the anime list (e.g. Spirited Away): fold the movie's traits in
        titles[j]['traits'] = set(titles[j]['traits']) | set(m['traits']); nm_merged += 1
        titles[j]['pop'] = min(titles[j]['pop'], m['pop']); continue
    titles.append(dict(label=m['label'], media='movie', year=m['year'], aliases=m['aliases'], pop=m['pop'], traits=set(m['traits']),
                       franchise='m:' + fkey(m['label'])))
print('movies added', len(MOV) - nm_merged, '| merged into anime', nm_merged, file=sys.stderr)
# one label per trait regardless of source casing ("Time Travel" vs "Time travel")
CANON = {lab.lower(): lab for lab in V}
def canon(tr):
    k = tr.lower()
    return CANON.setdefault(k, tr)
for t in titles: t['traits'] = {canon(x) for x in t['traits']}
# ---------- merge duplicate anime entries (same show under English and romaji names) ----------
lab_ix = {}
for i, t in enumerate(titles):
    lab_ix.setdefault((t['media'], norm(t['label'])), i)
drop = set()
for i, t in enumerate(titles):
    if i in drop: continue
    for a in t['aliases']:
        j = lab_ix.get((t['media'], norm(a)))
        if j is not None and j != i and j not in drop:
            keep_i, lose = (i, j) if t['pop'] <= titles[j]['pop'] else (j, i)
            titles[keep_i]['traits'] = set(titles[keep_i]['traits']) | set(titles[lose]['traits'])
            titles[keep_i]['aliases'] = list(dict.fromkeys(titles[keep_i]['aliases'] + [titles[lose]['label']] + titles[lose]['aliases']))[:8]
            drop.add(lose)
            if lose == i: break
titles = [t for k, t in enumerate(titles) if k not in drop]
print('merged duplicates', len(drop), file=sys.stderr)
# canonical traits for hand-tagged classics that aren't on Steam (or are listed under a different name)
EXTRA = {"tetris":["Puzzles","Arcade","Retro","Score Attack"],"pacman":["Arcade","Retro","Ghosts","Score Attack"],"minecraft":["Crafting","Survival","Open world","Sandbox","Base building"],
 "acnh":["Life sim","Cozy and relaxing","Fishing","Crafting"],"mario":["Platforming","Collectathon","Open world"],
 "botw":["Open world","Cooking","Puzzles","Physics sandbox","Archery","Survival"],"pokemon":["Creature collecting","Turn-based combat","Retro","JRPG"],
 "smash":["Fighting game","Party games","Crossovers"],"sonic":["Platforming","Retro","Collectathon"],"halo":["FPS","Aliens","Outer space","Military","Artificial intelligence"],
 "tlou":["Zombies","Post-apocalyptic","Survival horror","Stealth"],"ghost":["Open world","Feudal Japan","Stealth","Swordplay","Horses"],
 "deathstranding":["Open world","Post-apocalyptic","Walking Simulator"],"mgs":["Stealth","Military","Espionage"],
 "ff7r":["Cyberpunk","Swordplay","Magic","JRPG","Dystopia"],"p5":["Turn-based combat","JRPG","Dating sim","Heists and thieves","Tokyo"],
 "catherine":["Puzzles","Dating sim","Choices matter"],"ninokuni":["JRPG","Creature collecting","Magic"],"darksouls":["Souls-like combat","Dark fantasy","Medieval"],
 "genshin":["Open world","Magic","Swordplay","Mythology and gods","JRPG"],"fortnite":["Battle royale","Base building","Crossovers","Gunfights"],
 "overwatch":["Hero shooter","FPS","Robots and androids"],"gta5":["Open world","Crime and gangs","Heists and thieves","Racing"],
 "sf2":["Fighting game","Martial arts","Arcade","Retro"],"kirby":["Platforming","Collectathon"],"kh3":["JRPG","Magic","Hack and slash"],
 "sekiro":["Souls-like combat","Feudal Japan","Ninjas","Stealth"],"gow":["Mythology and gods","Vikings","Hack and slash"],"re4":["Survival horror","Zombies"],
 "sh2":["Psychological horror","Survival horror"],"wukong":["Souls-like combat","Mythology and gods"],"eldenring":["Souls-like combat","Open world","Dark fantasy"],
 "nier":["Hack and slash","Robots and androids","Post-apocalyptic"],"arise":["JRPG","Swordplay","Magic"],"chrono":["JRPG","Time travel","Retro"]}
# ---------- curated hand-tagged titles (keep their hand traits and labels) ----------
cur = json.load(open('../data/curated_graph.json'))
cur_tr = collections.defaultdict(dict)
for r in cur['rels']: cur_tr[r['f']][r['to']] = r['detail']
HAND = {n['id']: n for n in cur['nodes'] if n['t'] == 'trait'}
index = collections.defaultdict(list)
for i, t in enumerate(titles):
    for s in [t['label']] + t['aliases']: index[norm(s)].append(i)
for n in cur['nodes']:
    if n['t'] != 'work': continue
    hit = None
    for s in [n['label']] + n.get('aliases', []):
        for i in index.get(norm(s), []):
            if titles[i]['media'] == n['media'] and hit is None: hit = i
    if hit is None:
        titles.append(dict(label=n['label'], media=n['media'], year=n.get('year'), aliases=n.get('aliases', []), pop=40,
                           traits=set(), franchise=({'anime':'a:','game':'g:','movie':'m:'}[n['media']]) + fkey(n['label'])))
        hit = len(titles) - 1
    t = titles[hit]
    t['aliases'] = list(dict.fromkeys([a for a in [t['label']] + t['aliases'] + n.get('aliases', []) if a != n['label']]))[:8]
    t['label'] = n['label']; t['pop'] = min(t['pop'], 40); t['year'] = n.get('year') or t['year']
    t['hand'] = {HAND[h]['label']: d for h, d in cur_tr[n['id']].items()}
    for h in t['hand']: CATS[h] = HAND[[k for k in HAND if HAND[k]['label'] == h][0]]['cat']
    t['traits'] = set(t['traits']) | set(t['hand']) | set(EXTRA.get(n['id'], []))

# ---------- trait cap ----------
size = collections.Counter(tr for t in titles for tr in t['traits'])
hand_labels = {HAND[h]['label'] for h in HAND}
for t in titles:
    t['traits'] = sorted(tr for tr in t['traits'] if size[tr] >= 2 and (size[tr] <= CAP or tr in hand_labels or tr in ('Platforming','Arcade','Retro')))
tl = sorted({tr for t in titles for tr in t['traits']}); ti = {t: i for i, t in enumerate(tl)}
rows, cols = [], []
for i, t in enumerate(titles):
    for tr in t['traits']: rows.append(i); cols.append(ti[tr])
M = sparse.csr_matrix((np.ones(len(rows), dtype=np.int32), (rows, cols)), shape=(len(titles), len(tl)))
C = (M @ M.T).tocsr(); C.setdiag(0); C.eliminate_zeros()
E = (C >= NEED).astype(np.int8); E.eliminate_zeros()
ncomp, lab = connected_components(E, directed=False)
main = np.bincount(lab).argmax()
keep = [i for i in range(len(titles)) if lab[i] == main]
print(f'pool {len(titles)} (anime {na}, games {len(titles)-na}) | traits {len(tl)} | kept in main component {len(keep)}', file=sys.stderr)
mc = collections.Counter(titles[i]['media'] for i in keep); print('kept by media', dict(mc), file=sys.stderr)
# distance profile among popular endpoints
kidx = {i: j for j, i in enumerate(keep)}
Ek = E[keep][:, keep]
popk = sorted(range(len(keep)), key=lambda j: titles[keep[j]]['pop'])[:1500]
D = shortest_path(Ek, unweighted=True, directed=False, indices=popk[:300])
vals = D[:, popk].ravel()
c = collections.Counter(int(v) if np.isfinite(v) else -1 for v in vals)
print('popular-pair hops', sorted(c.items()), file=sys.stderr)
out = dict(titles=[{**titles[i], 'traits': titles[i]['traits']} for i in keep],
           cats={tr: CATS.get(tr, 'trope') for tr in tl}, need=NEED, cap=CAP)
json.dump(out, open('../build/final_graph.json', 'w'), ensure_ascii=False)
