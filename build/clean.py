import json, datetime as dt

RAW = json.load(open('/root/travel/raw_events.json'))
TODAY = dt.date(2026, 9, 1)
WINDOW_START = dt.date(2022, 10, 1)

MARKERS = {"Babe Leaves for India", "Parents Arrive!", "Leave for FLL", "Parents back"}

# summary -> (display place, country, bucket)
# Bucket order drives the palette: Home, United States, Central America & Mexico,
# South America, Europe, Africa, Asia
P = {
 "Wheaton":("Home","United States","Home"),
 "Wheaton 2":("Home","United States","Home"),
 "Hanoi":("Hanoi","Vietnam","Asia"),
 "Hanoi Street Hotel":("Hanoi","Vietnam","Asia"),
 "Ha long Bay":("Ha Long Bay","Vietnam","Asia"),
 "Ninh Binh Vientam":("Ninh Binh","Vietnam","Asia"),
 "Seoul, South Korea":("Seoul","South Korea","Asia"),
 "Chiang Mai, Thailand":("Chiang Mai","Thailand","Asia"),
 "Pai, Thailand":("Pai","Thailand","Asia"),
 "Elephant Nature Park, Thailand":("Elephant Nature Park","Thailand","Asia"),
 "Pa Pae Meditation Retreat, Thailand":("Pa Pae Retreat","Thailand","Asia"),
 "Koh Tao - Sairee Cottage":("Koh Tao","Thailand","Asia"),
 "Koh Tao Sairee Upgrade":("Koh Tao","Thailand","Asia"),
 "Koh Tao Sairee Downgrade":("Koh Tao","Thailand","Asia"),
 "Koh Tao Sairee Hut":("Koh Tao","Thailand","Asia"),
 "Ao Nang":("Ao Nang","Thailand","Asia"),
 "Krabi":("Krabi","Thailand","Asia"),
 "Ko Lanta":("Ko Lanta","Thailand","Asia"),
 "Ko Lipe":("Ko Lipe","Thailand","Asia"),
 "Georgetown Malaysia":("George Town","Malaysia","Asia"),
 "Kuala Lumpur":("Kuala Lumpur","Malaysia","Asia"),
 "Bangkok":("Bangkok","Thailand","Asia"),
 "Bangkok 2":("Bangkok","Thailand","Asia"),
 "Bangkok 3":("Bangkok","Thailand","Asia"),
 "Phnom Penh":("Phnom Penh","Cambodia","Asia"),
 "Siem Reap":("Siem Reap","Cambodia","Asia"),
 "Ho Chi Minh - TEFL":("Ho Chi Minh City","Vietnam","Asia"),
 "Ubud Bali":("Ubud, Bali","Indonesia","Asia"),
 "Candi Dasa Bali":("Candidasa, Bali","Indonesia","Asia"),
 "Gili T":("Gili Trawangan","Indonesia","Asia"),
 "Nusa Penida":("Nusa Penida","Indonesia","Asia"),
 "Uluwatu":("Uluwatu, Bali","Indonesia","Asia"),
 "Surat Thani":("Surat Thani","Thailand","Asia"),
 "Koh Phangan":("Koh Phangan","Thailand","Asia"),
 "Wonderland Koh Pangan":("Wonderland, Koh Phangan","Thailand","Asia"),
 "Koh Tao":("Koh Tao","Thailand","Asia"),
 "Stay at Morgans":(None,None,None),
 "Hoi An":("Hoi An","Vietnam","Asia"),
 "Da Nang, Vietnam":("Da Nang","Vietnam","Asia"),
 "Hanoi, Vietnam":("Hanoi","Vietnam","Asia"),
 "Heathrow":("London Heathrow","United Kingdom","Europe"),
 "Bergamo, Italy":("Bergamo","Italy","Europe"),
 "Pontessieve, Italy Workaway":("Pontassieve","Italy","Europe"),
 "Rome":("Rome","Italy","Europe"),
 "Barcelona":("Barcelona","Spain","Europe"),
 "Barcelona 2":("Barcelona","Spain","Europe"),
 "San Sebastian":("San Sebastián","Spain","Europe"),
 "Ericeira":("Ericeira","Portugal","Europe"),
 "Ericeira 2":("Ericeira","Portugal","Europe"),
 "Lisbon":("Lisbon","Portugal","Europe"),
 "Lisbon Outsite":("Lisbon","Portugal","Europe"),
 "London":("London","United Kingdom","Europe"),
 "Stay with Fem parents in Utrecht":("Utrecht","Netherlands","Europe"),
 "Amsterdam":("Amsterdam","Netherlands","Europe"),
 "Pride in Amsterdam":("Amsterdam","Netherlands","Europe"),
 "Stay with Dela / Jepper - Sonderberg":("Sønderborg","Denmark","Europe"),
 "Workaway - Gjovik, Norway":("Gjøvik","Norway","Europe"),
 "Oslo, Norway":("Oslo","Norway","Europe"),
 "Madrid":("Madrid","Spain","Europe"),
 "Valencia":("Valencia","Spain","Europe"),
 "Valencia 2":("Valencia","Spain","Europe"),
 "Seville":("Seville","Spain","Europe"),
 "Granada":("Granada","Spain","Europe"),
 "Tarifa - WiFi Tribe chapter":("Tarifa","Spain","Europe"),
 "Morocco":("Morocco","Morocco","Africa"),
 "Fort Lauderdale":("Fort Lauderdale","United States","United States"),
 "Fort Lauderdale 2":("Fort Lauderdale","United States","United States"),
 "Ft Lauderdale":("Fort Lauderdale","United States","United States"),
 "Iowa":("Iowa","United States","United States"),
 "New Orleans- Quinn Bach party":("New Orleans","United States","United States"),
 "Chicago":("Home","United States","Home"),
 "Chicago 2":("Home","United States","Home"),
 "Mexico":("Mexico","Mexico","Central America & Mexico"),
 "Mexico City":("Mexico City","Mexico","Central America & Mexico"),
 "Mexico City 2":("Mexico City","Mexico","Central America & Mexico"),
 "San Miguel":("San Miguel de Allende","Mexico","Central America & Mexico"),
 "Denver":("Denver","United States","United States"),
 "Denver 2":("Denver","United States","United States"),
 "Thanksgiving in AZ":("Arizona","United States","United States"),
 "Arizona":("Arizona","United States","United States"),
 "Arizona 2":("Arizona","United States","United States"),
 "Arizona 3":("Arizona","United States","United States"),
 "Arizona 4":("Arizona","United States","United States"),
 "Arizona 5":("Arizona","United States","United States"),
 "Phoenix":("Phoenix","United States","United States"),
 "Phoenix 2":("Phoenix","United States","United States"),
 "Crested Butte":("Crested Butte, CO","United States","United States"),
 "Stay at Townhome in North Salt Lake":("Salt Lake City","United States","United States"),
 "New York":("New York","United States","United States"),
 "New York 2":("New York","United States","United States"),
 "New York 3":("New York","United States","United States"),
 "NY for work":("New York","United States","United States"),
 "Hoboken":("Hoboken, NJ","United States","United States"),
 "Hoboken 2":("Hoboken, NJ","United States","United States"),
 "Hoboken 3":("Hoboken, NJ","United States","United States"),
 "Hoboken 4":("Hoboken, NJ","United States","United States"),
 "SF":("San Francisco","United States","United States"),
 "SF 2":("San Francisco","United States","United States"),
 "SF 3":("San Francisco","United States","United States"),
 "San Jose":("San Jose, CA","United States","United States"),
 "Belize - Noma chapter":("Belize","Belize","Central America & Mexico"),
 "CO":("Colorado","United States","United States"),
 "CO Springs - John Retirement":("Colorado Springs","United States","United States"),
 "Arkansas":("Arkansas","United States","United States"),
 "Petoskey Michigan":("Petoskey, MI","United States","United States"),
 "Miami":("Miami","United States","United States"),
 "Omaha (slept on road)":("Omaha, NE","United States","United States"),
 "Costa Rica":("Costa Rica","Costa Rica","Central America & Mexico"),
 "Costa Rica 2":("Costa Rica","Costa Rica","Central America & Mexico"),
 "Costa Rica 3":("Costa Rica","Costa Rica","Central America & Mexico"),
 "Ross Bach - Vegas":("Las Vegas","United States","United States"),
 "Austin TX":("Austin","United States","United States"),
 "Wisconsin for Skiing":("Wisconsin","United States","United States"),
 "Decatur":("Decatur, IL","United States","United States"),
 "Decatur/Hillsboro":("Decatur / Hillsboro, IL","United States","United States"),
 "Antigua - WiFi Tribe Chapter":("Antigua","Guatemala","Central America & Mexico"),
 "Lake Atitlan":("Lake Atitlán","Guatemala","Central America & Mexico"),
 "Medellin Colombia":("Medellín","Colombia","South America"),
 "Medellín":("Medellín","Colombia","South America"),
 "Jas Bday Medellin":("Medellín","Colombia","South America"),
 "Cartagena":("Cartagena","Colombia","South America"),
 "Rio de Janerio NYE":("Rio de Janeiro","Brazil","South America"),
 "Pipa Brazil - noma chapter":("Pipa","Brazil","South America"),
 "Buenos Aires":("Buenos Aires","Argentina","South America"),
 "Iguazu":("Iguazú","Argentina","South America"),
 "Cusco":("Cusco","Peru","South America"),
 "Machu Picchu":("Machu Picchu","Peru","South America"),
 "Huacachina":("Huacachina","Peru","South America"),
 "Paracas":("Paracas","Peru","South America"),
 "Lima":("Lima","Peru","South America"),
 "Sri Lanka Chapter":("Sri Lanka","Sri Lanka","Asia"),
 "Casa Shambala":(None,None,None),
}

DURATION_FIX = {}
INFERRED = {
 "Stay with Dela / Jepper - Sonderberg":
   "Read 'Sonderberg' as Sønderborg, Denmark. Say the word if that is wrong.",
 "Antigua - WiFi Tribe Chapter":
   "Read as Antigua, Guatemala (not Antigua & Barbuda), since Lake Atitlán sits inside this stay.",
}

d = lambda s: dt.date.fromisoformat(s)
changes, trips = [], []

for start, end, summary in RAW:
    s, e = d(start), d(end)
    if summary in MARKERS:
        changes.append(("dropped", summary, start, "Reminder/marker, not a stay")); continue
    if s >= TODAY:
        changes.append(("future", summary, f"{start} to {end}", "Hasn't happened yet, excluded")); continue
    if e <= WINDOW_START:
        continue
    if summary in DURATION_FIX:
        ne, why = DURATION_FIX[summary]
        changes.append(("fixed duration", summary, f"{end} -> {ne}", why)); e = d(ne)
    if summary in INFERRED:
        changes.append(("inferred location", summary, f"{start} to {end}", INFERRED[summary]))

    place, country, cont = P.get(summary, (None, None, None))
    if country is None:
        changes.append(("unknown location", summary, f"{start} to {end}",
                        "No location on the event. Counted as time away, not attributed to a country."))
    trips.append(dict(start=s, end=e, summary=summary, place=place, country=country, cont=cont))

trips.sort(key=lambda t: (t['start'], t['end']))

for i, t in enumerate(trips):
    for j in range(i+1, len(trips)):
        o = trips[j]
        if o['start'] >= t['end']: break
        if o['end'] <= t['end']:
            t.setdefault('nested', []).append(j)
            o['is_side'] = True; o['side_of'] = t['summary']
        else:
            if t['end'] != o['start']:
                changes.append(("trimmed overlap", t['summary'], f"end {t['end']} -> {o['start']}",
                                f"Ran past the start of '{o['summary']}'"))
            t['end'] = o['start']

for t in trips:
    t['gross'] = (t['end'] - t['start']).days
    t['sub'] = 0

# A nested event at the SAME place as its parent (or with no location at all) is a
# room change or a booking detail, not a side trip. Fold it into the parent stay.
for t in trips:
    for j in t.get('nested', []):
        sub = trips[j]
        same_place = (sub['place'] == t['place'])
        no_place = (sub['country'] is None)
        if same_place or no_place:
            sub['absorbed'] = True
            changes.append(("merged booking", sub['summary'], f"{sub['start']} to {sub['end']}",
                            f"Same stay as '{t['summary']}' (room change or booking detail), not a separate trip."))
        else:
            t['sub'] += sub['gross']
            changes.append(("side trip", sub['summary'], f"{sub['start']} to {sub['end']}",
                            f"Sits inside '{t['summary']}'. Its {sub['gross']} nights subtracted from that stay."))

trips = [t for t in trips if not t.get('absorbed')]
for t in trips:
    t['nights'] = t['gross'] - t['sub']

# Consecutive stays at the SAME place are one stay, not several. The Koh Tao
# cottage/upgrade/downgrade/hut chain is one continuous fortnight on one island.
merged, i = [], 0
while i < len(trips):
    t = trips[i]; j = i + 1
    while (j < len(trips) and trips[j]['place'] is not None
           and trips[j]['place'] == t['place'] and trips[j]['start'] <= t['end']
           and not trips[j].get('is_side') and not t.get('is_side')):
        changes.append(("merged run", trips[j]['summary'], f"{trips[j]['start']} to {trips[j]['end']}",
                        f"Continues '{t['summary']}' at the same place. Counted as one stay."))
        t['end'] = max(t['end'], trips[j]['end'])
        t['nights'] += trips[j]['nights']
        j += 1
    merged.append(t); i = j
trips = merged

out = [dict(start=t['start'].isoformat(), end=t['end'].isoformat(), summary=t['summary'],
            place=t['place'], country=t['country'], cont=t['cont'],
            nights=t['nights'], side=bool(t.get('is_side'))) for t in trips]

json.dump(out, open('/root/travel/trips.json','w'), indent=1)
json.dump(changes, open('/root/travel/changes.json','w'), indent=1)
print(f"{len(out)} stays kept, {len(changes)} adjustments")
neg = [t for t in out if t['nights'] < 0]
print("negative-night rows (should be none):", neg)
