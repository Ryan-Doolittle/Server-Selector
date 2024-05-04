import socket
from PyQt5.QtCore import QObject, pyqtSignal

class ServerCheckWorker(QObject):
    finished = pyqtSignal(bool)

    def __init__(self, ip, port=6969):
        super().__init__()
        self.ip = ip
        self.port = port

    def run(self):
        print(f"Attempting to connect to {self.ip}:{self.port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((self.ip, self.port))
        sock.close()
        is_online = (result == 0)
        print(f"Connection result for {self.ip}: {'online' if is_online else 'offline'}")
        self.finished.emit(is_online)
