# test-xapi-skill

Demo skills for the xAPI Skill Marketplace, authored with the `xapi-skill-creator` skill.

All metadata lives in `SKILL.md` YAML frontmatter (under `metadata.xapi`). The
legacy `xapi.skill.json` file is deprecated and no longer used.

## Layout

```
skills/<slug>/
  SKILL.md            # frontmatter: name, description, version, metadata.xapi
  references/*.md     # optional progressive docs
```

## Skills

- **twitter-research** — research a public Twitter/X profile and recent activity through xAPI.
- **xapi-capability-planner** — discover, compare, and plan xAPI capabilities for an agent task.
- **reddit-digest** — summarize what a public subreddit is discussing right now.
- **polymarket-odds** — look up live prediction-market prices and implied odds on Polymarket.
- **linkedin-lookup** — summarize a public LinkedIn profile into a short professional brief.

## Import into the marketplace

Either upload a zip of a `skills/<slug>/` folder, or import by GitHub URL pointing
at a single skill directory, e.g.:

```
https://github.com/dxiongya/test-xapi-skill/tree/main/skills/twitter-research
https://github.com/dxiongya/test-xapi-skill/tree/main/skills/reddit-digest
https://github.com/dxiongya/test-xapi-skill/tree/main/skills/polymarket-odds
https://github.com/dxiongya/test-xapi-skill/tree/main/skills/linkedin-lookup
https://github.com/dxiongya/test-xapi-skill/tree/main/skills/xapi-capability-planner
```
