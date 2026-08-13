# NorthPole CreditLens — Power BI Measure Catalog

These measures are intended for the aggregate portfolio and model-monitoring experience. They support analysis and scenario reporting; they are not eligibility rules for real individuals.

## Core Portfolio Measures

```DAX
Total Exposure =
SUM ( mart_live_portfolio_trend[total_exposure] )
```

```DAX
Average Modeled PD =
AVERAGE ( mart_live_portfolio_trend[average_modeled_pd] )
```

```DAX
Aggregate Expected Loss =
SUM ( mart_live_portfolio_trend[aggregate_expected_loss] )
```

```DAX
Aggregate Expected Revenue =
SUM ( mart_live_portfolio_trend[aggregate_expected_revenue] )
```

```DAX
Modeled Net Value =
[Aggregate Expected Revenue] - [Aggregate Expected Loss]
```

```DAX
Expected Loss Rate =
DIVIDE ( [Aggregate Expected Loss], [Total Exposure] )
```

```DAX
Latest Snapshot Time =
MAX ( mart_live_portfolio_trend[snapshot_at] )
```

```DAX
Minutes Since Refresh =
DATEDIFF ( [Latest Snapshot Time], UTCNOW(), MINUTE )
```

## Operational Health

```DAX
Average Pipeline Latency (ms) =
AVERAGE ( mart_live_portfolio_trend[pipeline_latency_ms] )
```

```DAX
Latest Pipeline Latency (ms) =
VAR LatestTime = [Latest Snapshot Time]
RETURN
CALCULATE (
    MAX ( mart_live_portfolio_trend[pipeline_latency_ms] ),
    mart_live_portfolio_trend[snapshot_at] = LatestTime
)
```

```DAX
Freshness Status =
SWITCH (
    TRUE(),
    [Minutes Since Refresh] <= 5, "LIVE",
    [Minutes Since Refresh] <= 15, "DELAYED",
    "STALE"
)
```

## Historical Risk Measures

```DAX
Historical Observations =
SUM ( mart_risk_segment[observations] )
```

```DAX
Historical Defaults =
SUM ( mart_risk_segment[defaults] )
```

```DAX
Historical Default Rate =
DIVIDE ( [Historical Defaults], [Historical Observations] )
```

## Model Monitoring Measures

```DAX
Prediction Count =
COUNTROWS ( model_prediction )
```

```DAX
Average Predicted PD =
AVERAGE ( model_prediction[probability_of_default] )
```

```DAX
Average Scoring Latency (ms) =
AVERAGE ( model_prediction[latency_ms] )
```

## Formatting

- Currency KPIs: `$#,0.0,,M` for millions where appropriate.
- Percentages: `0.0%` or `0.00%` for model-quality detail.
- Latency: `0 ms`.
- Large counts: `#,0`.
- Freshness is shown beside the header as a status chip, not as a primary business KPI.

All simulated financial outputs must be visibly labeled **Synthetic / Simulated** in the report.