"""
Page 5: Administrative CRUD Operations.
Enables validated Create, Read, Update, and Delete operations on the live MySQL database.
"""

import streamlit as st
import pandas as pd
from services.crud_service import CRUDService
from utils.validators import ALLOWED_ROLES

st.set_page_config(page_title="CRUD Operations | Cricbuzz LiveStats", page_icon="🛠️", layout="wide")

st.title("🛠️ Database CRUD Management Module")
st.markdown("Perform validated administrative operations on Player and Match datasets in **MySQL 9.6**.")

# Fetch Teams & Venues for Dropdowns
teams = CRUDService.get_teams_list()
team_dict = {f"{t['team_name']} ({t['team_short_name']})": t["team_id"] for t in teams}

crud_tabs = st.tabs([
    "📋 View / Read Players",
    "➕ Add New Player (Create)",
    "✏️ Edit Player (Update)",
    "🗑️ Delete Player (Delete)"
])

# -----------------------------------------------------------------------------
# TAB 1: READ PLAYERS
# -----------------------------------------------------------------------------
with crud_tabs[0]:
    st.subheader("📋 Active Player Database")
    players = CRUDService.get_all_players()

    if players:
        df_players = pd.DataFrame(players)
        # Search & Filter controls
        c_search, c_role = st.columns([2, 1])
        with c_search:
            search_query = st.text_input("🔍 Search by player name:", "")
        with c_role:
            role_filter = st.selectbox("Filter by Role:", ["All Roles"] + ALLOWED_ROLES)

        filtered_df = df_players.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df["player_name"].str.contains(search_query, case=False, na=False)]
        if role_filter != "All Roles":
            filtered_df = filtered_df[filtered_df["role"] == role_filter]

        st.caption(f"Displaying **{len(filtered_df)}** of **{len(df_players)}** players")
        st.dataframe(
            filtered_df[[
                "player_id", "player_name", "team_name", "role", 
                "batting_style", "bowling_style", "date_of_birth"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No player records found.")

# -----------------------------------------------------------------------------
# TAB 2: CREATE PLAYER
# -----------------------------------------------------------------------------
with crud_tabs[1]:
    st.subheader("➕ Register New Player")
    with st.form("create_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name*", placeholder="e.g. Jasprit Bumrah")
            new_team = st.selectbox("Team*", list(team_dict.keys()))
            new_role = st.selectbox("Playing Role*", ALLOWED_ROLES)
        with col2:
            new_batting = st.selectbox(
                "Batting Style*",
                ["Right-hand bat", "Left-hand bat"]
            )
            new_bowling = st.text_input("Bowling Style", placeholder="e.g. Right-arm fast, Legbreak, or None")
            new_dob = st.date_input("Date of Birth", value=None)

        submitted_create = st.form_submit_button("🚀 Add Player to Database", use_container_width=True)

        if submitted_create:
            dob_str = str(new_dob) if new_dob else None
            success, msg = CRUDService.create_player(
                player_name=new_name,
                team_id=team_dict[new_team],
                role=new_role,
                batting_style=new_batting,
                bowling_style=new_bowling or "None",
                date_of_birth=dob_str
            )
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

# -----------------------------------------------------------------------------
# TAB 3: UPDATE PLAYER
# -----------------------------------------------------------------------------
with crud_tabs[2]:
    st.subheader("✏️ Update Existing Player Details")
    players = CRUDService.get_all_players()

    if players:
        player_lookup = {f"{p['player_name']} (ID: {p['player_id']}, {p['team_name']})": p for p in players}
        selected_player_label = st.selectbox("Select Player to Edit:", list(player_lookup.keys()))
        current_data = player_lookup[selected_player_label]

        with st.form("update_player_form"):
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                up_name = st.text_input("Full Name*", value=current_data["player_name"])
                # Locate index for current team
                team_keys = list(team_dict.keys())
                curr_team_idx = 0
                for i, k in enumerate(team_keys):
                    if team_dict[k] == current_data["team_id"]:
                        curr_team_idx = i
                        break
                up_team = st.selectbox("Team*", team_keys, index=curr_team_idx)
                role_idx = ALLOWED_ROLES.index(current_data["role"]) if current_data["role"] in ALLOWED_ROLES else 0
                up_role = st.selectbox("Playing Role*", ALLOWED_ROLES, index=role_idx)

            with col_u2:
                bat_options = ["Right-hand bat", "Left-hand bat"]
                bat_idx = 0 if "Right" in current_data["batting_style"] else 1
                up_bat = st.selectbox("Batting Style*", bat_options, index=bat_idx)
                up_bowl = st.text_input("Bowling Style", value=current_data["bowling_style"] or "None")

            submitted_update = st.form_submit_button("💾 Save Player Changes", use_container_width=True)

            if submitted_update:
                success, msg = CRUDService.update_player(
                    player_id=current_data["player_id"],
                    player_name=up_name,
                    team_id=team_dict[up_team],
                    role=up_role,
                    batting_style=up_bat,
                    bowling_style=up_bowl,
                    date_of_birth=str(current_data["date_of_birth"]) if current_data.get("date_of_birth") else None
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.info("No players available to edit.")

# -----------------------------------------------------------------------------
# TAB 4: DELETE PLAYER
# -----------------------------------------------------------------------------
with crud_tabs[3]:
    st.subheader("🗑️ Remove Player from Database")
    players = CRUDService.get_all_players()

    if players:
        del_lookup = {f"{p['player_name']} (ID: {p['player_id']}, {p['team_name']})": p["player_id"] for p in players}
        del_label = st.selectbox("Select Player to Delete:", list(del_lookup.keys()), key="del_select")
        del_id = del_lookup[del_label]

        st.warning("⚠️ Warning: Deleting a player is permanent. Players with existing scorecard records are protected by foreign key constraints.")
        confirm_check = st.checkbox("I confirm that I want to delete this player permanently.")

        if st.button("🚨 Delete Player Record", type="primary"):
            if not confirm_check:
                st.error("Please check the confirmation box before deleting.")
            else:
                success, msg = CRUDService.delete_player(del_id)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.info("No players available to delete.")
