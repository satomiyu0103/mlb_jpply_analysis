# MLB 日本選手データ分析（mlb_jpply_analysis）

MLB で活躍する日本人選手のデータ分析プロジェクト。第 1 テーマは [山本由伸（2025）の分析計画](doc/agent/analysis-plan-yamamoto-2025.md)。

> **はじめての方**: [doc/初心者ガイド.md](doc/初心者ガイド.md)

## 含まれるもの

| パス | 内容 |
|------|------|
| `doc/agent/` | 分析計画・指標定義・データカタログ |
| `notebooks/` | 探索用 Jupyter Notebook |
| `src/analysis_project/` | 再利用可能な Python モジュール |
| `scripts/` | 品質チェック（raw データ・秘密情報の検証） |
| `data/` / `outputs/` | データと成果物の配置（raw は git 対象外） |

Cursor の rules / skills（`.cursor/`）は **gitignore** しており、リポジトリには含めません（ローカル開発用）。

## スタック

- Python 3.11+
- uv（パッケージ管理）
- polars / pybaseball / MLB-StatsAPI
- pytest / ruff / mypy

## セットアップ

```powershell
uv sync
powershell -File scripts/run_quality_checks.ps1
```

## 出典

| 種別 | リンク |
|------|--------|
| テンプレ由来 | [atsushi-green/ds-ai-coding-skills](https://github.com/atsushi-green/ds-ai-coding-skills) |
| 改変記録 | [`ATTRIBUTION.md`](ATTRIBUTION.md) |
| Statcast 列定義（日本語） | [`doc/agent/reference/Statcast検索CSV列定義.md`](doc/agent/reference/Statcast検索CSV列定義.md) |
| Statcast 球種コード（日本語） | [`doc/agent/reference/Statcast球種コード日本語.md`](doc/agent/reference/Statcast球種コード日本語.md) |
