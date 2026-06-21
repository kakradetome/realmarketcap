#!/usr/bin/env python3
"""Check for conflict markers and likely merge conflicts against a base ref.

This script is intentionally read-only. It does not merge, rebase, or edit files.
It gives Codex a deterministic pre-PR gate so conflicts are found before a pull
request is created or updated.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


CONFLICT_MARKERS = ("<" * 7, "=" * 7, ">" * 7)
SKIP_DIRECTORIES = {".git", "node_modules", "dist", ".venv", "venv", "__pycache__"}
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def run_git_command(arguments: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a git command and return the completed process."""
    return subprocess.run(
        ["git", *arguments],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def get_repository_root() -> Path:
    """Return the absolute repository root path."""
    result = run_git_command(["rev-parse", "--show-toplevel"], check=True)
    return Path(result.stdout.strip())


def resolve_base_ref(requested_base_ref: str) -> str | None:
    """Find the first usable base ref, preferring the requested ref."""
    candidate_refs = [requested_base_ref]

    if requested_base_ref != "origin/main":
        candidate_refs.append("origin/main")

    if requested_base_ref != "main":
        candidate_refs.append("main")

    for candidate_ref in candidate_refs:
        result = run_git_command(["rev-parse", "--verify", candidate_ref])

        if result.returncode == 0:
            return candidate_ref

    return None


def iter_text_files(repository_root: Path):
    """Yield tracked-looking text files while skipping large/generated directories."""
    for file_path in repository_root.rglob("*"):
        if not file_path.is_file():
            continue

        relative_parts = set(file_path.relative_to(repository_root).parts)

        if relative_parts & SKIP_DIRECTORIES:
            continue

        if file_path.suffix not in TEXT_SUFFIXES:
            continue

        yield file_path


def find_conflict_markers(repository_root: Path) -> list[str]:
    """Find files containing unresolved conflict markers."""
    files_with_markers: list[str] = []

    for file_path in iter_text_files(repository_root):
        try:
            contents = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if any(marker in contents for marker in CONFLICT_MARKERS):
            files_with_markers.append(str(file_path.relative_to(repository_root)))

    return files_with_markers


def check_merge_tree(base_ref: str) -> tuple[bool, str]:
    """Use git merge-tree as a read-only mergeability check against the base ref."""
    merge_base = run_git_command(["merge-base", "HEAD", base_ref])

    if merge_base.returncode != 0:
        return False, merge_base.stderr.strip() or f"Unable to find merge-base with {base_ref}"

    result = run_git_command(["merge-tree", merge_base.stdout.strip(), "HEAD", base_ref])
    output = result.stdout + result.stderr
    has_conflict = any(marker in output for marker in CONFLICT_MARKERS)

    return not has_conflict, output.strip()


def main() -> int:
    """Run all merge-conflict checks."""
    parser = argparse.ArgumentParser(description="Check for merge conflicts before push or PR creation.")
    parser.add_argument("--base", default="origin/main", help="Base ref to check against. Defaults to origin/main.")
    args = parser.parse_args()

    repository_root = get_repository_root()
    marker_files = find_conflict_markers(repository_root)

    if marker_files:
        print("Conflict markers found:")
        for marker_file in marker_files:
            print(f"- {marker_file}")
        return 1

    base_ref = resolve_base_ref(args.base)

    if base_ref is None:
        print("No base ref found. Checked requested base, origin/main, and main.")
        print("Skipping merge-tree check, but conflict-marker scan passed.")
        return 0

    mergeable, merge_output = check_merge_tree(base_ref)

    if not mergeable:
        print(f"Potential merge conflicts detected against {base_ref}.")
        if merge_output:
            print(merge_output)
        return 1

    print(f"No conflict markers found and merge-tree check passed against {base_ref}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
