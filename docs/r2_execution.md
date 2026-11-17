# Pelaksanaan R2

Pekerjaan dimulai 17 November 2026 dan meneruskan aplikasi lokal R1. Target mengikuti [7 fase dan 22 tahap](r2_plan.md).

| Checkpoint | Hasil yang telah diperiksa |
| --- | --- |
| 20% | Akses aset, grid 15 band, dan 56 kode kabupaten/kota diverifikasi. Unduhan raster 15 tahun lengkap pada 30 ubin. |
| 40% | Seluruh raster tahunan lolos pemeriksaan kode, grid, dan mask luar AOI. Kedua raster ujung identik dengan R1. Analisis terhadap 2010 tersedia untuk seluruh tahun. Sampel diagnostik 1.200 lokasi tidak menunjukkan kode tambahan di luar aturan yang diaudit. |
| 60% | Paket 15 tahun, 62 wilayah dan 105 pasangan lengkap. Seluruh luas, matriks, neraca dan regresi terhadap CSV R1 lulus validasi independen. |
| 80% | Grafik dan 15 pilihan tahun, pasangan contoh, filter, respons terlambat, galat dan coba ulang lulus di Edge serta Chrome. Empat lebar layar diperiksa. |
| 100% | Uji versi tampilan terbaru termasuk tombol tahun, fallback R1, manifest rusak dan pemulihan lulus. Panduan, roadmap dan Current State diperbarui. R2 selesai secara lokal. |

Persentase merupakan checkpoint keseluruhan pekerjaan, termasuk analisis, integrasi, dan validasi.

## Keputusan layanan

Peta memakai 15 raster UInt8 gzip yang dimuat sesuai tahun pilihan. Statistik disiapkan pada grid sumber sekitar 30 m untuk 62 wilayah dan 105 pasangan. Browser menyusun pasangan peta dari dua raster tahunan, lalu membaca statistik pasangan yang sesuai. Grafik luas tahunan memakai luas analisis, dengan area valid per tahun tersedia dalam tabel grafik.

Raster tahunan berukuran terkompresi sekitar 0,82–0,85 MB per tahun. Hasil pengukuran dan pemeriksaan tersimpan di [QA raster](../data/metadata/r2_display_qa.json). Empat tahun disimpan dalam cache memori aplikasi untuk membatasi penggunaan memori.

## Audit dan jejak hasil

- [Audit sumber](../data/metadata/r2_audit.json) mencatat aset, grid dan kunci cache.
- [Sampel kode mentah](../data/metadata/r2_class_sample_qa.json) merupakan pemeriksaan diagnostik. Sampel tersebut belum mengukur akurasi atau menjamin inventaris kelas lengkap.
- Reduksi luas memakai luas piksel dalam hektare pada transformasi grid R1. Daerah tidak valid di salah satu tahun dikeluarkan dari matriks transisi.
- Ringkasan kabupaten/kota 2010–2024 hasil hitung ulang berbeda maksimum sekitar 0,0014 ha dari R1, di bawah toleransi 0,01 ha. Pemeriksaan seluruh tabel dan matriks diterapkan ketika paket lengkap.
- Pemeriksaan API reducer merujuk [dokumentasi Google Earth Engine](https://developers.google.com/earth-engine/guides/reducers_weighting).

## Hasil validasi akhir

- [Validator data](../data/metadata/r2_validation.json) memeriksa 12.090 nilai luas tahunan dan 1.100.190 nilai transisi untuk 62 wilayah. Seluruh 105 pasangan memiliki matriks lengkap, luas nonnegatif, dan neraca luas yang sesuai.
- [QA paket](../data/metadata/r2_package_qa.json) mencatat selisih maksimum luas terhadap R1 sebesar 0,001714197 ha. Toleransi adalah 0,01 ha. Selisih pangsa perubahan maksimum sekitar 0,000000099 poin persentase. Raster kedua ujung periode identik dengan R1.
- [QA tahunan](../data/metadata/r2_annual_qa.json) mencatat cakupan valid AOI sekitar 99,9830–99,9833%. Sampel kode mentah dan angka cakupan merupakan pemeriksaan ketersediaan serta konsistensi data.
- Dua reduksi kabupaten awal dihitung ulang setelah pemeriksaan lintas pasangan menemukan selisih luas tahunan 0,036077 ha pada tingkat provinsi. Hasil sebelumnya diarsipkan di cache lokal. Paket final lolos toleransi konsistensi.
- [QA browser](../data/metadata/r2_browser_qa.json) lulus di Edge 157.0.4341.60 dan Chrome 157.0.8103.79. Uji mencakup semua 15 tahun, angka tabel dan grafik, pemilihan tahun melalui grafik, pasangan 2010–2011, 2014–2021, 2023–2024, regresi 2010–2024, filter kelas, dan perpindahan wilayah.
- Respons terlambat tidak menimpa pilihan terbaru. HTTP 404 pada raster atau statistik dapat dipulihkan dengan Coba lagi. Manifest R2 yang rusak menampilkan galat. Ketika manifest R2 tidak tersedia (404), pemuat memakai R1 dengan penanda dua pengamatan.
- Lebar 320, 390, 768 dan 1.366 px tidak menyebabkan halaman melebar secara horizontal. Grafik dan tabel dapat digeser di dalam panelnya pada layar kecil. Tangkapan layar diperiksa pada desktop dan lebar 390 px.
- Pengujian memakai tampilan terbaru yang ada di folder web saat uji browser. Berkas tampilan berubah selama pekerjaan berlangsung. Perubahan tersebut dipertahankan, dan pengujian tambahan mencakup pemuat data serta navigasi tahun yang tersedia pada versi tersebut.

Pengujian ini memakai dua browser berbasis Chromium secara headless pada localhost. Perangkat fisik, Safari, Firefox, pembaca layar dan performa hosting masih terbuka. Ketentuan distribusi BIG, kelengkapan batas, atribusi final dan identitas Koleksi 4.1 tetap perlu ditinjau sebelum publikasi.

## Definisi selesai

R2 selesai sebagai versi lokal yang menyediakan peta 15 tahun, grafik luas kelas, cakupan valid tahunan dan perbandingan seluruh 105 pasangan dengan tahun awal lebih kecil dari tahun akhir. Pekerjaan berikutnya adalah tinjauan pengalaman penggunaan serta penentuan prioritas R3. Animasi, pembanding geser, peringkat dan modul sawit pendukung mengikuti spesifikasi R3.
