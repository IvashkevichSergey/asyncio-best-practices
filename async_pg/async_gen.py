import asyncio

import asyncpg

from async_pg.settings import connection_settings
from utils import delay, async_timed


async def positive_numbers(until):
    for i in range(1, until):
        await delay(i)
        yield i


async def take(async_gen, num):
    counter = 0
    async for item in async_gen:
        if counter > num - 1:
            return
        counter += 1
        yield item


@async_timed()
async def main():
    conn: asyncpg.connection.Connection = await asyncpg.connect(**connection_settings)
    query = "SELECT * FROM sku"
    async with conn.transaction():
        cursor = conn.cursor(query)
        async for product in take(cursor, 10):
            print(product)
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
