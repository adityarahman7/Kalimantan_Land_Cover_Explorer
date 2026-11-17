# Rancangan metodologi

Dokumen ini memuat definisi kerja. Audit awal 1 November 2026 telah memakai pixelArea pada grid band 2010 dan aturan validitas di bawah; hasilnya tercatat pada inventaris/log. Rancangan produksi masih membutuhkan pemeriksaan batas, kelengkapan kode dan toleransi rekonsiliasi.

Acuan definisi produk dan indikator adalah [spesifikasi utama](project_specification.md). Dokumen ini merinci pelaksanaannya; perubahan definisi harus diselaraskan melalui log keputusan.

| Indikator | Definisi kerja |
| --- | --- |
| Luas kelas | Luas area valid dengan kelas tertentu pada tahun pilihan |
| Cakupan valid tahunan | Luas area valid tahun tersebut dibagi luas wilayah analisis; metode batas/luas harus konsisten |
| Area berubah | Area valid pada kedua tahun dengan kode kelas berbeda |
| Area stabil | Area valid pada kedua tahun dengan kode kelas sama |
| Area tidak dapat dibandingkan | Area yang tidak valid pada salah satu atau kedua tahun |
| Persentase berubah | Luas berubah / luas area valid pada kedua tahun × 100% |
| Transisi | Luas perpindahan kelas asal ke kelas tujuan |

## Aturan analisis

1. Gunakan satu versi koleksi dan batas administrasi untuk seluruh tahun.
2. Periksa kesamaan CRS, ukuran piksel, transformasi, dan alignment sebelum overlay.
3. Tetapkan mask valid dari hasil audit; jangan menyamakan nilai nol, NoData, dan kode tidak teramati tanpa bukti.
4. Pilih metode luas yang memperhitungkan luas piksel, lalu dokumentasikan satuan dan parameternya.
5. Rekonsiliasi luas kelas dengan luas valid; rekonsiliasi transisi dengan area valid bersama.
6. Bandingkan beberapa lokasi dengan citra referensi, dengan batas interpretasi yang jelas.

## Keterbatasan

Perubahan kode dapat dipengaruhi kesalahan klasifikasi. Perbandingan dua ujung tahun dapat melewatkan perubahan sementara. Hasil tidak dengan sendirinya menjelaskan penyebab perubahan. BIOPAMA diperlakukan sebagai produk statis pendukung; estimasi tahun tanam bukan bukti langsung tahun deforestasi.

## Belum diputuskan

Validasi produksi dan toleransi rekonsiliasi, kebutuhan resampling bila muncul grid berbeda, strategi pelayanan 105 pasangan tahun, serta penyelesaian versi/akurasi dan cakupan batas.

## Metode yang digunakan pada audit awal

- Band 2010/2024 memiliki CRS dan transformasi identik; audit mempertahankan grid tersebut. Transformasi lengkap tersimpan pada inventaris dan skrip.
- Kelas valid awal: `[3,5,9,13,21,24,25,30,31,33,35,40,76]`. Mask, kode 27 dan kode lain di luar daftar dikeluarkan; kategori penyebab invalid belum dipisahkan menyeluruh.
- Luas memakai `ee.Image.pixelArea() / 10000`, clip ke koleksi batas, dan penjumlahan pada grid acuan dengan region kotak sederhana. Seluruh hasil mengikuti batas kerja 56 fitur.
- Luas valid bersama adalah irisan validitas dua tahun. Wilayah dikurangi valid bersama dilaporkan sebagai area tidak dapat dibandingkan; tidak diasumsikan stabil atau diisi kelas lain.
- Tingginya cakupan valid bukan ukuran akurasi; pemeriksaan sampel tidak membuktikan tidak adanya kelas lain. Lihat [inventaris](data_inventory.md) dan [log](processing_log.md) untuk parameter, bukti dan keterbatasan.
