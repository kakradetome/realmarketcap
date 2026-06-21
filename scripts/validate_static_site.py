"""Validate the tiny static RealMarketCap homepage.

This script is intentionally small and dependency-free so new developers can run
`npm run lint` without installing a full frontend toolchain. It checks the first
pieces of app structure that matter right now: HTML exists, the stylesheet is
connected, the themed CSS exists, package.json is valid, and Render deployment
settings require lint/build before publishing.
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML_PATH = PROJECT_ROOT / "index.html"
STYLESHEET_PATH = PROJECT_ROOT / "src" / "styles.css"
PACKAGE_JSON_PATH = PROJECT_ROOT / "package.json"
RENDER_BLUEPRINT_PATH = PROJECT_ROOT / "render.yaml"


def read_text_file(file_path: Path) -> str:
    """Read a required project file and fail clearly if it is missing."""
    if not file_path.exists():
        raise FileNotFoundError(f"Required file is missing: {file_path.relative_to(PROJECT_ROOT)}")

    return file_path.read_text(encoding="utf-8")


def validate_homepage_structure() -> None:
    """Confirm the homepage still includes the core sections from this first pass."""
    index_html = read_text_file(INDEX_HTML_PATH)

    required_html_snippets = [
        '<link rel="stylesheet" href="/src/styles.css" />',
        '<header class="site-header"',
        '<section class="hero" id="overview">',
        '<aside class="market-card"',
        '<section class="feature-grid"',
    ]

    for required_html_snippet in required_html_snippets:
        if required_html_snippet not in index_html:
            raise AssertionError(f"Homepage is missing expected markup: {required_html_snippet}")


def validate_stylesheet_theme() -> None:
    """Confirm the stylesheet still contains the initial purple/pink visual language."""
    stylesheet = read_text_file(STYLESHEET_PATH)

    required_css_snippets = [
        "linear-gradient(135deg, #160822 0%, #27103f 46%, #3b0a39 100%)",
        "linear-gradient(135deg, #f472b6, #a855f7)",
        "@media (max-width: 760px)",
    ]

    for required_css_snippet in required_css_snippets:
        if required_css_snippet not in stylesheet:
            raise AssertionError(f"Stylesheet is missing expected styling: {required_css_snippet}")


def validate_package_json() -> None:
    """Confirm package.json remains parseable after adding documentation fields."""
    package_json = read_text_file(PACKAGE_JSON_PATH)
    json.loads(package_json)


def validate_render_blueprint() -> None:
    """Confirm Render deploys only after checks pass and publishes the built dist folder."""
    render_blueprint = read_text_file(RENDER_BLUEPRINT_PATH)

    required_render_snippets = [
        "runtime: static",
        "plan: free",
        "buildCommand: npm run lint && npm run build",
        "staticPublishPath: dist",
        "envVars: []",
    ]

    for required_render_snippet in required_render_snippets:
        if required_render_snippet not in render_blueprint:
            raise AssertionError(f"Render blueprint is missing: {required_render_snippet}")


def main() -> None:
    """Run all static checks used by the current lint script."""
    validate_homepage_structure()
    validate_stylesheet_theme()
    validate_package_json()
    validate_render_blueprint()
    print("Static site validation passed")


if __name__ == "__main__":
    main()
