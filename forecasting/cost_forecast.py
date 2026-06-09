import pandas as pd
from prophet import Prophet

# Read daily cost data
import duckdb
from prophet import Prophet

df = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/daily_cost/*.parquet'
)
""").df()

# Create date column
df["ds"] = pd.to_datetime(
    df[["year", "month", "day"]]
)

# Prophet expects:
# ds = date
# y = value

df = df[["ds", "total_cost"]]
df = df.rename(
    columns={"total_cost": "y"}
)

model = Prophet()

model.fit(df)

future = model.make_future_dataframe(
    periods=30
)

forecast = model.predict(future)

forecast[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].to_parquet(
    "forecasting/cost_forecast.parquet",
    index=False
)

print(
    forecast[
        ["ds", "yhat"]
    ].tail(30)
)