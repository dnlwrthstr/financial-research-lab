"""Compatibility imports for market-data helpers.

This lets examples use:

    from fetch_data import add_return_columns, generate_synthetic_ohlcv

from the repository root, while the implementation remains in
``02_market_data/data_pipeline/fetch_data.py``.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


_HELPER_PATH = Path(__file__).resolve().parent / "02_market_data" / "data_pipeline" / "fetch_data.py"
_SPEC = importlib.util.spec_from_file_location("_market_data_fetch_data", _HELPER_PATH)

if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Could not load market-data helper module from {_HELPER_PATH}")

_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

OHLCV_COLUMNS = _MODULE.OHLCV_COLUMNS
add_return_columns = _MODULE.add_return_columns
generate_synthetic_ohlcv = _MODULE.generate_synthetic_ohlcv
load_ohlcv = _MODULE.load_ohlcv
normalize_ohlcv = _MODULE.normalize_ohlcv
save_ohlcv = _MODULE.save_ohlcv

__all__ = [
    "OHLCV_COLUMNS",
    "add_return_columns",
    "generate_synthetic_ohlcv",
    "load_ohlcv",
    "normalize_ohlcv",
    "save_ohlcv",
]
