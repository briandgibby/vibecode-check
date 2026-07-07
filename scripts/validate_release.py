#!/usr/bin/env python3
"""Validate Vibecode Check skill packaging before release."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import zipfile

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment failure
    raise SystemExit("PyYAML is required to validate SKILL.md frontmatter") from exc

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "vibecode-check"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCE = SKILL_DIR / "references" / "prompting-principles.md"
ZIP_PATH = ROOT / "dist" / "vibecode-check.zip"
SKILL_ARCHIVE_PATH = ROOT / "dist" / "vibecode-check.skill"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_skill_md() -> None:
    content = SKILL_MD.read_text(encoding="utf-8")
    if not content.startswith("---"):
        fail("SKILL.md must start with YAML frontmatter")
    match = re.search(r"\n---\s*\n", content[3:])
    if not match:
        fail("SKILL.md frontmatter must close with ---")
    assert match is not None
    frontmatter = yaml.safe_load(content[3 : match.start() + 3])
    if not isinstance(frontmatter, dict):
        fail("SKILL.md frontmatter must parse as a mapping")
    for key in ["name", "description", "version", "author", "license", "metadata"]:
        if key not in frontmatter:
            fail(f"SKILL.md frontmatter missing {key}")
    if frontmatter["name"] != "vibecode-check":
        fail("SKILL.md name must be vibecode-check")
    description = frontmatter.get("description", "")
    if len(description) > 1024:
        fail(f"SKILL.md description is too long: {len(description)} chars")
    if len(description) > 800:
        fail(f"SKILL.md description should leave validator headroom; got {len(description)} chars")
    hermes = frontmatter.get("metadata", {}).get("hermes", {})
    if not hermes.get("tags"):
        fail("SKILL.md metadata.hermes.tags must be non-empty")
    body = content[match.end() + 3 :].strip()
    if not body:
        fail("SKILL.md body must be non-empty")
    ok(f"SKILL.md frontmatter valid; description {len(description)} chars")


def validate_json() -> None:
    plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    marketplace = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    expected_repo = "https://github.com/briandgibby/vibecode-check"
    expected_author = "https://github.com/briandgibby"
    if plugin.get("author", {}).get("url") != expected_author:
        fail("plugin.json author.url does not point to briandgibby")
    if plugin.get("homepage") != expected_repo or plugin.get("repository") != expected_repo:
        fail("plugin.json homepage/repository do not point to vibecode-check repo")
    if not marketplace.get("description"):
        fail("marketplace.json missing marketplace description")
    ok("plugin and marketplace JSON metadata valid")


def validate_placeholders() -> None:
    # Release/tooling code routinely carries review notes (e.g. "# TODO:
    # refactor") that should never block a skill release. Skip this directory
    # so the constants below can be plain string literals instead of split
    # tokens whose only purpose was to escape this very scan.
    skipped_dirs = {".git", "scripts"}
    checked_suffixes = {".md", ".json", ".py"}
    placeholders = ["your-username", "TODO", "FIXME"]
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or skipped_dirs & set(path.parts)
            or path.suffix.lower() not in checked_suffixes
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for placeholder in placeholders:
            if placeholder in text:
                hits.append(f"{path.relative_to(ROOT)} contains {placeholder}")
    if hits:
        fail("; ".join(hits))
    readme = README.read_text(encoding="utf-8")
    if "/plugin marketplace add briandgibby/vibecode-check" not in readme:
        fail("README missing correct marketplace install command")
    ok("no placeholder install metadata remains")


def validate_archives() -> None:
    if sha256(ZIP_PATH) != sha256(SKILL_ARCHIVE_PATH):
        fail(".zip and .skill artifacts must be byte-identical")
    expected = {
        "SKILL.md": SKILL_MD,
        "references/prompting-principles.md": REFERENCE,
    }
    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = set(archive.namelist())
        if names != set(expected):
            fail(f"unexpected archive contents: {sorted(names)}")
        for archive_name, source_path in expected.items():
            archive_hash = hashlib.sha256(archive.read(archive_name)).hexdigest()
            source_hash = sha256(source_path)
            if archive_hash != source_hash:
                fail(f"archive {archive_name} does not match {source_path.relative_to(ROOT)}")
    ok("dist archives are byte-identical and match source skill files")


def validate_claude_plugin() -> None:
    claude = subprocess.run(
        ["claude", "plugin", "validate", str(PLUGIN_JSON)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if claude.returncode != 0:
        print(claude.stdout)
        fail("claude plugin manifest validation failed")
    marketplace = subprocess.run(
        ["claude", "plugin", "validate", str(ROOT)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if marketplace.returncode != 0 or "warning" in marketplace.stdout.lower():
        print(marketplace.stdout)
        fail("claude marketplace validation failed or emitted warnings")
    ok("Claude Code plugin validators passed without warnings")


def main() -> None:
    validate_skill_md()
    validate_json()
    validate_placeholders()
    validate_archives()
    validate_claude_plugin()
    print("Release validation passed")


if __name__ == "__main__":
    main()
