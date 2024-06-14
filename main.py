import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import qdarktheme

from src.containers.add_server import AddServerDialog
from src.containers.server_list import ServerButton
from src.utilities.resource_path import resource_path

class ServerSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Server Selector 1.1.0')
        self.setWindowIcon(QIcon(resource_path('img/penrose.png')))
        self.setMinimumSize(512, 768)
        self.servers = self.load_servers()
        self.selected_button = None  # Track the selected button
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

        # Select the server marked as selected in servers.json
        self.select_initial_server()

    def load_servers(self):
        try:
            with open("servers.json", 'r') as file_in:
                return json.load(file_in)
        except FileNotFoundError:
            with open("servers.json", 'w') as file_init:
                json.dump([], file_init)
            return []

    def load_server_buttons(self):
        for server in self.servers:
            button = ServerButton(server['name'], server['ip'], self)
            self.scroll_layout.addWidget(button)
            if server.get('selected', False):
                self.selected_button = button

    def show_add_server_dialog(self):
        dialog = AddServerDialog(self)
        if dialog.exec_():
            new_server = {'name': dialog.server_name, 'ip': dialog.server_ip, 'selected': False}
            self.servers.append(new_server)
            self.save_servers()
            self.scroll_layout.addWidget(ServerButton(new_server['name'], new_server['ip'], self))

    def save_servers(self):
        with open("servers.json", 'w') as file:
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

    def select_server(self, server_button):
        if self.selected_button:
            self.selected_button.deselect()
            # Update the JSON file to mark the previous server as not selected
            for server in self.servers:
                if server['name'] == self.selected_button.name:
                    server['selected'] = False
                    break

        self.selected_button = server_button
        self.selected_button.select()

        # Update the JSON file to mark the current server as selected
        for server in self.servers:
            if server['name'] == self.selected_button.name:
                server['selected'] = True
                break

        self.save_servers()

    def select_initial_server(self):
        if self.selected_button:
            self.selected_button.select()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = ServerSelector()
    window.show()
    sys.exit(app.exec_())
