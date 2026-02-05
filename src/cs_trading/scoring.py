from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreInputs:
    buy_cny: float
    sell_cny: float
    volume: int


def compute_margin_pct(buy_cny: float, sell_cny: float, fee_pct: float = 2.5) -> float:
    fee = sell_cny * fee_pct / 100
    if buy_cny <= 0:
        return 0.0
    return ((sell_cny - fee) - buy_cny) / buy_cny * 100


def compute_score(
    inputs: ScoreInputs,
    bonus_limit_pct: float,
    min_margin_pct: float,
) -> tuple[float, float]:
    margin_pct = compute_margin_pct(inputs.buy_cny, inputs.sell_cny)
    if margin_pct < min_margin_pct:
        return margin_pct, 0.0
    bonus_pct = min(bonus_limit_pct, max(0.0, margin_pct * 0.25))
    score = margin_pct + bonus_pct
    return margin_pct, score
