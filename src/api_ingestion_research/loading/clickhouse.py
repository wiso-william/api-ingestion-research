import clickhouse_connect
from typing import Any 
from clickhouse_connect.driver.client import Client

from src.api_ingestion_research.settings.config import Settings


def create_client(settings: Settings) -> Client:
    """Creates a ClickHouse client using the provided settings.

    Args:
        settings: Application settings containing the ClickHouse connection
            parameters.

    Returns:
        A configured ClickHouse client.
    """
    return clickhouse_connect.get_client(
        host=settings.clickhouse_host,
        port=settings.clickhouse_port,
        database=settings.clickhouse_database,
        username=settings.clickhouse_user,
        password=settings.clickhouse_password,
    )


def load_batches(client: Client, 
                 batches: tuple[
                     list[tuple[Any, ...]], 
                     list[tuple[Any, ...]]
                     ]) -> None:
    """Loads product and review batches into ClickHouse.

    Args:
        client: ClickHouse client used to insert the batches.
        batches: A tuple containing the product batch and review batch.
    """
    product_batch, reviews_batch = batches

    client.insert(table="products", data=product_batch)
    client.insert(table="reviews", data=reviews_batch)