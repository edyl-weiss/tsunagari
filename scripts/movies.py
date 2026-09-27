"""IMDb Top 1000 movies -> Six Degrees titles.
Traits come from three places:
  1. TMDB keywords (matched by title + year) mapped onto the shared vocabulary, plus
     keywords that recur across the list as movie traits of their own;
  2. IMDb genres that line up with game/anime traits (Western, War, Horror, Film-Noir, Sport, Musical...);
  3. plot-summary patterns ("time travel", "samurai", "heist"...) for movies TMDB doesn't cover."""
import csv, json, re, collections, os
from movie_titles import english
from connectors import text_traits
from vocab import TMDB_EXTRA

HERE = os.path.dirname(os.path.abspath(__file__))
MDIR = os.path.join(HERE, '..', 'build', 'movies')

KW = {  # TMDB keyword -> shared trait
 "time travel": "Time travel", "time loop": "Time travel", "time machine": "Time travel",
 "dystopia": "Dystopia", "totalitarian regime": "Dystopia", "alien": "Aliens", "alien invasion": "Aliens", "extraterrestrial": "Aliens",
 "robot": "Robots and androids", "android": "Robots and androids", "artificial intelligence": "Artificial intelligence",
 "cyborg": "Cyborgs", "cyberpunk": "Cyberpunk", "steampunk": "Steampunk", "spacecraft": "Outer space", "space travel": "Outer space",
 "outer space": "Outer space", "space": "Outer space", "astronaut": "Outer space", "space battle": "Space battles", "mars": "Mars",
 "post-apocalyptic": "Post-apocalyptic", "post-apocalyptic future": "Post-apocalyptic", "apocalypse": "Post-apocalyptic", "nuclear war": "Post-apocalyptic",
 "zombie": "Zombies", "vampire": "Vampires", "werewolf": "Werewolves", "demon": "Demons", "devil": "Demons", "exorcism": "Exorcists and curses",
 "possession": "Exorcists and curses", "curse": "Exorcists and curses", "ghost": "Ghosts", "haunted house": "Ghosts", "witch": "Witches",
 "magic": "Magic", "wizard": "Magic", "sorcerer": "Magic", "school of witchcraft": "Magic school", "dragon": "Dragons", "dinosaur": "Dinosaurs",
 "superhero": "Superheroes", "super power": "Superpowers", "superpower": "Superpowers", "super powers": "Superpowers", "mutant": "Superpowers", "monster": "Monsters", "giant monster": "Kaiju",
 "samurai": "Feudal Japan", "feudal japan": "Feudal Japan", "ninja": "Ninjas", "martial arts": "Martial arts", "kung fu": "Martial arts",
 "sword": "Swordplay", "swordplay": "Swordplay", "sword fight": "Swordplay", "shootout": "Gunfights", "gunfight": "Gunfights", "sniper": "Sniping",
 "world war ii": "World War II", "nazi": "World War II", "d-day": "World War II", "soldier": "Military", "army": "Military", "military": "Military",
 "marine": "Military", "vietnam war": "Military", "war": "Military", "navy": "Naval warfare", "battleship": "Naval warfare", "submarine": "Submarines",
 "fighter pilot": "Flying aircraft", "pilot": "Flying aircraft", "airplane": "Flying aircraft", "tank": "Tanks",
 "prison": "Prison", "prison escape": "Prison", "prisoner": "Prison", "heist": "Heists and thieves", "bank robbery": "Heists and thieves", "robbery": "Heists and thieves",
 "thief": "Heists and thieves", "revenge": "Revenge", "vengeance": "Revenge", "mafia": "Crime and gangs", "gangster": "Crime and gangs",
 "organized crime": "Crime and gangs", "yakuza": "Crime and gangs", "drug dealer": "Crime and gangs", "detective": "Detective work",
 "investigation": "Detective work", "private detective": "Detective work", "police": "Police", "police officer": "Police", "cop": "Police",
 "assassin": "Assassins", "hitman": "Assassins", "contract killer": "Assassins", "spy": "Espionage", "secret agent": "Espionage", "espionage": "Espionage",
 "cia": "Espionage", "hacker": "Hacking", "computer": "Hacking", "pirate": "Pirates", "sailing": "Sailing", "ship": "Naval warfare",
 "ocean": "Under the sea", "underwater": "Under the sea", "shark": "Under the sea", "train": "Trains", "motorcycle": "Motorcycles",
 "car race": "Racing", "racing": "Racing", "race car": "Racing", "car chase": "Racing", "boxing": "Boxing and wrestling", "boxer": "Boxing and wrestling",
 "wrestling": "Boxing and wrestling", "baseball": "Baseball", "basketball": "Basketball", "soccer": "Soccer", "football (soccer)": "Soccer",
 "chess": "Board games", "gambling": "Gambling", "casino": "Gambling", "poker": "Gambling", "cooking": "Cooking", "chef": "Cooking",
 "fishing": "Fishing", "farm": "Farming", "farmer": "Farming", "horse": "Horses", "dog": "Dogs", "cat": "Cats",
 "mythology": "Mythology and gods", "greek mythology": "Mythology and gods", "norse mythology": "Vikings", "viking": "Vikings",
 "knight": "Knights", "medieval": "Medieval", "middle ages": "Medieval", "king": "Royal court", "queen": "Royal court", "royal family": "Royal court",
 "monarchy": "Royal court", "cult": "Faith and cults", "religion": "Faith and cults", "conspiracy": "Conspiracies", "terrorist": "Terrorism",
 "terrorism": "Terrorism", "amnesia": "Amnesia", "memory loss": "Amnesia", "clone": "Clones", "cloning": "Clones", "immortality": "Immortality",
 "body swap": "Body swap", "reincarnation": "Reincarnation", "coming of age": "Coming of age", "friendship": "Friendship", "orphan": "Orphans",
 "twins": "Twins", "sibling relationship": "Siblings", "brother brother relationship": "Siblings", "sister sister relationship": "Siblings",
 "marriage": "Marriage", "wedding": "Marriage", "divorce": "Marriage", "politics": "Politics", "politician": "Politics", "election": "Politics",
 "wall street": "Money and markets", "stock market": "Money and markets", "philosophy": "Philosophy", "psychopath": "Psychological twists",
 "psychological thriller": "Psychological twists", "surrealism": "Surreal", "satire": "Satire and parody", "parody": "Satire and parody",
 "black comedy": "Dark humor", "dark comedy": "Dark humor", "gore": "Gore", "splatter": "Gore", "anti-hero": "Anti-hero lead",
 "survival": "Survival", "desert": "Desert", "snow": "Snowy lands", "winter": "Snowy lands", "antarctica": "Snowy lands", "arctic": "Snowy lands",
 "tokyo": "Tokyo", "japan": "Tokyo", "hunting": "Hunting", "hunter": "Hunting", "archer": "Archery", "bow and arrow": "Archery",
 "musician": "Rhythm and music", "rock band": "Rhythm and music", "jazz": "Rhythm and music", "singer": "Rhythm and music", "music": "Rhythm and music",
 "dystopian": "Dystopia", "new york city": "America", "los angeles": "America", "wild west": "Wild West", "cowboy": "Wild West",
 "outlaw": "Wild West", "bounty hunter": "Bounty hunters", "treasure hunt": "Heists and thieves", "virtual reality": "Hacking",
 "found family": "Found family", "found footage": "Horror", "slasher": "Horror", "serial killer": "Serial killer", "hostage": "Terrorism",
 "sports": "Sports", "sport": "Sports", "idol": "Idols", "mecha": "Giant mechs", "giant robot": "Giant mechs",
}
GENRE = {"Western": "Wild West", "War": "Military", "Horror": "Horror", "Musical": "Rhythm and music", "Music": "Rhythm and music",
         "Sport": "Sports", "Mystery": "Mystery", "Thriller": "Thriller", "Film-Noir": "Noir", "Crime": "Crime and gangs"}
PAT = [(re.compile(p, re.I), lab) for p, lab in [
 (r'time travel|travels? back in time|time machine', 'Time travel'), (r'\bvampire', 'Vampires'), (r'\bzombie', 'Zombies'),
 (r'\balien|extraterrestrial', 'Aliens'), (r'\brobot|\bandroid|\bcyborg', 'Robots and androids'), (r'\bspace(ship|craft| station| travel)?\b|astronaut|\bgalaxy', 'Outer space'),
 (r'\bsamurai|\bronin\b|shogun', 'Feudal Japan'), (r'\bninja', 'Ninjas'), (r'mafia|\bmob\b|gangster|crime boss|crime family|yakuza|\bcartel', 'Crime and gangs'),
 (r'\bheist|robbery|\bthief|\bthieves|\bcon (man|artist)', 'Heists and thieves'), (r'revenge|avenge|vengeance', 'Revenge'),
 (r'detective|investigat|\bsleuth', 'Detective work'), (r'\bprison|\binmate|\bjail\b', 'Prison'), (r'\bspy\b|secret agent|espionage|\bCIA\b|\bMI6\b', 'Espionage'),
 (r'\bassassin|hitman|hit man|contract killer', 'Assassins'), (r'\bwitch', 'Witches'), (r'\bwizard|\bmagic|sorcer', 'Magic'), (r'\bdragon', 'Dragons'),
 (r'\bdinosaur', 'Dinosaurs'), (r'\bpirate', 'Pirates'), (r'\bboxer|\bboxing|wrestl', 'Boxing and wrestling'), (r'\bchess', 'Board games'),
 (r'\bking\b|\bqueen\b|\bprince(ss)?\b|\bemperor|royal', 'Royal court'), (r'world war ii|\bnazi|\bwwii|second world war|holocaust', 'World War II'),
 (r'\bsoldier|\barmy\b|\bplatoon|\bgeneral\b|battalion|\bwar\b', 'Military'), (r'\bghost|haunted', 'Ghosts'), (r'\bdemon|\bdevil|possess', 'Demons'),
 (r'serial killer', 'Serial killer'), (r'\bcult\b', 'Faith and cults'), (r'amnesia|lost his memory|lost her memory|memory loss', 'Amnesia'),
 (r'\bclone', 'Clones'), (r'musician|\bsinger|\bband\b|\bjazz|\bconcert', 'Rhythm and music'), (r'\bchef\b|restaurant|\bcook', 'Cooking'),
 (r'\bhorse', 'Horses'), (r'\bdog\b', 'Dogs'), (r'\bcat\b', 'Cats'), (r'\bsea\b|\bocean|\bsubmarine|\bshark', 'Under the sea'),
 (r'\btrain\b|railway|railroad', 'Trains'), (r'\bdesert\b', 'Desert'), (r'\bsnow|\barctic|antarctic|\bblizzard', 'Snowy lands'),
 (r'\btokyo\b|\bjapan', 'Tokyo'), (r'dystopi|totalitarian', 'Dystopia'), (r'post-apocalyptic|apocalypse|nuclear', 'Post-apocalyptic'),
 (r'artificial intelligence|\bAI\b|computer', 'Artificial intelligence'), (r'\bhacker|hacking', 'Hacking'), (r'superhero|super hero|super-powered|superpower', 'Superheroes'),
 (r'\bcowboy|outlaw|\bsheriff|gunslinger|wild west', 'Wild West'), (r'bounty hunter', 'Bounty hunters'), (r'\bpilot|fighter jet|aircraft|airplane', 'Flying aircraft'),
 (r'\bmotorcycle|biker', 'Motorcycles'), (r'\brac(e|ing) car|street rac|grand prix|formula (one|1)', 'Racing'), (r'\bsurviv', 'Survival'),
 (r'\bpolice|\bcop\b|\bcops\b|detective', 'Police'), (r'\bterroris', 'Terrorism'), (r'conspirac', 'Conspiracies'), (r'\bpolitic|election|senator|president', 'Politics'),
 (r'\bmarri|\bwedding|\bdivorce|\bhusband|\bwife\b', 'Marriage'), (r'\borphan', 'Orphans'), (r'\btwin\b|\btwins\b', 'Twins'),
 (r'\bbrothers?\b|\bsisters?\b|siblings?', 'Siblings'), (r'friendship|best friends?', 'Friendship'), (r'\bteen(age|ager)?s?\b|growing up|coming-of-age', 'Coming of age'),
 (r'\bknight|medieval|middle ages', 'Medieval'), (r'\bgod(s|dess)?\b|mytholog|\bzeus|\bthor\b', 'Mythology and gods'), (r'\bviking', 'Vikings'),
 (r'\bbaseball', 'Baseball'), (r'\bbasketball', 'Basketball'), (r'\bsoccer|\bfootball', 'Sports'), (r'\bgambl|\bcasino|\bpoker', 'Gambling'),
 (r'wall street|stock broker|stockbroker|\bbanker', 'Money and markets'), (r'\bmonster', 'Monsters'),
]]
KW_STOP = {"woman director", "duringcreditsstinger", "aftercreditsstinger", "independent film", "based on novel", "based on novel or book",
           "biography", "sequel", "remake", "3d", "based on comic", "based on comic book", "based on true story", "based on true events",
           "historical figure", "imax", "flashback", "fight", "rescue", "bravery", "chaos", "redemption", "dream", "hope", "fear", "lawyer", "transporter", "sex", "nudity", "female nudity", "sexuality", "rape", "suicide", "incest", "drug", "drugs", "prostitute",
           "prostitution", "child abuse", "sexual abuse", "love", "romance", "death", "family", "husband wife relationship", "father son relationship",
           "mother son relationship", "father daughter relationship", "mother daughter relationship", "new york", "usa", "london england",
           "paris", "france", "england", "italy", "germany", "india", "loss of loved one", "violence", "murder", "blood", "dying and death"}

def norm(s): return re.sub(r'[^a-z0-9]+', ' ', s.lower().replace('×', 'x')).strip()

def load_movies():
    imdb = list(csv.DictReader(open(os.path.join(MDIR, 'imdb_top_1000.csv'), encoding='utf-8')))
    kw = collections.defaultdict(set)
    for r in csv.DictReader(open(os.path.join(MDIR, 'tmdb10k.csv'), encoding='utf-8')):
        y = r.get('release_year') or r['release_date'][-4:]
        if r['keywords']: kw[(norm(r['original_title']), str(y))].update(r['keywords'].split('|'))
    for r in csv.DictReader(open(os.path.join(MDIR, 'tmdb5000.csv'), encoding='utf-8')):
        y = r['release_date'][:4]
        try: k = [x['name'] for x in json.loads(r['keywords'])]
        except Exception: k = []
        for t in (r['original_title'], r.get('title', '')):
            if t: kw[(norm(t), y)].update(k)
    out = []
    kwfreq = collections.Counter()
    rows = []
    for m in imdb:
        y = m['Released_Year']; t = norm(m['Series_Title'])
        k = set()
        if y.isdigit():
            for yy in (int(y), int(y) - 1, int(y) + 1):
                k |= kw.get((t, str(yy)), set())
        k = {x.lower() for x in k}
        kwfreq.update(k)
        rows.append((m, k))
    dcount = collections.Counter(m['Director'] for m, _ in rows)
    for rank, (m, k) in enumerate(sorted(rows, key=lambda r: -int(r[0]['No_of_Votes'] or 0)), 1):
        tr = set()
        for x in k:
            if x in TMDB_EXTRA: tr.add(TMDB_EXTRA[x])
            if x in KW: tr.add(KW[x])
            elif x not in TMDB_EXTRA and x not in KW_STOP and kwfreq[x] >= 4 and len(x) <= 30:
                tr.add(x[:1].upper() + x[1:])
        for g in [g.strip() for g in m['Genre'].split(',')]:
            if g in GENRE: tr.add(GENRE[g])
        for g in [g.strip() for g in m['Genre'].split(',')]:
            if g not in GENRE and g not in ('Drama', 'Comedy', 'Action', 'Adventure', 'Romance'): tr.add(g + ' film')
        if dcount[m['Director']] >= 2: tr.add('Directed by ' + m['Director'])
        ov = m['Overview']
        tr |= text_traits(ov)
        for p, lab in PAT:
            if p.search(ov): tr.add(lab)
        y = int(m['Released_Year']) if m['Released_Year'].isdigit() else None
        en = english(m['Series_Title'])
        dec = f"{(y // 10) * 10}s film" if y else None
        if dec: tr.add(dec)
        for g in [g.strip() for g in m['Genre'].split(',')]:
            if g in ('Drama', 'Comedy', 'Action', 'Adventure', 'Romance'): tr.add(g + ' film')
        out.append(dict(label=en, media='movie', year=y, aliases=[m['Series_Title'].replace('\x1a', '')] if en != m['Series_Title'] else [], pop=rank, traits=tr,
                        genres=m['Genre'], director=m['Director'], votes=int(m['No_of_Votes'] or 0), matched_keywords=bool(k)))
    return out

if __name__ == '__main__':
    ms = load_movies()
    print(len(ms), 'movies;', sum(m['matched_keywords'] for m in ms), 'with TMDB keywords')
    c = collections.Counter(len(m['traits']) for m in ms); print(sorted(c.items()))
    for m in ms[:12]: print(m['label'], sorted(m['traits']))
