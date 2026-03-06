# scraping Berita (PyQt6 + Selenium)

Aplikasi scraping data berbasis Python yang dibuat untuk mengotomatiskan proses mengambil artikel berita dari internet. **Pemahaman:**

Aplikasi ini menyediakan kemudahan untuk mengumpulkan data berita dari berbagai sumber berita dan mampu mengekspor data tersebut ke dalam format Excel (.xlsx).

Aplikasi ini menggunakan **PyQt6** untuk tampilan antarmuka pengguna (GUI) yang cepat merespons dan **Selenium** untuk melakukan proses scraping di bagian belakang tanpa membuat aplikasi menjadi lambat.

## Fitur Utama
Pengguna yang intuitif: antarmuka yang sederhana dan mudah digunakan oleh siapa saja.
* **Menggarap Latar Belakang (Multithreading):** Menggunakan `QThread` agar antarmuka pengguna tetap berjalan lancar saat proses penggarapan berlangsung lama.
* **Live Logging:** Menampilkan keadaan *scraping* secara langsung dan terus-menerus di dalam aplikasi.
**Navigasi Otomatisasi halaman: otomatis berpindah ke halaman berikutnya (cari tombol "Next" atau "Berikutnya") sesuai batas halaman yang ditentukan.
Data yang telah dikumpulkan langsung diubah menjadi format Excel dan disimpan dalam file `hasil_scrape_lengkap.xlsx.
* **Auto-Open File (Windows):** Otomatis membuka file Excel setelah proses scraping selesai.

---

## 📸 Preview Tampilan

![Image](https://github.com/user-attachments/assets/406ebe38-00d2-4160-a163-dd0c3a798b6f)
![Image](https://github.com/user-attachments/assets/e309650c-ae55-4311-be3f-3470375b18ae)
![Image](https://github.com/user-attachments/assets/eca0c6eb-8bb2-43a9-aeab-2fd581bb2fb1)
![Image](https://github.com/user-attachments/assets/cae23dd3-a5ef-47d0-b97b-434b1ec29694)

**Detail Antarmuka:**
Penjelasan Komponen Antarmuka:

1. **Link Utama Berita:** Kolom input URL utama untuk memasukkan tautan berita atau halaman pencarian yang ingin diekstrak datanya 
2. **Filter Tanggal:** Fitur pemilihan tanggal memungkinkan pengguna untuk memilah berita yang diambil berdasarkan rentang waktu tertentu.
3. **Halaman:** Input angka untuk membatasi jumlah halaman yang akan di scraping.
4. **Progress Bar:** Indikator di bawah filter yang menampilkan persentase progres secara visual (0% hingga 100%), sehingga user tau sejauh mana proses berjalan.
5. **Tombol actionnya:**
   * **Mulai Scraping_Filter:** Tombol untuk mengeksekusi bot. Tombol ini otomatis tidak aktif selama proses berjalan untuk mencegah penumpukan perintah.
   * **Export ke Excel:** Tombol yang baru akan aktif setelah proses scraping selesai, berfungsi untuk menyimpan data yang ada di tabel ke dalam format file `.xlsx`.
6. **Tabel Data (Preview):** Area tabel interaktif yang langsung menampilkan hasil ekstraksi berita ke dalam empat kolom: **Tanggal**, **Judul**, **Isi Berita**, dan **Link**. Pengguna dapat melihat hasilnya terlebih dahulu sebelum mengekspornya.
7. **Activity Log:** Kotak terminal di bagian bawah yang memberikan pembaruan status secara langsung (misalnya: `"Memproses Halaman 1..."`), memudahkan pelacakan jika terjadi *error*.

---

## Prasyarat (Prerequisites)

Sebelum menggunakan aplikasi ini, pastikan sudah menginstal:
* **Python 3.8+**
Penggunaan Selenium hanya bisa diakses menggunakan browser Microsoft Edge.

## Panduan Penggunaan
Jalankan aplikasi utama melalui terminal:

python main_ui.py

Setelah aplikasi terbuka, masukkan Link Berita dari hasil pencarian

Tentukan jumlah halaman yang ingin di scraping lewat kolom "Berapa Halaman".

Klik tombol "MULAI SCRAPING KE EXCEL".

Pantau prosesnya melalui kotak Log di bagian bawah aplikasi. Browser Microsoft Edge mungkin akan terbuka (atau berjalan di latar belakang) secara otomatis.

Setelah selesai, aplikasi akan menampilkan pesan sukses di kotak Log dan otomatis membuka file Excel (hasil_scrape_lengkap.xlsx) berisi data berita yang berhasil dikumpulkan.

## Cara Instalasi

1. **Clone repositori ini:**
```bash
git clone [https://github.com/username-anda/nama-repo-anda.git](https://github.com/username-anda/nama-repo-anda.git)
cd nama-repo-anda
