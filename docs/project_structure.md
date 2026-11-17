# Panduan belajar struktur proyek: folder dan berkas

Panduan ini menjelaskan folder dan 34 berkas kerja proyek, diperbarui pada 1 November 2026 dengan spesifikasi utama. Saat ini proyek berisi kerangka repositori dan dokumentasi; kode analisis serta aplikasi lokal belum diimplementasikan. Adanya folder tidak berarti tahap pekerjaan sudah selesai.

Mulai dari bagian 0 untuk memahami folder. Bagian 1–10 menjelaskan fungsi setiap berkas; bagian 11–14 menjelaskan alasan dan cara membuatnya. Bagian 16 menyediakan contoh kecil dan latihan bertahap.

**Tidak semua berkas wajib ada.** Sebagian merupakan konvensi atau pilihan organisasi proyek. Berkas konfigurasi hanya berpengaruh jika alat terkait mengenali nama/lokasinya; dokumentasi Markdown tidak menjalankan pengolahan secara otomatis.

## 0. Memahami folder sebelum berkas

### Konsep sederhana

**Folder/direktori** adalah wadah untuk mengelompokkan berkas. **Berkas/file** menyimpan isi, misalnya teks, kode, tabel, atau citra. Folder dapat berisi subfolder. **Path** adalah alamat lokasi folder atau berkas.

Contoh `data/raw/citra_2010.tif`: `data` merupakan folder, `raw` subfolder, dan `citra_2010.tif` nama berkas. Akhiran `.tif` adalah ekstensi yang menunjukkan format yang diharapkan. Nama contoh ini bukan berkas yang sudah tersedia.

`D:\project\Kalimantan_Land_Cover_Explorer` adalah path absolut menuju akar proyek di komputer ini. `data/raw` adalah path relatif terhadap akar tersebut. Windows biasanya menampilkan pemisah `\`, sedangkan dokumentasi repositori sering memakai `/`.

Bayangkan proyek sebagai meja kerja: `data/` menyimpan bahan, `notebooks/` menyimpan catatan percobaan, `src/` menyimpan alat yang bisa dipakai ulang, `outputs/` menyimpan hasil, dan `docs/` menyimpan penjelasan. Pemisahan ini membantu menelusuri hasil kembali ke sumbernya.

### Peta seluruh folder kerja

Untuk membuat folder secara manual, buka folder induknya di editor, pilih **New Folder**, lalu ketik nama terakhir pada kolom lokasi di bawah. Contoh: untuk `data/raw/`, buat `data` di akar proyek lalu buat `raw` di dalam `data`. Untuk folder bertingkat, ulangi langkah yang sama. Jangan membuat ulang struktur proyek yang sudah ada; latihan dilakukan di lokasi terpisah.

| Lokasi folder | Fungsi dan alasan disediakan | Cara membuat sendiri dan contoh isi mendatang |
| --- | --- | --- |
| Akar proyek: `Kalimantan_Land_Cover_Explorer/` | Mengumpulkan semua pekerjaan dalam satu konteks. Ini titik awal path relatif, dokumentasi, dan repositori. | Buat folder bernama demikian di lokasi pilihan lalu buka di editor. Isi awal yang sederhana cukup README, docs, dan data. Nama folder akar boleh disesuaikan. |
| `.github/` | Menempatkan berkas pendukung kolaborasi GitHub agar platform dapat menemukan template pada lokasi yang didukung. Opsional untuk proyek lokal. | Buat `.github` di akar, lalu isi panduan kontribusi dan template PR. Titik di depan nama merupakan bagian nama; bukan perintah. |
| `.github/ISSUE_TEMPLATE/` | Memisahkan template issue dari dokumen biasa. Dibutuhkan pada lokasi ini jika memakai template issue Markdown seperti proyek ini. | Di dalam `.github`, buat `ISSUE_TEMPLATE`, lalu `task.md`. Pertahankan nama dan lokasi untuk perilaku template yang dimaksud. |
| `config/` | Memusatkan parameter yang bisa berubah agar tidak tersebar dalam kode. | Buat `config` di akar, lalu `project.example.json`. Nama folder merupakan pilihan desain; kode pembacanya harus menggunakan path yang sesuai. |
| `data/` | Menyatukan data dan informasi pendampingnya, terpisah dari kode. | Buat `data` di akar, lalu subfolder berdasarkan tahap data. Folder ini belum berisi raster asli. |
| `data/raw/` | Menyimpan sumber asli agar dapat kembali ke kondisi awal dan membandingkan hasil pemrosesan. | Buat `raw` di dalam `data`. Kelak salin/unduh sumber ke sini setelah akses dan ketentuan penggunaan diperiksa; jangan menimpa sumber dengan hasil olahan. |
| `data/interim/` | Menyimpan hasil antara yang masih dipakai atau diperiksa sebelum tahap berikutnya. | Buat `interim` di dalam `data`. Contoh mendatang: raster hasil potongan yang belum selesai diperiksa. |
| `data/processed/` | Menyimpan data yang memenuhi kriteria siap untuk analisis atau penyajian berikutnya. | Buat `processed` di dalam `data`. Isi hanya setelah pemeriksaan yang ditentukan lulus; memindahkan berkas ke sini saja tidak menjamin kualitasnya. |
| `data/samples/` | Menyediakan contoh kecil agar alur dapat dipahami tanpa mengunduh seluruh data produksi. | Buat `samples` di dalam `data`. Kelak tambahkan contoh kecil berlabel, dengan izin berbagi dan ukuran yang sesuai. |
| `data/metadata/` | Menyimpan keterangan tentang data, sehingga versi, band, CRS, dan asalnya dapat ditelusuri. | Buat `metadata` di dalam `data`. Contoh mendatang: JSON hasil pembacaan metadata atau kamus kelas yang bersumber jelas. |
| `docs/` | Menampung uraian yang terlalu terperinci untuk README utama: metode, audit, keputusan, dan panduan. | Buat `docs` di akar; buat berkas Markdown sesuai pertanyaan yang perlu dijawab. Folder tidak membutuhkan program khusus untuk dibaca. |
| `notebooks/` | Tempat eksplorasi yang menggabungkan narasi, kode, dan keluaran. Memudahkan pembelajaran bertahap. | Buat `notebooks` di akar. Notebook aktual dibuat melalui Jupyter atau editor pendukung notebook dan disimpan sebagai `.ipynb`; jangan hanya mengganti ekstensi teks biasa menjadi `.ipynb`. |
| `scripts/` | Tempat program untuk menjalankan tugas tertentu secara berulang. Memisahkan tugas eksekusi dari catatan eksplorasi. | Buat `scripts` di akar. Kelak buat berkas kode sesuai bahasanya dan dokumentasikan input, parameter, serta cara menjalankannya. |
| `scripts/earth_engine/` | Mengelompokkan skrip khusus GEE agar tidak tercampur dengan tugas lokal. | Buat `earth_engine` di dalam `scripts`. Kelak simpan skrip `.js` dari/untuk Code Editor; menyimpan `.js` lokal tidak otomatis menjalankannya di GEE. |
| `src/` | Tempat source code atau kode inti yang ingin digunakan ulang oleh beberapa notebook/skrip. | Buat `src` di akar, lalu calon lokasi modul. Menambahkan folder ini tidak otomatis membuat paket terinstal. |
| `src/kalimantan_lc/` | Mengelompokkan fungsi Python khusus analisis proyek dalam satu nama yang konsisten. | Buat `kalimantan_lc` di dalam `src`. Kelak tambahkan modul `.py`; pengaturan impor/paket ditentukan ketika implementasi dimulai. |
| `tests/` | Memisahkan contoh pemeriksaan kebenaran kode dari kode produksi dan data analisis. | Buat `tests` di akar. Setelah ada fungsi, tambahkan kasus dengan jawaban yang diketahui dan pilih alat pengujian yang sesuai. Folder kosong tidak menjalankan pengujian. |
| `outputs/` | Menyatukan hasil terpilih yang dibaca atau dinilai, berbeda dari data perantara. | Buat `outputs` di akar lalu kelompokkan hasil menurut bentuknya. Sertakan sumber dan cara pembentukan hasil. |
| `outputs/figures/` | Memisahkan peta/grafik dari tabel dan laporan sehingga mudah ditemukan untuk komunikasi hasil. | Buat `figures` di dalam `outputs`. Kelak simpan PNG atau format gambar lain yang sudah diperiksa. |
| `outputs/tables/` | Menyimpan tabel ringkas untuk inspeksi atau penyajian statistik. | Buat `tables` di dalam `outputs`. Kelak simpan CSV kecil beserta keterangan kolom dan satuan. |
| `outputs/reports/` | Menyimpan uraian hasil yang menyatukan tujuan, metode, temuan, dan keterbatasan. | Buat `reports` di dalam `outputs`. Kelak tambahkan laporan yang sudah diperiksa; saat ini belum ada laporan analisis. |
| `web/` | Menempatkan kode antarmuka aplikasi terpisah dari pengolahan geospasial. | Buat `web` di akar. Struktur berikutnya mengikuti teknologi yang dipilih; jangan menganggap file HTML saja sudah menyediakan seluruh layanan data raster. |
| `.git/` | Menyimpan metadata pengelolaan versi pada repositori lokal ini. Berbeda dari `.github`, yang berisi berkas kerja kolaborasi. | Dibuat otomatis oleh Git saat inisialisasi/clone, bukan melalui New Folder. Jangan mengedit isinya manual. Sudah tersedia di proyek ini. |

Selain `.git/` dan lokasi yang dikenali alat tertentu, nama serta jumlah folder merupakan keputusan organisasi. Untuk proyek kecil, struktur dapat lebih sederhana. Di proyek ini, folder disiapkan lebih awal agar arah kerja terlihat; kita tidak harus langsung mengisi semuanya.

### Alur hubungan yang direncanakan

```text
data/raw → audit/penyiapan → data/interim → data/processed
                 │                              │
          data/metadata                  analisis/publikasi data
                                                │
                                     outputs dan layanan untuk web
```

`config` memasok parameter; `notebooks`, `scripts`, dan `src` menjalankan atau menjelaskan proses; `tests` memeriksa logika yang sudah dibuat; `docs` mencatat metode dan bukti. Diagram ini rancangan hubungan kerja, bukan pipeline otomatis yang sudah berjalan. Aplikasi web kelak dapat membaca produk data atau layanan yang disiapkan; tidak semua isi `outputs/` otomatis menjadi input aplikasi.

## 1. Berkas pada direktori utama

| Berkas | Fungsi | Kapan digunakan atau diperbarui |
| --- | --- | --- |
| `README.md` | Halaman pengantar utama yang ditampilkan GitHub. Menjelaskan tujuan, cakupan, status, struktur, sumber data, dan keterbatasan. | Dibaca pertama kali oleh pengunjung; diperbarui ketika kemampuan atau status utama proyek berubah. |
| `Current_State.md` | Catatan posisi kerja terbaru: sudah selesai apa, belum diuji apa, keputusan, dan langkah berikutnya. | Dibaca saat melanjutkan proyek dan diperbarui setelah checkpoint penting. |
| `.gitignore` | Aturan yang memberitahu Git berkas lokal mana yang tidak perlu dilacak, seperti data produksi, raster, cache, dan pola kredensial. | Ditinjau saat muncul jenis data atau output baru. Tidak menghapus berkas dari komputer dan tidak otomatis menghentikan pelacakan berkas yang telanjur masuk Git. |
| `.gitattributes` | Mengatur perlakuan Git terhadap berkas teks dan biner, termasuk konsistensi akhir baris. | Biasanya diatur sekali, lalu disesuaikan jika format berkas baru memerlukan perlakuan khusus. |
| `.editorconfig` | Memberi panduan editor tentang indentasi, UTF-8, akhir baris, dan spasi. Python memakai empat spasi; sebagian berkas lain dua spasi. | Bekerja jika editor mendukung EditorConfig; membantu menjaga format saat menulis kode. Tidak menjalankan pemeriksaan kode. |

Perbedaan penting: `README.md` menjawab **proyek ini apa**, sedangkan `Current_State.md` menjawab **pekerjaan sekarang sampai di mana**.

## 2. Panduan kerja GitHub: `.github/`

| Berkas | Fungsi | Contoh penggunaan |
| --- | --- | --- |
| `.github/CONTRIBUTING.md` | Panduan mengusulkan perubahan: lingkup kecil, bukti pemeriksaan, sumber data, dan pembaruan dokumentasi. | Dibaca sebelum menambahkan fitur atau memperbaiki analisis. |
| `.github/ISSUE_TEMPLATE/task.md` | Formulir Markdown untuk membuat issue pekerjaan di GitHub. Memuat tujuan, input, proses, output, dan kriteria selesai. | Membuat pekerjaan “Verifikasi band MapBiomas 2010 dan 2024”. |
| `.github/pull_request_template.md` | Kerangka deskripsi pull request, yaitu usulan penggabungan perubahan kode atau dokumentasi. | Menjelaskan perubahan, cara memeriksa hasil, dan keterbatasan sebelum penggabungan. |

Template tersebut membantu pencatatan pekerjaan setelah repositori diunggah ke GitHub. Berkas ini bukan program otomatis; belum ada workflow pengujian atau deployment.

## 3. Konfigurasi: `config/`

| Berkas | Fungsi | Cara membacanya |
| --- | --- | --- |
| `config/project.example.json` | Contoh parameter proyek: wilayah, periode, alamat aset, status verifikasi, dan lokasi folder data. | Nilai `null` berarti belum ditentukan atau belum diverifikasi. `asset_access_verified: false` berarti akses belum terkonfirmasi. |

Konfigurasi memisahkan **nilai yang dapat berubah** dari **logika pemrosesan**. Contohnya, pergantian alamat aset sebaiknya tidak mengharuskan pengeditan banyak skrip.

Salinan lokal yang direncanakan bernama `config/project.local.json`; berkas tersebut **belum dibuat** dan sudah masuk aturan pengabaian Git. Saat ini belum ada program yang membaca konfigurasi secara otomatis.

## 4. Dokumentasi: `docs/`

| Berkas | Fungsi | Kapan diisi |
| --- | --- | --- |
| `docs/project_specification.md` | Acuan utama tujuan, cakupan, prioritas rilis, interaksi dan kriteria penerimaan. | Disepakati pada fase 1; diperbarui jika ada perubahan cakupan yang disetujui. |
| `docs/data_inventory.md` | Inventaris dataset dan daftar audit akses, versi, tahun, kelas, CRS/grid, mask, serta lisensi. | Saat menemukan sumber dan setiap kali memperoleh bukti hasil audit. |
| `docs/methodology.md` | Definisi indikator, aturan analisis, dan keterbatasan interpretasi. Menjelaskan cara menghitung hasil yang dapat dipertanggungjawabkan. | Sebelum analisis dan ketika metode berubah. |
| `docs/roadmap.md` | Urutan fase, deliverable, kriteria selesai, serta status masing-masing fase. | Saat mengatur prioritas dan memeriksa kemajuan proyek. |
| `docs/decisions.md` | Riwayat keputusan beserta alasan dan statusnya. | Saat memutuskan sumber, metode, cakupan, atau arsitektur. Keputusan lama tetap berguna untuk menjelaskan alasan perubahan. |
| `docs/processing_log.md` | Catatan proses yang benar-benar dijalankan: input, versi kode, parameter, output, pemeriksaan, dan galat. | Sesudah menjalankan pengolahan. Saat ini hanya berisi format pencatatan. |
| `docs/github_checklist.md` | Daftar pemeriksaan sebelum publikasi dan setelah implementasi tersedia. | Sebelum commit/push atau rilis: periksa isi, ukuran data, kredensial, lisensi, dan status hasil. |
| `docs/project_structure.md` | Panduan fungsi setiap berkas dalam repositori; dokumen yang sedang dibaca. | Saat mempelajari struktur atau setelah susunan berkas berubah. |

Bedakan tiga catatan: **metodologi** menjelaskan bagaimana analisis dirancang, **log pengolahan** mencatat apa yang benar-benar dijalankan, dan **log keputusan** menjelaskan mengapa suatu pilihan dibuat.

## 5. Data: `data/`

| Berkas | Fungsi |
| --- | --- |
| `data/README.md` | Aturan penyimpanan data asli, data antara, hasil siap analisis, sampel, dan metadata. |
| `data/raw/.gitkeep` | Penanda agar folder data asli tetap tercatat dalam Git. Data sumber sebenarnya akan disimpan di folder ini secara lokal. |
| `data/interim/.gitkeep` | Penanda folder hasil sementara, misalnya hasil potongan atau penyesuaian raster yang masih perlu pemeriksaan. |
| `data/processed/.gitkeep` | Penanda folder data yang sudah melewati penyiapan dan siap digunakan untuk tahap berikutnya. |
| `data/samples/.gitkeep` | Penanda folder sampel kecil yang diizinkan untuk dibagikan atau digunakan sebagai contoh reproduksi. |
| `data/metadata/.gitkeep` | Penanda folder informasi pendamping dataset, misalnya daftar band, proyeksi, versi sumber, dan tanggal akses. |

Semua `.gitkeep` saat ini kosong. Nama ini merupakan konvensi penanda, bukan perintah khusus Git. Git menyimpan berkas, sehingga penanda digunakan untuk membawa folder yang belum berisi pekerjaan.

Isi `raw/`, `interim/`, dan `processed/` diabaikan Git kecuali `.gitkeep`. Isi `samples/` dan `metadata/` dapat dilacak, tetapi masih dipengaruhi aturan global: misalnya berkas `.tif` tetap diabaikan. Folder sampel tidak otomatis membebaskan pembatasan lisensi atau ukuran.

## 6. Eksplorasi, skrip, modul, dan pengujian

| Berkas | Fungsi | Penggunaan berikutnya |
| --- | --- | --- |
| `notebooks/README.md` | Panduan notebook untuk eksplorasi bertahap beserta penjelasan input, parameter, output, dan pemeriksaan. | Notebook `.ipynb` akan ditambahkan ketika eksplorasi dimulai. |
| `scripts/README.md` | Panduan skrip yang menjalankan tugas tertentu dan aturan menjaga data asli serta kredensial. | Digunakan saat membuat skrip audit, ekspor, atau pengolahan. |
| `scripts/earth_engine/.gitkeep` | Penanda lokasi skrip Earth Engine. | Nantinya dapat berisi JavaScript untuk audit metadata atau ekspor. |
| `src/README.md` | Panduan penempatan logika Python yang dapat digunakan ulang. | Menjelaskan pemisahan kode inti dari notebook dan skrip. |
| `src/kalimantan_lc/.gitkeep` | Penanda calon lokasi modul analisis Python. | Nantinya dapat berisi fungsi audit grid, luas, atau transisi. Belum menjadi paket Python yang siap diinstal. |
| `tests/README.md` | Panduan pengujian yang direncanakan, terutama kasus kecil dengan jawaban yang diketahui. | Saat fungsi analisis tersedia, uji mask valid bersama dan konsistensi luas/transisi. |

Contoh hubungan yang direncanakan: notebook menjelaskan percobaan perhitungan luas; modul `src/` menyimpan fungsi perhitungannya; skrip memanggil fungsi untuk pekerjaan berulang; pengujian memeriksa jawaban fungsi pada kasus kecil. Hubungan ini belum diimplementasikan.

## 7. Hasil untuk ditinjau: `outputs/`

| Berkas | Fungsi |
| --- | --- |
| `outputs/README.md` | Aturan menyimpan hasil terpilih beserta sumber, versi, periode, satuan, metode, dan keterbatasan. |
| `outputs/figures/.gitkeep` | Penanda lokasi gambar hasil, misalnya peta atau grafik yang telah diperiksa. |
| `outputs/tables/.gitkeep` | Penanda lokasi tabel ringkas hasil, misalnya luas kelas atau transisi. |
| `outputs/reports/.gitkeep` | Penanda lokasi laporan yang merangkum metode, hasil, dan batas interpretasi. |

Perbedaannya dengan `data/processed/`: data processed ditujukan sebagai input tahap analisis/penyajian berikutnya; outputs ditujukan sebagai hasil yang dibaca atau ditinjau. Lokasi penyimpanan tidak otomatis membuat suatu hasil benar atau siap dipublikasikan. Saat ini belum ada hasil analisis pada folder tersebut.

## 8. Aplikasi: `web/`

| Berkas | Fungsi |
| --- | --- |
| `web/README.md` | Menjelaskan lokasi pengembangan aplikasi lokal, status kode prototipe, dan target interaksi WebGIS. |

Belum ada HTML, CSS, JavaScript aplikasi, dependensi, maupun perintah menjalankan aplikasi. Kode prototipe cloud belum disalin ke folder ini.

## 9. Folder internal `.git/`

Folder ini dibuat oleh Git saat repositori diinisialisasi. Isinya mencatat konfigurasi repositori, referensi cabang, dan objek riwayat saat commit tersedia. Jangan mengedit berkas internalnya secara manual; gunakan perintah Git untuk mengelola repositori.

Folder `.git/` tidak termasuk daftar berkas sumber yang diunggah sebagai isi repositori. Saat ini cabang lokal bernama `main`, belum ada commit dan remote. Berkas internal Git dapat berubah setelah operasi Git; panduan ini mencakup berkas kerja proyek, bukan inventaris setiap berkas internal Git.

## 10. Urutan penggunaan paling sederhana

1. Buka `README.md` untuk memahami proyek.
2. Buka `Current_State.md` untuk mengetahui posisi terakhir.
3. Buka `docs/data_inventory.md` untuk checkpoint audit data.
4. Kerjakan satu pemeriksaan dan simpan bukti kecil pada `data/metadata/` bila sesuai.
5. Catat proses pada `docs/processing_log.md` dan perbarui status.
6. Sebelum publikasi, gunakan `docs/github_checklist.md`.

**English practice:** “Separate inputs, processing, and outputs.” Artinya: pisahkan masukan, proses pengolahan, dan hasil agar alur proyek mudah dipahami serta diulang.

## 11. Dasar membuat berkas

Untuk membuat berkas baru secara manual di editor seperti VS Code:

1. Buka folder utama `D:\project\Kalimantan_Land_Cover_Explorer`.
2. Buat folder induk bila belum tersedia melalui **New Folder**.
3. Di folder yang tepat, pilih **New File** dan ketik nama lengkap beserta ekstensinya.
4. Isi sesuai tujuan berkas, lalu simpan menggunakan UTF-8.
5. Periksa hasilnya sebelum dimasukkan ke Git. Bila berkas sudah ada, buka dan edit; jangan menimpanya dengan contoh kosong.

Ekstensi `.md` berarti teks Markdown. Judul dapat ditulis sebagai `# Judul`, daftar sebagai `- Butir`, dan checklist sebagai `- [ ] Pekerjaan`. Berkas JSON memerlukan sintaks yang valid: nama kunci memakai tanda kutip ganda, nilai boolean memakai `true`/`false`, dan tidak ada koma setelah elemen terakhir.

Berkas seperti `.gitignore` dan `.editorconfig` memakai nama lengkap tersebut tanpa tambahan `.txt`. Jika memakai File Explorer, tampilkan ekstensi berkas agar nama sebenarnya dapat diperiksa. Membuat berkas melalui editor juga membantu menghindari nama yang tidak sengaja berakhir dengan `.txt`.

Berikut contoh Markdown untuk memahami format, bukan untuk mengganti README proyek yang sudah ada:

```markdown
# Nama proyek

## Tujuan
Jelaskan masalah yang ingin diselesaikan.

## Status
- [x] Struktur repositori dibuat.
- [ ] Akses data diverifikasi.
```

## 12. Alasan dan cara membuat berkas utama, konfigurasi, serta template

Semua cara manual di bawah mengikuti langkah pada bagian 11. Istilah **disarankan** menunjukkan manfaat untuk proyek ini, bukan persyaratan agar Git dapat berfungsi.

| Berkas | Mengapa disediakan dan tingkat kebutuhan | Cara membuat serta isi awal |
| --- | --- | --- |
| `README.md` | Sangat disarankan untuk portofolio: pengunjung perlu memahami tujuan, status, dan cara menggunakan proyek tanpa membaca seluruh folder. Git dapat bekerja tanpa berkas ini. | Buat di direktori utama. Tulis judul, tujuan, cakupan, status aktual, struktur, petunjuk penggunaan, sumber, dan keterbatasan. Nama README memungkinkan GitHub menampilkannya sebagai pengantar repositori. |
| `Current_State.md` | Pilihan organisasi untuk menjaga kesinambungan kerja antarhari atau sesi. Mengurangi risiko mengulang audit atau menganggap rencana sudah selesai. Namanya bebas dan tidak memiliki perilaku khusus pada Git. | Buat di direktori utama. Isi tanggal pembaruan, hasil terverifikasi, keputusan, pertanyaan terbuka, dan langkah berikutnya. Perbarui berdasarkan bukti setelah checkpoint. |
| `.gitignore` | Sangat disarankan untuk proyek dengan data besar dan konfigurasi lokal. Membantu mencegah penambahan berkas yang tidak dimaksudkan ke repositori. | Buat di direktori utama. Tambahkan satu pola per baris, misalnya `.env`, `data/raw/*`, dan pengecualian `!data/raw/.gitkeep`. Gunakan `git check-ignore` untuk memeriksa contoh path. Nama ini dikenali Git. |
| `.gitattributes` | Opsional, berguna untuk konsistensi lintas Windows/Linux dan perlakuan berkas biner. Mengurangi perubahan akhir baris yang tidak berkaitan dengan isi. | Buat di direktori utama. Mulai dengan `* text=auto`, kemudian aturan format seperti `*.md text eol=lf` dan `*.png binary`. Pilih aturan sesuai jenis berkas proyek. |
| `.editorconfig` | Opsional, berguna agar editor yang mendukungnya memakai format konsisten tanpa mengatur ulang tiap berkas. | Buat di direktori utama. Isi `root = true`, bagian `[*]` untuk pengaturan umum, lalu bagian `[*.py]` untuk empat spasi pada Python. Ini konfigurasi editor, bukan kode Python. |
| `.github/CONTRIBUTING.md` | Opsional, membantu kontributor maupun diri sendiri mengikuti standar perubahan dan pemeriksaan yang sama. | Buat folder `.github`, lalu berkas `CONTRIBUTING.md`. Jelaskan alur perubahan, bukti pemeriksaan, aturan data, dan kewajiban pembaruan dokumentasi. |
| `.github/ISSUE_TEMPLATE/task.md` | Opsional, menyediakan format pekerjaan agar tujuan dan kriteria selesai tidak kabur. | Buat folder `.github/ISSUE_TEMPLATE` dan berkas `task.md`. Tambahkan metadata YAML di antara dua baris `---` seperti contoh yang sudah ada, kemudian bagian tujuan, input, proses, dan output. Lokasi dan metadata digunakan GitHub untuk template issue Markdown. |
| `.github/pull_request_template.md` | Opsional, membantu peninjau mengetahui apa yang berubah dan bagaimana hasil diperiksa. | Buat pada lokasi tersebut. Isi bagian perubahan, pemeriksaan, sumber data, keterbatasan, dan checklist. GitHub dapat memakai isi ini sebagai deskripsi awal pull request. |
| `config/project.example.json` | Pilihan desain yang disarankan bila parameter akan dipakai ulang. Mengurangi penulisan alamat aset atau periode yang berbeda di banyak tempat. Akhiran `.example` hanya konvensi. | Buat folder `config` lalu berkas JSON. Tulis parameter nonrahasia, gunakan `null` untuk keputusan yang belum ada, dan periksa sintaks. Salinan lokal dapat dibuat dengan menyalin ke `project.local.json`; kode pembaca konfigurasi tetap perlu diimplementasikan. |

Contoh pemeriksaan aturan Git dari direktori utama:

```powershell
git check-ignore data/raw/example.tif
```

Jika path tersebut ditampilkan, path cocok dengan aturan pengabaian. Perintah ini hanya memeriksa aturan; tidak membuat, mengunduh, atau menghapus raster.

## 13. Alasan dan cara membuat seluruh berkas dokumentasi

Semua berkas pada tabel ini merupakan pilihan dokumentasi, bukan syarat teknis Git atau Python. Pemisahan dilakukan karena pertanyaan yang dijawab berbeda. Pada proyek lebih kecil, beberapa catatan dapat digabung selama informasinya tetap jelas.

| Berkas | Mengapa disediakan | Cara membuat serta isi awal |
| --- | --- | --- |
| `docs/project_specification.md` | Agar kesepakatan produk memiliki satu acuan dan tidak perlu dicari pada banyak dokumen. | Buat Markdown pada folder docs; tulis tujuan, cakupan, tahap rilis, fitur, interaksi, indikator, penerimaan dan keputusan terbuka. Bedakan kesepakatan rencana dari hasil implementasi. |
| `docs/data_inventory.md` | Agar sumber, versi, akses, dan kelayakan data tidak hanya tersimpan dalam ingatan. Membantu mendeteksi ketidaksesuaian koleksi sebelum analisis. | Buat tabel dataset, peran, versi, tahun, CRS/grid, mask, dan lisensi; tambahkan checklist dan tautan bukti. Bedakan dokumentasi penyedia dari hasil pembacaan aktual. |
| `docs/methodology.md` | Agar definisi luas, perubahan, dan validitas data konsisten serta dapat diperiksa orang lain. | Tulis tujuan analisis, definisi indikator, rumus, aturan pengolahan, validasi, dan keterbatasan. Tandai metode yang masih berupa rancangan. |
| `docs/roadmap.md` | Agar pekerjaan besar dapat dipecah menjadi tahap dengan keluaran dan kriteria selesai yang jelas. | Buat tabel fase, deliverable, kriteria selesai, dan status. Mulai dari audit data sebelum integrasi dan rilis. |
| `docs/decisions.md` | Agar alasan pemilihan sumber, metode, atau arsitektur dapat ditelusuri ketika proyek berubah. | Buat tabel tanggal, keputusan, dasar, dan status. Saat keputusan berubah, catat perubahan beserta alasan; pertahankan konteks keputusan sebelumnya. |
| `docs/processing_log.md` | Agar proses dapat diulang dan hasil dapat ditelusuri ke input serta parameter tertentu. | Buat format entri tanggal, tujuan, input/versi, skrip, parameter, output, pemeriksaan, dan galat. Isi sesudah proses dijalankan; jangan mengisi hasil yang belum terjadi. |
| `docs/github_checklist.md` | Agar pemeriksaan publikasi tidak terlewat, terutama kredensial, lisensi, ukuran data, dan kejelasan status hasil. | Tulis checklist Markdown dengan `- [ ]` untuk langkah sebelum push dan rilis. Centang hanya setelah pemeriksaan dilakukan. |
| `docs/project_structure.md` | Agar pengguna baru memahami alasan struktur tanpa menebak dari nama folder. Juga menjadi bahan belajar pengorganisasian proyek. | Daftar seluruh berkas kerja, lalu jelaskan fungsi, alasan, cara membuat, serta tingkat kebutuhan. Perbarui ketika struktur berubah. |
| `data/README.md` | Agar data asli tidak tertukar dengan hasil sementara atau hasil siap analisis. | Buat di folder `data`. Jelaskan isi setiap subfolder, aturan menjaga sumber asli, aturan Git, dan ketentuan sampel/metadata yang boleh dibagikan. |
| `notebooks/README.md` | Agar notebook tidak menjadi kumpulan eksperimen tanpa urutan atau konteks. | Buat di folder `notebooks`. Jelaskan penomoran, tujuan tiap notebook, input/output, pemeriksaan, dan peninjauan output sebelum commit. Notebook aktual dibuat melalui Jupyter atau editor yang mendukung `.ipynb`. |
| `scripts/README.md` | Agar jelas skrip mana menjalankan pekerjaan tertentu dan bagaimana input/output-nya diatur. | Buat di folder `scripts`. Jelaskan pembagian tugas, lokasi skrip Earth Engine, cara menjaga input asli, dan petunjuk menjalankan skrip ketika sudah tersedia. |
| `src/README.md` | Agar logika yang digunakan ulang memiliki tempat dan batas tanggung jawab yang jelas. | Buat di folder `src`. Jelaskan lokasi modul, fungsi yang direncanakan, dan hubungannya dengan notebook serta skrip. Tambahkan petunjuk impor/instalasi hanya setelah implementasi tersedia. |
| `tests/README.md` | Agar rencana pemeriksaan didasarkan pada perilaku yang harus benar, bukan sekadar ada folder pengujian. | Buat di folder `tests`. Jelaskan kasus kecil dengan jawaban yang diketahui, misalnya luas transisi dan mask valid. Tambahkan cara menjalankan tes setelah alat pengujian dipilih. |
| `outputs/README.md` | Agar hasil portofolio memiliki provenance, satuan, dan keterbatasan yang dapat diperiksa. | Buat di folder `outputs`. Jelaskan pembagian gambar, tabel, laporan, serta metadata minimum dan aturan ukuran/izin berbagi. |
| `web/README.md` | Agar pembaca tidak mengira folder web sudah berisi aplikasi yang dapat dijalankan. | Buat di folder `web`. Nyatakan status implementasi, hubungan dengan prototipe Sites, dan target fitur. Tambahkan instalasi/build hanya setelah diuji. |

## 14. Alasan dan cara membuat setiap `.gitkeep`, serta folder Git

Semua `.gitkeep` bersifat **opsional**. Alasannya sama: membawa struktur folder kosong ke repositori. Perbedaan lokasi menunjukkan fungsi folder yang ingin disiapkan.

| Berkas | Mengapa penanda ditempatkan di sini | Cara membuat |
| --- | --- | --- |
| `data/raw/.gitkeep` | Agar lokasi data asli tetap tersedia setelah clone walaupun datanya disimpan terpisah. | Buat folder `data/raw`, lalu berkas kosong bernama `.gitkeep`. Pengecualian di `.gitignore` yang sudah ada mengizinkan penanda ini dilacak. |
| `data/interim/.gitkeep` | Agar lokasi hasil antara tetap tersedia tanpa membagikan isi pengolahannya. | Buat folder `data/interim`, lalu `.gitkeep` kosong; pertahankan pengecualian pada `.gitignore`. |
| `data/processed/.gitkeep` | Agar lokasi data siap analisis tersedia meskipun data produksinya tidak masuk Git. | Buat folder `data/processed`, lalu `.gitkeep` kosong; pertahankan pengecualian pada `.gitignore`. |
| `data/samples/.gitkeep` | Agar lokasi sampel sudah dikenali sebelum sampel yang layak dibagikan tersedia. | Buat folder `data/samples`, lalu `.gitkeep` kosong. |
| `data/metadata/.gitkeep` | Agar tempat bukti metadata tersedia sejak tahap audit. | Buat folder `data/metadata`, lalu `.gitkeep` kosong. |
| `scripts/earth_engine/.gitkeep` | Agar lokasi skrip GEE tercatat sebelum skrip pertama dibuat. | Buat folder `scripts/earth_engine`, lalu `.gitkeep` kosong. |
| `src/kalimantan_lc/.gitkeep` | Agar calon lokasi modul analisis tercatat sebelum kode inti tersedia. | Buat folder `src/kalimantan_lc`, lalu `.gitkeep` kosong. Berkas ini sendiri tidak membuat paket Python. |
| `outputs/figures/.gitkeep` | Agar lokasi peta dan grafik terpilih tersedia sebelum ada hasil. | Buat folder `outputs/figures`, lalu `.gitkeep` kosong. |
| `outputs/tables/.gitkeep` | Agar lokasi tabel ringkas tersedia sebelum statistik dihitung. | Buat folder `outputs/tables`, lalu `.gitkeep` kosong. |
| `outputs/reports/.gitkeep` | Agar lokasi laporan tersedia sebelum laporan pertama ditulis. | Buat folder `outputs/reports`, lalu `.gitkeep` kosong. |

Penanda dapat dihapus ketika folder sudah berisi berkas lain yang dilacak. Khusus folder data yang isinya diabaikan, penanda masih berguna selama tidak ada berkas lain yang dilacak di folder tersebut.

Folder `.git/` berbeda: folder ini diperlukan oleh **repositori Git lokal biasa ini** untuk menyimpan informasi pengelolaan versi. Folder tersebut dibuat otomatis melalui `git init -b main` saat memulai repositori, atau oleh Git ketika melakukan clone. Jangan membuat sendiri berkas internalnya seperti `HEAD` dan `config` melalui editor. **Repositori proyek ini sudah diinisialisasi; tidak perlu mengulangi langkah tersebut.** Dokumentasi dan kode biasa tetap dapat dibaca tanpa `.git/`, tetapi pengelolaan riwayat lokal memerlukan metadata Git yang sesuai.

## 15. Cek pemahaman ringan

Jika kita mengganti sumber raster, dokumen mana yang perlu mencatat **identitas dataset**, dan dokumen mana yang perlu mencatat **alasan pergantiannya**? Gunakan perbedaan inventaris data dan log keputusan untuk menjawab.

**English practice:** “This file records why we made the decision.” Artinya: berkas ini mencatat alasan kita mengambil keputusan tersebut.

## 16. Belajar membuat struktur sendiri secara bertahap

Tujuan latihan adalah memahami hubungan berkas dan folder. Gunakan folder latihan terpisah dari proyek ini, misalnya folder baru bernama `latihan_struktur_gis` di lokasi pilihanmu. Contoh di bawah tidak dijalankan otomatis dan tidak perlu disalin seluruhnya sekaligus.

### Latihan pertama: satu folder dan satu berkas

**Konsep:** folder mengelompokkan pekerjaan; README menjelaskan pekerjaan tersebut kepada pembaca.

**Langkah manual:**

1. Buat folder `latihan_struktur_gis` melalui File Explorer.
2. Buka folder tersebut di editor, misalnya melalui menu **Open Folder** di VS Code.
3. Buat berkas baru bernama `README.md`.
4. Isi bagian kosong pada contoh berikut dengan kalimatmu sendiri, lalu simpan.

```markdown
# Latihan Proyek GIS

## Tujuan
Saya ingin mempelajari ...

## Data yang direncanakan
Data yang akan saya gunakan adalah ...

## Status
Saat ini saya sudah ...
Bagian yang belum dikerjakan adalah ...
```

**Bagian penting:** `#` membuat judul utama, `##` membuat subjudul, dan baris kosong memisahkan paragraf. Markdown tetap merupakan teks; editor atau GitHub menampilkan formatnya. Judul berkas boleh sama dengan README proyek lain karena berada dalam folder yang berbeda.

**Periksa sebelum lanjut:** apakah nama berkas tepat `README.md`, apakah isi tersimpan, dan apakah pembaca dapat membedakan tujuan dari status? Jika tersedia, buka Markdown Preview untuk memeriksa tampilan. Kirim isi README latihan untuk diperiksa sebelum melanjutkan latihan berikutnya.

### Latihan berikutnya: memisahkan data dari dokumentasi

Setelah latihan pertama diperiksa, buat `data` dan `docs` di dalam folder latihan. Buat `data/raw` serta `data/metadata` sebagai subfolder. Buat `docs/data_inventory.md`, lalu isi satu baris contoh yang jelas berlabel rencana:

```markdown
# Inventaris Data Latihan

| Dataset | Sumber | Status |
| --- | --- | --- |
| Nama data yang ingin dipakai | Belum dipilih | Rencana, belum diunduh |
```

**Mengapa demikian?** File raster kelak berada pada `data/raw`; penjelasan sumber dan statusnya berada dalam inventaris. Informasi proyeksi atau daftar band yang diekstrak dari raster dapat disimpan pada `data/metadata`. Menulis “belum diunduh” menjaga agar dokumentasi tidak mengklaim pekerjaan yang belum dilakukan.

**Cek pemahaman:** bila kamu baru memperoleh hasil potongan raster yang belum diperiksa, apakah lebih tepat menyimpannya pada `raw`, `interim`, atau `processed`? Jelaskan alasannya sebelum melihat kembali tabel folder.

### Mengenal konfigurasi tanpa langsung membuat program

Setelah memahami dokumentasi, kamu dapat berlatih membuat folder `config` dan berkas `project.example.json` pada folder latihan:

```json
{
  "project": "Latihan GIS",
  "start_year": 2010,
  "asset_access_verified": false,
  "verified_crs": null
}
```

`project` berisi teks, `start_year` angka, `asset_access_verified` boolean, dan `verified_crs` bernilai null karena belum diketahui. Simbol `{}` membungkus objek; `:` memisahkan nama kunci dan nilai; `,` memisahkan pasangan. Tanda kurung dan tanda kutip harus lengkap. Berkas ini hanya menyimpan parameter; perlu kode pembaca agar parameter dipakai dalam proses.

**Latihan isian:** ubah nama proyek menjadi nama pilihanmu. Biarkan status verifikasi tetap `false` jika kamu belum melakukan pemeriksaan. Jangan mengubah nilai hanya agar terlihat selesai.

### Mengenal aturan Git setelah folder dasarnya dipahami

Pada folder latihan, `.gitignore` dapat dibuat sebagai berkas teks biasa dengan isi kecil:

```gitignore
# Abaikan data asli, tetapi simpan penanda folder
data/raw/*
!data/raw/.gitkeep
```

Baris `#` merupakan komentar. Pola `data/raw/*` mengabaikan isi langsung folder itu; untuk folder baru yang tidak dilacak, pengabaian foldernya juga mencegah penelusuran isinya. Awalan `!` membuat pengecualian bagi penanda. Buat `.gitkeep` kosong di dalam `data/raw` jika ingin membawa struktur folder kosong melalui Git. Aturan ini baru relevan bagi pengelolaan Git dan tidak menghapus data lokal.

Ini contoh pengajaran minimal, bukan pengganti `.gitignore` proyek utama yang memiliki aturan lebih lengkap. Jangan menyalin aturan latihan untuk menimpa konfigurasi proyek utama.

### Mengulang pola menjadi mini-project

Setelah latihan sebelumnya diperiksa, buat struktur kecil berisi README, inventaris data, log proses, dan folder data yang diperlukan. Jelaskan dengan kalimatmu sendiri **di mana data disimpan, di mana proses dicatat, dan di mana hasil disimpan**. Tambahkan folder baru hanya ketika kamu dapat menjelaskan kebutuhannya.

Kamu belum perlu membuat seluruh berkas dari ingatan. Kemampuan awal yang dituju adalah memilih tempat yang tepat dan menulis keterangan yang benar. Struktur lebih lengkap dapat ditambahkan ketika kebutuhan muncul.

**English practice:** lengkapi kalimat “The README explains ...” dengan satu frasa pendek. Artinya: README menjelaskan ....
