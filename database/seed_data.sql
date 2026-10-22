-- =============================================================================
-- CRICBUZZ LIVESTATS - REALISTIC SEED DATA SCRIPT (MySQL 8.0+)
-- Powers all 25 Analytical SQL Queries
-- =============================================================================

USE cricbuzz_db;

-- Clear previous data in correct foreign-key order
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE partnerships;
TRUNCATE TABLE fielding_scorecards;
TRUNCATE TABLE bowling_scorecards;
TRUNCATE TABLE batting_scorecards;
TRUNCATE TABLE matches;
TRUNCATE TABLE players;
TRUNCATE TABLE series;
TRUNCATE TABLE venues;
TRUNCATE TABLE teams;
SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------------------------------
-- 1. TEAMS (8 International Teams)
-- -----------------------------------------------------------------------------
INSERT INTO teams (team_id, team_name, team_short_name, country) VALUES
(1, 'India', 'IND', 'India'),
(2, 'Australia', 'AUS', 'Australia'),
(3, 'England', 'ENG', 'England'),
(4, 'South Africa', 'SA', 'South Africa'),
(5, 'New Zealand', 'NZ', 'New Zealand'),
(6, 'Pakistan', 'PAK', 'Pakistan'),
(7, 'West Indies', 'WI', 'West Indies'),
(8, 'Sri Lanka', 'SL', 'Sri Lanka');

-- -----------------------------------------------------------------------------
-- 2. VENUES (Global stadiums with distinct capacities & home countries)
-- -----------------------------------------------------------------------------
INSERT INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
(2, 'Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
(3, 'Eden Gardens', 'Kolkata', 'India', 68000),
(4, 'Lord\'s Cricket Ground', 'London', 'England', 31100),
(5, 'Sydney Cricket Ground', 'Sydney', 'Australia', 48000),
(6, 'Wankhede Stadium', 'Mumbai', 'India', 33108),
(7, 'Optus Stadium', 'Perth', 'Australia', 61266),
(8, 'SuperSport Park', 'Centurion', 'South Africa', 22000),
(9, 'The Oval', 'London', 'England', 27500),
(10, 'Adelaide Oval', 'Adelaide', 'Australia', 53583);

-- -----------------------------------------------------------------------------
-- 3. SERIES (Tournaments spanning 2020 - 2024)
-- -----------------------------------------------------------------------------
INSERT INTO series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
(1, 'Border-Gavaskar Trophy 2024-25', 'Australia', 'Test', '2024-11-22', '2025-01-07', 5),
(2, 'ICC Men\'s T20 World Cup 2024', 'West Indies', 'T20I', '2024-06-01', '2024-06-29', 55),
(3, 'England Tour of India 2024', 'India', 'Test', '2024-01-25', '2024-03-11', 5),
(4, 'ICC Cricket World Cup 2023', 'India', 'ODI', '2023-10-05', '2023-11-19', 48),
(5, 'Australia Tour of India 2023', 'India', 'ODI', '2023-03-17', '2023-03-22', 3),
(6, 'India Tour of South Africa 2023-24', 'South Africa', 'Test', '2023-12-26', '2024-01-07', 2),
(7, 'Asia Cup 2023', 'Sri Lanka', 'ODI', '2023-08-30', '2023-09-17', 13),
(8, 'T20 Bilateral Series 2024', 'India', 'T20I', '2024-01-11', '2024-01-17', 3);

-- -----------------------------------------------------------------------------
-- 4. PLAYERS (Diverse roles, styles, and team affiliations)
-- -----------------------------------------------------------------------------
INSERT INTO players (player_id, player_name, team_id, role, batting_style, bowling_style, date_of_birth) VALUES
-- Team India (team_id: 1)
(1, 'Rohit Sharma', 1, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1987-04-30'),
(2, 'Virat Kohli', 1, 'Batsman', 'Right-hand bat', 'Right-arm medium', '1988-11-05'),
(3, 'Yashasvi Jaiswal', 1, 'Batsman', 'Left-hand bat', 'Legbreak', '2001-12-28'),
(4, 'Shubman Gill', 1, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1999-09-08'),
(5, 'Rishabh Pant', 1, 'Wicket-keeper', 'Left-hand bat', 'None', '1997-10-04'),
(6, 'Ravindra Jadeja', 1, 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', '1988-12-06'),
(7, 'Hardik Pandya', 1, 'All-rounder', 'Right-hand bat', 'Right-arm fast-medium', '1993-10-11'),
(8, 'Jasprit Bumrah', 1, 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-12-06'),
(9, 'Mohammed Shami', 1, 'Bowler', 'Right-hand bat', 'Right-arm fast', '1990-09-03'),
(10, 'Kuldeep Yadav', 1, 'Bowler', 'Left-hand bat', 'Left-arm wrist spin', '1994-12-14'),
(11, 'KL Rahul', 1, 'Wicket-keeper', 'Right-hand bat', 'None', '1992-04-18'),

-- Team Australia (team_id: 2)
(12, 'Pat Cummins', 2, 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-05-08'),
(13, 'Mitchell Starc', 2, 'Bowler', 'Left-hand bat', 'Left-arm fast', '1990-01-30'),
(14, 'Steven Smith', 2, 'Batsman', 'Right-hand bat', 'Legbreak', '1989-06-02'),
(15, 'Travis Head', 2, 'Batsman', 'Left-hand bat', 'Right-arm offbreak', '1993-12-29'),
(16, 'Glenn Maxwell', 2, 'All-rounder', 'Right-hand bat', 'Right-arm offbreak', '1988-10-14'),
(17, 'Josh Hazlewood', 2, 'Bowler', 'Left-hand bat', 'Right-arm fast-medium', '1991-01-08'),
(18, 'Marnus Labuschagne', 2, 'Batsman', 'Right-hand bat', 'Legbreak', '1994-06-22'),
(19, 'Alex Carey', 2, 'Wicket-keeper', 'Left-hand bat', 'None', '1991-08-27'),

-- Team England (team_id: 3)
(20, 'Ben Stokes', 3, 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', '1991-06-04'),
(21, 'Joe Root', 3, 'Batsman', 'Right-hand bat', 'Right-arm offbreak', '1990-12-30'),
(22, 'Jos Buttler', 3, 'Wicket-keeper', 'Right-hand bat', 'None', '1990-09-08'),
(23, 'Jofra Archer', 3, 'Bowler', 'Right-hand bat', 'Right-arm fast', '1995-04-01'),

-- Team South Africa (team_id: 4)
(24, 'Kagiso Rabada', 4, 'Bowler', 'Left-hand bat', 'Right-arm fast', '1995-05-25'),
(25, 'Heinrich Klaasen', 4, 'Wicket-keeper', 'Right-hand bat', 'Right-arm offbreak', '1991-07-30');

-- -----------------------------------------------------------------------------
-- 5. MATCHES (Spans 2021-2024, includes close matches, recent 30-day fixtures)
-- -----------------------------------------------------------------------------
INSERT INTO matches (match_id, match_description, series_id, match_format, match_date, team1_id, team2_id, venue_id, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type, match_status) VALUES
-- Matches in 2024 (including recent 30 days relative to Oct/Nov 2024)
(101, 'IND vs AUS, 1st Test - Border-Gavaskar Trophy', 1, 'Test', '2024-11-22', 1, 2, 7, 1, 'bat', 1, 295, 'runs', 'Completed'),
(102, 'IND vs AUS, 2nd Test - Border-Gavaskar Trophy', 1, 'Test', '2024-12-06', 1, 2, 10, 2, 'bowl', 2, 10, 'wickets', 'Completed'),
(103, 'IND vs SA, ICC Men\'s T20 World Cup Final', 2, 'T20I', '2024-06-29', 1, 4, 3, 1, 'bat', 1, 7, 'runs', 'Completed'),
(104, 'IND vs ENG, 1st Test', 3, 'Test', '2024-01-25', 1, 3, 1, 3, 'bat', 3, 28, 'runs', 'Completed'),
(105, 'IND vs ENG, 2nd Test', 3, 'Test', '2024-02-02', 1, 3, 6, 1, 'bat', 1, 106, 'runs', 'Completed'),
(106, 'IND vs ENG, 3rd Test', 3, 'Test', '2024-02-15', 1, 3, 1, 1, 'bat', 1, 434, 'runs', 'Completed'),
(107, 'IND vs ENG, 4th Test', 3, 'Test', '2024-02-23', 1, 3, 3, 3, 'bat', 1, 5, 'wickets', 'Completed'),
(108, 'IND vs ENG, 5th Test', 3, 'Test', '2024-03-07', 1, 3, 1, 3, 'bat', 1, 64, 'runs', 'Completed'),

-- ODI World Cup 2023 Matches (India, Australia, South Africa)
(109, 'IND vs AUS, ICC World Cup Final 2023', 4, 'ODI', '2023-11-19', 1, 2, 1, 2, 'bowl', 2, 6, 'wickets', 'Completed'),
(110, 'IND vs NZ, ICC World Cup Semi-Final 2023', 4, 'ODI', '2023-11-15', 1, 5, 6, 1, 'bat', 1, 70, 'runs', 'Completed'),
(111, 'IND vs SA, ICC World Cup Group Match', 4, 'ODI', '2023-11-05', 1, 4, 3, 1, 'bat', 1, 243, 'runs', 'Completed'),
(112, 'IND vs AUS, ICC World Cup Group Match', 4, 'ODI', '2023-10-08', 1, 2, 1, 2, 'bat', 1, 6, 'wickets', 'Completed'),

-- Bilateral Head-to-Head IND vs AUS in 2023 (Ensures >= 5 matches in last 3 years)
(113, 'IND vs AUS, 1st ODI 2023', 5, 'ODI', '2023-03-17', 1, 2, 6, 1, 'bowl', 1, 5, 'wickets', 'Completed'),
(114, 'IND vs AUS, 2nd ODI 2023', 5, 'ODI', '2023-03-19', 1, 2, 3, 2, 'bowl', 2, 10, 'wickets', 'Completed'),
(115, 'IND vs AUS, 3rd ODI 2023', 5, 'ODI', '2023-03-22', 1, 2, 1, 2, 'bat', 2, 21, 'runs', 'Completed'),

-- Tests & T20Is in 2022 & 2023 (Close Matches & Varied Formats)
(116, 'IND vs SA, 1st Test Centurion', 6, 'Test', '2023-12-26', 1, 4, 8, 4, 'bowl', 4, 32, 'runs', 'Completed'),
(117, 'IND vs SA, 2nd Test Cape Town', 6, 'Test', '2024-01-03', 1, 4, 8, 4, 'bat', 1, 7, 'wickets', 'Completed'),
(118, 'AUS vs ENG, Ashes 1st Test 2023', 1, 'Test', '2023-06-16', 2, 3, 4, 3, 'bat', 2, 2, 'wickets', 'Completed'),
(119, 'IND vs PAK, Asia Cup Super 4 2023', 7, 'ODI', '2023-09-11', 1, 6, 3, 6, 'bowl', 1, 228, 'runs', 'Completed'),
(120, 'IND vs AUS, T20I Series Match 2022', 8, 'T20I', '2022-09-20', 1, 2, 6, 2, 'bowl', 2, 4, 'wickets', 'Completed'),
(121, 'IND vs AUS, T20I Series Match 2 2022', 8, 'T20I', '2022-09-23', 1, 2, 1, 1, 'bowl', 1, 6, 'wickets', 'Completed');

-- -----------------------------------------------------------------------------
-- 6. BATTING SCORECARDS (Granular innings performances)
-- -----------------------------------------------------------------------------
INSERT INTO batting_scorecards (match_id, player_id, innings, batting_position, runs_scored, balls_faced, fours, sixes, dismissal_status) VALUES
-- Match 101 (Test): Jaiswal 161, Kohli 100, Rahul 77
(101, 3, 2, 1, 161, 297, 15, 3, 'out'),
(101, 11, 2, 2, 77, 176, 5, 0, 'out'),
(101, 2, 2, 4, 100, 143, 8, 2, 'not out'),
(101, 15, 2, 1, 89, 101, 8, 1, 'out'),
(101, 14, 2, 4, 17, 60, 2, 0, 'out'),

-- Match 103 (T20I World Cup Final): Kohli 76, Axar/Hardik, Klaasen 52
(103, 2, 1, 2, 76, 59, 6, 2, 'out'),
(103, 1, 1, 1, 9, 5, 2, 0, 'out'),
(103, 7, 1, 6, 5, 2, 1, 0, 'not out'),
(103, 25, 2, 5, 52, 27, 2, 5, 'out'),

-- Match 109 (ODI World Cup Final): Rohit 47, Kohli 54, KL Rahul 66, Travis Head 137
(109, 1, 1, 1, 47, 31, 4, 3, 'out'),
(109, 4, 1, 2, 4, 7, 0, 0, 'out'),
(109, 2, 1, 3, 54, 63, 4, 0, 'out'),
(109, 11, 1, 5, 66, 107, 1, 0, 'out'),
(109, 15, 2, 1, 137, 120, 15, 4, 'out'),
(109, 18, 2, 4, 58, 110, 4, 0, 'not out'),

-- Match 110 (ODI Semi-Final): Rohit 47, Gill 80, Kohli 117, Iyer 105
(110, 1, 1, 1, 47, 29, 4, 4, 'out'),
(110, 4, 1, 2, 80, 66, 8, 3, 'retired hurt'),
(110, 2, 1, 3, 117, 113, 9, 2, 'out'),

-- Match 111 (ODI vs SA): Rohit 40, Kohli 101, Jadeja 29
(111, 1, 1, 1, 40, 24, 6, 2, 'out'),
(111, 2, 1, 3, 101, 121, 10, 0, 'not out'),
(111, 6, 1, 7, 29, 15, 3, 1, 'not out'),

-- Match 119 (Asia Cup vs PAK): Rohit 56, Gill 58, Kohli 122, Rahul 111
(119, 1, 1, 1, 56, 49, 6, 4, 'out'),
(119, 4, 1, 2, 58, 52, 10, 0, 'out'),
(119, 2, 1, 3, 122, 94, 9, 3, 'not out'),
(119, 11, 1, 4, 111, 106, 12, 2, 'not out'),

-- Additional scorecards to support multi-format averages, 1000+ runs for all-rounders, quarter trends
(104, 21, 1, 4, 29, 60, 2, 0, 'out'),
(104, 21, 2, 4, 103, 140, 10, 1, 'out'),
(104, 6, 1, 6, 87, 180, 5, 1, 'out'),
(105, 3, 1, 1, 209, 290, 19, 7, 'out'),
(106, 1, 1, 1, 131, 196, 14, 3, 'out'),
(106, 6, 1, 5, 112, 225, 9, 2, 'out'),
(118, 20, 1, 5, 43, 70, 3, 1, 'out'),
(118, 20, 2, 5, 155, 214, 9, 9, 'out'),
(120, 7, 1, 5, 71, 30, 7, 5, 'not out'),
(120, 16, 2, 4, 24, 16, 2, 1, 'out'),
(121, 1, 1, 1, 46, 20, 4, 4, 'not out'),
(113, 6, 1, 7, 45, 69, 5, 0, 'not out'),
(115, 2, 2, 3, 54, 72, 2, 1, 'out');

-- -----------------------------------------------------------------------------
-- 7. BOWLING SCORECARDS (Economy, wickets, overs across venues)
-- -----------------------------------------------------------------------------
INSERT INTO bowling_scorecards (match_id, player_id, innings, overs_bowled, maidens, runs_conceded, wickets_taken, dot_balls) VALUES
-- Match 101: Bumrah 5/30, Starc 3/85, Hazlewood 2/45
(101, 8, 1, 18.0, 4, 30, 5, 70),
(101, 13, 2, 25.0, 4, 85, 3, 90),
(101, 17, 2, 21.0, 5, 45, 2, 80),
(101, 12, 2, 20.0, 3, 60, 1, 72),

-- Match 103 (T20I Final): Bumrah 2/18 in 4 ov, Hardik 3/20, Nortje/Rabada
(103, 8, 2, 4.0, 0, 18, 2, 14),
(103, 7, 2, 3.0, 0, 20, 3, 10),
(103, 24, 1, 4.0, 0, 36, 1, 9),

-- Match 109 (World Cup Final): Starc 3/55, Cummins 2/34, Bumrah 2/43, Shami 1/47
(109, 13, 1, 10.0, 0, 55, 3, 32),
(109, 12, 1, 10.0, 1, 34, 2, 36),
(109, 8, 2, 9.0, 2, 43, 2, 30),
(109, 9, 2, 7.0, 1, 47, 1, 22),

-- Match 110 (World Cup Semi-Final): Shami 7/57!
(110, 9, 2, 9.5, 0, 57, 7, 34),
(110, 8, 2, 10.0, 1, 64, 1, 31),
(110, 10, 2, 10.0, 0, 56, 1, 28),

-- Match 111 (vs SA): Jadeja 5/33
(111, 6, 2, 9.0, 1, 33, 5, 35),
(111, 9, 2, 5.0, 0, 18, 2, 18),

-- Match 106 (Test vs ENG): Jadeja 5/41, Kuldeep 2/22
(106, 6, 2, 12.4, 4, 41, 5, 52),
(106, 10, 2, 8.0, 1, 22, 2, 34),

-- Venues repeat for Q14 (Bumrah & Starc with >= 3 matches at specific venues)
(104, 8, 1, 15.0, 3, 41, 4, 60),
(106, 8, 1, 15.0, 2, 46, 2, 58),
(112, 8, 2, 10.0, 1, 35, 2, 38), -- Narendra Modi Stadium repeats for Bumrah (Matches 104, 106, 109, 112)
(114, 13, 1, 8.0, 1, 37, 5, 30),
(113, 13, 2, 10.0, 1, 49, 3, 34),
(115, 13, 2, 10.0, 0, 62, 1, 28); -- Starc repeats at multiple grounds

-- -----------------------------------------------------------------------------
-- 8. FIELDING SCORECARDS (For Q21 Comprehensive Performance Ranking)
-- -----------------------------------------------------------------------------
INSERT INTO fielding_scorecards (match_id, player_id, innings, catches, stumpings, run_outs) VALUES
(101, 2, 2, 2, 0, 0), -- Virat Kohli catches
(101, 5, 2, 3, 1, 0), -- Rishabh Pant keeper catches/stumpings
(103, 5, 2, 2, 0, 0),
(109, 14, 1, 2, 0, 0), -- Steve Smith catches
(109, 19, 1, 3, 0, 0), -- Alex Carey keeper catches
(110, 6, 2, 3, 0, 1), -- Ravindra Jadeja fielding masterclass
(111, 2, 2, 1, 0, 0),
(119, 11, 1, 2, 1, 0); -- KL Rahul keeper catches/stumpings

-- -----------------------------------------------------------------------------
-- 9. PARTNERSHIPS (Consecutive batsmen scoring 100+ and 50+ runs for Q13 & Q24)
-- -----------------------------------------------------------------------------
INSERT INTO partnerships (match_id, innings, player1_id, player2_id, player1_position, player2_position, partnership_runs, balls_faced) VALUES
-- Jaiswal & Rahul (Pos 1 & 2): 201 runs in Match 101
(101, 2, 3, 11, 1, 2, 201, 380),

-- Rohit & Gill (Pos 1 & 2): 71 runs in Match 110, 121 runs in Match 119
(110, 1, 1, 4, 1, 2, 71, 50),
(119, 1, 1, 4, 1, 2, 121, 100),

-- Gill & Kohli (Pos 2 & 3): 93 runs in Match 110
(110, 1, 4, 2, 2, 3, 93, 86),

-- Kohli & Rahul (Pos 3 & 4): 233* runs in Match 119
(119, 1, 2, 11, 3, 4, 233, 194),

-- Travis Head & Marnus Labuschagne (Pos 3 & 4/consecutive): 192 runs in Match 109 Final
(109, 2, 15, 18, 3, 4, 192, 215),

-- Additional partnerships to satisfy partnerships count >= 5
(104, 1, 1, 4, 1, 2, 80, 75),
(105, 1, 1, 4, 1, 2, 95, 88),
(111, 1, 1, 4, 1, 2, 62, 50);
