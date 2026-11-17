# Paket data WebGIS R1

Paket lokal R1 menyediakan data 2010 dan 2024 pada batas kerja 56 kabupaten/kota. Titik masuknya adalah [manifest](../web/public/data/r1/manifest.json). Paket dapat disajikan melalui HTTP statis untuk integrasi fase 6.

| Produk | Lokasi dalam paket | Pemakaian |
| --- | --- | --- |
| Manifest, sumber, legenda dan indeks wilayah | `manifest.json` | Metadata awal, kode kelas, pilihan tahun dan alamat berkas |
| Batas tiga tingkat | `aoi.geojson`, `province.geojson`, `district.geojson` | Pilihan AOI, provinsi dan kabupaten/kota |
| Statistik wilayah | `stats/{region_id}.json` | Luas tahunan, cakupan valid, perubahan dan matriks transisi |
| Raster pasangan kelas | `class_pair_2010_2024.tif` | Turunkan tampilan 2010, 2024, perubahan dan filter transisi dari satu grid |

## Kontrak data

- ID wilayah adalah string. Pertahankan titik pada kode seperti `61.01`. Field penghubung tiap GeoJSON tercantum pada manifest.
- Statistik tahunan mengikuti `class_order`. Matriks transisi memakai urutan yang sama, dengan kelas awal pada baris dan kelas akhir pada kolom. Luas dalam ha. Pangsa tahunan memakai luas valid tahun terpilih, sedangkan perubahan dan transisi memakai luas valid bersama.
- AOI berasal dari reduksi langsung dan provinsi dari penjumlahan kabupaten/kota. Selisih penjumlahan kabupaten/kota terhadap AOI tetap tersedia di metadata.
- COG UInt16 menyimpan `100 × kelas_2010 + kelas_2024`. Contoh `335` berarti 3 → 35. Nol di salah satu posisi menandai invalid pada tahun itu. Nilai 65535 berarti di luar AOI. Nilai perubahan adalah 0 stabil, 1 berubah dan 2 tidak dapat dibandingkan.
- Raster tampilan berjarak grid nominal sekitar 300 m dalam EPSG:4326. Statistik bersumber dari analisis fase 4 pada grid sekitar 30 m. Batas GeoJSON digeneralisasi sebesar 0,001 derajat untuk tampilan. Pertahankan GeoPackage fase 3 untuk analisis spasial.
- GeoJSON memakai koordinat longitude/latitude. Ketiga layer dibuka ulang, geometri diperiksa valid, dan ID cocok dengan tabel. Generalisasi dilakukan per fitur sehingga garis batas tampilan dapat memiliki celah atau overlap kecil.
- Status integrasi lokal mempertahankan batasan kelengkapan batas, identitas koleksi 4.1 yang belum pasti, serta ketentuan distribusi BIG yang perlu ditinjau sebelum publikasi.

Format COG memakai empat overview dengan resampling nearest untuk nilai kategori. [Dokumentasi COG GDAL](https://gdal.org/en/stable/drivers/raster/cog.html)

## Pemeriksaan pemuatan

[Laporan QA](../data/metadata/phase5_qa.json) mencatat 67 berkas berhasil dimuat lewat HTTP lokal. Seluruh 62 statistik wilayah, ID batas, decoder kategori dan penanganan 404 diperiksa. Dekode perubahan cocok piksel demi piksel dengan raster tinjauan fase 4.

Total transfer uji 4,61 MB. Pemuatan awal yang diuji terdiri dari manifest, statistik AOI, batas AOI dan COG, sekitar 2,75 MB dalam 72,2 ms di localhost. Angka itu adalah satu pengukuran transfer lokal tanpa waktu rendering browser. Ukuran paket dapat dipakai sebagai patokan untuk pengujian hosting pada fase rilis.

## Integrasi fase 6

Sajikan folder `web` melalui server HTTP lokal dan gunakan URL manifest `/public/data/r1/manifest.json` untuk struktur folder ini. [Modul akses data](../web/r1-data.mjs) menyediakan `loadR1(manifestUrl)`, `getStats(regionId)`, `getBoundaries(level)`, `rasterUrl`, dan `decodePair(value)`. Aplikasi fase 6 memuat statistik per wilayah dan memakai salinan gzip UInt16 yang diturunkan dari COG. Lihat [panduan WebGIS](../web/README.md).

Untuk membangun ulang, jalankan `scripts/analyze_phase4.py --web-pairs-only` dengan akses Earth Engine, lalu `scripts/package_phase5.py` melalui Python QGIS/GDAL. Proses ini memakai CSV fase 4 sebagai sumber statistik. Folder hasil lokal diabaikan Git untuk memisahkan bahan integrasi dari paket yang kelak disetujui untuk publikasi.

## Proyek QGIS tunggal

Gunakan [Kalimantan Land Cover Explorer](../Kalimantan_Land_Cover_Explorer.qgz). Proyek utama berisi 19 layer dan tabel yang berhasil dibuka ulang. Grup fase 3, 4 dan 5 memisahkan bahan analisis dari bahan tampilan. Tiga layer batas siap analisis yang sama pada fase 3 dan 4 hanya disimpan sekali. Data tampilan web ditambahkan sebagai layer terpisah dengan visibilitas awal nonaktif.

Arsip di `data/interim/qgis_archive/` menyimpan proyek utama sebelum penggabungan dan dua snapshot fase lama. Jika perlu memulihkan snapshot, salin berkas yang dipilih kembali ke akar proyek agar jalur relatifnya kembali sesuai. Pekerjaan QGIS berikutnya diteruskan pada proyek utama.
