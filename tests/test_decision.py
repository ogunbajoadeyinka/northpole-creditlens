import pytest

from src.creditlens.decision import CreditEconomics, Decision, recommend_decision


def test_expected_loss_and_profit():
    economics = CreditEconomics(
        probability_of_default=0.10,
        loss_given_default=0.45,
        exposure_at_default=20_000,
        expected_revenue=3_000,
        operating_cost=250,
    )
    assert economics.expected_loss == pytest.approx(900.0)
    assert economics.risk_adjusted_expected_profit == pytest.approx(1_850.0)


@pytest.mark.parametrize(
    ("pd", "expected"),
    [
        (0.05, Decision.APPROVE),
        (0.12, Decision.APPROVE),
        (0.15, Decision.MANUAL_REVIEW),
        (0.20, Decision.MANUAL_REVIEW),
        (0.30, Decision.DECLINE),
    ],
)
def test_recommend_decision(pd, expected):
    assert recommend_decision(pd) == expected


def test_invalid_probability_rejected():
    with pytest.raises(ValueError):
        recommend_decision(1.1)
