"""
Page 1: Home & Platform Overview.
"""

import streamlit as st
from database.connection import db_manager

st.set_page_config(page_title="Home | Cricbuzz LiveStats", page_icon="🏠", layout="wide")

st.title("🏏 Cricbuzz LiveStats Platform")
st.subheader("Enterprise Sports Analytics, Live Feeds & SQL Knowledge Engine")

st.markdown("""
Welcome to **Cricbuzz LiveStats**, an end-to-end data engineering and analytics application 
integrating real-time telemetric feeds from the **Cricbuzz REST API** with a high-performance **MySQL 8.0/9.0 Relational Engine**.
""")

st.divider()

# High-Level KPIs
col1, col2, col3, col4 = st.columns(4)
try:
    p_cnt = db_manager.fetch_one("SELECT COUNT(*) AS c FROM players;")['c']
    m_cnt = db_manager.fetch_one("SELECT COUNT(*) AS c FROM matches;")['c']
    v_cnt = db_manager.fetch_one("SELECT COUNT(*) AS c FROM venues;")['c']
    q_cnt = 25

    col1.metric("🏏 Players in RDBMS", p_cnt, "+5 Formats")
    col2.metric("🏟️ Matches Cataloged", m_cnt, "2021-2024")
    col3.metric("📍 International Venues", v_cnt, "Global")
    col4.metric("🔍 SQL Queries Ready", q_cnt, "100% Tested")
except Exception as e:
    st.info("MySQL connection active.")

st.divider()

# Business Use Cases
st.markdown("### 💼 Real-World Business Applications")
c1, c2 = st.columns(2)

with c1:
    with st.expander("📺 1. Sports Media & Broadcasting", expanded=True):
        st.write("""
        * Real-time match telemetry for live commentary overlays.
        * Automated player form cards and head-to-head records during pre-match discussions.
        * Instant milestone tracking (centuries, 5-wicket hauls, strike rate trends).
        """)

    with st.expander("🎮 2. Fantasy Cricket Platforms", expanded=True):
        st.write("""
        * Player momentum tracking using 5-match and 10-match rolling averages.
        * Venue-specific pitch dynamics (average economy rate, boundary frequency).
        * Toss advantage models conditioned on team composition.
        """)

    with c2:
        with st.expander("📈 3. Cricket Analytics & Team Management", expanded=True):
            st.write("""
            * Multi-dimensional ranking algorithm weighing batting, bowling, and fielding.
            * Pressure-situation evaluation (performance in close matches < 50 runs / < 5 wickets).
            * Time-series career trajectory classification using window functions (`LAG()`).
            """)

        with st.expander("🎓 4. Educational & Academic Benchmarking", expanded=True):
            st.write("""
            * Production demonstration of 3rd Normal Form (3NF) relational database design.
            * Hands-on laboratory for complex SQL (CTEs, Window Functions, DENSE_RANK).
            * Robust API client implementation with exponential backoff and circuit breakers.
            """)

st.divider()

# Architecture & Clean Design
st.markdown("### 🏗️ Technical Architecture & Flow")
st.markdown("""
```text
┌─────────────────────────┐      ┌──────────────────────────┐      ┌────────────────────────┐
│  Presentation Layer     │ ───► │  Business / Service      │ ───► │  Persistence / DB      │
│  - Streamlit Multi-Page │      │  - MatchService          │      │  - MySQL 9.6 Server    │
│  - Plotly Visuals       │      │  - PlayerService         │      │  - PyMySQL Connection  │
│  - Form-based CRUD      │      │  - CRUDService           │      │    Pool & Transactions │
└─────────────────────────┘      └────────────┬─────────────┘      └────────────────────────┘
                                              │
                                              ▼
                                 ┌──────────────────────────┐
                                 │  External REST API       │
                                 │  - Cricbuzz via RapidAPI │
                                 │  - Resilient HTTP Client │
                                 └──────────────────────────┘
```
""")

st.info("👉 Use the sidebar to navigate to **⚡ Live Matches**, **📊 Top Stats**, **🔍 SQL Analytics**, or **🛠️ CRUD Operations**.")
