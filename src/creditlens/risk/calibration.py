"""Aggregate probability-calibration monitoring for historical PD research."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss


def calibration_summary(y_true, probability, bins: int = 10) -> pd.DataFrame:
    """Summarize predicted versus observed default rates by probability bucket.

    This supports model evaluation and aggregate monitoring. It does not make
    individual lending eligibility decisions.
    """
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(probability, dtype=float)
    if actual.shape != predicted.shape:
        raise ValueError("y_true and probability must have the same shape")
    if np.any((predicted < 0) | (predicted > 1)):
        raise ValueError("probability must be between 0 and 1")

    frame = pd.DataFrame({"actual": actual, "predicted_pd": predicted})
    frame["bucket"] = pd.qcut(frame["predicted_pd"], q=bins, duplicates="drop")
    result = (
        frame.groupby("bucket", observed=True)
        .agg(
            observations=("actual", "size"),
            average_predicted_pd=("predicted_pd", "mean"),
            observed_default_rate=("actual", "mean"),
        )
        .reset_index()
    )
    result["calibration_gap"] = (
        result["average_predicted_pd"] - result["observed_default_rate"]
    )
    result["bucket"] = result["bucket"].astype(str)
    return result


def brier_score(y_true, probability) -> float:
    """Return Brier score for probabilistic model evaluation."""
    return float(brier_score_loss(y_true, probability))
