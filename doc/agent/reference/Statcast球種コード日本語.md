# Statcast 球種コード（日本語マッピング）

Statcast の `pitch_type`（2 文字コード）を分析・可視化で読みやすくするための対応表。英語正本は MLB の球種分類（Savant / Statcast Search）に準拠する。

| 項目 | 内容 |
|------|------|
| 機械可読 | [`data/interim/mappings/statcast_pitch_type_ja.csv`](../../../data/interim/mappings/statcast_pitch_type_ja.csv) |
| Statcast 列全般 | [Statcast検索CSV列定義.md](Statcast検索CSV列定義.md) |
| 指標（球種別集計） | [metrics-and-definitions.md](../metrics-and-definitions.md) |

## コード一覧

| `pitch_type` | 日本語 | 英語（Savant） | 補足 |
|--------------|--------|----------------|------|
| CH | チェンジアップ | Changeup | 速球より遅い変化球 |
| CS | スローカーブ | Slow Curve | 通常より遅いカーブ |
| CU | カーブ | Curveball | 縦に大きく曲がる変化球 |
| EP | イーファス球 | Eephus | 極端に遅い球 |
| FA | ファストボール | Fastball | 詳細分類前の高速球 |
| FC | カットボール | Cutter | 速球に近い横切れ |
| FF | フォーシーム | Four-Seam Fastball | 一般的な「直球」 |
| FO | フォークボール | Forkball | フォーク系 |
| FS | スプリット | Splitter | スプリットフィンガー |
| KC | ナックルカーブ | Knuckle Curve | ナックル要素のカーブ |
| KN | ナックルボール | Knuckleball | ほぼ無回転 |
| PO | ピッチアウト | Pitchout | 盗塁阻止等の意図的な外角 |
| SC | スクリューボール | Screwball | スクリュー回転 |
| SI | シンカー | Sinker | ツーシーム系・沈む速球 |
| SL | スライダー | Slider | 横に鋭く曲がる |
| ST | スウィーパー | Sweeper | 横に大きく曲がる SL 系 |
| SV | スラーブ | Slurve | SL と CU の中間 |
| UN | 不明 | Unknown | 分類不能 |

## `pitch_name` との関係

同一 `pitch_type` でも `pitch_name`（英語の詳細名）が付く。集計の軸は **本プロジェクトでは `pitch_type` を正** とし、グラフラベルに日本語を付けるときはマッピング表の `pitch_name_ja` を使う。

## polars での結合例

```python
import polars as pl

from analysis_project.paths import data_dir

pitch_map_path = data_dir() / "interim" / "mappings" / "statcast_pitch_type_ja.csv"
pitch_map = pl.read_csv(pitch_map_path)

df_with_ja = df_statcast.join(
    pitch_map.select("pitch_type", "pitch_name_ja"),
    on="pitch_type",
    how="left",
)
```

`pitch_type` が表に無いコードが出たら `pitch_name_ja` は null になる。Footnote で件数を記載する。

## 変更履歴

| 日付 | 内容 |
|------|------|
| 2026-09-23 | 初版（Statcast 主要 18 コード） |
