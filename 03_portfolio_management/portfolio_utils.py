"""Portfolio management helpers for the lab notebooks."""

from __future__ import annotations

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def generate_synthetic_returns(periods: int = 504, seed: int = 123) -> pd.DataFrame:
    """Generate reproducible daily returns for a small multi-asset universe."""

    rng = np.random.default_rng(seed)
    assets = ["Global Equity", "Swiss Equity", "Bonds", "Real Estate", "Commodities"]
    annual_returns = np.array([0.075, 0.065, 0.030, 0.055, 0.040])
    annual_volatility = np.array([0.160, 0.140, 0.055, 0.120, 0.180])
    correlation = np.array(
        [
            [1.00, 0.78, -0.15, 0.55, 0.25],
            [0.78, 1.00, -0.10, 0.50, 0.20],
            [-0.15, -0.10, 1.00, 0.05, -0.05],
            [0.55, 0.50, 0.05, 1.00, 0.18],
            [0.25, 0.20, -0.05, 0.18, 1.00],
        ]
    )

    daily_mean = annual_returns / TRADING_DAYS
    daily_vol = annual_volatility / np.sqrt(TRADING_DAYS)
    daily_cov = np.outer(daily_vol, daily_vol) * correlation
    values = rng.multivariate_normal(daily_mean, daily_cov, periods)
    dates = pd.bdate_range("2024-01-02", periods=periods)
    return pd.DataFrame(values, index=dates, columns=assets)


def returns_to_prices(returns: pd.DataFrame, start_value: float = 100.0) -> pd.DataFrame:
    """Convert simple returns into an indexed price series."""

    return start_value * (1 + returns).cumprod()


def annualized_return(returns: pd.Series | pd.DataFrame) -> pd.Series | float:
    """Compound daily returns into annualized return."""

    compounded = (1 + returns).prod()
    years = len(returns) / TRADING_DAYS
    return compounded ** (1 / years) - 1


def annualized_volatility(returns: pd.Series | pd.DataFrame) -> pd.Series | float:
    """Annualize daily return volatility."""

    return returns.std() * np.sqrt(TRADING_DAYS)


def portfolio_return(weights: np.ndarray, expected_returns: pd.Series) -> float:
    """Expected annual portfolio return."""

    return float(np.dot(weights, expected_returns))


def portfolio_volatility(weights: np.ndarray, covariance: pd.DataFrame) -> float:
    """Expected annual portfolio volatility."""

    return float(np.sqrt(weights.T @ covariance.to_numpy() @ weights))


def portfolio_series(returns: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    """Daily portfolio return series from asset returns and weights."""

    return returns @ weights


def sharpe_ratio(portfolio_return_value: float, portfolio_volatility_value: float, risk_free_rate: float = 0.0) -> float:
    """Annualized Sharpe ratio."""

    if portfolio_volatility_value == 0:
        return np.nan
    return (portfolio_return_value - risk_free_rate) / portfolio_volatility_value


def random_weights(n_assets: int, n_portfolios: int = 5_000, seed: int = 123) -> np.ndarray:
    """Generate random long-only weights that sum to one."""

    rng = np.random.default_rng(seed)
    raw = rng.random((n_portfolios, n_assets))
    return raw / raw.sum(axis=1, keepdims=True)


def drawdown(returns: pd.Series) -> pd.DataFrame:
    """Calculate cumulative value, running peak, and drawdown."""

    wealth = (1 + returns).cumprod()
    peak = wealth.cummax()
    return pd.DataFrame({"wealth": wealth, "peak": peak, "drawdown": wealth / peak - 1})
