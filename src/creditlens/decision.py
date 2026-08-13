"""Core credit decision economics for NorthPole CreditLens."""

from dataclasses import dataclass
from enum import StrEnum


class Decision(StrEnum):
    APPROVE = "approve"
    MANUAL_REVIEW = "manual_review"
    DECLINE = "decline"


@dataclass(frozen=True)
class CreditEconomics:
    probability_of_default: float
    loss_given_default: float
    exposure_at_default: float
    expected_revenue: float
    operating_cost: float = 0.0

    @property
    def expected_loss(self) -> float:
        return (
            self.probability_of_default
            * self.loss_given_default
            * self.exposure_at_default
        )

    @property
    def risk_adjusted_expected_profit(self) -> float:
        return self.expected_revenue - self.expected_loss - self.operating_cost


def recommend_decision(
    probability_of_default: float,
    approve_threshold: float = 0.12,
    review_threshold: float = 0.20,
) -> Decision:
    """Map a calibrated PD to an initial policy decision.

    Thresholds are demonstration defaults and will later be optimized against
    NorthPole's simulated portfolio economics and risk appetite.
    """
    if not 0 <= probability_of_default <= 1:
        raise ValueError("probability_of_default must be between 0 and 1")
    if not 0 <= approve_threshold < review_threshold <= 1:
        raise ValueError("thresholds must satisfy 0 <= approve < review <= 1")

    if probability_of_default <= approve_threshold:
        return Decision.APPROVE
    if probability_of_default <= review_threshold:
        return Decision.MANUAL_REVIEW
    return Decision.DECLINE
