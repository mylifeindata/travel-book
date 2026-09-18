"""Write the public data/ exports from the payload stats.py just produced.

Run after stats.py. Keeps data/travel-log.csv, data/adjustments.csv and
data/travel-data.json in step with index.html so nobody downloads a stale CSV.
"""
import csv
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'repo', 'data')
os.makedirs(OUT, exist_ok=True)

src = open(os.path.join(BASE, 'data.js')).read()

# data.js is "const WORLD = ...;\nconst DATA = {...};" - take the DATA literal.
i = src.index('const DATA')
payload = src[src.index('=', i) + 1:].strip().rstrip(';')
DATA = json.loads(payload)

# Not useful outside the page: the world outline and the per-day render helpers.
pub = {k: v for k, v in DATA.items() if k not in ('path',)}
with open(os.path.join(OUT, 'travel-data.json'), 'w') as f:
    json.dump(pub, f, indent=1)

B = DATA['bucket_names']
with open(os.path.join(OUT, 'travel-log.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['start', 'end', 'nights', 'place', 'country', 'region',
                'is_home', 'is_side_trip', 'inferred_home'])
    for t in DATA['trips']:
        w.writerow([t['s'], t['e'], t['n'], t['place'], t['country'], B[t['b']],
                    int(t['home']), int(t['side']), int(t['filled'])])

with open(os.path.join(OUT, 'adjustments.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['action', 'event', 'change', 'reason'])
    for c in DATA['changes']:
        w.writerow([c['kind'], c['event'], c['detail'], c['why']])

# The legs behind the distance total, so the number can be checked by hand.
with open(os.path.join(OUT, 'distance-legs.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['arrived', 'place', 'country', 'lat', 'lon', 'leg_km', 'cumulative_km'])
    run = 0.0
    for p in DATA['path']:
        run += p['km']
        w.writerow([p['d'], p['place'], p['country'], p['lat'], p['lon'],
                    p['km'], round(run, 1)])

for n in ('travel-data.json', 'travel-log.csv', 'adjustments.csv', 'distance-legs.csv'):
    print(f'{n}: {os.path.getsize(os.path.join(OUT, n)):,} bytes')
