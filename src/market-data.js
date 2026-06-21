const COINGECKO_MARKETS_URL = new URL("https://api.coingecko.com/api/v3/coins/markets");
const MARKET_DATA_REFRESH_INTERVAL_MS = 45_000;

COINGECKO_MARKETS_URL.search = new URLSearchParams({
  vs_currency: "usd",
  order: "market_cap_desc",
  per_page: "100",
  page: "1",
  sparkline: "true",
  price_change_percentage: "1h,24h,7d",
  locale: "en",
}).toString();

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const compactCurrencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  notation: "compact",
  maximumFractionDigits: 2,
});

const percentageFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 2,
  minimumFractionDigits: 2,
});

const numberFormatter = new Intl.NumberFormat("en-US");


function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatCurrency(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return value >= 1_000_000 ? compactCurrencyFormatter.format(value) : currencyFormatter.format(value);
}

function formatPercentage(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "—";
  }

  return `${value >= 0 ? "+" : ""}${percentageFormatter.format(value)}%`;
}

function getChangeClass(value) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "neutral";
  }

  return value >= 0 ? "positive" : "negative";
}

function calculateDominanceScore(coin, largestMarketCap) {
  const marketCap = coin.market_cap ?? 0;
  const volume = coin.total_volume ?? 0;
  const rank = coin.market_cap_rank ?? 100;
  const oneHourChange = coin.price_change_percentage_1h_in_currency ?? 0;
  const dayChange = coin.price_change_percentage_24h_in_currency ?? coin.price_change_percentage_24h ?? 0;
  const weekChange = coin.price_change_percentage_7d_in_currency ?? 0;

  const marketCapScore = largestMarketCap > 0 ? Math.min((marketCap / largestMarketCap) * 100, 100) : 0;
  const rankScore = Math.max(0, 101 - rank);
  const liquidityScore = marketCap > 0 ? Math.min((volume / marketCap) * 1000, 100) : 0;
  const momentumScore = Math.max(0, Math.min(100, 50 + oneHourChange * 2 + dayChange * 1.5 + weekChange));

  return marketCapScore * 0.45 + rankScore * 0.25 + liquidityScore * 0.15 + momentumScore * 0.15;
}

async function fetchTopMarketData() {
  const response = await fetch(COINGECKO_MARKETS_URL, {
    headers: {
      accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`CoinGecko request failed with status ${response.status}`);
  }

  return response.json();
}

function createSparklinePath(prices) {
  if (!Array.isArray(prices) || prices.length < 2) {
    return "";
  }

  const width = 150;
  const height = 42;
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice || 1;

  return prices
    .map((price, index) => {
      const x = (index / (prices.length - 1)) * width;
      const y = height - ((price - minPrice) / priceRange) * height;
      return `${index === 0 ? "M" : "L"}${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(" ");
}

function setStatus(message, variant = "") {
  const statusElement = document.querySelector("[data-market-status]");

  if (!statusElement) {
    return;
  }

  statusElement.textContent = message;
  statusElement.dataset.variant = variant;
}

function updateLastUpdated() {
  const lastUpdatedElement = document.querySelector("[data-last-updated]");

  if (!lastUpdatedElement) {
    return;
  }

  lastUpdatedElement.textContent = `Updated ${new Date().toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  })}`;
}


function renderTop100Table(coins) {
  const tableBody = document.querySelector("[data-top100-table]");

  if (!tableBody) {
    return;
  }

  tableBody.innerHTML = coins
    .map((coin, index) => {
      const dayChange = coin.price_change_percentage_24h_in_currency ?? coin.price_change_percentage_24h;
      const sparklinePath = createSparklinePath(coin.sparkline_in_7d?.price);
      const animationDelay = `${Math.min(index * 0.018, 1.2).toFixed(2)}s`;

      return `
        <tr class="market-row" style="--row-delay: ${animationDelay}">
          <td class="rank-cell">#${coin.market_cap_rank ?? index + 1}</td>
          <td>
            <div class="coin-identity">
              <img src="${escapeHtml(coin.image)}" alt="" loading="lazy" />
              <div>
                <strong>${escapeHtml(coin.name)}</strong>
                <span>${escapeHtml(coin.symbol.toUpperCase())}</span>
              </div>
            </div>
          </td>
          <td class="numeric price-pulse">${formatCurrency(coin.current_price)}</td>
          <td class="numeric change ${getChangeClass(dayChange)}">${formatPercentage(dayChange)}</td>
          <td class="numeric">${formatCurrency(coin.market_cap)}</td>
          <td class="numeric">${formatCurrency(coin.total_volume)}</td>
          <td>
            <svg class="sparkline ${getChangeClass(dayChange)}" viewBox="0 0 150 42" role="img" aria-label="7 day sparkline for ${escapeHtml(coin.name)}">
              <path d="${sparklinePath}"></path>
            </svg>
          </td>
        </tr>
      `;
    })
    .join("");
}

function renderDominanceLeaders(coins) {
  const leaderGrid = document.querySelector("[data-dominance-grid]");
  const methodologyList = document.querySelector("[data-methodology-list]");

  if (!leaderGrid) {
    return;
  }

  const largestMarketCap = Math.max(...coins.map((coin) => coin.market_cap ?? 0));
  const scoredCoins = coins
    .map((coin) => ({
      ...coin,
      dominanceScore: calculateDominanceScore(coin, largestMarketCap),
    }))
    .sort((firstCoin, secondCoin) => secondCoin.dominanceScore - firstCoin.dominanceScore)
    .slice(0, 10);

  leaderGrid.innerHTML = scoredCoins
    .map((coin, index) => {
      const dayChange = coin.price_change_percentage_24h_in_currency ?? coin.price_change_percentage_24h;
      const weekChange = coin.price_change_percentage_7d_in_currency;
      const animationDelay = `${(index * 0.08).toFixed(2)}s`;

      return `
        <article class="dominance-card" style="--card-delay: ${animationDelay}">
          <div class="dominance-card__rank">${String(index + 1).padStart(2, "0")}</div>
          <div class="coin-identity">
            <img src="${escapeHtml(coin.image)}" alt="" loading="lazy" />
            <div>
              <strong>${escapeHtml(coin.name)}</strong>
              <span>${escapeHtml(coin.symbol.toUpperCase())} · Rank #${coin.market_cap_rank ?? "—"}</span>
            </div>
          </div>
          <div class="dominance-score">
            <span>Dominance score</span>
            <strong>${numberFormatter.format(Math.round(coin.dominanceScore))}</strong>
          </div>
          <div class="signal-list">
            <span>Market cap <strong>${formatCurrency(coin.market_cap)}</strong></span>
            <span>24h volume <strong>${formatCurrency(coin.total_volume)}</strong></span>
            <span>24h change <strong class="${getChangeClass(dayChange)}">${formatPercentage(dayChange)}</strong></span>
            <span>7d change <strong class="${getChangeClass(weekChange)}">${formatPercentage(weekChange)}</strong></span>
          </div>
        </article>
      `;
    })
    .join("");

  if (methodologyList) {
    methodologyList.innerHTML = `
      <li><strong>45%</strong> relative market capitalization versus the largest asset.</li>
      <li><strong>25%</strong> market-cap rank strength across the current top 100.</li>
      <li><strong>15%</strong> liquidity strength from volume relative to market cap.</li>
      <li><strong>15%</strong> blended 1h, 24h, and 7d momentum from live market data.</li>
    `;
  }
}

async function refreshMarketExperience() {
  setStatus("Refreshing live market data…");

  try {
    const coins = await fetchTopMarketData();
    renderTop100Table(coins);
    renderDominanceLeaders(coins);
    updateLastUpdated();
    setStatus("Live market data connected", "success");
  } catch (error) {
    console.error(error);
    setStatus("Unable to load live market data. CoinGecko may be rate limiting requests.", "error");
  }
}

refreshMarketExperience();
setInterval(refreshMarketExperience, MARKET_DATA_REFRESH_INTERVAL_MS);
