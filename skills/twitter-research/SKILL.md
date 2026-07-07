---
name: Twitter Research
description: Research a public Twitter/X profile and its recent activity through xAPI. Use this when the user asks to look up an X/Twitter user, summarize a profile, or review someone's recent public posts and engagement.
---

# Twitter Research

Use this skill when the user wants to research a **public** Twitter/X account
through xAPI — resolving a handle, reading the profile, and summarizing recent
public activity. It only reads public data; it never logs in as the target user
and never touches protected accounts.

## When to use

- "Research @openai and summarize the last 7 days of public activity."
- "Who is @paulg? Give me their bio, follower count, and recent themes."
- "What has @<handle> been posting about lately?"

Do **not** use this skill for private/protected accounts, DMs, or anything that
requires acting as the target user.

## Workflow

1. Extract the target handle from the request and strip a leading `@`.
2. Resolve the profile with the xAPI `twitter.user_by_screen_name` endpoint to
   get the user id, bio, follower/following counts, and verification state.
3. Read recent posts with `twitter.user_tweets` (default the latest ~20, or the
   window the user asked for).
4. Summarize: who they are, what they post about, notable recent posts, and
   engagement signals. Keep it factual and quote sparingly.
5. If the profile is not found or is protected, say so plainly and stop.

See `references/usage.md` for parameter details, cost notes, and failure handling.

## Parameters

- `handle` (required): public screen name, without `@`.
- `window` (optional): a time range or tweet count; defaults to the latest ~20 posts.

## Output

A concise brief: identity, bio, follower/following counts, 3–5 recent themes, and
1–3 representative recent posts with dates. No speculation about private details.

## Cost & safety

- Each xAPI call may consume balance per the service's pricing — make the minimum
  calls needed (one profile resolve + one timeline fetch is usually enough).
- On `429` rate limit, back off and tell the user instead of retrying in a loop.
- On `402` insufficient balance, tell the user to top up and stop.
