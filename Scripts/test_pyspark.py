from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[2]").appName("Test").getOrCreate()
print("Spark Version:", spark.version)
spark.stop()
