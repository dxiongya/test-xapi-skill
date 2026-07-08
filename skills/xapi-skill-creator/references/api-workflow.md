# xAPI Skill Marketplace API Workflow

Use this reference when the user wants to submit, update, import, or check a skill through the xAPI Skill Marketplace API.

## Configuration

Require the user to configure credentials outside chat:

```bash
export XAPI_API_BASE="https://api.xapi.to/api"
export XAPI_API_KEY="${XAPI_API_KEY}"
```

The API key needs:

- `skill:read` for package spec and status reads.
- `skill:submit` for inline or GitHub URL submissions.

Do not print, persist, or embed the API key in generated skill files.

## Current API-Key Endpoints

| Operation | Method | Path | Scope |
| --- | --- | --- | --- |
| Read package spec | `GET` | `/skills/agent/spec` | `skill:read` |
| Submit inline files | `POST` | `/skills/agent/submissions` | `skill:submit` |
| Submit GitHub URL | `POST` | `/skills/agent/submissions/github` | `skill:submit` |
| Check submission | `GET` | `/skills/agent/submissions/:id` | `skill:read` |

Header:

```text
XAPI-KEY: ${XAPI_API_KEY}
```

## Create And Update

The API-key path does not require a separate draft-create call. On submission, the backend reads the manifest, reserves or updates the owned skill, creates a new immutable `SkillVersion`, then opens a review submission.

Update means "submit a new version":

1. Keep the same slug.
2. Bump `version`.
3. Update `SKILL.md`, references, scripts, and `xapi.skill.json`.
4. Submit inline or by GitHub URL.
5. Track the new submission id.

If the same slug and version already exists, fix the package by bumping semver instead of retrying.

## Inline Submission

Inline submission sends file paths plus base64 content:

```json
{
  "files": [
    {
      "path": "SKILL.md",
      "contentBase64": "<base64>"
    },
    {
      "path": "xapi.skill.json",
      "contentBase64": "<base64>"
    }
  ]
}
```

Use the helper:

```bash
python scripts/xapi_skill_market.py submit-inline ./skills/my-skill
```

## GitHub URL Submission

Supported public URL forms:

```text
https://github.com/<owner>/<repo>
https://github.com/<owner>/<repo>/tree/<ref>/<skill-directory>
```

Use the helper:

```bash
python scripts/xapi_skill_market.py submit-github https://github.com/org/repo/tree/main/skills/my-skill
```

GitHub URL import is the preferred path when the skill is already in a repo and should be reviewed as a canonical source artifact.

## Zip Upload

Zip upload exists in the authenticated page/JWT flow, not the API-key agent flow. For API-key automation, prefer inline submission or GitHub URL submission.

The helper can still build a zip for page upload:

```bash
python scripts/xapi_skill_market.py package ./skills/my-skill ./my-skill.zip
```

## Delete And Deprecation

Remote skill delete, unpublish, and deprecate endpoints are not available in the MVP API-key flow.

When asked to delete:

1. Confirm the target slug and reason.
2. Do not remove public repo folders manually.
3. Prepare a request for the product/admin workflow.
4. If a future endpoint exists, require explicit user confirmation before using it.

Suggested future endpoint shape:

```text
DELETE /skills/agent/:slug
XAPI-KEY: ${XAPI_API_KEY}
Body: { "confirmSlug": "<slug>", "reason": "..." }
Scope: skill:delete
```

Until that endpoint exists, treat delete/deprecation as a manual governance action.
