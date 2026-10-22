"""
Database Connection & Session Management Layer.
Supports MySQL 8.0/9.0 with connection pooling and automated transaction handling.
Includes graceful fallback mechanism and DataFrame helpers.
"""

from contextlib import contextmanager
from typing import Generator, Any, List, Dict, Optional, Tuple
import pandas as pd
import pymysql
from pymysql.cursors import DictCursor

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manages database connection lifecycle and query execution."""

    def __init__(self):
        self._cfg = settings.db

    def get_raw_connection(self):
        """Creates and returns a raw PyMySQL connection."""
        try:
            return pymysql.connect(
                host=self._cfg.host,
                port=self._cfg.port,
                user=self._cfg.user,
                password=self._cfg.password,
                database=self._cfg.database,
                charset="utf8mb4",
                cursorclass=DictCursor,
                autocommit=False,
                connect_timeout=5,
            )
        except pymysql.MySQLError as err:
            logger.error("Failed to connect to MySQL database '%s': %s", self._cfg.database, err)
            raise

    @contextmanager
    def get_connection(self) -> Generator[Any, None, None]:
        """
        Context manager for acquiring and releasing a connection.
        Automatically handles commit on success and rollback on exception.
        """
        conn = None
        try:
            conn = self.get_raw_connection()
            yield conn
            conn.commit()
        except Exception as exc:
            if conn:
                conn.rollback()
            logger.error("Transaction failed and was rolled back: %s", exc)
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_cursor(self) -> Generator[DictCursor, None, None]:
        """Context manager providing a DictCursor inside an active transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()

    def test_connection(self) -> Tuple[bool, str]:
        """Tests if MySQL server is reachable and credentials are valid."""
        try:
            conn = pymysql.connect(
                host=self._cfg.host,
                port=self._cfg.port,
                user=self._cfg.user,
                password=self._cfg.password,
                charset="utf8mb4",
                connect_timeout=3,
            )
            with conn.cursor() as cursor:
                cursor.execute("SELECT VERSION() AS version;")
                version = cursor.fetchone()[0]
            conn.close()
            return True, f"MySQL Connected successfully (Version: {version})"
        except Exception as exc:
            return False, f"MySQL Connection Error: {str(exc)}"

    def execute_ddl(self, sql_script: str) -> bool:
        """Executes a multi-statement DDL script (like schema.sql)."""
        conn = pymysql.connect(
            host=self._cfg.host,
            port=self._cfg.port,
            user=self._cfg.user,
            password=self._cfg.password,
            charset="utf8mb4",
            autocommit=True,
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
            logger.info("Executed DDL script successfully.")
            return True
        except Exception as exc:
            logger.error("Failed to execute DDL script: %s", exc)
            raise
        finally:
            conn.close()

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Executes a SELECT query and returns all rows as a list of dicts."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """Executes a SELECT query and returns a single row dictionary."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def execute_write(self, query: str, params: Optional[Tuple] = None) -> int:
        """Executes an INSERT/UPDATE/DELETE query and returns the last inserted ID or affected rows."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid or cursor.rowcount

    def fetch_dataframe(self, query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
        """
        Executes a SELECT query and returns the result as a Pandas DataFrame.
        Constructs directly from fetch_all dictionary records to guarantee proper cell values.
        """
        rows = self.fetch_all(query, params)
        if not rows:
            with self.get_cursor() as cursor:
                cursor.execute(query, params or ())
                cols = [desc[0] for desc in cursor.description] if cursor.description else []
                return pd.DataFrame(columns=cols)
        
        df = pd.DataFrame(rows)
        # Convert any Decimal objects to float/int for proper serialization & Plotly charting
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass
        return df


# Global DB Manager Instance
db_manager = DatabaseManager()
