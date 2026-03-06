import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit, 
                             QSpinBox, QHBoxLayout, QProgressBar, QDateEdit)
from PyQt6.QtCore import QDate
from scraper_logic import ScraperWorker
import pandas as pd

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tugas Web Scraper Berita - 2026")
        self.resize(800, 600)
        layout = QVBoxLayout()

        # Input URL
        layout.addWidget(QLabel("Link Utama Berita:"))
        self.url_input = QLineEdit("https://www.detik.com/search/searchall?query=teknologi")
        layout.addWidget(self.url_input)

        # Filter Tanggal & Limit
        filter_layout = QHBoxLayout()
        self.date_start = QDateEdit(QDate.currentDate().addDays(-7))
        self.date_end = QDateEdit(QDate.currentDate())
        self.page_spin = QSpinBox()
        self.page_spin.setValue(1)
        
        filter_layout.addWidget(QLabel("Dari:"))
        filter_layout.addWidget(self.date_start)
        filter_layout.addWidget(QLabel("Sampai:"))
        filter_layout.addWidget(self.date_end)
        filter_layout.addWidget(QLabel("Halaman:"))
        filter_layout.addWidget(self.page_spin)
        layout.addLayout(filter_layout)

        # Progress Bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Tombol
        self.btn = QPushButton("Mulai Scraping & Filter")
        self.btn.clicked.connect(self.start_scraping)
        layout.addWidget(self.btn)

        self.export_btn = QPushButton("Export ke Excel")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_data)
        layout.addWidget(self.export_btn)

        # Tabel Hasil
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Judul", "Isi Berita", "Link"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.data_list = []

    def start_scraping(self):
        self.btn.setEnabled(False)
        self.table.setRowCount(0)
        self.worker = ScraperWorker(
            self.url_input.text(), 
            self.page_spin.value(),
            self.date_start.date().toPyDate(),
            self.date_end.date().toPyDate()
        )
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, data, status):
        self.data_list = data
        self.btn.setEnabled(True)
        if data:
            self.export_btn.setEnabled(True)
            for row_data in data:
                row = self.table.rowCount()
                self.table.insertRow(row)
                for i, val in enumerate(row_data):
                    self.table.setItem(row, i, QTableWidgetItem(str(val)))
        print(f"Status: {status}")

    def export_data(self):
        df = pd.DataFrame(self.data_list, columns=["Tanggal", "Judul", "Isi", "Link"])
        df.to_excel("hasil_tugas_scraping.xlsx", index=False)
        print("Data diexport!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NewsApp()
    win.show()
    sys.exit(app.exec())