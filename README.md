# NorthPole CreditLens

**Credit Risk Decision Intelligence Platform**

NorthPole CreditLens is a production-style portfolio project that connects data engineering, data analytics, business analytics, machine learning, decision science, business intelligence, cloud deployment, and monitoring in one end-to-end credit-risk system.

> **NorthPole is fictional.** Historical public data and all synthetic/live demo data are clearly separated and labeled.

## Product Philosophy

**Describe → Diagnose → Predict → Prescribe → Monitor**

- **Describe:** SQL/EDA shows what is happening in the credit portfolio.
- **Diagnose:** business analytics explains where risk and performance changes come from.
- **Predict:** calibrated ML estimates Probability of Default (PD).
- **Prescribe:** PD, LGD, EAD and economics feed approval-policy and expected-loss decisions.
- **Monitor:** Power BI and production monitoring track portfolio, model, data and platform health.

## Target Architecture

```mermaid
flowchart LR
    A[Public Historical Data] --> B[Validation / ETL]
    S[Synthetic Live Applications] --> B
    B --> C[(S3 Raw / Curated)]
    C --> D[(PostgreSQL / RDS)]
    D --> E[Analytics / SQL]
    D --> F[ML Scoring]
    F --> G[Decision Engine]
    G --> H[FastAPI]
    D --> I[Power BI]
    H --> J[Decision Lab]
    F --> K[Model Monitoring]
    K --> I
```

## Current Build Status

- [x] Business case and KPI framework
- [x] Initial platform architecture
- [x] Python package and CI foundation
- [x] Expected-loss / credit-decision primitives
- [x] UCI historical source adapter
- [x] Historical data-quality checks
- [x] Canonical transformation layer
- [x] PostgreSQL historical loader
- [x] Initial analytics schema and SQL views
- [ ] Full EDA and business-analysis notebook
- [ ] Statistical analysis and feature engineering
- [ ] PD baseline models and calibration
- [ ] SHAP / explainability
- [ ] Decision-policy optimization
- [ ] FastAPI serving layer
- [ ] Live synthetic application stream
- [ ] Professional Power BI experience
- [ ] AWS deployment and monitoring

## Historical Research Baseline

The initial PD benchmark uses the UCI **Default of Credit Card Clients** dataset. The raw dataset is not committed to GitHub. `src/creditlens/data/source.py` fetches it reproducibly from UCI, validation gates inspect data quality, and `transform.py` converts it into a stable analytical schema.

Historical credit-card fields are **not** presented as NorthPole loan-origination data. A separate synthetic schema will later power the live NorthPole application stream.

## Run the Historical Pipeline

```bash
python -m pip install -e ".[data,dev]"
python scripts/ingest_historical.py
```

To load into PostgreSQL:

```bash
export DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE"
python scripts/ingest_historical.py
```

Never commit credentials. Cloud secrets will be stored in appropriate secret-management/configuration systems.

## Repository Structure

```text
src/creditlens/      reusable Python application and ML logic
sql/                 analytical schema and BI-serving SQL
tests/               automated quality checks
scripts/             operational entry points
docs/                business, architecture, data and model documentation
.github/workflows/    CI/CD automation
```

## Planned BI Experience

The Power BI layer will be designed as a modern financial analytics application with Executive Overview, Applications Intelligence, Credit Risk, Profitability, Decision Lab, Model Intelligence, and Data/System Health experiences. Navigation, drill-through, tooltips, scenario parameters, dynamic metrics, and coordinated light/dark visual states are part of the design target.

## Documentation

See `docs/business_case.md`, `docs/architecture.md`, `docs/data_dictionary.md`, and `docs/roadmap.md` for design rationale and delivery milestones.
