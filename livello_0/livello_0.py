import clickhouse_connect
import requests

BASE_URL = "https://api.github.com/repos/duckdb/duckdb/issues?state=all&per_page=100"

response = requests.get(BASE_URL).json()

rows = []

for issue in response:
    row = (issue["id"], issue["url"], issue["repository_url"])
    rows.append(row) 

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password=""
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