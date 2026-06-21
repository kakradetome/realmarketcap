---
name: prevent-merge-conflicts
description: Use this skill before every push or pull request to check for merge conflicts against main, detect conflict markers, and resolve conflicts before a PR is created.
---

# Prevent Merge Conflicts

## Goal

Keep pull requests mergeable before they are opened or updated.

Use this skill before any push or PR creation, and whenever GitHub reports branch conflicts.

## Required Workflow

1. Inspect the working tree with `git status --short --branch`.
2. Run the bundled conflict check script:

   ```bash
   python3 .codex/skills/prevent-merge-conflicts/scripts/check_merge_conflicts.py --base origin/main
   ```

3. If the script reports conflict markers, remove every opening, separator, and closing conflict marker and resolve the surrounding content.
4. If the script reports merge conflicts against the base branch, resolve them before creating the PR.
5. Prefer the current `main` version for files GitHub already shows in the conflict UI unless the user explicitly asks to keep the branch version.
6. Move additive work into new files when possible instead of repeatedly editing known conflict-prone files.
7. Re-run the bundled script after fixes.
8. If the repository checkout does not include `origin/main`, fetch it before opening a PR; use `--allow-missing-base` only for local marker-only validation, not as PR approval.
9. Run the project checks required by `AGENTS.md`.
10. Only create or update the PR after the conflict check and project checks pass.

## Conflict Resolution Policy

When fixing conflicts:

- Preserve user-requested behavior first.
- Prefer simple resolutions over clever rewrites.
- Avoid reintroducing a change that was just removed to fix conflicts.
- Keep README edits minimal when README is already a conflicted file.
- Keep validators stable unless the user specifically asks for broader validation.
- If a conflict is only whitespace, match `main` exactly.

## Expected Passing State

Before creating a PR, these should be true:

- `git status --short --branch` does not show uncommitted conflict artifacts.
- No tracked project file contains conflict markers.
- The bundled conflict script exits successfully against `origin/main` or another explicit PR base.
- `npm run lint` passes.
- `npm run build` passes.
