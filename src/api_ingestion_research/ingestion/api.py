import requests
import tenacity

import logging 
from typing import Any

from src.api_ingestion_research.utils.error_handling import is_retriable_http_error



logger = logging.getLogger(__name__)


URL = "https://dummyjson.com/products"



@tenacity.retry(
    retry=tenacity.retry_if_exception(is_retriable_http_error),
    stop=tenacity.stop_after_attempt(10),
    wait=tenacity.wait_exponential(
        multiplier=1,
        min=1,
        max=10,
    ),
    reraise=True,
)
def extract_products(limit: int, skip_amount: int):
    """Extracts a page of products from the API.

    Args:
        limit: Maximum number of products to retrieve.
        skip_amount: Number of products to skip before retrieving the page.

    Returns:
        A list of products returned by the API.

    Raises:
        requests.HTTPError: If the API returns an unsuccessful HTTP status.
    """
    response = requests.get(
        URL,
        params={"limit": limit,
                "skip" : skip_amount},
    )

    response.raise_for_status()

    return response.json()["products"] 