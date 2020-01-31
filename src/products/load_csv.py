import csv
import uuid
import logging

from .db import MongodbProvider

logger = logging.getLogger(__name__)

async def load_csv(filename):
    provider = MongodbProvider()
    await provider.setup()

    with open(filename, 'r') as f:
        products_reader = csv.DictReader(f)

        import_id = str(uuid.uuid4())
        total_created, total_updated = 0, 0

        for row in products_reader:
            row["sku"] = row.pop("sku (unique id)")
            row["import_id"] = import_id
            created = int(await provider.save_product(row))

            if created:
                total_created += 1
            else:
                total_updated += 1

        total_deleted = await provider.delete_products_with_another_import_id(import_id)

    logger.info("CSV import finished. new=%s, exisiting=%s, deleted=%s", total_created, total_updated, total_deleted)





