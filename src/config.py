from dotenv import load_dotenv
import os
from pydantic import BaseModel, AnyHttpUrl, ValidationError
from typing import Optional

load_dotenv()

class Config(BaseModel):
    # ServiceNow
    SN_INSTANCE: Optional[AnyHttpUrl] = os.getenv("SN_INSTANCE") or None
    SN_USER: Optional[str] = os.getenv("SN_USER") or None
    SN_PASS: Optional[str] = os.getenv("SN_PASS") or None

    # Teams
    TEAMS_WEBHOOK_URL: Optional[AnyHttpUrl] = os.getenv("TEAMS_WEBHOOK_URL") or None

    # SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER") or None
    SMTP_PASS: Optional[str] = os.getenv("SMTP_PASS") or None
    SMTP_FROM: str = os.getenv("SMTP_FROM", "lab@example.local")
    SMTP_TO: str = os.getenv("SMTP_TO", "oncall@example.local")

def get_config() -> Config:
    try:
        return Config()
    except ValidationError as e:
        raise SystemExit(f"Config validation error: {e}")
