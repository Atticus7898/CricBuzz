"""
Page 4: SQL Queries & Production Analytics Engine.
Powers the 25 SQL practice questions with live execution, query plans, and visualizations.
"""

import time
import streamlit as st
import pandas as pd
import plotly.express as px
from database.connection import db_manager
from database.queries import QUERIES_REGISTRY

st.set_page_config(page_title="SQL Analytics | Cricbuzz LiveStats", page_icon="🔍", layout="wide")

st.title("🔍 SQL Analytics & Query Execution Engine")
st.markdown("Execute and inspect all **25 production-grade SQL analytical queries** on your live MySQL database.")

# Filters: Difficulty Level
col_filter, col_select = st.columns([1, 3])

with col_filter:
    difficulty = st.selectbox(
        "Filter by Level:",
        ["All Levels", "Beginner (Q1-Q8)", "Intermediate (Q9-Q16)", "Advanced (Q17-Q25)"]
    )

# Filter queries dictionary
if difficulty == "Beginner (Q1-Q8)":
    filtered_ids = [qid for qid in sorted(QUERIES_REGISTRY.keys()) if 1 <= qid <= 8]
elif difficulty == "Intermediate (Q9-Q16)":
    filtered_ids = [qid for qid in sorted(QUERIES_REGISTRY.keys()) if 9 <= qid <= 16]
elif difficulty == "Advanced (Q17-Q25)":
    filtered_ids = [qid for qid in sorted(QUERIES_REGISTRY.keys()) if 17 <= qid <= 25]
else:
    filtered_ids = sorted(QUERIES_REGISTRY.keys())

# Question Selector
with col_select:
    question_options = {
        f"Question {qid}: {QUERIES_REGISTRY[qid]['title']} ({QUERIES_REGISTRY[qid]['level']})": qid
        for qid in filtered_ids
    }
    selected_label = st.selectbox("Select SQL Question:", list(question_options.keys()))
    selected_qid = question_options[selected_label]

query_data = QUERIES_REGISTRY[selected_qid]

# Header Metrics & Badges
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Question Number", f"Q-{selected_qid:02d}")
c2.metric("Difficulty Tier", query_data["level"])
c3.metric("Analytics Category", query_data["category"])
c4.metric("Recommended Chart", query_data["chart_type"].capitalize())

# Business Context
with st.expander("🎯 Business Problem & Architectural Context", expanded=True):
    st.write(f"**Objective:** {query_data['business_problem']}")
    st.markdown(f"**Key SQL Concepts:** `{query_data['concepts']}`")

# Run Query Against MySQL
start_time = time.perf_counter()
try:
    df_result = db_manager.fetch_dataframe(query_data["sql"])
    exec_time_ms = (time.perf_counter() - start_time) * 1000
    has_error = False
    error_msg = ""
except Exception as exc:
    has_error = True
    error_msg = str(exc)
    df_result = pd.DataFrame()
    exec_time_ms = 0

# Interactive Tabs
tab_res, tab_sql, tab_plan, tab_chart = st.tabs([
    "📊 Query Results",
    "💻 SQL Query Source",
    "⚡ MySQL Execution Plan (EXPLAIN)",
    "📈 Interactive Chart"
])

with tab_res:
    if has_error:
        st.error(f"SQL Execution Error: {error_msg}")
    else:
        st.caption(f"⚡ Query executed in **{exec_time_ms:.2f} ms** | Returned **{len(df_result)} row(s)**")
        st.dataframe(df_result, use_container_width=True, hide_index=True)

        # CSV Download Button
        csv_data = df_result.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_data,
            file_name=f"cricbuzz_q{selected_qid}_results.csv",
            mime="text/csv"
        )

with tab_sql:
    st.code(query_data["sql"].strip(), language="sql")
    st.info("Tip: You can copy and execute this exact query directly in MySQL Workbench or the `mysql` CLI.")

with tab_plan:
    st.markdown("#### MySQL Optimizer Execution Plan")
    try:
        explain_sql = f"EXPLAIN {query_data['sql']}"
        df_explain = db_manager.fetch_dataframe(explain_sql)
        st.dataframe(df_explain, use_container_width=True, hide_index=True)
    except Exception as e:
        st.warning(f"Could not generate EXPLAIN plan: {e}")

with tab_chart:
    if has_error or df_result.empty:
        st.info("No data available to visualize.")
    else:
        chart_type = query_data["chart_type"]
        cols = list(df_result.columns)

        try:
            if chart_type == "bar" and len(cols) >= 2:
                # Bar Chart
                fig = px.bar(
                    df_result,
                    x=cols[0],
                    y=cols[1],
                    title=f"{query_data['title']} (Bar Chart)",
                    text=cols[1],
                    template="plotly_white"
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "pie" and len(cols) >= 2:
                # Pie / Donut Chart
                fig = px.pie(
                    df_result,
                    names=cols[0],
                    values=cols[1],
                    hole=0.4,
                    title=f"{query_data['title']} (Distribution)",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "scatter" and len(cols) >= 3:
                # Scatter Plot
                fig = px.scatter(
                    df_result,
                    x=cols[2],
                    y=cols[3] if len(cols) > 3 else cols[1],
                    hover_name=cols[0],
                    title=f"{query_data['title']} (Correlation)",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "line" and len(cols) >= 3:
                # Line Chart for Trends
                fig = px.line(
                    df_result,
                    x=cols[1],
                    y=cols[3] if len(cols) > 3 else cols[2],
                    color=cols[0],
                    markers=True,
                    title=f"{query_data['title']} (Trend Analysis)",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("#### Table Visualization")
                st.dataframe(df_result, use_container_width=True)
        except Exception as chart_err:
            st.info("Visual chart is optional for this tabular dataset.")
