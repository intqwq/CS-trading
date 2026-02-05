from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .models import Opportunity


def write_opportunities(path: Path, opportunities: Iterable[Opportunity]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "timestamp",
                "type",
                "item_name",
                "buy_cny",
                "sell_cny",
                "margin_pct",
                "bonus_pct",
                "score",
                "expected_profit_cny",
                "spread_pct",
                "volume",
                "source",
            ]
        )
        for opp in opportunities:
            writer.writerow(
                [
                    opp.timestamp.isoformat(),
                    opp.kind,
                    opp.name,
                    f"{opp.buy_cny:.2f}",
                    f"{opp.sell_cny:.2f}",
                    f"{opp.margin_pct:.2f}",
                    f"{opp.bonus_pct:.2f}",
                    f"{opp.score:.2f}",
                    f"{opp.expected_profit_cny:.2f}",
                    f"{opp.spread_pct:.2f}",
                    opp.volume,
                    opp.source,
                ]
            )
