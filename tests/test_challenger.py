import numpy as np
import pandas as pd

from src.creditlens.risk.comparison import build_calibration_table, fit_random_forest_challenger


def sample_frame(rows: int = 80) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "source_record_id": range(1, rows + 1),
            "credit_limit": [50_000 + i * 1_000 for i in range(rows)],
            "age": [24 + (i % 35) for i in range(rows)],
            "repayment_status_m0": [i % 4 for i in range(rows)],
            "repayment_status_m2": [i % 3 for i in range(rows)],
            "bill_amount_m1": [8_000 + i * 250 for i in range(rows)],
            "payment_amount_m1": [400 + i * 15 for i in range(rows)],
            "sex_code": [1 + (i % 2) for i in range(rows)],
            "education_code": [1 + (i % 3) for i in range(rows)],
            "marriage_code": [1 + (i % 2) for i in range(rows)],
            "default_next_month": [1 if i % 4 == 0 else 0 for i in range(rows)],
        }
    )


def test_calibration_table_has_expected_columns():
    table = build_calibration_table(
        np.array([0, 0, 1, 1]),
        np.array([0.1, 0.2, 0.7, 0.9]),
        n_bins=2,
    )
    assert list(table.columns) == [
        "mean_predicted_pd",
        "observed_default_rate",
        "calibration_gap",
    ]
    assert len(table) == 2


def test_random_forest_challenger_returns_metrics():
    _, metrics, calibration = fit_random_forest_challenger(sample_frame(), test_size=0.25)
    assert metrics.model_name == "random_forest"
    assert 0 <= metrics.roc_auc <= 1
    assert 0 <= metrics.pr_auc <= 1
    assert metrics.brier_score >= 0
    assert not calibration.empty
