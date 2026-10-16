const topo = require('world-atlas/countries-110m.json');
const { feature } = require('topojson-client');
const fs = require('fs');

const geo = feature(topo, topo.objects.countries);

/* ---------------------------------------------------------------------------
   Two outputs from one source.

   world.txt  - the flat map: equirectangular, projected and simplified here so
                the page ships no projection code for it.
   globe.txt  - the globe: raw lat/lon rings, because an orthographic globe has
                to reproject every vertex on every drag frame. Stored as
                tenths of a degree, delta encoded, so the payload stays small.
--------------------------------------------------------------------------- */

const LAT_TOP = 84, LAT_BOT = -56;
const W = 1000, H = 500;
const px = lon => (lon + 180) / 360 * W;
const py = lat => (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * H;
const r = n => Math.round(n * 10) / 10;
const DEC = 1.2;

function ringPath(ring){
  // Split the ring wherever it jumps the antimeridian, so no polygon smears
  // a horizontal line across the whole map.
  const segs = [[]];
  let prevLon = null;
  for (const [lon, lat] of ring) {
    if (prevLon !== null && Math.abs(lon - prevLon) > 180) segs.push([]);
    segs[segs.length - 1].push([lon, Math.max(LAT_BOT, Math.min(LAT_TOP, lat))]);
    prevLon = lon;
  }
  let out = '';
  for (const seg of segs) {
    let prev = null, kept = 0, s = '';
    for (const [lon, lat] of seg) {
      const x = r(px(lon)), y = r(py(lat));
      if (prev && Math.abs(x - prev[0]) < DEC && Math.abs(y - prev[1]) < DEC) continue;
      s += (kept === 0 ? 'M' : 'L') + x + ',' + y;
      prev = [x, y]; kept++;
    }
    if (kept > 2) out += s + 'Z';
  }
  return out;
}

/* --- flat ---------------------------------------------------------------- */

let d = '', dropped = 0;
const keep = [];
for (const f of geo.features) {
  const g = f.geometry; if (!g) continue;
  const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
  keep.push(polys);
  const allLats = polys.flat(1).flat(1).map(p => p[1]);
  // Antarctica is dropped from the FLAT map only: every vertex sits below its
  // bottom cut. The globe keeps it, because there the south pole is somewhere
  // you can actually turn to.
  if (Math.max(...allLats) < LAT_BOT + 2) { dropped++; continue; }
  for (const poly of polys) for (const ring of poly) d += ringPath(ring);
}
fs.writeFileSync('world.txt', d);

/* --- globe --------------------------------------------------------------- */

// Angular decimation. On a 420px globe one degree is a bit over 2px at the
// centre, so 0.9 degrees keeps coastlines smooth without carrying every vertex.
const GDEC = 0.9;

// No antimeridian split here: on a sphere 179E and 179W are neighbours, and the
// renderer clips against the horizon rather than against a map edge.
function ringLL(ring){
  const out = [];
  let prev = null;
  for (const [lon, lat] of ring) {
    const la = Math.round(lat * 10) / 10, lo = Math.round(lon * 10) / 10;
    if (prev) {
      const dlon = Math.abs(lo - prev[1]) * Math.cos(la * Math.PI / 180);
      if (Math.abs(la - prev[0]) < GDEC && dlon < GDEC) continue;
    }
    out.push([la, lo]);
    prev = [la, lo];
  }
  return out;
}

// Delta encoded in tenths of a degree against the previous vertex, then written
// in base 36 with a sign prefix. Rings separated by ";", the first vertex of
// each ring absolute.
const b36 = n => (n < 0 ? '-' : '') + Math.abs(n).toString(36);
const rings = [];
let verts = 0;
for (const polys of keep) {
  for (const poly of polys) for (const ring of poly) {
    const ll = ringLL(ring);
    if (ll.length < 4) continue;
    verts += ll.length;
    let s = '', pla = 0, plo = 0;
    ll.forEach(([la, lo], i) => {
      const ila = Math.round(la * 10), ilo = Math.round(lo * 10);
      s += (i ? ',' : '') + b36(ila - pla) + '_' + b36(ilo - plo);
      pla = ila; plo = ilo;
    });
    rings.push(s);
  }
}
const gtxt = rings.join(';');
fs.writeFileSync('globe.txt', gtxt);

console.log('flat path chars:', d.length, '| features dropped:', dropped);
console.log('globe rings:', rings.length, '| vertices:', verts, '| chars:', gtxt.length);
