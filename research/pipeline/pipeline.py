"""Applico le funzioni precedenti a tutti i record, non solo 1"""

import requests
from dataclasses import dataclass, astuple
from typing import Any
import clickhouse_connect
import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'https://dummyjson.com/PRODUCTS'
LIMIT = 10

def url_maker(url: str, limit: int, skip:int) -> str:
    return f"{url}/?limit={limit}&skip={skip}"


@dataclass(frozen=True)
class Product:
    id: int
    title: str
    description: str 
    category: str
    price: float
    discountPercentage: float 
    rating: float
    stock: int
    tags: list[str]
    sku: str
    weight: int
    # flat
    product_width: float 
    product_height: float 
    product_depth: float 
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    returnPolicy: str
    minimumOrderQuantity: int
    # meta: dict
    created_at: str
    updated_at: str
    barcode: str
    qr_code: str
    images: list
    thumbnail: str
    # Default
    brand: str | None = None


@dataclass(frozen=True)
class Review:
    product_id: int
    rating: int
    comment: str 
    date: str 
    reviewer_name: str
    reviewer_email: str


def transform_product(product: dict[str, Any]) -> tuple[Product, list[Review]]:
    # Cosa voglio appiattire ?
    dimensions: dict[str, float] = product["dimensions"]
    metadata: dict[str, Any] = product["meta"]

    reviews: list[dict[str, Any]] = product["reviews"]

    # dict comprehension
    flat_product = Product(
        **{ # Spacchetto il nuovo dict per avere named argument
            k: v # Valori del nuovo dict
            for k,v in product.items() # items crea pair (id, 2) (nome: Mario)
            if k not in {"dimensions", "meta", "reviews", "brand"} # Condizione + set(migliore per membership)
        },
        # Aggiungo le dimensioni che che mancano
        brand=product.get("brand"), # Non specifico il default quindi se brand non esiste è None
        product_width=dimensions["width"],
        product_height=dimensions["height"],
        product_depth=dimensions["depth"],
        # Aggiungo Metadata
        created_at=metadata["createdAt"],
        updated_at=metadata["updatedAt"],
        barcode=metadata["barcode"],
        qr_code=metadata["qrCode"]
    )

    product_reviews: list[Review] = []

    for review in reviews:
        rev = Review(
            **{
                k: v
                for (k,v) in review.items() 
                if k not in {"reviewerName", "reviewerEmail"}
                },
            product_id= flat_product.id,
            reviewer_name=review["reviewerName"],
            reviewer_email=review["reviewerEmail"]
            )
        product_reviews.append(rev)

    return flat_product, product_reviews

products = []
reviews = []
skipped = 0

while True:
    url = url_maker(BASE_URL, limit=LIMIT, skip=skipped)
    response = requests.get(url=url).json()
    if not response["products"]:
        break
    for product in response["products"]:
        flat_product, review_list = transform_product(product=product)
        products.append(flat_product)
        reviews.extend(review_list)
    skipped += LIMIT

print("Il numero di prodotti è %s", len(products))
print("Il numero di review è %s", len(reviews))

print(astuple(products[0]))
print("-----------------")
print(astuple(reviews[0]))

products_tuples = []
for product in products:
    product_tuple = astuple(product)
    products_tuples.append(product_tuple)

reviews_tuples = []
for review in reviews:
    product_review = astuple(review)
    reviews_tuples.append(product_review)


# Loading
client = clickhouse_connect.get_client(
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

client.insert(table="products", data=products_tuples)
client.insert(table="reviews", data=reviews_tuples)