import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTextEdit, QLabel, QLineEdit, QSpinBox, QHBoxLayout)
# Import logic dari file sebelah
from scraper_logic import ScraperWorker

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Meta News Scraper - Modular Version")
        self.setGeometry(100, 100, 550, 450)
        
        layout = QVBoxLayout()

        # UI Elements
        layout.addWidget(QLabel("Link Pencarian Berita:"))
        self.url_input = QLineEdit()
        self.url_input.setText("https://www.detik.com/search/searchall?query=teknologi")
        layout.addWidget(self.url_input)

        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Jumlah Halaman:"))
        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 10)
        h_layout.addWidget(self.page_spin)
        layout.addLayout(h_layout)

        self.btn = QPushButton("MULAI META SCRAPING")
        self.btn.setFixedHeight(45)
        self.btn.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:disabled { background-color: #95a5a6; }
        """)
        self.btn.clicked.connect(self.start_scraping)
        layout.addWidget(self.btn)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: Consolas;")
        layout.addWidget(self.log)

        self.setLayout(layout)

    def start_scraping(self):
        url = self.url_input.text()
        pages = self.page_spin.value()

        if not url.startswith("http"):
            self.log.append("⚠️ URL tidak valid!")
            return

        self.btn.setEnabled(False)
        self.log.clear()
        
        # Memanggil Worker dari file scraper_logic
        self.worker = ScraperWorker(url, pages)
        self.worker.log_signal.connect(self.log.append)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, msg):
        self.log.append(msg)
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewsApp()
    window.show()
    sys.exit(app.exec())