from dataclasses import astuple
from typing import Any, Iterable

from src.api_ingestion_research.models.product import Product
from src.api_ingestion_research.models.review import Review
from crs.api_ingestion_generators.ingestion.api import extract_products

def transform_product(product: dict[str, Any]):
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

    product_reviews: list[tuple] = []

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
        product_reviews.append(astuple(rev))


    yield astuple(flat_product), product_reviews


def burba(limit: int = 10, skip_amount:int = 0, batch_amount: int = 50):
    product_batch = []
    reviews_batch = []

    while True:

        for product in extract_products(limit=limit, skip_amount=skip_amount):
            # Questo è inutile perchè quando finisce lo stream il for termina da solo
            # if not product:
            #     yield product_batch, reviews_batch
            #     product_batch = []
            #     reviews_batch = []
            #     break

            for flat_product, product_reviews in transform_product(product=product):
                product_batch.append(flat_product)
                reviews_batch.extend(product_reviews)

        if len(product_batch) >= batch_amount:
            yield product_batch, reviews_batch
            product_batch = list()
            reviews_batch = list()  

        skip_amount += limit