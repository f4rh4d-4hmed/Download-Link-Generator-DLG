import sys
import os
import urllib.parse
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QGroupBox, QHBoxLayout, QScrollArea

class TorrentSearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BDIX bypass speed-Videos Downloader")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.search_label = QLabel("Search your video name here:")
        self.search_label.setStyleSheet("color: white; font-size: 16px;")
        self.layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: #333; color: white; border: 2px solid #555; padding: 10px;")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        self.search_button.setStyleSheet("background-color: #007bff; color: white; border: 2px solid #007bff; padding: 10px;")
        self.layout.addWidget(self.search_button)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.load_more_button = QPushButton("Load More")
        self.load_more_button.setVisible(False)
        self.load_more_button.clicked.connect(self.load_more_results)
        self.load_more_button.setStyleSheet("background-color: #007bff; color: white; border: 2px solid #007bff; padding: 10px;")
        self.layout.addWidget(self.load_more_button)

        self.current_page = 0
        self.results_per_page = 100

    def clear_results(self):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

    def search(self):
        self.clear_results()
        self.current_page = 0
        keyword = self.search_input.text().strip().lower()
        if keyword:
            matching_urls = self.search_urls(keyword)
            if matching_urls:
                self.show_results(matching_urls)
            else:
                QMessageBox.warning(self, "Warning", "No matching URLs found.")
        else:
            QMessageBox.warning(self, "Warning", "Please enter a keyword to search.")

    def search_urls(self, keyword):
        try:
            with open('url.lock', 'r') as file:
                matching_urls = [line.strip() for line in file if all(word.lower() in line.lower() for word in keyword.split())]
                return matching_urls
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "File 'url.lock' not found.")
            return []

    def show_results(self, matching_urls):
        start_index = self.current_page * self.results_per_page
        end_index = start_index + self.results_per_page
        for url in matching_urls[start_index:end_index]:
            file_name = os.path.basename(urllib.parse.unquote(url))
            file_name = file_name.replace('.', ' ').replace('-', ' ')
            group_box = QGroupBox(file_name)
            group_layout = QHBoxLayout()  # Horizontal layout for each result box
            download_button = QPushButton("Download")
            download_button.setFixedSize(100, 30)  # Adjusting button size
            download_button.clicked.connect(lambda checked, url=url: self.open_browser(url))
            download_button.setStyleSheet("background-color: #007bff; color: white; border: 2px solid #007bff; padding: 5px;")
            group_layout.addWidget(download_button)
            result_label = QLabel(file_name)
            result_label.setStyleSheet("color: white; font-size: 16px;")
            group_layout.addWidget(result_label)
            group_box.setLayout(group_layout)
            self.scroll_layout.addWidget(group_box)

        self.load_more_button.setVisible(end_index < len(matching_urls))

    def load_more_results(self):
        self.current_page += 1
        keyword = self.search_input.text().strip().lower()
        matching_urls = self.search_urls(keyword)
        self.show_results(matching_urls)

    def open_browser(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TorrentSearchWindow()
    window.setStyleSheet("background-color: #2b2b2b;")
    window.show()
    sys.exit(app.exec_())
