import asyncio

async def check_server(address, port):
    try:
        _, writer = await asyncio.open_connection(address, port)
        print(True)
        return True
    except (asyncio.TimeoutError, OSError):
        print(False)
        return False
    finally:
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()

