from __future__ import annotations

from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, Field


class BuffConfig(BaseModel):
    base_url: str = "https://buff.163.com"
    game: str = "csgo"
    request_delay_s: float = 1.0
    user_agent: str = "cs-trading/0.1"


class ScannerConfig(BaseModel):
    bonus_limit_pct: float = 5.0
    fee_pct: float = 2.5
    budget_cny: float = 5000.0
    circuit_breaker_cny: float = 1000.0
    min_volume: int = 20
    min_margin_pct: float = 2.0
    max_spread_pct: float = 15.0
    max_pages: int = 1


class OutputConfig(BaseModel):
    csv_path: str = "output/opportunities.csv"


class TradeupConfig(BaseModel):
    enabled: bool = True
    wear_tiers: List[str] = Field(default_factory=list)


class AppConfig(BaseModel):
    buff: BuffConfig = Field(default_factory=BuffConfig)
    scanner: ScannerConfig = Field(default_factory=ScannerConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    tradeup: TradeupConfig = Field(default_factory=TradeupConfig)


def load_config(path: Path) -> AppConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AppConfig.model_validate(data)
