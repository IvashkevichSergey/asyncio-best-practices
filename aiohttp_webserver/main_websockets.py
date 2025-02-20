from starlette.applications import Starlette
from starlette.routing import WebSocketRoute

from aiohttp_webserver.utils import UserCounter

app = Starlette(routes=[WebSocketRoute("/counter", UserCounter)])
