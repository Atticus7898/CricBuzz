"""
CRUD Service Layer for Cricbuzz LiveStats.
Provides atomic, validated Create, Read, Update, and Delete operations on MySQL database.
"""

from typing import List, Dict, Any, Optional, Tuple
from database.connection import db_manager
from utils.validators import validate_player_data, validate_match_data
from utils.logger import get_logger

logger = get_logger(__name__)


class CRUDService:
    """Service handling administrative CRUD operations on Players and Matches."""

    # -------------------------------------------------------------------------
    # PLAYER CRUD
    # -------------------------------------------------------------------------
    @staticmethod
    def get_all_players() -> List[Dict[str, Any]]:
        """Retrieves all players with their associated team names."""
        query = """
            SELECT 
                p.player_id,
                p.player_name,
                t.team_name,
                p.team_id,
                p.role,
                p.batting_style,
                p.bowling_style,
                p.date_of_birth,
                p.created_at
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.player_name ASC;
        """
        return db_manager.fetch_all(query)

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[Dict[str, Any]]:
        """Fetches a single player record by ID."""
        query = "SELECT * FROM players WHERE player_id = %s;"
        return db_manager.fetch_one(query, (player_id,))

    @staticmethod
    def create_player(
        player_name: str,
        team_id: int,
        role: str,
        batting_style: str,
        bowling_style: str = "None",
        date_of_birth: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Validates and creates a new player record."""
        is_valid, errors = validate_player_data(player_name, team_id, role, batting_style, bowling_style)
        if not is_valid:
            return False, " | ".join(errors)

        try:
            query = """
                INSERT INTO players (player_name, team_id, role, batting_style, bowling_style, date_of_birth)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            new_id = db_manager.execute_write(
                query,
                (player_name.strip(), team_id, role, batting_style.strip(), bowling_style.strip() or "None", date_of_birth)
            )
            logger.info("Successfully created player '%s' with ID %d.", player_name, new_id)
            return True, f"Player '{player_name}' added successfully (ID: {new_id})."
        except Exception as exc:
            logger.error("Failed to insert player: %s", exc)
            return False, f"Database error: {str(exc)}"

    @staticmethod
    def update_player(
        player_id: int,
        player_name: str,
        team_id: int,
        role: str,
        batting_style: str,
        bowling_style: str = "None",
        date_of_birth: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Validates and updates an existing player record."""
        is_valid, errors = validate_player_data(player_name, team_id, role, batting_style, bowling_style)
        if not is_valid:
            return False, " | ".join(errors)

        try:
            query = """
                UPDATE players
                SET player_name = %s,
                    team_id = %s,
                    role = %s,
                    batting_style = %s,
                    bowling_style = %s,
                    date_of_birth = %s
                WHERE player_id = %s;
            """
            affected = db_manager.execute_write(
                query,
                (player_name.strip(), team_id, role, batting_style.strip(), bowling_style.strip() or "None", date_of_birth, player_id)
            )
            if affected > 0:
                logger.info("Updated player ID %d successfully.", player_id)
                return True, f"Player ID {player_id} updated successfully."
            return False, "No player found with that ID or no changes detected."
        except Exception as exc:
            logger.error("Failed to update player ID %d: %s", player_id, exc)
            return False, f"Database error: {str(exc)}"

    @staticmethod
    def delete_player(player_id: int) -> Tuple[bool, str]:
        """Safely deletes a player if no foreign key constraints are violated."""
        try:
            query = "DELETE FROM players WHERE player_id = %s;"
            affected = db_manager.execute_write(query, (player_id,))
            if affected > 0:
                logger.info("Deleted player ID %d.", player_id)
                return True, f"Player ID {player_id} deleted successfully."
            return False, "Player not found."
        except Exception as exc:
            logger.error("Failed to delete player ID %d: %s", player_id, exc)
            return False, f"Cannot delete player: Active scorecard or match records depend on this player. ({str(exc)})"

    # -------------------------------------------------------------------------
    # TEAMS & VENUES HELPERS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_teams_list() -> List[Dict[str, Any]]:
        """Returns list of teams for selectboxes."""
        return db_manager.fetch_all("SELECT team_id, team_name, team_short_name FROM teams ORDER BY team_name ASC;")

    @staticmethod
    def get_venues_list() -> List[Dict[str, Any]]:
        """Returns list of venues for selectboxes."""
        return db_manager.fetch_all("SELECT venue_id, venue_name, city, country, capacity FROM venues ORDER BY venue_name ASC;")
