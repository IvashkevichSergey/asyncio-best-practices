import asyncio
from concurrent.futures import ProcessPoolExecutor
import asyncpg
from asyncpg import Pool

from async_pg import settings
from utils import async_timed

product_query = """
    SELECT
    p.product_id,
    p.product_name,
    p.brand_id,
    s.sku_id,
    pc.product_color_name,
    ps.product_size_name
    FROM product as p
    JOIN sku as s on s.product_id = p.product_id
    JOIN product_color as pc on pc.product_color_id = s.product_color_id
    JOIN product_size as ps on ps.product_size_id = s.product_size_id
    WHERE p.product_id = 100
"""


async def query_products(pool: Pool):
    """Выполняет запрос в БД, захватывая пул соединений"""
    async with pool.acquire() as conn:
        return await conn.fetchrow(product_query)


@async_timed()
async def query_products_concurrently(pool, queries):
    """Создает указанное количество асинхронных запросов к БД,
    сразу запуская их выполнение в цикле событий"""
    queries = [query_products(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


def run_in_loop(queries_num: int):
    """Запускает выполнение корутин для выполнения асинхронных запросов к БД
    с асинхронным пулом подключений"""
    async def run_queries():
        async with asyncpg.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USERNAME,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME
        ) as async_pool:
            return await query_products_concurrently(async_pool, queries_num)
    result = asyncio.run(run_queries())
    results = [dict(res) for res in result]
    return results


async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as proc_pool:
        tasks = [loop.run_in_executor(proc_pool, run_in_loop, 10000) for _ in range(10)]
    result = await asyncio.gather(*tasks)
    total_queries = [len(res) for res in result]
    print("Result is", total_queries)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
