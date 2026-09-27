"""Six Degrees: Anime x Games — expanded trait graph (v3).
One title per franchise. Traits are narrow (2-4 titles) so shortest routes run 3-6 degrees.
A degree = one hop from a title to another title through one shared trait."""
import json, collections, itertools, sys

W = []
def w(i, l, m, y, aliases=(), f=None):
    W.append(dict(id=i, label=l, t="work", sub="Anime" if m == "a" else "Video game",
                  media="anime" if m == "a" else "game", franchise=f or l, year=y, aliases=list(aliases)))

# ---------------- anime ----------------
w("demonslayer","Demon Slayer: Kimetsu no Yaiba","a",2019,["Kimetsu no Yaiba","Demon Slayer"])
w("jjk","Jujutsu Kaisen","a",2020,["JJK"])
w("chainsaw","Chainsaw Man","a",2022,["CSM"])
w("spy","SPY×FAMILY","a",2022,["Spy x Family","Spy Family"])
w("aot","Attack on Titan","a",2013,["AoT","Shingeki no Kyojin","SnK"])
w("frieren","Frieren: Beyond Journey's End","a",2023,["Sousou no Frieren","Frieren"])
w("mha","My Hero Academia","a",2016,["MHA","Boku no Hero Academia","BNHA"])
w("klk","Kill la Kill","a",2013,["KLK"])
w("violet","Violet Evergarden","a",2018)
w("onepiece","One Piece","a",1999)
w("dbz","Dragon Ball Z","a",1989,["DBZ","Dragon Ball"])
w("naruto","Naruto Shippuden","a",2007,["Naruto"])
w("bebop","Cowboy Bebop","a",1998)
w("fmab","Fullmetal Alchemist: Brotherhood","a",2009,["FMAB","FMA","Fullmetal Alchemist"])
w("fatezero","Fate/Zero","a",2011,["Fate Zero","Fate"])
w("sao","Sword Art Online","a",2012,["SAO"])
w("deathnote","Death Note","a",2006)
w("opm","One-Punch Man","a",2015,["OPM","One Punch Man"])
w("spirited","Spirited Away","a",2001,["Sen to Chihiro"])
w("hxh","Hunter x Hunter","a",2011,["HxH","Hunter Hunter"])
w("sololeveling","Solo Leveling","a",2024,["Ore dake Level Up na Ken"])
w("oshinoko","Oshi no Ko","a",2023,["Oshi no Ko","My Star"])
w("dandadan","Dandadan","a",2024,["Dan Da Dan"])
w("bleach","Bleach","a",2004)
w("tokyoghoul","Tokyo Ghoul","a",2014)
w("mob","Mob Psycho 100","a",2016,["Mob Psycho"])
w("eva","Neon Genesis Evangelion","a",1995,["Evangelion","Eva","NGE"])
w("steinsgate","Steins;Gate","a",2011,["Steins Gate"])
w("codegeass","Code Geass","a",2006,["Code Geass Lelouch of the Rebellion"])
w("haikyu","Haikyu!!","a",2014,["Haikyuu","Haikyu"])
w("bluelock","Blue Lock","a",2022)
w("yourname","Your Name","a",2016,["Kimi no Na wa"])
w("akira","Akira","a",1988)
w("mononoke","Princess Mononoke","a",1997,["Mononoke Hime"])
w("gits","Ghost in the Shell","a",1995,["GITS"])
w("sailormoon","Sailor Moon","a",1992,["Bishoujo Senshi Sailor Moon"])
w("jojo","JoJo's Bizarre Adventure","a",2012,["JoJo","Jojos"])
w("vinland","Vinland Saga","a",2019)
w("neverland","The Promised Neverland","a",2019,["Yakusoku no Neverland","Promised Neverland"])
w("rezero","Re:Zero","a",2016,["Re Zero","Re:Zero Starting Life in Another World"])
w("konosuba","KonoSuba","a",2016,["Konosuba","God's Blessing on This Wonderful World"])
w("bocchi","Bocchi the Rock!","a",2022,["Bocchi"])
w("dungeonmeshi","Delicious in Dungeon","a",2024,["Dungeon Meshi"])
w("kaiju8","Kaiju No. 8","a",2024,["Kaiju 8","Kaiju Number 8"])
w("apothecary","The Apothecary Diaries","a",2023,["Kusuriya no Hitorigoto","Apothecary Diaries"])
w("sakamoto","Sakamoto Days","a",2025)
w("abyss","Made in Abyss","a",2017)
w("gurren","Gurren Lagann","a",2007,["Tengen Toppa Gurren Lagann","TTGL"])
w("drstone","Dr. Stone","a",2019,["Dr Stone"])
w("gundam","Mobile Suit Gundam","a",1979,["Gundam"])
# ---------------- games ----------------
w("ff7r","Final Fantasy VII Remake","g",2020,["FF7R","FFVII Remake","FF7","Final Fantasy 7"])
w("kh3","Kingdom Hearts III","g",2019,["KH3","Kingdom Hearts 3","Kingdom Hearts"])
w("nier","NieR:Automata","g",2017,["Nier Automata","Nier"])
w("p5","Persona 5","g",2016,["P5","Persona"])
w("catherine","Catherine","g",2011)
w("arise","Tales of Arise","g",2021,["Tales of"])
w("ninokuni","Ni no Kuni: Wrath of the White Witch","g",2011,["Ni no Kuni"])
w("darksouls","Dark Souls","g",2011)
w("pokemon","Pokémon Red and Blue","g",1996,["Pokemon","Pokemon Red","Pokemon Blue","Pokémon Red and Green"])
w("cp2077","Cyberpunk 2077","g",2020,["CP2077","Cyberpunk"])
w("minecraft","Minecraft","g",2011)
w("tetris","Tetris","g",1985)
w("gta5","Grand Theft Auto V","g",2013,["GTA 5","GTA V","GTA","Grand Theft Auto"])
w("rdr2","Red Dead Redemption 2","g",2018,["RDR2","Red Dead"])
w("mario","Super Mario Odyssey","g",2017,["Mario Odyssey","Mario"])
w("botw","The Legend of Zelda: Breath of the Wild","g",2017,["Zelda","BotW","Breath of the Wild"])
w("witcher3","The Witcher 3: Wild Hunt","g",2015,["Witcher 3","Witcher"])
w("skyrim","The Elder Scrolls V: Skyrim","g",2011,["Skyrim","Elder Scrolls"])
w("eldenring","Elden Ring","g",2022)
w("mhw","Monster Hunter: World","g",2018,["Monster Hunter","MHW"])
w("acnh","Animal Crossing: New Horizons","g",2020,["Animal Crossing","ACNH"])
w("stardew","Stardew Valley","g",2016,["Stardew"])
w("terraria","Terraria","g",2011)
w("smash","Super Smash Bros. Ultimate","g",2018,["Smash","Smash Bros","SSBU"])
w("overwatch","Overwatch","g",2016)
w("fortnite","Fortnite","g",2017)
w("sonic","Sonic the Hedgehog","g",1991,["Sonic"])
w("wukong","Black Myth: Wukong","g",2024,["Wukong","Black Myth"])
w("ittakestwo","It Takes Two","g",2021)
w("amongus","Among Us","g",2018)
w("hollowknight","Hollow Knight","g",2017)
w("undertale","Undertale","g",2015)
w("hades","Hades","g",2020)
w("sf2","Street Fighter II","g",1991,["Street Fighter","SF2"])
w("mgs","Metal Gear Solid","g",1998,["MGS","Metal Gear"])
w("re4","Resident Evil 4","g",2005,["RE4","Resident Evil"])
w("sh2","Silent Hill 2","g",2001,["Silent Hill"])
w("portal2","Portal 2","g",2011,["Portal"])
w("halo","Halo: Combat Evolved","g",2001,["Halo"])
w("gow","God of War (2018)","g",2018,["God of War","GoW"])
w("tlou","The Last of Us","g",2013,["TLOU","Last of Us"])
w("ghost","Ghost of Tsushima","g",2020,["Tsushima"])
w("deathstranding","Death Stranding","g",2019)
w("bg3","Baldur's Gate 3","g",2023,["BG3","Baldurs Gate"])
w("sekiro","Sekiro: Shadows Die Twice","g",2019,["Sekiro"])
w("yakuza0","Yakuza 0","g",2015,["Yakuza","Like a Dragon"])
w("pacman","Pac-Man","g",1980,["Pacman"])

CAT = {"mechanic":"Mechanic","theme":"Theme","setting":"Setting","trope":"Trope","icon":"Icon","story":"Story type"}
T = {}
def t(i, label, cat, aliases, members):
    assert i not in T, i
    T[i] = (label, cat, aliases, members)

# ---------------- mechanics & power systems ----------------
t("collect","Collect monsters to fight for you","mechanic",["monster collecting","catch monsters","familiars"],
  {"pokemon":"Catch and train Pokémon","ninokuni":"Tame and raise familiars"})
t("turnbased","Turn-based battles","mechanic",["turn based","turn-based combat"],
  {"pokemon":"Turn-based Pokémon battles","p5":"One More and All-Out Attacks","bg3":"D&D-style turn-based fights"})
t("elements","Elemental types and weaknesses","mechanic",["elements","type chart","weakness"],
  {"pokemon":"The type chart","ff7r":"Hit enemy weaknesses with Materia","genshin":""} )
t("summon","Summoning","mechanic",["summons","summon"],
  {"ff7r":"Summon Materia: Ifrit, Shiva","fatezero":"Masters summon Servants","jjk":"Megumi's shikigami"})
t("fbt","Fire, Blizzard and Thunder spells","mechanic",["fire blizzard thunder","elemental spells"],
  {"ff7r":"Fire, Blizzard, Thunder Materia","kh3":"Fire, Blizzard, Thunder magic"})
t("parry","Parry-focused sword fights","mechanic",["parry","deflect","riposte"],
  {"sekiro":"Deflect to break posture","ghost":"Perfect parries and standoffs"})
t("losecurrency","Lose your currency when you die","mechanic",["corpse run","souls","lose souls on death"],
  {"darksouls":"Souls left at your bloodstain","eldenring":"Runes left where you fell","hollowknight":"Geo held by your Shade"})
t("deathpower","Coming back from death is a power","mechanic",["return by death","resurrection","respawn"],
  {"rezero":"Return by Death","hades":"Death sends Zagreus home to try again","sekiro":"Resurrect mid-fight"})
t("climbglide","Climb and glide anywhere","mechanic",["climbing","gliding","paraglider"],
  {"botw":"Climb any surface, glide with the paraglider","genshin":""})
t("minecraft_craft","Mine and craft","mechanic",["mining","crafting","sandbox"],
  {"minecraft":"","terraria":""})
t("build","Build structures anywhere","mechanic",["building","base building"],
  {"minecraft":"Block building","fortnite":"Build walls and ramps mid-fight"})
t("cookmonsters","Cooking monster meat","mechanic",["cooking","monster cooking","cook monsters"],
  {"dungeonmeshi":"Laios's party cooks dungeon monsters","mhw":"Grill monster meat, eat at the canteen","botw":"Cook monster parts into elixirs"})
t("monsterparts","Gear made from monster parts","mechanic",["monster parts","crafting from monsters"],
  {"mhw":"Forge armor from carves","kaiju8":"Numbers weapons made from kaiju"})
t("capture","Copy an enemy's form","mechanic",["possession","transform into enemies","capture"],
  {"mario":"Cappy captures enemies","wukong":"Transform into yaoguai you've beaten"})
t("coins","Collect coins, rings or pellets","mechanic",["coins","rings","pellets"],
  {"mario":"Coins and Power Moons","sonic":"Rings","pacman":"Pac-dots"})
t("eatpower","Eat something to gain powers","mechanic",["power pellet","devil fruit","power up food"],
  {"onepiece":"Devil Fruits","pacman":"Power Pellets"})
t("highscore","Endless high-score chase","mechanic",["high score","arcade"],
  {"tetris":"","pacman":""})
t("blockpuzzle","Block puzzles","mechanic",["blocks","puzzle blocks"],
  {"tetris":"Falling tetrominoes","catherine":"Push and pull blocks to climb"})
t("physics","Physics puzzles","mechanic",["puzzles","physics"],
  {"portal2":"Portals, gels and lasers","botw":"Shrine puzzles"})
t("coop","Two-player co-op story","mechanic",["co-op","coop","two player"],
  {"ittakestwo":"Co-op only","portal2":"Atlas and P-body co-op campaign"})
t("brawler","Street brawler","mechanic",["brawling","beat em up","fist fight"],
  {"yakuza0":"Kiryu's fighting styles","sf2":"Street fights around the world"})
t("fighting","Versus fighting game","mechanic",["fighting game","versus"],
  {"sf2":"","smash":""})
t("handblast","Energy blast fired from the hands","mechanic",["kamehameha","hadouken","energy blast"],
  {"sf2":"Hadouken","dbz":"Kamehameha","naruto":"Rasengan"})
t("stretch","Stretching limbs","mechanic",["stretchy","rubber"],
  {"onepiece":"Luffy's rubber body","sf2":"Dhalsim's yoga limbs"})
t("stealth","Stealth missions","mechanic",["stealth","sneaking"],
  {"mgs":"Sneak past guards","ghost":"The Ghost's stealth kills"})
t("heist","Heists","mechanic",["heist","infiltration","robbery"],
  {"gta5":"The heist crews","p5":"Infiltrating Palaces","cp2077":"The Konpeki Plaza job"})
t("gamestats","Game-style levels and stats in the story","mechanic",["leveling","stats","levels","system"],
  {"sololeveling":"The System levels Jinwoo up","sao":"Aincrad's levels and skills","konosuba":"Adventurer Cards show stats"})
t("vr","Diving into virtual worlds","mechanic",["virtual reality","vr","cyberspace"],
  {"sao":"NerveGear full-dive VR","gits":"Diving into the net","cp2077":"Braindances"})
t("commanddead","Command an army of the dead","mechanic",["necromancy","shadow army","spirit ashes"],
  {"sololeveling":"Jinwoo's shadow soldiers","eldenring":"Spirit Ashes"})
t("rules","Powers bound by strict rules and vows","mechanic",["vows","rules","restrictions"],
  {"hxh":"Nen restrictions and vows","jjk":"Binding vows","deathnote":"The rules of the Death Note"})
t("stands","A fighting spirit that appears beside you","mechanic",["stand","persona","guardian spirit"],
  {"jojo":"Stands","p5":"Personas"})
t("breathing","Breathing techniques","mechanic",["hamon","breathing","total concentration"],
  {"jojo":"Hamon","demonslayer":"Total Concentration Breathing"})
t("psychic","Psychic powers","mechanic",["psychokinesis","telekinesis","esper"],
  {"mob":"Mob's psychic powers","akira":"Tetsuo's powers","dandadan":"Momo's psychokinesis"})
t("alchemy","Alchemy","mechanic",["alchemist","potions crafting"],
  {"fmab":"Equivalent exchange","witcher3":"Brew potions and bombs","skyrim":"The Alchemy skill"})
t("transform","Magical transformation sequence","mechanic",["henshin","transformation","magical girl"],
  {"sailormoon":"Moon Prism Power, Make Up!","klk":"Kamui transformations"})
t("goldenform","Seven magic gems and a golden super form","mechanic",["chaos emeralds","dragon balls","super form"],
  {"sonic":"Chaos Emeralds and Super Sonic","dbz":"Dragon Balls and Super Saiyan"})
t("grapple","Grappling hook","mechanic",["grapple","odm gear","hookshot"],
  {"aot":"Omni-directional mobility gear","sekiro":"The Loaded Axe grappling hook"})
# ---------------- themes ----------------
t("revenge","Revenge quest","theme",["revenge","vengeance","avenge"],
  {"vinland":"Thorfinn hunts Askeladd","oshinoko":"Aqua hunts his mother's killer","codegeass":"Lelouch against Britannia"})
t("grief","Grief after a death","theme",["grief","loss","mourning"],
  {"frieren":"Frieren after Himmel's death","violet":"Violet and the Major","sh2":"James and Mary"})
t("parent","Searching for a missing parent","theme",["missing parent","looking for mom","looking for dad"],
  {"hxh":"Gon looks for Ging","abyss":"Riko follows her mother Lyza","hades":"Zagreus seeks Persephone","ninokuni":"Oliver tries to bring back his mother"})
t("absentfather","Cold, absent father","theme",["absent father","distant dad"],
  {"eva":"Gendo Ikari","fmab":"Van Hohenheim"})
t("fatherkid","Parent and child on the road","theme",["father figure","dad and kid","father daughter","father son"],
  {"gow":"Kratos and Atreus","tlou":"Joel and Ellie","witcher3":"Geralt and Ciri"})
t("siblings","Sibling bond","theme",["siblings","brothers","sister"],
  {"fmab":"Ed and Al","demonslayer":"Tanjiro and Nezuko","oshinoko":"Aqua and Ruby"})
t("twins","Twins","theme",["twin"],
  {"oshinoko":"Aqua and Ruby","genshin":"The Traveler's lost twin"})
t("family","Found family","theme",["chosen family","found-family"],
  {"spy":"The Forgers","onepiece":"The Straw Hat crew","rdr2":"The Van der Linde gang"})
t("marriage","Marriage troubles","theme",["marriage","divorce","fake marriage"],
  {"ittakestwo":"Cody and May's divorce","catherine":"Vincent's cold feet","spy":"Loid and Yor's fake marriage"})
t("rebellion","Rebels against an empire","theme",["rebellion","revolution","resistance"],
  {"codegeass":"The Black Knights","gurren":"Team Dai-Gurren against the Spiral King","arise":"Dahna rises against Rena"})
t("megacorp","Evil megacorporation","theme",["megacorp","evil company","corporation"],
  {"ff7r":"Shinra","cp2077":"Arasaka","portal2":"Aperture Science","stardew":"JojaMart"})
t("nature","Nature versus industry","theme",["environment","nature","industry"],
  {"mononoke":"Irontown against the forest gods","ff7r":"Mako reactors drain the Planet"})
t("rebuild","Rebuilding civilization","theme",["rebuild","reconnect","civilization"],
  {"drstone":"Senku rebuilds science from scratch","deathstranding":"Reconnecting America"})
t("nokill","Choosing not to kill","theme",["pacifist","mercy","no kill"],
  {"undertale":"Spare every monster","vinland":"\"I have no enemies\""})
t("contract","Power from a supernatural deal","theme",["contract","deal","pact"],
  {"codegeass":"Geass from C.C.","deathnote":"Ryuk's notebook","chainsaw":"Contracts with devils"})
t("mindgames","Genius mind games","theme",["mind games","battle of wits","chess"],
  {"codegeass":"Lelouch's chess-like plans","deathnote":"Light versus L"})
t("mystery","Solving mysteries","theme",["detective","mystery","investigation"],
  {"apothecary":"Maomao's poison cases","deathnote":"L's investigation"})
t("anxiety","Shy, anxious hero","theme",["social anxiety","introvert","shy"],
  {"bocchi":"Bocchi's crippling anxiety","eva":"Shinji","mob":"Mob's quiet awkwardness"})
t("debt","Paying off a huge debt","theme",["debt","loan"],
  {"acnh":"Tom Nook's home loans","chainsaw":"Denji's father's debt"})
t("guilt","Monsters born from your own mind","theme",["guilt","nightmares","shadows"],
  {"sh2":"Pyramid Head","p5":"Shadows of distorted desires","catherine":"Vincent's nightmares"})
t("impostor","An impostor hiding in the group","theme",["impostor","traitor","sus"],
  {"amongus":"The Impostor","aot":"Titan shifters in the Scouts","kaiju8":"Kafka hides that he's a kaiju"})
t("elimination","Eliminated one by one","theme",["elimination","voted out"],
  {"bluelock":"Losers leave Blue Lock","amongus":"Emergency meeting votes","fortnite":"Last player standing"})
# ---------------- settings & places ----------------
t("shibuya","Shibuya","setting",["shibuya tokyo","shibuya crossing"],
  {"p5":"The Shibuya hub","jjk":"The Shibuya Incident"})
t("feudal","Feudal Japan","setting",["samurai era","sengoku","medieval japan"],
  {"sekiro":"Sengoku-era Ashina","ghost":"The Mongol invasion of 1274","mononoke":"Muromachi-era Japan"})
t("cyberpunk","Neon cyberpunk city","setting",["cyberpunk","neo tokyo","night city"],
  {"gits":"New Port City","cp2077":"Night City","akira":"Neo-Tokyo"})
t("shrines","Shinto gods and shrines","setting",["shinto","shrine","kami"],
  {"yourname":"Mitsuha's family shrine","spirited":"The bathhouse of the gods","mononoke":"The Forest Spirit"})
t("spiritworld","A child crosses into a spirit world","setting",["other world","spirit world","portal"],
  {"spirited":"Chihiro goes through the tunnel","ninokuni":"Oliver crosses to the other world"})
t("isekai","Sent to another world","setting",["isekai","another world","transported"],
  {"rezero":"Subaru is summoned","konosuba":"Kazuma is sent by Aqua","genshin":"The Traveler arrives in Teyvat"})
t("underground","Life underground","setting",["underground","caves","below the surface"],
  {"gurren":"Jiha Village","undertale":"Monsters sealed beneath Mount Ebott","hollowknight":"Hallownest"})
t("fallenkingdom","Explore a fallen kingdom","setting",["ruined kingdom","fallen kingdom"],
  {"hollowknight":"Hallownest","darksouls":"Lordran","botw":"Hyrule after the Calamity"})
t("overgrown","Nature has reclaimed the ruins","setting",["post apocalyptic","overgrown","ruins"],
  {"nier":"The overgrown city","tlou":"Overgrown cities","drstone":"3,700 years of wilderness"})
t("ruinedamerica","A collapsed America","setting",["america","post-apocalyptic america"],
  {"tlou":"","deathstranding":"The United Cities of America"})
t("walls","Trapped behind giant walls","setting",["walls","wall"],
  {"aot":"Walls Maria, Rose and Sina","neverland":"The wall around Grace Field"})
t("orphanage","Orphanage kids","setting",["orphans","orphanage"],
  {"neverland":"Grace Field House","abyss":"Belchero Orphanage"})
t("dungeon","Delving deeper into a dungeon","setting",["dungeon","abyss","dungeon crawl"],
  {"abyss":"The Abyss","dungeonmeshi":"The dungeon","sololeveling":"Gates and dungeons"})
t("space","Life in outer space","setting",["space","spaceship","space colony"],
  {"bebop":"The Bebop","amongus":"The Skeld","gundam":"Space colonies"})
t("spacewar","War among the stars","setting",["space war"],
  {"halo":"Humanity versus the Covenant","gundam":"The One Year War"})
t("underworld","The afterlife or underworld","setting",["afterlife","underworld","hell"],
  {"hades":"The Underworld","bleach":"Soul Society"})
t("norse","Vikings and Norse lore","setting",["norse","vikings","nordic"],
  {"gow":"Midgard and the Nine Realms","vinland":"Viking-age Europe","skyrim":"Nords and Sovngarde"})
t("china","Ancient China-inspired world","setting",["china","chinese","imperial china"],
  {"apothecary":"The imperial rear palace","wukong":"Journey to the West"})
t("court","Royal court intrigue","setting",["palace","royal family","court"],
  {"apothecary":"The rear palace","codegeass":"The Britannian royal family"})
t("farm","Farming life","setting",["farming","farm","village life"],
  {"stardew":"Grandpa's farm","acnh":"Island life","vinland":"Ketil's farm"})
t("villagers","Villagers move into your town","setting",["villagers","npcs move in","town"],
  {"acnh":"Islanders move in","terraria":"Town NPCs move in"})
t("school","Special school for fighters","setting",["hero school","academy","school"],
  {"mha":"U.A. High","jjk":"Jujutsu High","klk":"Honnouji Academy"})
t("creepytown","Creepy isolated town","setting",["village","town","horror town"],
  {"re4":"The Ganado village","sh2":"The town of Silent Hill"})
# ---------------- tropes ----------------
t("eatpeople","Monsters that eat people","trope",["man-eating monsters","cannibal"],
  {"tokyoghoul":"Ghouls","aot":"Titans","neverland":"Demons","demonslayer":"Demons"})
t("halfmonster","Half-human, half-monster hero","trope",["hybrid","half monster"],
  {"tokyoghoul":"Kaneki, the half-ghoul","chainsaw":"Denji, the Chainsaw Devil hybrid","kaiju8":"Kafka, Kaiju No. 8"})
t("agency","Government anti-monster agency","trope",["defense force","public safety"],
  {"chainsaw":"Public Safety Devil Hunters","kaiju8":"The Defense Force"})
t("swordcorps","Sword-wielding demon hunters","trope",["demon hunters","soul reapers","slayers"],
  {"demonslayer":"The Demon Slayer Corps","bleach":"The Gotei 13"})
t("curses","Exorcising curses and hollows","trope",["exorcist","curses","hollows"],
  {"jjk":"Cursed spirits","bleach":"Hollows"})
t("ghosts","Fighting ghosts","trope",["ghosts","spirits","yokai"],
  {"pacman":"Blinky, Pinky, Inky and Clyde","dandadan":"Turbo Granny and friends","mob":"Evil spirits"})
t("aliens","Alien invaders","trope",["aliens","extraterrestrial"],
  {"dandadan":"The Serpoians","halo":"The Covenant","dbz":"Frieza and the Saiyans"})
t("shinigami","Shinigami","trope",["death god","soul reaper"],
  {"deathnote":"Ryuk","bleach":"Soul Reapers"})
t("sealed","Monster sealed inside the hero","trope",["sealed beast","jinchuriki","demon inside"],
  {"naruto":"Kurama","jjk":"Sukuna"})
t("rival","Best-friend rival","trope",["rival","childhood rival"],
  {"naruto":"Sasuke","kh3":"Riku","pokemon":"Blue","mha":"Bakugo"})
t("chosen","The chosen one of prophecy","trope",["chosen one","prophecy","destined hero"],
  {"skyrim":"The Dragonborn","kh3":"The Keyblade chose Sora","naruto":"The Child of Prophecy"})
t("strongest","Overpowered hero","trope",["op","strongest","overpowered"],
  {"opm":"Saitama","jjk":"Gojo","sololeveling":"Sung Jinwoo"})
t("heroes","A team of superheroes","trope",["superheroes","heroes","hero team"],
  {"mha":"Pro heroes","opm":"The Hero Association","overwatch":"The Overwatch strike team"})
t("kaiju","Giant monsters attacking the city","trope",["kaiju","monster attack","giant monster"],
  {"eva":"The Angels","kaiju8":"Kaiju","opm":"Mysterious Beings"})
t("robots","Giant robots","trope",["mecha","mech","robot"],
  {"eva":"Evangelion Units","gundam":"Mobile suits","gurren":"Gurren Lagann"})
t("robotwar","War with the machines","trope",["robot uprising","machines","omnics"],
  {"overwatch":"The Omnic Crisis","nier":"Androids against machine lifeforms"})
t("ai","An AI with a mind of its own","trope",["ai","artificial intelligence"],
  {"portal2":"GLaDOS","gits":"The Puppet Master","halo":"Cortana"})
t("madscientist","Mad scientist","trope",["scientist","mad science"],
  {"steinsgate":"Okabe, self-styled mad scientist","portal2":"Cave Johnson","sonic":"Dr. Eggman"})
t("clones","Clones","trope",["clone"],
  {"mgs":"Snake, clone of Big Boss","eva":"Rei","naruto":"Shadow Clone Jutsu"})
t("supersoldier","Super soldier","trope",["super soldier","spartan"],
  {"halo":"Master Chief","mgs":"Solid Snake"})
t("agent","Secret agent","trope",["spy","secret agent"],
  {"mgs":"Solid Snake","spy":"Loid, codename Twilight"})
t("assassin","Assassin living a normal life","trope",["hitman","assassin"],
  {"sakamoto":"Taro Sakamoto","spy":"Yor, the Thorn Princess"})
t("bounty","Bounties and wanted posters","trope",["bounty","bounty hunter","wanted"],
  {"onepiece":"Wanted posters","bebop":"Spike and Jet","rdr2":"Bounty hunting","sakamoto":"The billion-yen bounty"})
t("hunter","Monster hunter for hire","trope",["monster hunter","witcher"],
  {"witcher3":"Witcher contracts","mhw":"The Research Commission's quests"})
t("gangsters","Gangsters and the mob","trope",["mafia","yakuza","gang"],
  {"yakuza0":"The Tojo Clan","gta5":"","bebop":"The Red Dragon Syndicate"})
t("western","Western outlaws","trope",["cowboy","outlaws","western"],
  {"rdr2":"","bebop":"A space western"})
t("cat","Cat sidekick","trope",["cat","talking cat","palico"],
  {"p5":"Morgana","sailormoon":"Luna","mhw":"Your Palico"})
t("elves","Elves","trope",["elf","half-elf"],
  {"frieren":"Frieren","dungeonmeshi":"Marcille","skyrim":"Altmer, Bosmer and Dunmer","bg3":"Astarion and friends"})
t("mages","Mages","trope",["mage","wizard","magic"],
  {"frieren":"Frieren and Fern","konosuba":"Megumin","fatezero":"Magi"})
t("demonking","The Demon King","trope",["demon lord","demon king"],
  {"frieren":"Defeated before the story","konosuba":"Kazuma's goal"})
t("reincarnation","Reincarnated into a new life","trope",["reincarnation","reborn"],
  {"oshinoko":"Reborn as Ai's twins","konosuba":"Kazuma after his death","sailormoon":"Princess Serenity"})
t("amnesia","Amnesiac hero","trope",["amnesia","lost memories","memory loss"],
  {"botw":"Link wakes after 100 years","arise":"Alphen remembers nothing","ff7r":"Cloud's unreliable memories"})
t("silent","Silent protagonist","trope",["silent hero","mute protagonist"],
  {"botw":"Link","hollowknight":"The Knight","pokemon":"Red"})
t("princess","Rescue the princess","trope",["princess","damsel"],
  {"mario":"Peach","botw":"Zelda"})
t("escort","Protect your companion","trope",["escort","protect"],
  {"re4":"Ashley","tlou":"Ellie"})
t("parasites","Parasites that take over people","trope",["parasite","infection","tadpole"],
  {"re4":"Las Plagas","tlou":"Cordyceps","bg3":"Mind flayer tadpoles"})
t("fourthwall","Breaks the fourth wall","trope",["fourth wall","meta"],
  {"undertale":"Flowey remembers your saves","mgs":"Psycho Mantis reads your memory card"})
t("vampires","Vampires","trope",["vampire"],
  {"jojo":"Dio","skyrim":"Vampirism","witcher3":"Katakans and higher vampires"})
t("sunlight","Sunlight destroys them","trope",["sunlight","daylight"],
  {"demonslayer":"Demons burn in the sun","jojo":"Vampires and Pillar Men","minecraft":"Zombies burn at dawn"})
t("night","Monsters come out at night","trope",["night","nighttime"],
  {"minecraft":"","terraria":""})
t("stone","Turned to stone","trope",["petrified","petrification","stone"],
  {"drstone":"All of humanity","jojo":"The Pillar Men"})
t("godkiller","Killing gods","trope",["god slayer","deicide"],
  {"gow":"Kratos against the Aesir","wukong":"Fighting Heaven's armies"})
t("sunwukong","The Monkey King","trope",["sun wukong","monkey king","journey to the west"],
  {"wukong":"The Destined One follows Sun Wukong","dbz":"Goku is based on Sun Wukong"})
t("wish","A wish-granting prize","trope",["wish","holy grail"],
  {"dbz":"The Dragon Balls","fatezero":"The Holy Grail"})
t("dragons","Dragons","trope",["dragon"],
  {"skyrim":"Alduin and the dragons","eldenring":"Dragons of the Lands Between","darksouls":"Everlasting dragons","dbz":"Shenron"})
t("insects","Insect monsters","trope",["bugs","insects","chimera ants"],
  {"hxh":"The Chimera Ants","hollowknight":"A kingdom of bugs"})
t("ninja","Ninjas","trope",["ninja","shinobi"],
  {"naruto":"","sekiro":"Wolf, the shinobi"})
# ---------------- icons ----------------
t("masks","Masks","icon",["mask"],
  {"p5":"Phantom Thief masks","tokyoghoul":"Ghoul masks","spirited":"No-Face","demonslayer":"Urokodaki's fox masks"})
t("katana","Katana","icon",["sword","katana","samurai sword"],
  {"demonslayer":"Nichirin blades","bleach":"Zanpakutō","onepiece":"Zoro's three swords","ghost":"Jin's katana","sekiro":"Kusabimaru"})
t("bigsword","Oversized sword","icon",["giant sword","buster sword","greatsword"],
  {"ff7r":"The Buster Sword","klk":"The Scissor Blade","darksouls":"Greatswords"})
t("motorcycle","Iconic motorcycle","icon",["motorbike","bike"],
  {"akira":"Kaneda's bike","ff7r":"The Midgar highway chase"})
t("tree","A giant sacred tree","icon",["world tree","erdtree","deku tree"],
  {"eldenring":"The Erdtree","genshin":"Irminsul","botw":"The Great Deku Tree"})
t("horse","Trusty horse","icon",["horse","roach","torrent"],
  {"rdr2":"Arthur's horse","witcher3":"Roach","eldenring":"Torrent"})
t("hearts","Hearts","icon",["heart","stealing hearts"],
  {"kh3":"Hearts and the Heartless","p5":"Stealing hearts"})
t("prosthetic","Prosthetic arms","icon",["automail","robot arm","prosthetics"],
  {"fmab":"Ed's automail","violet":"Violet's metal arms"})
t("letters","Delivering letters and packages","icon",["delivery","mail","letters"],
  {"violet":"Auto Memory Dolls write letters","deathstranding":"Sam the porter"})
t("timemail","Messages sent across time","icon",["time travel","messages to the past","d-mail"],
  {"steinsgate":"D-Mail","yourname":"Notes across three years"})
t("toys","Living toys","icon",["toys","toy story"],
  {"ittakestwo":"Cody and May as dolls","kh3":"The Toy Box world"})
t("crossover","All-star crossover","icon",["crossover","collab"],
  {"smash":"Everyone is here","kh3":"Disney meets Final Fantasy","fortnite":"Crossover skins"})
t("ghibli","Studio Ghibli","icon",["ghibli"],
  {"spirited":"","mononoke":"","ninokuni":"Ghibli animated the cutscenes"})
t("jazz","Jazzy soundtrack","icon",["jazz","soundtrack"],
  {"bebop":"The Seatbelts","p5":"Acid-jazz soundtrack"})
t("stage","On stage","icon",["idol","band","concert"],
  {"bocchi":"Kessoku Band","oshinoko":"B-Komachi"})
t("treasure","A legendary treasure hunt","icon",["treasure","relics"],
  {"onepiece":"The One Piece","abyss":"Relics of the Abyss"})
t("medicine","Brewing medicine","icon",["medicine","potions","pharmacy"],
  {"apothecary":"Maomao the apothecary","drstone":"Senku's sulfa drugs","witcher3":"Witcher potions"})
# ---------------- story types ----------------
t("timeloop","Time loops","story",["time loop","time leap"],
  {"rezero":"Return by Death","steinsgate":"Time leaps to save Mayuri"})
t("battleroyale","Battle royale","story",["battle royale","last one standing"],
  {"fortnite":"","fatezero":"The Holy Grail War"})
t("tower","Climb a tower floor by floor","story",["tower","floors","climbing"],
  {"sao":"The 100 floors of Aincrad","catherine":"The block towers"})
t("tournament","Tournament to be the best","story",["tournament","league","championship"],
  {"sf2":"The World Warrior tournament","pokemon":"The Pokémon League","haikyu":"Nationals"})
t("sports","Sports team","story",["sports","team"],
  {"haikyu":"Karasuno volleyball","bluelock":"Blue Lock soccer"})
t("journeyafter","Journey after a loss","story",["journey","road trip"],
  {"frieren":"Retracing Himmel's route","violet":"Violet travels for each letter"})
t("truending","Replays reveal the true ending","story",["true ending","new game plus","multiple endings"],
  {"nier":"Routes A, B and C","undertale":"The True Pacifist route"})
t("claimthrone","Claim the throne","story",["throne","become king","emperor"],
  {"eldenring":"Become Elden Lord","codegeass":"Lelouch becomes Emperor"})

# Genshin appears in trait lists above
w("genshin","Genshin Impact","g",2020,["Genshin"])

# ---- extra popular titles on the edges of the graph ----
w("kirby","Kirby and the Forgotten Land","g",2022,["Kirby"])
w("totoro","My Neighbor Totoro","a",1988,["Totoro","Tonari no Totoro"])
w("chrono","Chrono Trigger","g",1995,["Chrono"])
w("kon","K-On!","a",2009,["K-On","Keion"])
T["capture"][3]["kirby"]="Copy Abilities"
t("swallow","Swallow enemies whole","mechanic",["inhale","swallow","eat enemies"],
  {"kirby":"Inhale enemies","pacman":"Chomp ghosts after a Power Pellet"})
T["ghibli"][3]["totoro"]=""
t("forestspirit","Forest spirits","trope",["forest spirit","kodama"],
  {"totoro":"Totoro","mononoke":"The Forest Spirit and the kodama"})
t("timetravel","Travel back to change the past","story",["time travel","change the past"],
  {"chrono":"The Epoch and the time gates","steinsgate":"Rewriting worldlines"})
T["truending"][3]["chrono"]="New Game+ and a dozen endings"
T["stage"][3]["kon"]="Ho-kago Tea Time"
t("club","After-school club","setting",["school club","club activities"],
  {"kon":"The Light Music Club","haikyu":"Karasuno's volleyball club"})

# Tags left off on purpose: each one created a shortcut that collapsed most routes to 3 degrees or less.
for wid, tid in [("minecraft","sunlight"),("acnh","farm"),("spirited","masks"),("haikyu","tournament"),
                 ("oshinoko","stage"),("eva","anxiety"),("fortnite","elimination")]:
    del T[tid][3][wid]

nodes = {n["id"]: n for n in W}
rels = []
k = 0
for tid, (label, cat, aliases, members) in T.items():
    assert len(members) >= 2, tid
    nodes["t_" + tid] = dict(id="t_" + tid, label=label, t="trait", sub=CAT[cat], cat=cat, aliases=aliases)
    for wid, detail in members.items():
        assert wid in nodes and nodes[wid]["t"] == "work", (tid, wid)
        k += 1
        rels.append(dict(id=f"r{k:03d}", f=wid, to="t_" + tid, type=cat, detail=detail))

adj = collections.defaultdict(set)
for r in rels:
    adj[r["f"]].add(r["to"]); adj[r["to"]].add(r["f"])
works = [n["id"] for n in W]
low = [(wid, len(adj[wid])) for wid in works if len(adj[wid]) < 2]
def bfs(s):
    d = {s: 0}; q = [s]
    for x in q:
        for y in adj[x]:
            if y not in d:
                d[y] = d[x] + 1; q.append(y)
    return d
dist = collections.Counter()
for a, b in itertools.combinations(works, 2):
    dd = bfs(a).get(b); dist[None if dd is None else dd // 2] += 1
traits = [n for n in nodes.values() if n["t"] == "trait"]
print(len(works), "titles", len(traits), "traits", len(rels), "links")
print("degree distribution", sorted(dist.items(), key=lambda x: (x[0] is None, x[0] or 0)))
print("titles per trait", sorted(collections.Counter(len(v[3]) for v in T.values()).items()))
print("traits per title", sorted(collections.Counter(len(adj[w]) for w in works).items()))
print("under 2 traits:", low)
json.dump(dict(nodes=list(nodes.values()), rels=rels), open("../data/curated_graph.json", "w"), ensure_ascii=False, separators=(",", ":"))
