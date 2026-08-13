# NorthPole CreditLens — PD Methodology

The historical UCI benchmark supports Probability of Default research only; it is not represented as real NorthPole borrower data.

The baseline excludes record identifiers and the target from predictors. It also excludes source-coded demographic fields from the default modeling feature set. These fields may be retained only for documented subgroup analysis.

The baseline workflow is: base-rate benchmark, logistic regression, probability calibration review, tree-based challengers, explainability, stability checks, and finally threshold selection based on business economics rather than accuracy alone.

Primary evaluation includes ROC-AUC, PR-AUC, Brier score, calibration, precision, recall, and later expected-loss and risk-adjusted profit measures once PD is connected to LGD and EAD.

All public results will be identified as historical benchmark results, backtests, or synthetic simulations.
