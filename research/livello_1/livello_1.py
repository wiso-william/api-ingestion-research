import clickhouse_connect
import requests

BASE_URL = "https://api.github.com/repos/duckdb/duckdb/issues?state=all&per_page=100&page="

rows=[]

for i in range(1,50):
    url = BASE_URL+str(i)
    print(url)
    response = requests.get(url=url).json()