# from pyspark.sql import SparkSession
# from pyspark.sql.functions import sum as spark_sum

# spark = SparkSession.builder \
#     .appName("SilverToGold") \
#     .getOrCreate()

# df = spark.read.parquet(
#     "data-lake/silver/ai_usage_clean.parquet"
# )

# provider_cost = (
#     df.groupBy("provider")
#       .agg(spark_sum("cost_usd").alias("total_cost"))
# )

# team_cost = (
#     df.groupBy("team")
#       .agg(spark_sum("cost_usd").alias("total_cost"))
# )

# daily_cost = (
#     df.groupBy("year", "month", "day")
#       .agg(spark_sum("cost_usd").alias("total_cost"))
# )

# model_cost = (
#     df.groupBy("model")
#       .agg(spark_sum("cost_usd").alias("total_cost"))
# )

# top_users = (
#     df.groupBy("user")
#       .agg(spark_sum("cost_usd").alias("total_cost"))
#       .orderBy("total_cost", ascending=False)
#       .limit(20)
# )

# provider_cost.write.mode("overwrite").parquet(
#     "data-lake/gold/provider_cost"
# )

# team_cost.write.mode("overwrite").parquet(
#     "data-lake/gold/team_cost"
# )

# daily_cost.write.mode("overwrite").parquet(
#     "data-lake/gold/daily_cost"
# )

# model_cost.write.mode("overwrite").parquet(
#     "data-lake/gold/model_cost"
# )

# top_users.write.mode("overwrite").parquet(
#     "data-lake/gold/top_users"
# )

# print("Gold Layer Created Successfully")

# spark.stop()

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count

spark = SparkSession.builder \
    .appName("SilverToGold") \
    .getOrCreate()

df = spark.read.parquet(
    "data-lake/silver/ai_usage_clean.parquet"
)

provider_cost = (
    df.groupBy("provider")
      .agg(
          sum("cost_usd").alias("total_cost"),
          count("*").alias("request_count")
      )
)

provider_cost.show()

provider_cost.write.mode("overwrite").parquet(
    "data-lake/gold/provider_cost_summary"
)

spark.stop()