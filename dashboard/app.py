import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

st.set_page_config(
    page_title="AI Cost Governance Platform",
    layout="wide"
)

st.title("💰 AI Cost Governance Platform")

# -----------------------
# LOAD DATA
# -----------------------

provider = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/provider_cost_summary/*.parquet'
)
""").df()

team = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/team_cost/*.parquet'
)
""").df()

daily = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/daily_cost/*.parquet'
)
""").df()

model = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/model_cost/*.parquet'
)
""").df()

users = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/gold/top_users/*.parquet'
)
""").df()

raw = duckdb.sql("""
SELECT *
FROM read_parquet(
'data-lake/silver/ai_usage_clean.parquet/*.parquet'
)
""").df()

# -----------------------
# KPI
# -----------------------

total_spend = round(raw["cost_usd"].sum(), 2)
total_requests = len(raw)
total_users = raw["user"].nunique()
avg_cost = round(raw["cost_usd"].mean(), 4)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Spend ($)", f"{total_spend:,.2f}")
c2.metric("Requests", f"{total_requests:,}")
c3.metric("Users", total_users)
c4.metric("Avg Cost/Request", avg_cost)

st.divider()

# -----------------------
# Budget Governance
# -----------------------

MONTHLY_BUDGET = 100000

utilization = (
    total_spend / MONTHLY_BUDGET
) * 100

st.subheader("Budget Governance")

if utilization < 70:
    st.success(f"Healthy - {utilization:.2f}% Budget Used")
elif utilization < 90:
    st.warning(f"Warning - {utilization:.2f}% Budget Used")
else:
    st.error(f"Critical - {utilization:.2f}% Budget Used")

# -----------------------
# Provider Cost
# -----------------------

st.subheader("Provider Cost")

fig1 = px.bar(
    provider,
    x="provider",
    y="total_cost"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------
# Team Cost
# -----------------------

st.subheader("Team Cost")

fig2 = px.bar(
    team,
    x="team",
    y="total_cost"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# Daily Trend
# -----------------------

daily["date"] = pd.to_datetime(
    daily[["year", "month", "day"]]
)

st.subheader("Daily AI Spend Trend")

fig3 = px.line(
    daily.sort_values("date"),
    x="date",
    y="total_cost"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# Forecast
# -----------------------

forecast = pd.read_parquet(
    "forecasting/cost_forecast.parquet"
)

st.subheader("30 Day Cost Forecast")

fig4 = px.line(
    forecast,
    x="ds",
    y="yhat"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------
# Anomalies
# -----------------------

anomalies = pd.read_parquet(
    "ml/anomalies.parquet"
)

st.subheader("Detected Cost Anomalies")

st.dataframe(
    anomalies,
    use_container_width=True
)

# -----------------------
# Top Users
# -----------------------

st.subheader("Top Users")

st.dataframe(
    users,
    use_container_width=True
)

# -----------------------
# Model Cost
# -----------------------

st.subheader("Model Cost")

fig5 = px.pie(
    model,
    names="model",
    values="total_cost"
)

st.plotly_chart(fig5, use_container_width=True)