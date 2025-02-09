from random import sample, choice
from typing import List

from asyncpg.connection import Connection


def get_random_words(num_of_words: int) -> List[str]:
    """Возвращает указанное количество слов из файла"""
    with open("words.txt", "r") as f:
        words = f.readlines()
    return [word.strip() for word in sample(words, num_of_words)]


async def get_random_db_words(db_model: str, num_of_words: int, connection: Connection):
    statement = f"select {db_model}.{db_model}_id from {db_model}"
    ids = await connection.fetch(statement)
    return [choice(ids)[f"{db_model}_id"] for _ in range(num_of_words)]
