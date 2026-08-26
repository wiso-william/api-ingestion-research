import logging 

from src.api_ingestion_research.extractors.base import BaseExtractor


logger = logging.getLogger(__name__)

class ApiExtractor(BaseExtractor):
    def __init__(self,base_url, endpoint, settings):
        super().__init__()
        self.limit = settings.limit
        self.api_base_url = base_url
        self.api_endpoint = endpoint

    def url_maker(self, skip_amount: int) -> str:
        return f"{self.api_base_url}/?limit={self.limit}&skip={skip_amount}"