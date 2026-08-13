"""Leakage-aware baseline PD modeling for NorthPole CreditLens."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET = "default_next_month"
GOVERNED_FIELDS = {"sex_code", "education_code", "marriage_code"}
NON_FEATURES = {"source_record_id", TARGET}


@dataclass(frozen=True)
class BaselineMetrics:
    roc_auc: float
    pr_auc: float
    brier_score: float
    precision_at_threshold: float
    recall_at_threshold: float
    threshold: float


@dataclass(frozen=True)
class BaselineResult:
    model: Pipeline
    metrics: BaselineMetrics
    train_rows: int
    test_rows: int
    feature_columns: tuple[str, ...]


def select_baseline_features(frame: pd.DataFrame, include_governed: bool = False) -> list[str]:
    excluded = set(NON_FEATURES)
    if not include_governed:
        excluded |= GOVERNED_FIELDS
    return [column for column in frame.columns if column not in excluded]


def fit_logistic_pd_baseline(
    frame: pd.DataFrame,
    *,
    test_size: float = 0.25,
    random_state: int = 42,
    operating_threshold: float = 0.20,
    include_governed: bool = False,
) -> BaselineResult:
    """Train and evaluate an interpretable logistic-regression PD baseline."""
    if TARGET not in frame.columns:
        raise ValueError(f"Missing target column: {TARGET}")

    features = select_baseline_features(frame, include_governed=include_governed)
    if not features:
        raise ValueError("No feature columns available for modeling")

    X = frame[features].copy()
    y = frame[TARGET].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    categorical = [c for c in features if c.startswith("repayment_status_")]
    numeric = [c for c in features if c not in categorical]

    numeric_pipe = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        [("num", numeric_pipe, numeric), ("cat", categorical_pipe, categorical)]
    )
    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]
    )
    model.fit(X_train, y_train)

    probability = model.predict_proba(X_test)[:, 1]
    predicted = (probability >= operating_threshold).astype(int)
    truth = y_test.to_numpy()
    tp = int(((predicted == 1) & (truth == 1)).sum())
    fp = int(((predicted == 1) & (truth == 0)).sum())
    fn = int(((predicted == 0) & (truth == 1)).sum())

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    metrics = BaselineMetrics(
        roc_auc=float(roc_auc_score(y_test, probability)),
        pr_auc=float(average_precision_score(y_test, probability)),
        brier_score=float(brier_score_loss(y_test, probability)),
        precision_at_threshold=float(precision),
        recall_at_threshold=float(recall),
        threshold=float(operating_threshold),
    )
    return BaselineResult(
        model=model,
        metrics=metrics,
        train_rows=len(X_train),
        test_rows=len(X_test),
        feature_columns=tuple(features),
    )
