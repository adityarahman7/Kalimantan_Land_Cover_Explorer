# Penyiapan spasial untuk analisis fase 4

Paket kerja R1 disiapkan dan diperiksa pada 10 November 2026. Analisis pilot memakai 2010 dan 2024. Kelima belas band tahunan 2010–2024 telah diperiksa kesamaan CRS dan transformasinya untuk perluasan berikutnya.

## Input → proses → output

| Input | Proses | Output |
| --- | --- | --- |
| SHP batas kerja yang sebelumnya diunggah ke Earth Engine | Baca dan validasi di QGIS MCP, buat kode teks yang stabil, dissolve menurut provinsi lalu seluruh AOI | `data/processed/phase3_boundaries.gpkg` pada grup fase 3 di proyek QGIS utama |
| Aset MapBiomas dan batas kerja GEE | Verifikasi akses, kode kabupaten/kota dan grid 15 band, lalu bentuk raster dan mask sebagai objek Earth Engine | Fungsi `prepare()` pada `scripts/prepare_phase3_rasters.py` |
| Raster dan mask pilot | Unduh dua jendela 128 × 128 pada grid asli, buka ulang di QGIS, bandingkan nilai kelas dan mask piksel | Dua GeoTIFF QA di `data/processed/phase3_qa/` dan laporan `data/metadata/phase3_raster_qa.json` |

## Paket batas

| Layer | Fitur valid | Atribut analisis |
| --- | ---: | --- |
| `kabupaten_kota` | 56 | `district_id`, `district_name`, `province_id`, `province_name` |
| `provinsi` | 5 | `province_id`, `province_name` |
| `aoi` | 1 | `aoi_id = KALIMANTAN_ID`, `aoi_name = Kalimantan Indonesia` |

QGIS berhasil membuka ulang ketiga layer dalam EPSG:4326. Kode kabupaten/kota unik dan seluruh 56 kode cocok dengan aset Earth Engine. Jumlah fitur menurut kode provinsi adalah 61 → 14, 62 → 14, 63 → 13, 64 → 10 dan 65 → 5. Diagnostik overlap memakai selisih jumlah luas planar komponen terhadap luas hasil dissolve. Selisih terbesar dalam provinsi sekitar 5,52 × 10⁻¹³ derajat² dan selisih antarprovinsi nol pada perhitungan tersebut. Pemeriksaan ini tidak mengukur kelengkapan cakupan terhadap batas independen. Rinciannya ada di [laporan batas](../data/metadata/phase3_boundary_qa.json).

Seluruh kode kabupaten/kota di geodatabase sumber untuk lima provinsi ditemukan pada batas kerja. Sumber juga memuat satu fitur tambahan Kalimantan Timur dengan `OBJECTID=1210`, geometri tidak kosong dan `KDPKAB` serta `WADMKK` kosong setelah pemangkasan spasi. Luasnya sekitar 44,33 ha menurut pengukuran elipsoid WGS84 atas geometri sumber. Angka itu adalah luas fitur sumber, belum merupakan luas tambahan di luar AOI kerja. Fitur tanpa kode tersebut tetap di luar paket pilot sebagaimana batas kerja fase 2. Cakupan final dan ketentuan distribusi BIG masih perlu ditetapkan sebelum rilis.

## Kontrak raster dan mask

- Raster utama berasal dari aset `collection4/...coverage_v2`. Identitas produk sebagai Koleksi 4.1 dan angka akurasi yang sesuai masih belum terkonfirmasi.
- Seluruh band `classification_2010` sampai `classification_2024` memiliki CRS EPSG:4326 dan transformasi yang cocok dengan konfigurasi audit. Saat menjalankan reduksi, gunakan `crs` dan `crsTransform` dari konfigurasi. Pertahankan grid ini dan gunakan `pixelArea() / 10000` untuk hektare.
- Fungsi `prepare()` mengembalikan batas kabupaten/kota GEE, kamus raster kelas per tahun, kamus mask valid tahunan, mask valid bersama, dan mask AOI. Kode wilayah pada aset GEE tetap `KDPKAB` dan `KDPPUM`, padanannya di GeoPackage adalah `district_id` dan `province_id`.
- Dalam AOI, mask tahunan bernilai 1 untuk 13 kode yang diizinkan dan 0 untuk piksel termask atau kode di luar daftar, termasuk 27. Mask valid bersama adalah irisan mask dari tahun yang diminta. Untuk transisi satu pasangan, panggil fungsi dengan dua tahun pasangan tersebut. Di luar AOI, piksel termask.
- Untuk luas per kelas tahunan, gunakan mask tahun itu. Untuk transisi, gunakan mask valid bersama. Laporkan area tidak dapat dibandingkan secara terpisah dan gunakan valid bersama sebagai penyebut proporsi perubahan.
- Nilai 255 dipakai sebagai NoData **pada kedua GeoTIFF QA lokal**. Urutan band adalah `class_2010`, `class_2024`, `valid_2010`, `valid_2024`, `valid_common`, `in_aoi`.

Kedua GeoTIFF berhasil dibuka ulang di QGIS. Pemeriksaan array memastikan mask bersama adalah irisan kedua mask tahunan dan piksel kelas sesuai mask. Pusat cuplikan sawit bernilai 35 pada kedua tahun, dengan mask bersama 1. Pusat cuplikan perbatasan berada di dalam AOI, dengan mask bersama 0 dan kelas disimpan sebagai NoData. Hasil ini memeriksa perilaku piksel pada dua jendela. Cakupan seluruh wilayah tetap merujuk ekspor fase 2 yang sudah tersimpan, dengan valid bersama 99,982994% pada batas kerja.

## Cara melanjutkan ke fase 4

1. Buka [proyek QGIS utama](../Kalimantan_Land_Cover_Explorer.qgz) untuk meninjau batas. Aktifkan cuplikan QA pada grup fase 3 saat ingin memeriksa mask.
2. Gunakan `scripts/prepare_phase3_rasters.py` dari lingkungan Python dengan `earthengine-api` dan kredensial Earth Engine yang dapat membaca aset. Pustaka yang dipakai dalam pemeriksaan ini adalah `earthengine-api==1.7.52`.
3. Jalankan contoh berikut dari akar proyek setelah autentikasi tersedia.

```python
import ee
from scripts.prepare_phase3_rasters import PROJECT, prepare

ee.Initialize(project=PROJECT)
boundary, classes, valid, common, aoi = prepare((2010, 2024))
kelas_2010 = classes[2010].updateMask(common)
kelas_2024 = classes[2024].updateMask(common)
```

Raster cakupan penuh diproses sebagai objek Earth Engine dari aset sumber. GeoTIFF lokal hanya mencakup dua jendela QA. Fase 4 dapat langsung memakai fungsi di atas untuk luas per kelas, matriks transisi dan peta perubahan. Tabel hasil fase 4 perlu direkonsiliasi terhadap cakupan valid fase 2 pada grid dan batas yang sama.
