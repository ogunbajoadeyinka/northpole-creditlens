# NorthPole CreditLens — Business Case

## Executive Summary
NorthPole is a fictional digital lending company. CreditLens is its production-style credit risk decision intelligence platform. The platform connects data ingestion, analytics, machine learning, credit-loss estimation, decision optimization, executive BI, and production monitoring in one end-to-end system.

## Business Problem
NorthPole needs to grow lending profitably while controlling credit losses. CreditLens is designed to answer five layers of questions:

1. **Describe — Data Analytics:** What is happening across applications and the loan portfolio?
2. **Diagnose — Business Analytics:** Why are approval, loss, and profitability metrics changing?
3. **Predict — Data Science:** Which applicants are likely to default and with what probability?
4. **Prescribe — Decision Science:** Which approval policy maximizes risk-adjusted value within risk constraints?
5. **Monitor — Business Intelligence:** Are portfolio, model, data, and system health within acceptable limits?

## Primary Users
- Credit Risk Executive
- Portfolio/Risk Manager
- Credit Analyst
- Data Scientist
- Business Intelligence Analyst
- Model Risk / Monitoring Analyst

## Core Decisions
- Approve, decline, or refer an application for manual review.
- Estimate Probability of Default (PD).
- Estimate Expected Loss using PD × LGD × EAD.
- Compare approval thresholds and their impact on approval rate, losses, revenue, and expected profit.
- Identify high-risk segments and emerging portfolio deterioration.
- Monitor model performance, calibration, drift, data quality, and pipeline health.

## Initial Business KPIs
### Portfolio
- Total applications
- Approval rate
- Approved exposure
- Average loan amount
- Risk-grade distribution

### Credit Risk
- Default rate
- Average predicted PD
- Expected Loss
- Expected Loss Rate
- Delinquency/default concentration by segment

### Economics
- Expected interest revenue
- Expected credit loss
- Estimated operating cost
- Risk-adjusted expected profit
- Profit per approved application

### Model
- ROC-AUC
- PR-AUC
- KS statistic
- Brier score
- Calibration error
- Precision/recall at operating threshold
- Prediction latency
- Feature/data drift indicators

### Data & Platform
- Records ingested
- Failed validations
- Missing-value rate
- Duplicate rate
- Last successful ingestion
- API health and latency

## Product Experiences
1. **Power BI Executive Intelligence** — portfolio, applications, risk, profitability, decision lab, model intelligence, and system health.
2. **CreditLens Decision Lab** — interactive scenario analysis and approval-policy simulation.
3. **Applicant Risk Experience** — applicant-level PD, expected loss, risk grade, decision, and explainability.
4. **Live Monitoring** — continuously changing portfolio and operational metrics as new synthetic applications arrive.

## Portfolio Integrity
NorthPole is fictional. Synthetic live applications and any simulated financial impact will be clearly labeled. Public historical datasets will be attributed. No simulated result will be represented as real corporate performance.
