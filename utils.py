import functools
import random
import time
from typing import Set, Callable, Any
import asyncio


def async_timed():
    """Декоратор для замера времени выполнения корутин"""
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Выполняется функция "{func.__name__}" с аргументами {args} {kwargs}')
            begin = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                print(f"{func.__name__} завершилась за ", end - begin, " сек")
        return wrapped
    return wrapper


def sync_timed():
    """Декоратор для замера времени выполнения функций"""
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            print(f'Выполняется функция "{func.__name__}" с аргументами {args} {kwargs}')
            begin = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.time()
                print(f"{func.__name__} завершилась за ", end - begin, " sec")
        return wrapped
    return wrapper


@async_timed()
async def delay(_time) -> None:
    """Функция симулирует какую-либо длительную операцию, засыпая на _time секунд"""
    print("READY to sleep", _time, "second")
    await asyncio.sleep(_time)
    print("Сон", _time, "секунд окончен")


def cancel_tasks() -> None:
    """Функция завершает запущенные корутины"""
    print('Получен сигнал SIGINT!')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Снимается {len(tasks)} задач.')
    [task.cancel() for task in tasks]


def generate_string() -> None:
    """Функция генерирует список рандомных строк для тестов и сохраняет их в txt файл"""
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'goldberg']
    random_strings = []
    for _ in range(25_000_000):
        word = random.choice(words)
        counter_1 = random.randint(0, 10)
        counter_2 = random.randint(0, 10)
        counter_3 = random.randint(0, 10)
        random_strings.append(f"{word} {counter_1} {counter_2} {counter_3}\n")

    with open("some_random_words.txt", "w") as f:
        f.writelines(random_strings)
