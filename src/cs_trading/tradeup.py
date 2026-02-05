from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from .models import Opportunity


@dataclass(frozen=True)
class TradeupCandidate:
    name: str
    buy_cny: float
    sell_cny: float
    volume: int


def evaluate_tradeups(candidates: List[TradeupCandidate]) -> List[Opportunity]:
    opportunities: List[Opportunity] = []
    timestamp = datetime.now(timezone.utc)
    for candidate in candidates:
        if candidate.buy_cny <= 0:
            continue
        margin_pct = ((candidate.sell_cny - candidate.buy_cny) / candidate.buy_cny) * 100
        opportunities.append(
            Opportunity(
                timestamp=timestamp,
                kind="tradeup",
                name=candidate.name,
                buy_cny=candidate.buy_cny,
                sell_cny=candidate.sell_cny,
                margin_pct=margin_pct,
                bonus_pct=0.0,
                score=margin_pct,
                volume=candidate.volume,
                source="BUFF",
            )
        )
    return opportunities
