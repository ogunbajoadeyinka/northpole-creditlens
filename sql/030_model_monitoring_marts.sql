CREATE OR REPLACE VIEW creditlens.mart_model_score_distribution AS
SELECT
    model_version,
    width_bucket(probability_of_default, 0.0, 1.0, 10) AS pd_decile,
    COUNT(*) AS predictions,
    AVG(probability_of_default)::NUMERIC(8,6) AS avg_pd,
    AVG(expected_loss)::NUMERIC(14,2) AS avg_expected_loss,
    AVG(risk_adjusted_expected_profit)::NUMERIC(14,2) AS avg_risk_adjusted_profit
FROM creditlens.model_prediction
GROUP BY model_version, width_bucket(probability_of_default, 0.0, 1.0, 10);

CREATE OR REPLACE VIEW creditlens.mart_model_decision_mix AS
SELECT
    model_version,
    recommended_decision,
    COUNT(*) AS predictions,
    AVG(probability_of_default)::NUMERIC(8,6) AS avg_pd,
    SUM(expected_loss)::NUMERIC(18,2) AS total_expected_loss,
    SUM(risk_adjusted_expected_profit)::NUMERIC(18,2) AS total_risk_adjusted_profit
FROM creditlens.model_prediction
GROUP BY model_version, recommended_decision;

CREATE OR REPLACE VIEW creditlens.mart_model_daily_health AS
SELECT
    DATE(scored_at) AS score_date,
    model_version,
    COUNT(*) AS predictions,
    AVG(probability_of_default)::NUMERIC(8,6) AS avg_pd,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY probability_of_default)::NUMERIC(8,6) AS median_pd,
    AVG(expected_loss)::NUMERIC(14,2) AS avg_expected_loss,
    SUM(expected_loss)::NUMERIC(18,2) AS total_expected_loss,
    SUM(risk_adjusted_expected_profit)::NUMERIC(18,2) AS total_risk_adjusted_profit
FROM creditlens.model_prediction
GROUP BY DATE(scored_at), model_version;
