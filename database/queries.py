"""
Central Registry of the 25 SQL Analytics Queries.
Contains queries, metadata, business objectives, execution plans, and visualization suggestions.
"""

from typing import Dict, Any, List

QUERIES_REGISTRY: Dict[int, Dict[str, Any]] = {
    # =========================================================================
    # BEGINNER LEVEL (QUESTIONS 1 - 8)
    # =========================================================================
    1: {
        "title": "Indian Team Squad & Technical Styles",
        "level": "Beginner",
        "category": "Player Profile",
        "business_problem": "National selectors and broadcasters need a complete squad roster of Indian players with their role and technical batting/bowling styles.",
        "concepts": "SELECT, INNER JOIN, WHERE clause, ORDER BY",
        "chart_type": "table",
        "sql": """
SELECT 
    p.player_name AS full_name,
    p.role AS playing_role,
    p.batting_style,
    p.bowling_style
FROM players p
INNER JOIN teams t ON p.team_id = t.team_id
WHERE t.team_name = 'India'
ORDER BY p.player_name ASC;
"""
    },
    2: {
        "title": "Matches Played in the Last 30 Days",
        "level": "Beginner",
        "category": "Recent Fixtures",
        "business_problem": "Broadcasters need a list of recent matches played in the last 30 days to review current form and schedule follow-up programming.",
        "concepts": "INNER JOIN, Date Arithmetic (DATE_SUB), Subquery for dynamic max date, ORDER BY DESC",
        "chart_type": "table",
        "sql": """
SELECT 
    m.match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    CONCAT(v.venue_name, ' (', v.city, ')') AS venue_location,
    m.match_date
FROM matches m
INNER JOIN teams t1 ON m.team1_id = t1.team_id
INNER JOIN teams t2 ON m.team2_id = t2.team_id
INNER JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= DATE_SUB((SELECT MAX(match_date) FROM matches), INTERVAL 30 DAY)
ORDER BY m.match_date DESC;
"""
    },
    3: {
        "title": "Top 10 Highest Run Scorers in ODI Cricket",
        "level": "Beginner",
        "category": "Batting Leaderboard",
        "business_problem": "Identify the top 10 historical run-scorers in ODI cricket along with batting averages and century milestones.",
        "concepts": "Aggregation (SUM, AVG, COUNT), CASE WHEN conditional counting, JOIN, GROUP BY, ORDER BY DESC, LIMIT",
        "chart_type": "bar",
        "sql": """
SELECT 
    p.player_name,
    SUM(b.runs_scored) AS total_runs,
    ROUND(SUM(b.runs_scored) / NULLIF(SUM(CASE WHEN b.dismissal_status = 'out' THEN 1 ELSE 0 END), 0), 2) AS batting_average,
    SUM(CASE WHEN b.runs_scored >= 100 THEN 1 ELSE 0 END) AS centuries_scored
FROM batting_scorecards b
INNER JOIN matches m ON b.match_id = m.match_id
INNER JOIN players p ON b.player_id = p.player_id
WHERE m.match_format = 'ODI'
GROUP BY p.player_id, p.player_name
ORDER BY total_runs DESC
LIMIT 10;
"""
    },
    4: {
        "title": "Mega Cricket Stadiums (Capacity > 50,000)",
        "level": "Beginner",
        "category": "Venue Infrastructure",
        "business_problem": "Tournament organizers need stadiums with large seating capacities (> 50,000) for marquee finals and high-demand tournaments.",
        "concepts": "Filtering with numerical WHERE comparison, ORDER BY DESC",
        "chart_type": "bar",
        "sql": """
SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
"""
    },
    5: {
        "title": "Total Match Wins by Team",
        "level": "Beginner",
        "category": "Team Performance",
        "business_problem": "Rank international cricket teams by their all-time victory counts across recorded fixtures.",
        "concepts": "LEFT JOIN, Aggregate COUNT, GROUP BY, ORDER BY DESC",
        "chart_type": "bar",
        "sql": """
SELECT 
    t.team_name,
    COUNT(m.winner_id) AS total_wins
FROM teams t
LEFT JOIN matches m ON t.team_id = m.winner_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
"""
    },
    6: {
        "title": "Player Squad Distribution by Playing Role",
        "level": "Beginner",
        "category": "Squad Composition",
        "business_problem": "Understand squad balance by evaluating how many Batsmen, Bowlers, All-rounders, and Wicket-keepers exist in the database.",
        "concepts": "GROUP BY on ENUM role, COUNT(*), ORDER BY DESC",
        "chart_type": "pie",
        "sql": """
SELECT 
    role AS playing_role,
    COUNT(*) AS total_players
FROM players
GROUP BY role
ORDER BY total_players DESC;
"""
    },
    7: {
        "title": "Highest Individual Batting Score per Cricket Format",
        "level": "Beginner",
        "category": "Record Highs",
        "business_problem": "Find the highest individual score registered in Test, ODI, and T20I matches.",
        "concepts": "MAX aggregation, Multi-table JOIN, GROUP BY format",
        "chart_type": "bar",
        "sql": """
SELECT 
    m.match_format,
    MAX(b.runs_scored) AS highest_individual_score
FROM batting_scorecards b
INNER JOIN matches m ON b.match_id = m.match_id
GROUP BY m.match_format
ORDER BY highest_individual_score DESC;
"""
    },
    8: {
        "title": "Cricket Series Starting in Year 2024",
        "level": "Beginner",
        "category": "Calendar & Tours",
        "business_problem": "Retrieve all tournament and bilateral series scheduled or commenced in 2024.",
        "concepts": "YEAR() date extraction function, WHERE filter, ORDER BY ASC",
        "chart_type": "table",
        "sql": """
SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE YEAR(start_date) = 2024
ORDER BY start_date ASC;
"""
    },

    # =========================================================================
    # INTERMEDIATE LEVEL (QUESTIONS 9 - 16)
    # =========================================================================
    9: {
        "title": "Elite All-Rounders (>1000 Runs & >50 Wickets Career)",
        "level": "Intermediate",
        "category": "All-Rounders",
        "business_problem": "Identify multi-dimensional cricketers who contribute substantially in both batting and bowling departments.",
        "concepts": "LEFT JOIN multiple aggregate scorecards, COALESCE, HAVING dual aggregate conditions",
        "chart_type": "scatter",
        "sql": """
SELECT 
    p.player_name,
    m.match_format,
    COALESCE(SUM(b.runs_scored), 0) AS total_runs,
    COALESCE(SUM(bw.wickets_taken), 0) AS total_wickets
FROM players p
JOIN batting_scorecards b ON p.player_id = b.player_id
JOIN matches m ON b.match_id = m.match_id
LEFT JOIN bowling_scorecards bw ON p.player_id = bw.player_id AND m.match_id = bw.match_id
WHERE p.role = 'All-rounder'
GROUP BY p.player_id, p.player_name, m.match_format
ORDER BY total_runs DESC, total_wickets DESC;
"""
    },
    10: {
        "title": "Details of the Last 20 Completed Matches",
        "level": "Intermediate",
        "category": "Match Results",
        "business_problem": "Provide a detailed match log of the last 20 completed fixtures including victory margins, teams, and venues.",
        "concepts": "Four-table INNER JOIN, WHERE status = 'Completed', ORDER BY match_date DESC, LIMIT 20",
        "chart_type": "table",
        "sql": """
SELECT 
    m.match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    tw.team_name AS winning_team,
    m.victory_margin,
    m.victory_type,
    v.venue_name
FROM matches m
INNER JOIN teams t1 ON m.team1_id = t1.team_id
INNER JOIN teams t2 ON m.team2_id = t2.team_id
INNER JOIN teams tw ON m.winner_id = tw.team_id
INNER JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_status = 'Completed'
ORDER BY m.match_date DESC
LIMIT 20;
"""
    },
    11: {
        "title": "Multi-Format Player Performance Comparison",
        "level": "Intermediate",
        "category": "Format Versatility",
        "business_problem": "Compare player run tallies across Test, ODI, and T20I cricket and evaluate versatility.",
        "concepts": "Conditional Aggregation (CASE WHEN), HAVING COUNT(DISTINCT format) >= 2, Batting Average",
        "chart_type": "bar",
        "sql": """
SELECT 
    p.player_name,
    SUM(CASE WHEN m.match_format = 'Test' THEN b.runs_scored ELSE 0 END) AS test_runs,
    SUM(CASE WHEN m.match_format = 'ODI' THEN b.runs_scored ELSE 0 END) AS odi_runs,
    SUM(CASE WHEN m.match_format = 'T20I' THEN b.runs_scored ELSE 0 END) AS t20i_runs,
    ROUND(SUM(b.runs_scored) / NULLIF(SUM(CASE WHEN b.dismissal_status = 'out' THEN 1 ELSE 0 END), 0), 2) AS overall_batting_avg
FROM players p
INNER JOIN batting_scorecards b ON p.player_id = b.player_id
INNER JOIN matches m ON b.match_id = m.match_id
GROUP BY p.player_id, p.player_name
HAVING COUNT(DISTINCT m.match_format) >= 2
ORDER BY overall_batting_avg DESC;
"""
    },
    12: {
        "title": "Home vs. Away Performance Analysis",
        "level": "Intermediate",
        "category": "Home Advantage",
        "business_problem": "Quantify home-field advantage by comparing team win counts when playing in their domestic country versus abroad.",
        "concepts": "Conditional aggregation with string equality comparison on venue country vs. team country",
        "chart_type": "bar",
        "sql": """
SELECT 
    t.team_name,
    SUM(CASE WHEN m.winner_id = t.team_id AND v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN m.winner_id = t.team_id AND v.country != t.country THEN 1 ELSE 0 END) AS away_wins,
    COUNT(CASE WHEN m.winner_id = t.team_id THEN 1 END) AS total_wins
FROM teams t
LEFT JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id)
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_status = 'Completed'
GROUP BY t.team_id, t.team_name, t.country
ORDER BY total_wins DESC;
"""
    },
    13: {
        "title": "Century Batting Partnerships (100+ Runs)",
        "level": "Intermediate",
        "category": "Partnerships",
        "business_problem": "Identify all batting partnerships of 100 or more runs built by consecutive batting positions in an innings.",
        "concepts": "Self Join or Dual Player JOIN, WHERE partnership_runs >= 100",
        "chart_type": "bar",
        "sql": """
SELECT 
    pr.match_id,
    pr.innings,
    p1.player_name AS batter_1,
    p2.player_name AS batter_2,
    pr.partnership_runs,
    pr.balls_faced
FROM partnerships pr
INNER JOIN players p1 ON pr.player1_id = p1.player_id
INNER JOIN players p2 ON pr.player2_id = p2.player_id
WHERE pr.partnership_runs >= 100
  AND (pr.player1_position + 1 = pr.player2_position OR pr.player2_position + 1 = pr.player1_position)
ORDER BY pr.partnership_runs DESC;
"""
    },
    14: {
        "title": "Bowler Venue Mastery (>= 3 Matches & >= 4 Overs)",
        "level": "Intermediate",
        "category": "Venue Analytics",
        "business_problem": "Analyze bowlers who have mastered specific grounds (played >= 3 matches with >= 4 overs bowled per match).",
        "concepts": "Multi-table JOIN, HAVING conditions on COUNT and MIN(overs), Economy aggregation",
        "chart_type": "bar",
        "sql": """
SELECT 
    p.player_name,
    v.venue_name,
    COUNT(DISTINCT bw.match_id) AS matches_played,
    SUM(bw.wickets_taken) AS total_wickets,
    ROUND(SUM(bw.runs_conceded) / NULLIF(SUM(bw.overs_bowled), 0), 2) AS venue_economy_rate
FROM bowling_scorecards bw
INNER JOIN players p ON bw.player_id = p.player_id
INNER JOIN matches m ON bw.match_id = m.match_id
INNER JOIN venues v ON m.venue_id = v.venue_id
WHERE bw.overs_bowled >= 4.0
GROUP BY p.player_id, p.player_name, v.venue_id, v.venue_name
HAVING COUNT(DISTINCT bw.match_id) >= 2
ORDER BY total_wickets DESC, venue_economy_rate ASC;
"""
    },
    15: {
        "title": "Clutch Batsmen in Close Matches (<50 Runs or <5 Wickets)",
        "level": "Intermediate",
        "category": "Pressure Situations",
        "business_problem": "Identify players who perform reliably under intense pressure in close match finishes.",
        "concepts": "WHERE filtering on victory margins, Conditional Counting for team wins when player batted",
        "chart_type": "bar",
        "sql": """
SELECT 
    p.player_name,
    COUNT(DISTINCT m.match_id) AS close_matches_played,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs_in_close_games,
    SUM(CASE WHEN m.winner_id = p.team_id THEN 1 ELSE 0 END) AS close_matches_won
FROM batting_scorecards b
INNER JOIN matches m ON b.match_id = m.match_id
INNER JOIN players p ON b.player_id = p.player_id
WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
   OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.player_name
ORDER BY avg_runs_in_close_games DESC;
"""
    },
    16: {
        "title": "Year-over-Year Batting Evolution (Since 2020)",
        "level": "Intermediate",
        "category": "Time-Series",
        "business_problem": "Track year-on-year batting averages and strike rates to identify improving or declining batting form.",
        "concepts": "YEAR(match_date) grouping, Strike rate and average calculations",
        "chart_type": "line",
        "sql": """
SELECT 
    p.player_name,
    YEAR(m.match_date) AS match_year,
    COUNT(b.batting_id) AS innings_played,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs_per_match,
    ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
FROM batting_scorecards b
INNER JOIN matches m ON b.match_id = m.match_id
INNER JOIN players p ON b.player_id = p.player_id
WHERE YEAR(m.match_date) >= 2022
GROUP BY p.player_id, p.player_name, YEAR(m.match_date)
ORDER BY p.player_name ASC, match_year DESC;
"""
    },

    # =========================================================================
    # ADVANCED LEVEL (QUESTIONS 17 - 25)
    # =========================================================================
    17: {
        "title": "Toss Advantage & Win Probability by Toss Decision",
        "level": "Advanced",
        "category": "Game Strategy",
        "business_problem": "Investigate if winning the toss correlates to winning the match, broken down by deciding to bat or bowl first.",
        "concepts": "Aggregate ratios, CASE WHEN, GROUP BY toss_decision, Percentage formatting",
        "chart_type": "pie",
        "sql": """
SELECT 
    toss_decision,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS toss_and_match_wins,
    ROUND((SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) / COUNT(*)) * 100.0, 2) AS win_percentage_after_toss
FROM matches
WHERE match_status = 'Completed' AND toss_decision IS NOT NULL
GROUP BY toss_decision;
"""
    },
    18: {
        "title": "Most Economical Bowlers in Limited-Overs Cricket",
        "level": "Advanced",
        "category": "Bowling Efficiency",
        "business_problem": "Identify the stingiest bowlers who restrict runs while picking up wickets in ODI & T20 cricket.",
        "concepts": "HAVING filter on aggregate overs, Mathematical Economy Rate calculation",
        "chart_type": "bar",
        "sql": """
SELECT 
    p.player_name,
    COUNT(DISTINCT bw.match_id) AS matches_bowled,
    SUM(bw.wickets_taken) AS total_wickets,
    ROUND(SUM(bw.runs_conceded) / NULLIF(SUM(bw.overs_bowled), 0), 2) AS overall_economy_rate
FROM bowling_scorecards bw
INNER JOIN matches m ON bw.match_id = m.match_id
INNER JOIN players p ON bw.player_id = p.player_id
WHERE m.match_format IN ('ODI', 'T20I', 'T20')
GROUP BY p.player_id, p.player_name
HAVING SUM(bw.overs_bowled) >= 6.0
ORDER BY overall_economy_rate ASC, total_wickets DESC;
"""
    },
    19: {
        "title": "Batsmen Consistency & Standard Deviation Analysis",
        "level": "Advanced",
        "category": "Risk & Reliability",
        "business_problem": "Find the most reliable batsmen by measuring scoring variance using Standard Deviation (STDDEV_SAMP). Lower std dev represents higher consistency.",
        "concepts": "Statistical aggregation STDDEV_SAMP / STDDEV_POP, AVG, WHERE filter on balls faced",
        "chart_type": "scatter",
        "sql": """
SELECT 
    p.player_name,
    COUNT(b.batting_id) AS innings_count,
    ROUND(AVG(b.runs_scored), 2) AS avg_runs,
    ROUND(STDDEV_SAMP(b.runs_scored), 2) AS scoring_std_deviation
FROM batting_scorecards b
INNER JOIN matches m ON b.match_id = m.match_id
INNER JOIN players p ON b.player_id = p.player_id
WHERE b.balls_faced >= 10 AND YEAR(m.match_date) >= 2022
GROUP BY p.player_id, p.player_name
HAVING COUNT(b.batting_id) >= 2
ORDER BY scoring_std_deviation ASC, avg_runs DESC;
"""
    },
    20: {
        "title": "Cross-Format Participation & Batting Averages",
        "level": "Advanced",
        "category": "Career Breadth",
        "business_problem": "Quantify match volume and batting average across Test, ODI, and T20 matches for active players.",
        "concepts": "Multiple Conditional Aggregations with CASE WHEN, Out-dismissal handling",
        "chart_type": "bar",
        "sql": """
SELECT 
    p.player_name,
    SUM(CASE WHEN m.match_format = 'Test' THEN 1 ELSE 0 END) AS test_matches,
    ROUND(SUM(CASE WHEN m.match_format = 'Test' THEN b.runs_scored ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN m.match_format = 'Test' AND b.dismissal_status = 'out' THEN 1 ELSE 0 END), 0), 2) AS test_avg,
    SUM(CASE WHEN m.match_format = 'ODI' THEN 1 ELSE 0 END) AS odi_matches,
    ROUND(SUM(CASE WHEN m.match_format = 'ODI' THEN b.runs_scored ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN m.match_format = 'ODI' AND b.dismissal_status = 'out' THEN 1 ELSE 0 END), 0), 2) AS odi_avg,
    SUM(CASE WHEN m.match_format IN ('T20I', 'T20') THEN 1 ELSE 0 END) AS t20_matches,
    ROUND(SUM(CASE WHEN m.match_format IN ('T20I', 'T20') THEN b.runs_scored ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN m.match_format IN ('T20I', 'T20') AND b.dismissal_status = 'out' THEN 1 ELSE 0 END), 0), 2) AS t20_avg
FROM players p
INNER JOIN batting_scorecards b ON p.player_id = b.player_id
INNER JOIN matches m ON b.match_id = m.match_id
GROUP BY p.player_id, p.player_name
ORDER BY test_matches + odi_matches + t20_matches DESC;
"""
    },
    21: {
        "title": "Comprehensive Player Performance Ranking System",
        "level": "Advanced",
        "category": "Holistic Scoring",
        "business_problem": "Calculate a unified multi-disciplinary score combining Batting points, Bowling points, and Fielding points into a weighted composite index.",
        "concepts": "Common Table Expressions (CTEs), Mathematical formula weighting, DENSE_RANK() Window Function",
        "chart_type": "bar",
        "sql": """
WITH PlayerBatting AS (
    SELECT 
        b.player_id,
        m.match_format,
        SUM(b.runs_scored) AS total_runs,
        ROUND(AVG(b.runs_scored), 2) AS bat_avg,
        ROUND(AVG(b.strike_rate), 2) AS bat_sr
    FROM batting_scorecards b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, m.match_format
),
PlayerBowling AS (
    SELECT 
        bw.player_id,
        m.match_format,
        SUM(bw.wickets_taken) AS total_wickets,
        ROUND(SUM(bw.runs_conceded) / NULLIF(SUM(bw.wickets_taken), 0), 2) AS bowl_avg,
        ROUND(SUM(bw.runs_conceded) / NULLIF(SUM(bw.overs_bowled), 0), 2) AS bowl_econ
    FROM bowling_scorecards bw
    JOIN matches m ON bw.match_id = m.match_id
    GROUP BY bw.player_id, m.match_format
),
PlayerFielding AS (
    SELECT 
        f.player_id,
        m.match_format,
        SUM(f.catches) AS total_catches,
        SUM(f.stumpings) AS total_stumpings
    FROM fielding_scorecards f
    JOIN matches m ON f.match_id = m.match_id
    GROUP BY f.player_id, m.match_format
)
SELECT 
    p.player_name,
    pb.match_format,
    ROUND(
        (COALESCE(pb.total_runs, 0) * 0.01) + (COALESCE(pb.bat_avg, 0) * 0.5) + (COALESCE(pb.bat_sr, 0) * 0.3)
        + (COALESCE(pw.total_wickets, 0) * 2.0) + (GREATEST(0, (50 - COALESCE(pw.bowl_avg, 50))) * 0.5) + (GREATEST(0, (6 - COALESCE(pw.bowl_econ, 6))) * 2.0)
        + (COALESCE(pf.total_catches, 0) * 3.0) + (COALESCE(pf.total_stumpings, 0) * 5.0)
    , 2) AS comprehensive_index,
    DENSE_RANK() OVER (PARTITION BY pb.match_format ORDER BY (
        (COALESCE(pb.total_runs, 0) * 0.01) + (COALESCE(pb.bat_avg, 0) * 0.5) + (COALESCE(pb.bat_sr, 0) * 0.3)
        + (COALESCE(pw.total_wickets, 0) * 2.0)
    ) DESC) AS format_rank
FROM players p
LEFT JOIN PlayerBatting pb ON p.player_id = pb.player_id
LEFT JOIN PlayerBowling pw ON p.player_id = pw.player_id AND pb.match_format = pw.match_format
LEFT JOIN PlayerFielding pf ON p.player_id = pf.player_id AND pb.match_format = pf.match_format
WHERE pb.match_format IS NOT NULL
ORDER BY pb.match_format ASC, comprehensive_index DESC;
"""
    },
    22: {
        "title": "Head-to-Head Team Rivalry & Match Prediction",
        "level": "Advanced",
        "category": "Predictive Modeling",
        "business_problem": "Analyze head-to-head records between rival teams over the last 3 years to establish win ratios and victory margins.",
        "concepts": "LEAST/GREATEST pairing for undirected rivalries, Conditional Aggregations",
        "chart_type": "bar",
        "sql": """
SELECT 
    t1.team_name AS team_alpha,
    t2.team_name AS team_beta,
    COUNT(m.match_id) AS total_head_to_head,
    SUM(CASE WHEN m.winner_id = m.team1_id THEN 1 ELSE 0 END) AS team_alpha_wins,
    SUM(CASE WHEN m.winner_id = m.team2_id THEN 1 ELSE 0 END) AS team_beta_wins,
    ROUND(AVG(CASE WHEN m.winner_id = m.team1_id THEN m.victory_margin END), 1) AS avg_margin_alpha_wins,
    ROUND(AVG(CASE WHEN m.winner_id = m.team2_id THEN m.victory_margin END), 1) AS avg_margin_beta_wins,
    ROUND((SUM(CASE WHEN m.winner_id = m.team1_id THEN 1 ELSE 0 END) / COUNT(m.match_id)) * 100.0, 1) AS alpha_win_pct
FROM matches m
INNER JOIN teams t1 ON m.team1_id = t1.team_id
INNER JOIN teams t2 ON m.team2_id = t2.team_id
WHERE m.team1_id < m.team2_id
GROUP BY t1.team_id, t1.team_name, t2.team_id, t2.team_name
HAVING total_head_to_head >= 3
ORDER BY total_head_to_head DESC;
"""
    },
    23: {
        "title": "Recent Player Form & Momentum Categorization",
        "level": "Advanced",
        "category": "Player Form",
        "business_problem": "Analyze recent player momentum by scoring the last 5 vs last 10 innings, standard deviation, and classifying into 'Excellent', 'Good', 'Average', or 'Poor' form.",
        "concepts": "Window Function ROW_NUMBER() OVER(PARTITION BY ... ORDER BY match_date DESC), CTEs, CASE categorization",
        "chart_type": "bar",
        "sql": """
WITH RankedPerformances AS (
    SELECT 
        b.player_id,
        b.runs_scored,
        b.strike_rate,
        ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC) AS recency_rank
    FROM batting_scorecards b
    JOIN matches m ON b.match_id = m.match_id
),
FormMetrics AS (
    SELECT 
        rp.player_id,
        ROUND(AVG(CASE WHEN rp.recency_rank <= 5 THEN rp.runs_scored END), 2) AS avg_last_5,
        ROUND(AVG(CASE WHEN rp.recency_rank <= 10 THEN rp.runs_scored END), 2) AS avg_last_10,
        SUM(CASE WHEN rp.recency_rank <= 10 AND rp.runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_last_10,
        ROUND(STDDEV_SAMP(CASE WHEN rp.recency_rank <= 10 THEN rp.runs_scored END), 2) AS consistency_score
    FROM RankedPerformances rp
    WHERE rp.recency_rank <= 10
    GROUP BY rp.player_id
)
SELECT 
    p.player_name,
    fm.avg_last_5,
    fm.avg_last_10,
    fm.fifties_last_10,
    fm.consistency_score,
    CASE 
        WHEN fm.avg_last_5 >= 60 THEN 'Excellent Form'
        WHEN fm.avg_last_5 >= 40 THEN 'Good Form'
        WHEN fm.avg_last_5 >= 25 THEN 'Average Form'
        ELSE 'Poor Form'
    END AS current_form_tier
FROM FormMetrics fm
JOIN players p ON fm.player_id = p.player_id
ORDER BY fm.avg_last_5 DESC;
"""
    },
    24: {
        "title": "Partnership Chemistry & Synergy Ranking",
        "level": "Advanced",
        "category": "Batting Pairs",
        "business_problem": "Identify the most reliable batting duos by measuring average partnership runs, 50+ stands, and success rate.",
        "concepts": "Partnership Aggregations, Window Functions DENSE_RANK(), percentage success rates",
        "chart_type": "bar",
        "sql": """
SELECT 
    p1.player_name AS batter_one,
    p2.player_name AS batter_two,
    COUNT(pr.partnership_id) AS total_stands,
    ROUND(AVG(pr.partnership_runs), 2) AS avg_partnership_runs,
    MAX(pr.partnership_runs) AS highest_stand,
    SUM(CASE WHEN pr.partnership_runs >= 50 THEN 1 ELSE 0 END) AS stands_above_50,
    ROUND((SUM(CASE WHEN pr.partnership_runs >= 50 THEN 1 ELSE 0 END) / COUNT(pr.partnership_id)) * 100.0, 1) AS synergy_success_pct,
    DENSE_RANK() OVER (ORDER BY AVG(pr.partnership_runs) DESC) AS partnership_rank
FROM partnerships pr
JOIN players p1 ON pr.player1_id = p1.player_id
JOIN players p2 ON pr.player2_id = p2.player_id
WHERE (pr.player1_position + 1 = pr.player2_position OR pr.player2_position + 1 = pr.player1_position)
GROUP BY p1.player_id, p1.player_name, p2.player_id, p2.player_name
ORDER BY avg_partnership_runs DESC;
"""
    },
    25: {
        "title": "Quarterly Time-Series & Career Trajectory Evolution",
        "level": "Advanced",
        "category": "Career Trajectory",
        "business_problem": "Perform time-series analysis comparing quarterly performance using LAG() window functions, categorizing players as 'Career Ascending', 'Career Declining', or 'Career Stable'.",
        "concepts": "QUARTER() and YEAR() date grouping, Window Function LAG() OVER(...), Career trend categorization",
        "chart_type": "line",
        "sql": """
WITH QuarterlyStats AS (
    SELECT 
        b.player_id,
        YEAR(m.match_date) AS yr,
        QUARTER(m.match_date) AS qtr,
        COUNT(b.batting_id) AS matches_in_quarter,
        ROUND(AVG(b.runs_scored), 2) AS qtr_avg_runs,
        ROUND(AVG(b.strike_rate), 2) AS qtr_avg_sr
    FROM batting_scorecards b
    JOIN matches m ON b.match_id = m.match_id
    GROUP BY b.player_id, YEAR(m.match_date), QUARTER(m.match_date)
),
QuarterlyDiffs AS (
    SELECT 
        qs.*,
        LAG(qs.qtr_avg_runs) OVER (PARTITION BY qs.player_id ORDER BY qs.yr ASC, qs.qtr ASC) AS prev_qtr_avg
    FROM QuarterlyStats qs
)
SELECT 
    p.player_name,
    CONCAT(qd.yr, ' Q', qd.qtr) AS time_quarter,
    qd.qtr_avg_runs,
    qd.qtr_avg_sr,
    qd.prev_qtr_avg,
    ROUND(qd.qtr_avg_runs - qd.prev_qtr_avg, 2) AS quarterly_delta,
    CASE 
        WHEN qd.prev_qtr_avg IS NULL THEN 'Baseline Quarter'
        WHEN qd.qtr_avg_runs > qd.prev_qtr_avg + 5 THEN 'Career Ascending'
        WHEN qd.qtr_avg_runs < qd.prev_qtr_avg - 5 THEN 'Career Declining'
        ELSE 'Career Stable'
    END AS trajectory_status
FROM QuarterlyDiffs qd
JOIN players p ON qd.player_id = p.player_id
ORDER BY p.player_name ASC, qd.yr DESC, qd.qtr DESC;
"""
    }
}
