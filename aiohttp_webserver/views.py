from typing import List, Dict

from aiohttp import web
from aiohttp.web import Request, Response
from asyncpg import Pool, Record

from aiohttp_webserver.utils import DB_KEY

routes = web.RouteTableDef()


@routes.get("/brands")
async def get_brands(request: Request) -> Response:
    connection: Pool = request.app.get(DB_KEY)
    result: List[Record] = await connection.fetch("SELECT * FROM brand")
    records: List[Dict] = [dict(res) for res in result]
    return web.json_response(
        records,
        status=200
    )


@routes.get("/products/{id}")
async def get_product(request: Request) -> Response:
    try:
        product_id = request.match_info.get("id")
        product_id = int(product_id)

        query = "SELECT * FROM product WHERE product_id = $1"
        connection: Pool = request.app.get(DB_KEY)
        record: Record = await connection.fetchrow(query, product_id)
        if not record:
            raise web.HTTPNotFound()
        return web.json_response(
            dict(record),
            status=200
        )
    except ValueError:
        raise web.HTTPBadRequest()


@routes.post("/product")
async def post_product(request: Request) -> Response:
    if not request.can_read_body:
        raise web.HTTPBadRequest()

    query = "INSERT into product(product_name, brand_id) VALUES ($1, $2)"
    connection: Pool = request.app.get(DB_KEY)
    body = await request.json()
    if "product_name" in body and "brand_id" in body:
        await connection.execute(query, body["product_name"], body["brand_id"])
        return web.Response(status=201)
    else:
        raise web.HTTPBadRequest()

