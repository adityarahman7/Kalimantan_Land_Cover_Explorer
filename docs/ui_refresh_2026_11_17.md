# Pembaruan UI lokal — 17 November 2026

## Revisi gelap, konteks peta, dan satuan luas

Atas instruksi terbaru pengguna, tema kini hijau gelap dengan teks utama/formulir lebih besar. Layout dashboard tetap dipertahankan. Untuk layar desktop pendek, halaman dapat digulir agar peta dan teks tidak dipadatkan berlebihan.

Zoom roda gulir sekarang langsung aktif tanpa Ctrl, berpusat pada posisi kursor, memakai delta kontinu dengan batas zoom. Indikator perbesaran relatif terhadap tampilan pas wilayah ditampilkan di peta. Basemap konteks daratan/lautan menggunakan Natural Earth `ne_10m_land` (skala 1:10 juta, bukan resolusi 10 meter), dipotong pada 85°–145° BT dan 20° LS–25° LU serta disederhanakan 0,002°. Sumber: [Natural Earth Physical Vectors](https://www.naturalearthdata.com/downloads/10m-physical-vectors/), [ketentuan public domain](https://www.naturalearthdata.com/about/terms-of-use/). Detail provenance tersedia di `web/public/context/source.json`; pembuatan paket melalui `scripts/package_context_basemap.py`. Basemap dibundel lokal (~998 KB) dan tidak dipakai sebagai input analisis atau acuan batas rinci. Jika gagal dimuat, peta tematik tetap bekerja dan footer menyatakan kegagalannya.

Rincian kelas dan bar komposisi diurutkan ascending dengan penyebut persentase yang sama. Kategori yang tidak memiliki persentase (tidak dapat dibandingkan) diletakkan terakhir. Pengurutan tidak mengubah urutan matriks atau array sumber.

Satuan tampilan bawaan km², dengan pemilih ha. Data sumber tetap ha; pembagi tampilan km² adalah 100. Pemilih satuan memperbarui kartu, rincian kelas, sumbu/titik/tabel grafik, dan ringkasan selisih kelas. Proporsi tidak berubah. Grafik berupa garis linear antartitik dengan area gradien menuju nol, titik aktif lebih jelas, serta nilai awal/akhir dan perubahan luas kelas; angka selisih ini bukan luas transisi kelas.

Pemeriksaan revisi di Chrome: seluruh 15 tahun masing-masing 13 kelas terurut; zoom gulir tanpa Ctrl mengubah indikator 1× → 1,6×; Natural Earth berhasil dimuat; perubahan 2010–2024 sebesar 104.748,04 km²; transisi hutan → sawit 6.497,4 km² atau 649.739,68 ha dengan proporsi 1,22% tetap sama; grafik kelas hutan menampilkan selisih −12.898,36 km² dan titik 2016 memperbarui peta. Nilai konversi 10.474.804,21 ha → 104.748,04 km² diuji melalui Node, dan sintaks modul diperiksa. Skrip uji browser lama disesuaikan untuk satuan bawaan baru serta urutan kelas; suite otomatis penuh tidak dijalankan dalam revisi ini.

Desktop CSS 1518×1000 tidak memiliki overflow halaman. Ponsel CSS 356 dan 434 diperiksa tanpa overflow horizontal. Ini bukan pengujian perangkat fisik, seluruh kombinasi, lintas browser, atau validasi akurasi data. Cuplikan: `outputs/ui/dashboard-dark-desktop.jpg` dan `outputs/ui/dashboard-dark-mobile.jpg`. Berikutnya: tinjau pengalaman tampilan bersama pengguna; publikasi tetap terpisah.

## Revisi dashboard berdasarkan referensi pengguna

Revisi terbaru menggantikan susunan halaman panjang di bawah ini. Sumber visual yang dibuka: [California Statewide Power Outages (Public View), ArcGIS Dashboards](https://www.arcgis.com/apps/dashboards/7edefc1970d44b839ebbfd7b45e51e2d). Diadaptasi susunan panel filter atas, indikator kiri, peta tengah, rincian kanan, dan grafik bawah. Pengguna secara eksplisit meminta palet hijau/latar terang yang telah ada.

Desktop mengisi viewport dengan scroll mandiri pada rincian dan legenda. Layar pendek/tablet memakai susunan yang dapat digulir; ponsel mengutamakan peta lalu ringkasan, grafik, dan rincian. Ditambahkan bar proporsi dari statistik aktif, atur ulang seluruh filter, dan panel sumber yang ditutup melalui summary atau Escape. Grafik menyesuaikan lebar kontainer. URL aset diberi versi untuk menghindari modul tampilan lama dari cache browser.

QA revisi: sintaks modul aplikasi/grafik; seluruh 15 pilihan tahun masing-masing memuat 13 baris kelas; Sambas; Formasi hutan → Sawit; pasangan 2014–2021; titik grafik 2016; atur ulang ke seluruh Kalimantan/2024; panel sumber dan Escape. Ukuran CSS Chrome 1707×710 dan 1518×1000 tidak memiliki overflow halaman. Lebar CSS 356, 434, 853 tanpa overflow horizontal. Skala browser membuat ukuran CSS berbeda dari override; ini bukan uji perangkat fisik. Log akhir yang dibaca memuat galat ekstensi Zotero, tanpa galat aplikasi. Edge/Firefox/Safari untuk layout ini belum diuji.

Cuplikan: `outputs/ui/dashboard-reference-desktop.jpg` dan `outputs/ui/dashboard-reference-mobile.jpg`. Paket dan aturan analisis tidak diubah. Langkah berikutnya: penilaian audiens dan QA lintas browser. Tidak ada deployment dalam revisi ini.

Tujuan: membantu audiens umum memilih wilayah, membaca peta, dan memahami statistik tanpa harus mengetahui struktur paket data atau urutan fase proyek.

## Keputusan desain

- Latar terang, warna hijau hutan, ruang kosong, dan panel yang konsisten. Warna kelas peta tetap dari manifest.
- Navigasi utama untuk eksplorasi dan informasi data. Pengaturan dikelompokkan menjadi wilayah dan tampilan/waktu.
- Peta tetap menjadi fokus. Tombol pas wilayah, zum, arah utara, dan petunjuk geser tersedia di sekitar peta.
- Ringkasan wilayah mendahului grafik dan tabel. Kalimat ringkasan dihitung dari statistik aktif; klaim perubahan tidak disamakan dengan deforestasi atau penyebab perubahan.
- Grafik tetap interaktif lewat tetikus dan papan ketik. Pada layar kecil grafik dapat digulir secara horizontal agar label tetap terbaca.
- Sumber dan keterbatasan dapat dibuka tanpa meninggalkan aplikasi. Mode reduced motion dan tautan langsung ke peta tersedia.

## Data yang benar-benar ditampilkan

Pada awal pemeriksaan, manifest R2 belum tersedia. Percobaan menjalankan pengemas yang sudah ada berhenti pada pemeriksaan konsistensi luas (`62`, `2010`); aturan analisis tidak diubah dalam pekerjaan UI. UI kemudian diuji menggunakan paket R1 asli melalui adapter dua tahun. Jika R2 tidak ada, tahun antara 2010 dan 2024 tidak diisi atau disimulasikan.

Pada akhir sesi, paket R2 tersedia melalui pembaruan di workspace. Memuat ulang aplikasi menampilkan data tahunan 2010–2024. Pekerjaan UI ini tidak mengklaim memperbaiki atau memvalidasi metodologi pengemasan R2. Pembacaan R2 menggunakan modul data proyek yang sudah ada.

## Pemeriksaan yang dijalankan

- Pemeriksaan sintaks JavaScript untuk modul aplikasi, grafik, peta dan pemilihan paket data.
- Chrome lokal: peta dan statistik awal; panah tahun R1 2024 → 2010; 13 baris kelas; perubahan R1 2010–2024 sebesar 10.474.804,21 ha; transisi Formasi hutan → Sawit sebesar 649.739,68 ha; pemilihan Kalimantan Barat dan Sambas.
- Setelah R2 tersedia: 15 pilihan tahun, 15 titik grafik, tahun 2010/2011/2016/2024 dan pasangan 2014–2021. Grafik titik 2016 mengubah tahun dan label peta. Tautan sumber membuka panel metadata.
- Tidak ditemukan gulir horizontal halaman pada ukuran CSS teramati 356, 434, dan 853 piksel. Ukuran override browser 320/390/768 berbeda dari ukuran CSS aktual karena skala browser; hasil ini bukan pengujian perangkat fisik.
- Log akhir Chrome memuat galat ekstensi Zotero; tidak ditemukan galat aplikasi pada log yang dibaca. QA ini tidak menggantikan pengujian semua kombinasi filter, simulasi jaringan gagal, atau pemeriksaan lintas browser.
- Cuplikan halaman desktop dan ponsel: `outputs/ui/desktop.jpg` dan `outputs/ui/mobile.jpg`.

## Langkah berikutnya

Tinjau pengalaman dengan audiens sasaran, termasuk ukuran teks dan pemahaman istilah kelas. Lanjutkan validasi analisis R2 pada alur data proyek dan pemeriksaan izin distribusi sebelum publikasi. Pembaruan UI disimpan lokal; tidak ada deployment dalam sesi ini.

## Koreksi urutan detail

Pengguna mengoreksi urutan menjadi persentase terbesar → terkecil (descending). Comparator rincian dan bar komposisi serta label UI diubah; kategori tanpa persentase tetap terakhir. Catatan ascending di atas merupakan riwayat pemeriksaan revisi sebelumnya.

