import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
import qdarktheme

from src.containers.add_server import AddServerDialog
from src.containers.server_list import ServerButton
from src.utilities.resource_path import resource_path



class ServerSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.active_threads = []
        self.setWindowTitle('Server Selector')
        self.setWindowIcon(QIcon(resource_path('img/penrose.png')))
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


    def create_server_button(self, name, ip):
        button = ServerButton(name, ip, self)
        button.clicked.connect(lambda: self.modify_server_ip(name, ip))
        self.scroll_layout.addWidget(button)
        self.active_threads.append(button.thread)
        button.thread.finished.connect(lambda: self.active_threads.remove(button.thread))


    def load_servers(self):
        try:
            with open(resource_path('save/servers.json'), 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []


    def refresh_server_status(self):
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, ServerButton):
                widget.check_status()


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
        with open(resource_path('save/servers.json'), 'w') as file:
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


    def add_server(self):
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()
        if name and ip:
            self.parent().servers.append({'name': name, 'ip': ip})
            self.parent().save_servers()
            self.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = ServerSelector()
    window.show()
    sys.exit(app.exec_())
