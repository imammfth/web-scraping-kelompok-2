# main_ui.py
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTextEdit, QLabel, QLineEdit, QSpinBox, QHBoxLayout)
from PyQt6.QtCore import QThread, pyqtSignal

# Import kelas logika dari file yang sudah kita pisahkan
from scraper_logic import NewsScraper

class ScraperWorker(QThread):
    finished_signal = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self, target_url, max_pages):
        super().__init__()
        self.target_url = target_url
        self.max_pages = max_pages

    def run(self):
        # Instansiasi objek scraper dan hubungkan callback ke pyqtSignal
        scraper = NewsScraper(
            target_url=self.target_url, 
            max_pages=self.max_pages, 
            log_callback=self.log_signal.emit
        )
        
        try:
            # Jalankan logika scraping
            result_message = scraper.run_scraper()
            self.finished_signal.emit(result_message)
        except Exception as e:
            self.finished_signal.emit(str(e))

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI News Scraper (Judul, Tanggal, Isi)")
        self.setGeometry(100, 100, 550, 450)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Link Berita (Contoh: Detik/Kompas/Google News):"))
        self.url_input = QLineEdit()
        self.url_input.setText("https://www.detik.com/search/searchall?query=kecerdasan+buatan")
        layout.addWidget(self.url_input)

        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Berapa Halaman:"))
        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 20)
        h_layout.addWidget(self.page_spin)
        layout.addLayout(h_layout)

        self.btn = QPushButton("MULAI SCRAPING KE EXCEL")
        self.btn.setFixedHeight(45)
        self.btn.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; border-radius: 5px;")
        self.btn.clicked.connect(self.start_scraping)
        layout.addWidget(self.btn)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; font-family: Consolas;")
        layout.addWidget(self.log)

        self.setLayout(layout)

    def start_scraping(self):
        self.btn.setEnabled(False)
        self.log.clear()
        
        # Mulai thread agar UI tidak 'freeze' (Not Responding)
        self.worker = ScraperWorker(self.url_input.text(), self.page_spin.value())
        self.worker.log_signal.connect(lambda m: self.log.append(m))
        self.worker.finished_signal.connect(self.done)
        self.worker.start()

    def done(self, msg):
        self.log.append(msg)
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewsApp()
    window.show()
    sys.exit(app.exec())