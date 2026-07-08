#!/usr/bin/env python3
"""Package every workflow into a downloadable zip and emit catalog.json.

Source of truth is each workflows/<slug>/ folder. This script:
  1. validates that each folder has a SKILL.md with name + description frontmatter
     and a catalog.json,
  2. writes dist/<slug>.zip (the whole folder, so it drops into Adapt or any
     SKILL.md-aware tool),
  3. writes dist/catalog.json (an array the website reads to render cards).

No third-party dependencies. Run: python3 scripts/build.py
"""
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WF_DIR = ROOT / "workflows"
DIST = ROOT / "dist"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text):
    """Minimal YAML frontmatter reader for the flat keys we use (name, description)."""
    m = FM_RE.match(text)
    if not m:
        return {}
    fm, block = {}, m.group(1)
    key, buf = None, []
    for line in block.splitlines():
        m2 = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m2:
            if key:
                fm[key] = " ".join(buf).strip().strip('"').strip("'")
            key, buf = m2.group(1), [m2.group(2)]
        elif key and line.strip():
            buf.append(line.strip())
    if key:
        fm[key] = " ".join(buf).strip().strip('"').strip("'")
    return fm


def main():
    errors, catalog = [], []
    DIST.mkdir(exist_ok=True)
    slugs = sorted(p for p in WF_DIR.iterdir() if p.is_dir())
    if not slugs:
        print("No workflows found.")
        return 1

    for folder in slugs:
        slug = folder.name
        skill = folder / "SKILL.md"
        cat = folder / "catalog.json"

        if not skill.exists():
            errors.append(f"{slug}: missing SKILL.md")
            continue
        fm = parse_frontmatter(skill.read_text())
        if not fm.get("name"):
            errors.append(f"{slug}: SKILL.md frontmatter missing 'name'")
        if not fm.get("description"):
            errors.append(f"{slug}: SKILL.md frontmatter missing 'description'")
        if not cat.exists():
            errors.append(f"{slug}: missing catalog.json")
            continue
        try:
            meta = json.loads(cat.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"{slug}: catalog.json is not valid JSON ({e})")
            continue

        # Build the zip (folder contents at the archive root).
        zip_path = DIST / f"{slug}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(folder.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(folder))

        meta["skill_name"] = fm.get("name", slug)
        meta["description"] = fm.get("description", "")
        meta["zip"] = f"{slug}.zip"
        meta["github"] = f"https://github.com/adaptcom/workflows/tree/main/workflows/{slug}"
        catalog.append(meta)
        print(f"  packaged {slug} -> dist/{slug}.zip")

    if errors:
        print("\nValidation errors:")
        for e in errors:
            print(f"  - {e}")
        return 1

    (DIST / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")
    print(f"\nWrote dist/catalog.json ({len(catalog)} workflows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
