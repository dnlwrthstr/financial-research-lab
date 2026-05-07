# Financial Research Lab

This lab is a collection of notebooks that cover the following topics:
1. Conceptual understanding (finance + math)
2. Applied modeling (notebooks, data, valuation)
3. System thinking (portfolio + ontology/agents)

## 1. Project Structure (Repository Layout)

financial-research-lab/
│
├── README.md
├── GUIDELINES.md                # your notebook standards
│
├── 00_foundations/
│   ├── 01_financial_statements.ipynb
│   ├── 02_time_value_of_money.ipynb
│   ├── 03_discounting_and_wacc.ipynb
│   └── 04_market_basics.ipynb
│
├── 01_valuation/
│   ├── 01_dcf_model.ipynb
│   ├── 02_relative_valuation.ipynb
│   ├── 03_wacc_deep_dive.ipynb
│   ├── 04_sensitivity_analysis.ipynb
│   └── case_studies/
│       ├── nestle_dcf.ipynb
│       └── peer_comparison.ipynb
│
├── 02_market_data/
│   ├── 01_ohlcv_basics.ipynb
│   ├── 02_technical_indicators.ipynb
│   ├── 03_factor_data.ipynb
│   └── data_pipeline/
│       ├── fetch_data.py
│       └── opensearch_integration.ipynb
│
├── 03_portfolio_management/
│   ├── 01_return_and_risk.ipynb
│   ├── 02_portfolio_theory.ipynb
│   ├── 03_optimization.ipynb
│   ├── 04_backtesting.ipynb
│   └── 05_performance_metrics.ipynb
│
├── 04_quantitative_methods/
│   ├── 01_probability.ipynb
│   ├── 02_statistics.ipynb
│   ├── 03_regression.ipynb
│   ├── 04_monte_carlo.ipynb
│   └── 05_time_series.ipynb
│
├── 05_strategies/
│   ├── 01_value_investing.ipynb
│   ├── 02_momentum.ipynb
│   ├── 03_quality_factor.ipynb
│   ├── 04_multi_factor.ipynb
│   └── 05_risk_parity.ipynb
│
├── 06_ai_agents/
│   ├── 01_financial_rag.ipynb
│   ├── 02_opensearch_queries.ipynb
│   ├── 03_agent_valuation.ipynb
│   └── 04_dashboard.ipynb
│
├── 07_case_studies/
│   ├── nestle/
│   │   ├── fundamentals.ipynb
│   │   ├── valuation.ipynb
│   │   └── investment_thesis.md
│   └── portfolio_build/
│       └── sample_portfolio.ipynb
│
└── data/
    ├── raw/
    ├── processed/
    └── external/

## 2. Learning Phases (Roadmap)

### Phase 1 — Foundations (Week 1–2)
> Goal: Understand how money grows and how companies work

### Notebooks:
- Financial statements (Income, Balance, Cash Flow)
- Time value of money
- Discounting and WACC

👉 Output:
- You can read a company
- You understand DCF inputs

### Phase 2 — Valuation (Week 3–4)
> Goal: Understand how markets price companies

### Notebooks:
- DCF modeling
- Relative valuation (P/E, EV/EBITDA)
- Sensitivity analysis

👉 Output:
- Build a **Nestlé DCF from scratch**
- Understand why valuation differs

### Phase 3 — Market Data (Week 5)
> Goal: Understand price formation

#### Topics:
- OHLCV
- Indicators (RSI, MACD, MA)
- Data ingestion (yfinance → OpenSearch/DuckDB)

👉 Output:
- You can pull and structure market data

### Phase 4 — Portfolio Theory (Week 6–7)
> Goal: Move from **single asset → portfolio**

#### Topics:
- Returns & volatility
- Efficient frontier
- Sharpe ratio
- Performance metrics
- Backtesting


👉 Output:
- Build a portfolio optimizer

### Phase 5 — Quant Methods (Week 8–9)
> Goal: Add statistical rigor

#### Topics:
- Probability
- Hypothesis testing
- Regression
- Monte Carlo simulation

👉 Output:
- Run **simulations** and **backtests**

### Phase 6 — Strategies (Week 10–11)
> Goal: Build investment strategies

#### Topics:
- Value investing
- Momentum
- Multi-factor models

👉 Output:
- Implement **systematic strategies**

### Phase 7 — AI + Your Stack (Week 12+)
> Goal: Integrate with the data store + ontology + agents

#### Topics:
- Financial RAG
- Agent-driven valuation
- Dashboarding

👉 Output:
- AI system answering: *“Is this stock undervalued?”*

## 3. Notebook Design Standard (VERY IMPORTANT)
Each notebook must follow this structure:

# Title

## 1. Intuition
Explain concept in plain English

## 2. Mathematics
Formal equations (LaTeX)

## 3. Implementation
Python code (pandas, numpy)

## 4. Visualization
Charts (matplotlib / plotly)

## 5. Application
Real-world example (Nestlé, etc.)

## 6. Reflection
- What did I learn?
- What assumptions matter?
- What can go wrong?

### Mathematics and notation standard

- The Mathematics section must show the core equations in LaTeX.
- Every equation block must be followed by a short `Where:` explanation of the variables and symbols used in the equation.
- Do not assume finance abbreviations or mathematical symbols are obvious to a learner. Explain abbreviations the first time they appear.
- Keep notation consistent across notebooks. For example, use `r` for a discount rate or return, `t` for a time period, `CF_t` for cash flow in period `t`, and `WACC` for weighted average cost of capital.

### Table and number formatting standard

- Learner-facing tables must use readable finance formatting, not raw scientific notation.
- Avoid values like `2.343435e-02` in displayed tables. Format this as `2.34%`, `0.0234`, or `0.02` depending on the concept being taught.
- Use percentages for returns, discount rates, margins, spreads, volatility, and yields.
- Use currency or thousands/millions labels for monetary values.
- Round displayed values enough for interpretation, while keeping full precision in the underlying calculation when needed.
- Scientific notation is acceptable only for internal numerical checks or debugging output, not for teaching tables.

## 4. Example: DCF Notebook Structure

# Discounted Cash Flow (DCF)

## Intuition
Future cash is worth less than today

## Formula
DCF equation

## Build Model
- Revenue growth
- Margins
- WACC

## Code
Compute valuation

## Sensitivity
Heatmap (WACC vs growth)

## Case Study
Nestlé valuation

## Reflection
DCF is assumption-driven

## 6. Key Principle
It is not just learning finance.

> It's about building:
> - Financial Intelligence System

Where:
Data → OpenSearch/DuckDB
Knowledge → Ontology
Logic → Notebooks
Reasoning → Agents

## 7. What You Will Achieve

- You can value companies professionally
- You can build portfolios
- You can design AI financial agents
- You understand markets structurally
