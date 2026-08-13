# NorthPole CreditLens — Business Analytics Question Bank

The historical analytics phase is designed to prove that CreditLens can move from raw credit data to management-relevant insight before any ML model is introduced.

## Executive Questions
1. What is the overall historical default rate?
2. How is risk distributed across credit-limit bands?
3. Which repayment-status groups contribute disproportionately to default?
4. How do payment behavior and outstanding balances relate to default risk?
5. Which customer segments combine large exposure with elevated default risk?
6. Where should an analyst investigate first if portfolio risk rises?

## Data Analytics Questions
7. What are the distributions of credit limits, age, bill balances, and payments?
8. Are there extreme or implausible values requiring treatment or governance review?
9. How stable are balances and payments across the six observed months?
10. Which variables are highly correlated and may be redundant?
11. How concentrated is the target class, and what does that imply for model evaluation?

## Business Analytics Questions
12. Which credit-limit bands carry the highest default rate versus the highest absolute number of defaults?
13. How does most-recent repayment status change the observed probability of default?
14. Do low payment-to-bill ratios identify materially higher-risk behavior?
15. Which groups have high balances but weak repayment behavior?
16. How much of observed default volume is concentrated in the riskiest 20% of behavioral segments?

## Data Science Preparation Questions
17. Which variables show the strongest univariate relationship with default?
18. Which fields risk target leakage or post-outcome contamination?
19. Which categories require careful encoding or grouping?
20. Which candidate features should be excluded from production decisioning for governance/fairness reasons?
21. What baseline performance should a simple logistic regression achieve before considering more complex models?
22. Is predicted probability well calibrated enough for expected-loss calculations?

## BI Translation
Each analytical question must map to at least one of the following Power BI experiences:
- Executive Overview
- Portfolio Risk
- Customer / Behavioral Segmentation
- Repayment & Exposure Analysis
- Model Intelligence
- Decision Lab

The dashboard should not merely display charts. Each page should make it possible to answer a management question and expose a clear path from observation → explanation → action.
