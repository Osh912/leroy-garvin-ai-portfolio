from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
TRUTH_DIR = APP_DIR / "truth"
PORTFOLIO_ROOT = ROOT.parent
MASTER_RESUME = PORTFOLIO_ROOT / "FINAL_MASTER_RESUME.md"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    greenhouse_boards: str = (
        "openai,anthropic,gitlab,automattic,zapier,stripe,datadog,airtable,"
        "hubspot,canonical,elastic,cloudflare,mozilla,docker,gusto,"
        "cloudinary,hashicorp,figma,notion,discord"
    )
    lever_companies: str = (
        "netflix,shopify,figma,canonical,twitch,spotify,reddit,duolingo"
    )
    ashby_boards: str = "openai,anthropic,ramp,notion"
    workable_companies: str = "qase,customer-io,tekion"
    database_url: str = f"sqlite:///{ROOT / 'data' / 'job_machine.db'}"
    host: str = "127.0.0.1"
    port: int = 8787

    @property
    def greenhouse_board_list(self) -> list[str]:
        return [x.strip() for x in self.greenhouse_boards.split(",") if x.strip()]

    @property
    def lever_company_list(self) -> list[str]:
        return [x.strip() for x in self.lever_companies.split(",") if x.strip()]

    @property
    def ashby_board_list(self) -> list[str]:
        return [x.strip() for x in self.ashby_boards.split(",") if x.strip()]

    @property
    def workable_company_list(self) -> list[str]:
        return [x.strip() for x in self.workable_companies.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
