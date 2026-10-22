"""
Match Service Layer.
Coordinates live match telemetry from Cricbuzz REST API with database fallback mechanisms.
"""

from typing import List, Dict, Any, Optional
from api.client import api_client
from api.endpoints import CricbuzzEndpoints
from database.connection import db_manager
from utils.logger import get_logger

logger = get_logger(__name__)


class MatchService:
    """Provides match data, live scorecards, and historical fixture records."""

    @staticmethod
    def get_live_matches() -> List[Dict[str, Any]]:
        """
        Fetches live matches from Cricbuzz API.
        Falls back to active database match records if API is unavailable.
        """
        raw_api_data = api_client.get(CricbuzzEndpoints.MATCHES_LIVE)

        if raw_api_data and "typeMatches" in raw_api_data:
            matches = []
            try:
                for match_type in raw_api_data.get("typeMatches", []):
                    for series_wrapper in match_type.get("seriesMatches", []):
                        series_ad = series_wrapper.get("seriesAdWrapper", {})
                        for match in series_ad.get("matches", []):
                            info = match.get("matchInfo", {})
                            score = match.get("matchScore", {})
                            matches.append({
                                "match_id": info.get("matchId"),
                                "series_name": info.get("seriesName", "International Match"),
                                "description": info.get("matchDesc", "Live Match"),
                                "format": info.get("matchFormat", "T20"),
                                "status": info.get("status", "In Progress"),
                                "team1_name": info.get("team1", {}).get("teamName", "Team 1"),
                                "team1_short": info.get("team1", {}).get("teamSName", "T1"),
                                "team2_name": info.get("team2", {}).get("teamName", "Team 2"),
                                "team2_short": info.get("team2", {}).get("teamSName", "T2"),
                                "venue": f"{info.get('venueInfo', {}).get('ground', '')}, {info.get('venueInfo', {}).get('city', '')}",
                                "score_summary": str(score),
                                "source": "Cricbuzz Live API"
                            })
                if matches:
                    return matches
            except Exception as exc:
                logger.error("Error parsing Cricbuzz live matches payload: %s", exc)

        # Fallback to Database Live / In-Progress Fixtures
        logger.info("Using database match fixtures for Live Matches view.")
        query = """
            SELECT 
                m.match_id,
                s.series_name,
                m.match_description AS description,
                m.match_format AS `format`,
                m.match_status AS `status`,
                t1.team_name AS team1_name,
                t1.team_short_name AS team1_short,
                t2.team_name AS team2_name,
                t2.team_short_name AS team2_short,
                CONCAT(v.venue_name, ', ', v.city) AS venue,
                m.victory_type,
                m.victory_margin,
                'Database Store' AS source
            FROM matches m
            LEFT JOIN series s ON m.series_id = s.series_id
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            ORDER BY m.match_date DESC
            LIMIT 10;
        """
        try:
            return db_manager.fetch_all(query)
        except Exception as exc:
            logger.error("Failed to fetch matches from DB: %s", exc)
            return []

    @staticmethod
    def get_match_scorecard(match_id: int) -> Dict[str, Any]:
        """Retrieves detailed scorecard (batters, bowlers, partnerships) for a match."""
        # Query Batting Scorecards
        batting_query = """
            SELECT 
                p.player_name,
                b.innings,
                b.batting_position,
                b.runs_scored,
                b.balls_faced,
                b.fours,
                b.sixes,
                b.strike_rate,
                b.dismissal_status
            FROM batting_scorecards b
            JOIN players p ON b.player_id = p.player_id
            WHERE b.match_id = %s
            ORDER BY b.innings ASC, b.batting_position ASC;
        """

        # Query Bowling Scorecards
        bowling_query = """
            SELECT 
                p.player_name,
                bw.innings,
                bw.overs_bowled,
                bw.maidens,
                bw.runs_conceded,
                bw.wickets_taken,
                bw.economy_rate,
                bw.dot_balls
            FROM bowling_scorecards bw
            JOIN players p ON bw.player_id = p.player_id
            WHERE bw.match_id = %s
            ORDER BY bw.innings ASC, bw.wickets_taken DESC;
        """

        # Query Partnerships
        partnership_query = """
            SELECT 
                p1.player_name AS batter_1,
                p2.player_name AS batter_2,
                pr.partnership_runs,
                pr.balls_faced,
                pr.innings
            FROM partnerships pr
            JOIN players p1 ON pr.player1_id = p1.player_id
            JOIN players p2 ON pr.player2_id = p2.player_id
            WHERE pr.match_id = %s
            ORDER BY pr.innings ASC, pr.partnership_runs DESC;
        """

        try:
            batting = db_manager.fetch_all(batting_query, (match_id,))
            bowling = db_manager.fetch_all(bowling_query, (match_id,))
            partnerships = db_manager.fetch_all(partnership_query, (match_id,))
            return {
                "match_id": match_id,
                "batting": batting,
                "bowling": bowling,
                "partnerships": partnerships
            }
        except Exception as exc:
            logger.error("Error fetching match scorecard for match_id %d: %s", match_id, exc)
            return {"match_id": match_id, "batting": [], "bowling": [], "partnerships": []}
