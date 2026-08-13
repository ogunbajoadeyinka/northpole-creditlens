"""Historical source adapters for NorthPole CreditLens."""

from __future__ import annotations

import pandas as pd

UCI_DEFAULT_DATASET_ID = 350

# UCI dataset 350 exposes predictors as X1..X23. These mappings follow the
# official variable descriptions and keep the downstream code semantic.
UCI_X_TO_SOURCE = {
    "x1": "limit_bal",
    "x2": "sex",
    "x3": "education",
    "x4": "marriage",
    "x5": "age",
    "x6": "pay_0",
    "x7": "pay_2",
    "x8": "pay_3",
    "x9": "pay_4",
    "x10": "pay_5",
    "x11": "pay_6",
    "x12": "bill_amt1",
    "x13": "bill_amt2",
    "x14": "bill_amt3",
    "x15": "bill_amt4",
    "x16": "bill_amt5",
    "x17": "bill_amt6",
    "x18": "pay_amt1",
    "x19": "pay_amt2",
    "x20": "pay_amt3",
    "x21": "pay_amt4",
    "x22": "pay_amt5",
    "x23": "pay_amt6",
}


def fetch_uci_default_data() -> pd.DataFrame:
    """Fetch and normalize the UCI Default of Credit Card Clients dataset.

    The full raw dataset is intentionally not committed to Git. This adapter
    makes the historical baseline reproducible from its authoritative source.
    """
    try:
        from ucimlrepo import fetch_ucirepo
    except ImportError as exc:  # pragma: no cover - environment guard
        raise RuntimeError(
            "Install the data extra before fetching UCI data: pip install -e '.[data]'"
        ) from exc

    dataset = fetch_ucirepo(id=UCI_DEFAULT_DATASET_ID)
    features = dataset.data.features.copy()
    targets = dataset.data.targets.copy()

    features.columns = [_normalize_column_name(column) for column in features.columns]
    features = features.rename(columns=UCI_X_TO_SOURCE)

    expected_predictors = set(UCI_X_TO_SOURCE.values())
    missing_predictors = sorted(expected_predictors.difference(features.columns))
    if missing_predictors:
        raise ValueError(f"UCI predictor mapping incomplete; missing: {missing_predictors}")

    if targets.shape[1] != 1:
        raise ValueError(f"Expected one target column, found {targets.shape[1]}")

    target = targets.iloc[:, 0].rename("default_next_month")

    ids = getattr(dataset.data, "ids", None)
    if ids is not None and len(ids) == len(features):
        source_ids = ids.iloc[:, 0].reset_index(drop=True).rename("id")
    else:
        # Stable fallback if the client library does not expose the ID-role column.
        source_ids = pd.Series(range(1, len(features) + 1), name="id")

    frame = pd.concat(
        [
            source_ids,
            features.reset_index(drop=True),
            target.reset_index(drop=True),
        ],
        axis=1,
    )
    frame.columns = [_normalize_column_name(column) for column in frame.columns]
    return frame


def _normalize_column_name(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")
