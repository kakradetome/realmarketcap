# realmarketcap

## Project Overview

RealMarketCap is a cryptocurrency market intelligence site focused on making live market data easier to understand.

The current version is a dependency-free static site that can be served locally or deployed to Render. It includes a homepage, a live Top 100 cryptocurrency market board, and a dynamic Dominance Top 10 page powered by CoinGecko market data.

## Features

- Modern purple/pink homepage introducing the RealMarketCap experience.
- Live Top 100 crypto market page available directly at `/top-100.html`.
- Dominance Top 10 page available directly at `/dominance.html` that ranks assets with an objective scoring model.
- CoinGecko-powered market data refreshes every 45 seconds in the browser.
- Live Market Pulse summary showing total top-100 market cap, 24h volume, average move, and advancing assets.
- Animated table rows, glowing prices, live status indicators, sparklines, and dominance cards.
- Static validation script used by both lint and build commands.
- Render deployment blueprint in `render.yaml`.
- Context7 MCP configuration for current documentation lookup.
- Local Codex skill for keeping this README current when features, routes, or dependencies change.

## Routes

| Route | Description |
| --- | --- |
| `/` | Homepage with the first marketing overview and static section anchors. |
| `/top-100.html` | Live Top 100 cryptocurrency board with price, 24h change, market cap, volume, and 7-day sparkline data. |
| `/dominance.html` | Dynamic Dominance Top 10 page using market cap, rank, liquidity, and 1h/24h/7d momentum signals. |

## Setup

Requirements:

- Python 3
- npm

Run the site locally:

```bash
npm run dev
```

Then open:

```text
http://localhost:4173
```

Run validation:

```bash
npm run lint
```

Run the build check:

```bash
npm run build
```

Both `npm run lint` and `npm run build` currently execute the same dependency-free static validator.

## Dependencies

This project intentionally avoids installed runtime dependencies right now.

External services and tools:

- CoinGecko API: used directly in the browser for live market data.
- Render: configured as the hosting platform in `render.yaml`.
- Context7 MCP: configured in `.cursor/mcp.json` for up-to-date documentation lookup.

No API keys, tokens, or credentials should be committed to this repository. Store secrets in Render Environment Variables or local developer configuration outside the repo.
