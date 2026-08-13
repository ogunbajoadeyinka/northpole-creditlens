import pandas as pd
import pytest

from creditlens.analytics.historical import (
    add_business_segments,
    portfolio_summary,
    segment_default_rate,
)


def _frame():
    return pd.DataFrame(
        {
            "default_next_month": [0, 1, 0, 1],
            "credit_limit": [40_000, 80_000, 150_000, 350_000],
            "age": [23, 31, 42, 59],
            "bill_amount_m1": [10_000, 20_000, 0, 50_000],
            "payment_amount_m1": [2_000, 1_000, 500, 5_000],
        }
    )


def test_portfolio_summary():
    summary = portfolio_summary(_frame())
    assert summary.observations == 4
    assert summary.default_rate == pytest.approx(0.5)
    assert summary.avg_credit_limit == pytest.approx(155_000.0)
    assert summary.median_credit_limit == pytest.approx(115_000.0)


def test_business_segments_and_default_rates():
    segmented = add_business_segments(_frame())
    assert list(segmented["credit_limit_band"].astype(str)) == [
        "<50K",
        "50K-99K",
        "100K-199K",
        "300K+",
    ]
    assert pd.isna(segmented.loc[2, "latest_payment_to_bill_ratio"])

    rates = segment_default_rate(segmented, "age_band")
    assert set(rates.columns) == {"age_band", "observations", "defaults", "default_rate"}
