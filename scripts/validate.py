#!/usr/bin/env python3
"""Validate every skill in this repo against docs/SKILL-STANDARDS.md.

Run from the repo root:

    python3 scripts/validate.py
    python3 scripts/validate.py --json

Checks, per skills/<name>/:
  - SKILL.md exists and starts with YAML frontmatter ('---' on line 1)
  - frontmatter uses only the portable keys: name, description, license,
    compatibility, metadata
  - name matches the folder name and matches ^[a-z0-9]+(-[a-z0-9]+)*$
  - description is present, third person (no leading "I "), 1..1024 chars
  - SKILL.md body is under 500 lines
  - every scripts/*.py runs `--help` and exits 0
  - evals/evals.json exists, is valid JSON, and has >= 3 evals
  - references/ has no nested subdirectories (one level deep)

Exit codes: 0 = all skills pass, 1 = one or more problems, 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = {"anthropic", "claude"}
MAX_DESCRIPTION = 1024
MAX_BODY_LINES = 500
MIN_EVALS = 3


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Minimal parser for the flat subset we use."""
    if not text.startswith("---"):
        raise ValueError("file does not start with '---'")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("frontmatter is not closed with '---'")
    fm_text = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    fm: dict = {}
    for raw in fm_text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            continue  # nested value (e.g. under metadata:); not needed here
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, body


def check_skill(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [f"{name}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{name}: {exc}"]

    extra = set(fm) - ALLOWED_KEYS
    if extra:
        problems.append(f"{name}: non-portable frontmatter key(s): {', '.join(sorted(extra))}")

    fm_name = fm.get("name", "")
    if fm_name != name:
        problems.append(f"{name}: frontmatter name '{fm_name}' != folder '{name}'")
    if fm_name and not NAME_RE.match(fm_name):
        problems.append(f"{name}: name '{fm_name}' is not kebab-case")
    if any(word in name for word in RESERVED):
        problems.append(f"{name}: name contains a reserved word")

    desc = fm.get("description", "")
    if not desc:
        problems.append(f"{name}: missing description")
    else:
        if len(desc) > MAX_DESCRIPTION:
            problems.append(f"{name}: description is {len(desc)} chars (> {MAX_DESCRIPTION})")
        if desc.startswith(("I ", "I'", "You ", "We ")):
            problems.append(f"{name}: description should be third person")

    body_lines = len(body.splitlines())
    if body_lines > MAX_BODY_LINES:
        problems.append(f"{name}: body is {body_lines} lines (> {MAX_BODY_LINES})")

    for ref in sorted((skill_dir / "references").glob("*")) if (skill_dir / "references").exists() else []:
        if ref.is_dir():
            problems.append(f"{name}: references/{ref.name}/ is nested (must be one level deep)")

    for script in sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").exists() else []:
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--help"],
                capture_output=True,
                timeout=20,
            )
        except subprocess.TimeoutExpired:
            problems.append(f"{name}: scripts/{script.name} --help timed out")
            continue
        if proc.returncode != 0:
            problems.append(
                f"{name}: scripts/{script.name} --help exited {proc.returncode}"
            )

    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.exists():
        problems.append(f"{name}: missing evals/evals.json")
    else:
        try:
            data = json.loads(evals_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{name}: evals/evals.json is invalid JSON ({exc})")
        else:
            count = len(data.get("evals", []))
            if count < MIN_EVALS:
                problems.append(f"{name}: only {count} evals (need >= {MIN_EVALS})")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate skills against SKILL-STANDARDS.md.")
    parser.add_argument("--skills-dir", default="skills", help="directory holding the skills (default: skills)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    skills_dir = Path(args.skills_dir)
    if not skills_dir.is_dir():
        sys.stderr.write(f"Error: '{skills_dir}' is not a directory. Run from the repo root.\n")
        return 2

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not skill_dirs:
        sys.stderr.write(f"Error: no skills found under '{skills_dir}'.\n")
        return 2

    all_problems: list[str] = []
    per_skill: dict[str, list[str]] = {}
    for d in skill_dirs:
        problems = check_skill(d)
        per_skill[d.name] = problems
        all_problems.extend(problems)

    if args.json:
        json.dump({"skills": len(skill_dirs), "problems": per_skill}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for d in skill_dirs:
            problems = per_skill[d.name]
            if problems:
                print(f"FAIL  {d.name}")
                for p in problems:
                    print(f"      - {p.split(': ', 1)[-1]}")
            else:
                print(f"ok    {d.name}")
        print()
        if all_problems:
            print(f"{len(all_problems)} problem(s) across {len(skill_dirs)} skill(s).")
        else:
            print(f"All {len(skill_dirs)} skills pass the standards check.")

    return 1 if all_problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
