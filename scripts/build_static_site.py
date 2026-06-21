"""Build the dependency-free RealMarketCap static site.

Render static sites expect a publish directory. This script creates that
`dist/` directory and copies only the public files the browser needs. Keeping the
build explicit makes deployment easier to understand for new contributors.
"""

from __future__ import annotations

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIRECTORY = PROJECT_ROOT / "dist"
SOURCE_STYLES_DIRECTORY = PROJECT_ROOT / "src"
DIST_STYLES_DIRECTORY = DIST_DIRECTORY / "src"
INDEX_HTML_PATH = PROJECT_ROOT / "index.html"
STYLESHEET_PATH = SOURCE_STYLES_DIRECTORY / "styles.css"


def recreate_dist_directory() -> None:
    """Remove old build output so each build starts from a clean directory."""
    if DIST_DIRECTORY.exists():
        shutil.rmtree(DIST_DIRECTORY)

    DIST_STYLES_DIRECTORY.mkdir(parents=True)


def copy_static_assets() -> None:
    """Copy the homepage and stylesheet into the deployable dist directory."""
    shutil.copy2(INDEX_HTML_PATH, DIST_DIRECTORY / "index.html")
    shutil.copy2(STYLESHEET_PATH, DIST_STYLES_DIRECTORY / "styles.css")


def main() -> None:
    """Create the final static files that Render will publish."""
    recreate_dist_directory()
    copy_static_assets()
    print("Static site built into dist/")


if __name__ == "__main__":
    main()
