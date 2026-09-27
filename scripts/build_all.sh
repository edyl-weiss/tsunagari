#!/usr/bin/env bash
# Full rebuild: fetch data -> anime franchises -> Steam extract -> graph -> puzzles -> page.
set -euo pipefail
cd "$(dirname "$0")"
[ -f ../build/movies/imdb_top_1000.csv ] || ./fetch_data.sh
python3 anime_prep.py
python3 extract_steam.py
python3 build_final.py 13000 13000 1000    # anime pool, game pool, max titles per trait
python3 puzzles2.py                         # ~5 minutes
python3 pack.py
python3 make_page.py
