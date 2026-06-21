---
name: update-readme
description: Use this skill when a new feature, route, or dependency is added to the project.
---

# Update README

## Goal

Keep `README.md` current whenever the project changes in a way that affects users, developers, setup, routing, or dependencies.

## Workflow

1. Inspect the change set and identify anything user-facing or developer-facing that should be documented.
2. Open the existing `README.md` and preserve its current structure, tone, and formatting.
3. Keep the README organized with these sections when they are relevant:
   - Project Overview
   - Features
   - Setup
   - Dependencies
4. Add or update the feature description so readers understand what changed and why it exists.
5. Add usage instructions for any new feature, route, command, script, or workflow.
6. Add setup instructions for any new environment requirement, service, or configuration.
7. Add dependency notes for any new package, API, tool, MCP server, or external service.
8. Remove or update outdated README content that conflicts with the new behavior.
9. Run the project checks that are appropriate for the repository before finishing.

## Route Updates

When a new route or page is added, document:

- The route path.
- What the page does.
- How users should navigate to it.
- Any live data, API, or refresh behavior the page depends on.

## Dependency Updates

When a dependency or external service is added, document:

- The dependency or service name.
- Why it is needed.
- Whether installation is required.
- Any setup or environment-variable requirements.
- Whether secrets must be configured outside the repository.

## Formatting Rules

- Follow the existing README format if one exists.
- Prefer concise sections and bullets over long prose.
- Keep instructions practical and runnable.
- Do not duplicate information across sections unless it helps quick scanning.
- Do not document secrets, tokens, or credentials directly in the README.
