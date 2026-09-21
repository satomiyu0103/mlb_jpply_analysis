# doc/research

External research notes for this project.
Normative definitions live in `doc/agent/` (analysis plans, metrics, data catalog).

## Folder map

| Folder | Purpose (JA) |
|--------|----------------|
| `mlb-calendar/` | MLB schedule, season boundaries, postseason rounds, major events |
| `baseball-general/` | Rules, terminology, league structure (not yet populated) |
| `pitching/` | Pitcher-focused background research (not yet populated) |
| `position-players/` | Hitter and fielder research (not yet populated) |
| `other/` | Data sources, APIs, cross-cutting topics |

## Naming rule

Research files use Japanese titles with a date prefix:

`YYYY-MM-DD_{日本語トピック}.md`

Contract files such as this README stay in English.

## Promotion to `doc/agent/`

When dates or definitions are confirmed, copy **only the facts** (e.g. split boundaries) into `doc/agent/`.
Do not delete research files; keep URLs and investigation history here.

## Index

| Researched | Folder | File | Summary | Promoted to agent |
|------------|--------|------|---------|-------------------|
| 2026-09-21 | `mlb-calendar/` | [2026-09-21_2025年MLB日程とシーズン区分.md](mlb-calendar/2026-09-21_2025年MLB日程とシーズン区分.md) | 2025 regular/post/WS dates, events, split filters | N |
| 2026-09-21 | `other/` | [2026-09-21_Statcastの試合種別とスプリット.md](other/2026-09-21_Statcastの試合種別とスプリット.md) | Savant `game_type` codes vs analysis splits | N |
