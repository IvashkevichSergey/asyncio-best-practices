import asyncio
from asyncio import StreamReader
import sys
from threading import Thread

from utils import delay


async def create_stdin_reader() -> StreamReader:
    stream_reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader


async def main():
    stdin_reader = await create_stdin_reader()
    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))

thread = Thread(target=sys.stdin.readline, daemon=True)
thread.start()
thread.join()
asyncio.run(main())


