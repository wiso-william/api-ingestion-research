from clickhouse_connect import get_client
import os 
from dotenv import load_dotenv

load_dotenv()

client = get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=os.getenv("CLICKHOUSE_PORT"),
    username=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD")
)

print(client.query("SHOW DATABASES").result_rows)