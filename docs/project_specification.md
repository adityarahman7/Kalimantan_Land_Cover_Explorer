# Spesifikasi Proyek — Kalimantan Land Cover Explorer

Tanggal: 1 November 2026  
Status: baseline fase 1; cakupan versi inti disepakati pengguna, dilanjutkan sampai versi lengkap.  
Implementasi: belum tersedia; kriteria di bawah merupakan target yang harus diuji.

## 1. Kedudukan dokumen

Dokumen ini menjadi acuan utama tujuan, cakupan, prioritas fitur, perilaku aplikasi, dan kriteria penerimaan. README merangkum dan menautkannya. Metodologi menjelaskan cara analisis; inventaris menyimpan bukti audit; log keputusan mencatat alasan perubahan; roadmap mengatur urutan; Current_State mencatat progres.

Spesifikasi adalah kesepakatan pekerjaan, bukan bukti bahwa data dapat diakses atau fitur sudah berfungsi. Perubahan cakupan yang material harus dibahas dengan pengguna, dicatat pada log keputusan, lalu diperbarui di sini.

## 2. Tujuan dan pengguna

Membangun WebGIS untuk mengeksplorasi persebaran tutupan lahan dan perubahannya di seluruh Kalimantan Indonesia. Proyek juga mendokumentasikan kemampuan pengolahan raster, analisis spasial, penyediaan data web, dan komunikasi hasil sebagai portofolio GIS Developer.

Pengguna sasaran awal adalah pembaca portofolio dan pengguna yang ingin meninjau tutupan lahan pada tingkat wilayah. Aplikasi mendukung eksplorasi, bukan penetapan hak lahan atau pembuktian penyebab perubahan.

Pertanyaan utama:

1. Bagaimana luas dan persebaran kelas berubah antartahun?
2. Di mana perubahan terjadi dan dari kelas apa menjadi kelas apa?
3. Bagaimana perkembangan kelas sawit tahunan dan riwayat tutupan lahannya?

## 3. Cakupan tetap dan sumber kandidat

| Komponen | Kesepakatan |
| --- | --- |
| Wilayah | Seluruh Kalimantan Indonesia: Barat, Tengah, Selatan, Timur, dan Utara; tidak mencakup Malaysia/Brunei |
| Target waktu akhir | Tahunan 2010–2024, tidak diperpanjang tanpa verifikasi dan pembahasan |
| Rilis inti | Tahun 2010 dan 2024 beserta perbandingan arah waktu 2010 → 2024 |
| Unit pilihan wilayah | Seluruh Kalimantan, provinsi, dan kabupaten/kota |
| Klasifikasi utama | MapBiomas sebagai kandidat; koleksi, akses, band, dan legenda harus lolos audit |
| Pelengkap sawit | BIOPAMA sebagai produk statis pendukung, diintegrasikan pada pengembangan lengkap |
| Batas administrasi | Satu sumber/versi konsisten untuk seluruh tahun; pilihan sumber ditentukan melalui audit |
| Bahasa antarmuka awal | Bahasa Indonesia |

Pada audit awal 1 November 2026, pengguna berhasil membaca band 2010/2024 dan memeriksa kode kelas sampel; hasil serta keterbatasan ada pada [inventaris](data_inventory.md). Ini belum membuktikan kelayakan seluruh 15 tahun atau kesiapan rilis. Jika audit lanjutan menunjukkan target tidak tersedia/layak, catat hambatan dan bahas revisi; jangan mengganti sumber, tahun, atau cakupan wilayah secara diam-diam.

## 4. Tahap rilis dan komitmen pengembangan

| Tahap | Cakupan | Syarat melanjutkan |
| --- | --- | --- |
| R1 — Versi inti | Peta 2010/2024, wilayah, statistik, perubahan/transisi, legenda/metadata | Semua kriteria inti lulus pemeriksaan dan bukti dicatat |
| R2 — Versi tahunan | Seluruh 15 tahun, grafik luas tahunan, pilihan pasangan tahun | Alur R1 tervalidasi; audit dan validasi diperluas ke seluruh tahun |
| R3 — Versi lengkap | Animasi, pembanding geser, peringkat perubahan, informasi titik dan sawit pendukung | Data, interaksi, angka, dan keterbatasan fitur lengkap diperiksa |

R1 adalah rilis pertama, bukan akhir proyek. Setelah tercapai, pekerjaan dilanjutkan ke R2 lalu R3. Tidak ada tanggal rilis yang ditetapkan pada fase ini. Tujuh fase pengerjaan digunakan untuk mewujudkan tiap tahap; perluasan dapat memerlukan pengulangan audit, analisis, integrasi, dan validasi.

## 5. Fitur inti dan kriteria penerimaan R1

| ID | Fitur dan perilaku | Kriteria penerimaan |
| --- | --- | --- |
| C01 | Peta tutupan lahan; pengguna memilih 2010 atau 2024 | Data asli hasil audit mencakup lima provinsi; pilihan tahun mengganti layer dan label; legenda sesuai kode raster; sumber/tahun terlihat |
| C02 | Pilihan seluruh Kalimantan/provinsi/kabupaten-kota | Pilihan wilayah membatasi area analisis dan memperbarui peta/statistik; kabupaten mengikuti provinsi yang dipilih; kembali ke seluruh Kalimantan memulihkan cakupan awal |
| C03 | Ringkasan luas kelas untuk kedua tahun | Tabel atau grafik menampilkan kode/nama kelas, luas hektare, proporsi pada area valid tahun tersebut, dan cakupan valid; angka dapat ditelusuri ke tabel analisis yang tersimpan |
| C04 | Peta perubahan 2010 → 2024 | Area stabil, berubah, dan tidak dapat dibandingkan dibedakan; statistik memakai area valid bersama; layer dapat dicocokkan dengan raster hasil analisis |
| C05 | Filter kelas asal dan tujuan | Pilihan asal → tujuan menampilkan area dan luas transisi yang sesuai; pilihan semua mengembalikan ringkasan lengkap; tidak ada hasil ditampilkan sebagai nol hanya karena permintaan gagal |
| C06 | Legenda, sumber, metode ringkas, dan keterbatasan | Pengguna dapat membaca identitas sumber/versi, tahun, arti kelas, arti mask, satuan, metode luas, versi batas, dan tanggal akses; hal belum terverifikasi ditandai |
| C07 | Penanganan keadaan aplikasi | Memuat data, galat, data tidak tersedia, dan hasil kosong dapat dibedakan; pergantian pilihan tidak meninggalkan angka/layer tahun atau wilayah lama tanpa penanda |

Kelas sawit mengikuti legenda klasifikasi utama yang lolos audit. Sawit dapat dieksplorasi melalui pilihan kelas/transisi R1; panel khusus tipe perkebunan dan tahun tanam BIOPAMA masuk R3. Enam kelas ringkas pada prototipe bukan legenda final.

## 6. Alur interaksi R1

1. Aplikasi membuka cakupan seluruh Kalimantan dengan peta 2024; tampilkan tahun dan status pemuatan.
2. Pengguna memilih wilayah; peta dan seluruh ringkasan mengikuti wilayah tersebut.
3. Pada tampilan tutupan lahan, pengguna memilih 2010 atau 2024. Statistik tahun tersebut memakai area valid tahun itu.
4. Pada tampilan perubahan, arah perbandingan tetap 2010 → 2024 dan ditulis jelas. Kartu perubahan memakai area valid pada kedua tahun.
5. Pengguna dapat memilih kelas asal/tujuan; filter transisi tidak mengubah definisi denominator persentase berubah seluruh wilayah.
6. Label menjelaskan ringkasan yang mengikuti filter dan yang tetap merangkum wilayah. Peta perubahan dan tutupan lahan memakai legenda sesuai mode masing-masing.
7. Jika kabupaten yang sedang dipilih tidak termasuk provinsi baru, pilihan kabupaten direset dan perubahan ditampilkan dengan jelas.

Komposisi UI mengikuti arah prototipe: sidebar kiri, peta dominan, statistik, dan area grafik. Timeline/animasi aktif ditambahkan ketika tahun tahunan tersedia. Bentuk batas, angka, dan peta sintetis diganti dengan produk yang terverifikasi sebelum rilis berbasis data asli. Detail visual dapat direvisi tanpa mengubah definisi indikator.

## 7. Definisi indikator dan aturan ilmiah

| Indikator | Definisi acuan |
| --- | --- |
| Luas kelas tahunan | Luas area valid yang memiliki kelas tertentu pada tahun pilihan, dalam hektare |
| Proporsi kelas | Luas kelas / luas valid tahun tersebut × 100% |
| Cakupan valid tahunan | Luas valid tahun tersebut / luas wilayah analisis × 100% |
| Area valid bersama | Area yang valid pada kedua tahun perbandingan |
| Area berubah | Area valid bersama dengan kelas berbeda |
| Area stabil | Area valid bersama dengan kelas sama |
| Area tidak dapat dibandingkan | Area analisis yang tidak valid pada salah satu atau kedua tahun |
| Persentase berubah | Luas berubah / luas valid bersama × 100% |
| Transisi | Luas kelas asal → kelas tujuan pada area valid bersama |

Jika denominator nol, persentase ditampilkan sebagai tidak tersedia, bukan nol. Mask valid, metode luas, grid acuan, dan toleransi rekonsiliasi ditetapkan setelah audit, sebelum analisis produksi. Metodologi harus menerapkan definisi ini; bila definisi akan berubah, spesifikasi diperbarui melalui keputusan bersama.

Satu koleksi dan satu versi batas digunakan lintas tahun. NoData/tidak teramati tidak boleh dihitung sebagai stabil. Perubahan klasifikasi belum otomatis perubahan nyata dan tidak membuktikan penyebabnya. Perbandingan dua ujung tahun dapat melewatkan perubahan sementara; R2 menambahkan riwayat tahunan. Pemeriksaan visual terbatas tidak diklaim sebagai estimasi akurasi seluruh Kalimantan. Tahun tanam sawit tidak otomatis tahun deforestasi.

## 8. Fitur R2 dan R3

| Tahap | Fitur | Target penerimaan |
| --- | --- | --- |
| R2 | Peta tahunan 2010–2024 dan grafik luas per kelas | Setiap tahun dapat dipilih; grafik/peta/tabel sesuai; cakupan valid tersedia per tahun; seluruh tahun memakai koleksi yang sama |
| R2 | Perbandingan pasangan tahun | Pilihan awal < akhir dalam 15 tahun didukung; pasangan dan arah tertulis; hasil sesuai tabel/raster analisis; strategi layanan 105 pasangan diputuskan berdasarkan audit dan performa |
| R3 | Timeline dan animasi | Putar, jeda, dan kecepatan bekerja; tahun aktif sinkron dengan layer dan statistik; kegagalan memuat tidak menampilkan data lama sebagai tahun baru |
| R3 | Pembanding dua tahun dengan pembatas geser | Kedua layer memakai wilayah, posisi peta, dan skala yang sama; tahun masing-masing terlihat; pergeseran hanya mengubah area tampilan |
| R3 | Peringkat perubahan wilayah | Peringkat hektare dan persentase memakai unit wilayah setara dan denominator yang jelas; cakupan valid menyertai hasil |
| R3 | Informasi lokasi | Klik pada lokasi menampilkan kelas tahun awal/akhir sesuai piksel dan mask; titik di luar cakupan atau invalid diberi keterangan |
| R3 | Modul sawit pendukung | Persebaran, tipe perkebunan, estimasi tahun tanam dan statistik disertai metadata terpisah; BIOPAMA tidak disajikan sebagai seri tahunan/kondisi terkini; perbedaan grid diaudit |

Pengembangan tambahan setelah versi utama lengkap: unduh CSV, unggah batas sendiri, dan riwayat lengkap kelas pada titik. Ketiganya dicatat sebagai backlog tambahan; bukan syarat penyelesaian R1–R3. Pengguna dapat memprioritaskannya melalui perubahan spesifikasi.

## 9. Produk dan bukti yang harus tersedia

- Inventaris dan metadata sumber yang telah diperiksa, termasuk band, grid, kelas, mask, lisensi, dan batas wilayah.
- Raster/layer yang siap analisis serta aturan pembentukannya.
- Tabel luas kelas per wilayah/tahun dan transisi per pasangan; skema memiliki ID wilayah, kode kelas, tahun, satuan dan cakupan valid yang relevan.
- Produk peta perubahan dengan kategori stabil, berubah, dan tidak dapat dibandingkan.
- Layanan data web dan aplikasi yang menampilkan produk tersebut secara konsisten.
- Notebook/skrip, konfigurasi tanpa rahasia, catatan proses, hasil pemeriksaan, dan petunjuk reproduksi.
- Dokumentasi portofolio yang membedakan prototipe, hasil terverifikasi, dan keterbatasan.

Data produksi besar tidak dimasukkan seluruhnya ke GitHub. Pilihan distribusi dan lokasi penyimpanannya didokumentasikan setelah arsitektur dipilih.

## 10. Kualitas dan batas tanggung jawab

Statistik aplikasi harus cocok dengan tabel sumber pada presisi tampilan yang didokumentasikan. Luas kelas, transisi, dan mask harus direkonsiliasi dengan area valid yang sesuai; toleransi numerik ditetapkan dan dicatat sebelum validasi produksi. Pemeriksaan meliputi lima provinsi, seluruh tingkat filter, hasil kosong, dan area invalid. Jangan mengklaim semua kabupaten diuji manual bila pemeriksaan hanya berupa sampel; pisahkan cakupan uji otomatis dan manual.

Uji pemuatan dan interaksi dilakukan pada perangkat, browser, koneksi, serta kondisi cache yang dicatat; waktu muat dan kegagalan dilaporkan. Ambang performa numerik ditetapkan setelah prototipe data tersedia, sebelum uji rilis. Pengolahan raster berat tidak dibebankan seluruhnya ke browser.

Tampilan utama ditujukan untuk penggunaan desktop. Tata letak lebih sempit diperiksa agar kontrol dan keterangan tetap dapat dibaca. Kebutuhan perangkat/browser spesifik diputuskan saat integrasi. Kredensial tidak dimasukkan ke repositori atau kode frontend. Atribusi dan ketentuan penggunaan data diperiksa sebelum distribusi.

Klasifikasi ulang mandiri seluruh Kalimantan, penentuan sebab perubahan, dan estimasi akurasi statistik regional bukan deliverable yang telah disepakati. Jika diperlukan, rancangan, data referensi, dan beban kerjanya dibahas sebagai perubahan lingkup.

## 11. Keputusan teknis yang dilanjutkan pada fase berikutnya

| Keputusan | Kapan harus diselesaikan |
| --- | --- |
| Akses/versi MapBiomas, band 2010/2024, legenda, mask dan batas administrasi | Audit data, sebelum penyiapan dan analisis |
| CRS/grid acuan, metode luas, toleransi dan aturan penyelarasan | Setelah audit, sebelum analisis produksi |
| Stack Python/web, tile, penyimpanan/layanan statistik | Sebelum implementasi layanan data dan integrasi |
| Strategi seluruh pasangan tahun, performa dan biaya layanan | Sebelum memperluas perbandingan pada R2 |
| Lisensi kode, izin distribusi data dan kebutuhan deployment | Sebelum publikasi/rilis terkait |
| Rincian validasi BIOPAMA dan agregasi tipe/tahun tanam | Sebelum implementasi modul R3 |

Keputusan tersebut tidak dianggap sudah terjawab oleh penutupan fase 1. Audit yang mengubah kelayakan produk harus memicu pembahasan, bukan asumsi baru.

## 12. Penutupan fase 1 dan penyelesaian rilis

- [x] Tujuan, wilayah, periode target dan unit wilayah dicatat.
- [x] Versi inti dahulu lalu dilanjutkan sampai versi lengkap disepakati pengguna pada 1 November 2026.
- [x] Fitur inti dipisahkan dari perluasan tahunan, versi lengkap, dan backlog tambahan.
- [x] Interaksi, indikator dan kriteria penerimaan ditulis.
- [x] Dependensi dan keputusan teknis yang belum terverifikasi dinyatakan secara eksplisit.
- [x] Dokumen spesifikasi utama tersedia dan dokumen pendukung ditautkan.

Fase 1 selesai sebagai baseline perencanaan. R1, R2, dan R3 belum selesai atau dirilis. Setiap rilis baru dianggap selesai setelah kriteria terkait dipenuhi, pemeriksaan dicatat, dan dokumentasi status diperbarui. Status pelaksanaan terbaru mengikuti [Current_State](../Current_State.md) dan roadmap; audit awal fase 2 terdokumentasi dengan pertanyaan terbuka sebelum penyiapan eksploratif.
