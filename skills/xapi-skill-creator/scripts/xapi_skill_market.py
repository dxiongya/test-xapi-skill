#!/usr/bin/env python3
"""Small helper for xAPI Skill Marketplace package and API workflows."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


MAX_PACKAGE_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 512 * 1024
MAX_FILES = 100
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$"
)
ALLOWED_SUFFIXES = {
    ".cjs",
    ".gif",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".png",
    ".py",
    ".rb",
    ".sh",
    ".ts",
    ".txt",
    ".webp",
    ".yaml",
    ".yml",
}
SCRIPT_SUFFIXES = {".cjs", ".js", ".mjs", ".py", ".rb", ".sh", ".ts"}
SCRIPT_DIRS = {"scripts", "eval-viewer"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=os.environ.get("XAPI_API_BASE", "https://api.xapi.to/api"),
        help="xAPI API base URL. Defaults to XAPI_API_BASE or production.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate_cmd = sub.add_parser("validate", help="validate a local skill folder")
    validate_cmd.add_argument("skill_dir")

    package_cmd = sub.add_parser("package", help="zip a local skill folder")
    package_cmd.add_argument("skill_dir")
    package_cmd.add_argument("output_zip")

    sub.add_parser("spec", help="fetch remote skill package spec")

    inline_cmd = sub.add_parser("submit-inline", help="submit local files by API key")
    inline_cmd.add_argument("skill_dir")

    github_cmd = sub.add_parser("submit-github", help="submit a public GitHub URL")
    github_cmd.add_argument("url")

    status_cmd = sub.add_parser("status", help="fetch submission status")
    status_cmd.add_argument("submission_id")

    delete_cmd = sub.add_parser("delete", help="explain delete/deprecation status")
    delete_cmd.add_argument("slug")

    args = parser.parse_args()

    if args.command == "validate":
        validate_skill(Path(args.skill_dir))
        print_json({"ok": True, "skillDir": str(Path(args.skill_dir).resolve())})
        return 0
    if args.command == "package":
        validate_skill(Path(args.skill_dir))
        package_skill(Path(args.skill_dir), Path(args.output_zip))
        print_json({"ok": True, "zip": str(Path(args.output_zip).resolve())})
        return 0
    if args.command == "spec":
        print_json(request(args.base, "GET", "/skills/agent/spec"))
        return 0
    if args.command == "submit-inline":
        skill_dir = Path(args.skill_dir)
        validate_skill(skill_dir)
        files = encode_files(skill_dir)
        print_json(request(args.base, "POST", "/skills/agent/submissions", {"files": files}))
        return 0
    if args.command == "submit-github":
        print_json(
            request(args.base, "POST", "/skills/agent/submissions/github", {"url": args.url})
        )
        return 0
    if args.command == "status":
        path = f"/skills/agent/submissions/{args.submission_id}"
        print_json(request(args.base, "GET", path))
        return 0
    if args.command == "delete":
        raise SystemExit(
            "Remote delete/deprecation is not available in the MVP API. "
            f"Prepare a manual admin request for slug '{args.slug}'."
        )
    return 1


def validate_skill(skill_dir: Path) -> None:
    skill_dir = skill_dir.resolve()
    if not skill_dir.is_dir():
        fail(f"not a directory: {skill_dir}")

    files = list_skill_files(skill_dir)
    if len(files) > MAX_FILES:
        fail(f"too many files: {len(files)} > {MAX_FILES}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail("SKILL.md is required")
    frontmatter = extract_frontmatter(skill_md.read_text(encoding="utf-8"))
    if not frontmatter:
        fail("SKILL.md must start with YAML frontmatter")
    name = frontmatter_field(frontmatter, "name")
    description = frontmatter_field(frontmatter, "description")
    if not name:
        fail("SKILL.md frontmatter must include name")
    if not description:
        fail("SKILL.md frontmatter must include description")

    manifest_path = skill_dir / "xapi.skill.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        slug = manifest.get("slug")
        version = manifest.get("version")
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            fail("xapi.skill.json slug is invalid")
        if not isinstance(version, str) or not SEMVER_RE.match(version):
            fail("xapi.skill.json version must be semver")
        if skill_dir.name != slug:
            fail(f"directory name '{skill_dir.name}' must match manifest slug '{slug}'")

    frontmatter_slug = frontmatter_field(frontmatter, "slug")
    if frontmatter_slug and skill_dir.name != frontmatter_slug:
        fail(f"directory name '{skill_dir.name}' must match SKILL.md slug '{frontmatter_slug}'")

    total = 0
    for path in files:
        rel = path.relative_to(skill_dir).as_posix()
        if any(part.startswith(".") for part in rel.split("/")):
            fail(f"hidden files are not allowed: {rel}")
        if path.is_symlink():
            fail(f"symlinks are not allowed: {rel}")
        suffix = path.suffix.lower()
        if suffix not in ALLOWED_SUFFIXES:
            fail(f"unsupported file extension for {rel}: {suffix or '(none)'}")
        if suffix in SCRIPT_SUFFIXES and rel.split("/", 1)[0] not in SCRIPT_DIRS:
            fail(f"script files must live under scripts/ or eval-viewer/: {rel}")
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            fail(f"file too large: {rel}")
        total += size

    if total > MAX_PACKAGE_BYTES:
        fail(f"package too large: {total} > {MAX_PACKAGE_BYTES}")


def package_skill(skill_dir: Path, output_zip: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in list_skill_files(skill_dir):
            rel = path.relative_to(skill_dir).as_posix()
            archive.write(path, rel)


def encode_files(skill_dir: Path) -> list[dict[str, str]]:
    encoded = []
    for path in list_skill_files(skill_dir):
        rel = path.relative_to(skill_dir).as_posix()
        encoded.append(
            {
                "path": rel,
                "contentBase64": base64.b64encode(path.read_bytes()).decode("ascii"),
            }
        )
    return encoded


def request(base: str, method: str, path: str, body: Any | None = None) -> Any:
    key_value = os.environ.get("XAPI_API_KEY")
    if not key_value:
        fail("XAPI_API_KEY is required for remote API calls")

    data = None
    headers = {"XAPI-KEY": key_value, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        base.rstrip("/") + path,
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {"ok": True}
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {err.code}: {detail}") from err


def list_skill_files(skill_dir: Path) -> list[Path]:
    return sorted(path for path in skill_dir.rglob("*") if path.is_file())


def extract_frontmatter(markdown: str) -> str | None:
    match = re.match(r"^---\s*\n([\s\S]*?)\n---", markdown)
    return match.group(1) if match else None


def frontmatter_field(frontmatter: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}\s*:\s*(.*)$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1]
    return value


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def fail(message: str) -> None:
    raise SystemExit(message)


if __name__ == "__main__":
    sys.exit(main())
