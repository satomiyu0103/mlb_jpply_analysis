"""main 直コミットのポリシーを検査する（モード B 既定）。

実装・分析成果のパスが main にステージされている場合は失敗する。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

PROTECTED_PREFIXES = (
    "src/",
    "tests/",
    "scripts/",
    "notebooks/",
    "doc/agent/",
    "data/",
)

ALLOW_MAIN_ENV = "DS_COMMIT_ALLOW_MAIN"


def get_current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_staged_paths() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def is_protected_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description="main 直コミット検査")
    parser.add_argument("--staged", action="store_true", help="ステージ済みパスを検査")
    _ = parser.parse_args()

    if os.environ.get(ALLOW_MAIN_ENV) == "1":
        print(f"SKIP: {ALLOW_MAIN_ENV}=1 のため main 検査をスキップします。")
        return 0

    branch = get_current_branch()
    if branch != "main":
        print(f"OK: 作業ブランチは {branch} です。")
        return 0

    staged = get_staged_paths()
    protected = [p for p in staged if is_protected_path(p)]
    if not protected:
        print("OK: main 上のステージに実装・分析パスはありません。")
        return 0

    print(
        "ERROR: main への直接コミットは禁止です（モード B 既定）。",
        file=sys.stderr,
    )
    print("  feat/ または fix/ ブランチを切ってからコミットしてください。", file=sys.stderr)
    print("  例: git switch -c feat/短い説明", file=sys.stderr)
    print("\n該当ステージ:", file=sys.stderr)
    for p in protected:
        print(f"  {p}", file=sys.stderr)
    print(
        f"\n例外（ソロ探索のみ）: 環境変数 {ALLOW_MAIN_ENV}=1 を一時設定。",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
