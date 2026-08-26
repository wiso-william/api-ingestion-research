from dataclasses import astuple
from typing import Any, Iterable

from src.api_ingestion_research.models.product import Product
from src.api_ingestion_research.models.review import Review

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


def convert_iterable_of_dataclasses_into_list_of_tuples(iterable: Iterable) -> list[tuple]:
    list_of_tuples = []
    for i in iterable:
        ituple = astuple(i)
        list_of_tuples.append(ituple)
    return list_of_tuples