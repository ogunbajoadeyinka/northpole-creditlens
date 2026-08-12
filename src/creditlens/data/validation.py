"""Data-quality gates for the historical CreditLens baseline."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DataQualityReport:
    row_count: int
    column_count: int
    duplicate_rows: int
    missing_cells: int
    target_default_rate: float


def validate_historical_frame(frame: pd.DataFrame) -> DataQualityReport:
    target = "default_next_month"
    if frame.empty:
        raise ValueError("Historical dataset is empty")
    if target not in frame.columns:
        raise ValueError(f"Required target column '{target}' is missing")

    target_values = set(frame[target].dropna().astype(int).unique())
    if not target_values.issubset({0, 1}):
        raise ValueError(f"Target must be binary; observed values: {sorted(target_values)}")
    if frame[target].isna().any():
        raise ValueError("Target contains missing values")

    return DataQualityReport(
        row_count=len(frame),
        column_count=len(frame.columns),
        duplicate_rows=int(frame.duplicated().sum()),
        missing_cells=int(frame.isna().sum().sum()),
        target_default_rate=float(frame[target].mean()),
    )
