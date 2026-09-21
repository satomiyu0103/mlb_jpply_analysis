"""paths モジュールのテスト。"""

from __future__ import annotations

from pathlib import Path

from analysis_project.paths import data_dir, ensure_parent_dir, get_repo_root, outputs_dir


def test_get_repo_root_contains_pyproject() -> None:
    """リポジトリルートに pyproject.toml が存在する。"""
    root = get_repo_root()
    assert (root / "pyproject.toml").is_file()


def test_data_dir_under_repo_root() -> None:
    """data_dir はリポジトリルート配下の data/ を指す。"""
    root = get_repo_root()
    assert data_dir() == root / "data"


def test_outputs_dir_under_repo_root() -> None:
    """outputs_dir はリポジトリルート配下の outputs/ を指す。"""
    root = get_repo_root()
    assert outputs_dir() == root / "outputs"


def test_ensure_parent_dir_creates_parents(tmp_path: Path) -> None:
    """ensure_parent_dir は親ディレクトリを作成する。"""
    target = tmp_path / "nested" / "dir" / "file.csv"
    result = ensure_parent_dir(target)
    assert result == target
    assert target.parent.is_dir()
