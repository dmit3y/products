import os

MONGO_URI = "mongodb://{}:{}@{}:{}".format(
    os.environ["MONGO_USER"],
    os.environ["MONGO_PASSWORD"],
    os.environ["MONGO_HOST"],
    os.environ["MONGO_PORT"],
)
MONGO_DB = os.environ.get("MONGO_DB", "products_api")
