import logging

import asyncpg
import asyncio

import settings
from async_pg.services import get_random_db_words
from utils import async_timed


async def insert_data(connection_: asyncpg.connection.Connection):
    products = await get_random_db_words("product", 1000, connection_)
    products_size = await get_random_db_words("product_size", 1000, connection_)
    product_colors = await get_random_db_words("product_color", 1000, connection_)
    result = await connection_.executemany(
        "INSERT INTO sku (product_id, product_size_id, product_color_id) VALUES ($1, $2, $3)",
        list(zip(products, products_size, product_colors))
    )
    return result


async def insert_one(connection_: asyncpg.connection.Connection):
    result = await connection_.executemany(
        "INSERT INTO brand (brand_name) VALUES ($1)", ("special",)
    )
    return result


async def query_product(pool):
    query = """SELECT
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
        WHERE p.product_id = 100"""
    async with pool.acquire() as connection_:
        return await connection_.fetchrow(query)


@async_timed()
async def main():
    conn: asyncpg.connection.Connection = await asyncpg.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )
    async with conn.transaction():
        await conn.execute("INSERT INTO brand (brand_name) VALUES ('new')")

        try:
            async with conn.transaction():
                await conn.execute("INSERT INTO brand VALUES (105, 'fictive')")
        except Exception as e:
            logging.log(logging.ERROR, "transaction is failed")

    results = await conn.fetch("SELECT * FROM brand")
    await conn.close()
    for res in results:
        print(res)

asyncio.get_event_loop().run_until_complete(main())
