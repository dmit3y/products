import asyncio
import os
import json
from unittest import TestCase
from aiofile import AIOFile
from aiohttp.test_utils import AioHTTPTestCase

from ..db import MongodbProvider
from .. import settings


TESTS_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DB_NAME = "test_db"

loop = asyncio.new_event_loop()
def async_test(coro):
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper


class SetUpProvderMixin(AioHTTPTestCase):
    async def setUpAsync(self):
        self.provider = MongodbProvider(settings.MONGO_URI, TEST_DB_NAME)
        await self.provider.setup()

        async with AIOFile(os.path.join(TESTS_PATH, 'products.json'), 'r') as f:
            self.products = json.loads(await f.read())

        for product in self.products:
            await self.provider.save_product(product)

    async def tearDownAsync(self):
        await self.provider.client.drop_database(TEST_DB_NAME)
