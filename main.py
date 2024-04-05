import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSystemTrayIcon, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import subprocess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Manager")
        self.setWindowIcon(QIcon("icon.ico"))  # Change "icon.png" to your icon file
        self.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")

        layout = QVBoxLayout()
        
        self.title_label = QLabel("What do you want to download?")
        self.title_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.title_label, alignment=Qt.AlignHCenter)
        
        options_layout = QHBoxLayout()
        
        self.video_button = QPushButton("Video-Movie, Animation, Others")
        self.video_button.setStyleSheet("background-color: rgb(70, 70, 70); color: white;")
        self.video_button.clicked.connect(self.open_video_search)
        options_layout.addWidget(self.video_button)
        
        self.torrent_button = QPushButton("Torrent-Videos and Games")
        self.torrent_button.setStyleSheet("background-color: rgb(70, 70, 70); color: white;")
        self.torrent_button.clicked.connect(self.prompt_torrent_options)
        options_layout.addWidget(self.torrent_button)
        
        layout.addLayout(options_layout)
        self.setLayout(layout)
        
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def open_video_search(self):
        subprocess.Popen(["python", "video_search.py"])

    def prompt_torrent_options(self):
        self.hide()
        torrent_options_dialog = TorrentOptionsDialog()
        torrent_options_dialog.exec_()
        self.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

class TorrentOptionsDialog(QDialog):  # Change here
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Torrent Options")
        self.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
        
        layout = QVBoxLayout()
        
        self.title_label = QLabel("Where do you want to download Games from?")
        self.title_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.title_label, alignment=Qt.AlignHCenter)
        
        options_layout = QHBoxLayout()
        
        self.kat_button = QPushButton("KAT-Videos and Games Both")
        self.kat_button.setStyleSheet("background-color: rgb(70, 70, 70); color: white;")
        self.kat_button.clicked.connect(self.execute_kat)
        options_layout.addWidget(self.kat_button)
        
        self.fitgirl_button = QPushButton("Fitgirl-Repack: Games Only")
        self.fitgirl_button.setStyleSheet("background-color: rgb(70, 70, 70); color: white;")
        self.fitgirl_button.clicked.connect(self.execute_fitgirl)
        options_layout.addWidget(self.fitgirl_button)
        
        layout.addLayout(options_layout)
        self.setLayout(layout)
        
    def execute_kat(self):
        subprocess.Popen(["python", "kat.py"])

    def execute_fitgirl(self):
        subprocess.Popen(["python", "fitgirl_repack.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
