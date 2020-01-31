import motor.motor_asyncio
import pymongo

from . import settings

class MongodbProvider:
    def __init__(self, uri=settings.MONGO_URI, db=settings.MONGO_DB):
        self.uri = uri
        self.db = db

    async def setup(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db]

    async def init(self):
        await self.db.products.create_index([("producer", pymongo.ASCENDING)])
        await self.db.products.create_index([("import_id", pymongo.ASCENDING)])

    async def get_products(self, limit, offset, producer=None, fields=None):
        qs = {}

        if producer is not None:
            qs["producer"] = producer

        proj = {'_id': False, "import_id": False}
        if fields:
            for field in fields:
                proj[field] = True

        cursor = self.db.products.find(qs, proj).skip(offset).limit(limit)
        return await cursor.to_list(None)

    async def save_product(self, product):
        result = await self.db.products.replace_one(
            {
                "sku": product["sku"]
            },
            product,
            upsert=True
        )
        return True if result.upserted_id else False

    async def delete_products_with_another_import_id(self, import_id):
        result = await self.db.products.delete_many({"import_id": {"$ne": import_id}})
        return result.deleted_count

def inject_data_provider(cls, name):
    async def injector(app):
        app[name] = cls()
        await app[name].setup()
    return injector

def get_provider_cls():
    return MongodbProvider

async def init_db():
    provider = MongodbProvider()
    await provider.setup()
    await provider.init()
