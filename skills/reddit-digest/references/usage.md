# Usage Notes — Reddit Digest

Read this when you need parameter specifics, cost math, or failure handling.

## Inputs

- `subreddit` (required): public subreddit name, without the `r/` prefix.
- `limit` (optional): how many hot posts to scan; default ~20, keep ≤ 50.
- `withComments` (optional): only set when the user wants the discussion angle.

## Building the digest

- Group by topic, not by post order. 3–6 themes is the sweet spot.
- Use `score` and `num_comments` as relative signal — a high-comment / low-score
  post is often controversial; say so rather than hiding it.
- Quote titles verbatim and keep them short. Never fabricate a post.

## Cost & rate limits

- Budget: one `reddit.subreddit_hot` call per request. Add at most one
  `reddit.post_comments` call for a single standout post.
- `429` → the upstream is rate-limiting; back off and inform the user.
- `402` → insufficient xAPI balance; instruct the user to top up and stop.

## Failure handling

| Case | Action |
| --- | --- |
| Subreddit not found / private | State it and stop; suggest re-checking the name |
| Empty / quarantined | Report it plainly; do not work around access controls |
| Rate limited (429) | Back off, inform the user |
| Insufficient balance (402) | Tell the user to top up; do not retry |
