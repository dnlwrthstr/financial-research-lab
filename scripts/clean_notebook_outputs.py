#!/usr/bin/env python3
"""Clear Jupyter notebook outputs before committing or pushing.

Examples:
    python scripts/clean_notebook_outputs.py
    python scripts/clean_notebook_outputs.py --staged
    python scripts/clean_notebook_outputs.py --check
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "venv",
    ".venv",
    "__pycache__",
}


def repo_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def find_notebooks(root: Path) -> list[Path]:
    notebooks: list[Path] = []
    for path in root.rglob("*.ipynb"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        notebooks.append(path)
    return sorted(notebooks)


def staged_notebooks(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SystemExit(f"Could not read staged files: {exc}") from exc

    notebooks = []
    for line in result.stdout.splitlines():
        if line.endswith(".ipynb"):
            path = root / line
            if path.exists():
                notebooks.append(path)
    return sorted(notebooks)


def clear_notebook(path: Path, check_only: bool) -> bool:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            changed = True
            if not check_only:
                cell["outputs"] = []
        if cell.get("execution_count") is not None:
            changed = True
            if not check_only:
                cell["execution_count"] = None

    if changed and not check_only:
        path.write_text(
            json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return changed


def git_add(paths: list[Path], root: Path) -> None:
    if not paths:
        return
    subprocess.run(
        ["git", "add", "--", *[str(path.relative_to(root)) for path in paths]],
        cwd=root,
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clear outputs and execution counts from Jupyter notebooks.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Notebook files or directories to clean. Defaults to all notebooks.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Clean only staged notebooks.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if notebooks contain outputs, but do not modify files.",
    )
    parser.add_argument(
        "--add",
        action="store_true",
        help="Run git add for notebooks changed by the cleaner.",
    )
    return parser.parse_args()


def notebooks_from_paths(root: Path, paths: list[str]) -> list[Path]:
    if not paths:
        return find_notebooks(root)

    notebooks: list[Path] = []
    for raw_path in paths:
        path = (root / raw_path).resolve()
        if path.is_dir():
            notebooks.extend(find_notebooks(path))
        elif path.suffix == ".ipynb" and path.exists():
            notebooks.append(path)
    return sorted(set(notebooks))


def main() -> int:
    args = parse_args()
    root = repo_root()

    if args.staged and args.paths:
        print("Use either --staged or explicit paths, not both.", file=sys.stderr)
        return 2

    notebooks = staged_notebooks(root) if args.staged else notebooks_from_paths(root, args.paths)
    changed = [path for path in notebooks if clear_notebook(path, args.check)]

    if args.check:
        if changed:
            print("Notebook outputs found:")
            for path in changed:
                print(f"  {path.relative_to(root)}")
            return 1
        print(f"OK: {len(notebooks)} notebooks have no saved outputs.")
        return 0

    if args.add:
        git_add(changed, root)

    if changed:
        print(f"Cleared outputs in {len(changed)} notebook(s):")
        for path in changed:
            print(f"  {path.relative_to(root)}")
    else:
        print(f"OK: {len(notebooks)} notebooks already had no saved outputs.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
