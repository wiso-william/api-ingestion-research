from logging import getLogger
from pathlib import Path

from src.api_ingestion_research.transformation.transform import batcher
from src.api_ingestion_research.loading.clickhouse import create_client, load_batches
from src.api_ingestion_research.settings.config import settings
from src.api_ingestion_research.settings.setup_logging import setup_logging
from src.api_ingestion_research.utils.checkpoint import load_checkpoint, save_checkpoint

QUERY_DIR = Path(__file__).resolve().parent / "queries"

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

    skip_amount = load_checkpoint()

    if skip_amount is None:
        client.command(truncate_products_query)
        client.command(truncate_reviews_query)
        skip_amount = 0
        
except Exception:
    logger.exception("An error occurred while preparing the tables")
    raise

# Loading batches
counter = 0
for product_batch, reviews_batch, next_skip in batcher(
    limit=10,
    batch_amount=50,
    skip_amount=skip_amount,
):
    load_batches(
        client=client,
        batches=(product_batch, reviews_batch),
    )

    save_checkpoint(next_skip)

    logger.info("Loaded batch up to skip=%s", next_skip)