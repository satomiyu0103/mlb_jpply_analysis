"""データ分析プロジェクトのパスユーティリティ。"""

from __future__ import annotations

from pathlib import Path


def get_repo_root() -> Path:
    """リポジトリルートの Path を返す。

    Returns:
        リポジトリルートの Path。
    """
    return Path(__file__).resolve().parents[2]


def data_dir() -> Path:
    """data/ ディレクトリの Path を返す。

    Returns:
        data/ ディレクトリの Path。
    """
    return get_repo_root() / "data"


def outputs_dir() -> Path:
    """outputs/ ディレクトリの Path を返す。

    Returns:
        outputs/ ディレクトリの Path。
    """
    return get_repo_root() / "outputs"


def ensure_parent_dir(path: Path) -> Path:
    """親ディレクトリを作成してパスを返す。

    Args:
        path: 出力先ファイルの Path。

    Returns:
        引数と同じ Path。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
