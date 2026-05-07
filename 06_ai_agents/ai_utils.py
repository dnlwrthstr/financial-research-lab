"""Offline AI-agent helpers for the financial research lab."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import NamedTuple

import numpy as np
import pandas as pd


TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9_]+")


class AgentState(NamedTuple):
    question: str
    retrieved_documents: pd.DataFrame
    valuation: pd.Series
    conclusion: str


def tokenize(text: str) -> list[str]:
    """Lowercase tokenizer for simple offline retrieval."""

    return TOKEN_PATTERN.findall(text.lower())


def sample_financial_documents() -> pd.DataFrame:
    """Create a small synthetic document corpus for RAG demonstrations."""

    records = [
        {
            "doc_id": "nestle_annual_2024",
            "ticker": "NESN.SW",
            "source": "annual_report",
            "section": "cash_flow",
            "date": "2024-12-31",
            "text": "Nestle generated resilient free cash flow supported by pricing power, disciplined capital expenditure, and stable working capital.",
        },
        {
            "doc_id": "nestle_annual_2024_margin",
            "ticker": "NESN.SW",
            "source": "annual_report",
            "section": "profitability",
            "date": "2024-12-31",
            "text": "Gross margin improved as input cost pressure eased. Operating margin remained supported by premium brands and productivity programs.",
        },
        {
            "doc_id": "nestle_risk_2024",
            "ticker": "NESN.SW",
            "source": "risk_factors",
            "section": "risk",
            "date": "2024-12-31",
            "text": "Key risks include commodity inflation, foreign exchange volatility, changing consumer preferences, and regulatory scrutiny.",
        },
        {
            "doc_id": "peer_note_2024",
            "ticker": "PEER.FOOD",
            "source": "analyst_note",
            "section": "valuation",
            "date": "2024-11-15",
            "text": "Consumer staples peers trade at premium multiples when revenue growth is defensive and cash conversion is predictable.",
        },
        {
            "doc_id": "market_data_2024",
            "ticker": "NESN.SW",
            "source": "market_data",
            "section": "price",
            "date": "2024-12-31",
            "text": "The share price declined modestly while volatility stayed below the broad equity market. Liquidity remained strong.",
        },
        {
            "doc_id": "valuation_model_base",
            "ticker": "NESN.SW",
            "source": "model",
            "section": "dcf",
            "date": "2025-01-10",
            "text": "The base DCF assumes 3.5 percent revenue growth, 13.5 percent free cash flow margin, 6.0 percent WACC, and 2.0 percent terminal growth.",
        },
    ]
    return pd.DataFrame(records)


def build_tfidf_index(documents: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Build a tiny TF-IDF matrix from a document frame with a text column."""

    tokenized = documents["text"].map(tokenize)
    vocabulary = sorted({token for tokens in tokenized for token in tokens})
    doc_count = len(documents)
    document_frequency = Counter(token for tokens in tokenized for token in set(tokens))
    idf = {term: math.log((1 + doc_count) / (1 + document_frequency[term])) + 1 for term in vocabulary}

    rows = []
    for tokens in tokenized:
        counts = Counter(tokens)
        total = sum(counts.values()) or 1
        rows.append([counts[term] / total * idf[term] for term in vocabulary])

    matrix = pd.DataFrame(rows, columns=vocabulary, index=documents.index)
    return matrix, vocabulary


def retrieve(documents: pd.DataFrame, query: str, top_k: int = 3, ticker: str | None = None) -> pd.DataFrame:
    """Retrieve relevant documents with cosine similarity."""

    candidates = documents.copy()
    if ticker is not None:
        candidates = candidates[candidates["ticker"] == ticker].copy()
    if candidates.empty:
        return candidates.assign(score=[])

    matrix, vocabulary = build_tfidf_index(candidates)
    query_counts = Counter(tokenize(query))
    query_vector = np.array([query_counts.get(term, 0) for term in vocabulary], dtype=float)
    if query_vector.sum() > 0:
        query_vector = query_vector / query_vector.sum()

    doc_values = matrix.to_numpy()
    denominator = np.linalg.norm(doc_values, axis=1) * np.linalg.norm(query_vector)
    scores = np.divide(doc_values @ query_vector, denominator, out=np.zeros(len(candidates)), where=denominator != 0)
    result = candidates.copy()
    result["score"] = scores
    return result.sort_values("score", ascending=False).head(top_k)


def opensearch_like_filter(documents: pd.DataFrame, ticker: str | None = None, source: str | None = None, section: str | None = None) -> pd.DataFrame:
    """Simple metadata filter that behaves like a basic search query filter."""

    result = documents.copy()
    if ticker:
        result = result[result["ticker"] == ticker]
    if source:
        result = result[result["source"] == source]
    if section:
        result = result[result["section"] == section]
    return result.reset_index(drop=True)


def simple_dcf_value(
    fcf0: float = 13_800,
    growth: float = 0.035,
    wacc: float = 0.060,
    terminal_growth: float = 0.020,
    years: int = 5,
    net_debt: float = 35_000,
    shares: float = 2_650,
) -> pd.Series:
    """Deterministic compact DCF for agent demonstrations."""

    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth.")
    forecast = np.array([fcf0 * (1 + growth) ** year for year in range(1, years + 1)])
    pv_fcf = sum(forecast[year - 1] / (1 + wacc) ** year for year in range(1, years + 1))
    terminal_value = forecast[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** years
    enterprise_value = pv_fcf + pv_terminal
    equity_value = enterprise_value - net_debt
    return pd.Series(
        {
            "pv_fcf": pv_fcf,
            "pv_terminal": pv_terminal,
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "value_per_share": equity_value / shares,
            "terminal_value_share": pv_terminal / enterprise_value,
        }
    )


def answer_valuation_question(question: str, current_price: float = 96.0) -> AgentState:
    """Run a deterministic retrieve-value-conclude workflow."""

    documents = sample_financial_documents()
    retrieved = retrieve(documents, question, top_k=4, ticker="NESN.SW")
    valuation = simple_dcf_value()
    upside = valuation["value_per_share"] / current_price - 1
    if upside > 0.15:
        conclusion = "The model indicates material upside, but the conclusion depends strongly on WACC and terminal growth."
    elif upside > -0.10:
        conclusion = "The model indicates the stock is roughly fairly valued within a normal uncertainty range."
    else:
        conclusion = "The model indicates downside risk versus the current price."
    return AgentState(question=question, retrieved_documents=retrieved, valuation=valuation, conclusion=conclusion)
