# BUFF Endpoints (reference)

These endpoints are used to retrieve market information via HTTP (preferred over cookies where possible). The scanner targets BUFF's public market APIs for listing data and sell orders.

## Market listings
- Endpoint: `/api/market/goods`
- Example:
  ```
  https://buff.163.com/api/market/goods?game=csgo&page_num=1&sort_by=price.asc
  ```
- Notes:
  - Returns goods list with price and volume information.
  - Paginated via `page_num`.

## Sell orders for a specific item
- Endpoint: `/api/market/goods/sell_order`
- Example:
  ```
  https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=12345&page_num=1
  ```
- Notes:
  - Returns sell orders for a single `goods_id`.

## Price history (optional)
- Endpoint: `/api/market/goods/price_history`
- Example:
  ```
  https://buff.163.com/api/market/goods/price_history?game=csgo&goods_id=12345
  ```

## Currency
BUFF prices are in **CNY**.
