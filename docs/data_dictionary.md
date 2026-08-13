# NorthPole CreditLens — Historical Data Dictionary

## Source
Historical PD research baseline: UCI Machine Learning Repository, **Default of Credit Card Clients** (dataset ID 350). NorthPole is fictional; the source data is used only as an attributed historical benchmark and is not represented as NorthPole customer data.

## Canonical Historical Table
`creditlens.historical_credit_observation`

| Column | Type | Meaning |
|---|---|---|
| source_record_id | integer | Source observation identifier |
| credit_limit | numeric | Granted credit limit / credit amount represented by the source |
| sex_code | integer | Source-coded sex category; retained without reinterpretation |
| education_code | integer | Source-coded education category |
| marriage_code | integer | Source-coded marital-status category |
| age | integer | Age in years |
| repayment_status_m0 | integer | Most recent repayment-status code |
| repayment_status_m2..m6 | integer | Prior monthly repayment-status codes |
| bill_amount_m1..m6 | numeric | Monthly bill-statement amounts |
| payment_amount_m1..m6 | numeric | Monthly payment amounts |
| default_next_month | binary | Historical target: default payment next month |

## Modeling Target
`default_next_month = 1` means the historical observation defaulted in the following month; `0` means it did not.

## Important Semantic Guardrails
- Source category codes are preserved. We will not invent demographic labels not supported by source documentation.
- Historical credit-card behavior is not relabeled as consumer-loan origination data.
- The historical source supports PD research and model benchmarking; the later NorthPole application stream will use a separate, explicitly synthetic schema.
- Protected/demographic attributes will be evaluated carefully and will not automatically be used as production decision features. Fairness and governance analysis will be documented before final feature selection.

## Derived Analytics
The SQL analytics layer provides portfolio summary, credit-limit bands, age bands, repayment-risk segments, and payment-to-bill behavior. These are descriptive/diagnostic analytics and are kept conceptually separate from model outputs.
