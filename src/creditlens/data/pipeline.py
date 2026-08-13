"""End-to-end historical data pipeline for NorthPole CreditLens."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from creditlens.data.load import LoadResult, build_engine, replace_historical_table
from creditlens.data.source import fetch_uci_default_data
from creditlens.data.transform import to_canonical_historical_frame
from creditlens.data.validation import DataQualityReport, validate_historical_frame


@dataclass(frozen=True)
class HistoricalPipelineResult:
    quality: DataQualityReport
    load: LoadResult | None

    def as_dict(self) -> dict[str, object]:
        return {
            "quality": asdict(self.quality),
            "load": asdict(self.load) if self.load is not None else None,
        }


def run_historical_pipeline(database_url: str | None = None) -> HistoricalPipelineResult:
    """Fetch, validate, canonicalize and optionally load the UCI baseline."""
    raw = fetch_uci_default_data()
    quality = validate_historical_frame(raw)
    canonical = to_canonical_historical_frame(raw)

    load_result = None
    if database_url:
        engine = build_engine(database_url)
        try:
            load_result = replace_historical_table(canonical, engine)
        finally:
            engine.dispose()

    return HistoricalPipelineResult(quality=quality, load=load_result)
