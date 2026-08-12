import pandas as pd
import pytest

from src.creditlens.data.validation import validate_historical_frame


def test_quality_report():
    frame = pd.DataFrame(
        {
            "limit_bal": [10_000, 20_000, 20_000],
            "default_next_month": [0, 1, 1],
        }
    )
    report = validate_historical_frame(frame)
    assert report.row_count == 3
    assert report.column_count == 2
    assert report.target_default_rate == pytest.approx(2 / 3)


def test_missing_target_rejected():
    with pytest.raises(ValueError, match="Required target"):
        validate_historical_frame(pd.DataFrame({"limit_bal": [10_000]}))


def test_nonbinary_target_rejected():
    frame = pd.DataFrame({"default_next_month": [0, 2]})
    with pytest.raises(ValueError, match="binary"):
        validate_historical_frame(frame)
