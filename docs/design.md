# Design: Counter-Strike Auto Trading Scanner (BUFF)

## Objective
Scan BUFF CS:GO market data using API endpoints, evaluate statistically preferable trades and tradeups, and log them to CSV. No auto-buy/sell.

## Key constraints
- Use BUFF endpoints (prefer API to cookies).
- Currency: **CNY**.
- Bonus: percentage-based (`bonus_limit_pct`).
- Budget and circuit breaker: absolute CNY.
- Cross-platform (Windows + Ubuntu/Raspberry Pi).

## Architecture
```
cs_trading/
  cli.py
  config.py
  buff_client.py
  models.py
  scoring.py
  tradeup.py
  csv_writer.py
```

### Data flow
1. **BUFF Client** fetches listing pages.
2. **Normalizer** maps raw fields to internal `ItemListing`.
3. **Scoring Engine** computes margins and preference score (bonus capped).
4. **Tradeup Engine** evaluates tradeup bundles (optional).
5. **CSV Writer** logs ranked opportunities.

## Scoring model
- **Expected margin**: `(sell_price - buy_price - fees) / buy_price`.
- **Liquidity filter**: volume threshold and max spread.
- **Bonus**: add `min(bonus_limit_pct, margin_pct * bonus_factor)`.
- **Circuit breaker**: halt if aggregate risk exceeds `circuit_breaker_cny`.

## Tradeup model (initial)
- Tradeup is computed from item rarity/wear buckets.
- Placeholder EV computation uses current BUFF price averages.
- Tradeups are ranked with the same preference score and logged to CSV.

## Output
CSV log with columns:
- `timestamp`, `type`, `item_name`, `buy_cny`, `sell_cny`, `margin_pct`, `bonus_pct`, `score`, `volume`, `source`
