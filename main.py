import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
import qdarktheme

class ServerButton(QPushButton):
    def __init__(self, name, ip, parent=None):
        super().__init__(name, parent)
        stylesheet = qdarktheme.load_stylesheet(theme="dark")
        QApplication.instance().setStyleSheet(stylesheet)
        self.name = name
        self.ip = ip
        self.parent = parent
        self.setFont(QFont('Arial', 20))
        self.setMinimumHeight(100)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())
        else:
            super().mousePressEvent(event)

    def show_context_menu(self, pos):
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.mapToGlobal(pos))
        if action == edit_action:
            self.edit_server()
        elif action == delete_action:
            self.delete_server()

    def edit_server(self):
        dialog = EditServerDialog(self.name, self.ip, self.parent)
        if dialog.exec_() == QDialog.Accepted:
            self.parent.update_server(self.name, dialog.name_input.text(), dialog.ip_input.text())

    def delete_server(self):
        reply = QMessageBox.question(self, 'Confirm Delete', f"Are you sure you want to delete {self.name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent.delete_server(self.name)

class ServerSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Server Selector')
        self.setWindowIcon(QIcon('.\internal\penrose.png'))
        self.setMinimumWidth(512)
        self.setMinimumHeight(768)
        self.servers = self.load_servers()
        self.init_ui()

    def init_ui(self):
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setAlignment(Qt.AlignTop)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.load_server_buttons()

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.add_button = QPushButton("Add New Server", self)
        self.add_button.setFont(QFont('Arial', 16))
        self.add_button.setMinimumHeight(60)
        self.add_button.clicked.connect(self.show_add_server_dialog)
        self.layout.addWidget(self.add_button)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def load_server_buttons(self):
        for server in self.servers:
            self.create_server_button(server['name'], server['ip'])

    def load_servers(self):
        try:
            with open('servers.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def create_server_button(self, name, ip):
        button = ServerButton(name, ip, self)
        button.clicked.connect(lambda: self.modify_server_ip(name, ip))
        self.scroll_layout.addWidget(button)

    def show_add_server_dialog(self):
        dialog = AddServerDialog(self)
        dialog.exec_()

    def update_server(self, old_name, new_name, new_ip):
        for server in self.servers:
            if server['name'] == old_name:
                server['name'] = new_name
                server['ip'] = new_ip
                break
        self.save_servers()
        self.refresh_ui()

    def delete_server(self, name):
        self.servers = [server for server in self.servers if server['name'] != name]
        self.save_servers()
        self.refresh_ui()

    def save_servers(self):
        with open('servers.json', 'w') as file:
            json.dump(self.servers, file, indent=2)
        self.refresh_ui()

    def refresh_ui(self):
        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().deleteLater()
        self.load_server_buttons()

    def modify_server_ip(self, name, ip):
        print(f"Changing IP for server: {ip}")
        with open("user/launcher/config.json", "r") as json_in:
            config = json.load(json_in)
            
        with open("user/launcher/config.json", "w") as json_out:
            config["Server"]["Name"] = name
            config["Server"]["Url"] = f"http://{ip}:6969"
            json.dump(config, json_out, indent=2)

class AddServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Server')
        self.setWindowIcon(QIcon('internal\penrose.png'))
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

class EditServerDialog(QDialog):
    def __init__(self, name, ip, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Server')
        self.setWindowIcon(QIcon('internal\penrose.png'))
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

if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    
    stylesheet = qdarktheme.load_stylesheet(theme="dark")
    QApplication.instance().setStyleSheet(stylesheet)

    window = ServerSelector()
    window.show()
    sys.exit(app.exec_())
