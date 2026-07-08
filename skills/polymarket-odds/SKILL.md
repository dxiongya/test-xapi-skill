---
name: Polymarket Odds
description: Look up live prediction-market prices and implied odds on Polymarket through xAPI. Use this when the user asks what the market thinks about an event, wants current YES/NO prices or implied probability for a market, or needs to compare related markets.
version: 0.1.0
metadata:
  xapi:
    categories: [crypto, data]
    tags: [polymarket, prediction-markets, odds, probability]
    dependencies:
      - service: polymarket
        endpoint: polymarket.markets_search
        required: true
        purpose: Find the Polymarket market that matches the user's event before reading its current price.
      - service: polymarket
        endpoint: polymarket.market_prices
        required: true
        purpose: Read the current YES/NO prices for a market to report the implied probability.
    permissions:
      externalWrites: false
      spendsCredits: true
      personalData: false
    examples:
      - title: Implied probability
        prompt: What does Polymarket imply for the odds of a US rate cut this quarter?
      - title: Compare markets
        prompt: Compare the current Polymarket odds for the top three 2026 election markets.
---

# Polymarket Odds

Read **public** prediction-market data on Polymarket through xAPI and translate
prices into plain-language implied odds. Read-only: it never places, cancels, or
signs any order or transaction.

## When to use

- "What are the current Polymarket odds for <event>?"
- "What's the implied probability of <outcome> right now?"
- "Compare the odds across these related markets."

Do **not** use this skill to trade, place orders, move funds, or sign anything.

## Workflow

1. Restate the event and find the matching market with `polymarket.markets_search`.
2. If several markets match, list the closest 2–3 and ask which one (or pick the
   most liquid and say so).
3. Read current prices with `polymarket.market_prices`.
4. Convert price → implied probability (a YES price of 0.63 ≈ 63% implied), and
   note liquidity/volume as a confidence signal.
5. Report: market title, current YES/NO price, implied probability, and a short
   caveat that prices move and are not financial advice.

See `references/usage.md` for price→probability details and failure handling.

## Output

Market title, YES/NO price, implied probability, and liquidity/volume context.
Always add a one-line "not financial advice; prices move" caveat.

## Cost & safety

- Read-only only. Never construct a trade, order, or signature.
- Prefer one search + one price call per market.
- On `429`, back off and inform the user. On `402`, tell the user to top up and stop.
