import requests
import tenacity

import logging 
from typing import Any

from src.api_ingestion_research.utils.error_handling import is_retriable_http_error



logger = logging.getLogger(__name__)


URL = "https://dummyjson.com/products"



@tenacity.retry(
        tenacity.retry_if_exception(is_retriable_http_error), # Dico quali codici mi interessano
        stop=tenacity.stop_after_attempt(10), 
        wait=tenacity.wait_exponential(multiplier=1,min=1,max=10), # Exponential Backoff
        reraise=True # Non mi perdo l'errore e lo raisa se fallisce 
)
def extract_products(limit: int, skip_amount: int):
    response = requests.get(
        URL,
        params={"limit": limit,
                "skip" : skip_amount},
    )

    response.raise_for_status()

    return response.json()["products"]