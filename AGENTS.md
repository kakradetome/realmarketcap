# AGENTS.md

## Project Name

RealMarketCap

---

## Vision

RealMarketCap is a modern cryptocurrency market intelligence platform.

The goal is not to create another CoinMarketCap clone.

The goal is to build a cryptocurrency experience that users genuinely enjoy using because it is:

- Fast
- Simple
- Clear
- Educational
- Trustworthy
- Mobile-friendly
- Beginner-friendly
- Data-focused

Every feature should improve clarity.

Every screen should reduce confusion.

Every decision should favor simplicity over complexity.

---

## Primary Objective

Build a cryptocurrency market platform that provides reliable market information while remaining easy to understand.

The first version should focus on delivering a polished experience rather than a large number of features.

---

## Technology Stack

Unless explicitly instructed otherwise, use the following stack.

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

### Validation

- Zod

### Data Source

- CoinGecko API (Free Tier)

### Deployment

- Render (Free Tier)

### Package Manager

- npm

### Version Control

- Git
- GitHub

---

## Cost Requirements

All infrastructure, services, and dependencies should remain free whenever possible.

Before introducing a paid service:

1. Confirm a free alternative does not exist.
2. Confirm the feature cannot be implemented another way.
3. Document why the paid service is required.

Default assumption:

- Free first
- Paid only when absolutely necessary

---

## Engineering Philosophy

### Simplicity First

Choose the simplest solution that:

- Works correctly
- Is easy to understand
- Is easy to maintain
- Can scale reasonably

Avoid unnecessary complexity.

Avoid premature optimization.

Avoid overengineering.

---

### Readability Over Cleverness

Code is read more often than it is written.

Prioritize:

- Readability
- Consistency
- Maintainability

Avoid clever code that sacrifices clarity.

---

### Standard Conventions

Use widely accepted industry conventions.

Prefer boring, predictable solutions over unusual patterns.

Future developers should immediately understand the codebase.

---

## Naming Standards

Always use descriptive names.

Variable names should explain intent without requiring comments.

### Good

```typescript
const cryptocurrencyMarketData = await fetchCryptocurrencyMarketData();

const formattedMarketCapitalization = formatCurrency(
  cryptocurrency.marketCap
);

const twentyFourHourPriceChangePercentage =
  cryptocurrency.priceChangePercentage24Hours;
```

### Bad

```typescript
const data = await fetchData();

const marketCap = coin.mc;

const value = coin.change;

const x = response.data;
```

Never use single-letter variable names except for loop counters when appropriate.

---

## TypeScript Standards

Use TypeScript throughout the application.

Avoid:

```typescript
any
```

Prefer:

```typescript
interface Cryptocurrency {
  id: string;
  name: string;
  symbol: string;
  currentPrice: number;
  marketCap: number;
}
```

All API responses should be typed.

All reusable structures should have explicit types.

---

## Component Standards

Each component should have one responsibility.

Components should be:

- Small
- Reusable
- Predictable
- Easy to test

When a component becomes difficult to understand, split it into smaller components.

---

## File Structure

```text
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── coins/
│
├── components/
│   ├── cryptocurrency-table.tsx
│   ├── cryptocurrency-card.tsx
│   ├── search-bar.tsx
│   └── ui/
│
├── lib/
│   ├── cryptocurrency-api.ts
│   ├── formatters.ts
│   └── utils.ts
│
├── services/
│   └── cryptocurrency-service.ts
│
├── types/
│   └── cryptocurrency.ts
│
├── constants/
│   └── routes.ts
│
└── hooks/
```

---

## API Standards

External APIs should never be consumed directly inside UI components.

Use service functions.

Example:

```typescript
const cryptocurrencyMarketData =
  await getCryptocurrencyMarketData();
```

Avoid:

```typescript
await fetch(url);
```

directly inside presentation components.

---

## Error Handling

Every API request must handle:

- Loading states
- Empty states
- Error states

Users should never see raw application errors.

Provide clear messages.

Example:

```text
Unable to load cryptocurrency data.
Please try again later.
```

---

## Commenting Guidelines

Do not comment obvious code.

Do comment:

- Complex business logic
- Unusual decisions
- Non-obvious calculations
- API workarounds
- Important architectural decisions

Good:

```typescript
// CoinGecko occasionally returns null volume values.
// Default to zero to prevent UI crashes.
```

Bad:

```typescript
// Create variable
const marketCap = cryptocurrency.marketCap;
```

Comments should add value.

---

## Testing Requirements

After meaningful changes:

Run:

```bash
npm run lint
```

Then:

```bash
npm run build
```

Future testing commands:

```bash
npm test
```

Do not continue building on top of failing code.

Fix issues before adding new features.

---

## Performance Standards

Prioritize:

- Fast page loads
- Minimal JavaScript
- Efficient API requests
- Responsive layouts

Prefer:

- Server Components
- Server-side data fetching

Avoid unnecessary client-side state.

---

## Security Standards

Never expose:

- Secrets
- API keys
- Environment variables

Validate all external API responses.

Assume third-party APIs can return invalid data.

Use Zod validation whenever appropriate.

---

## UI Principles

The interface should feel:

- Modern
- Clean
- Professional
- Premium
- Data-focused

The design should emphasize understanding.

Users should quickly answer:

- What is happening?
- Which assets are moving?
- Why should I care?

---

## User Experience Principles

Optimize for:

- Speed
- Clarity
- Simplicity

Avoid:

- Visual clutter
- Excessive animations
- Unnecessary popups
- Information overload

Every element should have a purpose.

---

## Data Presentation Standards

Always display:

- Coin Name
- Symbol
- Current Price
- Market Cap
- Trading Volume
- 24 Hour Change
- Market Rank

Format values properly.

Good:

```text
$1.24B
$12,456,221
+4.82%
```

Bad:

```text
1245622100
4.8211111
```

---

## Phase 1 Features

Build:

- Homepage
- Cryptocurrency market table
- Search functionality
- Responsive design
- Loading states
- Error states
- Coin detail pages

Focus on stability before adding advanced functionality.

---

## Features Explicitly Deferred

Do not build these yet:

- Authentication
- User accounts
- Watchlists
- Notifications
- Portfolios
- Payments
- Premium subscriptions
- AI features

Keep Version 1 focused.

---

## Agent Rules

When making implementation decisions:

1. Keep everything free.
2. Use the approved technology stack.
3. Use descriptive variable names.
4. Follow standard industry conventions.
5. Keep code simple.
6. Test after meaningful changes.
7. Fix errors before continuing.
8. Avoid unnecessary dependencies.
9. Write maintainable code.
10. Prioritize clarity over cleverness.
11. Prioritize readability over brevity.
12. Prefer long-term maintainability over short-term speed.
13. Do not over-engineer solutions.
14. Explain significant architectural decisions.
15. Build production-quality code from the beginning.

---

## Current Goal

Build the first production-ready version of RealMarketCap.

The first release should deliver:

- Accurate cryptocurrency market data
- Fast performance
- Responsive design
- Clear user experience
- Reliable deployment on Render

Success is measured by simplicity, reliability, and usability.
