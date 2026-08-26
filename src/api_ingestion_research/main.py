import logging
from pathlib import Path

from src.api_ingestion_research.settings.config import settings
from src.api_ingestion_research.settings.setup_logging import setup_logging
from src.api_ingestion_research.ingestion.api import extract_products
from src.api_ingestion_research.transformation.transform import transform_product, convert_iterable_of_dataclasses_into_list_of_tuples
from src.api_ingestion_research.loading.clickhouse import create_client


setup_logging()
logger = logging.getLogger(__name__)

QUERY_DIR = Path(__file__).resolve().parent / "queries"

# util to skip API pages
skip_amount = 0

# products and reviews storage
products_list = []
reviews_list = []

# Saving in RAM all products and reviews
while True:
    products = extract_products(limit=settings.limit, skip_amount=skip_amount)
    if not products:
        break
    for product in products:
        flat_product, extracted_reviews = transform_product(product=product)
        products_list.append(flat_product)
        reviews_list.extend(extracted_reviews)
    skip_amount += settings.limit

# logging info
logger.info("Il numero di prodotti è %s", len(products_list))
logger.info("Il numero di review è %s", len(reviews_list))

# Normalizing for clickhouse consumption
product_tuples = convert_iterable_of_dataclasses_into_list_of_tuples(products_list)
reviews_tuples = convert_iterable_of_dataclasses_into_list_of_tuples(reviews_list)

# Creating clickhouse client 
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

