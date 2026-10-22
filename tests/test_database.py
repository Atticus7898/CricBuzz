"""
Unit and Integration Tests for Database Layer.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from database.connection import db_manager
from database.queries import QUERIES_REGISTRY


def test_mysql_connection():
    """Verify MySQL connection succeeds."""
    connected, msg = db_manager.test_connection()
    assert connected is True, f"Connection failed: {msg}"


def test_tables_exist():
    """Verify all 9 normalized tables exist in cricbuzz_db."""
    tables = [list(r.values())[0] for r in db_manager.fetch_all("SHOW TABLES;")]
    expected = [
        "batting_scorecards", "bowling_scorecards", "fielding_scorecards",
        "matches", "partnerships", "players", "series", "teams", "venues"
    ]
    for exp in expected:
        assert exp in tables, f"Expected table '{exp}' not found in database."


def test_all_25_queries_execute():
    """Verify that all 25 SQL queries run successfully without syntax errors."""
    for qid in sorted(QUERIES_REGISTRY.keys()):
        qdata = QUERIES_REGISTRY[qid]
        df = db_manager.fetch_dataframe(qdata["sql"])
        assert df is not None, f"Query {qid} returned None"
