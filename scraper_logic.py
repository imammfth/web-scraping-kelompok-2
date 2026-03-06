import time
import pandas as pd
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class ScraperWorker(QThread):
    finished_signal = pyqtSignal(list, str) # Mengirim data hasil dan pesan status
    progress_signal = pyqtSignal(int)      # Mengirim persentase progress
    log_signal = pyqtSignal(str)           # Mengirim pesan log

    def __init__(self, target_url, max_pages, start_date=None, end_date=None):
        super().__init__()
        self.target_url = target_url
        self.max_pages = max_pages
        self.start_date = start_date # format: QDate
        self.end_date = end_date     # format: QDate

    # ... (bagian atas tetap sama)

    def run(self):
        driver = None
        all_data = []
        try:
            options = Options()
            options.add_argument("--headless") 
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Edge(options=options)
            
            current_url = self.target_url
            for page in range(1, self.max_pages + 1):
                self.log_signal.emit(f"Memproses Halaman {page}...")
                driver.get(current_url)
                time.sleep(3)

                articles = driver.find_elements(By.TAG_NAME, "article")
                if not articles: 
                    articles = driver.find_elements(By.CLASS_NAME, "list-content__item") # Selector umum lain

                links = []
                for art in articles:
                    try:
                        a_tag = art.find_element(By.TAG_NAME, "a")
                        links.append(a_tag.get_attribute("href"))
                    except: continue
                
                for i, link in enumerate(links):
                    prog = int(((page-1)/self.max_pages + (i+1)/(len(links)*self.max_pages)) * 100)
                    self.progress_signal.emit(prog)

                    try:
                        driver.execute_script(f"window.open('{link}', '_blank');")
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(2)

                        # 1. AMBIL JUDUL
                        judul = self._get_val(driver, "//meta[@property='og:title']", "content") or driver.title
                        
                        # 2. AMBIL TANGGAL (DENGAN FALLBACK)
                        raw_date = self._extract_date(driver)
                        
                        # 3. AMBIL ISI
                        isi = self._get_val(driver, "//meta[@property='og:description']", "content") or "Isi tidak ditemukan"

                        # --- LOGIKA FILTER TANGGAL ---
                        is_valid_date = True
                        display_date = "N/A"

                        if raw_date:
                            try:
                                # Bersihkan string tanggal (ambil 10 karakter pertama: YYYY-MM-DD)
                                clean_date_str = raw_date[:10]
                                dt_obj = datetime.strptime(clean_date_str, "%Y-%m-%d").date()
                                display_date = dt_obj.strftime("%d %b %Y")
                                
                                if self.start_date and self.end_date:
                                    if not (self.start_date <= dt_obj <= self.end_date):
                                        is_valid_date = False
                            except:
                                display_date = raw_date # Jika gagal parsing, tampilkan apa adanya

                        if is_valid_date:
                            all_data.append([display_date, judul, isi, link])

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    except:
                        if len(driver.window_handles) > 1: driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                
                # Pagination
                try:
                    next_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "Next") or \
                               driver.find_element(By.PARTIAL_LINK_TEXT, "Berikutnya")
                    current_url = next_btn.get_attribute("href")
                except: break

            driver.quit()
            self.finished_signal.emit(all_data, "Sukses")
        except Exception as e:
            if driver: driver.quit()
            self.finished_signal.emit([], str(e))

    def _extract_date(self, driver):
        """Fungsi khusus mencari tanggal dari berbagai sumber"""
        # Coba dari Meta Tag dulu (Paling akurat kalau ada)
        meta_selectors = [
            "//meta[@property='article:published_time']",
            "//meta[@name='pubdate']",
            "//meta[@name='publishdate']",
            "//meta[@name='content_PublishedDate']"
        ]
        for xpath in meta_selectors:
            val = self._get_val(driver, xpath, "content")
            if val: return val
        
        # Coba dari elemen teks yang sering dipakai situs berita Indo
        text_selectors = [
            ".date", ".detail__date", ".media__date", ".time", "time"
        ]
        for css in text_selectors:
            try:
                val = driver.find_element(By.CSS_SELECTOR, css).text
                if val: return val
            except: continue
            
        return None

    def _get_val(self, driver, xpath, attr):
        try: return driver.find_element(By.XPATH, xpath).get_attribute(attr)
        except: return None