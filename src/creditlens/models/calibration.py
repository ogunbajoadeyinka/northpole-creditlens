"""Probability calibration utilities for CreditLens PD models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss


@dataclass(frozen=True)
class CalibrationResult:
    method: str
    brier_before: float
    brier_after: float
    calibrated_model: object


def calibrate_classifier(model, x_train, y_train, x_valid, y_valid, method: str = "isotonic") -> CalibrationResult:
    """Fit a post-hoc probability calibrator and compare Brier score.

    Calibration is performed on a model already fit on training data. The
    validation split is used to fit the calibration map; a later untouched
    test set should be reserved for final reporting.
    """
    raw_pd = model.predict_proba(x_valid)[:, 1]
    calibrator = CalibratedClassifierCV(model, method=method, cv="prefit")
    calibrator.fit(x_valid, y_valid)
    calibrated_pd = calibrator.predict_proba(x_valid)[:, 1]
    return CalibrationResult(
        method=method,
        brier_before=float(brier_score_loss(y_valid, raw_pd)),
        brier_after=float(brier_score_loss(y_valid, calibrated_pd)),
        calibrated_model=calibrator,
    )


def calibration_table(y_true, probability, bins: int = 10) -> pd.DataFrame:
    """Return reliability bins for BI/model-monitoring consumption."""
    frame = pd.DataFrame({"actual": np.asarray(y_true), "pd": np.asarray(probability)})
    frame["bucket"] = pd.qcut(frame["pd"], q=bins, duplicates="drop")
    result = (
        frame.groupby("bucket", observed=True)
        .agg(observations=("actual", "size"), predicted_pd=("pd", "mean"), observed_default_rate=("actual", "mean"))
        .reset_index()
    )
    result["calibration_gap"] = result["predicted_pd"] - result["observed_default_rate"]
    result["bucket"] = result["bucket"].astype(str)
    return result
