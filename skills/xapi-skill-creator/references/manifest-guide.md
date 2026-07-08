# xAPI Skill Manifest Guide

Use `xapi.skill.json` to add marketplace metadata, xAPI dependency declarations, permissions, examples, and review hints. `SKILL.md` remains the primary skill instruction file.

## Minimal Manifest

```json
{
  "schemaVersion": "2026-07-01",
  "slug": "twitter-research",
  "version": "0.1.0",
  "categories": ["social", "research"],
  "tags": ["twitter", "x"],
  "supportedAgents": ["codex", "universal"],
  "riskLevel": "low",
  "xapiDependencies": [],
  "permissions": {
    "network": ["xapi.to"],
    "writesExternalState": false,
    "mayChargeUserBalance": false,
    "handlesPersonalData": false
  }
}
```

## Required Fields

- `schemaVersion`: Use `2026-07-01` unless the marketplace spec changes.
- `slug`: Must match the directory and `SKILL.md` slug when present. Use `^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$`.
- `version`: Semver. Bump for every marketplace submission under the same slug.

## Recommended Fields

- `categories`: Broad grouping, maximum 8.
- `tags`: Search and filtering hints, maximum 20.
- `supportedAgents`: Agent runtimes the instructions target. Use `universal` when the skill is not runtime-specific.
- `riskLevel`: `low`, `medium`, or `high`. Use `medium` when the package includes scripts or writes external state. Use `high` when it can spend funds, mutate third-party accounts, or process sensitive data.
- `examples`: Realistic user prompts that should trigger the skill.

## xAPI Dependencies

Declare dependencies when the skill expects xAPI capabilities.

```json
{
  "type": "endpoint",
  "serviceSlug": "twitter",
  "endpointKey": "twitter.user_by_screen_name",
  "required": true,
  "purpose": "Resolve a public Twitter/X profile before analysis."
}
```

Dependency `type` can be `action`, `apiService`, `endpoint`, `model`, or `oauth`.

Use `required: false` when the dependency is optional, a planned integration, or only used for submission/status automation.

## Permissions

- `network`: List external domains the skill or its scripts may contact.
- `writesExternalState`: Set `true` when the skill can create, update, submit, publish, delete, or otherwise mutate remote state.
- `mayChargeUserBalance`: Set `true` only if the skill can intentionally trigger paid xAPI calls.
- `handlesPersonalData`: Set `true` if the skill asks for or processes private user, customer, account, wallet, email, or identity data.

## Version Rules

- First public draft: `0.1.0`.
- Documentation-only or metadata-safe edit: patch bump.
- New workflow, endpoint dependency, or compatible capability: minor bump.
- Breaking behavior or removed capability: major bump.
- Never resubmit the same slug and version; the backend stores immutable versions.

## Common Mistakes

- Slug differs between folder, `SKILL.md`, and `xapi.skill.json`.
- Version missing from both `xapi.skill.json` and `SKILL.md`; this defaults to `0.1.0` and can collide on updates.
- Real API keys or bearer tokens in examples, scripts, screenshots, or test fixtures.
- Scripts placed outside `scripts/` or `eval-viewer/`.
- Marketing copy in the skill description instead of trigger-oriented instructions.
