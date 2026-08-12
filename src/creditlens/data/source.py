"""Historical source adapters for NorthPole CreditLens."""

from __future__ import annotations

import pandas as pd

UCI_DEFAULT_DATASET_ID = 350


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

    if targets.shape[1] != 1:
        raise ValueError(f"Expected one target column, found {targets.shape[1]}")

    target = targets.iloc[:, 0].rename("default_next_month")
    frame = pd.concat([features, target], axis=1)
    frame.columns = [_normalize_column_name(column) for column in frame.columns]
    return frame


def _normalize_column_name(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")
