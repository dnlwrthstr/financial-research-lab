# Introduction to the Financial Research Lab

The Financial Research Lab is a learning and research workspace for connecting finance theory with practical Python implementation. It is designed as a structured path from foundational concepts to valuation, market data, portfolio construction, quantitative methods, strategies, AI-assisted research, and case studies.

The goal is not only to collect formulas. Each notebook should build intuition, show the mathematics, implement the concept in Python, visualize the result, and connect it to real investment or risk-management workflows.

## What This Lab Is About

This lab covers three layers of financial research:

1. **Conceptual understanding**
   Finance concepts, accounting logic, valuation intuition, risk and return, instruments, and market structure.

2. **Applied modeling**
   Python notebooks for DCF valuation, relative valuation, market data analysis, curve construction, portfolio analytics, and strategy testing.

3. **System thinking**
   How data, models, risk systems, AI agents, and case studies fit together in a practical research process.

## Repository Structure

```text
financial-research-lab/
├── 00_foundations/
├── 01_valuation/
├── 02_market_data/
├── 03_portfolio_management/
├── 04_quantitative_methods/
├── 05_strategies/
├── 06_ai_agents/
├── 07_case_studies/
├── data/
├── scripts/
├── README.md
└── GUIDELINES.md
```

## Learning Path

### 00_foundations

Start here. These notebooks introduce the core language of finance:

- financial statements
- time value of money
- financial ratios
- capital structure
- WACC and discounting
- equity basics
- bond basics
- market data basics
- risk and return
- interest rates and yield curves

This section is the conceptual base for everything else in the lab.

### 01_valuation

This section turns fundamentals into valuation models. It includes:

- DCF modeling
- relative valuation
- WACC deep dives
- sensitivity analysis
- valuation case studies

The focus is on understanding what drives intrinsic value and how sensitive valuation is to assumptions.

### 02_market_data

This section introduces tradable market data and market-derived signals:

- OHLCV data
- technical indicators
- factor data
- alpha and beta from market data
- data pipelines

It connects raw market observations with analytics used in research and trading workflows.

### 03_portfolio_management

This section studies how individual assets combine into portfolios:

- return and risk
- portfolio theory
- optimization
- backtesting
- performance metrics

The goal is to move from single-security analysis to portfolio-level decision making.

### 04_quantitative_methods

This section provides the mathematical and statistical toolkit:

- probability
- statistics
- regression
- Monte Carlo simulation
- time series
- curve construction and bootstrapping
- option pricing and Greeks

These methods support valuation, risk, market data analysis, and strategy research.

### 05_strategies

This section explores investment strategy ideas:

- value investing
- momentum
- quality factor
- multi-factor investing
- risk parity

The emphasis is on turning financial concepts into testable investment logic.

### 06_ai_agents

This section explores AI-assisted financial research workflows:

- retrieval-augmented generation
- OpenSearch queries
- agent-assisted valuation
- dashboards

The goal is to understand how AI systems can support research, not replace financial judgment.

### 07_case_studies

This section applies the lab to concrete examples. Case studies combine fundamentals, valuation, market data, and investment reasoning into a more realistic research workflow.

## Notebook Structure

Most notebooks follow the same pattern:

1. **Intuition**
   What the concept means and why it matters.

2. **Mathematics**
   Key formulas with definitions of each variable.

3. **Implementation**
   Python code that calculates the concept.

4. **Visualization**
   Charts or tables that make the concept easier to interpret.

5. **Application**
   How the concept is used in valuation, risk, markets, or portfolio work.

6. **Reflection**
   Questions to test understanding.

## Suggested Use

For a first pass, read the lab in this order:

```text
00_foundations
01_valuation
02_market_data
03_portfolio_management
04_quantitative_methods
05_strategies
07_case_studies
```

The `06_ai_agents` section can be read once the basic research workflow is familiar.

## Working Style

This lab is meant to be iterative. A notebook may start with a simple example, then later gain better explanations, more realistic assumptions, cleaner visualizations, or additional edge cases.

Good additions should usually answer one of these questions:

- Does this make the financial intuition clearer?
- Does this improve the mathematical precision?
- Does this make the Python implementation more useful?
- Does this connect the concept to a real research, valuation, or risk workflow?

## Practical Notes

Use `README.md` for setup instructions and environment details.

Use `GUIDELINES.md` for notebook standards, project layout, and expected notebook style.

Before committing notebooks, clear outputs so diffs stay readable:

```bash
python scripts/clean_notebook_outputs.py
```
