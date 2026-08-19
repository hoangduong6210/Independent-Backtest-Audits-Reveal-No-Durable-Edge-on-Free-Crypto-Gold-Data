"""Statistical audit tools for aligned strategy-return matrices."""

from .statistics import cscv_pbo, deflated_sharpe_ratio, hansen_spa, run_all, white_reality_check

__all__ = ["cscv_pbo", "deflated_sharpe_ratio", "hansen_spa", "run_all", "white_reality_check"]
__version__ = "1.0.0"
