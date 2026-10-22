"""
Cricbuzz LiveStats - Enterprise Cricket Analytics & Live Streaming Platform.
Main Application Entry Point.
"""

import streamlit as st
from config.settings import settings
from database.connection import db_manager

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Cricbuzz LiveStats | Cricket Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Enterprise CSS Styling
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F52BA;
    }
    /* Sidebar header */
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    /* Status Badge */
    .status-badge-online {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Sidebar Global Info & Health Diagnostics
    with st.sidebar:
        st.title("🏏 Cricbuzz LiveStats")
        st.caption("Real-Time Cricket Insights & SQL Analytics")
        st.divider()

        # Database Connection Health Check
        is_connected, msg = db_manager.test_connection()
        if is_connected:
            st.markdown('<span class="status-badge-online">🟢 MySQL 9.6 Online</span>', unsafe_allow_html=True)
            st.caption(f"Host: `{settings.db.host}:{settings.db.port}` | DB: `{settings.db.database}`")
        else:
            st.error("🔴 MySQL Disconnected")
            st.caption(msg)

        # API Status
        if settings.api.rapidapi_key and not settings.api.rapidapi_key.startswith("your_"):
            st.markdown('<span class="status-badge-online">⚡ RapidAPI Connected</span>', unsafe_allow_html=True)
            st.caption("Cricbuzz Live Telemetry Active")
        else:
            st.warning("⚠️ RapidAPI Key Missing (Using Fallbacks)")

        st.divider()
        st.markdown("**Navigation Guide**")
        st.markdown("""
        * **1 🏠 Home**: Overview & System Architecture
        * **2 ⚡ Live Matches**: Real-Time Scorecards
        * **3 📊 Top Stats**: Batting & Bowling Records
        * **4 🔍 SQL Analytics**: 25 Production Queries
        * **5 🛠️ CRUD Operations**: Database Management
        """)
        st.divider()
        st.caption("Engineered for Production Sports Analytics.")

    # Redirect / Landing Page
    st.title("🏏 Welcome to Cricbuzz LiveStats")
    st.markdown("### Real-Time Insights & SQL-Based Analytics Platform")
    st.info("👈 **Select a page from the sidebar** to start exploring live matches, query analytics, or manage cricket data.")

    # Quick metrics summary
    try:
        col1, col2, col3, col4 = st.columns(4)
        total_players = db_manager.fetch_one("SELECT COUNT(*) AS c FROM players;")['c']
        total_matches = db_manager.fetch_one("SELECT COUNT(*) AS c FROM matches;")['c']
        total_venues = db_manager.fetch_one("SELECT COUNT(*) AS c FROM venues;")['c']
        total_series = db_manager.fetch_one("SELECT COUNT(*) AS c FROM series;")['c']

        col1.metric("Registered Players", total_players)
        col2.metric("Recorded Matches", total_matches)
        col3.metric("World Venues", total_venues)
        col4.metric("Active Tournaments", total_series)
    except Exception as exc:
        st.warning(f"Could not load overview telemetry: {exc}")


if __name__ == "__main__":
    main()
