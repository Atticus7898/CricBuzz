"""
Page 2: Live Matches & Real-Time Scorecards.
"""

import streamlit as st
import pandas as pd
from services.match_service import MatchService
from utils.formatters import format_runs, format_strike_rate, format_economy

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="⚡", layout="wide")

st.title("⚡ Real-Time Cricket Telemetry & Live Scorecards")
st.markdown("Live match updates fetched from the **Cricbuzz REST API** with database synchronization.")

# Controls Header
col_btn, col_info = st.columns([1, 4])
with col_btn:
    refresh = st.button("🔄 Refresh Live Feeds", use_container_width=True)

# Fetch Matches
with st.spinner("Fetching active matches from Cricbuzz API..."):
    live_matches = MatchService.get_live_matches()

if not live_matches:
    st.warning("No matches currently in progress. Showing cached fixtures.")
else:
    # Display match summary pills
    st.markdown(f"**Found {len(live_matches)} Fixture(s)**")

    # Match Cards Grid
    match_options = {}
    cols = st.columns(min(len(live_matches), 3))

    for idx, match in enumerate(live_matches):
        col = cols[idx % len(cols)]
        m_id = match.get("match_id")
        match_desc = match.get("description", "Match")
        t1 = match.get("team1_short", "T1")
        t2 = match.get("team2_short", "T2")
        title = f"{t1} vs {t2} - {match_desc}"
        match_options[title] = m_id

        with col:
            with st.container(border=True):
                st.caption(f"🏆 {match.get('series_name', 'International Series')}")
                st.markdown(f"### {t1} ⚔️ {t2}")
                st.markdown(f"**Format:** `{match.get('format', 'T20')}` | **Status:** `{match.get('status', 'In Progress')}`")
                st.markdown(f"📍 *{match.get('venue', 'International Ground')}*")
                source_badge = "🟢 Live API" if match.get("source") == "Cricbuzz Live API" else "🗄️ Database Record"
                st.caption(f"Source: {source_badge}")

    st.divider()

    # Detailed Scorecard Viewer
    st.subheader("📋 In-Depth Match Scorecard Explorer")
    selected_label = st.selectbox("Select a Match to inspect granular scorecards:", list(match_options.keys()))
    selected_id = match_options[selected_label]

    if selected_id:
        scard = MatchService.get_match_scorecard(selected_id)
        tab_bat, tab_bowl, tab_part = st.tabs(["🏏 Batting Scorecard", "🎯 Bowling Figures", "🤝 Partnerships"])

        with tab_bat:
            batting_data = scard.get("batting", [])
            if batting_data:
                df_bat = pd.DataFrame(batting_data)
                df_bat.columns = [
                    "Batter", "Innings", "Position", "Runs", "Balls", "4s", "6s", "Strike Rate", "Dismissal"
                ]
                st.dataframe(df_bat, use_container_width=True, hide_index=True)
            else:
                st.info("Batting scorecard telemetry will populate as the innings progresses.")

        with tab_bowl:
            bowling_data = scard.get("bowling", [])
            if bowling_data:
                df_bowl = pd.DataFrame(bowling_data)
                df_bowl.columns = [
                    "Bowler", "Innings", "Overs", "Maidens", "Runs Conceded", "Wickets", "Economy", "Dots"
                ]
                st.dataframe(df_bowl, use_container_width=True, hide_index=True)
            else:
                st.info("Bowling figures will display as overs are completed.")

        with tab_part:
            part_data = scard.get("partnerships", [])
            if part_data:
                df_part = pd.DataFrame(part_data)
                df_part.columns = ["Batter 1", "Batter 2", "Partnership Runs", "Balls Faced", "Innings"]
                st.dataframe(df_part, use_container_width=True, hide_index=True)
            else:
                st.info("No recorded partnership stands for this fixture.")
