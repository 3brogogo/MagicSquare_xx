"""Shared pytest fixtures — FR-LOC-01 / G1 (logic only, no domain)."""

import pytest

# G1: valid partial 4×4, exactly two zeros at 1-index (2,2) and (3,3), row-major order.
_GRID_G1 = [
    [16, 3, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


@pytest.fixture
def grid_g1():
    """G1 격자 — 0이 2개, row-major 빈칸 순서 (2,2) → (3,3) 1-index."""
    return [row[:] for row in _GRID_G1]
