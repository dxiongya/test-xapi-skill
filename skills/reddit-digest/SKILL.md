---
name: Reddit Digest
description: Summarize what a public subreddit is talking about right now through xAPI. Use this when the user asks what's trending or being discussed in a subreddit, wants a digest of hot/top posts, or needs a quick pulse on a community without opening Reddit.
version: 0.1.0
metadata:
  xapi:
    categories: [social, data]
    tags: [reddit, community, digest, trends]
    dependencies:
      - service: reddit
        endpoint: reddit.subreddit_hot
        required: true
        purpose: Fetch the current hot posts of a public subreddit to build the digest of active discussions.
      - service: reddit
        endpoint: reddit.post_comments
        required: false
        purpose: Read top comments on a standout post when the user wants the discussion angle, not just titles.
    permissions:
      spendsCredits: true
      personalData: false
    examples:
      - title: Subreddit pulse
        prompt: What is r/MachineLearning talking about today? Give me a short digest.
      - title: Top themes
        prompt: Summarize the hot posts in r/ethfinance and group them by theme.
---

# Reddit Digest

Turn a **public** subreddit's current activity into a short, skimmable digest
through xAPI. Read-only: it never posts, votes, or acts as a user.

## When to use

- "What's r/LocalLLaMA discussing today?"
- "Give me a digest of the hot posts in r/solana."
- "What are the top themes on r/startups this week?"

Do **not** use this for private subreddits, posting/commenting, or anything that
requires a logged-in Reddit account.

## Workflow

1. Extract the subreddit name (strip a leading `r/`).
2. Fetch hot posts with `reddit.subreddit_hot` (default ~15–25 posts).
3. Group posts into 3–6 themes; note score and comment counts as signal.
4. For one or two standout posts, optionally read top comments with
   `reddit.post_comments` to capture the discussion angle.
5. Return a digest: themes, a few representative post titles with scores, and a
   one-line "overall mood" if the user asks for it.

See `references/usage.md` for parameter and cost details.

## Output

A short digest: 3–6 themes, each with 1–2 representative post titles and their
score/comment counts. Keep it factual; do not invent posts or numbers.

## Cost & safety

- Prefer a single `reddit.subreddit_hot` call; only read comments when it adds value.
- On `429`, back off and tell the user instead of looping.
- On `402` insufficient balance, tell the user to top up and stop.
