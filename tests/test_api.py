"""
Unit Tests for Cricbuzz API Client.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from api.client import api_client
from api.endpoints import CricbuzzEndpoints


def test_api_client_session_configured():
    """Verify API client initializes session with proper headers."""
    headers = api_client._get_headers()
    assert "X-RapidAPI-Key" in headers
    assert "X-RapidAPI-Host" in headers
    assert headers["X-RapidAPI-Host"] == "cricbuzz-cricket.p.rapidapi.com"


def test_api_endpoint_builders():
    """Verify endpoint builders create valid URLs."""
    url = CricbuzzEndpoints.match_scorecard(12345)
    assert "12345/scard" in url
