# データカタログ

分析で使用するデータセットの一覧です。第 1 分析は [analysis-plan-yamamoto-2025.md](analysis-plan-yamamoto-2025.md) を参照。

## データセット一覧

### Statcast（Baseball Savant）

| 項目 | 内容 |
|------|------|
| パス | `data/external/statcast/{取得日}_{スプリット}.parquet`（例: `20260921_2025_regular.parquet`） |
| 粒度 | 1 行 = 1 球 |
| 更新頻度 | シーズン中は試合後〜日次追加。過去行の修正あり |
| オーナー | MLB / Baseball Savant |
| 機密度 | 公開データ（利用規約・再配布は要確認） |
| 注意点 | pybaseball `statcast(start_dt, end_dt)` で取得。raw は不変。取得日をファイル名に含める |

### MLB Stats API — 投手シーズン成績（レギュラー等）

| 項目 | 内容 |
|------|------|
| パス | `data/raw/mlb_statsapi/{取得日}_pitching_{season}_{gameType}.json`（例: `pitching_2025_regular.json`） |
| 粒度 | 1 エントリ = 投手 × シーズン × `gameType` |
| 更新頻度 | 試合後〜日次 |
| オーナー | MLB |
| 機密度 | 公開 API |
| 注意点 | `GET https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&season=2025&gameType=R&playerPool=QUALIFIED`（全員は `playerPool=ALL`）。順位母集団の正本 |

### Statcast 分析用 DuckDB

| 項目 | 内容 |
|------|------|
| パス | `data/processed/duckdb/mlb_statcast.duckdb`（gitignore） |
| 粒度 | 1 行 = 1 球（Parquet から VIEW または COPY） |
| 更新頻度 | Statcast raw 追加時に再構築または差分 INSERT |
| オーナー | 本リポジトリ（生成物） |
| 機密度 | 公開 Statcast のローカル索引 |
| 注意点 | 設計は [statcast-storage-and-database.md](statcast-storage-and-database.md) |

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
| `person.id` / `personId` | int | MLB Stats API 選手 ID（= MLBAM） | API 成績・Register `key_mlbam` |
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
