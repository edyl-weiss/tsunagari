"""New cross-media traits and the keyword connectors that detect them.

Each trait lists every way it can be spotted:
  anime  - anime-offline-database tags
  steam  - Steam community tags
  tmdb   - TMDB movie keywords
  text   - a regex run over Steam store descriptions and IMDb plot summaries
A title gets the trait if ANY connector fires. The text connectors are what let a
game or movie link to anime on concepts that no tag system shares."""
import re

C = {
 # ---------- story engines ----------
 "Time loop": ("story", ["time loop"], [], ["time loop"], r"time loop|same day over (and over|again)|reliv(e|es|ing) the same day|groundhog day"),
 "Parallel worlds": ("story", ["parallel world", "parallel universe", "alternate universe", "multiverse"], [], ["parallel world", "alternate reality", "multiverse", "parallel universe"],
                     r"parallel (world|universe|dimension)s?|multiverse|alternate (reality|dimension|timeline)"),
 "Chosen one": ("story", ["prophecy", "chosen one"], [], ["chosen one", "prophecy"], r"chosen one|the prophecy|prophesied|foretold"),
  "Treasure hunt": ("story", ["treasure hunting", "treasure"], [], ["treasure", "treasure hunt", "treasure map"], r"treasure (hunt|map|hunter)|lost treasure|hidden treasure|buried treasure"),
 "Journeys and road trips": ("story", ["travel", "road trip"], [], ["road trip", "road movie"], r"road trip|cross-country|across the country"),
 "Underdog story": ("story", ["underdog"], [], ["underdog"], r"underdogs?\b|against all odds"),
 "Resurrection": ("story", ["resurrection"], [], ["resurrection"], r"resurrect|back from the dead|brought back to life|rise from the grave"),
 "Kidnapping": ("story", ["kidnapping"], [], ["kidnapping", "abduction"], r"kidnap|abduct(ed|ion)"),
 "Escape plan": ("story", [], ["Escape Room"], ["escape", "prison escape"], r"\bescape (from|the)\b|break out of|plan (an|their) escape"),
 "Survival island": ("setting", ["island"], [], ["island", "shipwreck", "desert island"], r"stranded on (an?|the) (deserted |remote |mysterious )?island|shipwreck|castaway|deserted island"),
 "Coming home": ("theme", [], [], ["homecoming", "return home"], r"find (his|her|their) way home|journey home|get back home"),
 # ---------- themes ----------
 "Secret identity": ("theme", ["secret identity"], [], ["secret identity", "double life"], r"secret identity|double life|alter ego"),
 "Vigilante justice": ("theme", ["vigilante"], [], ["vigilante", "vigilantism"], r"vigilante|takes? the law into (his|her|their) own hands"),
 "Mind control": ("theme", ["mind control", "brainwashing"], [], ["mind control", "brainwashing", "hypnosis"], r"mind control|brainwash|hypnoti[sz]"),
 "Telepathy": ("trope", ["telepathy"], [], ["telepathy", "psychic"], r"telepath|read (people's )?minds|mind reader"),
 "Plague and outbreak": ("theme", ["epidemic", "pandemic", "virus"], [], ["virus", "epidemic", "pandemic", "plague", "outbreak"], r"\bplague\b|pandemic|outbreak|epidemic|deadly virus|infection spreads"),
 "Nuclear threat": ("theme", ["nuclear", "nuclear war"], [], ["nuclear war", "nuclear", "atomic bomb", "nuclear weapons"], r"nuclear (war|weapon|bomb|missile|holocaust)|atomic bomb|radiation"),
 "Cold War": ("setting", ["cold war"], ["Cold War"], ["cold war"], r"cold war|soviet|\bkgb\b"),
 "Surveillance state": ("theme", ["surveillance"], [], ["surveillance", "big brother"], r"surveillance|big brother|watched at all times"),
 "Simulated reality": ("story", ["simulation"], [], ["simulated reality", "virtual reality", "simulation"], r"simulated reality|reality is (a |just a )?simulation|trapped in a (virtual|digital|simulated) world|computer-generated world"),
 "Mutation": ("trope", ["mutation", "genetic engineering"], [], ["mutation", "mutant", "genetic engineering"], r"mutat|mutant|genetically (engineered|modified)"),
 "Deal with the devil": ("theme", ["deal with the devil", "contract"], [], ["deal with the devil", "faustian bargain", "pact"], r"deal with the devil|sold (his|her) soul|faustian|demonic pact"),
 "Afterlife": ("setting", ["afterlife", "heaven", "hell"], [], ["afterlife", "heaven", "hell", "purgatory", "limbo"], r"afterlife|purgatory|\blimbo\b|land of the dead|realm of the dead"),
 "Dreams and nightmares": ("setting", ["dreams", "dream"], [], ["dream", "dreams", "nightmare", "lucid dreaming"], r"\bdreams?\b world|nightmares?|lucid dream|inside (his|her|their) dreams"),
 "Loner hero": ("trope", ["hikikomori", "loner"], [], ["loner", "recluse"], r"\bloner\b|recluse|shut-in|hikikomori"),
 "Mentor and student": ("trope", ["mentor", "teacher"], [], ["mentor", "teacher", "student teacher relationship"], r"\bmentor|apprentice|\bmaster\b and (his|her) (student|pupil)|\bpupil\b"),
 "Evil corporation": ("theme", ["corporation"], [], ["evil corporation", "corporation", "corporate crime"], r"megacorp|evil corporation|corporation|conglomerate"),
 # ---------- settings ----------
 "Jungle": ("setting", ["jungle"], ["Jungle"], ["jungle", "rainforest", "amazon"], r"\bjungle|rainforest|\bamazon\b"),
 "Ancient Egypt": ("setting", ["egypt", "ancient egypt"], ["Egypt"], ["egypt", "ancient egypt", "pharaoh", "mummy"], r"\begypt|pharaoh|\bmummy\b|pyramids"),
 "Ancient Rome": ("setting", ["rome", "ancient rome"], ["Rome"], ["ancient rome", "roman empire", "gladiator", "rome"], r"ancient rome|roman empire|gladiator|\brome\b"),
  "Hospitals and doctors": ("setting", ["hospital", "medicine", "doctor"], ["Medical Sim"], ["hospital", "doctor", "surgeon", "nurse"], r"hospital|surgeon|\bdoctor\b|\bnurse\b"),
 "Courtroom": ("setting", ["law", "lawyer", "courtroom"], [], ["lawyer", "courtroom", "trial", "court case", "law"], r"courtroom|\btrial\b|lawyer|attorney|\bjury\b|prosecutor"),
 "Newsroom": ("setting", ["journalism"], [], ["journalism", "journalist", "reporter", "newspaper"], r"journalist|reporter|newspaper|newsroom"),
 "Circus and carnival": ("setting", ["circus"], [], ["circus", "carnival", "clown"], r"\bcircus|carnival|\bclowns?\b|amusement park"),
 "Summer vacation": ("setting", ["summer"], [], ["summer", "summer camp", "summer vacation"], r"summer (vacation|holiday|camp|break)|one summer"),
 "Christmas": ("setting", ["christmas"], ["Christmas"], ["christmas", "santa claus", "christmas eve"], r"christmas|santa claus|\bxmas\b"),
 "Halloween": ("setting", ["halloween"], ["Halloween"], ["halloween"], r"halloween|trick-or-treat"),
 "Mountains": ("setting", ["mountains"], [], ["mountains", "mountain climbing", "mountaineering"], r"mountain (climb|peak|pass|village)|climb(s|ing)? (the |a )?mountain|himalaya|\bsummit\b"),
 "Space station": ("setting", ["space station", "colony"], [], ["space station", "space colony"], r"space station|orbital station|space colony"),
 "Haunted house": ("setting", ["haunted house"], [], ["haunted house", "haunting", "haunted mansion"], r"haunted (house|mansion|manor|hotel|school)"),
 "Religious orders": ("setting", ["nun", "priest", "monk", "exorcist"], [], ["priest", "nun", "monk", "monastery", "exorcist"], r"\bpriest|\bnuns?\b|\bmonks?\b|monastery|convent"),
 "Festivals and fireworks": ("setting", ["festival", "fireworks"], [], ["fireworks", "festival"], r"fireworks|summer festival|\bfestival\b"),
 # ---------- tropes & icons ----------
 "Serial killer": ("trope", ["serial killer"], [], ["serial killer", "murderer"], r"serial killer|killing spree|\bslasher\b"),
 "Wolves": ("icon", ["wolves", "wolf"], ["Wolves"], ["wolf", "wolves", "wolf pack"], r"\bwol(f|ves)\b"),
 "Insects": ("icon", ["insects"], ["Insects"], ["insect", "insects", "bugs", "spider"], r"\binsects?\b|\bspiders?\b|\bants\b|\bbeetles?\b|\bbees\b"),
 "Talking animals": ("trope", ["talking animals"], [], ["talking animal", "anthropomorphism", "talking dog", "talking cat"], r"talking (animal|dog|cat|bird|fox)s?"),
 "Fairy tales": ("trope", ["fairy tale"], ["Fairy Tale"], ["fairy tale", "based on fairy tale"], r"fairy ?tale|once upon a time|brothers grimm"),
 "Dolls and puppets": ("icon", ["dolls"], [], ["doll", "puppet", "toys", "toy"], r"\bdolls?\b|puppet|\btoys?\b come to life|living toys?"),
 "Masks": ("icon", ["mask", "masks"], [], ["mask", "masked man", "masked vigilante"], r"\bmask(s|ed)?\b"),
 "Dancing": ("icon", ["dancing", "dance"], ["Dancing"], ["dance", "dancing", "dancer", "ballet"], r"\bdanc(e|er|ers|ing)\b|ballet"),
 "Surfing": ("icon", ["surfing"], [], ["surfing", "surfer"], r"\bsurf(ing|er|board)"),
 "Cosplay and fandom": ("icon", ["cosplay", "otaku culture"], [], ["cosplay", "fandom", "comic con"], r"cosplay|fandom|comic con"),
 "Artists and painters": ("trope", ["drawing", "manga artist", "artist"], ["Drawing"], ["painter", "artist", "painting"], r"\bpainters?\b|struggling artist|young artist"),
 "Writers and novelists": ("trope", ["writer", "novelist"], [], ["writer", "novelist", "author"], r"novelist|struggling writer|famous writer|best-?selling author|a writer\b"),
 "Teachers and classrooms": ("trope", ["teacher"], [], ["teacher", "student teacher relationship", "classroom"], r"\bteacher\b|classroom"),
 "Clowns": ("icon", [], [], ["clown", "killer clown"], r"\bclowns?\b"),
 "Monks and martial masters": ("trope", ["monk"], [], ["monk", "shaolin", "kung fu master"], r"shaolin|kung fu master|martial arts master"),
}

C_TEXT_ONLY = {"Tournaments": r"\btournament\b|championship bout|martial arts contest"}
COMPILED = {lab: re.compile(v[4], re.I) for lab, v in C.items() if v[4]}
COMPILED.update({lab: re.compile(p, re.I) for lab, p in C_TEXT_ONLY.items()})

def text_traits(text):
    """Keyword connectors: traits whose pattern appears in a description or plot summary."""
    if not text: return set()
    return {lab for lab, p in COMPILED.items() if p.search(text)}
