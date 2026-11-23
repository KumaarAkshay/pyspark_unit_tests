import os
import sys
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="module")
def spark():

    # Use the same Python interpreter for Spark workers
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("Pytest")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )

    yield session

    session.stop()