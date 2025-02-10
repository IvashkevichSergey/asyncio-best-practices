import asyncio
import hashlib
import os
import string
import random
from concurrent.futures import ThreadPoolExecutor

from utils import sync_timed, async_timed


def random_password(length: int) -> bytes:
    """Генерирует рандомный пароль указанной длины"""
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in range(length))


passwords = [random_password(10) for _ in range(1000)]


def hash_(password: bytes) -> str:
    """Вычисляет хеш указанного пароля"""
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


@sync_timed()
def main_sync():
    """Синхронно вычисляет хеши"""
    for password in passwords:
        hash_(password)


@async_timed()
async def main():
    """Вычисляет хеши асинхронно в пуле потоков"""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        tasks = [loop.run_in_executor(pool, hash_, password) for password in passwords]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    # main_sync()
