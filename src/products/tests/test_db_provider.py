from unittest import TestCase
from .utils import async_test, SetUpProvderMixin


class TestMongoProvider(SetUpProvderMixin, TestCase):
    @async_test
    async def setUp(self):
        await super(TestMongoProvider, self).setUpAsync()

    @async_test
    async def tearDown(self):
        await super(TestMongoProvider, self).tearDownAsync()

    @async_test
    async def test_save_and_get_product(self):
        await self.provider.save_product(self.products[0])

        product_from_db = await self.provider.get_products(1, 0)
        assert product_from_db[0]["sku"] == self.products[0]["sku"]

    @async_test
    async def test_delete_products_by_import_id(self):
        before = len(await self.provider.get_products(limit=100, offset=0))
        await self.provider.delete_products_with_another_import_id("yet_another_import")
        after = len(await self.provider.get_products(limit=100, offset=0))

        self.assertNotEqual(before, after)
