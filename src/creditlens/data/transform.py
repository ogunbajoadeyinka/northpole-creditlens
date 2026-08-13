"""Transform UCI credit data into CreditLens canonical columns."""

from __future__ import annotations

import pandas as pd

SOURCE_TO_CANONICAL = {
    "id": "source_record_id",
    "limit_bal": "credit_limit",
    "sex": "sex_code",
    "education": "education_code",
    "marriage": "marriage_code",
    "age": "age",
    "pay_0": "repayment_status_m0",
    "pay_2": "repayment_status_m2",
    "pay_3": "repayment_status_m3",
    "pay_4": "repayment_status_m4",
    "pay_5": "repayment_status_m5",
    "pay_6": "repayment_status_m6",
    "bill_amt1": "bill_amount_m1",
    "bill_amt2": "bill_amount_m2",
    "bill_amt3": "bill_amount_m3",
    "bill_amt4": "bill_amount_m4",
    "bill_amt5": "bill_amount_m5",
    "bill_amt6": "bill_amount_m6",
    "pay_amt1": "payment_amount_m1",
    "pay_amt2": "payment_amount_m2",
    "pay_amt3": "payment_amount_m3",
    "pay_amt4": "payment_amount_m4",
    "pay_amt5": "payment_amount_m5",
    "pay_amt6": "payment_amount_m6",
    "default_next_month": "default_next_month",
}

CANONICAL_COLUMNS = list(SOURCE_TO_CANONICAL.values())


def to_canonical_historical_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a stable, database-ready historical frame.

    The transformation is intentionally conservative: source semantics are
    preserved and only column names/types are standardized for analytics.
    """
    missing = sorted(set(SOURCE_TO_CANONICAL).difference(frame.columns))
    if missing:
        raise ValueError(f"Missing required UCI columns: {missing}")

    canonical = frame.rename(columns=SOURCE_TO_CANONICAL)[CANONICAL_COLUMNS].copy()

    integer_columns = [
        "source_record_id",
        "sex_code",
        "education_code",
        "marriage_code",
        "age",
        "repayment_status_m0",
        "repayment_status_m2",
        "repayment_status_m3",
        "repayment_status_m4",
        "repayment_status_m5",
        "repayment_status_m6",
        "default_next_month",
    ]
    numeric_columns = [
        "credit_limit",
        "bill_amount_m1",
        "bill_amount_m2",
        "bill_amount_m3",
        "bill_amount_m4",
        "bill_amount_m5",
        "bill_amount_m6",
        "payment_amount_m1",
        "payment_amount_m2",
        "payment_amount_m3",
        "payment_amount_m4",
        "payment_amount_m5",
        "payment_amount_m6",
    ]

    for column in integer_columns:
        canonical[column] = pd.to_numeric(canonical[column], errors="raise").astype("int64")
    for column in numeric_columns:
        canonical[column] = pd.to_numeric(canonical[column], errors="raise").astype("float64")

    return canonical
