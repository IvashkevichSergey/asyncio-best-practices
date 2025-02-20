from aiohttp import web

from aiohttp_webserver.utils import kill_pool, create_pool
from aiohttp_webserver.views import routes

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(create_pool)
    app.on_cleanup.append(kill_pool)
    web.run_app(app)
