from aiohttp import web
from .db import MongodbProvider
from .db import inject_data_provider


async def handle(request):
    producer = request.query.get("producer")
    try:
        limit = min(int(request.query.get("limit", 20)), 100)
        offset = max(int(request.query.get("offset", 0)), 0)
    except ValueError:
        raise web.HTTPBadRequest()

    data = await request.app["db"].get_products(limit, offset, producer)
    return web.json_response(data)


def make_app():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    app.on_startup.append(inject_data_provider(MongodbProvider, "db"))
    return app


def run():
    app = make_app()
    web.run_app(app)
