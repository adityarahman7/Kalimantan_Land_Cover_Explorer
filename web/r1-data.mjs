// Data access for the R1 WebGIS. Pass the deployed or local manifest URL.
export async function loadR1(manifestUrl) {
  const manifestLocation = new URL(manifestUrl, globalThis.location?.href);

  async function fetchFile(path) {
    const url = new URL(path, manifestLocation);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Gagal memuat ${url.pathname} (HTTP ${response.status}).`);
    }
    return response;
  }

  const manifest = await (await fetchFile(manifestLocation)).json();
  if (manifest.schema_version !== 1 || manifest.release !== "R1") {
    throw new Error("Versi manifest data R1 tidak didukung.");
  }
  const regions = new Map(manifest.region_index.map(region => [region.region_id, region]));
  const valid = new Set(manifest.class_order);
  const {nodata_outside_aoi: nodata, invalid_class: invalid} = manifest.raster;

  return {
    manifest,

    async getStats(regionId) {
      const entry = regions.get(regionId);
      if (!entry) throw new RangeError(`Wilayah tidak tersedia: ${regionId}`);
      const stats = await (await fetchFile(entry.stats)).json();
      if (stats.region_id !== regionId) throw new Error("ID statistik dan manifest berbeda.");
      return stats;
    },

    async getBoundaries(level) {
      if (!Object.hasOwn(manifest.boundaries, level)) {
        throw new RangeError(`Tingkat batas tidak tersedia: ${level}`);
      }
      return (await fetchFile(manifest.boundaries[level].path)).json();
    },

    rasterUrl: new URL(manifest.raster.path, manifestLocation).href,

    decodePair(value) {
      if (value === nodata) return null;
      const before = Math.floor(value / 100);
      const after = value % 100;
      if (!Number.isInteger(value) || (before !== invalid && !valid.has(before))
          || (after !== invalid && !valid.has(after))) {
        throw new RangeError(`Kode raster tidak dikenal: ${value}`);
      }
      return {
        class2010: before === invalid ? null : before,
        class2024: after === invalid ? null : after,
        change: before === invalid || after === invalid ? 2 : Number(before !== after),
      };
    },
  };
}
