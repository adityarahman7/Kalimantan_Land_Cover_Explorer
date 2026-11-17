# Validasi lokal WebGIS R1

Diuji pada 11 November 2026. Cakupan uji meliputi paket data fase 5, keluaran analisis fase 4, serta aplikasi fase 6 yang disajikan melalui server lokal.

| Kriteria | Bukti |
| --- | --- |
| C01 · Peta tahunan | Tahun awal 2024 menampilkan 13 kelas pada tabel. Pemilihan 2010 mengubah label dan raster. Warna formasi hutan diperiksa pada piksel kanvas. |
| C02 · Wilayah | ID semua 62 wilayah cocok dengan GeoJSON pada tiga tingkat. Uji browser mencakup seluruh Kalimantan, pemilihan provinsi dan Sambas, pembatasan daftar kabupaten/kota, serta kembali ke seluruh Kalimantan. |
| C03 · Luas tahunan | Sebanyak 1.612 baris luas kelas dan penyebut area valid cocok dengan CSV fase 4. Proporsi tahunan ditampilkan terhadap area valid tahun terpilih. |
| C04 · Perubahan | Seluruh 13.491.162 nilai raster web sama dengan COG. Dekode menjadi stabil, berubah, tidak dapat dibandingkan, dan luar AOI cocok piksel demi piksel dengan raster perubahan fase 4. Sebanyak 62 ringkasan cocok dengan CSV. Angka AOI pada aplikasi adalah 10.474.804,21 ha berubah kelas atau 19,61% dari area valid bersama. |
| C05 · Filter transisi | Sebanyak 10.478 nilai matriks dan penyebut valid bersama cocok dengan CSV. Uji browser mencakup filter asal saja, Formasi hutan → Sawit (649.739,68 ha), kombinasi nol di Sambas, dan pemulihan peta setelah kedua filter dikosongkan. |
| C06 · Legenda dan metadata | Legenda merespons mode dan filter. Panel metadata dapat dibuka dan mencantumkan sumber, tanggal akses, metode luas dan keterbatasan versi serta batas. |
| C07 · Status aplikasi | Selama respons wilayah ditahan, tabel lama disembunyikan. Respons provinsi yang datang setelah statistik kabupaten tidak menimpa tampilan. Simulasi HTTP 404 pada statistik dan raster menampilkan galat serta tombol Coba lagi, yang berhasil memulihkan tampilan. |

Uji browser otomatis lulus pada Edge 157.0.4341.42 dan Chrome 157.0.8103.50. Lebar viewport 320, 390, 768, dan 1.366 px tidak menimbulkan gulir horizontal pada halaman. Kedua browser memakai Chromium. Safari, Firefox, perangkat fisik, pembaca layar dan performa hosting belum diuji.

## Pekerjaan lanjutan

- Grafik perbandingan 2010/2024 dan diagram aliran transisi masuk pekerjaan desain berikutnya. Validasi lokal ini menguji baseline peta dan tabel.
- Ketentuan distribusi BIG dan atribusi final perlu ditinjau sebelum rilis. Kecocokan paket dengan keluaran fase 4 mengukur konsistensi penyajian data. Akurasi klasifikasi dan kelengkapan batas tetap pertanyaan terpisah.
