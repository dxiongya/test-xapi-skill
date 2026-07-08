# Usage Notes — LinkedIn Lookup

Read this when you need input specifics, cost math, the personal-data policy, or
failure handling.

## Inputs

- `profile` (required): a public LinkedIn profile URL or handle.

## Personal-data policy (read first)

- Summarize only **public** fields. Never guess sensitive attributes.
- Keep it neutral and factual — a professional brief, not a dossier.
- Decline bulk lookups, contact harvesting, surveillance, or harassment intent.
- If the profile is private, stop. Do not attempt to bypass access controls.

## Cost & rate limits

- Budget: one `linkedin.profile_by_url` call per person.
- `429` → back off and inform the user; do not tight-loop.
- `402` → insufficient xAPI balance; tell the user to top up and stop.

## Failure handling

| Case | Action |
| --- | --- |
| Profile not found | Say so; suggest re-checking the URL |
| Private / restricted | State it and stop; do not work around it |
| Rate limited (429) | Back off, inform the user |
| Insufficient balance (402) | Tell the user to top up; do not retry |
