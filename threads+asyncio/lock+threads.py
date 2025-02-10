import asyncio
import functools
from threading import Lock

import requests
from concurrent.futures import ThreadPoolExecutor

from utils import async_timed


global_lock = Lock()
counter: int = 0
REPEATS = 200


def get_random_fact(rand_num):
    """Выполняет запрос на API стороннего ресурса, возвращает ответ,
    попутно увеличивая глобальный счетчик на 1"""
    global counter
    result = requests.get(f'http://numbersapi.com/{rand_num}/trivia')
    with global_lock:
        counter += 1
    return result.text


async def reporter(count_requested: int):
    """Мониторит текущее состояние глобального счетчика и вычисляет процент
    выполнения задач"""
    while counter < count_requested:
        print(f"Completed on {counter/count_requested:.1%}")
        await asyncio.sleep(1)


@async_timed()
async def main():
    """Запускает выполнение задач в пуле потоков в асинхронном контексте"""
    loop = asyncio.get_running_loop()
    daemon_counter = asyncio.create_task(reporter(REPEATS))
    with ThreadPoolExecutor(max_workers=10) as pool:
        get_random_fact_partial = (functools.partial(get_random_fact, i) for i in range(REPEATS))
        urls = [loop.run_in_executor(pool, func) for func in get_random_fact_partial]
        res = await asyncio.gather(*urls)
        await daemon_counter
        # print(*res, sep='\n')


# @async_timed()
# async def main():
#     """Запускает выполнение синхронных задач в фоновых потоках асинхронно ожидая их завершения"""
#     daemon_counter = asyncio.create_task(reporter(REPEATS))
#     urls = [asyncio.to_thread(get_random_fact, i) for i in range(REPEATS)]
#     res = await asyncio.gather(*urls)
#     await daemon_counter
#     print(*res, sep='\n')


if __name__ == '__main__':
    asyncio.run(main())
