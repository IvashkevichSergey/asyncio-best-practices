import asyncio
import logging
import random
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from math import ceil
from typing import Callable, Optional

from aiohttp import ClientSession


class StressTest:
    """Класс управляет запуском стресс-тестирования указанного URL отправкой множества
     запросов. Метод .start() запускает тестирование, метод .stop() останавливает"""
    def __init__(self,
                 loop: AbstractEventLoop,
                 url: str,
                 total_requests: int,
                 callback: Callable[[int, int], None]):
        self._completed_requests: int = 0
        self._total_request: int = total_requests
        self._load_test_future: Optional[Future] = None
        self._loop: AbstractEventLoop = loop
        self._url = url
        self._callback: Callable[[int, int], None] = callback
        self._refresh_rate: int = ceil(self._total_request / 100)

    async def _get_url(self, session: ClientSession, url: str):
        try:
            # random_int = random.randint(0, 500)
            # url = f'http://numbersapi.com/{random_int}/trivia'
            # async with session.get(url) as res:
            #     await res.text()
            await session.get(url)
        except Exception as e:
            logging.error("Error happened: %s", e)

        self._completed_requests += 1
        if self._completed_requests % self._refresh_rate == 0 or self._completed_requests == self._total_request:
            self._callback(self._completed_requests, self._total_request)

    async def _make_requests(self):
        print("Starting to make requests for url", self._url)
        async with ClientSession() as session_:
            requests = [self._get_url(session_, self._url) for _ in range(self._total_request)]
            await asyncio.gather(*requests)

    def start(self):
        future = asyncio.run_coroutine_threadsafe(self._make_requests(), self._loop)
        self._load_test_future = future

    def cancel(self):
        if self._load_test_future:
            self._loop.call_soon_threadsafe(self._load_test_future.cancel)


