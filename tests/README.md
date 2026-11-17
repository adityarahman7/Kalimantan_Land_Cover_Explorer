# Pengujian R2

Jalankan `python scripts/validate_r2.py` dari akar proyek setelah paket R2 dibuat. Pemeriksaan ini mencakup seluruh wilayah, luas tahunan, matriks semua pasangan, neraca luas, kode raster, dan regresi terhadap CSV R1. Toleransi rekonsiliasi adalah 0,01 ha.

`r2_browser.cjs` menguji aplikasi dengan Edge dan Chrome melalui Playwright. Jalankan dengan Node.js, alamat modul Playwright yang tersedia di komputer, dan alamat Python 3.

```text
node tests/r2_browser.cjs <alamat-modul-playwright> <alamat-python>
```

Skrip menjalankan server pada 127.0.0.1 port 8767 dan menghentikannya setelah uji. Dua alamat browser Windows tercantum di skrip. Uji meliputi seluruh 15 pilihan tahun, nilai tabel tahunan, 15 titik grafik, pilihan tahun melalui grafik, contoh pasangan tahun, filter kelas, pergantian wilayah, respons terlambat, HTTP 404 dan coba ulang, serta empat lebar layar.

Tangkapan layar pemeriksaan disimpan di `data/interim/r2/qa/`. Hasil uji fungsional dipisahkan dari penilaian akurasi klasifikasi dan kelengkapan batas.
