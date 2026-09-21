# Statcast 保管と分析用 DB 選定

- **作成日**: 2026-09-22
- **関連**: [analysis-plan-yamamoto-2025.md](analysis-plan-yamamoto-2025.md) · [data-catalog.md](data-catalog.md)

本書は、リーグ全体 Statcast（1 球粒度）を **ローカルで再現可能に分析** するための DB 候補比較と、本プロジェクトの推奨構成を定める。

---

## 1. データ量の見積もり（2025・本リポジトリ実測ベース）

| スプリット | 行数（概算） | Parquet サイズ（概算） |
|------------|-------------|------------------------|
| レギュラー | 約 74 万行 | 約 97 MB |
| ポスト | 約 1.4 万行 | 約 2 MB |

列数は Statcast 全列（100 列前後）を想定。複数年・全打者を足しても **単一シーズン・投手分析では 1 GB 未満** が当面の上限。クラウド無料枠の主な制約は「容量」より **運用・認証・アップロード手間** になる。

---

## 2. 選定条件（利用者要件）

| 条件 | 解釈 |
|------|------|
| 無料または無料範囲 | ライセンス無料の OSS、または恒常的な無料枠で本分析が収まる |
| メジャー | 採用実績・文献・求人・チュートリアルが多く、単独利用者でも情報が得やすい |

---

## 3. 候補比較（5 案）

### 3.1 一覧

| 候補 | コスト | メジャー度（本用途） | Statcast 適性 | 要約 |
|------|--------|---------------------|---------------|------|
| **DuckDB**（ローカル `.duckdb`） | 無料 OSS | ◎（分析 Python 界隈で標準級） | ◎ 列指向・Parquet 直読 | **推奨** |
| **SQLite**（`.sqlite`） | 無料 OSS | ◎（最も普及） | △ 行指向・広表の集計は遅め | 小規模・学習用 |
| **PostgreSQL**（ローカル / Docker） | 無料 OSS | ◎（業務 DB のデファクト） | ○ インデックス・SQL 豊富 | 将来マルチユーザーなら有力 |
| **Google BigQuery**（無料枠） | 無料枠あり※ | ◎（クラウド DW） | ○ 大規模向き | 公開 MLB BQ は古い・自前ロードは手間 |
| **MotherDuck**（DuckDB クラウド） | 無料枠あり※ | △〜○ | ◎ DuckDB 互換 | 共有・クラウド要否で判断 |

※ BigQuery: ストレージ・クエリに月次無料枠（政策変更あり。公式 Pricing を都度確認）。MotherDuck: 無料ティアは容量・同時実行に上限。

### 3.2 DuckDB（推奨）

| 項目 | 内容 |
|------|------|
| 強み | `read_parquet()` / 外部テーブルで **raw を複製せず** SQL 可能。Window・GROUP BY・JOIN が高速。Polars ↔ DuckDB 連携が容易 |
| 弱み | 本番 OLTP・高 concurrent 書込は向かない（本分析は読み取り中心で問題なし） |
| 無料 | Apache 2.0。クラウド不要 |
| 本プロジェクト | `data/processed/duckdb/mlb_statcast.duckdb`（gitignore）。必要列だけマテリアライズするテーブルも可 |

### 3.3 SQLite

| 項目 | 内容 |
|------|------|
| 強み | Python 標準同梱感、単一ファイル、ツールが everywhere |
| 弱み | 70 万行 × 100 列の **全表スキャン集計** は DuckDB より遅いことが多い。Parquet は拡張経由 |
| 無料 | Public domain |
| 向くケース | 既に SQLite しか使えない環境、行数が 10 万未満のサブセットのみ |

### 3.4 PostgreSQL

| 項目 | 内容 |
|------|------|
| 強み | エコシステム最大級、制約・権限・複数クライアント、本番移行の慣れ |
| 弱み | ローカルセットアップ（サービス or Docker）の手間。単独分析 laptop では **オーバーヘッド** |
| 無料 | OSS（ローカル） |
| 向くケース | チーム共有 DB、API バックエンドと同一 DB にしたい将来 |

### 3.5 Google BigQuery

| 項目 | 内容 |
|------|------|
| 強み | ペタ規模、SQL 分析、Looker 等連携 |
| 弱み | `bigquery-public-data.baseball` の Statcast は **2016 年止まり**（2025 は自前ロード）。GCP プロジェクト・課金アラート管理 |
| 無料枠 | 小〜中規模分析は収まることが多いが、**本件はローカル Parquet の方が単純** |
| 向くケース | 複数年・全リーグをチームで常時クエリ、既に GCP 標準 |

### 3.6 MotherDuck

| 項目 | 内容 |
|------|------|
| 強み | DuckDB 互換 SQL、ノートブックからクラウドへオフロード |
| 弱み | アカウント・ネットワーク依存、無料枠超過時の判断 |
| 向くケース | ローカル RAM が厳しい、ノートブック共有先を 1 つにしたい |

---

## 4. ベストプラクティス（本プロジェクト採用案）

### 4.1 レイヤー（メダリオンと整合）

```text
data/external/statcast/*.parquet   … 不変 raw（取得日付きファイル名）
        ↓
DuckDB: VIEW statcast_pitches AS SELECT * FROM read_parquet('.../*.parquet')
        または
        TABLE statcast_pitches（初回 COPY、以降はスプリット追加時のみ INSERT）
        ↓
data/processed/  … 投手×球種×スプリット等の集計 Parquet（commit 可・小さい）
```

- **raw Parquet は正本**。DB はクエリ用の「索引付きコピー」または「ビュー」に留める。
- DB ファイルは **gitignore**（`data/processed/duckdb/`）。

### 4.2 スキーマ・キー

| 列 | 用途 |
|----|------|
| `pitcher` | 投手 MLBAM。由伸 808967 フィルタ |
| `game_date`, `game_pk` | スプリット・API 突合 |
| `pitch_type`, `batter` | 球種・打者分析 |
| `events`, `description` | Whiff・PA 終了判定（実装固定） |

全 100 列を DB に入れてよい（ディスク余裕あり）。不要になった列は VIEW で投影してもよい。

### 4.3 インデックス（マテリアライズテーブル時）

DuckDB では `CREATE INDEX idx_pitcher ON statcast_pitches(pitcher)` 等、**フィルタ列**（`pitcher`, `game_date`, `game_pk`）を優先。ビューのみ Parquet 直読の場合はファイルレイアウトとパーティション（将来: 年・game_type 別ファイル）で十分なことが多い。

### 4.4 分析フロー

1. Notebook / `src/` から `duckdb.connect(path)` または `pl.read_database`
2. リーグ全体 SQL（CSW%、球種別集計、パーセンタイル用分布）
3. 結果を `outputs/tables/` と小さい `data/processed/` に書き出し
4. 可視化は polars/matplotlib（既存規約）

### 4.5 依存

`pyproject.toml` に **`duckdb`** を追加（Phase 1 実装時）。SQLite は標準ライブラリのため追加不要だが、本件では第一選択にしない。

---

## 5. 決定

| 項目 | 決定 |
|------|------|
| 分析用 DB | **DuckDB（ローカルファイル）** |
| 代替（将来） | チーム共有が必要になったら PostgreSQL へ ETL、または MotherDuck |
| 採用しない（第 1 分析） | BigQuery 自前ロード（コスト・運用対効果が低い）、SQLite 全量（性能・Parquet 連携） |

---

## 6. 変更履歴

| 日付 | 内容 |
|------|------|
| 2026-09-22 | 初版（候補比較・DuckDB 推奨） |
