import time
import pandas as pd
import os
from PyQt6.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class ScraperWorker(QThread):
    finished_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self, target_url, max_pages):
        super().__init__()
        self.target_url = target_url
        self.max_pages = max_pages

    def run(self):
        driver = None
        try:
            self.log_signal.emit("🚀 Menyiapkan Edge dengan Mode Meta-Scraping...")
            options = Options()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # options.add_argument("--headless") # Opsional
            
            driver = webdriver.Edge(options=options)
            all_data = []
            current_url = self.target_url

            for page in range(1, self.max_pages + 1):
                self.log_signal.emit(f"📂 Memindai Halaman Pencarian {page}...")
                driver.get(current_url)
                time.sleep(3)

                articles = driver.find_elements(By.TAG_NAME, "article")
                if not articles:
                    articles = driver.find_elements(By.CLASS_NAME, "list-content")

                links_to_visit = [
                    art.find_element(By.TAG_NAME, "a").get_attribute("href") 
                    for art in articles if art.find_elements(By.TAG_NAME, "a")
                ]

                # Membedah tiap link di tab baru
                for link in links_to_visit[:15]: 
                    try:
                        self.log_signal.emit(f"🔗 Membedah Metadata: {link[:50]}...")
                        driver.execute_script(f"window.open('{link}', '_blank');")
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(2)

                        # --- XPATH META EXTRACTION ---
                        judul = self._get_meta(driver, "//meta[@property='og:title']", driver.title)
                        
                        tanggal = self._get_meta_list(driver, [
                            "//meta[@property='article:published_time']",
                            "//meta[@name='pubdate']",
                            "//meta[@name='publishdate']",
                            "//meta[@property='og:updated_time']"
                        ], "Tidak ditemukan")

                        ringkasan = self._get_meta_list(driver, [
                            "//meta[@property='og:description']",
                            "//meta[@name='description']",
                            "//meta[@name='twitter:description']"
                        ], "Tidak ada ringkasan")

                        all_data.append({
                            "Tanggal": tanggal,
                            "Judul": judul,
                            "Ringkasan": ringkasan,
                            "Link": link
                        })

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    except:
                        if len(driver.window_handles) > 1:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        continue

                # Pagination logic
                if page < self.max_pages:
                    try:
                        next_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
                        current_url = next_btn.get_attribute("href")
                    except: break

            driver.quit()

            if all_data:
                file_name = "hasil_meta_scrape.xlsx"
                pd.DataFrame(all_data).to_excel(file_name, index=False)
                self.finished_signal.emit(f"Selesai! {len(all_data)} data disimpan ke {file_name}")
                os.startfile(file_name) if os.name == 'nt' else os.system(f"open {file_name}")
            else:
                self.finished_signal.emit("❌ Gagal mendapatkan data meta.")

        except Exception as e:
            if driver: driver.quit()
            self.finished_signal.emit(f"⚠️ Error: {str(e)}")

    def _get_meta(self, driver, xpath, default):
        try:
            val = driver.find_element(By.XPATH, xpath).get_attribute("content")
            return val if val else default
        except:
            return default

    def _get_meta_list(self, driver, xpaths, default):
        for xpath in xpaths:
            val = self._get_meta(driver, xpath, None)
            if val: return val
        return default