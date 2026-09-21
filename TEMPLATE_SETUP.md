# DS 分析テンプレート — セットアップガイド

このテンプレートは **Cursor** 向けのデータ分析プロジェクト雛形です。  
正本: `dev_templates/ds-analysis-template/`（Documents ワークスペース内）

---

## 含まれるファイル

```
.cursor/
  rules/          … ds_core + パス別 rules
  skills/         … 作業別 10 + ワークフロー 7 + Agentic セキュリティ 4
AGENTS.md
DESIGN.md         … デザイン正本（図・スライドの色・トーン）
skills-lock.json  … OWASP 防御系 skills の出典・ハッシュ（更新時は手動コピー or npx skills experimental_install）
doc/agent/        … プロジェクト文脈
doc/design/       … ai-design-brief（依頼手順）・design-refs（参考）
src/analysis_project/
data/ outputs/ notebooks/ scripts/ tests/
pyproject.toml
```

**意図的に含めないもの**: `ai-agent-devenv-template` の Phase skills・`template_sync`・`doc/specs/` ライフサイクル

---

## A. 新規 DS プロジェクトの作成

### 1. テンプレートをコピーする

```powershell
$src = "Documents\dev_templates\ds-analysis-template"
$dest = "Documents\Data_Science\my_new_project"
Copy-Item -Recurse $src $dest
```

### 2. プレースホルダーを置換する

| プレースホルダー | 置換内容 | 例 |
|---|---|---|
| `{{APP_PACKAGE}}` | `src/` 配下のパッケージ名 | `my_analysis` |
| `{{PROJECT_DESCRIPTION}}` | 1 行概要 | `売上予測分析` |

置換対象:

- `pyproject.toml` の `name` と `[tool.hatch.build.targets.wheel] packages`
- `src/analysis_project/` ディレクトリ名
- skill 内の `from analysis_project.paths import ...` 参照
- `doc/agent/Development/dev_templates/web-static-template/doc/agent/プロジェクト概要.md`

### 3. プロジェクト文脈を埋める

- `doc/agent/Development/dev_templates/web-static-template/doc/agent/プロジェクト概要.md`
- `doc/agent/data-catalog.md`
- `doc/agent/metrics-and-definitions.md`

### 4. 環境構築と検証

```powershell
cd Data_Science\my_new_project
uv sync
uv run python scripts/validate_agent_docs.py
powershell -File scripts/run_quality_checks.ps1
```

### 5. データ配置

- 生データ: `data/raw/`（gitignore 対象・不変）
- 外部参照: `data/external/`
- 加工データ: `data/interim/` / `data/processed/`
- 図表・レポート: `outputs/`

### 5b. 図・プレゼンのデザイン（任意）

1. [doc/design/doc/life/playbook/AIデザイン依頼手順書.md](doc/design/doc/life/playbook/AIデザイン依頼手順書.md) でトーン・配色を選ぶ（§7 カラー、パワポ節）
2. ルートの [DESIGN.md](DESIGN.md) にパレットを転記
3. 図の実装は [visualization](.cursor/skills/visualization/SKILL.md) skill に従う

### 6. Agentic セキュリティ skills の更新（任意）

テンプレ同梱の OWASP 防御系 skills（`agent-governance` 等）は `skills-lock.json` で出典を固定している。正本から更新する場合:

```powershell
# グローバルに入っている場合は手動コピー（ESET 誤検知を避ける）
$src = "$env:USERPROFILE\.agents\skills"
Copy-Item -Recurse -Force "$src\agent-governance" ".cursor\skills\agent-governance"
# 他 skill も同様。または lock がある場合:
npx skills experimental_install
```

攻撃プレイブック系 repo（例: `yaklang/hack-skills`）は ESET 誤検知のため **導入しない**。ASI01 は `agent-owasp-compliance`・`llm-security` でカバーする。

---

## B. 既存プロジェクトへの段階導入

既存の `Data_Science/` プロジェクト（例: `analysis_titanic`）には、一括置換ではなく **skills のみ** から導入する。

1. `.cursor/skills/` から必要な skill をコピー（推奨: `visualization`, `safe-data-handling`, `dataframe-polars`）
2. 既存 `agent_core.mdc` は維持（CHANGELOG 義務など）
3. `outputs/` ディレクトリを追加
4. 新規コードから polars を使用。既存 pandas notebook はそのまま

---

## C. ワークフロー skills の使い方

Cursor チャットで明示的に依頼する:

- 「plan-analysis skill に従って分析計画を作って」
- 「run-eda skill で `data/raw/...` の EDA を実装して」
- 「summarize-analysis skill で結果をまとめて」

---

## 検証

```powershell
uv run python scripts/validate_agent_docs.py
powershell -File scripts/run_quality_checks.ps1
```

---

## ai-agent-devenv-template との使い分け

| テンプレ | 用途 |
|---|---|
| `ai-agent-devenv-template` | 汎用アプリ開発・specs ライフサイクル |
| `ds-analysis-template` | データ分析・EDA・モデリング |

混在させない。DS プロジェクトに Phase 1〜3 skills を入れない。
