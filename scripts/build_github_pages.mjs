import {cp, mkdir, readFile, readdir, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {gunzipSync} from 'node:zlib';

const root = fileURLToPath(new URL('../', import.meta.url));
const web = path.join(root, 'web');
const out = path.join(root, '.pages-build');
const dataRoot = path.join(web, 'public/data/r2');
const manifest = JSON.parse(await readFile(path.join(dataRoot, 'manifest.json'), 'utf8'));
if (manifest.release !== 'R2' || manifest.years.length !== 15 || manifest.region_index.length !== 62) {
  throw new Error('Paket R2 belum lengkap.');
}
// Include only referenced display data, never local credentials or original rasters.
const referenced = new Set([
  ...Object.values(manifest.boundaries).map(item => item.path),
  ...Object.values(manifest.raster.year_paths),
  ...manifest.region_index.map(item => item.stats),
]);
await mkdir(out, {recursive: true});
for (const entry of await readdir(web, {withFileTypes: true})) {
  if (entry.isFile() && /\.(html|mjs|css)$/.test(entry.name)) {
    const content = await readFile(path.join(web, entry.name), 'utf8');
    await writeFile(path.join(out, entry.name), content.trimEnd() + '\n');
  }
}
await cp(path.join(web, 'public/context'), path.join(out, 'public/context'), {recursive: true});
let bytes = 0;
for (const relative of referenced) {
  const source = path.resolve(dataRoot, relative);
  if (!source.startsWith(dataRoot + path.sep)) throw new Error('Jalur di luar paket R2.');
  const buffer = await readFile(source);
  bytes += buffer.length;
  if (relative.endsWith('.gz')) {
    const pixels = gunzipSync(buffer);
    const [width, height] = manifest.raster.dimensions;
    if (pixels.length !== width * height) throw new Error(`Ukuran raster salah: ${relative}`);
    const codes = new Set([0, 255, ...manifest.class_order]);
    for (const value of pixels) if (!codes.has(value)) throw new Error(`Kode raster salah: ${relative}`);
  } else {
    const value = JSON.parse(buffer.toString('utf8'));
    const region = manifest.region_index.find(item => item.stats === relative);
    if (region && value.region_id !== region.region_id) throw new Error(`ID statistik salah: ${relative}`);
  }
  const target = path.join(out, 'public/data/r2', relative);
  await mkdir(path.dirname(target), {recursive: true});
  await writeFile(target, buffer);
}
await writeFile(path.join(out, 'public/data/r2/manifest.json'), JSON.stringify({...manifest,
  publication_status: 'Public exploratory dashboard; source-version, accuracy and boundary-distribution limitations remain documented in the data panel.',
}) + '\n');
await writeFile(path.join(out, '.nojekyll'), '');
await writeFile(path.join(out, 'SOURCE.md'),
  '# Kalimantan Land Cover Explorer\n\n' +
  'Dashboard R2: dibuat dari main dengan scripts/build_github_pages.mjs.\n\n' +
  'Kode: https://github.com/adityarahman7/Kalimantan_Land_Cover_Explorer\n\n' +
  'Tutupan lahan: MapBiomas Indonesia (CC-BY-SA menurut penyedia; versi aset dan akurasi belum terkonfirmasi). ' +
  'Batas: BIG, disederhanakan; kelengkapan dan ketentuan distribusi belum terverifikasi. ' +
  'Basemap: Natural Earth, public domain. Rincian sumber tersedia di panel Tentang data.\n');
console.log(JSON.stringify({output: out, dataFiles: referenced.size + 1, dataBytes: bytes,
  years: manifest.years.length, regions: manifest.region_index.length}));
