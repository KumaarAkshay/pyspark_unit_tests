import runpy
from unittest.mock import MagicMock, patch
from pathlib import Path
from pyspark.sql import DataFrame

from tests.utils import read_csv


TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
ASSETS_PATH = TEST_DIR / "Assets" / "read_bq_data_spark"


def test_pyscript(spark):

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

    # Capture the DataFrame being written
    captured = {}

    mock_writer = MagicMock()
    mock_writer.format.return_value = mock_writer
    mock_writer.option.return_value = mock_writer
    mock_writer.mode.return_value = mock_writer

    def mock_write(df):
        captured["df"] = df
        return mock_writer

    # Mock BigQuery reads
    mock_load = MagicMock(
        side_effect=[sample_df1, sample_df2]
    )

    with patch(
        "pyspark.sql.readwriter.DataFrameReader.load",
        mock_load
    ), patch.object(
        DataFrame,
        "write",
        property(mock_write)
    ), patch.object(
        spark,
        "stop"
    ) as mock_stop:

        runpy.run_path(
            str(PROJECT_ROOT / "Scripts" / "read_bq_data_spark.py")
        )

    # Verify BigQuery reads
    assert mock_load.call_count == 2

    # Verify BigQuery write configuration
    mock_writer.format.assert_called_once_with("bigquery")
    mock_writer.mode.assert_called_once_with("overwrite")
    mock_writer.save.assert_called_once()

    # Verify output DataFrame
    actual_df = captured["df"]

    assert actual_df.schema == expected_df.schema
    assert sorted(actual_df.collect()) == sorted(expected_df.collect())

    # Verify Spark stop
    mock_stop.assert_called_once()