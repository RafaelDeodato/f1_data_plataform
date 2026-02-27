import requests
from app.core.logger import setup_logger, get_logger
import time

class OpenF1Client:
    def __init__(self):
        self.logger = get_logger(__name__)

        self.base_url = "https://api.openf1.org/v1/"
        self.timeout = 10

        self.logger.info("Openf1Client initialized with base URL: %s", self.base_url)

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

    def get_meetings_by_season(self, season: int):
        url = f"meetings?year={season}"
        self.logger.info(f"Fetching meetings for season {season} on OpenF1 API with URL: {self.base_url + url}")
        return self._get(f"meetings?year={season}")
    
    def get_sessions_by_meeting(self, meeting_id: int):
        url = f"sessions?meeting_key={meeting_id}"
        self.logger.info(f"Fetching sessions for meeting {meeting_id} on OpenF1 API with URL: {self.base_url + url}")
        return self._get(url)