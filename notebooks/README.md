# Notebook

Belum ada notebook analisis. Gunakan urutan bernomor saat pekerjaan dimulai, misalnya audit data, penyiapan spasial, lalu analisis.

Setiap notebook perlu menjelaskan tujuan, input, parameter, output, hasil pemeriksaan, dan keterbatasan. Hindari path absolut perangkat. Periksa output notebook sebelum commit agar tidak memuat kredensial atau informasi pribadi.

## Acuan gaya Markdown

Disepakati pada 29 Oktober 2026: gunakan gaya Markdown `UrbanRVM_Tahap1_Simulasi.ipynb` sebagai acuan untuk notebook proyek ini. Seluruh sel Markdown referensi telah dibaca. Acuan berlaku untuk susunan dan cara menjelaskan; metode hidrologi, kode, dan hasil referensi tidak dipindahkan ke proyek tutupan lahan.

Pola yang dipertahankan:

- Satu judul utama `#` di awal, diikuti paragraf singkat mengenai tujuan dan input utama.
- Bagian pembuka **Cara menjalankan** dalam daftar bernomor dan **Keluaran** dalam tabel nama berkas/isi.
- Judul tahap memakai `##` dengan nama pendek dan konkret, misalnya Persiapan, Parameter, Data, dan Menyimpan keluaran.
- Sel Markdown ditempatkan sebelum blok kode terkait. Penjelasan cukup satu atau beberapa kalimat yang menerangkan tujuan dan keputusan penting; tidak semua tahap membutuhkan paragraf panjang.
- Nama variabel, parameter, dan berkas memakai backtick.
- Tabel dipakai untuk membandingkan pilihan parameter, metadata, atau keluaran.
- Rumus LaTeX dan diagram teks dipakai hanya jika membantu memahami metode yang benar-benar digunakan.
- Tampilan sederhana, tanpa dekorasi atau bagian panjang yang tidak mendukung proses.

## Penerapan pada notebook pertama

Notebook pertama direncanakan untuk audit data, bukan analisis perubahan. Urutan kerja dapat berupa:

1. Judul dan pengantar singkat, cara menjalankan, serta keluaran yang direncanakan.
2. Persiapan lingkungan dan akses.
3. Parameter.
4. Data dan identitas sumber.
5. Membaca aset dan daftar band.
6. Memeriksa band tahun target, proyeksi, dan grid setelah nama band terkonfirmasi.
7. Pemeriksaan kelas, mask, dan cakupan sesuai kemampuan serta cakupan audit.
8. Menyimpan metadata jika ekspor sudah diimplementasikan.
9. Ringkasan hasil pemeriksaan, keterbatasan, dan langkah berikutnya.

Ini rancangan urutan, bukan jumlah sel tetap atau daftar pemeriksaan yang sudah selesai. Satu tahap dapat memerlukan lebih dari satu sel. Tambahkan penjelasan singkat input → proses → output pada tahap yang membutuhkannya; jangan memaksakan tiga subjudul berulang pada setiap sel.

Untuk pendampingan belajar, jalankan dan periksa satu checkpoint sebelum melanjutkan. Petunjuk “Run all” dari referensi hanya diterapkan bila alur notebook kita sudah lengkap, dependensinya tersedia, dan eksekusi berurutan sudah diuji. Judul keluaran harus membedakan rencana keluaran dari berkas yang sudah dihasilkan. Temuan dan angka hanya diisi dari hasil eksekusi yang benar-benar diperiksa.
