import clickhouse_connect

from src.api_ingestion_research.connectors.base import BaseConnector



class ClickHouseConnector(BaseConnector):
    def __init__(self, settings):
        super().__init__()
        self.host = settings.clickhouse_host
        self.port = settings.clickhouse_port
        self.database = settings.clickhouse_database
        self.username = settings.clickhouse_user
        self.password = settings.clickhouse_password
        self.client = self.connect()

    def connect(self):
        """Returns a clickhouse client"""
        return clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            database=self.database,
            username=self.username,
            password=self.password
        )

    def load(self):
        pass