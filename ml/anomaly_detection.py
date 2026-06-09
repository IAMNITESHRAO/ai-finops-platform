import duckdb
import pandas as pd
from sklearn.ensemble import IsolationForest

df = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/daily_cost/*.parquet'
)
""").df()

df["date"] = pd.to_datetime(
    df[["year", "month", "day"]]
)

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df["anomaly"] = model.fit_predict(
    df[["total_cost"]]
)

anomalies = df[
    df["anomaly"] == -1
]

print("\nAnomalies Found:\n")
print(
    anomalies[
        ["date", "total_cost"]
    ]
)

anomalies.to_parquet(
    "ml/anomalies.parquet",
    index=False
)