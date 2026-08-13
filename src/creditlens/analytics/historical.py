"""Reusable descriptive and diagnostic analytics for historical credit data."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PortfolioSummary:
    observations: int
    default_rate: float
    avg_credit_limit: float
    median_credit_limit: float
    avg_age: float
    avg_latest_bill: float
    avg_latest_payment: float


def portfolio_summary(frame: pd.DataFrame) -> PortfolioSummary:
    """Compute executive-level historical portfolio metrics."""
    required = {
        "default_next_month",
        "credit_limit",
        "age",
        "bill_amount_m1",
        "payment_amount_m1",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Missing required analytics columns: {missing}")

    return PortfolioSummary(
        observations=len(frame),
        default_rate=float(frame["default_next_month"].mean()),
        avg_credit_limit=float(frame["credit_limit"].mean()),
        median_credit_limit=float(frame["credit_limit"].median()),
        avg_age=float(frame["age"].mean()),
        avg_latest_bill=float(frame["bill_amount_m1"].mean()),
        avg_latest_payment=float(frame["payment_amount_m1"].mean()),
    )


def add_business_segments(frame: pd.DataFrame) -> pd.DataFrame:
    """Add transparent descriptive segments used by analytics and BI."""
    result = frame.copy()
    result["credit_limit_band"] = pd.cut(
        result["credit_limit"],
        bins=[-np.inf, 50_000, 100_000, 200_000, 300_000, np.inf],
        labels=["<50K", "50K-99K", "100K-199K", "200K-299K", "300K+"],
        right=False,
    )
    result["age_band"] = pd.cut(
        result["age"],
        bins=[-np.inf, 25, 35, 45, 55, np.inf],
        labels=["<25", "25-34", "35-44", "45-54", "55+"],
        right=False,
    )
    result["latest_payment_to_bill_ratio"] = np.where(
        result["bill_amount_m1"] > 0,
        result["payment_amount_m1"] / result["bill_amount_m1"],
        np.nan,
    )
    return result


def segment_default_rate(frame: pd.DataFrame, segment: str) -> pd.DataFrame:
    """Return observation counts and default rates by a descriptive segment."""
    if segment not in frame.columns:
        raise ValueError(f"Unknown segment column: {segment}")
    if "default_next_month" not in frame.columns:
        raise ValueError("default_next_month is required")

    grouped = (
        frame.groupby(segment, observed=False)["default_next_month"]
        .agg(observations="size", defaults="sum", default_rate="mean")
        .reset_index()
    )
    return grouped.sort_values("default_rate", ascending=False).reset_index(drop=True)
