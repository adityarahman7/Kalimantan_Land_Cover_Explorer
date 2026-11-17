# Kalimantan Land Cover Explorer

**[Buka dashboard publik](https://adityarahman7.github.io/Kalimantan_Land_Cover_Explorer/)** · [Panduan publikasi GitHub Pages](docs/github_pages.md). Website diterbitkan dari cabang `gh-pages`; kode proyek berada di `main`.

WebGIS untuk mengeksplorasi tutupan lahan dan perubahannya di seluruh Kalimantan wilayah Indonesia. Proyek ini dikembangkan sebagai portofolio GIS Developer, mulai dari audit data raster, analisis perubahan, hingga penyajian hasil melalui aplikasi web.

> **Status R2 tersedia secara lokal.** [Jalankan WebGIS](web/README.md) untuk menjelajahi peta dan grafik 2010–2024 serta perbandingan 105 pasangan tahun. [Laporan R2](docs/r2_execution.md) dan [Current State](Current_State.md) mencatat hasil validasi dan keterbatasannya.

**Spesifikasi utama:** [tujuan, cakupan, fitur, dan kriteria penerimaan](docs/project_specification.md). Fase 1 selesai sebagai baseline perencanaan pada 1 November 2026. Pengembangan dimulai dari **R1 versi inti (2010/2024)**, dilanjutkan **R2 seluruh tahun 2010–2024**, kemudian **R3 versi lengkap**. Rilis inti merupakan langkah pertama menuju target lengkap; R1 dan R2 tersedia secara lokal. R3 masih direncanakan.

## Pertanyaan proyek

- Bagaimana luas dan persebaran kelas tutupan lahan berubah setiap tahun?
- Di mana perubahan terjadi, dan kelas apa yang berubah menjadi kelas lain?
- Bagaimana perkembangan kelas sawit tahunan dan riwayat tutupan lahannya?

## Cakupan

| Komponen | Rencana |
| --- | --- |
| Wilayah | Kalimantan Barat, Tengah, Selatan, Timur, dan Utara |
| Periode kerja | 2010–2024 tersedia pada R2; sumber menyediakan band 1990–2024 |
| Interval | Tahunan |
| Uji awal | Tahun 2010 dan 2024, tetap mencakup seluruh Kalimantan Indonesia |
| Unit ringkasan | Seluruh wilayah, provinsi, dan kabupaten/kota |

## Sumber data dan status verifikasi

| Sumber | Peran | Status |
| --- | --- | --- |
| MapBiomas Indonesia | Sumber kerja sementara untuk penyiapan eksploratif | Akses, grid dan data 2010–2024 diperiksa pada R2. Versi internal v2 pada direktori collection4; identitas 4.1 dan akurasi sesuai belum pasti |
| BIOPAMA Global Oil Palm v1.2 | Pelengkap statis tipe perkebunan dan estimasi tahun tanam | Belum diintegrasikan; bukan seri tahunan 2010–2024 |
| Batas administrasi | Pembatas wilayah dan agregasi statistik | Berkas sumber BIG BATASWILAYAH_KABKOTA_20260601.gdb menurut pengguna; batas kerja 56 fitur. Satu fitur pulau dihapus; kelengkapan serta izin distribusi belum dipastikan |

Catatan sumber dan daftar pemeriksaan tersedia pada [inventaris data](docs/data_inventory.md). Lisensi data mengikuti ketentuan masing-masing penyedia.

Hasil audit tersimpan pada [skrip Earth Engine](scripts/earth_engine/01_audit_data.js), [CSV cakupan valid](data/metadata/audit_cakupan_valid_2010_2024.csv), dan [CSV tiga titik pemeriksaan](data/metadata/contoh_lokasi_tidak_valid.csv). Cakupan valid bersama sekitar 99,982994% pada batas kerja; angka ini bukan akurasi klasifikasi. Input, parameter, galat dan batas verifikasi dicatat pada [log pengolahan](docs/processing_log.md).

## Alur kerja

**Audit data → penyiapan spasial → analisis → layanan data web → integrasi UI → validasi dan rilis.**

Analisis luas dan penyiapan data dijalankan di luar browser. Aplikasi lokal menggunakan Canvas untuk menampilkan grid yang telah disiapkan.

## Struktur repositori

```text
.
├── .github/                 # Panduan kontribusi dan template issue/PR
├── config/                  # Konfigurasi contoh tanpa rahasia
├── data/
│   ├── raw/                 # Data asli lokal, diabaikan Git
│   ├── interim/             # Data antara lokal, diabaikan Git
│   ├── processed/           # Data siap analisis lokal, diabaikan Git
│   ├── samples/             # Sampel kecil yang boleh dibagikan
│   └── metadata/            # Provenance dan catatan dataset
├── docs/                    # Metode, inventaris, roadmap, keputusan
├── notebooks/               # Eksplorasi dan audit bertahap
├── scripts/
│   └── earth_engine/        # Skrip audit/ekspor Earth Engine
├── src/
│   └── kalimantan_lc/       # Tempat modul Python yang dapat digunakan ulang
├── tests/                   # Tempat pengujian logika saat diimplementasikan
├── outputs/
│   ├── figures/             # Gambar terpilih untuk dokumentasi
│   ├── tables/              # Tabel ringkas terpilih
│   └── reports/             # Laporan terpilih
├── web/                     # Aplikasi WebGIS R2 lokal
├── Current_State.md         # Status kerja terbaru
└── README.md
```

Folder dengan `.gitkeep` sengaja disiapkan agar ikut tersimpan dalam Git meskipun belum berisi pekerjaan. Folder tersebut tidak menandakan bahwa tahapnya sudah selesai.

## Memulai

**Catatan clone cabang `main`:** data produksi dan paket WebGIS `web/public/data/r1/` serta `r2/` tidak disertakan pada cabang ini. Menjalankan server saja pada clone `main` belum cukup untuk menampilkan dashboard; siapkan kembali paket data sesuai [panduan WebGIS](web/README.md). Cabang `gh-pages` menyertakan paket tampilan R2 dan dapat langsung disajikan sebagai website statis.

Panduan fungsi setiap berkas tersedia di [panduan struktur proyek](docs/project_structure.md).

1. Baca [Current_State.md](Current_State.md) dan [roadmap](docs/roadmap.md).
2. Catat akses, versi, periode, kelas, grid, mask, serta ketentuan penggunaan dataset pada inventaris.
3. Gunakan `config/project.example.json` sebagai referensi konfigurasi. Salinan lokal `config/project.local.json` diabaikan Git.
4. Simpan data asli di `data/raw/`; jangan mengubah berkas sumber. Catat transformasi pada log pengolahan.
5. Jalankan satu checkpoint audit sebelum berpindah ke langkah berikutnya.

[Panduan WebGIS](web/README.md) memuat perintah untuk menjalankan aplikasi lokal. Skrip audit dijalankan di Earth Engine Code Editor sesuai [panduan skrip](scripts/README.md).

## Prinsip analisis dan keterbatasan

- Gunakan satu koleksi klasifikasi dan satu versi batas administrasi untuk seluruh periode.
- Pisahkan area stabil, area berubah, dan area yang tidak dapat dibandingkan.
- Hitung luas dengan metode yang mempertimbangkan luas piksel; jangan mengasumsikan semua piksel geografis memiliki luas sama.
- Perbedaan kelas antartahun belum otomatis menunjukkan perubahan nyata atau membuktikan penyebabnya.
- Pemeriksaan visual beberapa lokasi bukan estimasi akurasi yang mewakili seluruh Kalimantan.
- Estimasi tahun tanam sawit tidak otomatis menunjukkan tahun deforestasi.

Definisi indikator tersedia pada [metodologi](docs/methodology.md).

## Prototipe

[Preview UI](https://kalimantan-landcover-aditya.fairymyna66.chatgpt.site) dilaporkan tersedia secara privat dalam handover. Tautan dapat memerlukan login; akses dan tampilan belum diperiksa ulang dalam sesi penyiapan repositori. Aplikasi fase 6 di [folder web](web/) adalah implementasi lokal terpisah.

## Kontribusi dan publikasi

Lihat [panduan kontribusi](.github/CONTRIBUTING.md) dan [checklist publikasi](docs/github_checklist.md). Jangan mengunggah token, kredensial akun, data berlisensi terbatas, atau raster produksi berukuran besar. GitHub digunakan untuk kode, dokumentasi, metadata, dan artefak kecil yang telah diperiksa.

Lisensi kode belum dipilih. Sebelum penggunaan ulang atau distribusi kode, periksa keputusan lisensi yang akan ditambahkan pemilik proyek. Ketentuan data tetap terpisah dari lisensi kode.

## Referensi awal

- [MapBiomas: akses Earth Engine](https://landy.mapbiomas.id/en/gee)
- [MapBiomas: alamat aset](https://landy.mapbiomas.id/en/landsatmosaics)
- [MapBiomas: unduhan koleksi](https://landy.mapbiomas.id/en/collectionmap)
- [MapBiomas: legenda](https://landy.mapbiomas.id/en/legendcode)
- [MapBiomas: ketentuan penggunaan](https://landy.mapbiomas.id/en/termsofuse)
- [BIOPAMA Global Oil Palm v1.2](https://developers.google.com/earth-engine/datasets/catalog/BIOPAMA_GlobalOilPalm_v1_2)

Referensi akses/aset/unduhan diperiksa pada 26 Oktober 2026. Legenda, ketentuan penggunaan, halaman akurasi dan bagian relevan ATBD diperiksa pada audit 1 November 2026. Identitas Koleksi 4.1 belum terhubung secara pasti ke aset kerja; BIOPAMA masih rujukan handover yang belum diaudit.
