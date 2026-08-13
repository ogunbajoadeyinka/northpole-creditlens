CREATE OR REPLACE VIEW creditlens.v_historical_portfolio_summary AS
SELECT
    COUNT(*) AS observations,
    AVG(credit_limit)::NUMERIC(14,2) AS avg_credit_limit,
    AVG(default_next_month::NUMERIC)::NUMERIC(8,6) AS default_rate,
    AVG(age)::NUMERIC(8,2) AS avg_age,
    AVG(bill_amount_m1)::NUMERIC(14,2) AS avg_latest_bill,
    AVG(payment_amount_m1)::NUMERIC(14,2) AS avg_latest_payment
FROM creditlens.historical_credit_observation;

CREATE OR REPLACE VIEW creditlens.v_default_by_credit_limit_band AS
SELECT
    CASE
        WHEN credit_limit < 50000 THEN '<50K'
        WHEN credit_limit < 100000 THEN '50K-99K'
        WHEN credit_limit < 200000 THEN '100K-199K'
        WHEN credit_limit < 300000 THEN '200K-299K'
        ELSE '300K+'
    END AS credit_limit_band,
    COUNT(*) AS observations,
    SUM(default_next_month) AS defaults,
    AVG(default_next_month::NUMERIC)::NUMERIC(8,6) AS default_rate,
    AVG(credit_limit)::NUMERIC(14,2) AS avg_credit_limit
FROM creditlens.historical_credit_observation
GROUP BY 1;

CREATE OR REPLACE VIEW creditlens.v_default_by_age_band AS
SELECT
    CASE
        WHEN age < 25 THEN '<25'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END AS age_band,
    COUNT(*) AS observations,
    SUM(default_next_month) AS defaults,
    AVG(default_next_month::NUMERIC)::NUMERIC(8,6) AS default_rate,
    AVG(credit_limit)::NUMERIC(14,2) AS avg_credit_limit
FROM creditlens.historical_credit_observation
GROUP BY 1;

CREATE OR REPLACE VIEW creditlens.v_repayment_risk AS
SELECT
    repayment_status_m0,
    COUNT(*) AS observations,
    SUM(default_next_month) AS defaults,
    AVG(default_next_month::NUMERIC)::NUMERIC(8,6) AS default_rate,
    AVG(credit_limit)::NUMERIC(14,2) AS avg_credit_limit,
    AVG(bill_amount_m1)::NUMERIC(14,2) AS avg_latest_bill,
    AVG(payment_amount_m1)::NUMERIC(14,2) AS avg_latest_payment
FROM creditlens.historical_credit_observation
GROUP BY repayment_status_m0;

CREATE OR REPLACE VIEW creditlens.v_payment_behavior AS
SELECT
    source_record_id,
    credit_limit,
    age,
    repayment_status_m0,
    bill_amount_m1,
    payment_amount_m1,
    CASE
        WHEN bill_amount_m1 <= 0 THEN NULL
        ELSE payment_amount_m1 / NULLIF(bill_amount_m1, 0)
    END AS latest_payment_to_bill_ratio,
    default_next_month
FROM creditlens.historical_credit_observation;
