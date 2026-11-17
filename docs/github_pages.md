# Publikasi GitHub Pages

URL dashboard: https://adityarahman7.github.io/Kalimantan_Land_Cover_Explorer/

- `main`: kode, dokumentasi, dan metadata proyek.
- `gh-pages`: isi dashboard dari folder `web`, dengan `index.html` di akar, `.nojekyll`, basemap, serta paket R2 yang dirujuk manifest.
- Pengaturan Pages: **Deploy from a branch → gh-pages → / (root)**.
- Bangun paket dengan `node scripts/build_github_pages.mjs`. Skrip memeriksa 15 tahun, 62 wilayah, ukuran dan kode raster, serta ID statistik. Output `.pages-build/` diabaikan Git.
- Untuk memperbarui website, jalankan skrip, commit isi `.pages-build/` ke cabang `gh-pages`, push, lalu tunggu build Pages. Push `main` saja tidak memperbarui website.

Paket publikasi hanya memuat peta sekitar 300 m, batas yang disederhanakan, dan statistik. Raster analisis asli, kredensial, dan lingkungan lokal tidak disertakan. Atribusi serta keterbatasan dipertahankan dalam panel **Tentang data** dan `SOURCE.md`. Publikasi teknis tidak membuktikan akurasi klasifikasi, kelengkapan batas, atau kepastian ketentuan distribusi sumber.

## Verifikasi 17 November 2026

Build GitHub Actions `44123704181` selesai dengan status `success`, memakai commit `0f1f198` dari `gh-pages`. Halaman publik di Chrome berhasil memuat dashboard, raster dan statistik R2, 15 pilihan tahun dan grafik. Pemeriksaan representatif mencakup 2016, wilayah Sambas, perubahan 2014–2021 dengan filter Formasi hutan → Sawit (25,15 km²; 0,42%), satuan km²/ha, dan atur ulang. Tidak ada galat pada log browser yang diperiksa. Ini bukan uji seluruh kombinasi atau seluruh browser/perangkat. Cuplikan: `outputs/ui/github-pages-public.png`.
