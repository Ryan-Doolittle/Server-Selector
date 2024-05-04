from PyQt5.QtWidgets import *

from ..utilities.validate import is_valid_ip



class AddServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.server_name = None
        self.server_ip = None

    def setup_ui(self):
        layout = QVBoxLayout()
        name_label = QLabel("Server Name:")
        self.name_input = QLineEdit()
        ip_label = QLabel("Server IP:")
        self.ip_input = QLineEdit()

        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_server)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def add_server(self):
        server_name = self.name_input.text().strip()
        server_ip = self.ip_input.text().strip()
        if server_name and server_ip:
            if is_valid_ip(server_ip):
                self.server_name = server_name
                self.server_ip = server_ip
                self.accept()  # Only set attributes and accept if valid
            else:
                QMessageBox.warning(self, "Invalid IP", "The IP address entered is invalid. Please enter a valid IPv4 address.")
                self.ip_input.setFocus()
        else:
            QMessageBox.warning(self, "Incomplete Details", "Please enter both a server name and an IP address.")