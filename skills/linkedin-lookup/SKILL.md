---
name: LinkedIn Lookup
description: Look up a public LinkedIn profile and summarize a person's professional background through xAPI. Use this when the user wants a quick professional brief on someone, their current role and company, or a summary of their public experience before a meeting or outreach.
version: 0.1.0
metadata:
  xapi:
    categories: [social, research]
    tags: [linkedin, people, profile, professional]
    dependencies:
      - service: linkedin
        endpoint: linkedin.profile_by_url
        required: true
        purpose: Resolve a public LinkedIn profile from its URL or handle to read the person's public details.
    permissions:
      externalWrites: false
      spendsCredits: true
      personalData: true
    examples:
      - title: Pre-meeting brief
        prompt: Give me a short professional brief on this LinkedIn profile before my call.
      - title: Role and company
        prompt: What is this person's current role and company, based on their public LinkedIn?
---

# LinkedIn Lookup

Summarize a **public** LinkedIn profile into a short professional brief through
xAPI. Read-only: it never sends connection requests, messages, or acts as a user.

## When to use

- "Give me a quick professional brief on <public LinkedIn URL>."
- "What's this person's current role and background?"
- "Summarize their public experience before my outreach."

Do **not** use this skill for private profiles, contact scraping, bulk lists, or
anything that acts on the person's behalf.

## Handles personal data — be careful

This skill reads **personal data** about a real person. Only summarize what is
publicly visible, keep it factual and neutral, and do not infer sensitive
attributes (health, beliefs, protected characteristics). If the user's intent
looks like harassment, surveillance, or bulk harvesting, decline.

## Workflow

1. Take the public profile URL or handle from the request.
2. Resolve it with `linkedin.profile_by_url`.
3. Summarize: name, current role and company, a short career arc, and notable
   public highlights.
4. If the profile is private or not found, say so and stop — do not work around
   access controls.

See `references/usage.md` for inputs, cost notes, and the personal-data policy.

## Output

A short brief: name, current role + company, 2–4 line career summary, and 1–2
public highlights. No sensitive inferences, no private contact details.

## Cost & safety

- One `linkedin.profile_by_url` call per person is usually enough.
- On `429`, back off and inform the user. On `402`, tell the user to top up and stop.
- Refuse bulk/scraping requests and anything targeting private data.
