# scraping Berita (PyQt6 + Selenium)

Aplikasi meja kerja berbasis Python yang dibuat untuk mengotomatiskan proses mengambil artikel berita dari internet. **Pemahaman:**

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

(Ganti link gambar di bawah ini dengan screenshot aplikasi Anda yang sudah diunggah ke folder repositori, misalnya di folder `/assets/ui_preview.png`)

![Screenshot Antarmuka AI News Scraper](link-gambar-screenshot-anda-disini.png)

**Detail Antarmuka:**
Kolom untuk memasukkan tautan pencarian berita target.
2. **Input Halaman:** *Spinbox* untuk menentukan jumlah maksimal halaman yang ingin di-*scrape*, yaitu antara 1 hingga 20 halaman.
Tombol hijau besar untuk memulai proses scraping. Tombol ini akan tidak bisa digunakan (*disabled*) selama proses sedang berlangsung agar mencegah klik dua kali (*double-click*).
Area layar berwarna gelap yang menampilkan proses dan status bot secara real-time.

---

## Prasyarat (Prerequisites)

Sebelum menggunakan aplikasi ini, pastikan Anda sudah menginstal:
* **Python 3.8+**
Penggunaan Selenium hanya didukung oleh browser Microsoft Edge.
*Library Python yang diperlukan (lihat bagian instalasi)*.

## Panduan Penggunaan
Jalankan aplikasi utama melalui terminal atau command prompt:

python main_ui.py

Setelah jendela aplikasi terbuka, masukkan Link Berita dari hasil pencarian (misalnya: https://www.detik.com/search/searchall?query=kecerdasan+buatan).

Tentukan jumlah halaman yang ingin di-scrape melalui kolom "Berapa Halaman".

Klik tombol "MULAI SCRAPING KE EXCEL".

Pantau prosesnya melalui kotak Log di bagian bawah aplikasi. Browser Microsoft Edge mungkin akan terbuka (atau berjalan di latar belakang) secara otomatis.

Setelah selesai, aplikasi akan menampilkan pesan sukses di kotak Log dan otomatis membuka file Excel (hasil_scrape_lengkap.xlsx) berisi data berita yang berhasil dikumpulkan.

## Cara Instalasi

1. **Clone repositori ini:**
```bash
git clone [https://github.com/username-anda/nama-repo-anda.git](https://github.com/username-anda/nama-repo-anda.git)
cd nama-repo-anda
