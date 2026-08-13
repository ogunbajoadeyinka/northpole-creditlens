# NorthPole CreditLens — Data Strategy

## Historical Modeling Source
The first reproducible baseline uses the **UCI Default of Credit Card Clients** dataset (I-Cheng Yeh, 2009; UCI dataset ID 350; DOI: 10.24432/C55S3H), licensed CC BY 4.0.

Why this source:
- 30,000 observations and 23 explanatory variables: large enough for a credible baseline without creating unnecessary infrastructure cost.
- Explicit next-month default target suitable for Probability of Default modeling.
- Repayment status, bill amounts and payment history support meaningful risk analytics and feature engineering.
- Official UCI provenance and permissive attribution license make the portfolio reproducible.

## Important Scope Note
The source is a credit-card default dataset rather than a loan-origination dataset. NorthPole therefore uses it as the **historical PD research baseline**, while the later live demo layer will generate clearly labeled synthetic NorthPole applications with human-readable lending fields. We will not misrepresent synthetic fields as fields observed in the UCI source.

## Storage Pattern
### Development
- Source is fetched reproducibly through `ucimlrepo` rather than committed as a full raw dataset.
- Small derived samples may be stored only when necessary for tests.
- Local PostgreSQL is used before cloud deployment.

### Cloud target
- AWS S3: immutable/raw and curated analytical artifacts.
- AWS RDS PostgreSQL: serving tables for analytics, scoring, APIs and Power BI.
- Model artifacts: versioned object storage.

## Data Layers
1. **Raw/Bronze** — source-faithful data plus ingestion metadata.
2. **Curated/Silver** — renamed, typed, validated analytical records.
3. **Serving/Gold** — model features, predictions, portfolio metrics and BI-ready facts/dimensions.

## Target Definition
The UCI target represents default payment in the next month. In CreditLens it is normalized to `default_next_month` where 1 indicates default and 0 indicates non-default.

## Governance
- Dataset attribution remains in project documentation.
- Protected/demographic variables will be identified and handled deliberately; they are not automatically treated as acceptable underwriting features.
- Leakage review occurs before model training.
- All synthetic NorthPole data and simulated economics are labeled as such.
