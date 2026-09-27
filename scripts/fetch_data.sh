#!/usr/bin/env bash
# Downloads the two source datasets into ../build (about 160 MB).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p ../build
curl -L -o ../build/aod.json https://github.com/manami-project/anime-offline-database/releases/latest/download/anime-offline-database-minified.json
curl -L -o ../build/steamdb.min.json.gz https://media.githubusercontent.com/media/leinstay/steamdb/main/steamdb.min.json.gz
# Movies: IMDb Top 1000 list plus two TMDB keyword datasets
mkdir -p ../build/movies
curl -L -o ../build/movies/imdb_top_1000.csv https://raw.githubusercontent.com/krishna-koly/IMDB_TOP_1000/main/imdb_top_1000.csv
curl -L -o ../build/movies/tmdb10k.csv https://raw.githubusercontent.com/yubialam/TMDB-5000-Movie-Dataset/main/tmdb_movies_data.csv
curl -L -o ../build/movies/tmdb5000.csv https://raw.githubusercontent.com/vamshi121/TMDB-5000-Movie-Dataset/main/tmdb_5000_movies.csv
