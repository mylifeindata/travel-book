"""Assemble index.html from the page parts plus data.js.

Kept in the repo so a rebuild cannot quietly reintroduce strings that were
deliberately removed (the full name, the old nickernst02 URLs).
Run after build/stats.py has regenerated data.js.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = 'https://mylifeindata.github.io/travel-book/'
TITLE = 'Where in the World is Nick'
# No full name here on purpose: the GitHub account was renamed to drop it.
DESC = ('Four years of one travel calendar, cleaned up and counted: 904 nights away, '
        '23 countries, 169,761 miles, an animated world map and a year-to-region-to-place Sankey.')

head = open(os.path.join(BASE, 'page_head.html')).read()
body = open(os.path.join(BASE, 'page_body.html')).read()
scr  = open(os.path.join(BASE, 'page_script.html')).read()
data = open(os.path.join(BASE, 'data.js')).read()
scr  = scr.replace('<script src="./data.js"></script>', '<script>\n' + data + '\n</script>')

# The Artifact host wraps the page itself, so that build gets no doctype/head/body.
open(os.path.join(BASE, 'travel.html'), 'w').write(head + '\n' + body + '\n' + scr)

# GitHub Pages serves the file directly, so that build is a full document.
doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<link rel="canonical" href="{SITE_URL}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>">
{head}
</head>
<body>
{body}
{scr}
</body>
</html>
'''
out = os.path.join(BASE, 'repo', 'index.html')
open(out, 'w').write(doc)

for path, label in ((os.path.join(BASE, 'travel.html'), 'artifact'), (out, 'pages')):
    txt = open(path).read()
    for bad in ('Nick Ernst', 'nickernst02'):
        assert bad not in txt, f'{label} build still contains {bad!r}'
    print(f'{label}: {os.path.getsize(path):,} bytes, clean')
