CREATE OR REPLACE VIEW creditlens.mart_risk_overview AS
SELECT
    COUNT(*) AS observations,
    SUM(default_next_month) AS defaults,
    AVG(default_next_month::NUMERIC)::NUMERIC(8,6) AS default_rate,
    AVG(credit_limit)::NUMERIC(14,2) AS avg_credit_limit,
    SUM(credit_limit)::NUMERIC(18,2) AS total_credit_limit,
    AVG(bill_amount_m1)::NUMERIC(14,2) AS avg_latest_bill,
    AVG(payment_amount_m1)::NUMERIC(14,2) AS avg_latest_payment,
    AVG(
        CASE WHEN bill_amount_m1 > 0
            THEN payment_amount_m1 / bill_amount_m1
            ELSE NULL
        END
    )::NUMERIC(10,6) AS avg_payment_to_bill_ratio
FROM creditlens.historical_credit_observation;

CREATE OR REPLACE VIEW creditlens.mart_risk_segment AS
WITH segmented AS (
    SELECT
        source_record_id,
        credit_limit,
        age,
        repayment_status_m0,
        default_next_month,
        CASE
            WHEN credit_limit < 50000 THEN '<50K'
            WHEN credit_limit < 100000 THEN '50K-99K'
            WHEN credit_limit < 200000 THEN '100K-199K'
            WHEN credit_limit < 300000 THEN '200K-299K'
            ELSE '300K+'
        END AS credit_limit_band,
        CASE
            WHEN age < 25 THEN '<25'
            WHEN age < 35 THEN '25-34'
            WHEN age < 45 THEN '35-44'
            WHEN age < 55 THEN '45-54'
            ELSE '55+'
        END AS age_band,
        CASE
            WHEN repayment_status_m0 <= 0 THEN 'Current / no delay'
            WHEN repayment_status_m0 = 1 THEN '1 month delay'
            WHEN repayment_status_m0 = 2 THEN '2 months delay'
            ELSE '3+ months delay'
        END AS repayment_risk_band
    FROM creditlens.historical_credit_observation
)
SELECT
    credit_limit_band,
    age_band,
    repayment_risk_band,
    COUNT(*) AS observations,
    SUM(default_next_month) AS defaults,
    AVG(default_next_month::NUMERIC)::NUMERIC(8,6) AS default_rate,
    SUM(credit_limit)::NUMERIC(18,2) AS total_credit_limit,
    AVG(credit_limit)::NUMERIC(14,2) AS avg_credit_limit
FROM segmented
GROUP BY credit_limit_band, age_band, repayment_risk_band;

CREATE OR REPLACE VIEW creditlens.mart_payment_behavior AS
SELECT
    source_record_id,
    credit_limit,
    age,
    repayment_status_m0,
    bill_amount_m1,
    payment_amount_m1,
    CASE
        WHEN bill_amount_m1 > 0 THEN payment_amount_m1 / bill_amount_m1
        ELSE NULL
    END AS payment_to_bill_ratio,
    CASE
        WHEN bill_amount_m1 <= 0 THEN 'No positive bill'
        WHEN payment_amount_m1 / NULLIF(bill_amount_m1, 0) < 0.05 THEN '<5%'
        WHEN payment_amount_m1 / NULLIF(bill_amount_m1, 0) < 0.20 THEN '5%-19%'
        WHEN payment_amount_m1 / NULLIF(bill_amount_m1, 0) < 0.50 THEN '20%-49%'
        ELSE '50%+'
    END AS payment_behavior_band,
    default_next_month
FROM creditlens.historical_credit_observation;
