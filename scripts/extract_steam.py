"""Pull the fields the game needs out of the Steam catalogue dump (games with 80+ reviews and community tags)."""
import gzip, ijson, json, re, html
keep = []
with gzip.open('../build/steamdb.min.json.gz', 'rb') as f:
    for g in ijson.items(f, 'item'):
        rc = g.get('steam_reviews_count') or 0
        tags = g.get('tags') or []
        if rc < 80 or not tags: continue
        d = g.get('description') or ''
        d = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', d))).strip()[:1200]  # store text for keyword connectors
        keep.append(dict(name=g['name'], reviews=int(rc), date=g.get('release_date'), tags=tags, devs=(g.get('developers') or [])[:2], desc=d))
json.dump(keep, open('../build/steam_small.json', 'w'))
print(len(keep), 'games')
