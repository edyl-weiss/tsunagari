# Tsunagatteru (つながってる)

"Tsunagatteru" is Japanese for "they're connected". It's a daily puzzle in the style of a manga manuscript page. Connect two titles, drawn from 18,211 anime, video games and movies, in six hops or fewer. Each hop needs the two titles to share **at least two traits** (mechanics, themes, settings, tropes, icons or story types).

## Play

`index.html` is the whole game: one self-contained file with the data built in. Open it in a browser, or publish it with GitHub Pages:

1. Push this repo to GitHub.
2. Go to **Settings → Pages**, choose **Deploy from a branch**, pick `main` and `/ (root)`.
3. The game is live at `https://<your-username>.github.io/<repo-name>/`.

## Deploy on Vercel

The repo includes `vercel.json` (static site, no build step) and `.vercelignore` (only `index.html` is uploaded).

- **From GitHub:** on vercel.com choose **Add New → Project**, import this repo, leave the framework as **Other**, and click **Deploy**.
- **From your computer:** run `npx vercel` in this folder, then `npx vercel --prod` to publish.

## Game modes

- **Daily and Practice:** connect two titles in six hops or fewer, where each hop shares at least two traits.
  - **Planning:** the target's traits are always visible, and matching traits glow on your cards.
  - **The hand:** you pick from 8 cards. Reshuffle once per hop, or tap a trait to deal only cards with it. Search covers every connection.
  - **Hot/cold meters:** always on for Easy, 5 peeks on Medium, 3 on Hard, off on Expert.
  - **Lifelines (once each):** Radar (hops left), Stepping stone (a card on a shortest route), Bridge trait (the trait most routes into the target use).
  - **Combos:** three hops in a row through three different kinds of trait score +50.
  - **Your route** builds as a manga comic strip. Stats, daily progress and streaks stay in the player's browser.
- **Detective:** a mystery title reveals its traits one at a time, vaguest first. Each wrong guess tells you how many traits it shares with the answer.
- **Bridge:** five 30-second rounds. Pick the one title that shares two traits with both sides.

## Repo layout

```
index.html              the game (generated; this is what GitHub Pages serves)
data/pack.json          compact title/trait graph plus precomputed puzzles (generated)
data/curated_graph.json 102 hand-tagged classics with written trait details
scripts/                the build pipeline
  fetch_data.sh         downloads the two source datasets into build/
  anime_prep.py         groups anime into franchises, picks English titles, estimates popularity
  extract_steam.py      pulls names, review counts and tags from the Steam dump
  movies.py             turns the IMDb Top 1000 into titles (TMDB keywords, genres, plot patterns, directors)
  movie_titles.py       English titles for movies listed under their original-language names
  vocab.py              canonical trait vocabulary and content filters
  connectors.py         56 cross-media traits and the keyword connectors (tags, movie keywords, regexes over store text and plot summaries) that detect them
  build_curated.py      builds data/curated_graph.json from the hand-written traits
  build_final.py        merges everything into one graph (2-shared-trait links)
  puzzles2.py           finds 3–6 hop puzzles between popular titles
  pack.py               writes data/pack.json
  make_page.py          injects the data into template.html and writes index.html
  template.html         page template (HTML, CSS, game logic)
  build_all.sh          runs the whole pipeline
```

## Rebuilding the data

Requires Python 3.10+ and about 2 GB of RAM.

```bash
pip install -r requirements.txt
cd scripts
./build_all.sh
```

`build/` holds the large downloads and intermediate files; it's ignored by git. To change only the look or the game logic, edit `scripts/template.html` and run `python3 make_page.py`. To change the hand-tagged classics, edit `scripts/build_curated.py`, run it, then rerun from `build_final.py` onward.

## Data sources and credits

- **Anime:** [manami-project/anime-offline-database](https://github.com/manami-project/anime-offline-database), licensed ODbL 1.0 / DbCL 1.0. Any public use of the derived data must credit it and keep the derived database under the ODbL.
- **Games:** Steam community tags and review counts from [leinstay/steamdb](https://github.com/leinstay/steamdb) (the Game Gauntlets catalogue). Check that repository's license before commercial use.
- **Movies:** the IMDb Top 1000 list as published in a public Kaggle dataset (mirrored on GitHub), with keywords from the TMDB 5000 and TMDB 10k datasets. The list is a 2020-era snapshot. This product uses TMDB data but is not endorsed or certified by TMDB.
- **Fonts:** QR Ames by QR Type (embedded in the page; a commercial license is required for public or commercial use), plus Knewave, Comic Neue, Rampart One and Zen Kaku Gothic New from Google Fonts.
