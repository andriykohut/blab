import asyncio
from aiohttp import web
import rethinkdb as r

from blab import config

loop = asyncio.get_event_loop()
app = web.Application(loop=loop, debug=config.DEBUG)
app.conn = r.connect(
    host=config.RETHINKDB_HOST,
    port=config.RETHINKDB_PORT,
    db=config.DB_NAME
)
app.r = r
# add routes
from blab import routes
