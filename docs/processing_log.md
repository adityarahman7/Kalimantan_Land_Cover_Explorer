# Log pengolahan

## 2026-11-11 — Penggabungan QGIS dan paket fase 5 R1

- Gabungkan proyek utama dengan snapshot fase 3 dan 4 melalui PyQGIS lokal saat sesi MCP tidak merespons. Pertahankan layer asli, salin layer unik, tautkan tiga CSV, dan arsipkan dua proyek fase lama setelah verifikasi buka ulang.
- Unduh 30 ubin pasangan kelas untuk tinjauan sekitar 300 m. Paketkan COG, tiga batas tampilan dan 62 statistik wilayah. Periksa bahwa dekode perubahan cocok dengan raster tinjauan fase 4 pada semua piksel.
- Uji paket lewat HTTP loopback. Semua 67 berkas termuat. Pemuatan awal 2.747.396 byte tercatat 72,2 ms dalam satu uji lokal. Pembukaan ulang proyek utama mengonfirmasi 19 layer dan tabel.
- [Panduan fase 5](phase5_data_service.md) mencatat kontrak data, langkah regenerasi dan batas publikasi.
- Fase 6 menghubungkan data tersebut ke WebGIS lokal. Kesetaraan raster gzip terhadap COG dan interaksi inti di Edge telah diuji. Lihat [panduan dan hasil uji](../web/README.md).

## 2026-11-11 — Analisis fase 4 R1

- Reduksi Earth Engine memakai grid asli EPSG:4326, luas piksel dalam ha dan pasangan kode kelas 2010 → 2024. Cakupan AOI dihitung langsung dan cakupan provinsi diturunkan dari 56 kabupaten/kota.
- Ketiga CSV diperiksa ulang untuk 62 wilayah. Luas kelas tahunan cocok dengan luas valid tiap tahun. Matriks transisi cocok dengan valid bersama dan diagonal cocok dengan luas stabil.
- Luas berubah AOI 10.474.804,21 ha atau 19,606065% valid bersama. Selisih AOI terhadap fase 2 di bawah 0,01 ha untuk keempat ukuran. Luas agregat kabupaten/kota 6.839,51 ha di atas AOI langsung.
- Unduh satu raster tinjauan mencapai batas memori Earth Engine. Unduh 30 ubin lebih kecil berhasil. GDAL menyusun mosaik dan memeriksa neraca jumlah piksel. PyQGIS lokal membuka ulang proyek dengan empat layer setelah sesi MCP tidak merespons.
- [Analisis dan berkas fase 4](phase4_analysis.md) mencatat hasil, skema serta keterbatasan untuk fase 5.

## 2026-11-10 — Paket spasial fase 3

- Input adalah SHP 56 fitur dari fase 2, geodatabase BIG yang terbuka di QGIS, aset batas GEE dan MapBiomas.
- QGIS MCP memeriksa geometri SHP, menyusun skema ID teks, membentuk dissolve provinsi/AOI, menulis GeoPackage dan membuka ulang 56/5/1 fitur valid.
- Aset GEE diverifikasi langsung. Lima provinsi dan 56 kode kabupaten/kota cocok dengan GeoPackage. Metadata semua 15 band 2010–2024 sesuai grid acuan.
- Dua jendela QA 128 × 128 diunduh pada grid asli. QGIS membuka ulang keduanya, dan array menunjukkan konsistensi mask tahunan, mask bersama serta kode kelas. Proyek fase 3 dibuka ulang dengan tiga layer batas dan dua cuplikan QA.
- [Panduan fase 3](phase3_handoff.md) memuat input, metode, hasil dan keterbatasan. Statistik luas dan transisi menjadi pekerjaan fase 4.

Audit awal raster telah dijalankan pengguna di Earth Engine pada 1 November 2026. Entri berikut disusun dari keluaran yang dilaporkan, tangkapan layar, dan berkas hasil tersimpan. Saat merapikan log, asisten membaca ulang CSV dan skrip; tidak menjalankan ulang analisis cloud atau konversi batas.

## 2026-11-01 — Penyiapan dan audit batas

- **Input:** unduhan BIG `BATASWILAYAH_KABKOTA_20260601.gdb`, menurut pengguna berasal dari Ina-Geoportal pada 1 November 2026. GDB sumber lokal belum diverifikasi.
- **Proses oleh pengguna:** memilih wilayah Kalimantan, menyederhanakan atribut, memeriksa lima provinsi, kode kosong/berulang dan validitas GEOS. Satu fitur pulau kecil dengan atribut tidak jelas dihapus sehingga 57 menjadi 56 fitur.
- **Penanganan format:** ekspor SHP awal hanya menulis 53 fitur akibat MultiSurface. Setelah segmentasi, 55 fitur; masih tidak lengkap. GDAL `CONVERT_TO_LINEAR` + `PROMOTE_TO_MULTI` menghasilkan GPKG MultiPolygonZ 56 fitur menurut metadata pengguna, kemudian SHP diekspor dan diunggah.
- **Output:** GPKG kerja di raw, GPKG linear dan SHP/ZIP di interim, aset GEE bernama `batas_admin_gee` pada project yang terlihat sebagai `portofolio-513404`.
- **Pemeriksaan yang dilaporkan:** lima provinsi tanpa nama kosong; seleksi kode bermasalah 0; GEOS sebelum konversi valid; jumlah dan atribut unggahan sesuai 56 fitur.
- **Keterbatasan:** tidak ada pemeriksaan ulang geometri pascakonversi dalam pekerjaan dokumentasi ini; kelengkapan wilayah, overlap/gap, identitas fitur dihapus dan izin distribusi BIG belum dipastikan. Berkas raw saat ini sudah dimodifikasi pengguna.

## 2026-11-01 — Metadata dan sampling MapBiomas

- **Input:** `projects/mapbiomas-public/assets/indonesia/lulc/collection4/mapbiomas_indonesia_collection4_coverage_v2`, aset batas, legenda resmi.
- **Skrip:** [01_audit_data.js](../scripts/earth_engine/01_audit_data.js), belum memiliki revisi commit.
- **Proses:** membaca properti/band/proyeksi/skala, memilih 2010/2024, mengambil sampel dan menghitung histogram.
- **Parameter:** EPSG:4326; transformasi identik kedua band sebagaimana inventaris; target 1.000 sampel, skala 30 m, seed 42, tileScale 4. `unmask(-9999, false)` diikuti clip ke koleksi digunakan untuk membedakan mask dari kode kelas.
- **Output yang dilaporkan pengguna:** 35 band 1990–2024; metadata `v2`/annual; nominal ~30 m; 455 sampel; 12 kode pada 2010 dan 13 pada 2024. Setelah penandaan mask, tidak muncul -9999 atau 27 dalam sampel tersebut.
- **Galat dan penanganan:** percobaan awal memakai `batasAdmin.geometry()` mengalami user memory limit; diganti clipToCollection, region kotak sederhana dan tileScale 4.
- **Keterbatasan:** keluaran Console mentah sampling belum diarsipkan terpisah; ringkasan bersumber dari percakapan. Tidak ada klaim inventaris kelas menyeluruh, cakupan 100% atau akurasi dari sampel.

## 2026-11-01 — Luas cakupan kelas valid

- **Input:** dua band target dan batas kerja 56 fitur.
- **Proses:** kode legenda yang dikenali diberi 1; kode lain dan mask diberi 0. Hitung luas wilayah, valid tiap tahun dan valid bersama pada grid acuan; ekspor satu baris CSV melalui Tasks ke Drive.
- **Parameter:** valid `[3,5,9,13,21,24,25,30,31,33,35,40,76]`; luas pixelArea/10000; EPSG:4326; transform `[0.0002694945852358564,0,93.51839400103549,0,-0.0002694945852358564,7.2919844873118045]`; region `[108.59,-4.95,119.04,4.42]`; tileScale 4; maxPixels 1e10.
- **Galat dan penanganan:** `projection().transform()` mengembalikan string yang ditolak oleh crsTransform; diganti daftar enam angka hasil metadata, lalu tugas ekspor baru berhasil.
- **Output:** [audit_cakupan_valid_2010_2024.csv](../data/metadata/audit_cakupan_valid_2010_2024.csv).
- **Hasil dibaca ulang dari CSV:** wilayah 53.435.434,03534286 ha; valid 2010 53.426.361,23797169 ha; valid 2024 53.426.510,20063842 ha; valid bersama 53.426.346,61365083 ha.
- **Pemeriksaan lokal:** 0 ≤ valid bersama ≤ masing-masing valid tahunan ≤ wilayah; persentase masing-masing 99,9830210093%, 99,9832997806%, 99,9829936411%; selisih wilayah–valid bersama 9.087,42169203 ha.
- **Keterbatasan:** luas cakupan bukan luas per kelas/akurasi; seluruh angka mengikuti batas yang satu fiturnya dihapus. Penyebab invalid belum dipisahkan menyeluruh menjadi mask/27/kode tak dikenal.

## 2026-11-01 — Lokasi termask dan referensi visual

- **Proses:** stratifiedSample pada area tidak dapat dibandingkan, numPoints 3, seed 42, proyeksi band 2010, tileScale 4; ekspor koordinat. Periksa nilai piksel pada tiap titik dengan penanda mask -9999.
- **Output:** [contoh_lokasi_tidak_valid.csv](../data/metadata/contoh_lokasi_tidak_valid.csv), berisi tiga baris koordinat. Menurut pengguna, ketiganya termask pada dua tahun dan berada sekitar perbatasan Indonesia–Malaysia. CSV tidak menyimpan hasil nilai kelas; hasil pemeriksaan dicatat pada inventaris.
- **Referensi visual:** titik 116.11180945083655, -2.0012525891793755; buffer 2 km; `COPERNICUS/S2_SR_HARMONIZED`, 2024-01-01 sampai sebelum 2025-01-01; pertahankan SCL 2,4,5,6, median RGB B4/B3/B2 dibagi 10000; tampilan min 0, max 0.2, gamma 1.3.
- **Pengamatan:** jalan dan blok vegetasi konsisten dengan perkebunan; jenis tanaman belum terkonfirmasi independen. Pemeriksaan visual berbasis tangkapan layar yang dibagikan pengguna.
- **Keterbatasan:** tiga titik bukan penjelasan seluruh invalid; satu lokasi perkebunan bukan sampel acak atau penilaian akurasi; komposit mencampurkan tanggal; tahun 2010 belum dibandingkan dengan citra referensi.

## 2026-11-01 — Penyelarasan arsip oleh asisten

- **Input:** empat berkas audit pengguna, hasil percakapan dan tangkapan layar.
- **Proses:** melengkapi deklarasi aset batas dari project/nama yang terlihat pada tangkapan layar, menyelaraskan status/checklist, menambahkan provenance/lisensi, dan memperbarui log/status/roadmap serta ringkasan pendukung.
- **Output:** skrip lokal dengan deklarasi batas, inventaris konsisten, log ini dan status yang mengakui hasil audit awal serta pertanyaan terbuka.
- **Batas verifikasi:** deklarasi baru `projects/portofolio-513404/assets/batas_admin_gee` belum dieksekusi ulang oleh asisten. Pemeriksaan lokal meliputi sintaks JavaScript, format konfigurasi, konsistensi CSV dan tautan; bukan pengujian akses akun cloud.
- **Selanjutnya:** fase 3 secara bertahap bersama pengguna; tinjau batas dan rancangan produk siap analisis sebelum analisis produksi.

## Format entri

- Tanggal:
- Tujuan:
- Input dan versi:
- Skrip/notebook dan revisi kode:
- Parameter (CRS, grid, mask, metode luas):
- Output:
- Pemeriksaan dan hasil:
- Keterbatasan/galat:
- Langkah berikutnya:

## R2 — 17 November 2026

Audit, analisis native-grid, pengemasan, integrasi grafik dan validasi lokal selesai. [Laporan R2](r2_execution.md) mencatat checkpoint 20–100%, koreksi dua reduksi awal, strategi 15 raster tahunan, dan hasil pengujian data serta browser.
