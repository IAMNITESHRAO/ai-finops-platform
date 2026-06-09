import duckdb

con = duckdb.connect(
    "warehouse/ai_finops.db"
)

# Provider Cost
con.execute("""
CREATE OR REPLACE TABLE provider_cost AS
SELECT *
FROM read_parquet(
'data-lake/gold/provider_cost_summary/*.parquet'
)
""")

# Team Cost
con.execute("""
CREATE OR REPLACE TABLE team_cost AS
SELECT *
FROM read_parquet(
'data-lake/gold/team_cost/*.parquet'
)
""")

# Daily Cost
con.execute("""
CREATE OR REPLACE TABLE daily_cost AS
SELECT *
FROM read_parquet(
'data-lake/gold/daily_cost/*.parquet'
)
""")

print("Warehouse Loaded Successfully")