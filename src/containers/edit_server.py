from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from ..utilities.resource_path import resource_path



class EditServerDialog(QDialog):
    def __init__(self, name, ip, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Server')
        self.setWindowIcon(QIcon(resource_path('img/penrose.png')))
        self.setup_ui(name, ip)


    def setup_ui(self, name, ip):
        layout = QVBoxLayout(self)
        name_layout = QHBoxLayout()
        ip_layout = QHBoxLayout()

        name_label = QLabel("Server Name:", self)
        self.name_input = QLineEdit(self)
        self.name_input.setText(name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        ip_label = QLabel("Server IP:", self)
        self.ip_input = QLineEdit(self)
        self.ip_input.setText(ip)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)

        update_button = QPushButton('Update', self)
        update_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)

        layout.addLayout(name_layout)
        layout.addLayout(ip_layout)
        layout.addWidget(update_button)
        layout.addWidget(cancel_button)