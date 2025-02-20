import asyncio

import asyncpg
import typing
from aiohttp.web_app import Application
from asyncpg import Pool
from starlette.endpoints import WebSocketEndpoint, WebSocket

from async_pg import settings

DB_KEY = "database"


async def create_pool(app: Application):
    print("pool is creating")
    pool = await asyncpg.create_pool(
            min_size=1,
            max_size=10,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USERNAME,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
    )
    app[DB_KEY] = pool


async def kill_pool(app: Application):
    print("pool is closing")
    pool: Pool = app[DB_KEY]
    await pool.close()


class UserCounter(WebSocketEndpoint):

    encoding = "text"
    users = []

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        UserCounter.users.append(websocket)
        await self._send_count()

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        UserCounter.users.remove(websocket)
        await self._send_count()

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        pass

    async def _send_count(self):
        if len(UserCounter.users) > 0:
            count_str = str(len(UserCounter.users))
            tasks_to_sockets = {
                asyncio.create_task(websocket.send_text(count_str)): websocket
                for websocket in UserCounter.users
            }
            done, pending = await asyncio.wait(tasks_to_sockets)
            for task in done:
                if task.execption() is not None:
                    if tasks_to_sockets[task] in UserCounter.users:
                        UserCounter.users.remove(tasks_to_sockets[task])
