# WebGIS R2 lokal

Revisi terbaru memakai tema hijau gelap dan teks lebih besar. Gulir di peta untuk zoom langsung; geser untuk pan. Basemap daratan/laut Natural Earth dibundel lokal sebagai konteks regional. Rincian kelas diurutkan persentase terbesar → terkecil. Satuan awal km² dapat diganti menjadi ha melalui pemilih di header; sumber tetap ha. Grafik area/garis menyediakan nilai awal–akhir dan selisih luas kelas. [Catatan revisi dan QA](../docs/ui_refresh_2026_11_17.md).

Layout dashboard diperbarui mengikuti referensi ArcGIS pengguna dengan palet hijau yang sama: filter atas, indikator kiri, peta tengah, rincian kanan dan grafik bawah. **Atur ulang** memulihkan seluruh pilihan. **Tentang data** membuka informasi sumber; Escape menutupnya. Pada ponsel, panel disusun vertikal dengan peta lebih dahulu. [Catatan UI dan pemeriksaan](../docs/ui_refresh_2026_11_17.md).

WebGIS menampilkan data MapBiomas 2010–2024 pada cakupan kerja 56 kabupaten/kota, lima provinsi dan satu AOI Kalimantan Indonesia. Jalankan dari akar proyek dengan Python 3.

```powershell
python -m http.server 8766 --bind 127.0.0.1 --directory web
```

Buka [WebGIS lokal](http://127.0.0.1:8766/). Pilih wilayah dan tahun untuk menampilkan peta, luas kelas, serta cakupan validnya. Pilih kelas pada grafik untuk melihat luas selama 15 tahun. Titik grafik bisa diklik atau diaktifkan dengan keyboard untuk memilih peta tahun tersebut.

Mode perubahan menyediakan tahun awal dan akhir dengan aturan awal lebih kecil dari akhir. Semua 105 pasangan didukung. Filter kelas asal dan tujuan mengikuti pasangan serta wilayah yang dipilih.

## Input, proses, dan output

| Input | Proses | Output |
| --- | --- | --- |
| Manifest dan batas tampilan fase 5 | Hubungkan ID wilayah dan potong peta sesuai batas pilihan | Peta AOI, provinsi, atau kabupaten/kota |
| 15 raster tahunan | Muat tahun yang dibutuhkan dan susun pasangan kelas di browser | Peta tahunan, stabil/berubah/tidak dapat dibandingkan, dan filter transisi |
| Statistik 62 wilayah pada grid sumber | Ambil JSON wilayah, lalu pilih tahun atau matriks pasangan | Grafik tahunan, tabel luas, cakupan valid, dan statistik transisi |

Paket berada di `public/data/r2/` dan diabaikan Git. Manifest menunjuk berkas pada subfolder versi data. Browser menyimpan paling banyak empat raster tahunan dalam cache memori. Paket R1 dan laporan validasinya tetap tersedia sebagai acuan. Pemuat aplikasi memakai R1 bila manifest R2 menghasilkan HTTP 404 dan menandai bahwa hanya dua tahun pengamatan tersedia.

## Membuat ulang paket

Gunakan lingkungan Earth Engine proyek yang sudah tersedia dan akun dengan akses aset yang tercatat pada konfigurasi. Jalankan tahap berikut dari akar proyek.

```powershell
$env:PYTHONPATH = (Resolve-Path '.venv/phase3-ee').Path
python scripts/analyze_r2.py --sample-classes --workers 4
python scripts/download_r2.py
```

Skrip analisis menyimpan cache terpisah untuk setiap pasangan dan tingkat wilayah. Jalankan ulang perintah untuk melanjutkan hasil yang belum lengkap. Perubahan metadata aset atau konfigurasi menghasilkan kunci cache baru.

Pengemasan memerlukan Python dengan GDAL dan NumPy. Pada komputer proyek, gunakan Python bawaan QGIS.

```powershell
& 'C:/Program Files/QGIS 3.44.15/bin/python-qgis-ltr.bat' scripts/package_r2.py
python scripts/validate_r2.py
```

Manifest diperbarui setelah seluruh hasil tersedia dan lolos pemeriksaan. Aturan kelas valid, NoData dan mask mengikuti R1. Nilai nol pada raster tahunan adalah data invalid. Nilai 255 menandai luar AOI. Raster disimpan sebagai byte UInt8 dalam gzip dan dibaca dengan `DecompressionStream`.

## Hasil validasi

[Laporan R2](../docs/r2_execution.md) menjelaskan checkpoint dan bukti pemeriksaan. Validator data memeriksa seluruh 15 tahun, 62 wilayah dan 105 pasangan serta regresi terhadap tabel R1. Uji browser mencakup 15 pilihan tahun, grafik, contoh pasangan tahun, filter, pergantian wilayah, keadaan galat dan empat lebar layar. [Cara menjalankan uji](../tests/README.md).

Peta memakai grid tampilan sekitar 300 m dan batas yang disederhanakan. Angka luas memakai analisis sekitar 30 m. Detail transisi kecil dapat tercatat pada tabel tanpa terlihat pada grid tampilan. Kesiapan publikasi tetap memerlukan tinjauan atribusi, identitas koleksi dan izin distribusi batas.

