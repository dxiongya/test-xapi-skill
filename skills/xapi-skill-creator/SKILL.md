---
name: xapi-skill-creator
description: Create, update, package, validate, submit, and manage xAPI Skill Marketplace skills. Use this skill whenever the user asks to build an xAPI skill, write or repair xapi.skill.json, convert an existing workflow into a marketplace skill, submit a skill with an xAPI API key, import a skill from GitHub, check review status, or plan update/delete/deprecation handling for published skills.
---

# xAPI Skill Creator

## Overview

Use this skill to turn a workflow, prompt pattern, tool integration, or existing folder into a valid xAPI Skill Marketplace package. The output should follow the public repo layout, pass local validation, and optionally submit to the xAPI Skill Marketplace API when the user has configured an API key.

## Workflow

1. Clarify the intended skill: target users, trigger phrases, expected agent behavior, required xAPI capabilities, and whether scripts or references are needed.
2. Choose a slug using lowercase letters, digits, and hyphens. Keep it stable because the public marketplace path is `skills/<slug>`.
3. Create or update a package folder containing `SKILL.md` and, preferably, `xapi.skill.json`.
4. Write `SKILL.md` in the standard skills.sh style: concise frontmatter, clear trigger description, workflow instructions, and progressive references.
5. Read `references/manifest-guide.md` before writing `xapi.skill.json`.
6. Read `references/review-checklist.md` before packaging or submission.
7. For remote operations, read `references/api-workflow.md` and use `scripts/xapi_skill_market.py` when useful.

## Package Rules

- Required file: `SKILL.md`.
- Recommended file: `xapi.skill.json`.
- Optional folders: `references/`, `scripts/`, `agents/`, `assets/`, `tests/`, `eval-viewer/`.
- Maximum package size is currently 2 MB for upload/import.
- Keep scripts only under `scripts/` or `eval-viewer/`.
- Do not include credentials, private keys, live API keys, bearer tokens, or user-private data in the package.
- If updating an existing skill, bump the semver version. The same slug cannot reuse an existing version.

## Remote Operations

Only call the remote xAPI API when the user has intentionally configured an API key outside the prompt, for example through `XAPI_API_KEY`. Do not ask the user to paste credentials into chat.

Current API-key actions:

- Get package spec: `GET /skills/agent/spec`
- Submit inline files: `POST /skills/agent/submissions`
- Submit from public GitHub URL: `POST /skills/agent/submissions/github`
- Check status: `GET /skills/agent/submissions/:id`

Create/update through the API-key path is handled by the submission endpoints: the server upserts the skill from the manifest and creates a new immutable version. Zip upload and manual draft creation exist in the authenticated web flow, not the API-key agent flow.

Remote delete/deprecation is not available in the MVP API. If the user asks to delete or unpublish, prepare a safe request plan and explain that it requires the product/admin workflow until a dedicated delete/deprecate endpoint exists.

## Helper Script

Use the bundled helper for repeatable tasks:

```bash
python scripts/xapi_skill_market.py validate ./skills/my-skill
python scripts/xapi_skill_market.py package ./skills/my-skill ./my-skill.zip
XAPI_API_KEY="${XAPI_API_KEY}" python scripts/xapi_skill_market.py spec
XAPI_API_KEY="${XAPI_API_KEY}" python scripts/xapi_skill_market.py submit-inline ./skills/my-skill
XAPI_API_KEY="${XAPI_API_KEY}" python scripts/xapi_skill_market.py submit-github https://github.com/org/repo/tree/main/skills/my-skill
XAPI_API_KEY="${XAPI_API_KEY}" python scripts/xapi_skill_market.py status <submission-id>
```

The script defaults to `https://api.xapi.to/api`. Override with `XAPI_API_BASE` for local or staging environments.

## Versioning Guidance

- New skill: start at `0.1.0` unless the user gives a release policy.
- Backward-compatible docs or metadata update: bump patch.
- New capability or changed workflow: bump minor.
- Breaking behavior, removed files, or incompatible config: bump major.
- Do not submit the same slug and version twice; create a new version instead.

## Completion Report

When finishing, report:

- Where the skill package was created or updated.
- Which version was produced.
- Whether it was only validated locally, packaged as zip, submitted inline, or submitted by GitHub URL.
- The returned submission id and current status if a remote API call was made.
- Any remaining manual actions, especially review, GitHub publish approval, or unavailable delete/deprecate actions.
