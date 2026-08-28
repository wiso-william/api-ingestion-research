from collections.abc import Iterator
from dataclasses import astuple
from typing import Any, Iterable

from src.api_ingestion_research.models.product import Product
from src.api_ingestion_research.models.review import Review
from src.api_ingestion_research.ingestion.api import extract_products

def transform_product(product: dict[str, Any]) -> Iterator[
    tuple[
        tuple[Any, ...],
        list[tuple[Any, ...]]
    ]
]:
    """Transforms a raw product into flattened product and review records.

    Args:
        product: Raw product data returned by the API.

    Yields:
        A tuple containing the flattened product record and a list of
        associated review records.
    """
    dimensions: dict[str, float] = product["dimensions"]
    metadata: dict[str, Any] = product["meta"]

    reviews: list[dict[str, Any]] = product["reviews"]

    flat_product = Product(
        **{ 
            k: v 
            for k,v in product.items() 
            if k not in {"dimensions", "meta", "reviews", "brand"} 
        },
        brand=product.get("brand"), 
        product_width=dimensions["width"],
        product_height=dimensions["height"],
        product_depth=dimensions["depth"],
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


def batcher(limit: int = 10, skip_amount: int = 0, batch_amount: int = 50) -> Iterator[
    tuple[
        list[tuple[Any, ...]],
        list[tuple[Any, ...]],
        int,
    ]
]:
    """Creates batches of tuples ready to be loaded.

    This function reads data from the API and fills both product and review
    batches since they are coupled. Once the batch reaches the configured
    size, it yields the batches together with the offset to use for the next
    API request.

    Args:
        limit: Maximum number of records per API page.
        skip_amount: Number of records to skip before retrieving the first
            API page.
        batch_amount: Maximum number of products in each batch.

    Yields:
        A tuple containing the product batch, the review batch, and the
        offset to use for the next API request.
    """
    product_batch = []
    reviews_batch = []

    while True:
        products_received = 0

        for product in extract_products(limit=limit, skip_amount=skip_amount):
            products_received += 1

            for flat_product, product_reviews in transform_product(product=product):
                product_batch.append(flat_product)
                reviews_batch.extend(product_reviews)

        skip_amount += products_received

        if len(product_batch) >= batch_amount:
            yield product_batch, reviews_batch, skip_amount

            product_batch = list()
            reviews_batch = list() 

        if products_received < limit:
            if product_batch:
                yield product_batch, reviews_batch, skip_amount

            break