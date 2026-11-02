#!/usr/bin/env python3
"""Validate and package the skill without dependencies or network access."""

import argparse
from pathlib import Path
import re
import sys
import zipfile

from page_marketer.markdown import inventory


ROOT = Path(__file__).resolve().parents[1]
NAME = "github-page-marketer"
INCLUDED = ["SKILL.md", "agents", "assets", "references", "templates", "examples", "scripts/audit.py", "scripts/share_buttons.py", "scripts/page_marketer"]


def validate(root=ROOT):
    errors = []
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or "\n---\n" not in skill[4:]:
        errors.append("SKILL.md requires YAML front matter")
    else:
        front = skill.split("---", 2)[1]
        if not re.search(r"^name: github-page-marketer$", front, re.M):
            errors.append("Skill name must be github-page-marketer")
        if not re.search(r"^description: .{40,}$", front, re.M):
            errors.append("Provide a useful trigger description")
    for path in [root / "SKILL.md", *sorted((root / "references").glob("*.md")), *sorted((root / "templates").glob("*.md"))]:
        content = path.read_text(encoding="utf-8")
        parsed = inventory(content)
        for link in parsed["links"] + parsed["images"]:
            target = link["url"]
            if "://" in target or target.startswith("#") or "{{" in target:
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append(f"Unresolved or external local reference in {path.name}: {target}")
    for required in INCLUDED:
        if not (root / required).exists():
            errors.append(f"Missing skill asset: {required}")
    interface_path = root / "agents" / "openai.yaml"
    if interface_path.is_file():
        interface = interface_path.read_text(encoding="utf-8")
        for target in re.findall(r'^\s+icon_(?:small|large):\s*"([^"]+)"', interface, re.M):
            resolved = (root / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append(f"Missing or external skill icon: {target}")
    return errors


def package(output, root=ROOT):
    errors = validate(root)
    if errors:
        raise ValueError("; ".join(errors))
    output = Path(output)
    if output.exists():
        raise ValueError("Archive already exists; choose a new output path")
    files = set()
    for relative in INCLUDED:
        path = root / relative
        files.update(path.rglob("*") if path.is_dir() else [path])
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            entry = zipfile.ZipInfo(NAME + "/" + path.relative_to(root).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate only")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / (NAME + ".skill"))
    args = parser.parse_args(argv)
    try:
        errors = validate()
        if errors:
            raise ValueError("; ".join(errors))
        if args.check:
            print("Skill structure and local references validated.")
        else:
            print(package(args.output))
    except (OSError, ValueError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
