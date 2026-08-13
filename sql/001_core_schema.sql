CREATE SCHEMA IF NOT EXISTS creditlens;

CREATE TABLE IF NOT EXISTS creditlens.historical_credit_observation (
    observation_id BIGSERIAL PRIMARY KEY,
    source_record_id BIGINT,
    credit_limit NUMERIC(14,2),
    sex_code SMALLINT,
    education_code SMALLINT,
    marriage_code SMALLINT,
    age SMALLINT,
    repayment_status_m0 SMALLINT,
    repayment_status_m2 SMALLINT,
    repayment_status_m3 SMALLINT,
    repayment_status_m4 SMALLINT,
    repayment_status_m5 SMALLINT,
    repayment_status_m6 SMALLINT,
    bill_amount_m1 NUMERIC(14,2),
    bill_amount_m2 NUMERIC(14,2),
    bill_amount_m3 NUMERIC(14,2),
    bill_amount_m4 NUMERIC(14,2),
    bill_amount_m5 NUMERIC(14,2),
    bill_amount_m6 NUMERIC(14,2),
    payment_amount_m1 NUMERIC(14,2),
    payment_amount_m2 NUMERIC(14,2),
    payment_amount_m3 NUMERIC(14,2),
    payment_amount_m4 NUMERIC(14,2),
    payment_amount_m5 NUMERIC(14,2),
    payment_amount_m6 NUMERIC(14,2),
    default_next_month SMALLINT NOT NULL CHECK (default_next_month IN (0, 1)),
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS creditlens.model_prediction (
    prediction_id BIGSERIAL PRIMARY KEY,
    application_id TEXT NOT NULL,
    model_version TEXT NOT NULL,
    probability_of_default NUMERIC(8,6) NOT NULL CHECK (probability_of_default BETWEEN 0 AND 1),
    loss_given_default NUMERIC(8,6) NOT NULL CHECK (loss_given_default BETWEEN 0 AND 1),
    exposure_at_default NUMERIC(14,2) NOT NULL,
    expected_loss NUMERIC(14,2) NOT NULL,
    expected_revenue NUMERIC(14,2),
    risk_adjusted_expected_profit NUMERIC(14,2),
    recommended_decision TEXT NOT NULL,
    scored_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_creditlens_prediction_scored_at
    ON creditlens.model_prediction (scored_at DESC);
