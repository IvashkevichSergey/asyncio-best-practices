from asyncio import AbstractEventLoop
from queue import Queue
from tkinter import Tk
from tkinter.ttk import Label, Entry, Button, Progressbar
from typing import Optional

from stresstest import StressTest


class LoadTester(Tk):
    """Класс отвечает за отрисовку GUI для программы для тестирования различных URL"""
    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super(LoadTester, self).__init__(*args, **kwargs)
        self._queue: Queue = Queue()
        self._refresh_ms: int = 25

        self._loop: AbstractEventLoop = loop
        self._load_test: Optional[StressTest] = None
        self.title("URL requester")
        self.geometry("400x250")

        self._url_label = Label(self, text="URL")
        self._url_label.grid(column=0, row=0)

        self._url_field = Entry(self, width=30)
        self._url_field.grid(column=1, row=0)
        self._url_field.insert(0, "https://example.com")

        self._request_label = Label(self, text="Number of requests:")
        self._request_label.grid(column=0, row=1)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        self._submit = Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)

        self._pb = Progressbar(self, orient="horizontal", length=250, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    def _queue_update(self, completed_request: int, total_request: int):
        self._queue.put(int(completed_request / total_request * 100))

    def _update_bar(self, percentage: int):
        self._pb["value"] = percentage
        if percentage == 100:
            self._load_test = None
            self._submit["text"] = "Submit"
        else:
            self.after(self._refresh_ms, self._pool_queue)

    def _pool_queue(self):
        if not self._queue.empty():
            percent_completed = self._queue.get()
            self._update_bar(percent_completed)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._pool_queue)

    def _start(self):
        if self._load_test is None:
            self._load_test = StressTest(
                self._loop,
                self._url_field.get(),
                int(self._request_field.get()),
                self._queue_update
            )
            self._load_test.start()
            self._submit["text"] = "Cancel"
            self.after(self._refresh_ms, self._pool_queue)
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit["text"] = "Submit"
