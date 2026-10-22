"""
Unit Tests for Validation and CRUD Operations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils.validators import validate_player_data, validate_match_data
from services.crud_service import CRUDService


def test_player_validation_valid():
    """Verify valid player payload passes."""
    is_valid, errors = validate_player_data("Sanju Samson", 1, "Wicket-keeper", "Right-hand bat")
    assert is_valid is True
    assert len(errors) == 0


def test_player_validation_invalid_role():
    """Verify invalid role fails validation."""
    is_valid, errors = validate_player_data("Player X", 1, "Cheerleader", "Right-hand bat")
    assert is_valid is False
    assert any("Role must be one of" in e for e in errors)


def test_player_validation_short_name():
    """Verify name less than 3 chars fails validation."""
    is_valid, errors = validate_player_data("AB", 1, "Batsman", "Right-hand bat")
    assert is_valid is False
    assert any("between 3 and 100 characters" in e for e in errors)


def test_crud_create_read_delete_cycle():
    """Verify complete Create -> Read -> Delete lifecycle."""
    test_name = "Test Junior Player"
    success, msg = CRUDService.create_player(
        player_name=test_name,
        team_id=1,
        role="Batsman",
        batting_style="Right-hand bat"
    )
    assert success is True, f"Failed to create: {msg}"

    # Verify presence in DB
    players = CRUDService.get_all_players()
    created_list = [p for p in players if p["player_name"] == test_name]
    assert len(created_list) >= 1
    new_player_id = created_list[0]["player_id"]

    # Delete test player
    del_success, del_msg = CRUDService.delete_player(new_player_id)
    assert del_success is True, f"Failed to delete: {del_msg}"
