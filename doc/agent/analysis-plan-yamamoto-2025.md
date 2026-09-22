# 分析計画: 山本由伸（2025 レギュラー基準・WS 偉業）

- **作成日**: 2026-03-21
- **状態**: 計画更新（FanGraphs → MLB Stats API、Statcast は DuckDB）
- **関連**: [analysis-workflow.md](analysis-workflow.md) · [metrics-and-definitions.md](metrics-and-definitions.md) · [data-catalog.md](data-catalog.md)

本書は、2025 年ワールドシリーズにおける山本由伸の偉業をデータで説明するための **第 1 分析** の計画である。チャット（2026-03-21）で整理した目的・手順・成功条件を正本とする。

---

## 1. 目的

2025 年 **レギュラーシーズン** において、山本由伸が MLB 先発投手としてどの位置にいたか（順位・分布）を定量的に示す。そのうえで **ポストシーズン・ワールドシリーズ** における成績・投球内容が、レギュラー比でどう変わったか、および WS 3 勝・投手 MVP としてどこが際立つかをデータで説明する。

### 1.1 分析の3層（混ぜない）

| 層 | 問い | 主データ |
|----|------|----------|
| A. 公式成績 | 勝率・防御率・登板・ポスト結果 | **MLB Stats API**（シーズン投手成績） |
| B. 投球内容 | 球種・球速・制球・打たれ方 | Statcast（pybaseball）→ **DuckDB** でリーグ全体 SQL |
| C. 偉業の文脈 | WS 3 勝・MVP・クリンチ登板 | MLB Stats API ＋ Statcast（日付フィルタ） |

**原則**: 順位・リーグ比較の母集団は **2025 レギュラー先発**。WS は **サンプルが小さい** ため順位ではなく **記録値とレギュラーからの変化** で扱う。

### 1.2 スコープ外（第 1 分析）

- 日本人投手全体の横断比較（将来拡張可）
- 打者視点の詳細分析
- 予測モデル・機械学習による将来成績予測
- 商用再配布を前提としたデータパイプラインの本番運用設計

---

## 2. 背景・動機

2025 年 MLB ワールドシリーズで 3 勝を挙げ、投手として MVP を獲得した山本由伸のプレーをきっかけに、**すごさをデータの視点で理解したい** という利用者ニーズがある。本計画はその第 1 段階として、再現可能な取得・指標・可視化までを定義する。

---

## 3. 期間・スプリット

| スプリット | 用途 | raw 保存の目安 |
|------------|------|----------------|
| **2025 レギュラー** | 順位・リーグ比較の基準 | `data/external/statcast/2025_regular.parquet` 等 |
| **2025 ポスト** | レギュラー比の変化（LDS/LCS/WS 含む） | `data/external/statcast/2025_post.parquet` |
| **2025 WS のみ** | 偉業の詳細（3 勝・登板内容） | 同上＋ API JSON |

日付境界は取得時に MLB 公式スケジュールで確認する。Statcast は **後から修正** されるため、再取得したときは **コミットメッセージまたは notebook 実行日** で取得日を残す（ファイル名はスプリット固定）。

---

## 4. 分析単位（粒度）

| 分析 | 1 行が表すもの | 由伸の集計 |
|------|----------------|------------|
| 投手成績 | 投手 × シーズン × スプリット | 由伸 × 2025 × レギュラー 等 |
| 順位 | 指標 × スプリット × 母集団内順位 | 由伸の順位は 1 点、分布は全先発 |
| 球種別 | 投手 × 球種 × スプリット | 由伸 × FF 等 × 2025 レギュラー |
| Statcast 生 | 1 球 | フィルタ後に集計 |

**勝ち星数**（例: WS 3 勝）は **勝率と別列** で扱う。指標定義は [metrics-and-definitions.md](metrics-and-definitions.md) を正とする。

---

## 5. データソース

| ソース | 取得手段 | 用途 |
|--------|----------|------|
| Statcast / Baseball Savant | `pybaseball.statcast` | 1 球・球種・物理・結果（raw Parquet） |
| MLB Stats API | `GET /api/v1/stats` 等 | **シーズン投手成績・母集団順位**（`gameType=R`, `group=pitching`, `playerPool=QUALIFIED` / `ALL`） |
| Chadwick Register | `pybaseball.chadwick_register` / `playerid_lookup` | MLBAM ↔ 名前（FG ID は参照のみ） |
| MLB Stats API | `mlb-statsapi` / `requests` | schedule、boxscore、WS gamePk、公式 W-L |
| DuckDB | `duckdb`（ローカル `.duckdb`） | Statcast 全投手・リーグ集計 SQL（[statcast-storage-and-database.md](statcast-storage-and-database.md)） |
| 列定義 | [Savant CSV ドキュメント](https://baseballsavant.mlb.com/csv-docs) · [Statcast検索CSV列定義.md](reference/Statcast検索CSV列定義.md) | 列の意味確認 |

詳細パス・更新頻度は [data-catalog.md](data-catalog.md) を参照。

### 5.1 保存ポリシー

- `data/raw/`・`data/external/` は **不変**（上書きしない）
- 加工結果は `data/interim/` → `data/processed/`
- 図表は `outputs/figures/`・`outputs/tables/`
- raw を git に commit しない

---

## 6. 主要指標

第 1 分析で用いる指標の一覧。定義の全文は [metrics-and-definitions.md](metrics-and-definitions.md)。

### 6.1 レギュラー先発成績（順位の主役）

ERA、WHIP、**勝率**（勝/(勝+敗)）、K%、BB%、K-BB%、IP、**派生 FIP**（MLB API の HR/BB/K/IP から計算。定数は metrics に明記）。**xFIP・fWAR は第 1 分析の順位から除外**（FG 非利用）。CSW% 等の詳細は Statcast（DuckDB）から算出。

### 6.2 球種・Statcast（順位 or パーセンタイル）

球種別使用率、Whiff%、**球種別打席終了アウト率**、リリース位置 SD（球種別）、必要に応じ release_speed・変化量のパーセンタイル。

### 6.3 偉業・WS（順位は原則作らない）

WS 勝利数、WS 登板・防御率・WHIP、レギュラー同一指標との並列表。

---

## 7. 母集団（「MLB 先発」の定義）

| 項目 | 定義 |
|------|------|
| 対象 | 2025 MLB レギュラーシーズンの **先発投手** |
| 規定 | MLB Stats API `playerPool=QUALIFIED` を優先。全員比較は `ALL`＋metrics の最低 IP（例: 100）で脚注 |
| 除外 | 救援のみ、極端に少ない IP |
| ポスト | 順位母集団に **含めない**（IP 不足） |

---

## 8. 成功条件（完了定義）

| # | 条件 | 検証 |
|---|------|------|
| 1 | 由伸の ID 固定（MLBAM = API `person.id`） | Register 突合表 |
| 2 | 2025 レギュラー Statcast 取得 | raw 行数・日付・pitcher 唯一 |
| 3 | 2025 ポスト＋ WS Statcast 取得 | WS 試合日を含む |
| 4 | MLB API 2025 レギュラー投手成績 JSON 取得 | QUALIFIED 人数・由伸含有 |
| 4b | Statcast を DuckDB に載せる | 行数・`pitcher` ユニーク数・由伸球数 |
| 5 | 指標定義が metrics に記載 | レビュー |
| 6 | **レギュラー指標の順位可視化** | 分布＋由伸位置（複数指標） |
| 7 | 球種・Statcast 系の順位 or パーセンタイル可視化 | 同上 |
| 8 | 既知事実と矛盾なし | WS 3 勝・MVP 方向、ERA オーダー |
| 9 | 限界の明記 | WS n 小、定義差、Statcast 修正 |
| 10 | 再現可能 | Notebook Restart & Run All または papermill |

---

## 9. 可視化・成果物

### 9.1 図の型

1. リーグ分布＋由伸（ヒストグラム / 箱ひげ＋マーカー）
2. 指標ごとの順位バー（同順位は帯で表現）
3. パーセンタイル一覧表
4. レギュラー vs ポスト/WS の同指標比較（**順位なし**）

### 9.2 出力先

| 種類 | パス |
|------|------|
| 図 | `outputs/figures/2025_yamamoto_*` |
| 表 | `outputs/tables/2025_yamamoto_*` |
| 短文サマリー | `outputs/reports/`（任意） |

### 9.3 Notebook 分割（推奨）

| Notebook | 内容 |
|----------|------|
| `001_yamamoto_ids_and_fetch.ipynb` | ID・raw 取得 |
| `002_yamamoto_regular_ranks.ipynb` | レギュラー順位可視化 |
| `003_yamamoto_pitch_types.ipynb` | 球種・Statcast |
| `004_yamamoto_post_ws_story.ipynb` | ポスト・WS・偉業 |

探索用の `test_eda.ipynb` は上記に統合またはリネームする。

---

## 10. EDA・分析手順（ベストプラクティス）

```text
0. 目的・粒度・スプリットを Notebook 先頭に記載
1. データ取得 → data/raw（日付付き、不変）
2. DataFrame 化（pybaseball → polars 優先）
3. 理解（スキーマ・欠損・キー・既知事実）
4. 可視化（探索）
5. 整形（フィルタ・球種マップ・集計）
6. 再可視化（問いへの回答・順位）
7. 特徴量（必要時のみ）
8. サマリー・outputs/ 保存・src/ へ共通化
```

---

## 11. リスクと対策

| リスク | 対策 |
|--------|------|
| WS のみで順位を語る | 順位はレギュラーのみ |
| 勝率と勝ち星の混同 | 列分離・metrics 定義 |
| 球種アウト率の定義ブレ | PA 終了球ベースで固定 |
| Statcast 後日修正 | 再取得手順と取得日をコミット／memory_stream に記録 |
| 大量 API 取得 | 期間分割・キャッシュ・間隔 |
| API と Savant の定義差（PA vs BF 等） | 表に出典列・metrics 脚注 |
| FanGraphs 403 | **計画から除外**（MLB API に一本化） |

---

## 12. 実装フェーズ

| Phase | 内容 |
|-------|------|
| 0 | metrics / data-catalog 更新（本計画と整合） |
| 1 | ID 固定・raw 取得（Statcast レギュラー/ポスト → MLB API 投手成績 → API WS）・DuckDB 構築 |
| 2 | EDA・既知事実チェック |
| 3 | レギュラー成績順位の表・図 |
| 4 | 球種・Statcast 順位 / パーセンタイル |
| 5 | ポスト・WS ストーリー（3 勝タイムライン含む） |
| 6 | `src/analysis_project/` への抽出・quality checks |

---

## 13. 検証

- MLB Stats API の WS 登板・勝敗と Statcast の試合日・game_pk の一致
- MLB API 由伸 2025 レギュラー ERA / W-L と公開記録の方向性一致
- 母集団人数が API `QUALIFIED` と整合（`ALL` 使用時は脚注）
- DuckDB 集計の由伸 K% と API 由来 K% が大きく乖離しないこと（定義差は脚注）

---

## 14. 依存パッケージ（取得レイヤー）

`pyproject.toml` に含める想定: `pybaseball`, `requests`, `mlb-statsapi`, `polars`, `duckdb`, `matplotlib`, `japanize-matplotlib` 等。分析本体は polars を優先し、リーグ全体 SQL は DuckDB。

---

## 15. 変更履歴

| 日付 | 内容 |
|------|------|
| 2026-03-21 | 初版（チャット要約・計画確定） |
| 2026-09-22 | FanGraphs 廃止・MLB Stats API 成績に変更。Statcast は DuckDB 分析層を追加 |
