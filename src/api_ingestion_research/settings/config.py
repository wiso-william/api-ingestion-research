import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.clickhouse_host: str = os.environ["CLICKHOUSE_HOST"]
        self.clickhouse_port: int = int(os.environ["CLICKHOUSE_PORT"])
        self.clickhouse_database: str = os.environ["CLICKHOUSE_DATABASE"]
        self.clickhouse_user: str = os.environ["CLICKHOUSE_USER"]
        self.clickhouse_password: str = os.environ["CLICKHOUSE_PASSWORD"]

        self.limit: int = int(os.environ["LIMIT"])
        self.batch_amount: int = int(os.environ["BATCH_AMOUNT"]) 

settings = Settings()