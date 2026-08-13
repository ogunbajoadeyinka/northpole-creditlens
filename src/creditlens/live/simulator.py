"""Synthetic aggregate telemetry for the NorthPole CreditLens live demo.

This module produces fictional portfolio-level observations for dashboard and
pipeline demonstrations. It does not represent real customers and does not make
individual lending decisions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import random


@dataclass(frozen=True)
class PortfolioSnapshot:
    snapshot_at: datetime
    observations: int
    total_exposure: float
    average_modeled_pd: float
    aggregate_expected_loss: float
    aggregate_expected_revenue: float
    pipeline_latency_ms: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def generate_snapshot(seed: int | None = None) -> PortfolioSnapshot:
    """Generate one reproducible synthetic portfolio-level snapshot."""
    rng = random.Random(seed)
    observations = rng.randint(8_000, 15_000)
    total_exposure = rng.uniform(80_000_000, 180_000_000)
    average_modeled_pd = rng.uniform(0.055, 0.115)
    aggregate_expected_loss = total_exposure * average_modeled_pd * rng.uniform(0.35, 0.55)
    aggregate_expected_revenue = total_exposure * rng.uniform(0.055, 0.095)
    pipeline_latency_ms = rng.uniform(45.0, 180.0)

    return PortfolioSnapshot(
        snapshot_at=datetime.now(UTC),
        observations=observations,
        total_exposure=round(total_exposure, 2),
        average_modeled_pd=round(average_modeled_pd, 6),
        aggregate_expected_loss=round(aggregate_expected_loss, 2),
        aggregate_expected_revenue=round(aggregate_expected_revenue, 2),
        pipeline_latency_ms=round(pipeline_latency_ms, 2),
    )
