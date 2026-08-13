"""Train the NorthPole CreditLens historical logistic-regression PD baseline."""

from __future__ import annotations

import json

from creditlens.data.source import fetch_uci_default_data
from creditlens.data.transform import to_canonical_historical_frame
from creditlens.data.validation import validate_historical_frame
from creditlens.risk.baseline import fit_logistic_pd_baseline


def main() -> None:
    raw = fetch_uci_default_data()
    quality = validate_historical_frame(raw)
    frame = to_canonical_historical_frame(raw)
    result = fit_logistic_pd_baseline(frame)

    payload = {
        "data_quality": {
            "rows": quality.row_count,
            "columns": quality.column_count,
            "duplicate_rows": quality.duplicate_rows,
            "missing_cells": quality.missing_cells,
            "default_rate": quality.target_default_rate,
        },
        "split": {"train_rows": result.train_rows, "test_rows": result.test_rows},
        "features": list(result.feature_columns),
        "metrics": {
            "roc_auc": result.metrics.roc_auc,
            "pr_auc": result.metrics.pr_auc,
            "brier_score": result.metrics.brier_score,
            "precision_at_threshold": result.metrics.precision_at_threshold,
            "recall_at_threshold": result.metrics.recall_at_threshold,
            "threshold": result.metrics.threshold,
        },
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
