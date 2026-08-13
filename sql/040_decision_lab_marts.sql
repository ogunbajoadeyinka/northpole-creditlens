CREATE OR REPLACE VIEW creditlens.mart_decision_lab AS
SELECT
    prediction_id,
    application_id,
    model_version,
    probability_of_default,
    loss_given_default,
    exposure_at_default,
    expected_loss,
    expected_revenue,
    risk_adjusted_expected_profit,
    recommended_decision,
    scored_at,
    CASE
        WHEN probability_of_default <= 0.05 THEN '0-5%'
        WHEN probability_of_default <= 0.10 THEN '5-10%'
        WHEN probability_of_default <= 0.15 THEN '10-15%'
        WHEN probability_of_default <= 0.20 THEN '15-20%'
        ELSE '20%+'
    END AS pd_band
FROM creditlens.model_prediction;

CREATE OR REPLACE VIEW creditlens.mart_decision_summary AS
SELECT
    model_version,
    recommended_decision,
    COUNT(*) AS applications,
    SUM(exposure_at_default)::NUMERIC(18,2) AS exposure,
    AVG(probability_of_default)::NUMERIC(8,6) AS avg_pd,
    SUM(expected_loss)::NUMERIC(18,2) AS expected_loss,
    SUM(expected_revenue)::NUMERIC(18,2) AS expected_revenue,
    SUM(risk_adjusted_expected_profit)::NUMERIC(18,2) AS expected_profit,
    CASE
        WHEN SUM(exposure_at_default) = 0 THEN 0
        ELSE (SUM(expected_loss) / SUM(exposure_at_default))::NUMERIC(8,6)
    END AS expected_loss_rate
FROM creditlens.model_prediction
GROUP BY model_version, recommended_decision;

CREATE OR REPLACE VIEW creditlens.mart_pd_distribution AS
SELECT
    model_version,
    CASE
        WHEN probability_of_default <= 0.05 THEN '0-5%'
        WHEN probability_of_default <= 0.10 THEN '5-10%'
        WHEN probability_of_default <= 0.15 THEN '10-15%'
        WHEN probability_of_default <= 0.20 THEN '15-20%'
        WHEN probability_of_default <= 0.30 THEN '20-30%'
        ELSE '30%+'
    END AS pd_band,
    COUNT(*) AS applications,
    SUM(exposure_at_default)::NUMERIC(18,2) AS exposure,
    AVG(expected_loss)::NUMERIC(14,2) AS avg_expected_loss,
    AVG(risk_adjusted_expected_profit)::NUMERIC(14,2) AS avg_expected_profit
FROM creditlens.model_prediction
GROUP BY model_version, pd_band;
