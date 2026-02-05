# CS Trading Scanner (BUFF)

A cross-platform (Windows/Linux) scanner that pulls BUFF market data, computes statistically preferable trades/tradeups, and logs results to CSV (no auto-buy/sell).

## Goals
- Prefer **API endpoints** over cookies where possible.
- Operate in **CNY** by default (BUFF native currency).
- Support **bonus limit (percentage)**, **budget**, and **circuit breaker** (absolute currency).
- Output results to **CSV**.
- Designed for Windows development and Ubuntu/Raspberry Pi runtime.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cs-trading --config config/example.yaml
```

## Configuration
See `config/example.yaml` for the full schema. Key settings:
- `buff.base_url`: BUFF API base URL
- `scanner.bonus_limit_pct`: max bonus in percent (e.g. 5.0)
- `scanner.budget_cny`: total budget in CNY
- `scanner.circuit_breaker_cny`: halt threshold in CNY
- `output.csv_path`: where to write log output

## Data sources
This scanner uses BUFF market endpoints (see `docs/buff_endpoints.md`).

## Notes
This project only logs opportunities; it does **not** perform automated purchases or listings.
