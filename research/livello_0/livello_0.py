from clickhouse_connect import get_client
import os 
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = "https://api.github.com/repos/duckdb/duckdb/issues?state=all&per_page=100"

response = requests.get(BASE_URL).json()

rows = []

for issue in response:
    row = (issue["id"], issue["url"], issue["repository_url"])
    rows.append(row) 

client = get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=os.getenv("CLICKHOUSE_PORT"),
    username=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD")
)

client.command("""
    CREATE TABLE IF NOT EXISTS github_test
    (
        id UInt64,
        url String,
        repository_url String
    )
    ENGINE = MergeTree
    ORDER BY id
""")

client.insert(table="github_test", data=rows, column_names=["id", "url", "repository_url"])

rn = client.query("SELECT COUNT(1) FROM default.github_test").first_row

print(rn)