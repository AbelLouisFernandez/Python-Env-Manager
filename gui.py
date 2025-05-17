from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QTextEdit, QLabel, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from logic import find_virtualenvs,list_packages,generate_graph
import os
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Env Manager")
        self.setGeometry(100, 100, 700, 500)

        # Widgets
        self.env_list = QListWidget()
        self.pkg_output = QTextEdit()
        self.pkg_output.setReadOnly(True)

        self.btn_scan = QPushButton("Scan Environments")
        self.btn_list_pkgs = QPushButton("List Packages")
        self.btn_graph = QPushButton("Generate Dependency Graph")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Environments"))
        layout.addWidget(self.env_list)
        layout.addWidget(self.btn_scan)
        layout.addWidget(self.btn_list_pkgs)
        layout.addWidget(self.btn_graph)
        layout.addWidget(QLabel("Package Info"))
        layout.addWidget(self.pkg_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect events
        self.btn_scan.clicked.connect(self.scan_envs)
        self.btn_list_pkgs.clicked.connect(self.show_packages)
        self.btn_graph.clicked.connect(self.make_graph)

    def scan_envs(self):
        home = os.path.expanduser("~")
        possible_dirs = [
            os.path.join(home, "Envs"),  # pipenv/virtualenvwrapper
            os.path.join(home, ".virtualenvs"),
            home  # fallback
        ]
        self.env_list.clear()
        found = find_virtualenvs(possible_dirs)
        if not found:
            QMessageBox.information(self, "Scan", "No virtual environments found.")
        for env in found:
            self.env_list.addItem(env)

    def show_packages(self):
        item = self.env_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Select an environment first.")
            return
        env_path = item.text()
        output = list_packages(env_path)
        self.pkg_output.setText(output)

    def make_graph(self):
        item = self.env_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Select an environment first.")
            return
        env_path = item.text()
        try:
            generate_graph(env_path)
            os.startfile('tree.png')
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

