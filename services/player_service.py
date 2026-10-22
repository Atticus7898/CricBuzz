"""
Player Service Layer.
Aggregates batting and bowling statistics, ICC style leaderboards, and comparative data.
"""

from typing import List, Dict, Any
import pandas as pd
from database.connection import db_manager
from utils.logger import get_logger

logger = get_logger(__name__)


class PlayerService:
    """Provides player leaderboards, form metrics, and career aggregations."""

    @staticmethod
    def get_top_batsmen(limit: int = 10) -> pd.DataFrame:
        """Retrieves top run-scorers across all matches."""
        query = """
            SELECT 
                p.player_name AS `Player`,
                t.team_short_name AS `Team`,
                COUNT(b.batting_id) AS `Innings`,
                SUM(b.runs_scored) AS `Total Runs`,
                MAX(b.runs_scored) AS `Highest Score`,
                ROUND(AVG(b.runs_scored), 2) AS `Average`,
                ROUND(AVG(b.strike_rate), 2) AS `Avg Strike Rate`,
                SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS `100s`,
                SUM(CASE WHEN b.runs_scored >= 50 AND b.runs_scored < 100 THEN 1 ELSE 0 END) AS `50s`
            FROM batting_scorecards b
            JOIN players p ON b.player_id = p.player_id
            JOIN teams t ON p.team_id = t.team_id
            GROUP BY p.player_id, p.player_name, t.team_short_name
            ORDER BY `Total Runs` DESC
            LIMIT %s;
        """
        try:
            return db_manager.fetch_dataframe(query, (limit,))
        except Exception as exc:
            logger.error("Error fetching top batsmen: %s", exc)
            return pd.DataFrame()

    @staticmethod
    def get_top_bowlers(limit: int = 10) -> pd.DataFrame:
        """Retrieves top wicket-takers across all matches."""
        query = """
            SELECT 
                p.player_name AS `Player`,
                t.team_short_name AS `Team`,
                COUNT(bw.bowling_id) AS `Innings`,
                SUM(bw.wickets_taken) AS `Wickets`,
                ROUND(AVG(bw.economy_rate), 2) AS `Economy`,
                SUM(bw.maidens) AS `Maidens`,
                SUM(bw.runs_conceded) AS `Runs Conceded`,
                SUM(CASE WHEN bw.wickets_taken >= 5 THEN 1 ELSE 0 END) AS `5W Hauls`
            FROM bowling_scorecards bw
            JOIN players p ON bw.player_id = p.player_id
            JOIN teams t ON p.team_id = t.team_id
            GROUP BY p.player_id, p.player_name, t.team_short_name
            ORDER BY `Wickets` DESC, `Economy` ASC
            LIMIT %s;
        """
        try:
            return db_manager.fetch_dataframe(query, (limit,))
        except Exception as exc:
            logger.error("Error fetching top bowlers: %s", exc)
            return pd.DataFrame()

    @staticmethod
    def get_player_role_distribution() -> pd.DataFrame:
        """Counts players by playing role for visualization."""
        query = """
            SELECT 
                role AS `Role`, 
                COUNT(*) AS `Player Count`
            FROM players
            GROUP BY role
            ORDER BY `Player Count` DESC;
        """
        try:
            return db_manager.fetch_dataframe(query)
        except Exception as exc:
            logger.error("Error fetching player role distribution: %s", exc)
            return pd.DataFrame()
