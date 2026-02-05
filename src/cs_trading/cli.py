from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

from .buff_client import BuffClient, iter_goods_pages
from .config import AppConfig, load_config
from .csv_writer import write_opportunities
from .models import ItemListing, Opportunity
from .scoring import ScoreInputs, compute_score


def parse_goods(payload: dict) -> Iterable[ItemListing]:
    items = payload.get("data", {}).get("items", [])
    for item in items:
        try:
            goods_id = int(item.get("id"))
            name = item.get("name")
            sell_min = float(item.get("sell_min_price") or item.get("price") or 0)
            buy_max = item.get("buy_max_price")
            buy_max_value = float(buy_max) if buy_max is not None else None
            volume = int(item.get("sell_num") or item.get("sell_count") or 0)
        except (TypeError, ValueError):
            continue

        if not name:
            continue

        yield ItemListing(
            goods_id=goods_id,
            name=name,
            price_cny=sell_min,
            sell_min_cny=sell_min,
            volume=volume,
            buy_max_cny=buy_max_value,
        )


def compute_spread_pct(buy_cny: float, sell_cny: float) -> float:
    if sell_cny <= 0:
        return 100.0
    return (sell_cny - buy_cny) / sell_cny * 100


def scan_market(config: AppConfig, max_pages: int) -> List[Opportunity]:
    client = BuffClient(
        base_url=config.buff.base_url,
        game=config.buff.game,
        user_agent=config.buff.user_agent,
    )
    opportunities: List[Opportunity] = []

    for response in iter_goods_pages(client, max_pages=max_pages):
        for listing in parse_goods(response.data):
            if listing.volume < config.scanner.min_volume:
                continue

            buy_cny = listing.buy_max_cny or listing.sell_min_cny
            sell_cny = listing.sell_min_cny

            if buy_cny > config.scanner.budget_cny:
                continue

            if buy_cny >= config.scanner.circuit_breaker_cny:
                return opportunities

            spread_pct = compute_spread_pct(buy_cny, sell_cny)
            if spread_pct > config.scanner.max_spread_pct:
                continue

            margin_pct, score = compute_score(
                ScoreInputs(
                    buy_cny=buy_cny,
                    sell_cny=sell_cny,
                    volume=listing.volume,
                ),
                bonus_limit_pct=config.scanner.bonus_limit_pct,
                min_margin_pct=config.scanner.min_margin_pct,
            )
            if score <= 0:
                continue

            bonus_pct = max(0.0, score - margin_pct)
            opportunities.append(
                Opportunity(
                    timestamp=datetime.now(timezone.utc),
                    kind="trade",
                    name=listing.name,
                    buy_cny=buy_cny,
                    sell_cny=sell_cny,
                    margin_pct=margin_pct,
                    bonus_pct=bonus_pct,
                    score=score,
                    volume=listing.volume,
                    source="BUFF",
                )
            )

        time.sleep(config.buff.request_delay_s)

    return opportunities


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BUFF CS trading scanner")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--pages", type=int, default=1)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)
    opportunities = scan_market(config, max_pages=args.pages)

    output_path = Path(config.output.csv_path)
    write_opportunities(output_path, opportunities)

    print(f"Wrote {len(opportunities)} opportunities to {output_path}")


if __name__ == "__main__":
    main()
