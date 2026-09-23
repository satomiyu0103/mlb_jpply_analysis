# Statcast DataFrame（`df_statcast` 等）列ガイド

Notebook や分析コードで `df_statcast`・`sc_regular`・`sc_post` などと名付ける **1 球 1 行の polars DataFrame** を指す。中身は `pybaseball.statcast` の取得結果を `data/external/statcast/*.parquet` に保存したものと同一スキーマである。

## 列説明はどこにあるか

| 用途 | 文書 |
|------|------|
| **全列の日本語説明（正本）** | [reference/Statcast検索CSV列定義.md](reference/Statcast検索CSV列定義.md) |
| **列名の日本語ラベル（機械可読）** | `data/interim/mappings/statcast_column_ja.csv` · `rename_statcast_columns()`（[statcast_columns.py](../../src/analysis_project/statcast_columns.py)） |
| **`pitch_type` の日本語** | [reference/Statcast球種コード日本語.md](reference/Statcast球種コード日本語.md) |
| 英語正本（MLB） | [Statcast Search CSV Documentation](https://baseballsavant.mlb.com/csv-docs) |
| データ配置・主要キー・第 1 分析でよく使う列 | [data-catalog.md](data-catalog.md) の Statcast 節 |
| 試合種別 `game_type` とスプリット | [../research/other/2026-09-21_Statcastの試合種別とスプリット.md](../research/other/2026-09-21_Statcastの試合種別とスプリット.md) |

`df_statcast` 専用の別スキーマはない。上記「Statcast 検索 CSV 列定義」が列意味の日本語正本である。

## 本リポジトリ Parquet の列数

`data/external/statcast/2025_regular.parquet`（pybaseball 経由・2026-09 時点の取得分）では **119 列**。再取得後に列が増減する場合がある。確認コマンド:

```python
import polars as pl
from analysis_project.paths import data_dir

path = data_dir() / "external" / "statcast" / "2025_regular.parquet"
sorted(pl.read_parquet(path).columns)
```

## pybaseball / Parquet で Savant ドキュメントと異なる列名

Savant の csv-docs では `release_spin`・`hit_distance` と書かれることが多い。本プロジェクトの Parquet では次の名前が使われる。

| Parquet / pybaseball | csv-docs 上の対応 | 説明 |
|----------------------|-------------------|------|
| `release_spin_rate` | `release_spin` | リリース時回転数（rpm） |
| `hit_distance_sc` | `hit_distance` | 打球の推定飛距離（フィート） |

意味の詳細は [Statcast検索CSV列定義.md](reference/Statcast検索CSV列定義.md) の該当行（または `release_spin` / `hit_distance` の説明）を参照する。

## Parquet にあって列定義表へ追記した列

Bat Tracking 等で csv-docs 更新後に Parquet に載る列。説明は [Statcast検索CSV列定義.md](reference/Statcast検索CSV列定義.md) に追記済み。

| 列名 | 要約 |
|------|------|
| `post_fld_score` | ピッチ後の守備側得点 |
| `bat_speed` | スイートスポットでのバット速度（mph） |
| `swing_length` | スイング開始から接触までバットヘッドの移動距離（フィート） |
| `miss_distance` | スイングと球のミス距離（インチ） |
| `estimated_slg_using_speedangle` | 初速・角度に基づく推定長打率 |
| `delta_pitcher_run_exp` | ピッチ前後の投手視点得点期待値の変化 |

## Notebook での読み込み例

```python
import polars as pl
from analysis_project.paths import data_dir

df_statcast = pl.read_parquet(
    data_dir() / "external" / "statcast" / "2025_regular.parquet"
)
```

列名を日本語にした表示用 DataFrame（値はそのまま）:

```python
from analysis_project.statcast_columns import rename_statcast_columns

df_statcast_ja = rename_statcast_columns(df_statcast)
```

スプリットごとに別 DataFrame（`sc_regular` / `sc_post`）に分けてもよい。列定義は同じである。

## 変更履歴

| 日付 | 内容 |
|------|------|
| 2026-09-23 | 初版（`df_statcast` 入口・pybaseball 列名差・Parquet 列数） |
