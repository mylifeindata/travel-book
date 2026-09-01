const topo = require('world-atlas/countries-110m.json');
const { feature } = require('topojson-client');
const fs = require('fs');

const geo = feature(topo, topo.objects.countries);
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

let d = '', dropped = 0;
for (const f of geo.features) {
  const g = f.geometry; if (!g) continue;
  const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
  // drop Antarctica: every vertex below the bottom cut
  const lats = polys.flat(2).filter((_, i) => i % 2 === 1);
  const allLats = polys.flat(1).flat(1).map(p => p[1]);
  if (Math.max(...allLats) < LAT_BOT + 2) { dropped++; continue; }
  for (const poly of polys) for (const ring of poly) d += ringPath(ring);
}
fs.writeFileSync('world.txt', d);
console.log('path chars:', d.length, '| features dropped:', dropped);
