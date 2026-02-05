from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

import requests


@dataclass(frozen=True)
class BuffResponse:
    data: Dict


class BuffClient:
    def __init__(self, base_url: str, game: str, user_agent: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.game = game
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def _get(self, path: str, params: Dict) -> BuffResponse:
        url = f"{self.base_url}{path}"
        response = self.session.get(url, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()
        return BuffResponse(data=payload)

    def list_goods(self, page: int = 1, sort_by: str = "price.asc") -> BuffResponse:
        return self._get(
            "/api/market/goods",
            {
                "game": self.game,
                "page_num": page,
                "sort_by": sort_by,
            },
        )

    def sell_orders(self, goods_id: int, page: int = 1) -> BuffResponse:
        return self._get(
            "/api/market/goods/sell_order",
            {
                "game": self.game,
                "goods_id": goods_id,
                "page_num": page,
            },
        )


def iter_goods_pages(client: BuffClient, max_pages: int) -> Iterable[BuffResponse]:
    for page in range(1, max_pages + 1):
        yield client.list_goods(page=page)
