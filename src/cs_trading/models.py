from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ItemListing:
    goods_id: int
    name: str
    price_cny: float
    sell_min_cny: float
    volume: int
    buy_max_cny: Optional[float] = None


@dataclass(frozen=True)
class Opportunity:
    timestamp: datetime
    kind: str
    name: str
    buy_cny: float
    sell_cny: float
    margin_pct: float
    bonus_pct: float
    score: float
    expected_profit_cny: float
    spread_pct: float
    volume: int
    source: str
