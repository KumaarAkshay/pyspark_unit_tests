from pathlib import Path

def read_csv(spark, csv_path):
    """
    Read a CSV file and return a Spark DataFrame.
    """
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(csv_path))
    )