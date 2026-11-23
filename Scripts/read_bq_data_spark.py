from pyspark.sql import SparkSession
from pyspark.sql.functions import col,sum
from pyspark.sql.types import DecimalType


spark = SparkSession.builder.master("local[2]").appName("Testing").getOrCreate()

sql = "SELECT * FROM `project-4618bee0-3860-4865-b85.sample_data.sample_employee_salary`;"
project = "project-4618bee0-3860-4865-b85"
dataset = "sample_data"

# Read data from BigQuery
df = spark.read.format("bigquery") \
    .option("materializationProject",project) \
    .option("materializationDataset", dataset) \
    .option("viewsEnabled", "true") \
    .option("query", sql) \
    .load()

# Show the data
print("Data first Bigquery Call:")
df.show(truncate=False)

df.withColumn("round_bonus",col("bonus").cast(DecimalType(25,2))).show(truncate=False)

# round off other way

# sql_new = "SELECT employee_id, employee_name, department, ROUND(cast(bonus as NUMERIC),2) as round_new FROM `project-4618bee0-3860-4865-b85.sample_data.sample_employee_salary`;"

sql_new = "SELECT employee_id, employee_name, department, ROUND(bonus,2) as round_new FROM `project-4618bee0-3860-4865-b85.sample_data.sample_employee_salary`;"

df_bq = spark.read.format("bigquery") \
    .option("materializationProject",project) \
    .option("materializationDataset", dataset) \
    .option("viewsEnabled", "true") \
    .option("query", sql_new) \
    .load()

# Show the data
print("Data second Bigquery Call:")
df_bq.show(truncate=False)

df_bq.printSchema()
df.printSchema()



df_aggr = df.groupBy("department").agg(sum("bonus").alias("sum_bonus"))

print("Data aggregated:")
df_aggr.show(truncate=False)

# Bigquery Type --> Spark Type
# STRING --> String
# FLOAT64 --> Double
# NUMERIC --> DecimalType(38,9)

# write to bigquery
df_aggr.write.format("bigquery") \
    .option("table", f"{project}.{dataset}.sample_employee_salary_new") \
    .mode("overwrite") \
    .save()

spark.stop()