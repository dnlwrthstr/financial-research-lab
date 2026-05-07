"""Quantitative method helpers for the lab notebooks."""

from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def generate_return_sample(periods: int = 756, seed: int = 404) -> pd.DataFrame:
    """Generate a reproducible return sample with market and asset returns."""

    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2023-01-02", periods=periods)
    market = rng.normal(0.00035, 0.010, periods)
    asset = 0.00008 + 0.85 * market + rng.normal(0, 0.0065, periods)
    defensive = 0.00012 + 0.45 * market + rng.normal(0, 0.0045, periods)
    rates = rng.normal(0.00004, 0.00001, periods)
    return pd.DataFrame(
        {
            "market": market,
            "asset": asset,
            "defensive_asset": defensive,
            "risk_free": rates,
        },
        index=dates,
    )


def annualized_return(returns: pd.Series) -> float:
    """Compound daily returns into an annualized return."""

    compounded = (1 + returns).prod()
    years = len(returns) / TRADING_DAYS
    return float(compounded ** (1 / years) - 1)


def annualized_volatility(returns: pd.Series) -> float:
    """Annualize daily volatility."""

    return float(returns.std() * np.sqrt(TRADING_DAYS))


def drawdown(returns: pd.Series) -> pd.DataFrame:
    """Return wealth, running peak, and drawdown."""

    wealth = (1 + returns).cumprod()
    peak = wealth.cummax()
    return pd.DataFrame({"wealth": wealth, "peak": peak, "drawdown": wealth / peak - 1})


def ordinary_least_squares(y: np.ndarray, x: np.ndarray) -> dict[str, np.ndarray | float]:
    """Estimate OLS with an intercept using numpy only."""

    x = np.asarray(x)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    y = np.asarray(y)
    x_design = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(x_design, y, rcond=None)[0]
    fitted = x_design @ beta
    residuals = y - fitted
    sse = float(residuals @ residuals)
    sst = float(((y - y.mean()) @ (y - y.mean())))
    r_squared = 1 - sse / sst
    return {
        "coefficients": beta,
        "fitted": fitted,
        "residuals": residuals,
        "r_squared": float(r_squared),
    }


def simulate_gbm_paths(
    start_value: float = 100.0,
    annual_return: float = 0.07,
    annual_volatility_value: float = 0.16,
    years: float = 1.0,
    paths: int = 2_000,
    seed: int = 505,
) -> pd.DataFrame:
    """Simulate geometric Brownian motion price paths."""

    rng = np.random.default_rng(seed)
    steps = int(TRADING_DAYS * years)
    dt = 1 / TRADING_DAYS
    shocks = rng.normal(0, 1, size=(steps, paths))
    increments = (annual_return - 0.5 * annual_volatility_value**2) * dt
    increments += annual_volatility_value * np.sqrt(dt) * shocks
    log_paths = np.vstack([np.zeros(paths), np.cumsum(increments, axis=0)])
    values = start_value * np.exp(log_paths)
    return pd.DataFrame(values)
