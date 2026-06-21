"""Validate the tiny static RealMarketCap homepage.

This script is intentionally small and dependency-free so new developers can run
`npm run lint` or `npm run build` without installing a full frontend toolchain.
It checks the first pieces of app structure that matter right now: HTML exists,
the stylesheet is connected, the themed CSS exists, and package.json is valid.
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML_PATH = PROJECT_ROOT / "index.html"
TOP_100_HTML_PATH = PROJECT_ROOT / "top-100.html"
DOMINANCE_HTML_PATH = PROJECT_ROOT / "dominance.html"
STYLESHEET_PATH = PROJECT_ROOT / "src" / "styles.css"
PACKAGE_JSON_PATH = PROJECT_ROOT / "package.json"
HTML_PAGE_PATHS = (INDEX_HTML_PATH, TOP_100_HTML_PATH, DOMINANCE_HTML_PATH)
REQUIRED_SITE_LINKS = ('href="/"', 'href="/top-100.html"', 'href="/dominance.html"')


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


def validate_site_navigation() -> None:
    """Confirm every active page links to every other active page."""
    for html_page_path in HTML_PAGE_PATHS:
        html_page = read_text_file(html_page_path)

        for required_site_link in REQUIRED_SITE_LINKS:
            if required_site_link not in html_page:
                relative_page_path = html_page_path.relative_to(PROJECT_ROOT)
                raise AssertionError(f"{relative_page_path} is missing site link: {required_site_link}")


def validate_package_json() -> None:
    """Confirm package.json remains parseable after adding documentation fields."""
    package_json = read_text_file(PACKAGE_JSON_PATH)
    json.loads(package_json)


def main() -> None:
    """Run all static checks used by the current lint and build scripts."""
    validate_homepage_structure()
    validate_stylesheet_theme()
    validate_site_navigation()
    validate_package_json()
    print("Static site validation passed")


if __name__ == "__main__":
    main()
