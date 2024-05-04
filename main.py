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
        self.setWindowTitle('Server Selector 0.3.0')
        self.setWindowIcon(QIcon(resource_path('img/penrose.png')))
        self.setMinimumSize(512, 768)
        self.servers = self.load_servers()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.load_server_buttons()

        self.scroll_area.setWidget(scroll_widget)
        layout.addWidget(self.scroll_area)

        add_button = QPushButton("Add New Server", self)
        add_button.clicked.connect(self.show_add_server_dialog)
        layout.addWidget(add_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_servers(self):
        try:
            with open(resource_path('save/servers.json'), 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def load_server_buttons(self):
        for server in self.servers:
            button = ServerButton(server['name'], server['ip'], self)
            self.scroll_layout.addWidget(button)

    def show_add_server_dialog(self):
        dialog = AddServerDialog(self)
        if dialog.exec_():
            new_server = {'name': dialog.server_name, 'ip': dialog.server_ip}
            self.servers.append(new_server)
            self.save_servers()
            self.scroll_layout.addWidget(ServerButton(new_server['name'], new_server['ip'], self))

    def save_servers(self):
        with open(resource_path('save/servers.json'), 'w') as file:
            json.dump(self.servers, file, indent=2)

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

    def refresh_ui(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.load_server_buttons()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = ServerSelector()
    window.show()
    sys.exit(app.exec_())
