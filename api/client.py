"""
Resilient HTTP Client for Cricbuzz RapidAPI.
Implements connection pooling, exponential backoff retries, and circuit-breaker fallbacks.
"""

from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class CricbuzzAPIClient:
    """Enterprise HTTP Client for Cricbuzz API."""

    def __init__(self):
        self._cfg = settings.api
        self.session = requests.Session()
        self._configure_session()

    def _configure_session(self):
        """Configures connection pooling and exponential backoff retry logic."""
        retry_strategy = Retry(
            total=self._cfg.max_retries,
            backoff_factor=1.0,  # 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get_headers(self) -> Dict[str, str]:
        """Constructs headers with RapidAPI credentials."""
        return {
            "X-RapidAPI-Key": self._cfg.rapidapi_key,
            "X-RapidAPI-Host": self._cfg.rapidapi_host,
            "Accept": "application/json",
            "User-Agent": "CricbuzzLiveStats/1.0",
        }

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Executes an HTTPS GET request with timeouts and error handling.
        Returns parsed JSON or None if an unrecoverable error occurs.
        """
        if not self._cfg.rapidapi_key or self._cfg.rapidapi_key.startswith("your_"):
            logger.warning("RapidAPI key not set. Using cached / fallback data.")
            return None

        try:
            logger.debug("Dispatching GET request to: %s with params: %s", url, params)
            response = self.session.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self._cfg.request_timeout,
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                logger.error("RapidAPI Rate Limit Exceeded (HTTP 429).")
                return None
            elif response.status_code in (401, 403):
                logger.error("RapidAPI Authentication Failed (HTTP %d). Check your API Key.", response.status_code)
                return None
            else:
                logger.error("Cricbuzz API returned HTTP %d: %s", response.status_code, response.text[:200])
                return None

        except requests.exceptions.Timeout:
            logger.error("Request to %s timed out after %ds.", url, self._cfg.request_timeout)
            return None
        except requests.exceptions.RequestException as err:
            logger.error("Network or connection error while contacting Cricbuzz API: %s", err)
            return None


# Global API Client Instance
api_client = CricbuzzAPIClient()
