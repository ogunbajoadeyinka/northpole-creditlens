"""Decision-policy economics for NorthPole CreditLens."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PolicyAssumptions:
    loss_given_default: float = 0.45
    annual_interest_rate: float = 0.18
    operating_cost_rate: float = 0.02
    manual_review_cost: float = 35.0


@dataclass(frozen=True)
class PolicyOutcome:
    pd_threshold: float
    applications: int
    approved: int
    approval_rate: float
    exposure: float
    expected_revenue: float
    expected_loss: float
    operating_cost: float
    expected_profit: float


def evaluate_threshold(
    probability_of_default,
    exposure,
    pd_threshold: float,
    assumptions: PolicyAssumptions | None = None,
) -> PolicyOutcome:
    """Evaluate an approval threshold using simplified expected economics."""
    assumptions = assumptions or PolicyAssumptions()
    pd = np.asarray(probability_of_default, dtype=float)
    ead = np.asarray(exposure, dtype=float)
    if pd.shape != ead.shape:
        raise ValueError("probability_of_default and exposure must have the same shape")
    if not 0 <= pd_threshold <= 1:
        raise ValueError("pd_threshold must be between 0 and 1")
    if np.any((pd < 0) | (pd > 1)):
        raise ValueError("probability values must be between 0 and 1")
    if np.any(ead < 0):
        raise ValueError("exposure values must be non-negative")

    approved_mask = pd <= pd_threshold
    approved_pd = pd[approved_mask]
    approved_ead = ead[approved_mask]
    total_exposure = float(approved_ead.sum())
    expected_loss = float((approved_pd * assumptions.loss_given_default * approved_ead).sum())
    expected_revenue = float((approved_ead * assumptions.annual_interest_rate).sum())
    operating_cost = float((approved_ead * assumptions.operating_cost_rate).sum())
    expected_profit = expected_revenue - expected_loss - operating_cost
    approved = int(approved_mask.sum())
    applications = int(len(pd))
    return PolicyOutcome(
        pd_threshold=float(pd_threshold),
        applications=applications,
        approved=approved,
        approval_rate=float(approved / applications) if applications else 0.0,
        exposure=total_exposure,
        expected_revenue=expected_revenue,
        expected_loss=expected_loss,
        operating_cost=operating_cost,
        expected_profit=expected_profit,
    )


def optimize_threshold(
    probability_of_default,
    exposure,
    thresholds=None,
    assumptions: PolicyAssumptions | None = None,
    minimum_approval_rate: float = 0.0,
    maximum_expected_loss_rate: float | None = None,
) -> tuple[PolicyOutcome, pd.DataFrame]:
    """Search candidate PD cutoffs for maximum expected profit under constraints."""
    if thresholds is None:
        thresholds = np.linspace(0.02, 0.40, 77)
    outcomes = [evaluate_threshold(probability_of_default, exposure, float(t), assumptions) for t in thresholds]
    table = pd.DataFrame([outcome.__dict__ for outcome in outcomes])
    table["expected_loss_rate"] = np.where(table["exposure"] > 0, table["expected_loss"] / table["exposure"], 0.0)

    eligible = table[table["approval_rate"] >= minimum_approval_rate].copy()
    if maximum_expected_loss_rate is not None:
        eligible = eligible[eligible["expected_loss_rate"] <= maximum_expected_loss_rate]
    if eligible.empty:
        raise ValueError("No threshold satisfies the supplied policy constraints")

    best_row = eligible.loc[eligible["expected_profit"].idxmax()]
    best = PolicyOutcome(
        pd_threshold=float(best_row["pd_threshold"]),
        applications=int(best_row["applications"]),
        approved=int(best_row["approved"]),
        approval_rate=float(best_row["approval_rate"]),
        exposure=float(best_row["exposure"]),
        expected_revenue=float(best_row["expected_revenue"]),
        expected_loss=float(best_row["expected_loss"]),
        operating_cost=float(best_row["operating_cost"]),
        expected_profit=float(best_row["expected_profit"]),
    )
    return best, table
