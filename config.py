"""
Configuration settings for the AI Receptionist application
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,   # ❗ IMPORTANT FIX
        extra="ignore"
    )

    # ================= SERVER =================
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # ================= CORS =================
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # ================= OPENAI =================
    OPENAI_API_KEY: str ="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"
    OPENAI_MODEL: str ="gpt-4o-mini"

    # ================= GOOGLE SHEETS =================
    GOOGLE_SHEETS_CREDENTIALS_FILE: str = "credentials.json"
    GOOGLE_SHEETS_SPREADSHEET_ID: str = ""

    # ================= EMAIL =================
    EMAIL_ENABLED: bool = True
    EMAIL_FROM: str = "noreply@softechsol.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""

    # ================= AI RECEPTIONIST =================
    COMPANY_NAME: str = "Softechsol"
    COMPANY_EMAIL: str = "hamdzahid73@gmail.com"
    COMPANY_PHONE: str = "+1-555-0123"
    BUSINESS_HOURS: str = "Monday-Friday, 9 AM - 5 PM"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
