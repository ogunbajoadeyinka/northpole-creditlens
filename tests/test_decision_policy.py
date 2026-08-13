import numpy as np
import pytest

from src.creditlens.decision_policy import PolicyAssumptions, evaluate_threshold, optimize_threshold


def test_evaluate_threshold_computes_expected_economics():
    pd_values = np.array([0.05, 0.10, 0.30])
    exposure = np.array([10_000.0, 20_000.0, 30_000.0])
    assumptions = PolicyAssumptions(loss_given_default=0.5, annual_interest_rate=0.2, operating_cost_rate=0.01)
    outcome = evaluate_threshold(pd_values, exposure, 0.10, assumptions)
    assert outcome.approved == 2
    assert outcome.approval_rate == pytest.approx(2 / 3)
    assert outcome.exposure == pytest.approx(30_000.0)
    assert outcome.expected_loss == pytest.approx(1_250.0)
    assert outcome.expected_revenue == pytest.approx(6_000.0)
    assert outcome.operating_cost == pytest.approx(300.0)
    assert outcome.expected_profit == pytest.approx(4_450.0)


def test_optimizer_respects_constraints():
    pd_values = np.array([0.03, 0.08, 0.12, 0.25])
    exposure = np.array([10_000.0, 10_000.0, 10_000.0, 10_000.0])
    best, table = optimize_threshold(
        pd_values,
        exposure,
        thresholds=[0.05, 0.10, 0.15, 0.30],
        minimum_approval_rate=0.5,
        maximum_expected_loss_rate=0.08,
    )
    assert best.approval_rate >= 0.5
    assert not table.empty


def test_invalid_probability_is_rejected():
    with pytest.raises(ValueError):
        evaluate_threshold([1.2], [1000], 0.2)
