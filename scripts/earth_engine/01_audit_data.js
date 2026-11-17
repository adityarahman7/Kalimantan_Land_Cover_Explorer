// Audit awal fase 2 — 1 November 2026.
// Jalankan di Earth Engine Code Editor dengan akun yang memiliki akses aset.
// ID batas di bawah disusun dari project dan nama aset pada tangkapan layar
// pengguna: portofolio-513404 / batas_admin_gee. Belum diuji ulang oleh asisten.
// Keluaran asli CSV dan keterbatasan tercatat di docs/data_inventory.md.
// Menjalankan editor membuat tugas ekspor; ekspor baru berjalan setelah Run
// pada Tasks. Jangan menimpa arsip hasil lama tanpa mencatat run baru.
var boundaryAssetId = 'projects/portofolio-513404/assets/batas_admin_gee';
var batasAdmin = ee.FeatureCollection(boundaryAssetId);

var assetId =
  'projects/mapbiomas-public/assets/indonesia/lulc/collection4/' +
  'mapbiomas_indonesia_collection4_coverage_v2';

var landCover = ee.Image(assetId);

print('Metadata citra', landCover);
print('Daftar band', landCover.bandNames());

var lc2010 = landCover.select('classification_2010');
var lc2024 = landCover.select('classification_2024');

print('Proyeksi 2010', lc2010.projection());
print('Proyeksi 2024', lc2024.projection());
print('Skala nominal 2010 (m)',
      lc2010.projection().nominalScale());
print('Skala nominal 2024 (m)',
      lc2024.projection().nominalScale());
      
print('Jumlah fitur batas', batasAdmin.size());
print('Contoh atribut', batasAdmin.first());

print(
  'Daftar provinsi',
  batasAdmin.aggregate_array('WADMPR').distinct().sort()
);

// Kotak yang mencakup extent batas yang kamu laporkan.
var kotakKajian = ee.Geometry.Rectangle(
  [108.59, -4.95, 119.04, 4.42], null, false
);

var citraAudit = landCover
  .select(['classification_2010', 'classification_2024'])
  .unmask(-9999, false)
  .clipToCollection(batasAdmin);

var sampelKelas = citraAudit.sample({
  region: kotakKajian,
  scale: 30,
  numPixels: 1000,
  seed: 42,
  tileScale: 4,
  geometries: false
});

print('Jumlah sampel audit', sampelKelas.size());

print('Kode kelas 2010',
      sampelKelas.aggregate_histogram('classification_2010'));

print('Kode kelas 2024',
      sampelKelas.aggregate_histogram('classification_2024'));
      
Map.setCenter(114, -0.5, 6);

var sawit2010 = lc2010.eq(35)
  .selfMask()
  .clipToCollection(batasAdmin);

var sawit2024 = lc2024.eq(35)
  .selfMask()
  .clipToCollection(batasAdmin);

Map.addLayer(
  sawit2010, {palette: ['9065d0']}, 'Sawit 2010', false
);

Map.addLayer(
  sawit2024, {palette: ['9065d0']}, 'Sawit 2024', true
);

print('Properti aset MapBiomas', landCover.toDictionary());

// 1. Kode kelas yang dihitung sebagai valid.
var kodeValid = [
  3, 5, 9, 13, 21, 24, 25,
  30, 31, 33, 35, 40, 76
];

var penandaValid = ee.List.repeat(1, kodeValid.length);

// 2. Ubah kelas menjadi penanda: valid = 1, lainnya = 0.
var valid2010 = lc2010
  .remap(kodeValid, penandaValid, 0)
  .unmask(0, false);

var valid2024 = lc2024
  .remap(kodeValid, penandaValid, 0)
  .unmask(0, false);

// 3. Luas piksel dalam hektare.
var luasHa = ee.Image.pixelArea().divide(10000);

var citraLuas = ee.Image.cat([
  luasHa.rename('wilayah_ha'),
  luasHa.multiply(valid2010).rename('valid_2010_ha'),
  luasHa.multiply(valid2024).rename('valid_2024_ha'),
  luasHa.multiply(valid2010.and(valid2024))
    .rename('valid_bersama_ha')
]).clipToCollection(batasAdmin);

// 4. Jumlahkan luas pada grid asli band 2010.
var ringkasanLuas = citraLuas.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: kotakKajian,
  crs: 'EPSG:4326',
  crsTransform: [
    0.0002694945852358564,
    0,
    93.51839400103549,
    0,
    -0.0002694945852358564,
    7.2919844873118045
  ],
  maxPixels: 1e10,
  tileScale: 4
});

// 5. Buat tugas ekspor CSV.
Export.table.toDrive({
  collection: ee.FeatureCollection([
    ee.Feature(null, ringkasanLuas)
  ]),
  description: 'audit_cakupan_valid_2010_2024',
  fileNamePrefix: 'audit_cakupan_valid_2010_2024',
  fileFormat: 'CSV',
  selectors: [
    'wilayah_ha',
    'valid_2010_ha',
    'valid_2024_ha',
    'valid_bersama_ha'
  ]
});

var tidakDapatDibandingkan = valid2010
  .and(valid2024)
  .not()
  .selfMask()
  .clipToCollection(batasAdmin);

Map.addLayer(
  tidakDapatDibandingkan,
  {palette: ['ff0000']},
  'Area tidak dapat dibandingkan'
);

var contohTidakValid = tidakDapatDibandingkan
  .rename('invalid')
  .toByte()
  .addBands(ee.Image.pixelLonLat())
  .stratifiedSample({
    numPoints: 3,
    classBand: 'invalid',
    region: kotakKajian,
    projection: lc2010.projection(),
    seed: 42,
    tileScale: 4,
    geometries: false
  });

Export.table.toDrive({
  collection: contohTidakValid,
  description: 'contoh_lokasi_tidak_valid',
  fileFormat: 'CSV',
  selectors: ['longitude', 'latitude']
});

var titikAudit = ee.Geometry.Point([
  114.7288306, 1.834314894
]);

Map.centerObject(titikAudit, 15);
Map.addLayer(titikAudit, {color: 'yellow'}, 'Titik audit');

var nilaiTitik = landCover
  .select(['classification_2010', 'classification_2024'])
  .unmask(-9999, false)
  .reduceRegion({
    reducer: ee.Reducer.first(),
    geometry: titikAudit,
    crs: lc2010.projection(),
    maxPixels: 10
  });

print('Nilai kelas di titik audit', nilaiTitik);

var titikSawit = ee.Geometry.Point([
  116.11180945083655, -2.0012525891793755
]);

var areaReferensi = titikSawit.buffer(2000);

var s2Referensi = ee.ImageCollection(
    'COPERNICUS/S2_SR_HARMONIZED'
  )
  .filterBounds(areaReferensi)
  .filterDate('2024-01-01', '2025-01-01')
  .map(function(image) {
    var scl = image.select('SCL');

    // Pertahankan kelas gelap, vegetasi, tanah terbuka, dan air.
    var maskReferensi = scl.remap(
      [2, 4, 5, 6], [1, 1, 1, 1], 0
    );

    return image
      .updateMask(maskReferensi)
      .select(['B4', 'B3', 'B2'])
      .divide(10000);
  });

var rgb2024 = s2Referensi.median().clip(areaReferensi);

Map.centerObject(titikSawit, 16);

Map.addLayer(
  rgb2024,
  {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 0.2,
  gamma: 1.3
  },
  'Referensi Sentinel-2 median 2024'
);

Map.addLayer(titikSawit, {color: 'yellow'}, 'Titik sawit');
