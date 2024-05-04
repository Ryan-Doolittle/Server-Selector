from PyQt5.QtCore import QObject, pyqtSignal
import asyncio

class ServerCheckWorker(QObject):
    finished = pyqtSignal(bool)

    def __init__(self, address, port):
        super().__init__()
        self.address = address
        self.port = port

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.check_async())
        loop.close()
        self.finished.emit(result)

    async def check_async(self):
        try:
            reader, writer = await asyncio.open_connection(self.address, self.port)
            writer.close()
            await writer.wait_closed()
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
