import runpy
from unittest.mock import MagicMock, patch
from pathlib import Path
from pyspark.sql import DataFrame
from tests.utils import read_csv


TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
ASSETS_PATH = TEST_DIR / "Assets" / "read_bq_data_spark"

def test_pyscript(spark,mock_bq_write,mock_bq_read,mock_spark_stop):

    sample_df1 = read_csv(
        spark,
        ASSETS_PATH / "read_bq_data.csv"
    )
    sample_df2 = read_csv(
        spark,
        ASSETS_PATH / "read_bq_data_2.csv"
    )
    expected_df = read_csv(
        spark,
        ASSETS_PATH / "expected_output.csv"
    )

    # Configure BigQuery mock responses
    mock_bq_read["load"].side_effect = [sample_df1,sample_df2]

    # Execute production script
    runpy.run_path(
        str(PROJECT_ROOT / "Scripts" / "read_bq_data_spark.py")
    )

    # Verify BigQuery reads
    assert mock_bq_read["load"].call_count == 2

    # Verify BigQuery write configuration
    mock_bq_write["writer"].format.assert_called_once_with("bigquery")
    mock_bq_write["writer"].mode.assert_called_once_with("overwrite")
    mock_bq_write["writer"].save.assert_called_once()

    # Verify output DataFrame
    actual_df = mock_bq_write["captured"]["df"]

    assert actual_df.schema == expected_df.schema
    assert sorted(actual_df.collect()) == sorted(expected_df.collect())

    # Verify Spark stop
    mock_spark_stop["stop"].assert_called_once()