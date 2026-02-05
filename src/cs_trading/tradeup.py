from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from .models import Opportunity
from .scoring import compute_expected_profit, compute_margin_pct


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
        margin_pct = compute_margin_pct(candidate.buy_cny, candidate.sell_cny)
        expected_profit_cny = compute_expected_profit(candidate.buy_cny, candidate.sell_cny)
        spread_pct = 0.0
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
                expected_profit_cny=expected_profit_cny,
                spread_pct=spread_pct,
                volume=candidate.volume,
                source="BUFF",
            )
        )
    return opportunities
