# NorthPole CreditLens — Power BI Semantic Model

## Objective
Create a recruiter-grade semantic layer that makes Data Analytics, Business Analytics, Data Science, model monitoring, and system health visible in one report.

## Core Tables

### Historical / Research
- `creditlens.historical_credit_observation`
- `creditlens.mart_risk_overview`
- `creditlens.mart_risk_segment`
- `creditlens.mart_payment_behavior`

### Model Monitoring
- `creditlens.model_prediction`
- model calibration / monitoring marts

### Live Synthetic Portfolio
- `creditlens.synthetic_portfolio_event`
- `creditlens.synthetic_portfolio_snapshot`
- `creditlens.pipeline_health_event`

## Recommended Report Pages
1. Executive Overview
2. Portfolio & Segment Analytics
3. Risk Intelligence
4. Model Intelligence
5. Scenario Lab
6. Data & System Health

## Model Relationships
Use a star-schema mindset for live data:
- `DimDate` → snapshots, predictions, health events
- `DimRiskBand` → portfolio snapshots / monitoring aggregates
- `DimModelVersion` → model monitoring facts
- `FactPortfolioSnapshot` → executive KPIs and trends
- `FactModelMonitoring` → calibration, score distribution, quality metrics
- `FactPipelineHealth` → refresh/system status

Historical UCI research tables remain visually separated from fictional NorthPole live-demo tables.

## Power BI Interaction Features
- Collapsible sidebar using bookmarks + selection pane
- Slide-out filters
- Light and dark coordinated themes
- Dynamic metric selector using field parameters
- Drill-through to segment detail
- Report-page tooltips
- What-if parameter for aggregate scenario analysis
- Synced slicers
- Dynamic page titles
- Conditional KPI formatting
- Last-refresh and freshness indicators

## Governance Boundary
The report is an educational/research portfolio system. Synthetic live data is fictional, historical source data is attributed, and aggregate scenarios are for analytics demonstration rather than making lending decisions for real people.
