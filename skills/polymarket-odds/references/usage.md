# Usage Notes — Polymarket Odds

Read this when you need price→probability specifics, cost math, or failure handling.

## Inputs

- `query` (required): the event or market description in natural language.
- `marketId` (optional): skip search when the user already gives a market id/slug.

## Price → implied probability

- For a binary market, the YES token price ≈ implied probability of YES.
  Price `0.63` ≈ **63%** implied. NO ≈ `1 − YES`.
- Small spreads and higher volume → more reliable. Call it out when a market is
  thin or the spread is wide.
- Never present odds as certainty. Always add a "prices move; not financial
  advice" caveat.

## Cost & rate limits

- Budget: one `polymarket.markets_search` + one `polymarket.market_prices` per market.
- `429` → back off and inform the user; do not tight-loop.
- `402` → insufficient xAPI balance; tell the user to top up and stop.

## Failure handling

| Case | Action |
| --- | --- |
| No matching market | Say so; suggest a more specific event description |
| Multiple matches | List the closest 2–3 and ask, or pick most liquid and state it |
| Resolved / closed market | Report the resolution instead of live odds |
| Rate limited (429) | Back off, inform the user |
| Insufficient balance (402) | Tell the user to top up; do not retry |

## Hard rule

This skill is **read-only**. Do not build, sign, or submit any order, trade, or
transaction, even if the user asks — direct them to the appropriate trading flow.
