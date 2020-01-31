import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from ..server import make_app
from .utils import SetUpProvderMixin


class TestServer(SetUpProvderMixin, AioHTTPTestCase):
    async def get_application(self):
        return make_app()

    async def setUpAsync(self):
        # await SetUpProvderMixin.setUpsetUpAsync(self)
        await super(TestServer, self).setUpAsync()

    @unittest_run_loop
    async def test_products_all(self):
        resp = await self.client.request("GET", "/")
        print(resp.status, resp.text)
        assert resp.status == 200
        data = json.loads(await resp.text())
        self.assertGreater(len(data), 0)

    @unittest_run_loop
    async def test_products_limit(self):
        resp = await self.client.request("GET", "/?limit=5")
        data = json.loads(await resp.text())
        self.assertEqual(len(data), 5)

        resp = await self.client.request("GET", "/?limit=2")
        data = json.loads(await resp.text())
        self.assertEqual(len(data), 2)

    @unittest_run_loop
    async def test_products_offset(self):
        resp = await self.client.request("GET", "/?limit=5&offset=0")
        data1 = json.loads(await resp.text())

        resp = await self.client.request("GET", "/?limit=1&offset=2")
        data2 = json.loads(await resp.text())
        self.assertEquals(data1[2]["sku"], data2[0]["sku"])

    @unittest_run_loop
    async def test_products_filter(self):
        resp = await self.client.request("GET", "/?producer=Kerluke-Gerhold")
        data = json.loads(await resp.text())
        self.assertEquals(data[0]["sku"], "a2d7a9df-5cd4-4293-bbea-d5ce9af19609")
        self.assertEquals(len(data), 1)
