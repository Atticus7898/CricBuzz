"""
Page 3: Top Stats & Comparative Leaderboards.
"""

import streamlit as st
import plotly.express as px
from services.player_service import PlayerService

st.set_page_config(page_title="Top Stats | Cricbuzz LiveStats", page_icon="📊", layout="wide")

st.title("📊 Player Statistics & Comparative Leaderboards")
st.markdown("Aggregated batting, bowling, and squad performance metrics derived from verified match scorecards.")

tab_batting, tab_bowling, tab_squad = st.tabs([
    "🏏 Batting Leaderboards", 
    "🎯 Bowling Leaderboards", 
    "👥 Squad Composition & Visuals"
])

# 1. BATTING LEADERBOARD
with tab_batting:
    st.subheader("🔥 Top Run-Scorers Leaderboard")
    limit_b = st.slider("Select number of top batsmen to display:", 5, 20, 10, key="slider_bat")
    df_bat = PlayerService.get_top_batsmen(limit=limit_b)

    if not df_bat.empty:
        st.dataframe(df_bat, use_container_width=True, hide_index=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            # Bar Chart: Total Runs
            fig_runs = px.bar(
                df_bat,
                x="Player",
                y="Total Runs",
                color="Team",
                title="Top Run Scorers by Team",
                text="Total Runs",
                template="plotly_white"
            )
            fig_runs.update_traces(textposition='outside')
            st.plotly_chart(fig_runs, use_container_width=True)

        with col_b2:
            # Scatter Plot: Average vs Strike Rate
            fig_scatter = px.scatter(
                df_bat,
                x="Average",
                y="Avg Strike Rate",
                size="Total Runs",
                color="Player",
                hover_name="Player",
                title="Batting Efficiency: Average vs. Strike Rate",
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No batting records found.")

# 2. BOWLING LEADERBOARD
with tab_bowling:
    st.subheader("🎯 Top Wicket-Takers Leaderboard")
    limit_bw = st.slider("Select number of top bowlers to display:", 5, 20, 10, key="slider_bowl")
    df_bowl = PlayerService.get_top_bowlers(limit=limit_bw)

    if not df_bowl.empty:
        st.dataframe(df_bowl, use_container_width=True, hide_index=True)

        col_bw1, col_bw2 = st.columns(2)
        with col_bw1:
            fig_wickets = px.bar(
                df_bowl,
                x="Player",
                y="Wickets",
                color="Economy",
                color_continuous_scale="Viridis",
                title="Top Bowlers by Wickets (Colored by Economy)",
                text="Wickets",
                template="plotly_white"
            )
            fig_wickets.update_traces(textposition='outside')
            st.plotly_chart(fig_wickets, use_container_width=True)

        with col_bw2:
            fig_econ = px.bar(
                df_bowl.sort_values(by="Economy", ascending=True),
                x="Player",
                y="Economy",
                color="Team",
                title="Bowler Economy Rates (Lower is Better)",
                text="Economy",
                template="plotly_white"
            )
            fig_econ.update_traces(textposition='outside')
            st.plotly_chart(fig_econ, use_container_width=True)
    else:
        st.info("No bowling records found.")

# 3. SQUAD COMPOSITION
with tab_squad:
    st.subheader("👥 Squad Composition Analysis")
    df_roles = PlayerService.get_player_role_distribution()

    if not df_roles.empty:
        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            fig_pie = px.pie(
                df_roles,
                names="Role",
                values="Player Count",
                hole=0.45,
                title="Squad Playing Role Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_r2:
            st.markdown("#### Squad Balance Breakdown")
            st.dataframe(df_roles, use_container_width=True, hide_index=True)
            st.info("""
            * **Batsmen:** Anchors and top-order accumulators.
            * **Bowlers:** Primary strike & containment options.
            * **All-rounders:** Core balance providing depth in both innings.
            * **Wicket-keepers:** Key dismissals and batting resilience.
            """)
