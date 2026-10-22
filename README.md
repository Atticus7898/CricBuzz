# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%20%2F%209.0-orange.svg)](https://www.mysql.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Tests-Passing%20(9%2F9)-brightgreen.svg)](https://docs.pytest.org/)

An enterprise-grade sports analytics platform that ingests real-time telemetric feeds from the **Cricbuzz REST API** (via RapidAPI), normalizes and persists data into an ACID-compliant **MySQL 8.0/9.0 Relational Database** (3NF), and renders an interactive multi-page web application in **Streamlit**.

---

## 📌 Table of Contents
1. [Business Problem & Objective](#-business-problem--objective)
2. [Multi-Tier Architecture](#-multi-tier-architecture)
3. [Database Design & 3NF Normalization](#-database-design--3nf-normalization)
4. [Live Cricbuzz API Integration](#-live-cricbuzz-api-integration)
5. [The 25 SQL Analytics Engine](#-the-25-sql-analytics-engine)
6. [Interactive Streamlit Multi-Page UI](#-interactive-streamlit-multi-page-ui)
7. [Installation & Quickstart Guide](#-installation--quickstart-guide)
8. [Automated Testing](#-automated-testing)
9. [Comprehensive 50 Interview & Viva Questions](#-comprehensive-50-interview--viva-questions)

---

## 🎯 Business Problem & Objective
Cricket matches generate multi-dimensional telemetry (ball-by-ball events, player career trajectories, venue characteristics, and toss dynamics). However:
* Live feeds sit in siloed third-party JSON APIs without relational querying capabilities.
* Historical records require complex analytical processing (window functions, conditional aggregations, partnership metrics).
* Non-technical team analysts lack administrative CRUD tools to curate and audit player statistics.

**Cricbuzz LiveStats** resolves this by delivering:
* **⚡ Real-Time Live Match Updates** directly from Cricbuzz.
* **🗄️ Normalized 3NF MySQL Database** supporting complex relational joins.
* **🔍 25 Production-Grade SQL Analytical Queries** (Beginner, Intermediate, Advanced).
* **🛠️ Form-based Transactional CRUD Operations** with input validation and audit feedback.
* **📊 Modern Data Visualizations** powered by Plotly and Streamlit.

---

## 🏗️ Multi-Tier Architecture

```text
cricbuzz_livestats/
├── app.py                    # Main navigation router & health diagnostics
├── config/                   # Centralized configuration (12-Factor App)
│   └── settings.py
├── database/                 # Persistence Layer (MySQL 8.0/9.0)
│   ├── schema.sql            # Master 3NF DDL (PK/FK, constraints, generated columns)
│   ├── seed_data.sql         # Curated international cricket dataset
│   ├── connection.py         # PyMySQL connection pool & transaction manager
│   ├── queries.py            # Central registry of 25 SQL queries & metadata
│   └── init_db.py            # Automated DB creation & migration script
├── api/                      # External API Integration Layer
│   ├── endpoints.py          # Cricbuzz API routes registry
│   └── client.py             # Requests session with retries & circuit breaker
├── services/                 # Core Business Logic Layer
│   ├── match_service.py      # Live match extraction & scorecard parsing
│   ├── player_service.py     # Aggregated leaderboards & rankings
│   └── crud_service.py       # Validated transactional CRUD on players & matches
├── pages/                    # Presentation Layer (Streamlit Multi-Page)
│   ├── 1_🏠_Home.py          # Business use cases, architecture, KPIs
│   ├── 2_⚡_Live_Matches.py  # Real-time scorecards, bats/bowlers
│   ├── 3_📊_Top_Stats.py     # Interactive leaderboards & Plotly charts
│   ├── 4_🔍_SQL_Analytics.py # 25-Question SQL runner, EXPLAIN plans & charts
│   └── 5_🛠️_CRUD_Operations.py# Form-based player creation, edit, and deletion
├── utils/                    # Shared Utilities
│   ├── logger.py             # Rotating file & console logging
│   ├── validators.py         # Form input sanitation & constraint checks
│   └── formatters.py         # Formatting for dates, strike rates, economy
└── tests/                    # Pytest Test Suite
    ├── test_database.py      # Connection & query execution tests
    ├── test_api.py           # API client tests
    └── test_crud.py          # Validation & CRUD transactional tests
```

---

## 🗄️ Database Design & 3NF Normalization
The database schema (`cricbuzz_db`) models 9 relational entities:
1. `teams` - Country, team name, and short code.
2. `venues` - Stadium name, city, country, and spectator capacity.
3. `series` - Tournaments, bilateral series, start dates, and total matches.
4. `players` - Player identity, role, batting/bowling styles.
5. `matches` - Fixture details, format, toss winner, toss decision, and match winner.
6. `batting_scorecards` - Innings runs, balls, 4s, 6s, and stored generated `strike_rate`.
7. `bowling_scorecards` - Overs bowled, maidens, runs conceded, wickets, and stored `economy_rate`.
8. `fielding_scorecards` - Catches, stumpings, and run-outs.
9. `partnerships` - Stand runs, balls, and consecutive batting positions.

---

## 🔍 The 25 SQL Analytics Engine

| # | Difficulty | Question Title | Core SQL Concepts |
|---|---|---|---|
| **Q01** | Beginner | Indian Team Squad Profile | `SELECT`, `INNER JOIN`, `WHERE`, `ORDER BY` |
| **Q02** | Beginner | Matches in the Last 30 Days | `DATE_SUB`, Subqueries, Date Filtering |
| **Q03** | Beginner | Top 10 Highest ODI Run Scorers | `SUM`, `AVG`, `CASE WHEN`, `LIMIT` |
| **Q04** | Beginner | Stadiums with Capacity > 50,000 | Numerical Comparison, `ORDER BY DESC` |
| **Q05** | Beginner | Total Match Wins by Team | `LEFT JOIN`, `COUNT`, `GROUP BY` |
| **Q06** | Beginner | Player Squad by Playing Role | `GROUP BY role`, `COUNT(*)` |
| **Q07** | Beginner | Highest Individual Score per Format | `MAX()`, `GROUP BY format` |
| **Q08** | Beginner | Series Starting in Year 2024 | `YEAR(start_date) = 2024` |
| **Q09** | Intermediate | Elite All-Rounders (>1000 Runs & >50 Wickets) | Multi-table `JOIN`, `HAVING` dual conditions |
| **Q10** | Intermediate | Last 20 Completed Matches Details | Multi-table equijoin, `LIMIT 20` |
| **Q11** | Intermediate | Multi-Format Player Comparison | Conditional Aggregation `CASE WHEN`, `HAVING COUNT(DISTINCT format) >= 2` |
| **Q12** | Intermediate | Home vs. Away Performance Analysis | Conditional Counting (`v.country = t.country`) |
| **Q13** | Intermediate | Century Batting Partnerships (100+ Runs) | Dual player joins, Consecutive position check |
| **Q14** | Intermediate | Bowler Venue Mastery (>= 3 Matches) | Venue grouping, Economy aggregation, `HAVING` |
| **Q15** | Intermediate | Clutch Batsmen in Close Matches | Filtering on margin `< 50 runs` or `< 5 wkts` |
| **Q16** | Intermediate | Batting Performance Evolution by Year | `YEAR(match_date)` grouping, strike rate trends |
| **Q17** | Advanced | Toss Advantage & Win Probability | Conditional percentages, `GROUP BY toss_decision` |
| **Q18** | Advanced | Most Economical Limited-Overs Bowlers | Overs thresholding, Economy calculation |
| **Q19** | Advanced | Batsmen Consistency (Standard Deviation) | Statistical `STDDEV_SAMP(runs_scored)` |
| **Q20** | Advanced | Cross-Format Participation & Averages | Test/ODI/T20 format aggregations |
| **Q21** | Advanced | Comprehensive Performance Ranking | Multi-CTE weighting algorithm, `DENSE_RANK()` |
| **Q22** | Advanced | Head-to-Head Team Rivalry Prediction | Undirected pairing, Win percentages, Margins |
| **Q23** | Advanced | Recent Player Form Categorization | `ROW_NUMBER() OVER(PARTITION BY ...)` Window Function |
| **Q24** | Advanced | Partnership Chemistry & Synergy Ranking | Consecutive stands, 50+ ratios, `DENSE_RANK()` |
| **Q25** | Advanced | Quarterly Time-Series & Career Trajectory | `QUARTER()`, `LAG() OVER(...)`, Trend Classification |

---

## 🚀 Installation & Quickstart Guide

### 1. Clone & Setup Virtual Environment
```bash
git clone <repo_url>
cd CricBuzz
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)
```ini
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cricbuzz_db
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
```

### 3. Initialize MySQL Database & Ingest Seed Data
```bash
python database/init_db.py
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing
Run the comprehensive Pytest suite:
```bash
pytest -v tests/
```
All 9 tests pass with 100% compliance:
* API client session and endpoint URL generation.
* Input validation boundary conditions.
* Complete CRUD insertion, retrieval, and deletion lifecycles.
* Live MySQL connection and table integrity.
* Execution of all 25 SQL queries with zero syntax errors.

---

## 🎓 Comprehensive 50 Interview & Viva Questions

### Section 1: SQL & Database Design (Questions 1–15)
1. **Explain the difference between 2NF and 3NF.**
   * *Answer:* 2NF eliminates partial dependencies (every non-key attribute must depend on the whole composite primary key). 3NF eliminates transitive dependencies (non-key attributes must not depend on other non-key attributes).
2. **What are MySQL Generated Columns, and why use `STORED` instead of `VIRTUAL`?**
   * *Answer:* Generated columns evaluate an expression automatically based on other column values. `STORED` calculates and persists the result on disk upon insert/update, allowing B-tree indexing on that column for faster query filtering.
3. **How does `DENSE_RANK()` differ from `RANK()` and `ROW_NUMBER()`?**
   * *Answer:* `ROW_NUMBER()` assigns distinct consecutive integers (1, 2, 3, 4). `RANK()` leaves gaps after ties (1, 2, 2, 4). `DENSE_RANK()` does not leave gaps after ties (1, 2, 2, 3).
4. **Explain how `LAG()` works in SQL Query 25.**
   * *Answer:* `LAG(column, offset)` accesses a row at a physical offset prior to the current row within the partitioned window, enabling quarter-over-quarter difference calculation without performing an expensive self-join.
5. **Why do we use `NULLIF()` in division operations?**
   * *Answer:* `NULLIF(expr1, expr2)` returns `NULL` if both expressions are equal. Using `NULLIF(denominator, 0)` protects queries from `Division by zero` exceptions by evaluating to `NULL`.
6. **What is the purpose of foreign key cascading (`ON DELETE CASCADE`)?**
   * *Answer:* It automatically deletes child records (such as batting scorecards) when the parent record (a match) is deleted, preserving referential integrity without manual cleanup.
7. **What is an equijoin vs a cross join?**
   * *Answer:* An equijoin combines records using equality conditions on common keys. A cross join produces the Cartesian product of all rows between two tables.
8. **Why are surrogate keys preferred over natural composite keys in large schemas?**
   * *Answer:* Surrogate keys (like auto-increment integers) provide smaller, fixed-size primary keys that optimize foreign key joins and B-tree index traversal.
9. **How does MySQL execute a `GROUP BY` query under the hood?**
   * *Answer:* MySQL uses either an index scan (if grouped columns are indexed) or creates an internal temporary table in memory and performs a sort (`filesort`).
10. **Explain how Common Table Expressions (CTEs) improve query readability.**
    * *Answer:* CTEs (`WITH cte AS (...)`) break down monolithic queries into modular, named logical blocks evaluated top-to-bottom, eliminating nested subqueries.
11. **What is the significance of `STDDEV_SAMP` in Query 19?**
    * *Answer:* It calculates the sample standard deviation of runs scored, quantifying volatility. A lower value indicates a more reliable, consistent batter.
12. **Why was `(player1_position + 1 = player2_position)` used in partnerships instead of subtraction?**
    * *Answer:* In MySQL, subtracting two unsigned integers when the subtrahend is greater results in an `UNSIGNED value out of range` error (error 1690). Addition avoids unsigned underflow.
13. **How do indexes affect read vs. write performance?**
    * *Answer:* B-tree indexes speed up `SELECT`, `WHERE`, and `JOIN` operations ($O(\log N)$), but incur a slight overhead on `INSERT`, `UPDATE`, and `DELETE` operations as index trees must be rebalanced.
14. **What is the ACID guarantee in MySQL InnoDB?**
    * *Answer:* Atomicity (all or nothing), Consistency (preserves constraints), Isolation (concurrent transactions don't interfere), and Durability (committed data survives crashes).
15. **What does the `EXPLAIN` statement output signify?**
    * *Answer:* It displays the execution plan chosen by the optimizer, indicating access type (`const`, `ref`, `range`, `ALL`), keys used, and rows examined.

### Section 2: Python & Architecture (Questions 16–30)
16. **What is the 12-Factor App methodology regarding configuration?**
    * *Answer:* Code and configuration must be strictly separated. Credentials and environment-specific settings are injected via environment variables (`.env`) rather than hardcoded.
17. **Why use `contextlib.contextmanager` for database sessions?**
    * *Answer:* It guarantees that connections and cursors are properly committed on success, rolled back on error, and returned to the pool in a `finally` block, preventing resource leaks.
18. **What is connection pooling and why is it necessary in web applications?**
    * *Answer:* Establishing a new TCP handshake and authenticating with MySQL on every HTTP request creates latency. Connection pooling maintains a set of warm connections reused across requests.
19. **How did we handle transient HTTP failures in the Cricbuzz API client?**
    * *Answer:* By configuring `urllib3.util.Retry` with exponential backoff on HTTP status codes 429, 500, 502, 503, and 504.
20. **What is a Circuit Breaker pattern?**
    * *Answer:* When external API calls consistently fail or exceed quotas, the circuit breaker stops hammering the remote server and serves cached or fallback data immediately.
21. **How do Python dataclasses differ from standard classes?**
    * *Answer:* Dataclasses (`@dataclass(frozen=True)`) automatically generate `__init__`, `__repr__`, and `__eq__`, providing immutable, type-annotated configuration objects.
22. **Why should presentation code never directly execute raw SQL?**
    * *Answer:* Direct SQL in presentation leads to tight coupling, security risks (SQL injection), and makes unit testing presentation logic without a database impossible.
23. **What is the purpose of `sys.path.insert(0, ...)`?**
    * *Answer:* It ensures Python resolves modules relative to the application's root directory, preventing `ModuleNotFoundError` during script execution.
24. **How does parameterization protect against SQL injection?**
    * *Answer:* Parameterized queries treat user input strictly as literal values rather than executable code, preventing attackers from injecting malicious SQL fragments.
25. **What is the benefit of type hinting in Python 3.10+?**
    * *Answer:* It enhances readability, enables static type analysis (mypy), and catches data mismatch bugs before runtime.
26. **What is PEP 8?**
    * *Answer:* The official Python style guide prescribing naming conventions, indentation (4 spaces), line lengths, and import organization.
27. **What is the purpose of rotating log handlers?**
    * *Answer:* `RotatingFileHandler` prevents application log files from growing indefinitely by capping file size (e.g., 5 MB) and archiving older logs.
28. **How does Python handle garbage collection for database cursors?**
    * *Answer:* Cursors are collected via reference counting and cyclic GC, but explicit closing (`cursor.close()`) is required to release server-side buffers immediately.
29. **What is the difference between `fetchone()`, `fetchall()`, and `fetchmany()`?**
    * *Answer:* `fetchone()` retrieves one row, `fetchall()` loads the entire result set into memory, and `fetchmany(size)` streams chunks of rows to prevent memory spikes.
30. **How does `pytest` discover test files?**
    * *Answer:* By scanning for files matching `test_*.py` or `*_test.py` and executing functions prefixed with `test_`.

### Section 3: Streamlit & Visualization (Questions 31–40)
31. **Explain the reactive execution model of Streamlit.**
    * *Answer:* Whenever a user interacts with a widget (click, slider, input), Streamlit reruns the Python script from top to bottom, updating the DOM dynamically.
32. **Why is caching critical in Streamlit (`st.cache_data` vs `st.cache_resource`)?**
    * *Answer:* `@st.cache_data` caches serializable computation results (DataFrames). `@st.cache_resource` caches non-serializable objects (database connections, ML models) across all user sessions.
33. **How does multi-page routing work in Streamlit?**
    * *Answer:* Any Python file placed in the `pages/` directory is automatically indexed and rendered as a distinct navigation item in the sidebar.
34. **What is `st.session_state` and when should it be used?**
    * *Answer:* A key-value store that persists state across top-to-bottom script reruns (e.g., tracking selected match IDs or pagination indexes).
35. **Why choose Plotly over Matplotlib for enterprise web dashboards?**
    * *Answer:* Plotly renders interactive SVG/WebGL charts supporting zooming, hover tooltips, and click filtering, whereas Matplotlib outputs static raster PNG images.
36. **How does `st.form` optimize UI performance?**
    * *Answer:* `st.form` batches widget inputs together so the page does not rerun on every keystroke, rerunning only when `st.form_submit_button` is clicked.
37. **What is the function of `use_container_width=True` in Streamlit?**
    * *Answer:* It expands tables and charts responsively to fill the entire width of their parent container.
38. **How do you handle secrets safely when deploying Streamlit to the cloud?**
    * *Answer:* By using Streamlit Secrets Management (`.streamlit/secrets.toml`), which exposes keys via `st.secrets` without committing credentials to Git.
39. **How do you prevent UI freezing during long-running database queries?**
    * *Answer:* By wrapping queries in `st.spinner()` and caching repeated query executions with `@st.cache_data(ttl=300)`.
40. **How can you display toast notifications in Streamlit?**
    * *Answer:* By calling `st.toast("Message", icon="✅")`, which renders a non-intrusive floating alert that disappears after a few seconds.

### Section 4: System Design & API Integration (Questions 41–50)
41. **How do you handle API rate limits (HTTP 429) gracefully?**
    * *Answer:* Inspect the `Retry-After` header, apply exponential backoff, and serve cached responses to end-users.
42. **What is the difference between horizontal and vertical database scaling?**
    * *Answer:* Vertical scaling adds CPU/RAM to a single server. Horizontal scaling distributes data across multiple read replicas and sharded partitions.
43. **Why use `InnoDB` over `MyISAM` as the MySQL storage engine?**
    * *Answer:* InnoDB supports row-level locking, ACID transactions, and foreign key constraints. MyISAM only supports table-level locking and lacks transaction safety.
44. **How would you scale Cricbuzz LiveStats to support 100,000 concurrent users?**
    * *Answer:* Deploy Streamlit behind a load balancer (Nginx/AWS ALB), introduce a Redis cache layer for live match scores, and use MySQL read replicas for analytics queries.
45. **What is soft deletion vs hard deletion in database management?**
    * *Answer:* Soft deletion marks a row as deleted (e.g., `is_deleted = TRUE`) without removing data, preserving audit history. Hard deletion executes `DELETE FROM` and frees disk space.
46. **What is the role of an API Gateway in microservices?**
    * *Answer:* An API gateway acts as a single entry point handling rate limiting, authentication, SSL termination, and request routing across backend services.
47. **How do you maintain data consistency when updating multiple related tables?**
    * *Answer:* Wrap the operations in an atomic database transaction (`BEGIN ... COMMIT`), issuing a `ROLLBACK` if any intermediate step fails.
48. **What is the purpose of HTTP headers like `User-Agent` and `Accept`?**
    * *Answer:* `User-Agent` identifies the client application to the server. `Accept` specifies the media type the client can process (`application/json`).
49. **How does indexing on composite columns `(team1_id, team2_id)` work?**
    * *Answer:* MySQL can use the index for queries filtering on `team1_id` alone, or both `team1_id` AND `team2_id` (Leftmost Prefix Rule), but cannot use it for queries filtering only on `team2_id`.
50. **How does Docker improve application deployment?**
    * *Answer:* Docker packages the code, runtime, system libraries, and dependencies into an immutable container image that runs identically on Mac, Linux, and Cloud environments.
