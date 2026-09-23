"""Statcast 列名マッピングのテスト。"""

import polars as pl

from analysis_project.paths import data_dir
from analysis_project.statcast_columns import (
    rename_statcast_columns,
    statcast_column_rename_summary,
)


def test_rename_maps_all_parquet_columns() -> None:
    path = data_dir() / "external" / "statcast" / "2025_regular.parquet"
    if not path.exists():
        return
    df = pl.read_parquet(path, n_rows=5)
    summary = statcast_column_rename_summary(df)
    assert summary["unmapped_columns"] == []
    assert summary["mapped_count"] == summary["total_columns"]
    ja = rename_statcast_columns(df)
    assert "release_speed" not in ja.columns
    assert "球速_mph" in ja.columns
