import json, datetime as dt, statistics, sys
from collections import defaultdict, Counter
sys.path.insert(0,'/root/travel')
from coords import COORD

trips = json.load(open('/root/travel/trips.json'))
d = lambda s: dt.date.fromisoformat(s)
START, TODAY = dt.date(2022,10,1), dt.date(2026,9,1)
HOME_PLACE, HOME_COUNTRY = 'Wheaton, IL', 'United States'
# BUCKETS fixes the colour index for each region and never changes.
BUCKETS = ['Home','United States','Central America & Mexico','South America','Europe','Africa','Asia']
BI = {b:i for i,b in enumerate(BUCKETS)}
# DISPLAY is the top-to-bottom stacking order, with Home and the US pushed to the
# bottom. Validated for colourblind safety as an adjacent sequence in both themes.
DISPLAY = ['Central America & Mexico','South America','Europe','Africa','Asia','United States','Home']

for t in trips:
    s, e = max(d(t['start']), START), min(d(t['end']), TODAY)
    t['_s'], t['_e'] = s, e
    outside = (s - d(t['start'])).days + (d(t['end']) - e).days
    t['n'] = max(0, t['nights'] - outside)
    if t['cont'] == 'Home': t['place'] = HOME_PLACE
trips = [t for t in trips if t['n'] > 0]

# Every day in the window belongs to exactly one stay. Side trips win over the
# stay that surrounds them; anything still unclaimed is a night at home.
owner = {}
for t in sorted(trips, key=lambda t: (t['side'], t['_s'])):
    x = t['_s']
    while x < t['_e']: owner[x] = t; x += dt.timedelta(days=1)

home_runs, x, run = [], START, None
while x <= TODAY:
    inside = x < TODAY and x not in owner
    if inside and run is None: run = x
    if (not inside) and run is not None:
        home_runs.append((run, x)); run = None
    x += dt.timedelta(days=1)

for a,b in home_runs:
    t = dict(start=a.isoformat(), end=b.isoformat(), summary='Home', place=HOME_PLACE,
             country=HOME_COUNTRY, cont='Home', nights=(b-a).days, side=False,
             _s=a, _e=b, n=(b-a).days, filled=True)
    trips.append(t)
    y = a
    while y < b: owner[y] = t; y += dt.timedelta(days=1)

trips.sort(key=lambda t: (t['_s'], t['_e']))
for t in trips: t.setdefault('filled', False)

window_days = (TODAY - START).days
assert len(owner) == window_days, (len(owner), window_days)

home_nights = sum(1 for t in owner.values() if t['cont']=='Home')
away_nights = window_days - home_nights
away_trips = [t for t in trips if t['cont']!='Home']
countries = sorted({t['country'] for t in trips if t['country']})
places    = sorted({t['place'] for t in trips if t['place']})
away_places = sorted({t['place'] for t in away_trips})

# The country ranking counts nights AWAY only. Home is its own number elsewhere,
# so the US total here is US travel, not US travel plus 533 nights in Wheaton.
nights_c, stays_c, nights_b = Counter(), Counter(), Counter()
for t in owner.values():
    nights_b[t['cont']] += 1
    if t['cont'] != 'Home': nights_c[t['country']] += 1
for t in away_trips:
    stays_c[t['country']] += 1

years = defaultdict(lambda: {'away':0,'home':0,'trips':0,'countries':set(),'places':set()})
for day, t in owner.items():
    years[day.year]['home' if t['cont']=='Home' else 'away'] += 1
for t in away_trips:
    y = years[t['_s'].year]; y['trips'] += 1
    y['countries'].add(t['country']); y['places'].add(t['place'])

year_rows = []
for y in sorted(years):
    ys, ye = max(dt.date(y,1,1), START), min(dt.date(y+1,1,1), TODAY)
    dd = (ye-ys).days; v = years[y]
    year_rows.append(dict(year=y, nights=v['away'], home=v['home'], trips=v['trips'],
                          countries=len(v['countries']), places=len(v['places']),
                          days_in_year=dd, pct=round(100*v['away']/dd,1),
                          partial=(dd < 360)))

# Sankey: year -> bucket -> destination. Inside the US bucket each place is its own
# node; everywhere else the node is the country.
def dest(t):
    return t['place'] if t['cont'] in ('Home','United States') else t['country']

sk_yb, sk_bd = Counter(), Counter()
for day, t in owner.items():
    sk_yb[(str(day.year), t['cont'])] += 1
    sk_bd[(t['cont'], dest(t))] += 1

yrs = sorted({str(t['_s'].year) for t in trips})
bucks = [b for b in DISPLAY if any(k[1]==b for k in sk_yb)]
by_b = defaultdict(list)
for (b,k), v in sk_bd.items(): by_b[b].append((k,v))
dest_order = []
for b in bucks:
    for k,_ in sorted(by_b[b], key=lambda x:(-x[1], x[0])): dest_order.append((b,k))

nodes = ([{'id':'Y'+y,'label':y,'layer':0,'b':-1} for y in yrs] +
         [{'id':'B'+b,'label':b,'layer':1,'b':BI[b],'home':b=='Home'} for b in bucks] +
         [{'id':'D'+b+'|'+k,'label':k,'layer':2,'b':BI[b],'home':b=='Home'} for b,k in dest_order])
links = ([{'s':'Y'+k[0],'t':'B'+k[1],'v':v,'b':BI[k[1]],'home':k[1]=='Home'}
          for k,v in sorted(sk_yb.items(), key=lambda x:(yrs.index(x[0][0]), bucks.index(x[0][1])))] +
         [{'s':'B'+k[0],'t':'D'+k[0]+'|'+k[1],'v':v,'b':BI[k[0]],'home':k[0]=='Home'}
          for k,v in sorted(sk_bd.items(), key=lambda x:dest_order.index((x[0][0],x[0][1])))])

# Map: chronological sequence of stays with coordinates, for markers and arcs.
missing = sorted({t['place'] for t in trips if t['place'] not in COORD})
if missing: print('!! MISSING COORDS:', missing)
seq = []
for t in trips:
    if t['place'] in COORD:
        la, lo = COORD[t['place']]
        seq.append({'s':t['_s'].isoformat(),'e':t['_e'].isoformat(),'place':t['place'],
                    'country':t['country'],'b':BI[t['cont']],'n':t['n'],
                    'lat':la,'lon':lo,'home':t['cont']=='Home','side':t['side']})

# The true movement path, walked day by day off the owner map. Deriving it this way
# rather than from the stay list gives the return hop after a nested side trip
# (Tarifa -> Morocco -> Tarifa -> Seville), which the stay list alone would skip.
path, prev = [], None
for day in sorted(owner):
    t = owner[day]
    if t['place'] != prev and t['place'] in COORD:
        la, lo = COORD[t['place']]
        path.append({'d':day.isoformat(),'place':t['place'],'country':t['country'],
                     'b':BI[t['cont']],'lat':la,'lon':lo,'home':t['cont']=='Home'})
        prev = t['place']

import math
def haversine(a, b):
    R = 6371.0088  # km, mean Earth radius
    p1, p2 = math.radians(a['lat']), math.radians(b['lat'])
    dp, dl = p2 - p1, math.radians(b['lon'] - a['lon'])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(h))

path[0]['km'] = 0.0
for i in range(1, len(path)):
    path[i]['km'] = round(haversine(path[i-1], path[i]), 1)
total_km = round(sum(p['km'] for p in path))

place_totals = Counter()
for t in owner.values(): place_totals[t['place']] += 1
map_places = [{'place':p,'lat':COORD[p][0],'lon':COORD[p][1],'n':v,
               'b':BI[next(t['cont'] for t in trips if t['place']==p)],
               'country':next(t['country'] for t in trips if t['place']==p)}
              for p,v in place_totals.most_common() if p in COORD]

longest = sorted(away_trips, key=lambda t:-t['n'])[:10]
us = nights_c['United States']  # away nights in the US

changes = json.load(open('/root/travel/changes.json'))
data = dict(
  meta=dict(window_start=START.isoformat(), window_end=TODAY.isoformat(), window_days=window_days,
            total_nights=away_nights, home_nights=home_nights,
            pct=round(100*away_nights/window_days,1),
            n_trips=len(away_trips), n_countries=len(countries), n_places=len(away_places),
            n_buckets=len(bucks), us_nights=us, intl_nights=away_nights-us,
            median_trip=int(statistics.median([t['n'] for t in away_trips])),
            max_trip=max(t['n'] for t in away_trips),
            home_place=HOME_PLACE,
            total_km=total_km, total_mi=round(total_km*0.621371),
            n_legs=sum(1 for p in path if p['km'] > 0),
            earth_laps=round(total_km/40075.017, 2)),
  bucket_names=BUCKETS, display_order=DISPLAY,
  nights_by_bucket={b:nights_b[b] for b in DISPLAY if nights_b[b]},
  years=year_rows,
  countries=[{'name':k,'nights':v,'trips':stays_c[k],
              'b':BI[next(t['cont'] for t in away_trips if t['country']==k)]}
             for k,v in nights_c.most_common()],
  longest=[{'place':t['place'],'country':t['country'],'b':BI[t['cont']],
            'start':t['_s'].isoformat(),'end':t['_e'].isoformat(),'n':t['n']} for t in longest],
  trips=[{'s':t['_s'].isoformat(),'e':t['_e'].isoformat(),'n':t['n'],'place':t['place'],
          'country':t['country'],'b':BI[t['cont']],'side':t['side'],
          'filled':t['filled'],'home':t['cont']=='Home'} for t in trips],
  seq=seq, path=path, map_places=map_places,
  sankey=dict(nodes=nodes, links=links),
  changes=[{'kind':c[0],'event':c[1],'detail':c[2],'why':c[3]} for c in changes],
)
open('/root/travel/data.js','w').write(
    'const WORLD = ' + json.dumps(open('/root/travel/world.txt').read()) + ';\n' +
    'const DATA = ' + json.dumps(data, separators=(',',':'), ensure_ascii=False) + ';')

print(f"Window {START} to {TODAY} ({window_days} days)")
print(f"Away {away_nights} ({data['meta']['pct']}%) | Home {home_nights} | stays away {len(away_trips)}")
print(f"Countries {len(countries)} | away places {len(away_places)} | median {data['meta']['median_trip']} | longest {data['meta']['max_trip']}")
print("\nBy bucket (stack order):"); [print(f"  {b:<26}{nights_b[b]:>4}n") for b in DISPLAY if nights_b[b]]
print("\nBy year:"); [print(f"  {r['year']}  away {r['nights']:>3} / home {r['home']:>3} of {r['days_in_year']:>3}d = {r['pct']:>5}%  {r['trips']:>2} stays, {r['countries']} countries") for r in year_rows]
print("\nLongest away:"); [print(f"  {t['n']:>3}n  {t['place']}, {t['country']} ({t['start']})") for t in data['longest'][:6]]
print(f"\nSankey nodes {len(nodes)} links {len(links)} | map points {len(map_places)} | seq {len(seq)} | path {len(path)}")
n_legs = sum(1 for p in path if p["km"] > 0)
print(f"Distance: {total_km:,} km / {round(total_km*0.621371):,} mi over {n_legs} legs = {round(total_km/40075.017,2)} laps of the Earth")
print("CHECK owner days =", len(owner), "== window", window_days)
print("CHECK away+home =", away_nights+home_nights, "== window", window_days)
print("CHECK sum(country away) =", sum(nights_c.values()), "== away", away_nights)
print("CHECK sankey L1 =", sum(l['v'] for l in links if l['s'][0]=='Y'), "L2 =", sum(l['v'] for l in links if l['s'][0]=='B'))
