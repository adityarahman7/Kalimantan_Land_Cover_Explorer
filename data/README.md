# Penyimpanan data

- `raw/`: sumber asli, tidak diubah; isinya diabaikan Git.
- `interim/`: hasil sementara; isinya diabaikan Git.
- `processed/`: hasil siap analisis/penyajian; isinya diabaikan Git.
- `samples/`: hanya sampel kecil yang telah diperiksa dan boleh dibagikan.
- `metadata/`: catatan provenance, skema, dan metadata kecil yang boleh dibagikan.

Pengecualian kondisi saat ini: `raw/batas_admin_kalimantan_BIG_2026.gpkg` telah diseleksi, disederhanakan dan satu fitur pulaunya dihapus oleh pengguna, lalu dipertahankan di raw atas pilihan pengguna. Jangan menganggapnya salinan unduhan asli yang tidak berubah. Berkas sumber yang dilaporkan adalah `BATASWILAYAH_KABKOTA_20260601.gdb`; keberadaan arsip sumber lokal belum diverifikasi. Riwayat serta keterbatasan ada pada [inventaris](../docs/data_inventory.md).

`metadata/audit_cakupan_valid_2010_2024.csv` menyimpan luas hasil ekspor GEE dengan presisi asli. `metadata/contoh_lokasi_tidak_valid.csv` menyimpan tiga koordinat pemeriksaan. Hasil nilai kelas di tiga titik dicatat pada inventaris berdasarkan laporan pengguna, bukan tersimpan dalam CSV koordinat.

Raster, GeoPackage, arsip, dan tile besar juga diabaikan secara global. Jika sampel memerlukan format tersebut, tentukan pengecualian secara sengaja setelah memeriksa ukuran dan lisensi. Statistik produksi besar disimpan lokal; hanya tabel ringkas terpilih masuk repositori.
