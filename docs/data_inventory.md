# Inventaris dan audit data

Status diperbarui: 1 November 2026. Audit awal telah dijalankan pengguna di QGIS dan Earth Engine. Ringkasan di bawah menggabungkan keluaran yang dilaporkan pengguna, tangkapan layar, pemeriksaan dokumen, dan dua CSV yang dibaca ulang dari repositori. Penyelarasan dokumentasi ini tidak menjalankan ulang Earth Engine atau audit geometri.

| Dataset                      | Peran                  | Versi                                                | Status akses       | Tahun/band aktual | Grid/CRS        | Mask/NoData     | Lisensi                                   |
| ---------------------------- | ---------------------- | ---------------------------------------------------- | ------------------ | ----------------- | --------------- | --------------- | ----------------------------------------- |
| MapBiomas Indonesia          | Klasifikasi tahunan    | Direktori collection4, versi internal v2; identitas 4.1 belum pasti | Berhasil dijalankan pengguna | Band 1990–2024 terbaca; fokus audit 2010/2024 | EPSG:4326; transformasi identik; nominal ~30 m | Cakupan valid dihitung; tiga titik termask diperiksa | CC-BY-SA menurut penyedia; nomor versi lisensi tidak dicantumkan |
| BIOPAMA Global Oil Palm v1.2 | Sawit statis pendukung | v1.2 menurut handover                                | Belum diuji        | Belum dibaca      | Belum diperiksa | Belum diperiksa | CC-BY-4.0 menurut handover; periksa ulang |
| Batas administrasi           | AOI dan agregasi       | BIG, berkas sumber BATASWILAYAH_KABKOTA_20260601.gdb; tanggal edisi resmi belum dipastikan | GPKG/SHP lokal dan aset GEE digunakan | Lima provinsi, 56 fitur kerja | EPSG:4326; hasil konversi MultiPolygonZ menurut metadata pengguna | Satu fitur pulau dihapus; cakupan belum dipastikan lengkap | Ketentuan distribusi BIG belum dicatat/terverifikasi |

## Checkpoint MapBiomas

- [x] Aset berhasil dibaca oleh akun Earth Engine pengguna.
- [x] Nama band 2010 dan 2024 terkonfirmasi.
- [x] Identitas aset, label direktori koleksi dan versi internal dicatat, dengan ketidakpastian 4.1 dipertahankan.
- [x] CRS dan transformasi grid masing-masing band dicatat.
- [x] Kode pada sampel dibandingkan dengan legenda; ini bukan inventaris kelas menyeluruh.
- [x] Mask dan kode 27 dibedakan dalam definisi audit; tiga titik terbukti termask pada kedua tahun. Luas tiap penyebab invalid belum dipisahkan.
- [x] Keberadaan lima provinsi dan cakupan valid pada batas kerja diperiksa; kelengkapan semua pulau belum terverifikasi.
- [x] Lisensi, format atribusi, dan keterbatasan bukti akurasi dicatat.
- [ ] Identitas aset sebagai Koleksi 4.1 dipastikan.
- [ ] Angka akurasi yang sesuai dengan aset dan periode dipastikan.

Checklist selesai menyatakan pemeriksaan awal telah dilakukan, bukan bahwa seluruh keterbatasan telah diselesaikan.

## Bukti yang perlu disimpan

Simpan keluaran metadata kecil di `data/metadata/` dan catatan pemeriksaan di `docs/processing_log.md`. Catat tanggal akses, URL/asset ID, versi, parameter, serta keterbatasan. Jangan menyimpan token atau informasi akun.

## Sumber

- [Alamat aset MapBiomas](https://landy.mapbiomas.id/en/landsatmosaics): diperiksa ulang 26 Oktober 2026.
- [Akses GEE](https://landy.mapbiomas.id/en/gee): diperiksa ulang 26 Oktober 2026.
- [Unduhan MapBiomas](https://landy.mapbiomas.id/en/collectionmap): diperiksa ulang 26 Oktober 2026.
- [Legenda](https://landy.mapbiomas.id/en/legendcode): kode Koleksi 4 diperiksa pada audit 1 November 2026.
- [Ketentuan penggunaan MapBiomas](https://landy.mapbiomas.id/en/termsofuse): diperiksa 1 November 2026.
- [Penilaian akurasi](https://landy.mapbiomas.id/en/accuracy-assessment): halaman yang diperiksa masih membahas Koleksi 2.0.
- [Ina-Geoportal](https://tanahair.indonesia.go.id/portal-web/): portal sumber batas menurut pengguna; tautan dataset spesifik belum tersimpan.
- [BIOPAMA](https://developers.google.com/earth-engine/datasets/catalog/BIOPAMA_GlobalOilPalm_v1_2): rujukan handover; perlu pemeriksaan ulang.

## Audit MapBiomas — 1 November 2026

### Identitas aset yang diperiksa

- Asset ID: `projects/mapbiomas-public/assets/indonesia/lulc/collection4/mapbiomas_indonesia_collection4_coverage_v2`
- Label koleksi pada dokumentasi alamat aset: Koleksi 4.
- Metadata aset: `version: v2`, `data_type: annual`, dan `band_format: classification_{year}`.
- Akses aset berhasil diuji melalui Earth Engine.
- Band `classification_2010` dan `classification_2024` tersedia.
- Identitas aset sebagai Koleksi 4.1 belum terkonfirmasi. Versi internal `v2` tidak otomatis berarti Koleksi 4.1.

### Dokumen metodologi

Dokumen: **Algorithm Theoretical Basis Document (ATBD), Collection 4.1, Version 1, Februari 2026**.

Berkas: `ATBD Mapbiomas ID Col 4.1 EN.pdf`.

Bagian yang diperiksa: sampul, Tabel 1 pada halaman 4–5, perbaikan Koleksi 4.1 pada halaman 26–27, serta strategi validasi pada halaman 27–30.

| Aspek                        | Temuan                                                                                                            |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Periode                      | Koleksi 4 dan 4.1 mencakup 1990–2024.                                                                             |
| Perbaikan Koleksi 4.1        | Filter temporal dan spasial, koreksi menggunakan GEDI, serta penyesuaian konsistensi kelas kebun kayu.            |
| Angka akurasi                | Kolom akurasi Koleksi 4 dan 4.1 pada Tabel 1 berisi tanda “–”. Angka akurasi tidak disajikan pada tabel tersebut. |
| Validasi independen          | Dokumen menjelaskan 12.957 sampel untuk 2000–2022 yang pertama kali digunakan pada Koleksi 2.                     |
| Hubungan dokumen dengan aset | Alamat aset `coverage_v2` belum ditemukan dalam pemeriksaan teks dokumen.                                         |

### Batas interpretasi

- Penjelasan perbaikan metode bukan bukti kuantitatif akurasi Koleksi 4.1.
- Akurasi Koleksi 2 tidak digunakan sebagai angka akurasi aset yang sedang dianalisis.
- Tanda “–” pada tabel tidak berarti akurasi nol.
- Kelas 13 diperlakukan sebagai antropogenik dalam analisis transisi yang dijelaskan dokumen. Hal ini tidak membuktikan penyebab perubahan setiap piksel secara individual.
- Pemeriksaan sampel dan tampilan peta yang telah dilakukan belum merupakan penilaian akurasi statistik.
- Cakupan kode kelas valid sudah dihitung pada batas kerja; hasilnya tidak membuktikan ketepatan klasifikasi atau kelengkapan batas.

### Tindak lanjut

- [ ] Memastikan hubungan aset `coverage_v2` dengan versi koleksi produk.
- [ ] Menelusuri hasil evaluasi akurasi yang sesuai jika tersedia.
- [x] Menghitung cakupan data valid untuk 2010 dan 2024 pada wilayah kerja.
- [ ] Menambahkan URL resmi PDF saat tautannya tersedia.
- [ ] Memastikan ketentuan atribusi/distribusi batas BIG sebelum publikasi.
- [ ] Menelusuri fitur pulau yang dihapus dan memeriksa kelengkapan batas sebelum analisis final/rilis.

### Pemeriksaan cakupan valid dan lokasi termask

Berdasarkan batas kerja 56 fitur, luas wilayah sekitar 53.435.434 ha. Cakupan kelas valid mencapai 99,9830% pada 2010, 99,9833% pada 2024, dan 99,9830% pada kedua tahun secara bersamaan. Area tidak dapat dibandingkan sekitar 9.087 ha.

Tiga titik contoh dari area tidak dapat dibandingkan diperiksa. Seluruhnya berada di sekitar perbatasan Indonesia–Malaysia dan termask pada kedua tahun. Nilai `-9999` adalah penanda pemeriksaan, bukan kode kelas asli.

Temuan ini konsisten dengan kemungkinan perbedaan cakupan raster dan batas administrasi. Pemeriksaan tiga titik tidak mewakili seluruh area tidak valid dan belum memastikan penyebab keseluruhannya.

Area tidak valid tetap dilaporkan secara terpisah dan dikeluarkan dari analisis perubahan. Persentase perubahan menggunakan luas valid bersama sebagai denominator. Hasil cakupan tetap memiliki keterbatasan akibat penghapusan satu fitur pulau dari batas kerja.

### Pemeriksaan visual lokasi contoh 2024

- Koordinat: 116.11180945, −2.00125259.
- Lokasi dipilih dari tampilan kelas sawit MapBiomas 2024.
- Referensi: komposit median Sentinel-2 SR Harmonized sepanjang 2024, dengan penyaringan menggunakan SCL.
- Pengamatan: terlihat jaringan jalan dan pembagian blok vegetasi yang konsisten dengan kawasan perkebunan.
- Kesimpulan: terdapat kesesuaian visual awal dengan pola perkebunan, tetapi jenis tanaman belum dipastikan secara independen.
- Keterbatasan: satu lokasi pilihan pengguna, bukan sampel acak; komposit bukan citra satu tanggal; pemeriksaan ini tidak menghasilkan angka akurasi dan belum memeriksa kondisi 2010.

## Parameter audit dan berkas bukti

- Skrip: [01_audit_data.js](../scripts/earth_engine/01_audit_data.js).
- Band: `classification_2010` dan `classification_2024`.
- CRS: `EPSG:4326`.
- Transformasi identik kedua band: `[0.0002694945852358564, 0, 93.51839400103549, 0, -0.0002694945852358564, 7.2919844873118045]`.
- Skala nominal yang dilaporkan pengguna: `29.999999999999996` m, sekitar 30 m. Luas piksel tidak diasumsikan seragam.
- Kode valid awal: `3, 5, 9, 13, 21, 24, 25, 30, 31, 33, 35, 40, 76`. Piksel termask, kode 27, dan kode lain dikeluarkan. Penyebab di luar mask masih perlu dipisahkan bila diperlukan.
- Metode luas: `ee.Image.pixelArea() / 10000`, penjumlahan pada grid band 2010, `clipToCollection(batasAdmin)`, kotak region `[108.59, -4.95, 119.04, 4.42]`, `tileScale: 4`, `maxPixels: 1e10`. Batas kerja digunakan sebagai gabungan cakupan tanpa menjumlahkan poligon satu per satu.
- Sampling kelas: target perkiraan 1.000 piksel, skala 30 m, `seed: 42`, `tileScale: 4`; pengguna melaporkan 455 sampel. Ditemukan 12 kode pada 2010 dan 13 pada 2024. Tidak ditemukannya kelas pada sampel tidak membuktikan ketiadaan kelas pada seluruh wilayah.
- CSV asli: [audit_cakupan_valid_2010_2024.csv](../data/metadata/audit_cakupan_valid_2010_2024.csv).

| Hasil dari CSV asli | Nilai |
| --- | ---: |
| Luas wilayah kerja (ha) | 53.435.434,03534286 |
| Luas valid 2010 (ha) | 53.426.361,23797169 |
| Luas valid 2024 (ha) | 53.426.510,20063842 |
| Luas valid bersama (ha) | 53.426.346,61365083 |
| Cakupan valid 2010 (%) | 99,9830210093 |
| Cakupan valid 2024 (%) | 99,9832997806 |
| Cakupan valid bersama (%) | 99,9829936411 |
| Tidak dapat dibandingkan (ha; wilayah dikurangi valid bersama) | 9.087,42169203 |

Angka CSV dibaca ulang dan persentasenya dihitung ulang secara lokal pada penyelarasan dokumentasi. Ini bukan eksekusi ulang Earth Engine. Presisi penyimpanan angka tidak sama dengan ketelitian spasial atau akurasi produk.

CSV titik: [contoh_lokasi_tidak_valid.csv](../data/metadata/contoh_lokasi_tidak_valid.csv). Menurut hasil yang dijalankan pengguna, ketiga titik berikut bernilai penanda `-9999` pada kedua tahun dan berada di sekitar perbatasan:

| Titik | Bujur | Lintang | Nilai 2010 | Nilai 2024 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 114.82099773288161 | 2.1234825843659317 | -9999 | -9999 |
| 2 | 113.67887968065205 | 1.2354979260137853 | -9999 | -9999 |
| 3 | 114.72883058473096 | 1.834314894407858 | -9999 | -9999 |

CSV menyimpan koordinat; nilai kelas dan pengamatan lokasinya bersumber dari laporan eksekusi pengguna dalam percakapan, bukan kolom tambahan pada CSV. Skrip menyimpan titik ketiga sebagai contoh aktif; koordinat lain dapat menggantikannya saat mengulang pemeriksaan.

## Provenance batas administrasi

- Penyedia: Badan Informasi Geospasial, portal Ina-Geoportal; sumber ini dinyatakan pengguna.
- Nama unduhan asli: `BATASWILAYAH_KABKOTA_20260601.gdb`.
- Tanggal unduh menurut pengguna: 1 November 2026.
- `20260601` adalah bagian nama berkas; belum dicatat sebagai tanggal edisi resmi yang diverifikasi dari metadata penyedia.
- Berkas kerja: `data/raw/batas_admin_kalimantan_BIG_2026.gpkg`. Atas pilihan pengguna, hasil seleksi dan penyederhanaan atribut disimpan di raw. Karena sudah dimodifikasi, berkas ini tidak dianggap salinan asli yang tidak berubah. Keberadaan arsip GDB sumber di repositori lokal belum diverifikasi.
- Atribut pada tangkapan layar setelah penyederhanaan: `fid`, `REMARK`, `METADATA`, `KDPKAB`, `KDPPUM`, `WADMKK`, `WADMPR`, `Shape_Length`, `Shape_Area`. Kolom luas bawaan tidak digunakan untuk perhitungan cakupan raster.
- Seleksi awal berisi 57 fitur. Pengguna menghapus satu fitur pulau kecil dengan atribut tidak jelas sehingga tersisa 56; identitas dan implikasi cakupannya belum dituntaskan. Ini bukan penghapusan baris tanpa geometri.
- Menurut pemeriksaan pengguna: lima provinsi tersedia dan nama provinsi tidak kosong; ekspresi pemeriksaan kode kosong/berulang menghasilkan 0 fitur; pemeriksaan GEOS sebelum konversi melaporkan seluruh geometri valid. Validitas tersebut bukan bukti bebas overlap/gap atau lengkapnya semua pulau.
- Ekspor SHP awal gagal karena MultiSurface. Segmentasi belum menyelesaikan semua fitur. GDAL dengan `CONVERT_TO_LINEAR` dan `PROMOTE_TO_MULTI` menghasilkan `data/interim/batas_admin_kalimantan_linear.gpkg`, tipe MultiPolygonZ, 56 fitur menurut metadata pengguna.
- SHP hasil ekspor: `data/interim/batas_admin_gee/batas_admin_kalimantan.shp` beserta berkas pendamping. ZIP unggahan: `data/interim/batas_admin_gee.zip`.
- Unggahan GEE diperiksa pengguna: 56 fitur, lima provinsi, dan atribut utama terbaca. Nama project dan aset terlihat pada tangkapan layar: `portofolio-513404` / `batas_admin_gee`.
- Deklarasi dalam skrip lokal memakai `projects/portofolio-513404/assets/batas_admin_gee`, disusun dari project/nama aset tersebut. Deklarasi eksplisit ini belum dijalankan ulang oleh asisten; sebelumnya pengguna menjalankan lewat Imports.
- Geometri pascakonversi, overlap/gap dan kelengkapan wilayah menjadi pemeriksaan fase 3 sebelum penggunaan final. Konversi dapat mendekati kurva dengan segmen, sehingga jumlah fitur yang tetap tidak sendirinya menjamin semua bentuk identik.

## Lisensi dan atribusi MapBiomas

Halaman ketentuan penggunaan yang diperiksa pada 1 November 2026 menyebut CC-BY-SA, membolehkan penyalinan dan redistribusi, serta meminta atribusi MapBiomas Indonesia. Nomor versi lisensi tidak disebutkan; jangan menambahkan 4.0 tanpa bukti. Lisensi dataset tidak otomatis menjadi lisensi seluruh kode repositori.

Format atribusi yang diminta penyedia:

> MapBiomas Indonesia - Collection [version] time-series maps of land-use and land-cover, accessed on [date] via: [link]

Sebelum publikasi, lengkapi versi koleksi produk yang benar, tanggal akses, dan tautan. Untuk catatan internal saat ini gunakan deskripsi literal: direktori collection4, versi internal v2, identitas Koleksi 4.1 belum terkonfirmasi.

## Kesimpulan audit awal fase 2

Audit awal tersedia sebagai dasar penyiapan data eksploratif: akses, band, grid, kode sampel, batas kerja, cakupan valid dan pemeriksaan visual awal telah didokumentasikan. Hasil belum merupakan validasi akurasi regional atau perhitungan perubahan kelas. Hubungan aset dengan Koleksi 4.1, akurasi yang sesuai, kelengkapan batas dan izin distribusi BIG tetap terbuka. Lanjut ke fase 3 dengan catatan tersebut; klaim cakupan lengkap dan kesiapan rilis belum diberikan.
