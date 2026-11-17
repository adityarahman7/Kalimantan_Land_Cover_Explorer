# Skrip

`earth_engine/01_audit_data.js` menyimpan audit awal fase 2: metadata/band/grid, sampel kelas, luas cakupan valid, titik termask, dan citra referensi Sentinel-2. Pelaksanaan awal dilakukan pengguna; keluaran Console dan tangkapan layar yang dibagikan dirangkum pada inventaris.

## Menjalankan audit kembali

1. Buka Earth Engine Code Editor dengan akun yang memiliki project dan izin aset yang diperlukan.
2. Salin isi [01_audit_data.js](earth_engine/01_audit_data.js). Deklarasi `batasAdmin` kini ada di dalam skrip; Imports dengan nama sama tidak diperlukan untuk salinan ini.
3. Periksa `boundaryAssetId`. Nilai `projects/portofolio-513404/assets/batas_admin_gee` disusun dari nama project/aset pada tangkapan layar pengguna; deklarasi eksplisit baru belum diuji ulang oleh asisten. Jika lokasi berbeda, gunakan Asset ID yang disalin langsung dari panel Assets dan catat perubahannya.
4. Jalankan sesuai checkpoint. Pemanggilan `Export.table.toDrive()` hanya membuat tugas; klik Run di Tasks untuk mengeksekusi ekspor. Jangan menjalankan ulang tugas ekspor lama bila hanya ingin memeriksa akses.
5. Pertahankan keluaran lama sebagai bukti run awal; catat tanggal/parameter bila mengekspor ulang. Hasil dapat berbeda bila sumber atau batas dimutakhirkan.

Input/output dan galat yang pernah terjadi tersedia pada [log pengolahan](../docs/processing_log.md). Parameter, provenance dan batas interpretasi tersedia pada [inventaris](../docs/data_inventory.md). Tidak ada token atau kredensial dalam skrip; Asset ID adalah alamat data, bukan rahasia autentikasi.

Logika Python yang digunakan ulang ditempatkan di `src/kalimantan_lc/`. Skrip tidak boleh menimpa data asli atau memuat token secara langsung.
