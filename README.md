# Where in the World is Nick

Four years of one Google Calendar, cleaned up and counted. Oct 1 2022 to Sep 1 2026.

**Live site:** https://mylifeindata.github.io/travel-book/

898 nights away, 533 at home in Wheaton, out of 1,431 days. 23 countries, 90 places
away from home, 120 separate stays.

## What's in here

| Path | What it is |
|---|---|
| `index.html` | The whole site. One self-contained file, no build step, no dependencies. |
| `data/travel-log.csv` | Every stay: dates, nights, place, country, region, and flags for home / side trip / inferred. |
| `data/travel-data.json` | The full payload the page reads, including the Sankey graph and map coordinates. |
| `data/adjustments.csv` | Every edit made to the raw calendar, with the reason. |
| `build/` | The scripts that turn raw calendar events into that payload. |

## The tabs

- **Overview** — headline numbers, pace by year, longest stays
- **The map** — world map with a leg drawn for every move, plus a date slider and playback
- **Rhythm** — one column per day, colored by where that night was spent
- **Flow** — Sankey from year to region to place, with the US broken out place by place
- **Countries** — nights away by country and by region
- **The log** — all 151 rows, home stretches included
- **Method** — every cleaning rule and every adjustment

## How the numbers work

Every one of the 1,431 days in the window belongs to exactly one stay, so "away" is a
real complement rather than "what happened to be logged". The rules, in order:

1. **Home is the default.** Chicago and Wheaton events are Home, and so is any day with
   nothing on the calendar.
2. **Nights, not days.** A stay is end date minus start date.
3. **Overlaps are trimmed, not merged.** Where one stay ran past the start of the next,
   the earlier one is cut back to the day the next began (48 times).
4. **Room changes are not new trips.** Consecutive events at the same place, and nested
   events at the same place, collapse into one stay.
5. **Side trips are nested.** A stay entirely inside a longer one is listed separately and
   its nights are subtracted from the surrounding stay (9 of them).
6. **Reminders are dropped.** Four events were notes to self, not stays.

Aggregates are all derived from one day-to-stay map rather than by summing rows, which is
what keeps the ribbon, the Sankey and the country bars from disagreeing.

**The number to distrust:** home nights are inferred. Any unlogged travel counts here as a
night in Wheaton, so 898 nights away is a floor, not a ceiling.

## Rebuilding after a calendar edit

```bash
# 1. Re-pull the calendar into build/raw_events.json (two API calls; the range is
#    too wide for one), then:
cd build
python3 clean.py     # markers, overlaps, nesting, consolidation -> trips.json
python3 stats.py     # day map, aggregates, Sankey, map coords -> data.js
node worldpath.js    # only if you want to regenerate the world outline
```

Then inline `data.js` into `index.html` in place of the existing `const WORLD = ... const DATA = ...`
block.

The world outline comes from [world-atlas](https://github.com/topojson/world-atlas)
(Natural Earth 110m), projected equirectangular and simplified at build time so the page
ships with zero runtime dependencies.

## Deploying

GitHub Pages, serving from the repo root on the default branch. No Jekyll, no Actions,
nothing to install.

---

Built with [Claude](https://claude.ai) from the "Travel" calendar.
