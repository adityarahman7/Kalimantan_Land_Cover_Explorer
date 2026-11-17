# Roadmap

Semua tahap berikut merupakan target, kecuali yang secara eksplisit ditandai selesai.

Acuan cakupan dan penerimaan: [spesifikasi utama](project_specification.md). Tujuh fase berikut merupakan alur kerja, sedangkan R1–R3 merupakan tahap rilis. Perluasan rilis dapat mengulang audit, analisis, integrasi dan validasi.

| Fase | Deliverable | Kriteria selesai | Status |
| --- | --- | --- | --- |
| 1. Spesifikasi | Cakupan dan prioritas fitur | Definisi indikator dan versi pertama disepakati | Selesai sebagai baseline 2026-11-01; lihat spesifikasi utama |
| 2. Audit data | Inventaris, metadata, kamus kelas | Akses serta metadata 2010/2024 terverifikasi | Audit awal terdokumentasi 2026-11-01; lanjut penyiapan eksploratif dengan pertanyaan versi, akurasi, kelengkapan batas dan izin distribusi BIG tetap terbuka |
| 3. Penyiapan spasial | Paket batas, raster dan mask siap analisis | Batas, grid, kelas dan mask diperiksa pada cakupan pilot | Siap untuk R1 pada 2026-11-10. Lihat [paket fase 3](phase3_handoff.md) dan keterbatasan batas kerja |
| 4. Analisis | Luas kelas, transisi, layer perubahan | Luas dapat direkonsiliasi dan keterbatasan dicatat | R1 selesai 2026-11-11. Lihat [analisis fase 4](phase4_analysis.md) |
| 5. Layanan web | COG, GeoJSON, statistik per wilayah dan metadata | Paket dapat dimuat melalui HTTP dengan hasil uji terukur | Paket lokal R1 siap. Lihat [panduan data](phase5_data_service.md) |
| 6. Integrasi | WebGIS dengan data asli | Filter, peta, legenda, dan statistik konsisten | Integrasi lokal R1 selesai. Lihat [cara menjalankan WebGIS](../web/README.md) |
| 7. Validasi dan rilis | Aplikasi dan dokumentasi rilis | Angka, interaksi, performa, atribusi, serta tampilan diperiksa | Validasi lokal R1 selesai. Publikasi dan tinjauan izin distribusi masih terbuka. |

R1 telah divalidasi secara lokal. R2 memperluas aplikasi yang sama ke 15 tahun dan 105 pasangan. Lihat [pelaksanaan R2](r2_execution.md) untuk hasil pemeriksaan pada 17 November 2026.

## Urutan rilis yang disepakati

1. **R1 — Inti:** peta 2010/2024, filter wilayah, luas kelas, perubahan/transisi, legenda dan metadata. Seluruh Kalimantan tetap dicakup.
2. **R2 — Tahunan:** perluas WebGIS R1 yang ada ke 2010–2024, grafik tahunan, dan pasangan tahun. Lihat [rencana R2 dengan 7 fase dan 22 tahap](r2_plan.md).
3. **R3 — Lengkap:** animasi, pembanding geser, peringkat perubahan, informasi lokasi, dan modul sawit pendukung.

Setelah R1 tervalidasi, lanjutkan ke R2 dan R3. Fitur unduh CSV, unggah batas sendiri, dan riwayat kelas lengkap pada titik merupakan backlog tambahan setelah versi utama lengkap.
