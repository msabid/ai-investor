from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

def b(v, default=False):
    if v is None:
        return default
    return str(v).lower() in ["true", "1", "yes", "y"]

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///database/portfolio_command_center.db")
    default_admin_email: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@example.com")
    default_admin_password: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "ChangeMeNow123!")
    execution_mode: str = os.getenv("EXECUTION_MODE", "PAPER")
    live_trading_enabled: bool = b(os.getenv("LIVE_TRADING_ENABLED", "false"))
    paper_trading_enabled: bool = b(os.getenv("PAPER_TRADING_ENABLED", "true"))
    agent_execution_enabled: bool = b(os.getenv("AGENT_EXECUTION_ENABLED", "true"))
    human_approval_required: bool = b(os.getenv("HUMAN_APPROVAL_REQUIRED", "true"))
    broker_mode: str = os.getenv("BROKER_MODE", "paper")

SETTINGS = Settings()
