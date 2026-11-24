import os
import sys
import pytest
from pyspark.sql import SparkSession
from unittest.mock import MagicMock, patch
from pyspark.sql import DataFrame


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

@pytest.fixture
def mock_bq_read(spark):
    # Mock BigQuery reader
    mock_load = MagicMock()

    with patch("pyspark.sql.readwriter.DataFrameReader.load", mock_load):
        yield {
            "load": mock_load
        }

@pytest.fixture
def mock_bq_write(spark):
    captured = {}
    # Mock BigQuery writer
    mock_writer = MagicMock()
    mock_writer.format.return_value = mock_writer
    mock_writer.option.return_value = mock_writer
    mock_writer.mode.return_value = mock_writer

    def mock_write(df):
        captured["df"] = df
        return mock_writer

    with patch.object(DataFrame, "write", property(mock_write)):
        yield {
            "writer": mock_writer,
            "captured": captured
        }

@pytest.fixture
def mock_spark_stop(spark):
    with patch.object(spark, "stop") as mock_stop:
        yield {
            "stop": mock_stop
        }


# @pytest.fixture
# def mock_bq(spark):

#     captured = {}

#     # Mock BigQuery writer
#     mock_writer = MagicMock()
#     mock_writer.format.return_value = mock_writer
#     mock_writer.option.return_value = mock_writer
#     mock_writer.mode.return_value = mock_writer

#     def mock_write(df):
#         captured["df"] = df
#         return mock_writer

#     # Mock BigQuery reader
#     mock_load = MagicMock()

#     with patch("pyspark.sql.readwriter.DataFrameReader.load", mock_load), \
#         patch.object(DataFrame, "write", property(mock_write)), \
#         patch.object(spark, "stop") as mock_stop:

#         yield {
#             "load": mock_load,
#             "writer": mock_writer,
#             "captured": captured,
#             "stop": mock_stop
#         }