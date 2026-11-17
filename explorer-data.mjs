import {loadR1} from "./r1-data.mjs";
import {loadR2} from "./r2-data.mjs";
import {loadPairs} from "./raster-map.mjs";

// Only fall back when R2 is absent. A malformed published R2 must show an error.
export async function loadExplorer() {
  const r2Url = new URL("./public/data/r2/manifest.json", import.meta.url);
  const response = await fetch(r2Url);
  if (response.ok) return loadR2(r2Url);
  if (response.status !== 404) throw new Error(`Manifest R2 gagal dimuat (${response.status}).`);
  const url = new URL("./public/data/r1/manifest.json", import.meta.url);
  const source = await loadR1(url);
  let original;
  return {
    manifest: source.manifest,
    getBoundaries: source.getBoundaries,
    async getStats(id) {
      const stats = await source.getStats(id);
      return {...stats,
        annual_valid_ha: Object.fromEntries(source.manifest.years.map(year => [year, stats.summary[`valid_${year}_ha`]])),
        pairs: {"2010_2024": {summary: stats.summary, transition_area_ha: stats.transition_area_ha}},
      };
    },
    async getRasterPair(before, after) {
      if (![before, after].every(year => source.manifest.years.includes(year)) || before > after) {
        throw new RangeError("Pasangan tahun R1 tidak tersedia.");
      }
      original ??= await loadPairs(new URL("class_pair_2010_2024.u16.gz", url), source.manifest.raster);
      if (before !== after) return original;
      const pair = new DataView(new ArrayBuffer(original.byteLength));
      for (let i = 0; i < original.byteLength; i += 2) {
        const value = original.getUint16(i, true);
        const code = before === 2010 ? Math.floor(value / 100) : value % 100;
        pair.setUint16(i, value === 65535 ? value : code * 101, true);
      }
      return pair;
    },
  };
}
