import pandas as pd
import pytest

from creditlens.data.transform import CANONICAL_COLUMNS, to_canonical_historical_frame


def _source_row():
    return {
        "id": 1,
        "limit_bal": 20000,
        "sex": 2,
        "education": 2,
        "marriage": 1,
        "age": 24,
        "pay_0": 2,
        "pay_2": 2,
        "pay_3": -1,
        "pay_4": -1,
        "pay_5": -2,
        "pay_6": -2,
        "bill_amt1": 3913,
        "bill_amt2": 3102,
        "bill_amt3": 689,
        "bill_amt4": 0,
        "bill_amt5": 0,
        "bill_amt6": 0,
        "pay_amt1": 0,
        "pay_amt2": 689,
        "pay_amt3": 0,
        "pay_amt4": 0,
        "pay_amt5": 0,
        "pay_amt6": 0,
        "default_next_month": 1,
    }


def test_transform_produces_canonical_schema():
    result = to_canonical_historical_frame(pd.DataFrame([_source_row()]))
    assert list(result.columns) == CANONICAL_COLUMNS
    assert result.loc[0, "source_record_id"] == 1
    assert result.loc[0, "credit_limit"] == pytest.approx(20000.0)
    assert result.loc[0, "default_next_month"] == 1


def test_transform_rejects_missing_required_column():
    row = _source_row()
    row.pop("age")
    with pytest.raises(ValueError, match="Missing required UCI columns"):
        to_canonical_historical_frame(pd.DataFrame([row]))
