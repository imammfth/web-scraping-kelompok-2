# scraper_logic.py
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class NewsScraper:
    def __init__(self, target_url, max_pages, log_callback=None):
        self.target_url = target_url
        self.max_pages = max_pages
        # log_callback digunakan untuk mengirim pesan kembali ke UI tanpa perlu mengimpor PyQt
        self.log_callback = log_callback 

    def _log(self, message):
        """Fungsi internal untuk memicu callback log jika tersedia."""
        if self.log_callback:
            self.log_callback(message)

    def run_scraper(self):
        driver = None
        try:
            self._log("🚀 Menyiapkan Microsoft Edge...")
            options = Options()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            driver = webdriver.Edge(options=options)
            all_data = []
            current_url = self.target_url

            for page in range(1, self.max_pages + 1):
                self._log(f"📂 Membuka Halaman {page}...")
                driver.get(current_url)
                time.sleep(4)

                articles = driver.find_elements(By.TAG_NAME, "article") 
                if not articles:
                    articles = driver.find_elements(By.CLASS_NAME, "list-content") 

                for art in articles:
                    try:
                        title_el = art.find_element(By.TAG_NAME, "h3") 
                        judul = title_el.text.strip()
                        link = art.find_element(By.TAG_NAME, "a").get_attribute("href")

                        try:
                            tanggal = art.find_element(By.CSS_SELECTOR, ".date, .time, time, .content__date").text.strip()
                        except:
                            tanggal = "Tidak ditemukan"

                        try:
                            isi = art.find_element(By.CSS_SELECTOR, ".desc, .content__desc, p, .subtitle").text.strip()
                        except:
                            isi = "Tidak ada ringkasan"

                        if judul:
                            all_data.append({
                                "Tanggal": tanggal,
                                "Judul Berita": judul,
                                "Ringkasan": isi,
                                "Link": link
                            })
                    except:
                        continue

                self._log(f"✅ Halaman {page} selesai. Total data: {len(all_data)}")

                # PAGINATION
                if page < self.max_pages:
                    try:
                        next_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
                        current_url = next_btn.get_attribute("href")
                    except:
                        try:
                            next_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "Berikutnya")
                            current_url = next_btn.get_attribute("href")
                        except:
                            self._log("🛑 Tombol Next tidak ditemukan, berhenti.")
                            break

            driver.quit()

            if all_data:
                df = pd.DataFrame(all_data)
                file_name = "hasil_scrape_lengkap.xlsx"
                df.to_excel(file_name, index=False)
                
                # Membuka file khusus pengguna Windows
                if os.name == 'nt': 
                    os.startfile(file_name) 
                
                return f"Selesai! {len(all_data)} data disimpan ke {file_name}"
            else:
                return "❌ Gagal: Tidak ada data yang tertangkap. Periksa Selector CSS."

        except Exception as e:
            if driver: driver.quit()
            raise Exception(f"⚠️ Error: {str(e)}")