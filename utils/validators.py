"""
Input Validation and Data Sanitization Utilities.
Protects application integrity and database constraints.
"""

from typing import Tuple, List, Optional
import re

ALLOWED_ROLES = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
ALLOWED_FORMATS = ["Test", "ODI", "T20I", "T20"]
ALLOWED_TOSS_DECISIONS = ["bat", "bowl"]
ALLOWED_VICTORY_TYPES = ["runs", "wickets", "tie", "no result"]


def validate_player_data(
    player_name: str,
    team_id: int,
    role: str,
    batting_style: str,
    bowling_style: str = "None"
) -> Tuple[bool, List[str]]:
    """
    Validates player input fields before database persistence.
    Returns (is_valid, error_messages).
    """
    errors = []

    # Name validation
    cleaned_name = player_name.strip()
    if not cleaned_name:
        errors.append("Player name cannot be empty.")
    elif len(cleaned_name) < 3 or len(cleaned_name) > 100:
        errors.append("Player name must be between 3 and 100 characters.")
    elif not re.match(r"^[A-Za-z\s\.\'\-]+$", cleaned_name):
        errors.append("Player name contains invalid special characters.")

    # Team ID validation
    if not isinstance(team_id, int) or team_id <= 0:
        errors.append("Valid team selection is required.")

    # Role validation
    if role not in ALLOWED_ROLES:
        errors.append(f"Role must be one of: {', '.join(ALLOWED_ROLES)}.")

    # Batting style validation
    if not batting_style.strip():
        errors.append("Batting style cannot be empty.")

    return (len(errors) == 0, errors)


def validate_match_data(
    match_description: str,
    match_format: str,
    match_date: str,
    team1_id: int,
    team2_id: int,
    venue_id: int,
    toss_decision: Optional[str] = None,
    victory_margin: Optional[int] = None,
    victory_type: Optional[str] = None,
) -> Tuple[bool, List[str]]:
    """Validates match input data."""
    errors = []

    if not match_description.strip():
        errors.append("Match description is required.")

    if match_format not in ALLOWED_FORMATS:
        errors.append(f"Format must be one of: {', '.join(ALLOWED_FORMATS)}.")

    if team1_id == team2_id:
        errors.append("Team 1 and Team 2 must be different teams.")

    if venue_id <= 0:
        errors.append("Valid venue must be selected.")

    if toss_decision and toss_decision not in ALLOWED_TOSS_DECISIONS:
        errors.append("Toss decision must be 'bat' or 'bowl'.")

    if victory_margin is not None and victory_margin < 0:
        errors.append("Victory margin cannot be negative.")

    if victory_type and victory_type not in ALLOWED_VICTORY_TYPES:
        errors.append(f"Victory type must be one of: {', '.join(ALLOWED_VICTORY_TYPES)}.")

    return (len(errors) == 0, errors)
