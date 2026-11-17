export async function loadR2(manifestUrl) {
  const location = new URL(manifestUrl, globalThis.location?.href);
  async function json(path) {
    const response = await fetch(new URL(path, location));
    if (!response.ok) throw new Error(`Data R2 gagal dimuat (HTTP ${response.status}).`);
    return response.json();
  }
  const manifest = await json(location);
  if (manifest.schema_version !== 1 || manifest.release !== "R2" || manifest.years.length !== 15) {
    throw new Error("Kontrak manifest R2 tidak didukung.");
  }
  const index = new Map(manifest.region_index.map(region => [region.region_id, region]));
  const cache = new Map();
  const validCodes = new Set([0, 255, ...manifest.class_order]);
  async function getYear(year) {
    if (!Object.hasOwn(manifest.raster.year_paths, year)) throw new RangeError("Tahun tidak tersedia.");
    if (cache.has(year)) return cache.get(year);
    const response = await fetch(new URL(manifest.raster.year_paths[year], location));
    if (!response.ok) throw new Error(`Peta ${year} gagal dimuat (HTTP ${response.status}).`);
    const stream = response.body.pipeThrough(new DecompressionStream("gzip"));
    const values = new Uint8Array(await new Response(stream).arrayBuffer());
    const [width, height] = manifest.raster.dimensions;
    if (values.length !== width * height) throw new Error("Ukuran raster tahunan salah.");
    for (const value of values) {
      if (!validCodes.has(value)) throw new Error("Kode raster tahunan tidak dikenal.");
    }
    cache.set(year, values);
    while (cache.size > 4) cache.delete(cache.keys().next().value);
    return values;
  }
  return {
    manifest,
    async getStats(regionId) {
      const region = index.get(regionId);
      if (!region) throw new RangeError("Wilayah tidak tersedia.");
      const stats = await json(region.stats);
      if (stats.region_id !== regionId) throw new Error("ID statistik berbeda dari manifest.");
      return stats;
    },
    async getBoundaries(level) {
      if (!Object.hasOwn(manifest.boundaries, level)) throw new RangeError("Tingkat wilayah tidak tersedia.");
      return json(manifest.boundaries[level].path);
    },
    async getRasterPair(before, after) {
      if (before > after) throw new RangeError("Tahun awal harus lebih kecil dari tahun akhir.");
      const a = await getYear(before);
      const b = before === after ? a : await getYear(after);
      const values = new DataView(new ArrayBuffer(a.length * 2));
      for (let i = 0; i < a.length; i++) {
        if ((a[i] === 255) !== (b[i] === 255)) throw new Error("Cakupan raster tahunan berbeda.");
        values.setUint16(i * 2, a[i] === 255 ? 65535 : 100 * a[i] + b[i], true);
      }
      return values;
    },
  };
}
