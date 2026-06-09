from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ReadGold") \
    .getOrCreate()

df = spark.read.parquet(
    "data-lake/gold/provider_cost_summary"
)

df.show()

spark.stop()