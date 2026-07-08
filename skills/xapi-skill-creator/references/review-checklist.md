# Review Checklist

Run this checklist before packaging or submitting a skill.

## Structure

- `SKILL.md` exists and starts with YAML frontmatter.
- Frontmatter has `name` and trigger-oriented `description`.
- Folder name, `SKILL.md` slug if present, and `xapi.skill.json.slug` match.
- Optional files are under allowed folders.
- Script files live only under `scripts/` or `eval-viewer/`.

## Content

- Instructions are concise and actionable.
- Resource references say when to read each file.
- The skill does not include process notes, implementation diary, or unnecessary README files.
- Examples are realistic user prompts, not marketing text.

## Manifest

- `schemaVersion` is current.
- `version` is semver and bumped for updates.
- `riskLevel` matches actual behavior.
- `permissions` honestly reflect network, mutation, payment, and personal-data behavior.
- `xapiDependencies` list the xAPI capabilities the skill expects.

## Security

- No API keys, bearer tokens, private keys, cookies, `.env` contents, or credentials.
- No hidden files, symlinks, binary executables, or generated dependency folders.
- No destructive operation is automated without explicit confirmation.
- Remote submission uses environment variables for credentials.

## Submission

- Local validation passes.
- The package is under size limits.
- If using GitHub URL import, the repo or tree URL is public and points at the skill root.
- If using API key submission, the key has `skill:submit` and `skill:read`.
- Record the returned submission id and status.
