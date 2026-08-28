from logging import getLogger
from pathlib import Path

from crs.api_ingestion_generators.transform.transformation import batcher
from crs.api_ingestion_generators.loading.clickhouse import create_client, load_batches
from src.api_ingestion_research.settings.config import settings
from src.api_ingestion_research.settings.setup_logging import setup_logging

QUERY_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "api_ingestion_research" / "queries"

setup_logging()
logger = getLogger(__name__)

client = create_client(settings=settings)

# SQL Paths
create_products_table_path = QUERY_DIR / "create_products.sql"
create_reviews_table_path = QUERY_DIR / "create_reviews.sql"
truncate_products_path = QUERY_DIR / "truncate_products.sql"
truncate_reviews_path = QUERY_DIR / "truncate_reviews.sql"

# SQL Queries
create_products_table_query = create_products_table_path.read_text()
create_reviews_table_query = create_reviews_table_path.read_text()
truncate_products_query = truncate_products_path.read_text()
truncate_reviews_query = truncate_reviews_path.read_text()

# Running SQL commands
try:
    client.command(create_products_table_query)
    client.command(create_reviews_table_query)
    client.command(truncate_products_query)
    client.command(truncate_reviews_query)
    logger.info("Tables are ready to accept data")
except:
    logger.exception("An error has occured while creating fresh tables")


# Loading batches
counter = 0
for batch in batcher(limit=10,batch_amount=50):
    counter += 1
    logger.info("Loaded batch number: %s", counter)
    load_batches(client=client, batches=batch)