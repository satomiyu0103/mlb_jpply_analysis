# Statcast 検索 CSV 列定義

Statcast Search からダウンロードする CSV の列説明の **日本語訳** です。定義の正本は MLB 公式の英語ページです。

| 項目 | 内容 |
|------|------|
| 英語正本 | [Statcast Search CSV Documentation](https://baseballsavant.mlb.com/csv-docs) |
| 翻訳基準日 | 2026-03-21 |
| 利用上の注意 | 列名・定義は MLB 側で変更される場合がある。分析前に正本を確認する |

---

## 概要

Baseball Savant の Statcast Search で取得する CSV データの各列の意味を示す。1 行は原則 **1 球**（ピッチ）に対応する。

---

## 列一覧（CSV カラム）

### 試合・状況

| 列名 | 日本語説明 |
|------|------------|
| `game_date` | 試合日 |
| `game_year` | 試合が行われた年 |
| `game_pk` | 試合を一意に識別する ID |
| `game_type` | 試合種別。E=エキシビション、S=春季キャンプ、R=レギュラーシーズン、F=ワイルドカード、D=地区シリーズ、L=リーグチャンピオンシップシリーズ、W=ワールドシリーズ |
| `home_team` | ホームチームの略称 |
| `away_team` | アウェイチームの略称 |
| `inning` | ピッチ前のイニング |
| `inning_topbot` | ピッチ前の表（Top）か裏（Bot）か |
| `outs_when_up` | ピッチ前のアウト数 |
| `at_bat_number` | 試合内の打席通算番号 |
| `pitch_number` | 当該打席内のピッチ通算番号 |

### 選手・ID

| 列名 | 日本語説明 |
|------|------------|
| `player_name` | 検索条件に紐づく選手名（当該プレーイベント） |
| `pitcher` | プレーイベントに紐づく投手の MLB 選手 ID |
| `batter` | プレーイベントに紐づく打者の MLB 選手 ID |
| `p_throws` | 投手の投球腕（右/左） |
| `stand` | 打者の打席側（右/左） |
| `fielder_2` | ピッチ前の捕手の MLB 選手 ID |
| `fielder_3` | ピッチ前の一塁手の MLB 選手 ID |
| `fielder_4` | ピッチ前の二塁手の MLB 選手 ID |
| `fielder_5` | ピッチ前の三塁手の MLB 選手 ID |
| `fielder_6` | ピッチ前の遊撃手の MLB 選手 ID |
| `fielder_7` | ピッチ前の左翼手の MLB 選手 ID |
| `fielder_8` | ピッチ前の中堅手の MLB 選手 ID |
| `fielder_9` | ピッチ前の右翼手の MLB 選手 ID |
| `on_1b` | ピッチ前の一塁走者の MLB 選手 ID |
| `on_2b` | ピッチ前の二塁走者の MLB 選手 ID |
| `on_3b` | ピッチ前の三塁走者の MLB 選手 ID |
| `age_pit_legacy` | 投手年齢（6/30 時点・旧定義） |
| `age_bat_legacy` | 打者年齢（6/30 時点・旧定義） |
| `age_pit` | 投手年齢（12/31 時点） |
| `age_bat` | 打者年齢（12/31 時点） |
| `n_thruorder_pitcher` | 投手が打順を何周目か |
| `n_priorpa_thisgame_player_at_bat` | 当該打者のこの試合での prior 打席数 |
| `pitcher_days_since_prev_game` | 投手の前試合からの日数 |
| `batter_days_since_prev_game` | 打者の前試合からの日数 |
| `pitcher_days_until_next_game` | 投手の次試合までの日数 |
| `batter_days_until_next_game` | 打者の次試合までの日数 |

### 球種・投球物理

| 列名 | 日本語説明 |
|------|------------|
| `pitch_type` | Statcast から導出した球種コード |
| `pitch_name` | Statcast データから導出した球種名 |
| `release_speed` | 球速（mph）。2008–2016 は PitchFX 由来でリリース付近に調整。2017 以降は Statcast の手元リリース基準。いずれも同一スケール |
| `effective_speed` | 投手のリリース延伸（extension）を踏まえた換算球速 |
| `release_spin` | Statcast が計測した回転数（rpm） |
| `release_spin_rate` | 上記と同義。pybaseball / 本リポジトリ Parquet の列名 |
| `spin_axis` | 2D X–Z 平面での回転軸（0–360°）。180°=真後ろ回転（ストレート系）、0°=真上回転（12–6 カーブ系） |
| `release_extension` | Statcast 計測のリリース延伸（フィート） |
| `release_pos_x` | 捕手視点の水平リリース位置（フィート） |
| `release_pos_y` | 捕手視点のリリース位置（フィート・奥行） |
| `release_pos_z` | 捕手視点の垂直リリース位置（フィート） |
| `pfx_x` | 捕手視点の水平方向の球の動き（フィート） |
| `pfx_z` | 捕手視点の垂直方向の球の動き（フィート） |
| `vx0` | y=50 フィート地点での x 方向初速（フィート/秒） |
| `vy0` | y=50 フィート地点での y 方向初速（フィート/秒） |
| `vz0` | y=50 フィート地点での z 方向初速（フィート/秒） |
| `ax` | y=50 フィート地点での x 方向加速度（フィート/秒²） |
| `ay` | y=50 フィート地点での y 方向加速度（フィート/秒²） |
| `az` | y=50 フィート地点での z 方向加速度（フィート/秒²） |
| `api_break_z_with_gravity` | 重力を含めた垂直ブレーク |
| `api_break_x_arm` | 投手の腕側へのブレーク（インチ） |
| `api_break_x_batter_in` | 打者側プレート方向へのブレーク（インチ） |
| `arm_angle` | 地面に平行な線と、投球肩位置から球位置への線のなす角 |

### コース・ゾーン

| 列名 | 日本語説明 |
|------|------------|
| `plate_x` | 捕手視点で本塁上を横切ったときの水平位置。**2025 年まで**は plate 手前。**2026 年以降**は plate 中央（ABS 整合） |
| `plate_z` | 捕手視点で本塁上を横切ったときの垂直位置。**2025 年まで**は plate 手前。**2026 年以降**は plate 中央（ABS 整合） |
| `zone` | 捕手視点で plate を横切ったときのゾーン位置 |
| `sz_top` | 球が plate 中間地点に来たときにオペレータが設定した打者ストライクゾーン上端。**2026 年以降**は ABS 定義ゾーン上端 |
| `sz_bot` | 球が plate 中間地点に来たときにオペレータが設定した打者ストライクゾーン下端。**2026 年以降**は ABS 定義ゾーン下端 |

### カウント・結果（ピッチ・打席）

| 列名 | 日本語説明 |
|------|------------|
| `balls` | ピッチ前のボール数 |
| `strikes` | ピッチ前のストライク数 |
| `type` | ピッチ結果の短縮表記。B=ボール、S=ストライク、X=インプレイ |
| `description` | 当該ピッチの結果説明 |
| `events` | 打席（plate appearance）の最終イベント |
| `des` | GameDay 由来の打席説明文 |
| `sv_id` | 試合内プレーイベント ID（試合内で一意ではない場合あり） |

### 打球・バッティング（当該ピッチがインプレイの場合）

| 列名 | 日本語説明 |
|------|------------|
| `hit_location` | 最初に球に触れた守備位置 |
| `bb_type` | 打球種。ground_ball / line_drive / fly_ball / popup |
| `hc_x` | 打球座標 X |
| `hc_y` | 打球座標 Y |
| `hit_distance` | 打球の推定飛距離 |
| `hit_distance_sc` | 上記と同義。pybaseball / 本リポジトリ Parquet の列名 |
| `launch_speed` | Statcast 計測の打球初速（mph）。未計測分は推定値を含む |
| `launch_angle` | Statcast 計測の打球角度（度）。未計測分は推定値を含む |
| `launch_speed_angle` | 初速・角度に基づくゾーン（1=Weak … 6=Barrel 等） |
| `estimated_ba_using_speedangle` | 初速・角度に基づく推定打率 |
| `estimated_woba_using_speedangle` | 初速・角度に基づく推定 wOBA |
| `estimated_slg_using_speedangle` | 初速・角度に基づく推定長打率 |
| `hyper_speed` | Savant 表示名 Adjusted EV。88 mph 未満は 88 として扱い、それ以外は実測 EV |

### 価値・期待値（当該プレー）

| 列名 | 日本語説明 |
|------|------------|
| `woba_value` | プレー結果に基づく wOBA 値 |
| `woba_denom` | プレー結果に基づく wOBA 分母 |
| `babip_value` | プレー結果に基づく BABIP 値 |
| `iso_value` | プレー結果に基づく ISO 値 |
| `delta_home_win_exp` | 打席前後のホーム勝利期待値の変化 |
| `delta_run_exp` | ピッチ前後の得点期待値（Run Expectancy）の変化 |
| `delta_pitcher_run_exp` | ピッチ前後の投手視点得点期待値（Run Expectancy）の変化 |

### スコア（ピッチ前・後）

| 列名 | 日本語説明 |
|------|------------|
| `home_score` | ピッチ前のホーム得点 |
| `away_score` | ピッチ前のアウェイ得点 |
| `bat_score` | ピッチ前の攻撃側得点 |
| `fld_score` | ピッチ前の守備側得点 |
| `post_home_score` | ピッチ後のホーム得点 |
| `post_away_score` | ピッチ後のアウェイ得点 |
| `post_bat_score` | ピッチ後の攻撃側得点 |
| `post_fld_score` | ピッチ後の守備側得点 |
| `home_score_diff` | ホーム得点 − アウェイ得点 |
| `bat_score_diff` | 攻撃側得点 − 守備側得点 |
| `home_win_exp` | ホームチームの勝利期待値 |
| `bat_win_exp` | 攻撃側チームの勝利期待値 |

### 守備配置・バットトラッキング（該当データがある場合）

| 列名 | 日本語説明 |
|------|------------|
| `if_fielding_alignment` | ピッチ時の内野守備シフト |
| `of_fielding_alignment` | ピッチ時の外野守備シフト |
| `attack_angle` | 打球時、バットスイートスポットの進行方向の垂直角（地面との比較） |
| `attack_direction` | 打球時、スイートスポットの水平角（本塁–中堅方向線との比較） |
| `swing_path_tilt` | 接触前 40 ms のスイング軌道がなす垂直角（スイング平面の傾き） |
| `intercept_ball_minus_batter_pos_x_inches` | バット/球接触点と打者重心の X 方向距離（インチ） |
| `intercept_ball_minus_batter_pos_y_inches` | バット/球接触点と打者重心の Y 方向距離（インチ・マウンド–本塁） |
| `bat_speed` | スイートスポットでのバット速度（mph） |
| `swing_length` | 計測開始から接触までバットヘッドが移動した距離の合計（フィート） |
| `miss_distance` | スイング軌道と球のミス距離（インチ） |

### 非推奨・旧トラッキング系

| 列名 | 日本語説明 |
|------|------------|
| `spin_dir` | 旧トラッキングシステム由来（非推奨） |
| `spin_rate_deprecated` | 旧トラッキング由来（非推奨）。`release_spin` に置換 |
| `break_angle_deprecated` | 旧トラッキング由来（非推奨） |
| `break_length_deprecated` | 旧トラッキング由来（非推奨） |
| `tfs_deprecated` | 旧トラッキング由来（非推奨） |
| `tfs_zulu_deprecated` | 旧トラッキング由来（非推奨） |
| `umpire` | 旧トラッキング由来（非推奨） |

---

## Statcast 用語集（ページ下部 glossary の訳）

正本ページの Statcast Glossary を要約訳したもの。詳細は [csv-docs](https://baseballsavant.mlb.com/csv-docs) を参照。

### 打撃（Batting）

| 用語 | 説明 |
|------|------|
| Exit Velocity（EV） | 打球初速（mph） |
| Launch Angle（LA） | 打球角度（度） |
| Barrels | 初速と角度の組み合わせが最適な打球 |
| Hard Hit | 初速 95 mph 以上の打球 |
| Launch Angle Sweet-Spot | 打球角度 8–32 度の範囲 |
| Batted Ball Event（BBE） | 結果を生んだ打球イベント |
| Expected Batting Average（xBA） | 打球がヒットになる確率の推定 |
| Expected wOBA（xwOBA） | 初速・角度等に基づく推定 wOBA |
| EV50 | 打者は最も硬い 50% 打球の平均初速。投手は許した打球の最も軟らかい 50% の平均 |
| Adjusted EV | 各 BBE について max(88, 実測 EV) の平均 |

### バットトラッキング（Bat Tracking）

| 用語 | 説明 |
|------|------|
| Bat Speed | スイートスポットでのバット速度。平均は上位 90% スイングの平均 |
| Fast Swing Rate | バット速度 75 mph 以上のスイングの割合 |
| Swing Length | 計測開始から接触までバットヘッドが X/Y/Z で移動した距離の合計（フィート） |
| Ideal Attack Angle | Attack Angle が 5–20° の打球 |
| Squared-Up Rate | スイング・球速から得られる最大 EV に対する実 EV の達成度 |
| Blasts | squared-up かつ fast swing の打球 |
| Swords | 打者が非競争的・見苦しいスイングをした場合の投手側指標 |

### 投球（Pitching）

| 用語 | 説明 |
|------|------|
| Pitch Velocity | 球速（mph） |
| Pitch Movement | 球の動き（インチ、平均との差も） |
| Active Spin | 球の動きに寄与する回転成分 |
| Spin Rate | 回転数（rpm） |
| Extension | マウンドからのリリース距離（フィート） |
| Expected ERA（xERA） | xwOBA を ERA スケールに 1:1 換算した指標 |

### 守備・捕手（Fielding / Catching）

| 用語 | 説明 |
|------|------|
| Pop Time | 捕手が盗塁・牽制で本塁送球までに要する時間（秒） |
| Arm Strength | 守備送球速度（mph） |
| Lead Distance | ピッチャー始動またはリリース時点での走者リード（フィート） |
| Jump | 外野手の反応・ルートの速さ |
| Outs Above Average（OAA） | 同ポジション比較でのアウト貢献 |
| Fielding Run Value | 守備をラン価値に統合した指標 |
| Catch Probability | 外野捕球確率（%） |
| Blocks Above Average | 捕手のブロック技術の同価比較 |

### 走塁（Running）

| 用語 | 説明 |
|------|------|
| Sprint Speed | 最速 1 秒区間の走速（フィート/秒） |
| Bolt | Sprint Speed が 30 ft/sec 以上の走塁 |

---

## 本プロジェクトでの参照

- データ配置: [data-catalog.md](../data-catalog.md)
- Notebook 上の DataFrame 名と Parquet 列: [statcast-dataframe.md](../statcast-dataframe.md)
- 由伸分析でよく使う列: `pitcher`, `pitch_type`, `pitch_name`, `release_speed`, `release_spin_rate`（= `release_spin`）, `pfx_x`, `pfx_z`, `release_pos_x`, `release_pos_z`, `release_extension`, `plate_x`, `plate_z`, `zone`, `description`, `events`, `game_type`, `game_date`, `game_pk`, `balls`, `strikes`, `stand`

pybaseball 等で列名が英語正本と微妙に異なる場合がある。取得直後に `schema` を確認する。

---

## 変更履歴

| 日付 | 内容 |
|------|------|
| 2026-03-21 | 初版（[csv-docs](https://baseballsavant.mlb.com/csv-docs) に基づく日本語訳） |
| 2026-09-23 | pybaseball 列名・Bat Tracking 列・`post_fld_score` 等を追記 |
