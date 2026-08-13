import pandas as pd

from src.creditlens.risk.baseline import fit_logistic_pd_baseline, select_baseline_features


def sample_frame(rows: int = 40) -> pd.DataFrame:
    data = []
    for i in range(rows):
        data.append(
            {
                "source_record_id": i + 1,
                "credit_limit": 50_000 + (i * 2_500),
                "sex_code": 1 if i % 2 == 0 else 2,
                "education_code": 1 + (i % 3),
                "marriage_code": 1 + (i % 2),
                "age": 24 + (i % 30),
                "repayment_status_m0": i % 4,
                "repayment_status_m2": i % 3,
                "bill_amount_m1": 10_000 + i * 500,
                "payment_amount_m1": 500 + i * 25,
                "default_next_month": 1 if i % 4 == 0 else 0,
            }
        )
    return pd.DataFrame(data)


def test_governed_fields_excluded_by_default():
    features = select_baseline_features(sample_frame())
    assert "source_record_id" not in features
    assert "default_next_month" not in features
    assert "sex_code" not in features
    assert "education_code" not in features
    assert "marriage_code" not in features


def test_baseline_returns_probability_metrics():
    result = fit_logistic_pd_baseline(sample_frame(), test_size=0.25)
    assert result.train_rows == 30
    assert result.test_rows == 10
    assert 0 <= result.metrics.roc_auc <= 1
    assert 0 <= result.metrics.pr_auc <= 1
    assert result.metrics.brier_score >= 0
