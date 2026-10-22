-- =============================================================================
-- CRICBUZZ LIVESTATS - DATABASE SCHEMA DEFINITION (MySQL 8.0+)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS cricbuzz_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cricbuzz_db;

-- 1. TEAMS TABLE
CREATE TABLE IF NOT EXISTS teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    team_short_name VARCHAR(10) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. VENUES TABLE
CREATE TABLE IF NOT EXISTS venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity INT UNSIGNED NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_venue_capacity CHECK (capacity >= 0)
) ENGINE=InnoDB;

-- 3. SERIES TABLE
CREATE TABLE IF NOT EXISTS series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100) NOT NULL,
    match_type ENUM('Test', 'ODI', 'T20I', 'T20') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    total_matches INT UNSIGNED NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 4. PLAYERS TABLE
CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(150) NOT NULL,
    team_id INT NOT NULL,
    role ENUM('Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper') NOT NULL,
    batting_style VARCHAR(50) NOT NULL,
    bowling_style VARCHAR(50) DEFAULT 'None',
    date_of_birth DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE RESTRICT,
    INDEX idx_players_team (team_id),
    INDEX idx_players_role (role)
) ENGINE=InnoDB;

-- 5. MATCHES TABLE
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_description VARCHAR(255) NOT NULL,
    series_id INT NULL,
    match_format ENUM('Test', 'ODI', 'T20I', 'T20') NOT NULL,
    match_date DATE NOT NULL,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    venue_id INT NOT NULL,
    toss_winner_id INT NULL,
    toss_decision ENUM('bat', 'bowl') NULL,
    winner_id INT NULL,
    victory_margin INT UNSIGNED NULL,
    victory_type ENUM('runs', 'wickets', 'tie', 'no result') NULL,
    match_status ENUM('Scheduled', 'Live', 'Completed', 'Abandoned') DEFAULT 'Completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(series_id) ON DELETE SET NULL,
    FOREIGN KEY (team1_id) REFERENCES teams(team_id) ON DELETE RESTRICT,
    FOREIGN KEY (team2_id) REFERENCES teams(team_id) ON DELETE RESTRICT,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE RESTRICT,
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    INDEX idx_matches_date (match_date),
    INDEX idx_matches_format (match_format),
    INDEX idx_matches_teams (team1_id, team2_id),
    INDEX idx_matches_venue (venue_id)
) ENGINE=InnoDB;

-- 6. BATTING SCORECARDS TABLE
CREATE TABLE IF NOT EXISTS batting_scorecards (
    batting_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    innings TINYINT UNSIGNED NOT NULL DEFAULT 1,
    batting_position TINYINT UNSIGNED NOT NULL,
    runs_scored INT UNSIGNED NOT NULL DEFAULT 0,
    balls_faced INT UNSIGNED NOT NULL DEFAULT 0,
    fours INT UNSIGNED NOT NULL DEFAULT 0,
    sixes INT UNSIGNED NOT NULL DEFAULT 0,
    strike_rate DECIMAL(6,2) GENERATED ALWAYS AS (
        CASE WHEN balls_faced > 0 THEN (runs_scored / balls_faced) * 100.0 ELSE 0.0 END
    ) STORED,
    dismissal_status ENUM('out', 'not out', 'retired hurt') DEFAULT 'out',
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE RESTRICT,
    UNIQUE KEY uq_match_player_innings (match_id, player_id, innings),
    INDEX idx_batting_player (player_id),
    INDEX idx_batting_match (match_id)
) ENGINE=InnoDB;

-- 7. BOWLING SCORECARDS TABLE
CREATE TABLE IF NOT EXISTS bowling_scorecards (
    bowling_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    innings TINYINT UNSIGNED NOT NULL DEFAULT 1,
    overs_bowled DECIMAL(4,1) UNSIGNED NOT NULL DEFAULT 0.0,
    maidens INT UNSIGNED NOT NULL DEFAULT 0,
    runs_conceded INT UNSIGNED NOT NULL DEFAULT 0,
    wickets_taken INT UNSIGNED NOT NULL DEFAULT 0,
    economy_rate DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE WHEN overs_bowled > 0 THEN runs_conceded / (FLOOR(overs_bowled) + (overs_bowled - FLOOR(overs_bowled))*10/6) ELSE 0.0 END
    ) STORED,
    dot_balls INT UNSIGNED DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE RESTRICT,
    UNIQUE KEY uq_match_bowler_innings (match_id, player_id, innings),
    INDEX idx_bowling_player (player_id),
    INDEX idx_bowling_match (match_id)
) ENGINE=InnoDB;

-- 8. FIELDING SCORECARDS TABLE
CREATE TABLE IF NOT EXISTS fielding_scorecards (
    fielding_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    innings TINYINT UNSIGNED NOT NULL DEFAULT 1,
    catches INT UNSIGNED NOT NULL DEFAULT 0,
    stumpings INT UNSIGNED NOT NULL DEFAULT 0,
    run_outs INT UNSIGNED NOT NULL DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE RESTRICT,
    UNIQUE KEY uq_match_fielder_innings (match_id, player_id, innings),
    INDEX idx_fielding_player (player_id)
) ENGINE=InnoDB;

-- 9. PARTNERSHIPS TABLE
CREATE TABLE IF NOT EXISTS partnerships (
    partnership_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings TINYINT UNSIGNED NOT NULL DEFAULT 1,
    player1_id INT NOT NULL,
    player2_id INT NOT NULL,
    player1_position TINYINT UNSIGNED NOT NULL,
    player2_position TINYINT UNSIGNED NOT NULL,
    partnership_runs INT UNSIGNED NOT NULL DEFAULT 0,
    balls_faced INT UNSIGNED NOT NULL DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player1_id) REFERENCES players(player_id) ON DELETE RESTRICT,
    FOREIGN KEY (player2_id) REFERENCES players(player_id) ON DELETE RESTRICT,
    INDEX idx_partnership_players (player1_id, player2_id),
    INDEX idx_partnership_match (match_id)
) ENGINE=InnoDB;
