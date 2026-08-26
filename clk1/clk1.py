from clickhouse_connect import get_client
import os 
from dotenv import load_dotenv

load_dotenv()

client = get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=os.getenv("CLICKHOUSE_PORT"),
    username=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD")
)

query = """
    CREATE TABLE IF NOT EXISTS products
    (
    id UInt32,
    title String,
    description String,
    category Nullable(String),
    price Decimal(3),
    discountPercentage Decimal(3),
    rating Decimal(3),
    stock UInt16,
    tags Array(String),
    sku String,
    weight UInt16,
    brand Nullable(String),
    product_width Float32,
    product_height Float32,
    product_depth Float32,
    warrantyInformation Nullable(String),
    shippingInformation Nullable(String),
    availabilityStatus Nullable(String),
    returnPolicy Nullable(String),
    minimumOrderQuantity Nullable(UInt8),
    created_at String,
    updated_at Nullable(String),
    barcode String,
    qr_code Nullable(String),
    images Array(String),
    thumbnail Nullable(String)
    )
    ENGINE = MergeTree
    ORDER BY id
"""
client.command(query)

print(client.query("SHOW CREATE TABLE default.products").result_rows)