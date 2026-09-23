"""ステージ済み変更が atomic コミット単位を守っているか検査する。

ノートブックと分析コード・エージェント文書などを同一コミットに混在させない。
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Callable

BucketFn = Callable[[str], bool]

BUCKET_ORDER = (
    "notebooks",
    "code",
    "agent_doc",
    "data_mapping",
    "data_other",
    "root_doc",
    "cursor",
    "deps",
    "other",
)


def _norm(path: str) -> str:
    return path.replace("\\", "/")


def _is_notebooks(p: str) -> bool:
    return p.startswith("notebooks/")


def _is_code(p: str) -> bool:
    return p.startswith(("src/", "tests/", "scripts/"))


def _is_agent_doc(p: str) -> bool:
    return p.startswith("doc/agent/")


def _is_data_mapping(p: str) -> bool:
    return p.startswith("data/interim/mappings/")


def _is_data_other(p: str) -> bool:
    return p.startswith("data/")


def _is_root_doc(p: str) -> bool:
    return p in {"README.md", "AGENTS.md", "DESIGN.md", "TEMPLATE_SETUP.md", "ATTRIBUTION.md"} or (
        p.startswith("doc/") and not p.startswith("doc/agent/")
    )


def _is_cursor(p: str) -> bool:
    return p.startswith(".cursor/")


def _is_deps(p: str) -> bool:
    return p in {"pyproject.toml", "uv.lock"}


BUCKET_RULES: list[tuple[str, BucketFn]] = [
    ("notebooks", _is_notebooks),
    ("code", _is_code),
    ("agent_doc", _is_agent_doc),
    ("data_mapping", _is_data_mapping),
    ("data_other", _is_data_other),
    ("root_doc", _is_root_doc),
    ("cursor", _is_cursor),
    ("deps", _is_deps),
]

# 同一コミットに混在してはいけないバケットの組（どちらかがあれば両方禁止）
FORBIDDEN_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset({"notebooks", "code"}),
        frozenset({"notebooks", "agent_doc"}),
        frozenset({"notebooks", "data_mapping"}),
        frozenset({"notebooks", "data_other"}),
        frozenset({"notebooks", "cursor"}),
        frozenset({"notebooks", "deps"}),
    }
)


def classify_path(path: str) -> str:
    """1 パスをコミット単位バケットに分類する。"""
    p = _norm(path)
    for name, fn in BUCKET_RULES:
        if fn(p):
            return name
    return "other"


def buckets_for_paths(paths: list[str]) -> dict[str, list[str]]:
    """バケットごとにパスを集約する。"""
    out: dict[str, list[str]] = {k: [] for k in BUCKET_ORDER}
    for path in paths:
        bucket = classify_path(path)
        out.setdefault(bucket, []).append(_norm(path))
    return {k: sorted(v) for k, v in out.items() if v}


def find_forbidden_mix(buckets: dict[str, list[str]]) -> list[tuple[str, str]]:
    """禁止混在のバケットペアを返す。"""
    present = set(buckets)
    hits: list[tuple[str, str]] = []
    for pair in FORBIDDEN_PAIRS:
        if pair <= present:
            a, b = sorted(pair)
            hits.append((a, b))
    return hits


def get_staged_paths() -> list[str]:
    """git diff --cached --name-only の結果を返す。"""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="ステージ済み変更の atomic コミット検査")
    parser.add_argument(
        "--staged",
        action="store_true",
        help="ステージ済みのみ検査（pre-commit 用。省略時もステージ済み）",
    )
    args = parser.parse_args()
    if not args.staged:
        pass

    paths = get_staged_paths()
    if not paths:
        print("OK: ステージ済み変更はありません。")
        return 0

    buckets = buckets_for_paths(paths)
    forbidden = find_forbidden_mix(buckets)

    if forbidden:
        print("ERROR: 1 コミットに混在できない変更がステージされています。", file=sys.stderr)
        for a, b in forbidden:
            print(f"  - {a} と {b}", file=sys.stderr)
        print("\nバケット内のファイル:", file=sys.stderr)
        for name in BUCKET_ORDER:
            if name in buckets:
                print(f"  [{name}]", file=sys.stderr)
                for p in buckets[name]:
                    print(f"    {p}", file=sys.stderr)
        print(
            "\n対処: git reset でアンステージし、"
            "バケットごとに add → commit を分けてください。"
            "手順は .cursor/skills/git-commit-conventions/SKILL.md",
            file=sys.stderr,
        )
        return 1

    present = set(buckets)
    feature_unit = frozenset({"code", "agent_doc", "data_mapping", "root_doc"})
    if present - feature_unit - {"notebooks"}:
        extra = present - feature_unit - {"notebooks"}
        print(
            "ERROR: 同一コミットにまとめられないバケットが混在しています。",
            file=sys.stderr,
        )
        print(f"  余分なバケット: {', '.join(sorted(extra))}", file=sys.stderr)
        print(
            "  同一機能としてまとめられるのは "
            "code / agent_doc / data_mapping / root_doc のみです。",
            file=sys.stderr,
        )
        return 1

    print("OK: ステージ済み変更は atomic コミット単位を満たしています。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
