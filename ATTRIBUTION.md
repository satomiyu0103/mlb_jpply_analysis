# 出典・改変記録

## ベース

| 項目 | URL |
|---|---|
| Zenn 記事 | [データサイエンティストのためのAGENTS.mdとSkills](https://zenn.dev/green_tea/articles/d310e5cf809190) |
| GitHub リポジトリ | https://github.com/atsushi-green/ds-ai-coding-skills |
| 著者 | atsushi-green (redtea) |

## 改変概要（Cursor 移植）

本テンプレートは upstream を **Cursor** 向けに再配置したものです。

| upstream | 本テンプレート |
|---|---|
| `.github/skills/` | `.cursor/skills/` |
| `.github/Development\RPA_scripts\quest_1\ai-agent-devenv-template\.github\GitHub Copilot エージェント行動規範.md` | `.cursor/rules/ds_core.mdc` |
| `.github/instructions/` | `.cursor/rules/ds_*.mdc` |
| `.github/prompts/` + `.claude/commands/` | `.cursor/skills/*` ワークフロー skills |
| `.claude/skills/` | `.cursor/skills/` に統合 |
| `CLAUDE.md` | `ds_core.mdc` + `AGENTS.md` に統合 |
| `docs/agent/` | `doc/agent/` |
| `validate_agent_docs.py` | Cursor パス用に改修 |
| — | `run_quality_checks.ps1` を新規追加 |
| — | `src/analysis_project/paths.py` を新規追加 |
| upstream 英語文書 | **日本語化**（`AGENTS.md`・`.cursor/rules`・`.cursor/skills`） |

## ライセンス

upstream リポジトリのライセンスに従う。利用・改変時は元リポジトリと記事への言及を推奨。

## 個別 skill の出典

テンプレ内の各 skill の由来・出典性質は [doc/agent/Development/dev_templates/ai-agent-devenv-template/doc/agent/エージェント能力一覧.md](doc/agent/Development/dev_templates/ai-agent-devenv-template/doc/agent/エージェント能力一覧.md) が正本。更新手順: [agent-capabilities-index](.cursor/skills/agent-capabilities-index/SKILL.md)。
