"""
Cricbuzz RapidAPI Endpoint Registry.
Provides constants and URL builders for Cricbuzz API endpoints.
"""

from config.settings import settings


class CricbuzzEndpoints:
    """Registry of Cricbuzz API routes."""
    BASE_URL = settings.api.base_url

    # Live & Matches
    MATCHES_LIVE = f"{BASE_URL}/matches/v1/live"
    MATCHES_RECENT = f"{BASE_URL}/matches/v1/recent"
    MATCHES_UPCOMING = f"{BASE_URL}/matches/v1/upcoming"

    @classmethod
    def match_scorecard(cls, match_id: int) -> str:
        """Returns the scorecard URL for a specific match ID."""
        return f"{cls.BASE_URL}/mcenter/v1/{match_id}/scard"

    @classmethod
    def match_info(cls, match_id: int) -> str:
        """Returns the match information URL."""
        return f"{cls.BASE_URL}/mcenter/v1/{match_id}/hscard"

    # Rankings
    RANKINGS_BATSMEN = f"{BASE_URL}/stats/v1/rankings/batsmen"
    RANKINGS_BOWLERS = f"{BASE_URL}/stats/v1/rankings/bowlers"
    RANKINGS_ALLROUNDERS = f"{BASE_URL}/stats/v1/rankings/allrounders"
