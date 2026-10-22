"""
Database Initialization Script for Cricbuzz LiveStats.
Executes schema.sql and seed_data.sql to prepare MySQL for the application.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def initialize_database():
    """Initializes the MySQL database with tables and seed data."""
    cfg = settings.db
    logger.info("Attempting to initialize MySQL database on %s:%s with user '%s'...", cfg.host, cfg.port, cfg.user)

    # 1. Connect without selecting database to execute CREATE DATABASE
    try:
        conn = pymysql.connect(
            host=cfg.host,
            port=cfg.port,
            user=cfg.user,
            password=cfg.password,
            charset="utf8mb4",
            autocommit=True,
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
            connect_timeout=5,
        )
    except pymysql.MySQLError as err:
        logger.error("Could not connect to MySQL server: %s", err)
        print(f"\n❌ MySQL Connection Failed: {err}")
        print("\n👉 Please check your password in .env (DB_PASSWORD=your_password).")
        return False

    try:
        # Read schema.sql
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        logger.info("Executing schema.sql DDL statements...")
        with conn.cursor() as cursor:
            cursor.execute(schema_sql)
        logger.info("Schema created successfully!")

        # Read seed_data.sql
        seed_path = os.path.join(os.path.dirname(__file__), "seed_data.sql")
        with open(seed_path, "r", encoding="utf-8") as f:
            seed_sql = f.read()

        logger.info("Executing seed_data.sql DML statements...")
        with conn.cursor() as cursor:
            cursor.execute(seed_sql)
        logger.info("Seed data ingested successfully!")

        print("\n✅ MySQL Database 'cricbuzz_db' initialized and seeded successfully!")
        return True

    except Exception as exc:
        logger.exception("Error executing database scripts: %s", exc)
        print(f"\n❌ Error during database initialization: {exc}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
