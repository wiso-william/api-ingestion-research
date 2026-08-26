"""Applico le funzioni precedenti a tutti i record, non solo 1"""

import requests
from dataclasses import dataclass, astuple
from typing import Any


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