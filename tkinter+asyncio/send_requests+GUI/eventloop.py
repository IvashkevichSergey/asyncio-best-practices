import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from loadtester import LoadTester


class ThreadedEventLoop(Thread):
    """Класс расширяет класс Thread, инициируя запуск непрерывного цикла событий
    при вызове метода Thread.start()"""
    def __init__(self, loop: AbstractEventLoop):
        super(ThreadedEventLoop, self).__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


loop = asyncio.new_event_loop()

asyncio_thread = ThreadedEventLoop(loop)
asyncio_thread.start()

app = LoadTester(loop)
app.mainloop()


