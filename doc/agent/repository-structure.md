# リポジトリ構成

各ディレクトリの役割を説明します。

| ディレクトリ | 役割 |
|-------------|------|
| `src/analysis_project/` | 再利用可能なPythonモジュール |
| `notebooks/` | 探索・分析用Jupyter Notebook |
| `scripts/` | CI・検証用スクリプト |
| `tests/` | pytest用テスト |
| `data/raw/` | 元データ（不変・gitignore対象） |
| `data/external/` | 外部データ（不変・gitignore対象） |
| `data/interim/` | 中間加工データ |
| `data/processed/` | 最終加工データ |
| `outputs/figures/` | グラフ・図 |
| `outputs/tables/` | 集計テーブル |
| `outputs/reports/` | レポート |
| `doc/agent/` | エージェント向けプロジェクト文書（分析計画・指標等。一部は gitignore） |
| `doc/agent/reference/` | 外部ツール・ライブラリの使い方リファレンス |
| `doc/research/` | 外部調査メモ（調査ファイルは日本語ファイル名、索引は README） |
| `.cursor/` | ローカルの Cursor 設定（skills / rules）。**gitignore・push 対象外** |
| `doc/初心者ガイド.md` | データサイエンス初心者向けの使い方 |
