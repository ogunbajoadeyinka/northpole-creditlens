"""Model comparison and probability-calibration utilities for CreditLens."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from creditlens.risk.baseline import TARGET, select_baseline_features


@dataclass(frozen=True)
class ComparisonMetrics:
    model_name: str
    roc_auc: float
    pr_auc: float
    brier_score: float


def _feature_preprocessor(features: list[str]) -> ColumnTransformer:
    categorical = [c for c in features if c.startswith("repayment_status_")]
    numeric = [c for c in features if c not in categorical]
    return ColumnTransformer(
        [
            ("num", SimpleImputer(strategy="median"), numeric),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )


def fit_random_forest_challenger(
    frame: pd.DataFrame,
    *,
    test_size: float = 0.25,
    random_state: int = 42,
) -> tuple[Pipeline, ComparisonMetrics, pd.DataFrame]:
    """Fit a nonlinear challenger and return BI-ready calibration bins."""
    features = select_baseline_features(frame)
    X = frame[features].copy()
    y = frame[TARGET].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    model = Pipeline(
        [
            ("preprocessor", _feature_preprocessor(features)),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    min_samples_leaf=10,
                    class_weight="balanced_subsample",
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    model.fit(X_train, y_train)
    probability = model.predict_proba(X_test)[:, 1]
    metrics = ComparisonMetrics(
        model_name="random_forest",
        roc_auc=float(roc_auc_score(y_test, probability)),
        pr_auc=float(average_precision_score(y_test, probability)),
        brier_score=float(brier_score_loss(y_test, probability)),
    )
    calibration = build_calibration_table(y_test.to_numpy(), probability)
    return model, metrics, calibration


def calibrate_classifier(
    fitted_model: Pipeline,
    X_calibration: pd.DataFrame,
    y_calibration: pd.Series,
    *,
    method: str = "sigmoid",
) -> CalibratedClassifierCV:
    """Calibrate an already-fitted classifier on a separate calibration set."""
    calibrated = CalibratedClassifierCV(fitted_model, method=method, cv="prefit")
    calibrated.fit(X_calibration, y_calibration)
    return calibrated


def build_calibration_table(
    y_true: np.ndarray,
    probability: np.ndarray,
    *,
    n_bins: int = 10,
) -> pd.DataFrame:
    observed, predicted = calibration_curve(
        y_true,
        probability,
        n_bins=n_bins,
        strategy="quantile",
    )
    return pd.DataFrame(
        {
            "mean_predicted_pd": predicted,
            "observed_default_rate": observed,
            "calibration_gap": observed - predicted,
        }
    )
