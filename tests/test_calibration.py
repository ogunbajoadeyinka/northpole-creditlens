import numpy as np

from src.creditlens.models.calibration import calibration_table


def test_calibration_table_has_reliability_fields():
    y_true = np.array([0, 0, 1, 0, 1, 1, 0, 1, 0, 1])
    pd_values = np.array([0.02, 0.08, 0.15, 0.20, 0.35, 0.55, 0.65, 0.72, 0.85, 0.95])
    result = calibration_table(y_true, pd_values, bins=5)
    expected = {"bucket", "observations", "predicted_pd", "observed_default_rate", "calibration_gap"}
    assert expected.issubset(result.columns)
    assert result["observations"].sum() == len(y_true)
