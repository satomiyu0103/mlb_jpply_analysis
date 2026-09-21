# データカタログ

分析で使用するデータセットの一覧です。第 1 分析は [analysis-plan-yamamoto-2025.md](analysis-plan-yamamoto-2025.md) を参照。

## データセット一覧

### Statcast（Baseball Savant）

| 項目 | 内容 |
|------|------|
| パス | `data/raw/statcast/{取得日}_{スプリット}.parquet`（例: `20260321_2025_regular.parquet`） |
| 粒度 | 1 行 = 1 球 |
| 更新頻度 | シーズン中は試合後〜日次追加。過去行の修正あり |
| オーナー | MLB / Baseball Savant |
| 機密度 | 公開データ（利用規約・再配布は要確認） |
| 注意点 | pybaseball `statcast(start_dt, end_dt)` で取得。raw は不変。取得日をファイル名に含める |

### FanGraphs 投手成績（シーズン）

| 項目 | 内容 |
|------|------|
| パス | `data/raw/fangraphs/pitching_stats_{season}.parquet` |
| 粒度 | 1 行 = 投手 × シーズン（集計） |
| 更新頻度 | 日次〜試合後（スクレイピング経由） |
| オーナー | FanGraphs |
| 機密度 | 公開（研究利用一般的、大量取得は控える） |
| 注意点 | `pybaseball.pitching_stats(season)`。順位母集団・qual 用 |

### Chadwick Register（選手 ID）

| 項目 | 内容 |
|------|------|
| パス | `data/external/register/chadwick_register.parquet`（初回取得後） |
| 粒度 | 1 行 = 選手 |
| 更新頻度 | 公開版はおおよそ週次 |
| オーナー | Chadwick Bureau |
| 機密度 | 公開 |
| 注意点 | `key_mlbam` が Statcast `pitcher` と結合。由伸の ID 固定に使用 |

### MLB Stats API（JSON）

| 項目 | 内容 |
|------|------|
| パス | `data/raw/mlb_statsapi/{取得日}_{種別}.json`（schedule / boxscore / player_stats 等） |
| 粒度 | エンドポイント依存（試合・選手・成績） |
| 更新頻度 | 試合日はほぼリアルタイム〜試合後 |
| オーナー | MLB |
| 機密度 | 公開 API（非公式ドキュメント、レートに注意） |
| 注意点 | `mlb-statsapi` または `requests`。WS gamePk・公式 W-L の裏取り |

### 加工データ（派生）

| 項目 | 内容 |
|------|------|
| パス | `data/interim/` · `data/processed/` |
| 粒度 | 分析単位に依存（投手×スプリット、投手×球種 等） |
| 更新頻度 | 分析実行時 |
| オーナー | 本リポジトリ |
| 機密度 | 集計のみ（commit 可） |
| 注意点 | raw から生成。上書き方針は Notebook / スクリプトで明示 |

## 主要キー

| キー名 | 型 | 説明 | 備考 |
|--------|-----|------|------|
| `pitcher` | int | Statcast 投手 MLBAM ID | 由伸でフィルタ |
| `key_mlbam` | int | Register 上の MLBAM ID | Statcast と同一 |
| `IDfg` / FanGraphs ID | int | FanGraphs 選手 ID | pitching_stats 結合 |
| `personId` | int | MLB Stats API 選手 ID | API 成績取得 |
| `game_pk` | int | 試合 ID | Statcast と API の突合 |
| `pitch_type` | string | 球種コード | 球種別集計 |

## 主要 Statcast 列（第 1 分析）

| カラム名 | 型 | 説明 | 備考 |
|---------|-----|------|------|
| `game_date` | date | 試合日 | スプリット境界 |
| `release_speed` | float | 球速 | mph |
| `pfx_x`, `pfx_z` | float | 変化量 | 慣例はインチ換算あり |
| `release_spin_rate` | float | スピン | |
| `release_pos_x`, `release_pos_z` | float | リリース位置 | SD 計算 |
| `pitch_type`, `pitch_name` | string | 球種 | マッピング表を interim に |
| `description`, `events` | string | 結果 | Whiff・アウト判定 |
| `plate_x`, `plate_z` | float | コース | 制球 proxy |
| `stand`, `p_throws` | string | 打者/投手の左右 | 配球分析 |

列の正本（英語）: [Savant CSV ドキュメント](https://baseballsavant.mlb.com/csv-docs) · 日本語訳: [Statcast検索CSV列定義.md](reference/Statcast検索CSV列定義.md)
