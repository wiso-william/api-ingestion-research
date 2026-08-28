import clickhouse_connect
from typing import Any 
from clickhouse_connect.driver.client import Client


def create_client(settings):
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
    product_batch, reviews_batch = batches

    client.insert(table="products", data=product_batch)
    client.insert(table="reviews", data=reviews_batch)