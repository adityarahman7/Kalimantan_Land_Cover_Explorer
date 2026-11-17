// Peta fase 4 R1. Tempel di Earth Engine Code Editor.
var batas = ee.FeatureCollection('projects/portofolio-513404/assets/batas_admin_gee');
var sumber = ee.Image(
  'projects/mapbiomas-public/assets/indonesia/lulc/collection4/' +
  'mapbiomas_indonesia_collection4_coverage_v2'
);
var kodeValid = [3, 5, 9, 13, 21, 24, 25, 30, 31, 33, 35, 40, 76];
var crs = 'EPSG:4326';
var grid = [
  0.0002694945852358564, 0, 93.51839400103549,
  0, -0.0002694945852358564, 7.2919844873118045
];
var region = ee.Geometry.Rectangle([108.59, -4.95, 119.04, 4.42], null, false);

function kelasValidAtauNol(tahun) {
  return sumber.select('classification_' + tahun)
    .remap(kodeValid, kodeValid, 0)
    .unmask(0, false)
    .toInt16();
}

var awal = kelasValidAtauNol(2010);
var akhir = kelasValidAtauNol(2024);
var bersama = awal.neq(0).and(akhir.neq(0));
var transisi = awal.multiply(100).add(akhir)
  .updateMask(bersama).clipToCollection(batas).rename('transition').toInt16();
// 0 stabil, 1 berubah, 2 tidak dapat dibandingkan.
var perubahan = ee.Image.constant(2)
  .where(bersama, awal.neq(akhir))
  .clipToCollection(batas).rename('change').toByte()
  .setDefaultProjection(crs, grid);

Map.setCenter(114, -0.5, 6);
Map.addLayer(perubahan, {
  min: 0, max: 2, palette: ['2b8c63', 'e1842f', '747b86']
}, 'Perubahan 2010–2024 (tinjauan)', true);

// Ubah kedua kode ini untuk memeriksa pasangan kelas lain.
var kodeAsal = 3;
var kodeTujuan = 35;
Map.addLayer(transisi.eq(kodeAsal * 100 + kodeTujuan).selfMask(),
  {palette: ['af3c8b']}, 'Transisi pilihan ' + kodeAsal + ' → ' + kodeTujuan, false);

// Tugas dibuat saat skrip dijalankan. Klik Run di Tasks jika perlu raster penuh.
// Statistik resmi memakai skrip analisis pada grid asli, bukan tampilan zoom peta.
Export.image.toDrive({
  image: perubahan.unmask(255, false),
  description: 'phase4_change_2010_2024_native',
  region: region,
  crs: crs,
  crsTransform: grid,
  maxPixels: 1e10,
  fileFormat: 'GeoTIFF',
  formatOptions: {cloudOptimized: true, noData: 255}
});
