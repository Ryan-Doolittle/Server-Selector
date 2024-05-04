from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from ..utilities.resource_path import resource_path

class AddServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Server')
        self.setWindowIcon(QIcon(resource_path('img/penrose.png')))
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        name_layout = QHBoxLayout()
        ip_layout = QHBoxLayout()

        name_label = QLabel("Server Name:", self)
        self.name_input = QLineEdit(self)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        ip_label = QLabel("Server IP:", self)
        self.ip_input = QLineEdit(self)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)

        add_button = QPushButton('Add', self)
        add_button.clicked.connect(self.add_server)
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)

        layout.addLayout(name_layout)
        layout.addLayout(ip_layout)
        layout.addWidget(add_button)
        layout.addWidget(cancel_button)
        

    def add_server(self):
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()
        if name and ip:
            self.parent().servers.append({'name': name, 'ip': ip})
            self.parent().save_servers()
            self.accept()
