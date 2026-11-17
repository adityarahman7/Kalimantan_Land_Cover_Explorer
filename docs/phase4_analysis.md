# Analisis perubahan tutupan lahan R1

Pasangan analisis adalah 2010 → 2024 pada batas kerja 56 kabupaten/kota. Identitas aset, batas, grid, dan mask mengikuti [serah terima fase 3](phase3_handoff.md).

| Input | Proses | Output |
| --- | --- | --- |
| Dua band MapBiomas, batas kabupaten/kota, serta mask tahunan dan mask valid bersama | Kelompokkan luas piksel berdasarkan pasangan kelas di grid asli | Luas kelas per tahun, matriks transisi, dan ringkasan perubahan pada tiga tingkat wilayah |
| Pasangan kelas pada area valid bersama | Tentukan area stabil, berubah, dan tidak dapat dibandingkan | Raster perubahan dalam Earth Engine, dengan GeoTIFF tinjauan untuk QGIS |

## Metode

Perhitungan memakai `pixelArea() / 10000` dan grid asli EPSG:4326. Untuk setiap piksel, kode internal `100 × kelas_awal + kelas_akhir` menyimpan pasangan kelas. Nilai 0 pada salah satu posisi menandai piksel invalid pada tahun tersebut. Nol internal ini dikeluarkan dari matriks transisi. Piksel itu tetap dapat menyumbang luas kelas pada tahun lain jika kelasnya valid.

Luas kelas tahunan memakai luas valid pada tahun yang sama sebagai penyebut. Persentase perubahan serta proporsi transisi memakai luas valid bersama. Diagonal matriks menunjukkan area stabil dan sel lainnya menunjukkan area berubah. Area tidak dapat dibandingkan dilaporkan terpisah.

Statistik kabupaten/kota dihitung melalui reduksi berbobot pada batas masing-masing. Statistik provinsi adalah penjumlahan kabupaten/kota. Statistik seluruh Kalimantan dihitung secara langsung pada cakupan AOI dengan mask dan kotak perhitungan yang sama dengan fase 2. Kuantisasi bobot piksel di tepi zona dapat menyebabkan selisih kecil antarlevel. [Dokumentasi reduksi wilayah Earth Engine](https://developers.google.com/earth-engine/guides/reducers_reduce_region).

## Pemeriksaan

- Pastikan semua 56 kode kabupaten/kota muncul satu kali dan dapat dikelompokkan menjadi lima provinsi.
- Pada setiap wilayah, luas stabil + berubah + tidak dapat dibandingkan harus sama dengan luas wilayah dalam toleransi aritmetika 0,000001 ha.
- Selisih empat luas AOI terhadap ekspor fase 2 harus ≤ 1 ha. Ini toleransi reproduksi komputasi.
- Selisih penjumlahan kabupaten/kota terhadap AOI langsung harus ≤ 0,1% luas AOI. Simpan selisih aktual, termasuk pada tiap kategori perubahan.
- Simpan semua kombinasi kelas dalam tabel dengan nol untuk pasangan yang tidak muncul setelah reduksi berhasil. Persentase kosong bila penyebutnya nol.

## Menjalankan ulang

Jalankan `scripts/analyze_phase4.py` menggunakan Python dengan `earthengine-api`, `requests`, serta kredensial Earth Engine yang dapat membaca kedua aset. Reduksi berhasil disimpan di `data/interim/phase4/` menurut identitas aset, konfigurasi, dan versi skrip. Berkas tersebut memungkinkan pekerjaan dilanjutkan tanpa mengulang reduksi yang sama.

Skrip `scripts/earth_engine/02_change_map_r1.js` menyediakan layer peta dan contoh filter transisi di Code Editor. Tugas ekspor GeoTIFF grid asli disiapkan oleh skrip dan baru dijalankan saat dipilih pada tab Tasks. Kode peta 0 = stabil, 1 = berubah, 2 = tidak dapat dibandingkan, 255 = NoData di luar batas kerja pada GeoTIFF.

## Batas interpretasi

Perubahan yang dihitung adalah perbedaan kode klasifikasi antara dua tahun. Perbedaan itu dapat mencakup kesalahan pemetaan dan tidak mengidentifikasi waktu pasti, penyebab, atau status legal perubahan. Cakupan tetap memakai 56 fitur kerja. Fitur BIG tanpa kode yang diidentifikasi pada fase 3 masih di luar paket pilot.

## Hasil statistik 2010–2024

| Ukuran seluruh AOI | Hasil |
| --- | ---: |
| Luas wilayah kerja | 53.435.434,03 ha |
| Luas valid bersama | 53.426.346,60 ha |
| Stabil | 42.951.542,40 ha |
| Berubah kelas | 10.474.804,21 ha |
| Persentase berubah terhadap valid bersama | 19,606065% |
| Tidak dapat dibandingkan | 9.087,42 ha |
| Sawit terpetakan 2010, area valid tahun tersebut | 3.306.668,41 ha |
| Sawit terpetakan 2024, area valid tahun tersebut | 6.602.708,10 ha |

Pada valid bersama, 3.323.829,60 ha berpindah dari kelas lain ke kelas sawit dan 27.939,18 ha berpindah dari sawit ke kelas lain. Formasi hutan → sawit mencakup 649.739,68 ha. Angka tersebut adalah hasil perbandingan kelas peta. Luas sawit tahunan memakai cakupan valid masing-masing sehingga selisihnya dapat berbeda dari perubahan bersih pada valid bersama.

| Transisi non-diagonal terbesar | Kode | Luas (ha) |
| --- | --- | ---: |
| Tumbuhan non-hutan lainnya → sawit | 13 → 35 | 1.391.682,42 |
| Formasi hutan → tumbuhan non-hutan lainnya | 3 → 13 | 1.381.955,38 |
| Tumbuhan non-hutan lainnya → formasi hutan | 13 → 3 | 1.041.882,08 |
| Formasi hutan → sawit | 3 → 35 | 649.739,68 |
| Hutan rawa gambut → tumbuhan non-hutan lainnya | 76 → 13 | 497.494,17 |

### Berkas hasil

- [Ringkasan perubahan](../outputs/tables/phase4/ringkasan_perubahan.csv) memuat 62 wilayah.
- [Luas kelas tahunan](../outputs/tables/phase4/luas_kelas.csv) memuat 1.612 baris, terdiri dari 13 kelas × 2 tahun × 62 wilayah.
- [Transisi kelas](../outputs/tables/phase4/transisi_kelas.csv) memuat 10.478 baris, terdiri dari 13 × 13 pasangan pada 62 wilayah.
- [Laporan rekonsiliasi](../data/metadata/phase4_qa.json) menyimpan luas dan selisih sebelum pembulatan.

### Hasil pemeriksaan

Tiga CSV dibaca ulang. Untuk seluruh 62 wilayah, jumlah luas tahunan sama dengan luas valid tahun tersebut, jumlah transisi sama dengan luas valid bersama, dan jumlah diagonal sama dengan luas stabil, masing-masing dalam toleransi 0,000001 ha. Setiap wilayah memiliki 26 baris tahunan dan 169 pasangan unik. Keempat luas AOI berbeda kurang dari 0,01 ha dari fase 2.

Penjumlahan 56 kabupaten/kota menghasilkan luas wilayah 6.839,51 ha lebih besar daripada reduksi AOI langsung, sekitar 0,0128% luas AOI. Luas berubah hasil penjumlahan juga lebih besar 1.058,13 ha. Selisih memenuhi toleransi antartingkat yang ditetapkan untuk audit ini. Statistik AOI diambil dari reduksi langsung. Statistik provinsi diturunkan dari kabupaten/kota. Selisih aktual dipertahankan untuk integrasi fase 5.

### Peta perubahan

[Proyek QGIS utama](../Kalimantan_Land_Cover_Explorer.qgz) memuat raster tinjauan dan tiga tabel pada grup fase 4. GeoTIFF lokal `data/processed/phase4_change_overview_300m.tif` tersusun dari 30 ubin setelah permintaan unduh penuh mencapai batas memori Earth Engine. Seluruh ubin diperiksa terhadap transformasi, dimensi dan CRS yang diharapkan. Jumlah piksel mosaik cocok dengan jumlah piksel ubin untuk keempat nilai 0, 1, 2 dan 255. Layer tersebut berhasil dibuka ulang melalui PyQGIS lokal.

Raster tinjauan memakai jarak grid 10 kali grid sumber, sekitar 300 m nominal. Fungsinya untuk eksplorasi peta. Angka tabel memakai reduksi grid asli sekitar 30 m. Untuk pekerjaan grid asli di Earth Engine gunakan skrip peta R1 dan parameter ekspor yang tercatat. Sintaks JavaScript diperiksa secara lokal dan tugas ekspor GeoTIFF grid asli tersedia untuk dijalankan di Code Editor.

Untuk membentuk ulang peta lokal, jalankan `scripts/analyze_phase4.py --map-only` untuk mengunduh ubin, lalu jalankan `scripts/assemble_phase4_qgis.py` di lingkungan QGIS dengan provider GDAL. Hasil setempat berada pada folder data yang diabaikan Git.
