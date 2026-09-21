# TimesFM 使い方リファレンス

Google Research の時系列基盤モデル **TimesFM**（Time Series Foundation Model）を、本テンプレでゼロショット予測に使うときの手順書です。

> **正本リポジトリ**: [google-research/timesfm](https://github.com/google-research/timesfm)  
> **ライセンス**: Apache-2.0（オープン版は Google の公式サポート製品ではない）

## 概要

TimesFM は事前学習済みの decoder-only モデルで、**学習なし（zero-shot）** で単変量時系列の将来値を予測します。

| 項目 | TimesFM 2.5（推奨） |
|------|---------------------|
| パラメータ | 約 2 億 |
| コンテキスト長 | 最大 16,384 点 |
| 予測 horizon | 設定次第（分位点 head 利用時は最大 1,000） |
| 出力 | 点予測（中央値）+ 10 分位点帯 |
| 頻度指定 | 不要（2.0 以前の `frequency` 指標は廃止） |

論文: [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688)（ICML 2024）

## いつ使うか

**向いているケース**

- 単変量の需要・売上・センサ値などを、**すぐに** 将来予測したい
- ARIMA / Prophet のパラメータ調整より、**汎用基盤モデル** を試したい
- 予測区間（不確実性）が必要
- 多数系列のバッチ予測（店舗別・SKU 別など）

**向いていないケース**

- 係数解釈が必要な古典統計モデル（ARIMA 等）
- 多変量 VAR・Granger 因果など **系列間の構造** が主目的
- 時系列分類・クラスタリング
- 表形式データの一般 ML（`scikit-learn` 等を優先）

本テンプレの [run-modeling](.cursor/skills/run-modeling/SKILL.md) では、ベースライン比較・リーク確認・評価指標の保存が必須です。TimesFM 単体の結果だけで終えず、単純ベースライン（直近平均・季節ナイーブ等）と並べて `outputs/tables/` に記録してください。

## 前提条件

### ハードウェア（TimesFM 2.5）

| 環境 | 目安 |
|------|------|
| CPU | RAM 4 GB 以上（8 GB 以上を推奨） |
| GPU | VRAM 2 GB 以上（任意・高速化） |
| ディスク | 初回ダウンロード約 800 MB（Hugging Face キャッシュ） |

モデル重みはリポジトリに含まれません。初回 `from_pretrained` 時に Hugging Face から取得されます。

### Python

- TimesFM 公式: Python 3.10+
- 本テンプレ: Python 3.11+（`pyproject.toml`）

## インストール（本テンプレは uv のみ）

プロジェクトルートで実行します。`timesfm` は **オプション依存** です。予測タスクのときだけ追加してください。

```powershell
# PyTorch バックエンド（一般的）
uv add "timesfm[torch]"

# 共変量（XReg）が必要なとき
uv add "timesfm[xreg]"

# Flax / JAX バックエンド（TPU・GPU で高速化したいとき）
uv add "timesfm[flax]"
```

PyTorch 本体は CUDA / CPU に合わせて [PyTorch 公式](https://pytorch.org/get-started/locally/) から選び、`uv add torch` 等で合わせます。

## 最小コード例

```python
import numpy as np
import timesfm
import torch

torch.set_float32_matmul_precision("high")

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch"
)

model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        use_continuous_quantile_head=True,
        force_flip_invariance=True,
        infer_is_positive=True,
        fix_quantile_crossing=True,
    )
)

point_forecast, quantile_forecast = model.forecast(
    horizon=12,
    inputs=[
        np.linspace(0, 1, 100, dtype=np.float32),
        np.sin(np.linspace(0, 20, 67)).astype(np.float32),
    ],
)
# point_forecast.shape       → (2, 12)
# quantile_forecast.shape    → (2, 12, 10)
```

## 出力の読み方

| 戻り値 | shape | 内容 |
|--------|-------|------|
| `point_forecast` | `(系列数, horizon)` | 中央値（0.5 分位点） |
| `quantile_forecast` | `(系列数, horizon, 10)` | 平均 + 10 〜 90 パーセンタイル |

分位点インデックス（よく使うもの）:

| インデックス | 意味 |
|-------------|------|
| 0 | 平均 |
| 1 | 10 パーセンタイル（80% PI の下限） |
| 5 | 中央値（`point_forecast` と一致） |
| 9 | 90 パーセンタイル（80% PI の上限） |

```python
lower_80 = quantile_forecast[:, :, 1]
upper_80 = quantile_forecast[:, :, 9]
```

## ForecastConfig の要点

```python
timesfm.ForecastConfig(
    max_context=1024,                  # 履歴の最大長（データに合わせる）
    max_horizon=256,                   # 予測步の上限
    normalize_inputs=True,             # 推奨: スケール差の安定化
    per_core_batch_size=32,            # メモリに応じて調整
    use_continuous_quantile_head=True, # 長 horizon の分位点精度
    force_flip_invariance=True,
    infer_is_positive=True,          # 全入力が正なら 0 未満を抑制
    fix_quantile_crossing=True,        # 分位点の単調性を保証
)
```

| パラメータ | 変更の目安 |
|-----------|------------|
| `normalize_inputs` | ほぼ常に `True` |
| `infer_is_positive` | 気温・リターンなど負値があり得る系列では `False` |
| `max_context` | 利用可能な履歴長に合わせる（最大 16,384） |
| `per_core_batch_size` | CPU 8 GB → 8 前後、GPU 16 GB → 64〜128 |

## 本テンプレでの配置

| 用途 | 推奨パス |
|------|----------|
| 前処理済み系列 | `data/processed/` |
| 予測スクリプト | `scripts/` または `src/analysis_project/` |
| 探索 Notebook | `notebooks/` |
| 予測結果 CSV | `outputs/tables/` |
| 予測グラフ | `outputs/figures/` |
| レポート | `outputs/reports/` |

**禁止**: `data/raw/` の上書き、raw データの Git コミット（[safe-data-handling](.cursor/skills/safe-data-handling/SKILL.md)）。

### polars から series を渡す例

```python
import polars as pl
import numpy as np

df = pl.read_csv("data/processed/weekly_demand.csv")
values = df.sort("week").select("demand").to_series().to_numpy().astype(np.float32)

point, quantiles = model.forecast(horizon=52, inputs=[values])
```

欠損値は事前に補完または系列を分割してください。入力に NaN を含めないでください。

## ホールドアウト評価

```python
H = 24
train, actual = values[:-H], values[-H:]
point, quantiles = model.forecast(horizon=H, inputs=[train])
pred = point[0]

mae = np.mean(np.abs(actual - pred))
rmse = np.sqrt(np.mean((actual - pred) ** 2))
coverage = np.mean(
    (actual >= quantiles[0, :, 1]) & (actual <= quantiles[0, :, 9])
) * 100
```

結果は `outputs/tables/timesfm_metrics.csv` 等に保存し、[statistical-ml-review](.cursor/skills/statistical-ml-review/SKILL.md) の観点（リーク・分割・ベースライン比較）を満たしてください。

## 共変量（XReg）

価格・プロモ・曜日など **外生変数** がある場合は TimesFM 2.5 + `timesfm[xreg]` で `forecast_with_covariates` を使います。

```python
point, quantiles = model.forecast_with_covariates(
    inputs=inputs,
    dynamic_numerical_covariates={"price": price_arrays},
    dynamic_categorical_covariates={"holiday": holiday_arrays},
    static_categorical_covariates={"region": region_labels},
    xreg_mode="xreg + timesfm",
)
```

動的共変量は **コンテキスト期間と予測 horizon の両方** に値が必要です。将来共変量が未知のときは、別途仮定を文書化してください。

## 異常検知（分位点の応用）

組み込みの異常検知 API はありません。予測区間外の実測値を「統計的に稀」とみなす方法が一般的です。

```python
anomalies = (actual < quantiles[0, :, 1]) | (actual > quantiles[0, :, 9])
```

トレンドの強い系列では、まずトレンド除去してから残差を評価する方が安全です。

## バッチ予測（多数系列）

```python
inputs = [
    df[col].drop_nulls().to_numpy().astype(np.float32)
    for col in series_columns
]

# メモリ不足時は CHUNK 単位で分割
CHUNK = 50
for i in range(0, len(inputs), CHUNK):
    p, q = model.forecast(horizon=H, inputs=inputs[i : i + CHUNK])
```

## よくあるミス

1. **分位点インデックス**: `quantile_forecast[..., 0]` は平均であり q0 ではない。q10=1、q90=9。
2. **系列長**: コンテキストは **32 点以上** が目安。
3. **NaN**: 推論前に除去または補完する。
4. **旧版の frequency**: 2.5 では不要。1.0/2.0 を使う場合のみ `freq` 指定（月次は `[0]`）。
5. **`infer_is_positive`**: 負になり得る系列で `True` のままにしない。
6. **可視化（ヘッドレス）**: `import matplotlib.pyplot as plt` の前に `matplotlib.use("Agg")` を設定する。

## 品質チェックリスト

- [ ] `point_forecast` が `(n_series, horizon)`、`quantile_forecast` が `(n_series, horizon, 10)`
- [ ] 出力に NaN がない
- [ ] ベースラインと MAE / RMSE / 区間カバレッジを比較した
- [ ] 図・表を `outputs/` に保存した
- [ ] 再現コマンド（`uv run python scripts/...`）を記録した

## 公式リンク

| 種別 | URL |
|------|-----|
| GitHub | https://github.com/google-research/timesfm |
| Hugging Face チェックポイント | https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6 |
| Google Research ブログ | https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/ |
| BigQuery ML 連携 | https://cloud.google.com/bigquery/docs/timesfm-model |
| ファインチューニング例（LoRA） | https://github.com/google-research/timesfm/tree/master/timesfm-forecasting/examples/finetuning |
| 公式 SKILL（詳細） | https://github.com/google-research/timesfm/tree/master/timesfm-forecasting |

## モデル版一覧

| 版 | パラメータ | コンテキスト | 状態 | チェックポイント |
|----|-----------|-------------|------|-----------------|
| **2.5** | 200M | 16,384 | **最新・推奨** | `google/timesfm-2.5-200m-pytorch` |
| 2.0 | 500M | 2,048 | アーカイブ | `google/timesfm-2.0-500m-pytorch` |
| 1.0 | 200M | 2,048 | アーカイブ | `google/timesfm-1.0-200m-pytorch` |

旧版は `uv add "timesfm==1.3.0"` およびリポジトリ内 `v1/` ディレクトリを参照してください。
