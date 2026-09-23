"""Statcast DataFrame の列名を日本語ラベルに置き換える。"""

from __future__ import annotations

__all__ = [
    "arsenal_report_map_path",
    "load_statcast_column_map",
    "rename_arsenal_report_columns",
    "rename_columns_from_mapping_csv",
    "rename_statcast_columns",
    "statcast_column_map_path",
    "statcast_column_rename_summary",
]

from pathlib import Path

import polars as pl

from analysis_project.paths import data_dir

_COLUMN_MAP_PATH = data_dir() / "interim" / "mappings" / "statcast_column_ja.csv"


def statcast_column_map_path() -> Path:
    """列名マッピング CSV のパス。"""
    return _COLUMN_MAP_PATH


def load_statcast_column_map() -> pl.DataFrame:
    """`statcast_column_ja.csv` を読み込む。"""
    return pl.read_csv(statcast_column_map_path())


def statcast_column_rename_summary(df: pl.DataFrame) -> dict[str, int | list[str]]:
    """列名リネームの適用状況（マッピング漏れの確認用）。

    Returns:
        mapped_count: 日本語ラベルに置換した列数。
        unmapped_columns: CSV に無い英語列名（そのまま残る）。
        total_columns: df の列数。
    """
    column_map = load_statcast_column_map()
    rename_dict = dict(
        zip(
            column_map["column_en"].to_list(),
            column_map["column_ja"].to_list(),
            strict=True,
        )
    )
    unmapped = sorted(set(df.columns) - set(rename_dict.keys()))
    mapped_count = sum(1 for name in df.columns if name in rename_dict)
    return {
        "mapped_count": mapped_count,
        "unmapped_columns": unmapped,
        "total_columns": len(df.columns),
    }


def rename_columns_from_mapping_csv(
    df: pl.DataFrame,
    mapping_path: Path,
    *,
    strict: bool = False,
) -> pl.DataFrame:
    """任意の column_en → column_ja CSV で列名を置換する。"""
    column_map = pl.read_csv(mapping_path)
    rename_dict = dict(
        zip(
            column_map["column_en"].to_list(),
            column_map["column_ja"].to_list(),
            strict=True,
        )
    )
    present = {k: v for k, v in rename_dict.items() if k in df.columns}
    unknown = set(df.columns) - set(rename_dict.keys())
    if strict and unknown:
        missing_in_map = ", ".join(sorted(unknown))
        raise ValueError(f"列名マッピングに無い列があります: {missing_in_map}")
    return df.rename(present)


def arsenal_report_map_path() -> Path:
    """球種別集計レポート用の列名マッピング CSV。"""
    return data_dir() / "interim" / "mappings" / "arsenal_report_columns_ja.csv"


def rename_arsenal_report_columns(df: pl.DataFrame, *, strict: bool = False) -> pl.DataFrame:
    """球種別集計表（report_ja）の列名を日本語化する。"""
    return rename_columns_from_mapping_csv(df, arsenal_report_map_path(), strict=strict)


def rename_statcast_columns(
    df: pl.DataFrame,
    *,
    strict: bool = False,
) -> pl.DataFrame:
    """英語列名を日本語ラベルにリネームして返す（存在する列のみ）。

    Args:
        df: Statcast 1 球 1 行の DataFrame。
        strict: True のとき、マッピングに無い列があれば例外。

    Returns:
        列名を日本語化した DataFrame（値は変更しない）。
    """
    return rename_columns_from_mapping_csv(
        df, statcast_column_map_path(), strict=strict
    )
