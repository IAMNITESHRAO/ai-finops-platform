# THIS IS THROUGH PANDAS

# import pandas as pd

# # Read bronze layer
# df = pd.read_parquet("data-lake/bronze/ai_usage.parquet")

# print("Original Records:", len(df))

# # Remove duplicates
# df = df.drop_duplicates()

# # Remove nulls
# df = df.dropna()

# # Standardize timestamp
# df["timestamp"] = pd.to_datetime(df["timestamp"])

# # Extract date parts
# df["year"] = df["timestamp"].dt.year
# df["month"] = df["timestamp"].dt.month
# df["day"] = df["timestamp"].dt.day

# # Cost validation
# df = df[df["cost_usd"] >= 0]

# print("Clean Records:", len(df))

# # Save silver layer
# df.to_parquet(
#     "data-lake/silver/ai_usage_clean.parquet",
#     index=False
# )

# print("Silver layer created successfully")
# print(df.head())

# THIS IS THROUGH APACHE SPARK

from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month, dayofmonth, col

spark = SparkSession.builder \
    .appName("BronzeToSilver") \
    .getOrCreate()

df = spark.read.parquet("data-lake/bronze/ai_usage.parquet")

print("Original Records:", df.count())

df = df.dropDuplicates()
df = df.na.drop()

df = (
    df.withColumn("year", year(col("timestamp")))
      .withColumn("month", month(col("timestamp")))
      .withColumn("day", dayofmonth(col("timestamp")))
)

df = df.filter(col("cost_usd") >= 0)

print("Clean Records:", df.count())

df.write.mode("overwrite").parquet(
    "data-lake/silver/ai_usage_clean.parquet"
)

print("Silver layer created successfully")

spark.stop()