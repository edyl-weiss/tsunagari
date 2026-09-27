"""Inject data/pack.json into scripts/template.html and write a standalone ../index.html."""
t = open('template.html').read()
body = t.replace('__DATA__', open('../data/pack.json').read())
i = body.index('<style>'); j = body.index('</style>') + len('</style>')
html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{body[:i].strip()}
<style>html,body{{margin:0}}</style>
{body[i:j]}
</head>
<body>
{body[j:].strip()}
</body>
</html>
'''
open('../index.html', 'w').write(html)
print('wrote ../index.html', round(len(html.encode()) / 1e6, 2), 'MB')
