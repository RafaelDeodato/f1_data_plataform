import requests
from app.core.logger import setup_logger, get_logger
import time

class JolpicaClient:
    def __init__(self):
        self.logger = get_logger(__name__)

        self.base_url = "https://api.jolpi.ca/ergast/f1/"
        self.timeout = 10

        self.logger.info("JolpicaClient initialized with base URL: %s", self.base_url)

    def _get(self, endpoint: str, params: dict = None):
        url = self.base_url + endpoint
        max_retries = 5

        for attempt in range(max_retries):
            response = requests.get(
                url, 
                timeout=self.timeout, 
                params=params
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                wait_time = 2 ** attempt

                self.logger.warning("API rate limit exceeded. Retrying in %d seconds... (Attempt %d/%d)", wait_time, attempt + 1, max_retries)
                time.sleep(wait_time)
            else:
                response.raise_for_status()
                
        raise Exception(f"Failed to fetch data from {url} after {max_retries} attempts due to rate limiting.")
    
    def _get_paginated(self, endpoint: str, data_path: list[str], limit: int = 100):
        all_data = []
        offset = 0

        data = self._get(endpoint, {"limit": limit, "offset": offset})

        mrData = data["MRData"]
        total = int(mrData["total"])

        items = data
        for key in data_path:
            items = items[key]

        all_data.extend(items)

        if total <= limit:
            return all_data
        
        offset += limit

        while offset < total:
            data = self._get(endpoint, {"limit": limit, "offset": offset})

            items = data
            for key in data_path:
                items = items[key]

            all_data.extend(items)

            offset += limit

        return all_data

    def get_season(self, year: int):
        self.logger.info("Fetching season data for year: %d. On Jolpica API", year)
        return self._get(f"{year}/")
    
    def get_all_seasons(self):
        self.logger.info("Fetching all seasons data on Jolpica API")
        return self._get_paginated("seasons", ["MRData", "SeasonTable", "Seasons"])
    
    def get_all_circuits(self):
        self.logger.info("Fetching all circuits data on Jolpica API")
        return self._get_paginated("circuits", ["MRData", "CircuitTable", "Circuits"])
    
    def get_all_races(self, year: int):
        self.logger.info("Fetching all races data for year: %d. On Jolpica API", year)
        return self._get_paginated(f"{year}/races", ["MRData", "RaceTable", "Races"])



