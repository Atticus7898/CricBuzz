"""
Centralized Configuration Module for Cricbuzz LiveStats.
Follows the 12-Factor App methodology.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file from project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))


@dataclass(frozen=True)
class DatabaseSettings:
    """MySQL Database connection configuration."""
    host: str = os.getenv("DB_HOST", "127.0.0.1")
    port: int = int(os.getenv("DB_PORT", "3306"))
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PASSWORD", "")
    database: str = os.getenv("DB_NAME", "cricbuzz_db")
    pool_name: str = os.getenv("DB_POOL_NAME", "cricbuzz_pool")
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))


@dataclass(frozen=True)
class APISettings:
    """Cricbuzz REST API configuration."""
    rapidapi_key: str = os.getenv("RAPIDAPI_KEY", "")
    rapidapi_host: str = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
    base_url: str = f"https://{os.getenv('RAPIDAPI_HOST', 'cricbuzz-cricket.p.rapidapi.com')}"
    request_timeout: int = int(os.getenv("API_TIMEOUT", "10"))
    max_retries: int = int(os.getenv("API_MAX_RETRIES", "3"))
    use_mock_on_failure: bool = os.getenv("USE_MOCK_ON_API_FAILURE", "true").lower() == "true"


@dataclass(frozen=True)
class AppSettings:
    """Application level settings."""
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    root_dir: str = ROOT_DIR
    db: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()


# Global Singleton Configuration Instance
settings = AppSettings()
