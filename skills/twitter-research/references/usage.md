# Usage Notes

Progressive detail for the Twitter Research skill. Read this only when you need
parameter specifics, cost math, or failure handling.

## Handle resolution

- Accept `@handle` or bare `handle`; always strip the leading `@`.
- Resolve once via `twitter.user_by_screen_name`. Cache the returned `userId`
  for the timeline call so you don't resolve twice.
- If the response is empty or 404, the account does not exist or was renamed —
  report it and stop.

## Reading recent activity

- Use `twitter.user_tweets` with the resolved `userId`.
- Default to the latest ~20 posts. If the user gives a time window (e.g. "last
  7 days"), filter client-side by post timestamp rather than over-fetching.
- Exclude retweets from theme analysis unless the user asks about amplification.

## Cost & rate limits

- Budget: one profile resolve + one timeline fetch per request. That is the
  minimum and usually sufficient.
- `429` → the upstream is rate-limiting; back off, do not tight-loop, and tell
  the user the request was throttled.
- `402` → insufficient xAPI balance; instruct the user to top up and stop.

## Failure handling

| Case | Action |
| --- | --- |
| User not found (404) | Report clearly, suggest re-checking the handle |
| Protected / suspended | State it and stop; do not attempt workarounds |
| Insufficient balance (402) | Tell the user to top up; do not retry |
| Rate limited (429) | Back off, inform the user |

## Output shape

A short brief: identity + bio, follower/following counts, 3–5 recent themes, and
1–3 representative posts with dates. Keep quotes short and factual.
