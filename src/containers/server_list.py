import socket
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
import qdarktheme

from ..utilities.worker import ServerCheckWorker

from ..containers.edit_server import EditServerDialog


class ServerButton(QPushButton):
    def __init__(self, name, ip, parent=None):
        super().__init__(name, parent)
        stylesheet = qdarktheme.load_stylesheet(theme="dark")
        QApplication.instance().setStyleSheet(stylesheet)
        self.name = name
        self.ip = ip
        self.thread = None
        self.parent = parent
        self.setFont(QFont('Arial', 20))
        self.setMinimumHeight(100)
        self.initUI()


    def initUI(self):
        self.setStyleSheet("QPushButton {background-color: #FF6347; color: white;}")
        self.check_status()


    def check_status(self):
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        self.setup_thread()


    def setup_thread(self):
        self.thread = QThread()
        self.worker = ServerCheckWorker(self.ip, 6969)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.update_button_color)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()


    def update_button_color(self, is_online):
        color = "#4CAF50" if is_online else "#FF6347"
        self.setStyleSheet(f"QPushButton {{background-color: {color}; color: white;}}")


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
