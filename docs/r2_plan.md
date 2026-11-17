# Rencana R2 — WebGIS tahunan 2010–2024

R2 memperluas aplikasi WebGIS R1 yang telah divalidasi secara lokal. Gunakan folder `web/` yang sama dan pertahankan alur R1 sebagai acuan uji. Tambahkan 13 tahun di antara 2010 dan 2024 setelah data siap. Peta dan statistik memakai batas kerja serta ID wilayah R1 selama audit menyatakan keduanya tetap sesuai. Pengembangan dan validasi dilakukan secara lokal. Publikasi merupakan pekerjaan terpisah.

| Fase | Tahap | Pekerjaan |
| --- | ---: | --- |
| 1. Spesifikasi R2 | 2 | (1) Kunci cakupan fitur inti. (2) Tetapkan kriteria penerimaan peta, grafik, dan perbandingan. |
| 2. Audit data tahunan | 3 | (1) Tinjau pemeriksaan grid 15 band. (2) Audit kode kelas dan cakupan valid per tahun, terutama 13 tahun tambahan. (3) Catat anomali dan tindak lanjutnya. |
| 3. Penyiapan spasial | 3 | (1) Gunakan batas dan ID wilayah R1. (2) Siapkan raster tahunan dengan grid dan aturan mask konsisten. (3) Periksa hasil pada beberapa tahun dan wilayah. |
| 4. Analisis tahunan dan transisi | 4 | (1) Hitung luas kelas per tahun dan wilayah. (2) Hitung cakupan valid tahunan. (3) Uji transisi untuk pasangan berurutan dan berjeda panjang. (4) Cocokkan kembali pasangan 2010 → 2024 dengan R1. |
| 5. Paket data WebGIS | 3 | (1) Ukur ukuran dan waktu muat paket contoh. (2) Pilih strategi penyajian 105 pasangan tahun berdasarkan hasil uji. (3) Bangun dan uji paket lokal. |
| 6. Integrasi WebGIS | 4 | (1) Hubungkan paket R2 dan pilihan 15 tahun ke aplikasi yang ada. (2) Tambahkan grafik luas tahunan berdasarkan kelas dan wilayah. (3) Tambahkan pemilih tahun awal dan akhir. (4) Sinkronkan peta, legenda, tabel, dan filter transisi. |
| 7. Validasi lokal R2 | 3 | (1) Cocokkan hasil aplikasi dengan keluaran analisis. (2) Uji pilihan pengguna, galat pemuatan, dan beberapa lebar layar. (3) Catat hasil dan keterbatasan. |
| **Total** | **22** | |

R2 selesai secara lokal ketika 15 tahun dapat dipilih, grafik sesuai dengan statistik wilayah, dan aplikasi mendukung 105 pasangan dengan tahun awal lebih kecil dari tahun akhir. Statistik tahunan memakai area valid tahun terpilih. Statistik transisi memakai area yang valid pada kedua tahun pilihan.

Status 17 November 2026. R2 selesai secara lokal. Hasil dan checkpoint tersedia pada [laporan pelaksanaan](r2_execution.md).

Rujukan: [Spesifikasi proyek](project_specification.md), [roadmap](roadmap.md), dan [hasil validasi R1](phase6_validation.md).
