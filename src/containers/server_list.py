import json
import socket
from PyQt5.QtWidgets import QPushButton, QMenu, QDialog, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor

from ..containers.edit_server import EditServerDialog

class ServerButton(QPushButton):
    def __init__(self, name, ip, server_selector, parent=None):
        super().__init__(name, parent)
        self.name = name
        self.ip = ip
        self.server_selector = server_selector
        self.setFont(QFont('Arial', 20))
        self.setMinimumHeight(100)
        self.active_thread = None
        self.is_online = None
        self.selected = False
        self.launch_thread()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.launch_thread)
        self.timer.start(10000)

    def launch_thread(self):
        def check_status():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.ip, 6969))
            sock.close()
            self.update_button_color(result == 0)

        QTimer.singleShot(0, check_status)

    def update_button_color(self, is_online):
        self.is_online = is_online
        if is_online:
            base_color = QColor("#4CAF50")
        else:
            base_color = QColor("#FF6347")
        
        if self.selected:
            color = base_color.darker(150).name()  # Darker tone
            self.setText(f"> {self.name} <")
        else:
            color = base_color.name()
            self.setText(self.name)

        self.setStyleSheet(f"QPushButton {{background-color: {color} !important; color: white;}}")
        self.update()

    def cleanup_thread(self):
        self.active_thread = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.server_selector.select_server(self)
            self.modify_server_ip()
        elif event.button() == Qt.RightButton:
            self.handle_right_click(event.pos())
        else:
            super().mousePressEvent(event)

    def select(self):
        self.selected = True
        self.update_button_color(self.is_online)

    def deselect(self):
        self.selected = False
        self.update_button_color(self.is_online)

    def handle_right_click(self, pos):
        self.show_context_menu(pos)

    def modify_server_ip(self):
        """Modify the server IP in the config file."""
        config_path = "user/launcher/config.json"
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            
            # Update the server information
            if 'Server' in config and isinstance(config['Server'], dict):
                config['Server']['Name'] = self.name
                config['Server']['Url'] = f"http://{self.ip}:6969"
            else:
                raise ValueError("Invalid JSON structure: 'Server' key missing or not a dictionary")
            
            with open(config_path, 'w') as file:
                json.dump(config, file, indent=4)
                
            print(f"Updated config.json with {self.name} IP {self.ip}")
        except FileNotFoundError:
            error_message = f"Config file not found at {config_path}"
            print(error_message)
        except json.JSONDecodeError:
            error_message = "Error decoding JSON from config file."
            print(error_message)
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(error_message)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.mapToGlobal(pos))
        if action == edit_action:
            self.edit_server()
        elif action == delete_action:
            self.delete_server()

    def edit_server(self):
        dialog = EditServerDialog(self.name, self.ip, self)
        if dialog.exec_() == QDialog.Accepted:
            self.server_selector.update_server(self.name, dialog.name_input.text(), dialog.ip_input.text())
            self.name = dialog.name_input.text()
            self.setText(self.name)

    def delete_server(self):
        reply = QMessageBox.question(self, 'Confirm Delete', f"Are you sure you want to delete {self.name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server_selector.delete_server(self.name)
            self.deleteLater()
