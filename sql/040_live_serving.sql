CREATE TABLE IF NOT EXISTS creditlens.live_portfolio_snapshot (
    snapshot_at TIMESTAMPTZ PRIMARY KEY,
    observations INTEGER NOT NULL CHECK (observations >= 0),
    total_exposure NUMERIC(18,2) NOT NULL CHECK (total_exposure >= 0),
    average_modeled_pd NUMERIC(10,6) NOT NULL CHECK (average_modeled_pd BETWEEN 0 AND 1),
    aggregate_expected_loss NUMERIC(18,2) NOT NULL CHECK (aggregate_expected_loss >= 0),
    aggregate_expected_revenue NUMERIC(18,2) NOT NULL CHECK (aggregate_expected_revenue >= 0),
    pipeline_latency_ms NUMERIC(12,2) NOT NULL CHECK (pipeline_latency_ms >= 0),
    source_name TEXT NOT NULL DEFAULT 'northpole_synthetic_portfolio'
);

CREATE TABLE IF NOT EXISTS creditlens.pipeline_health_event (
    event_id BIGSERIAL PRIMARY KEY,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    component TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('healthy', 'degraded', 'failed')),
    latency_ms NUMERIC(12,2),
    records_processed INTEGER,
    failed_records INTEGER,
    message TEXT
);

CREATE OR REPLACE VIEW creditlens.mart_live_portfolio_latest AS
SELECT *
FROM creditlens.live_portfolio_snapshot
ORDER BY snapshot_at DESC
LIMIT 1;

CREATE OR REPLACE VIEW creditlens.mart_live_portfolio_trend AS
SELECT
    snapshot_at,
    observations,
    total_exposure,
    average_modeled_pd,
    aggregate_expected_loss,
    aggregate_expected_revenue,
    aggregate_expected_revenue - aggregate_expected_loss AS modeled_net_value,
    CASE
        WHEN total_exposure > 0 THEN aggregate_expected_loss / total_exposure
        ELSE NULL
    END AS expected_loss_rate,
    pipeline_latency_ms
FROM creditlens.live_portfolio_snapshot;

CREATE OR REPLACE VIEW creditlens.mart_pipeline_health_latest AS
SELECT DISTINCT ON (component)
    component,
    observed_at,
    status,
    latency_ms,
    records_processed,
    failed_records,
    message
FROM creditlens.pipeline_health_event
ORDER BY component, observed_at DESC;
