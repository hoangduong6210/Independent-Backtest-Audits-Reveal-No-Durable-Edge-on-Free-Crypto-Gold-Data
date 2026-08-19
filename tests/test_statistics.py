from pathlib import Path

import numpy as np

from backtest_audit.statistics import cscv_pbo, load_matrix, sharpe_per_bar


def test_released_matrix_contract():
    matrix = load_matrix()
    assert matrix.shape == (21949, 4)
    assert list(matrix.columns) == ["ml_rr", "ta_funding", "asym_barrier", "ml_barrier"]
    assert all(sharpe_per_bar(matrix[column].to_numpy()) < 0 for column in matrix.columns)


def test_cscv_returns_a_probability():
    rng = np.random.default_rng(42)
    matrix = rng.normal(size=(200, 4))
    result = cscv_pbo(matrix, S=10)
    assert result["n_splits"] == 252
    assert 0.0 <= result["pbo"] <= 1.0
