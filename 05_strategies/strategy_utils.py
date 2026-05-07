"""Strategy research helpers for the lab notebooks."""

from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def generate_strategy_universe(periods: int = 504, n_assets: int = 24, seed: int = 515) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate synthetic prices, returns, and fundamentals for strategy tests."""

    rng = np.random.default_rng(seed)
    tickers = [f"Stock_{i:02d}" for i in range(1, n_assets + 1)]
    dates = pd.bdate_range("2024-01-02", periods=periods)

    market = rng.normal(0.00025, 0.009, periods)
    quality = rng.normal(0, 1, n_assets)
    value = rng.normal(0, 1, n_assets)
    momentum_trait = rng.normal(0, 1, n_assets)
    beta = rng.uniform(0.65, 1.25, n_assets)
    idiosyncratic_vol = rng.uniform(0.006, 0.014, n_assets)

    returns = pd.DataFrame(index=dates, columns=tickers, dtype=float)
    for i, ticker in enumerate(tickers):
        alpha = 0.00003 + 0.00004 * quality[i] + 0.00003 * value[i] + 0.00002 * momentum_trait[i]
        noise = rng.normal(0, idiosyncratic_vol[i], periods)
        returns[ticker] = alpha + beta[i] * market + noise

    prices = 100 * (1 + returns).cumprod()
    fundamentals = pd.DataFrame(
        {
            "ticker": tickers,
            "pe": np.clip(20 - 3.5 * value + rng.normal(0, 2, n_assets), 7, 35),
            "price_book": np.clip(3.0 - 0.45 * value + rng.normal(0, 0.35, n_assets), 0.8, 6.0),
            "ev_ebitda": np.clip(13 - 1.8 * value + rng.normal(0, 1.2, n_assets), 5, 24),
            "roic": np.clip(0.10 + 0.035 * quality + rng.normal(0, 0.015, n_assets), 0.03, 0.25),
            "gross_margin": np.clip(0.38 + 0.08 * quality + rng.normal(0, 0.03, n_assets), 0.15, 0.70),
            "debt_to_ebitda": np.clip(2.4 - 0.45 * quality + rng.normal(0, 0.35, n_assets), 0.2, 5.0),
            "market_cap": rng.uniform(8_000, 250_000, n_assets),
        }
    )
    return prices, returns, fundamentals


def annualized_return(returns: pd.Series) -> float:
    compounded = (1 + returns).prod()
    years = len(returns) / TRADING_DAYS
    return float(compounded ** (1 / years) - 1)


def annualized_volatility(returns: pd.Series) -> float:
    return float(returns.std() * np.sqrt(TRADING_DAYS))


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.015) -> float:
    vol = annualized_volatility(returns)
    if vol == 0:
        return np.nan
    return (annualized_return(returns) - risk_free_rate) / vol


def drawdown(returns: pd.Series) -> pd.Series:
    wealth = (1 + returns).cumprod()
    return wealth / wealth.cummax() - 1


def performance_summary(returns: pd.Series, benchmark: pd.Series | None = None) -> pd.Series:
    """Summarize a strategy return stream."""

    summary = {
        "annualized_return": annualized_return(returns),
        "annualized_volatility": annualized_volatility(returns),
        "sharpe": sharpe_ratio(returns),
        "max_drawdown": drawdown(returns).min(),
        "hit_rate": (returns > 0).mean(),
    }
    if benchmark is not None:
        active = returns - benchmark
        tracking_error = active.std() * np.sqrt(TRADING_DAYS)
        active_return = annualized_return(returns) - annualized_return(benchmark)
        summary["active_return"] = active_return
        summary["tracking_error"] = tracking_error
        summary["information_ratio"] = active_return / tracking_error if tracking_error else np.nan
    return pd.Series(summary)


def equal_weight_return(returns: pd.DataFrame, tickers: list[str]) -> pd.Series:
    """Equal-weight return for a selected basket of tickers."""

    return returns.loc[:, tickers].mean(axis=1)


def zscore(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Cross-sectional z-score with direction control."""

    values = series.astype(float)
    score = (values - values.mean()) / values.std(ddof=0)
    return score if higher_is_better else -score


def inverse_volatility_weights(returns: pd.DataFrame) -> pd.Series:
    """Long-only inverse volatility weights."""

    inverse_vol = 1 / returns.std()
    return inverse_vol / inverse_vol.sum()
