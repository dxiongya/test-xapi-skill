# xAPI Capability Planning Guide

Use this guide when a request requires comparing or composing xAPI capabilities.

## Discovery Questions

- What entity does the user care about: profile, token, wallet, market, URL, API service, document, or task?
- Is the requested data public, private, authenticated, paid, or time-sensitive?
- Does the user need a one-shot answer, recurring monitor, integration code, or marketplace registration?
- Is an existing xAPI action enough, or does the workflow need multiple calls?

## Comparison Criteria

| Criterion | Prefer |
| --- | --- |
| Fit | The action/capability returns the exact data needed with minimal transformation. |
| Inputs | Inputs the user already has, such as username, token address, URL, or query. |
| Freshness | Real-time or recent enough for the task. |
| Auth | No OAuth unless the user explicitly needs private account data. |
| Cost | Fewer calls and narrower queries when balance may be charged. |
| Agent usability | Stable schemas, clear errors, and predictable output fields. |

## Plan Template

```text
Recommended: <action or capability>
Inputs:
- <field>: <source>
Call:
<command or HTTP example>
Expected output:
- <field>: <meaning>
Fallback:
- <what to try if this fails>
Warnings:
- <cost, auth, privacy, rate-limit, or mutation risk>
```

## Multi-Step Template

```text
1. Resolve entity
   Action: <action>
   Output used next: <field>

2. Fetch detail
   Action: <action>
   Input from step 1: <field>

3. Summarize or transform
   Action: <action>
   Output: <final format>
```

## Common Patterns

- Social research: resolve profile -> fetch timeline/posts -> summarize themes.
- Crypto token research: fetch token metadata -> check security/liquidity -> inspect holders/traders.
- Web research: search web/news -> fetch or summarize source snippets -> produce cited answer.
- API onboarding: inspect OpenAPI -> map endpoints -> produce provider registration plan.
