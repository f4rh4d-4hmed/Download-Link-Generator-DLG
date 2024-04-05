from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QHBoxLayout, QLineEdit, QGroupBox
from PyQt5.QtGui import QIcon, QFont
import webbrowser
import re
import requests
from bs4 import BeautifulSoup
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class Signal(QObject):
    result_ready = pyqtSignal(str, str)

class TorrentSearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KAT-Everything is here")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.setStyleSheet("background-color: #272727; color: white;")

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter your search query")
        self.search_input.setStyleSheet("background-color: #444; color: white; border: 2px solid #555; padding: 10px;")
        self.search_input.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.search_input)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        self.search_button.setStyleSheet("background-color: #007bff; color: white; border: 2px solid #007bff; padding: 10px;")
        self.search_button.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.search_button)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Scroll Widget
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        # Debug Label
        self.debug_label = QLabel()
        self.debug_label.setStyleSheet("background-color: #272727; color: red;")
        self.layout.addWidget(self.debug_label)

        self.torrent_data = {}
        self.load_torrent_data()

        # Create a signal instance
        self.signal = Signal()
        # Connect signal to slot
        self.signal.result_ready.connect(self.add_result)

    def search(self):
        search_input = self.search_input.text().strip().lower()
        self.show_debug(f"Searching for '{search_input}'...")
        threading.Thread(target=self.scrape_and_save, args=(search_input,)).start()

    def load_torrent_data(self):
        try:
            with open('torrent.lock', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                name = None
                for line in lines:
                    if line.startswith("name="):
                        name = line[len("name="):].strip()
                    elif line.startswith("url="):
                        url = line[len("url="):].strip()
                        if name and url:
                            self.torrent_data[name.lower()] = url
                            name = None
        except FileNotFoundError:
            with open('torrent.lock', 'w', encoding='utf-8'):
                pass

    def add_result(self, name, magnet_link):
        group_box = QGroupBox()
        group_layout = QVBoxLayout()

        name_label = QLabel(name)
        name_label.setWordWrap(True)  # Wrap text if it exceeds the width of the box
        name_label.setStyleSheet("color: white;")
        name_label.setFont(QFont("Arial", 12))
        group_layout.addWidget(name_label)

        download_button = QPushButton("Download")
        download_button.setStyleSheet("background-color: #007bff; color: white; border: 2px solid #007bff; padding: 5px;")
        download_button.clicked.connect(lambda _, url=magnet_link: webbrowser.open(url))
        group_layout.addWidget(download_button)

        group_box.setLayout(group_layout)
        self.scroll_layout.addWidget(group_box)

    def scrape_and_save(self, search_input):
        try:
            base_url = f"https://kat.am/usearch/{search_input}"
            response = requests.get(base_url)
            if response.status_code == 200:
                self.show_debug(f"Scraping page {base_url}...")
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', class_='cellMainLink', href=True)
                for link in links:
                    directory_link = link['href']
                    directory_name = link.text.strip()
                    magnet_link = self.get_magnet_link(directory_link)
                    if magnet_link:
                        self.torrent_data[directory_name.lower()] = magnet_link
                        self.signal.result_ready.emit(directory_name, magnet_link)
                        with open('torrent.lock', 'a', encoding='utf-8') as file:
                            file.write(f"name={directory_name}\n")
                            file.write(f"url={magnet_link}\n")
                self.show_debug(f"Scraping finished for '{search_input}'.")
            else:
                self.show_debug(f"Failed to fetch page {base_url}", error=True)
        except Exception as e:
            self.show_debug(f"An error occurred: {e}", error=True)

    def get_magnet_link(self, directory_url):
        try:
            response = requests.get(f"https://kat.am{directory_url}")
            if response.status_code == 200:
                magnet_lines = re.findall(r'magnet:\?xt=urn:btih:[^\n]*announce\b', response.text)
                if magnet_lines:
                    return magnet_lines[0]
        except Exception as e:
            self.show_debug(f"An error occurred: {e}", error=True)
        return None

    def show_debug(self, message, error=False):
        debug_text = f"Debug: {message}"
        if error:
            debug_text = f"<font color='red'>{debug_text}</font>"
        self.debug_label.setText(debug_text)


if __name__ == "__main__":
    app = QApplication([])
    window = TorrentSearchWindow()
    window.show()
    app.exec_()
