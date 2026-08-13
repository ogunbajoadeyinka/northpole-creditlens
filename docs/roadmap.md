# NorthPole CreditLens — Delivery Roadmap

| Milestone | Deliverable | Acceptance signal |
|---|---|---|
| M1 | Business case, architecture, repo foundation | Scope, KPIs, users, decisions and architecture documented |
| M2 | Data acquisition, validation and database | Reproducible pipeline loads documented historical data into analytical schema |
| M3 | SQL, EDA and business analysis | Business questions answered with reproducible SQL/Python analysis |
| M4 | Statistics and feature engineering | Leakage-safe features and statistical rationale documented |
| M5 | PD modeling and explainability | Baselines compared; champion justified; calibration and SHAP documented |
| M6 | Expected-loss and decision engine | PD/LGD/EAD economics and approval policies produce reproducible scenarios |
| M7 | FastAPI and interactive Decision Lab | Applicant and scenario endpoints tested and usable |
| M8 | Professional Power BI experience | Executive, risk, profitability, decision, model and health experiences connected to serving data |
| M9 | Live ingestion and AWS deployment | New applications flow through ingestion/scoring/serving and dashboards update |
| M10 | Monitoring, CI/CD and recruiter package | Automated tests, monitoring, documentation, demo and portfolio case study complete |

## Power BI Experience Targets
- Modern application-like navigation
- Collapsible/slide-out navigation and filter experiences using native Power BI interactions
- Coordinated light and dark visual experiences
- Executive Overview
- Applications Intelligence
- Credit Risk
- Profitability
- Decision Lab / What-if analysis
- Model Intelligence
- Data & System Health
- Drill-through and report-page tooltips
- Dynamic metric selection
- Clearly labeled simulated/live demo metrics

## Quality Gates
- No secrets committed to Git.
- Tests required for production Python logic.
- Data leakage checks before model selection.
- Business metrics separated from model metrics.
- Simulated results labeled as simulated/backtested.
- Reproducibility and limitations documented.
