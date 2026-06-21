"""Validate the tiny static RealMarketCap homepage.

This script is intentionally small and dependency-free so new developers can run
`npm run lint` or `npm run build` without installing a full frontend toolchain.
It checks the first pieces of app structure that matter right now: HTML exists,
the stylesheet is connected, the themed CSS exists, package.json is valid, and
the Context7 MCP config is present.
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML_PATH = PROJECT_ROOT / "index.html"
STYLESHEET_PATH = PROJECT_ROOT / "src" / "styles.css"
TOP_100_PAGE_PATH = PROJECT_ROOT / "top-100.html"
DOMINANCE_PAGE_PATH = PROJECT_ROOT / "dominance.html"
MARKET_DATA_SCRIPT_PATH = PROJECT_ROOT / "src" / "market-data.js"
PACKAGE_JSON_PATH = PROJECT_ROOT / "package.json"
CURSOR_MCP_CONFIG_PATH = PROJECT_ROOT / ".cursor" / "mcp.json"


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
        '/top-100.html',
        '/dominance.html',
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


def validate_live_market_pages() -> None:
    """Confirm both live market pages and the shared CoinGecko script are wired together."""
    top_100_page = read_text_file(TOP_100_PAGE_PATH)
    dominance_page = read_text_file(DOMINANCE_PAGE_PATH)
    market_data_script = read_text_file(MARKET_DATA_SCRIPT_PATH)

    required_top_100_snippets = [
        'data-top100-table',
        '/src/market-data.js',
        'Top 100 Live',
    ]

    required_dominance_snippets = [
        'data-dominance-grid',
        'data-methodology-list',
        '/src/market-data.js',
    ]

    required_script_snippets = [
        'https://api.coingecko.com/api/v3/coins/markets',
        'MARKET_DATA_REFRESH_INTERVAL_MS = 45_000',
        'renderTop100Table',
        'renderDominanceLeaders',
        'calculateDominanceScore',
    ]

    for required_top_100_snippet in required_top_100_snippets:
        if required_top_100_snippet not in top_100_page:
            raise AssertionError(f"Top 100 page is missing: {required_top_100_snippet}")

    for required_dominance_snippet in required_dominance_snippets:
        if required_dominance_snippet not in dominance_page:
            raise AssertionError(f"Dominance page is missing: {required_dominance_snippet}")

    for required_script_snippet in required_script_snippets:
        if required_script_snippet not in market_data_script:
            raise AssertionError(f"Market data script is missing: {required_script_snippet}")


def validate_package_json() -> None:
    """Confirm package.json remains parseable after adding documentation fields."""
    package_json = read_text_file(PACKAGE_JSON_PATH)
    json.loads(package_json)


def validate_context7_mcp_config() -> None:
    """Confirm the project configures Context7 without committing credentials."""
    cursor_mcp_config = read_text_file(CURSOR_MCP_CONFIG_PATH)
    parsed_cursor_mcp_config = json.loads(cursor_mcp_config)

    context7_server = parsed_cursor_mcp_config.get("mcpServers", {}).get("context7")

    if context7_server is None:
        raise AssertionError("Cursor MCP config must define the context7 server")

    if context7_server.get("command") != "npx":
        raise AssertionError("Context7 MCP should run through npx for this project")

    if "@upstash/context7-mcp" not in context7_server.get("args", []):
        raise AssertionError("Context7 MCP config must reference @upstash/context7-mcp")

    forbidden_secret_keys = {"CONTEXT7_API_KEY", "apiKey", "api_key"}

    if any(forbidden_secret_key in cursor_mcp_config for forbidden_secret_key in forbidden_secret_keys):
        raise AssertionError("Do not commit Context7 API keys or credentials")


def main() -> None:
    """Run all static checks used by the current lint and build scripts."""
    validate_homepage_structure()
    validate_stylesheet_theme()
    validate_live_market_pages()
    validate_package_json()
    validate_context7_mcp_config()
    print("Static site validation passed")


if __name__ == "__main__":
    main()
