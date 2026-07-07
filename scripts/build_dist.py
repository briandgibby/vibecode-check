#!/usr/bin/env python3
"""Build deterministic Vibecode Check skill distributables."""

from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "vibecode-check"
DIST_DIR = ROOT / "dist"
ZIP_PATH = DIST_DIR / "vibecode-check.zip"
SKILL_PATH = DIST_DIR / "vibecode-check.skill"

# Stable timestamp accepted by ZIP readers. Keeps artifacts byte-for-byte
# reproducible when source content does not change.
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def iter_skill_files() -> list[Path]:
    files = [p for p in SKILL_DIR.rglob("*") if p.is_file()]
    return sorted(files, key=lambda p: p.relative_to(SKILL_DIR).as_posix())


def write_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in iter_skill_files():
            rel = source.relative_to(SKILL_DIR).as_posix()
            info = zipfile.ZipInfo(rel, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            # rw-r--r--, regular file. Avoids platform-dependent permissions.
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())


def main() -> None:
    if not (SKILL_DIR / "SKILL.md").exists():
        raise SystemExit(f"Missing skill file: {SKILL_DIR / 'SKILL.md'}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    write_zip(ZIP_PATH)
    shutil.copyfile(ZIP_PATH, SKILL_PATH)
    print(f"Built {ZIP_PATH.relative_to(ROOT)}")
    print(f"Built {SKILL_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
