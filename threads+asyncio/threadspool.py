import asyncio
import functools

import requests
from concurrent.futures import ThreadPoolExecutor

from utils import async_timed, sync_timed


def get_random_fact(rand_num):
    """Выполняет запрос на API стороннего ресурса, возвращает текст ответа"""
    result = requests.get(f'http://numbersapi.com/{rand_num}/trivia')
    return result.text


@sync_timed()
def main():
    """Стандартная синхронная реализация множества запросов на API"""
    res = [get_random_fact(i) for i in range(100)]
    print(*res, sep='\n')


@sync_timed()
def main():
    """Реализация множества запросов на API посредством пула потоков"""
    with ThreadPoolExecutor(max_workers=200) as pool:
        res = pool.map(get_random_fact, range(200))
        print(*res, sep='\n')


if __name__ == '__main__':
    main()
