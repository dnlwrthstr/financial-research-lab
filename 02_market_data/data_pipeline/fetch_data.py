"""Market data generation and normalization helpers.

The lab defaults to reproducible synthetic OHLCV data so notebooks can run
offline. A live provider such as yfinance can be added later behind the same
normalized schema.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OHLCV_COLUMNS = ["date", "ticker", "open", "high", "low", "close", "volume"]


def generate_synthetic_ohlcv(
    ticker: str = "NESN.SW",
    start: str = "2024-01-02",
    periods: int = 252,
    start_price: float = 105.0,
    drift: float = 0.00025,
    volatility: float = 0.010,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate a reproducible OHLCV time series for one ticker."""

    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start, periods=periods)
    returns = rng.normal(loc=drift, scale=volatility, size=periods)
    close = start_price * np.cumprod(1 + returns)
    open_price = close * (1 + rng.normal(0, 0.003, periods))
    high = np.maximum(open_price, close) * (1 + rng.uniform(0.001, 0.012, periods))
    low = np.minimum(open_price, close) * (1 - rng.uniform(0.001, 0.012, periods))
    volume = rng.integers(1_200_000, 5_000_000, periods)

    data = pd.DataFrame(
        {
            "date": dates,
            "ticker": ticker,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    return normalize_ohlcv(data)


def normalize_ohlcv(data: pd.DataFrame) -> pd.DataFrame:
    """Return OHLCV data with standard columns, types, and ordering."""

    missing = set(OHLCV_COLUMNS) - set(data.columns)
    if missing:
        raise ValueError(f"Missing OHLCV columns: {sorted(missing)}")

    normalized = data.loc[:, OHLCV_COLUMNS].copy()
    normalized["date"] = pd.to_datetime(normalized["date"])
    normalized["ticker"] = normalized["ticker"].astype(str)
    numeric_columns = ["open", "high", "low", "close", "volume"]
    normalized[numeric_columns] = normalized[numeric_columns].apply(pd.to_numeric)
    normalized = normalized.sort_values(["ticker", "date"]).reset_index(drop=True)
    return normalized


def add_return_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Add simple returns, log returns, and traded value."""

    enriched = normalize_ohlcv(data)
    enriched["simple_return"] = enriched.groupby("ticker")["close"].pct_change()
    enriched["log_return"] = np.log(enriched["close"] / enriched.groupby("ticker")["close"].shift(1))
    enriched["traded_value"] = enriched["close"] * enriched["volume"]
    return enriched


def save_ohlcv(data: pd.DataFrame, path: str | Path) -> Path:
    """Save normalized OHLCV data to CSV."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    normalize_ohlcv(data).to_csv(output_path, index=False)
    return output_path


def load_ohlcv(path: str | Path) -> pd.DataFrame:
    """Load normalized OHLCV data from CSV."""

    return normalize_ohlcv(pd.read_csv(path))


def main() -> None:
    output_path = Path("data/raw/synthetic_ohlcv.csv")
    data = generate_synthetic_ohlcv()
    save_ohlcv(data, output_path)
    print(f"Wrote {len(data)} rows to {output_path}")


if __name__ == "__main__":
    main()
