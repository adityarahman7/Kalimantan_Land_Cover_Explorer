# Current State — Kalimantan Land Cover Explorer

Updated: 2026-11-17 (Asia/Jakarta)

## Penyimpanan GitHub — 17 November 2026

- Repositori privat dibuat di [adityarahman7/Kalimantan_Land_Cover_Explorer](https://github.com/adityarahman7/Kalimantan_Land_Cover_Explorer), dengan cabang utama `main`.
- Snapshot mencakup kode analisis dan WebGIS, dokumentasi, metadata QA, tabel ringkasan, proyek QGIS, serta cuplikan UI. Data produksi, lingkungan lokal, kredensial, dan paket `web/public/data/r1/` serta `r2/` dikecualikan melalui `.gitignore`.
- Clone repositori memerlukan penyiapan ulang data sebelum dashboard dapat digunakan. Unggahan kode bukan deployment website. Izin distribusi batas, identitas versi sumber, dan lisensi kode tetap terbuka.
- Keputusan: simpan versi saat ini; perbaikan berikutnya mengikuti masukan pengguna. Periksa riwayat commit dan cabang remote untuk status sinkronisasi terbaru.

## Pembaruan UI — 17 November 2026

- Revisi terbaru: tema hijau gelap, teks/formulir lebih besar, zoom gulir langsung berpusat pada kursor, basemap lokal daratan/laut Natural Earth, dan detail kelas descending berdasarkan persentase (terbesar → terkecil), sesuai koreksi pengguna (kategori tanpa persentase tetap di akhir).
- Satuan utama dashboard kini km², dengan pilihan ha. Konversi hanya untuk tampilan: 1 km² = 100 ha; statistik sumber, proporsi, dan raster tidak berubah. Grafik area/garis menampilkan ringkasan awal–akhir dan selisih luas kelas, serta titik tahun interaktif.
- QA revisi gelap: Chrome, 15 tahun × 13 kelas terurut; gulir tanpa Ctrl mengubah zoom 1× → 1,6×; pilihan km²/ha, perubahan 2010–2024, filter hutan → sawit, grafik kelas hutan dan pilihan titik 2016 diperiksa. Konversi angka acuan diuji melalui Node. Lebar CSS 356/434 tanpa overflow horizontal; desktop CSS 1518×1000 tanpa overflow halaman. Pengujian lintas browser/perangkat fisik revisi ini belum dijalankan.
- Cuplikan terbaru: `outputs/ui/dashboard-dark-desktop.jpg` dan `outputs/ui/dashboard-dark-mobile.jpg`. Basemap hanya konteks regional, bukan batas rinci atau input perhitungan. Berikutnya: tinjau tema, ukuran teks, dan pengalaman grafik bersama pengguna.

- Revisi terbaru mengikuti susunan dashboard ArcGIS pilihan pengguna: filter atas, indikator kiri, peta tengah, rincian kelas kanan, dan grafik bawah. Palet hijau/latar terang dipertahankan. Susunan ini menggantikan halaman panjang pada revisi awal.
- Tambahan: tombol atur ulang seluruh filter, bar proporsi kelas, panel sumber yang dapat ditutup dengan Escape, dan grafik responsif terhadap lebar kontainer.
- QA revisi: Chrome lokal, seluruh 15 tahun masing-masing memuat 13 baris kelas; Sambas, transisi hutan → sawit, pasangan 2014–2021, titik grafik 2016, atur ulang dan panel sumber berhasil. Desktop CSS 1707×710 serta 1518×1000 tanpa overflow halaman; lebar CSS 356/434/853 tanpa overflow horizontal. Belum diuji pada perangkat fisik atau lintas browser untuk layout terbaru.
- Cuplikan terbaru: `outputs/ui/dashboard-reference-desktop.jpg` dan `outputs/ui/dashboard-reference-mobile.jpg`. Berikutnya: penilaian audiens dan pemeriksaan lintas browser; publikasi tetap terpisah.

- UI lokal diperbarui dengan palet hijau hutan, navigasi sederhana, pengaturan wilayah/waktu yang dikelompokkan, peta utama, ringkasan angka, penjelasan otomatis dari statistik aktif, serta grafik dan tabel komposisi. Detail implementasi dan QA: [catatan UI](docs/ui_refresh_2026_11_17.md).
- Paket R2 tersedia pada akhir sesi. Pemeriksaan UI di Chrome mengonfirmasi 15 pilihan tahun dan 15 titik grafik; tahun perwakilan 2010, 2011, 2016, 2024 serta perubahan 2014–2021 berhasil dimuat. Memilih titik 2016 pada grafik memperbarui peta.
- Jika manifest R2 tidak tersedia (HTTP 404), UI memakai paket R1 asli dengan hanya dua tahun dan penanda keterbatasan. Kesalahan kontrak atau server R2 tetap dilaporkan, bukan disembunyikan.
- Keputusan: pertahankan warna kelas dan angka dari sumber; tampilkan sumber/metode dalam panel yang dapat dibuka; pengembangan tetap lokal. Cuplikan tersimpan di `outputs/ui/`.
- Terbuka: QA UI sesi ini bukan penilaian akurasi klasifikasi, uji pengguna, atau validasi perangkat fisik. Perizinan publikasi batas tetap mengikuti catatan proyek.
- Berikutnya: tinjau keterbacaan bersama audiens sasaran; lanjutkan validasi dan dokumentasi analisis R2 dalam alur data proyek sebelum publikasi.

## Status dan tujuan

- Fase 1 selesai sebagai baseline perencanaan; acuan [spesifikasi utama](docs/project_specification.md).
- Fase 2: audit awal terdokumentasi, dapat dilanjutkan ke penyiapan eksploratif dengan keterbatasan terbuka. Ini bukan persetujuan rilis atau bukti batas lengkap.
- Target tetap seluruh Kalimantan Indonesia, tahunan 2010–2024. R1 inti 2010/2024 → R2 tahunan → R3 lengkap.
- Fase 3 siap untuk analisis pilot R1. QGIS MCP menghasilkan GeoPackage tiga tingkat dan proyek QGIS yang berhasil dibuka ulang. Earth Engine memverifikasi akses aset, kode wilayah dan grid seluruh 15 band. Dua cuplikan raster lokal lolos QA kelas dan mask.
- Fase 4 selesai untuk pilot R1 2010 → 2024. Tabel dan peta tinjauan telah diperiksa dan siap disiapkan untuk web pada fase 5.
- Fase 5 siap untuk integrasi lokal R1. Paket statis memuat tiga GeoJSON, 62 statistik wilayah, legenda dan COG pasangan kelas 2010/2024. Uji HTTP lokal memuat 67 berkas dan seluruh pemeriksaan lulus.
- Fase 6 selesai untuk integrasi lokal R1. [WebGIS lokal](web/README.md) menyediakan pilihan 62 wilayah, dua tahun, mode perubahan, filter transisi, legenda, tabel luas dan metadata. Uji interaksi inti di Edge dan pembandingan raster terhadap COG lulus.
- Validasi lokal R1 lulus di Edge dan Chrome. [Catatan validasi](docs/phase6_validation.md) memuat kecocokan data seluruh wilayah, uji respons terlambat, simulasi galat, dan tampilan empat lebar layar. Grafik luas tahunan ditambahkan pada R2. Diagram aliran transisi tetap menjadi pekerjaan desain lanjutan.

## Paket R2

- WebGIS yang sama telah diperluas ke 15 tahun (2010–2024), grafik luas per kelas, cakupan valid tahunan, dan 105 pasangan tahun pada 62 wilayah kerja.
- [Laporan pelaksanaan](docs/r2_execution.md) mencatat checkpoint, keputusan layanan dan batas pengujian. Paket berada di `web/public/data/r2/` dengan manifest dan subfolder versi data.
- [Validasi data](data/metadata/r2_validation.json) lulus untuk 12.090 nilai luas tahunan dan 1.100.190 nilai transisi. Selisih maksimum luas terhadap R1 sekitar 0,001715 ha, di bawah toleransi 0,01 ha.
- Seluruh raster tahunan lolos QA. Raster 2010 dan 2024 identik dengan R1. Cakupan valid AOI sekitar 99,9830–99,9833% selama periode kerja.
- [Uji browser R2](data/metadata/r2_browser_qa.json) lulus pada Edge dan Chrome untuk empat lebar layar, termasuk grafik, filter, respons terlambat, galat, fallback R1 dan pemulihan. R2 selesai secara lokal pada 17 November 2026.
- [Panduan menjalankan dan membangun ulang aplikasi](web/README.md) memuat alur analisis, unduhan raster, pengemasan dan validasi lokal.

## Paket fase 5 dan proyek QGIS utama

- [Proyek utama](Kalimantan_Land_Cover_Explorer.qgz) adalah satu-satunya proyek QGIS aktif. Pembukaan ulang mengonfirmasi 19 layer dan tabel dari pekerjaan awal sampai fase 5.
- Dua proyek fase lama dan cadangan proyek utama sebelum penggabungan tersimpan di `data/interim/qgis_archive/`.
- [Panduan data WebGIS](docs/phase5_data_service.md) menjelaskan manifest, skema dan QA. Paket berada di `web/public/data/r1/`; [modul akses data](web/r1-data.mjs) dipakai pada fase 6.
- COG tampilan sekitar 300 m cocok piksel demi piksel dengan peta tinjauan fase 4 setelah didekode. Statistik tetap dari analisis sekitar 30 m. Izin distribusi batas BIG tetap terbuka sebelum publikasi.

## Paket fase 4

- [Hasil dan metode](docs/phase4_analysis.md) menautkan tiga tabel CSV untuk 1 AOI, 5 provinsi dan 56 kabupaten/kota. Laporan rekonsiliasi tersimpan di `data/metadata/phase4_qa.json`.
- AOI langsung menghasilkan 10.474.804,21 ha berubah kelas, atau 19,606065% dari 53.426.346,60 ha valid bersama. Luas stabil 42.951.542,40 ha dan tidak dapat dibandingkan 9.087,42 ha.
- Grup fase 4 pada proyek utama memuat mosaik tinjauan sekitar 300 m dan tiga tabel CSV. Statistik dihitung pada grid sumber sekitar 30 m. Skrip peta Earth Engine menyediakan alur grid asli.
- Selisih empat ukuran luas AOI terhadap audit fase 2 di bawah 0,01 ha. Penjumlahan luas kabupaten/kota 6.839,51 ha lebih besar dari AOI langsung. Gunakan statistik sesuai tingkat wilayah dan pertahankan catatan rekonsiliasi.

## Paket fase 3

- Grup fase 3 pada proyek utama berisi 56 kabupaten/kota, 5 provinsi, 1 AOI, dan 2 cuplikan QA.
- Paket batas lokal berada di `data/processed/phase3_boundaries.gpkg`. AOI memakai ID `KALIMANTAN_ID`. Laporan batas dan raster tersimpan di `data/metadata/`.
- [Panduan fase 4](docs/phase3_handoff.md) menjelaskan skema, parameter dan cara menggunakan fungsi penyiapan raster Earth Engine.
- Pengecekan sumber BIG menemukan satu fitur tambahan Kalimantan Timur (`OBJECTID=1210`) tanpa kode dan nama kabupaten/kota. Cakupan pilot tetap 56 fitur. Diagnostik overlap mendekati nol pada presisi numerik, sedangkan kelengkapan cakupan terhadap referensi independen belum dinilai.

## Progres dan keluaran fase 2

- Aset MapBiomas direktori `collection4`, versi internal `v2`, berhasil dibaca pengguna. Band 1990–2024 tersedia; audit rinci difokuskan pada 2010/2024.
- Kedua band: EPSG:4326, transformasi identik, skala nominal sekitar 30 m. Parameter lengkap pada [inventaris](docs/data_inventory.md).
- Sampel kelas: 455 piksel; 12 kode pada 2010 dan 13 pada 2024, sesuai kode legenda yang diperiksa. Ini bukan inventaris kelas menyeluruh atau penilaian akurasi.
- Batas BIG: sumber menurut pengguna `BATASWILAYAH_KABKOTA_20260601.gdb`, diunduh 1 November 2026 dari Ina-Geoportal. Berkas kerja 56 fitur, lima provinsi. Satu fitur pulau telah dihapus; kelengkapan cakupan belum dipastikan.
- Konversi geometri MultiSurface ke MultiPolygonZ dan ekspor SHP berhasil menurut pengguna. Aset batas terunggah dan pemeriksaan jumlah/atribut oleh pengguna lolos.
- [Skrip audit](scripts/earth_engine/01_audit_data.js) menyimpan deklarasi eksplisit aset batas. ID yang sama berhasil dibaca langsung melalui API Earth Engine pada 10 November 2026.
- [CSV cakupan](data/metadata/audit_cakupan_valid_2010_2024.csv) dibaca ulang: wilayah 53.435.434,04 ha; valid 2010 99,983021%; valid 2024 99,983300%; valid bersama 99,982994%; tidak dapat dibandingkan 9.087,42 ha.
- [CSV tiga titik](data/metadata/contoh_lokasi_tidak_valid.csv) tersimpan. Ketiganya termask pada dua tahun dan berada sekitar perbatasan menurut pemeriksaan pengguna; penyebab seluruh area invalid belum dipastikan.
- Satu lokasi kelas sawit 2024 dibandingkan dengan komposit median Sentinel-2 2024: terlihat pola perkebunan, belum konfirmasi independen jenis tanaman dan belum pemeriksaan tahun 2010.
- ATBD 4.1, legenda, ketentuan CC-BY-SA dan keterbatasan bukti akurasi dicatat pada inventaris.

## Keputusan kerja

- Grid asli yang identik dipertahankan untuk audit; luas memakai `ee.Image.pixelArea() / 10000`, bukan asumsi 900 m² per piksel.
- Kode valid awal: 3, 5, 9, 13, 21, 24, 25, 30, 31, 33, 35, 40, 76. Mask, kode 27 dan kode lain di luar daftar tidak dihitung valid.
- Analisis perubahan menggunakan area valid bersama; area tidak dapat dibandingkan tidak diisi dengan kelas perkiraan atau dihitung stabil.
- Berkas batas yang telah diseleksi/disederhanakan tetap berada di `data/raw/` atas pilihan pengguna; provenance menyatakan bahwa ini berkas kerja yang sudah dimodifikasi.
- Mode pendampingan kembali ke langkah kecil yang dijalankan pengguna setelah tugas perapian ini. Gaya Markdown notebook mengikuti UrbanRVM sebagaimana dicatat pada `notebooks/README.md`.

## Pertanyaan terbuka dan batas hasil

- Identitas aset `coverage_v2` sebagai Koleksi 4.1 belum terkonfirmasi; metadata `v2` tidak cukup.
- Angka akurasi yang cocok belum ditemukan; tidak menggunakan angka Koleksi 2 sebagai akurasi aset ini.
- Kelengkapan kabupaten/kota/pulau dan celah terhadap batas independen masih perlu ditinjau sebelum rilis. Validitas geometri hasil konversi/dissolve dan diagnostik overlap telah diperiksa untuk cakupan pilot.
- Ketentuan distribusi batas BIG dan URL dataset spesifik belum dicatat; lisensi kode juga belum dipilih.
- Statistik luas dan transisi serta paket data lokal tersedia untuk pasangan pilot 2010/2024. Deret seluruh tahun sudah tersedia pada R2. Analisis BIOPAMA dan hosting publik tetap pada pekerjaan lanjutan.
- Interpretasi fase 4 terbatas pada kelas yang terpetakan. Cakupan valid dan hasil rekonsiliasi mengukur ketersediaan serta konsistensi perhitungan.

## Rencana R2

- [Rencana R2](docs/r2_plan.md) menetapkan 7 fase dan 22 tahap yang dikerjakan pada 17 November 2026. Data 13 tahun tambahan diintegrasikan ke aplikasi yang sama.

## Langkah berikutnya

1. Tinjau pengalaman menggunakan grafik dan pemilihan tahun R2, lalu tentukan prioritas R3. Safari, Firefox dan performa hosting masih terbuka.
2. Verifikasi atribusi, status versi sumber dan ketentuan distribusi batas BIG sebelum rilis.
3. Lanjutkan semua pekerjaan QGIS pada proyek utama. Pertahankan catatan versi, cakupan dan perizinan sebelum rilis.

## Dokumen dan bukti

- [Inventaris dan audit](docs/data_inventory.md): provenance, parameter, lisensi, hasil dan keterbatasan.
- [Log pengolahan](docs/processing_log.md): input → proses → output, pemeriksaan dan galat.
- [Roadmap](docs/roadmap.md): fase kerja dan urutan rilis.
- Repositori GitHub privat tersedia; lihat bagian penyimpanan GitHub di atas. Lisensi kode belum dipilih.
- Belum ada notebook Kalimantan; audit saat ini tersimpan sebagai JavaScript GEE.

## Referensi prototipe dari handover
- Sites project: appgprj_6add7c7a0a488191b6a1415f95630043
- Preview: https://kalimantan-landcover-aditya.fairymyna66.chatgpt.site
- Checkout cloud yang disebut handover belum diverifikasi tersedia secara lokal.

