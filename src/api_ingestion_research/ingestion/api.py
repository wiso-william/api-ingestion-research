import requests

import logging 



logger = logging.getLogger(__name__)


URL = "https://dummyjson.com/products"


def extract_products(limit: int, skip_amount: int):
    response = requests.get(
        URL,
        params={"limit": limit,
                "skip" : skip_amount},
    )

    response.raise_for_status()

    return response.json()["products"]