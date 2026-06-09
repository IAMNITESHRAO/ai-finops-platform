import duckdb

con = duckdb.connect(
    "warehouse/ai_finops.db"
)

result = con.execute("""
SELECT *
FROM provider_cost
ORDER BY total_cost DESC
""").fetchdf()

print(result)