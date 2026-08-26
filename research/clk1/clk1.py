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

query_create_product_table = """
    CREATE TABLE IF NOT EXISTS products
    (
    id UInt32,
    title String,
    description String,
    category Nullable(String),
    price Float64,
    discountPercentage Float32,
    rating Float32,
    stock UInt16,
    tags Array(String),
    sku String,
    weight UInt16,
    product_width Float32,
    product_height Float32,
    product_depth Float32,
    warrantyInformation Nullable(String),
    shippingInformation Nullable(String),
    availabilityStatus Nullable(String),
    returnPolicy Nullable(String),
    minimumOrderQuantity Nullable(UInt8),
    created_at DateTime64(3),
    updated_at Nullable(DateTime64(3)),
    barcode String,
    qr_code Nullable(String),
    images Array(String),
    thumbnail Nullable(String),
    brand Nullable(String),
    )
    ENGINE = MergeTree
    ORDER BY id
"""
client.command("DROP TABLE default.products")
client.command(query_create_product_table)

#print(client.query("SHOW CREATE TABLE default.products").result_rows)

query_create_reviews_table = """
CREATE TABLE IF NOT EXISTS reviews
(
    product_id UInt32,
    rating UInt8,
    comment Nullable(String),
    date String,
    reviewerName String,
    reviewerEmail Nullable(String)
)
ENGINE = MergeTree
ORDER BY product_id
"""

client.command(query_create_reviews_table)

#print(client.query("SHOW CREATE TABLE default.reviews").result_rows)

query_truncate_products = "TRUNCATE TABLE products"
query_truncate_reviews = "TRUNCATE TABLE reviews"

client.command(query_truncate_products)
client.command(query_truncate_reviews)

product_example = [(1, 'Essence Mascara Lash Princess', 'The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.', 'beauty', 9.99, 10.48, 2.56, 99, ['beauty', 'mascara'], 'BEA-ESS-ESS-001', 4, 15.14, 13.08, 22.99, '1 week warranty', 'Ships in 3-5 business days', 'In Stock', 'No return policy', 48, '2025-04-30T09:41:02.053Z', '2025-04-30T09:41:02.053Z', '5784719087687', 'https://cdn.dummyjson.com/public/qr-code.png', ['https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp'], 'https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp', 'Essence')]
review_example = [(1, 3, 'Would not recommend!', '2025-04-30T09:41:02.053Z', 'Eleanor Collins', 'eleanor.collins@x.dummyjson.com')]

client.insert(table="products", data=product_example)
client.insert(table="reviews", data=review_example)

print(client.query("SELECT * FROM default.products").result_rows)
print(client.query("SELECT * FROM default.reviews").result_rows)