"""check_commit_atomicity の分類・禁止混在のテスト。"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.check_commit_atomicity import (
    buckets_for_paths,
    classify_path,
    find_forbidden_mix,
)


def test_classify_notebook() -> None:
    assert classify_path("notebooks/EDA.ipynb") == "notebooks"


def test_classify_code_and_mapping() -> None:
    assert classify_path("src/foo.py") == "code"
    assert classify_path("data/interim/mappings/statcast_column_ja.csv") == "data_mapping"


def test_notebook_must_not_mix_with_code() -> None:
    paths = ["notebooks/a.ipynb", "src/b.py"]
    buckets = buckets_for_paths(paths)
    assert find_forbidden_mix(buckets) == [("code", "notebooks")]


def test_feature_buckets_may_coexist() -> None:
    paths = [
        "src/a.py",
        "doc/agent/x.md",
        "data/interim/mappings/m.csv",
        "README.md",
    ]
    buckets = buckets_for_paths(paths)
    assert find_forbidden_mix(buckets) == []
