#!/usr/bin/env python3
"""Check whether a codebase has the day-zero SaaS scaffolding in place.

Scans a repository for the structural pieces a solo founder needs before a coding
agent can build slices: a package manifest, a committed lockfile, an env template
and a .gitignore that covers secrets, a deploy config, CI, migrations, a health
route, tests, one-command local setup, a README setup section, and seed data.

Usage:
    python3 repo_scan.py                  # scan the current directory
    python3 repo_scan.py path/to/repo
    python3 repo_scan.py --json [path]

Output: one line per expected piece (found / missing), a coverage percentage, and
the single next piece to add, in day-zero priority order. Missing pieces are
findings, not script errors: exit 0 means the scan ran, exit 2 means bad usage.

The scan is deliberately shallow and bounded (it skips node_modules, .git, build
output, and other generated dirs, and caps how much it reads) so it stays fast on
a real repository. Run it from the repo you are scaffolding, once per scaffold
pass — it answers "is the workshop set up?", not "is the code any good?".
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Directories that never contain the scaffolding we are looking for, or that are
# generated and would produce false negatives by filling the file cap.
EXCLUDE_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", ".output", "dist", "build",
    "out", "coverage", ".turbo", ".vercel", ".cache", "vendor", "target",
    "__pycache__", ".venv", "venv", "env", ".idea", ".vscode", "tmp", ".pytest_cache",
}

MAX_FILES = 6000          # hard cap on files walked; keeps the scan bounded
MAX_BYTES = 256_000       # do not read files larger than this looking for content
GREP_SCAN_CAP = 800       # max files read for any single content check

TEXT_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".rb", ".php",
    ".java", ".rs", ".sql", ".sh", ".yml", ".yaml", ".json", ".toml", ".ini",
    ".cfg", ".conf", ".md", ".txt", ".env", ".html", ".vue", ".svelte",
}

# Source/config files only — used for content checks (e.g. a health route) where a
# match inside documentation would be a false positive, not evidence of code.
CODE_EXTS = TEXT_EXTS - {".md", ".txt"}


def collect(root: str) -> list[str]:
    """Return repo-relative file paths (forward slashes), bounded and filtered."""
    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            files.append(rel.replace(os.sep, "/"))
            if len(files) >= MAX_FILES:
                return files
    return files


def read_text(root: str, rel: str) -> str:
    full = os.path.join(root, *rel.split("/"))
    try:
        if os.path.getsize(full) > MAX_BYTES:
            return ""
        with open(full, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def grep(root: str, files: list[str], pattern: str, exts: set[str] | None = None) -> list[str]:
    """Return rel paths whose text matches pattern (case-insensitive), bounded."""
    rx = re.compile(pattern, re.IGNORECASE)
    hits: list[str] = []
    scanned = 0
    for rel in files:
        if exts is not None:
            ext = os.path.splitext(rel)[1].lower()
            if ext not in exts:
                continue
        scanned += 1
        if scanned > GREP_SCAN_CAP:
            break
        if rx.search(read_text(root, rel)):
            hits.append(rel)
    return hits


def first_named(files: list[str], names: set[str]) -> str | None:
    for rel in files:
        if os.path.basename(rel) in names:
            return rel
    return None


def first_matching(files: list[str], pattern: str) -> str | None:
    rx = re.compile(pattern)
    for rel in files:
        if rx.search(rel):
            return rel
    return None


def check_manifest(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_named(files, {
        "package.json", "pyproject.toml", "requirements.txt", "go.mod",
        "composer.json", "Gemfile", "Cargo.toml", "setup.py", "pom.xml",
    })
    return (bool(hit), hit or "no package.json / pyproject.toml / go.mod found")


def check_lockfile(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_named(files, {
        "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
        "bun.lock", "poetry.lock", "uv.lock", "Pipfile.lock", "go.sum",
        "composer.lock", "Gemfile.lock", "Cargo.lock",
    })
    return (bool(hit), hit or "no lockfile committed — dependency versions are unowned")


def check_gitignore(root: str, files: list[str]) -> tuple[bool, str]:
    gi = first_named(files, {".gitignore"})
    if not gi:
        return False, "no .gitignore — .env and build output can be committed by accident"
    text = read_text(root, gi)
    if re.search(r"(^|\n)\s*\.env", text):
        return True, f"{gi} excludes .env"
    return False, f"{gi} exists but does not exclude .env (or .env*)"


def check_env_example(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_named(files, {".env.example", ".env.sample", ".env.template"})
    return (bool(hit), hit or "no .env.example — teammates and CI cannot know the required config")


def check_deploy(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_named(files, {
        "vercel.json", "netlify.toml", "fly.toml", "render.yaml", "railway.json",
        "railway.toml", "app.yaml", "Dockerfile", "Procfile", "serverless.yml",
        "wrangler.toml", "supabase/config.toml",
    })
    return (bool(hit), hit or "no deploy config (Dockerfile, vercel.json, fly.toml, …)")


def check_ci(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_matching(files, r"^\.github/workflows/.+\.(ya?ml)$")
    if hit:
        return True, hit
    hit = first_named(files, {".gitlab-ci.yml", "azure-pipelines.yml", ".travis.yml"})
    if hit:
        return True, hit
    if first_matching(files, r"^\.circleci/config\.ya?ml$"):
        return True, ".circleci/config.yml"
    return False, "no CI workflow — every deploy is a manual, unrepeatable step"


def check_migrations(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_matching(files, r"(^|/)(migrations|prisma|alembic|supabase/migrations)/")
    if hit:
        return True, hit
    hit = first_named(files, {"schema.sql", "schema.prisma", "schema.rb"})
    return (bool(hit), hit or "no migrations or schema file — the database is defined by vibes")


def check_health(root: str, files: list[str]) -> tuple[bool, str]:
    hits = grep(root, files, r"/health\b|healthz|/api/health", exts=CODE_EXTS)
    return (bool(hits), hits[0] if hits else "no health route — uptime checks have nothing to hit")


def check_tests(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_matching(files, r"(^|/)(tests?|__tests__)/")
    if hit:
        return True, hit
    hit = first_matching(files, r"\.(test|spec)\.[a-z]+$|(^|/)test_.*\.py$|_test\.go$")
    if hit:
        return True, hit
    hit = first_named(files, {"jest.config.js", "jest.config.ts", "vitest.config.ts", "pytest.ini"})
    return (bool(hit), hit or "no tests found — nothing verifies a slice before it ships")


def check_local_dev(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_named(files, {"Makefile", "docker-compose.yml", "docker-compose.yaml", "justfile", "Taskfile.yml", "compose.yaml"})
    if hit:
        return True, hit
    pkg = first_named(files, {"package.json"})
    if pkg and re.search(r'"(dev|start)"\s*:', read_text(root, pkg)):
        return True, f"{pkg} defines a dev/start script"
    return False, "no one-command dev path (Makefile, docker compose, or a dev script)"


def check_readme_setup(root: str, files: list[str]) -> tuple[bool, str]:
    readme = first_matching(files, r"(^|/)README(\.md|\.mdx)?$")
    if not readme:
        return False, "no README — a new machine cannot be brought up from the repo"
    text = read_text(root, readme)
    has_install = re.search(r"(?im)^#{1,4}\s*.*(install|setup|getting started|quick ?start)", text)
    has_run = re.search(r"(?im)^#{1,4}\s*.*(run|develop|dev|usage)", text)
    if has_install and has_run:
        return True, f"{readme} has install + run sections"
    return False, f"{readme} is missing an obvious install/setup and run/dev section"


def check_seed(root: str, files: list[str]) -> tuple[bool, str]:
    hit = first_matching(files, r"(^|/)(seeds?|fixtures?)/|seed\.[a-z]+$")
    return (bool(hit), hit or "no seed or fixtures — every new environment starts empty")


# Day-zero priority order: the "next step" is the first gap in this list.
CHECKS = [
    ("manifest", "Package manifest", check_manifest),
    ("gitignore", ".gitignore covering .env", check_gitignore),
    ("env_example", ".env.example template", check_env_example),
    ("deploy", "Deploy config", check_deploy),
    ("ci", "CI workflow", check_ci),
    ("migrations", "Migrations / schema", check_migrations),
    ("health", "Health route", check_health),
    ("tests", "Test setup", check_tests),
    ("local_dev", "One-command local dev", check_local_dev),
    ("readme", "README setup section", check_readme_setup),
    ("lockfile", "Committed lockfile", check_lockfile),
    ("seed", "Seed / fixtures", check_seed),
]


def scan(root: str) -> dict:
    files = collect(root)
    rows = []
    for cid, label, fn in CHECKS:
        ok, evidence = fn(root, files)
        rows.append({"id": cid, "label": label, "status": "found" if ok else "missing", "evidence": evidence})

    found = sum(1 for r in rows if r["status"] == "found")
    total = len(rows)
    next_step = next((r for r in rows if r["status"] == "missing"), None)
    return {
        "root": root,
        "files_scanned": len(files),
        "found": found,
        "total": total,
        "percent": round(100 * found / total) if total else 0,
        "checks": rows,
        "next_step": next_step,
    }


def render(result: dict) -> str:
    lines = [f"Repo scaffold scan — {result['root']}", "=" * 60,
             f"({result['files_scanned']} files walked, generated dirs skipped)", ""]
    for r in result["checks"]:
        mark = "[x]" if r["status"] == "found" else "[ ]"
        lines.append(f"  {mark} {r['label']:<26} — {r['evidence']}")
    lines.append("")
    lines.append(f"Scaffold coverage: {result['found']}/{result['total']} ({result['percent']}%)")
    lines.append("")
    lines.append("Next piece to add:")
    step = result["next_step"]
    if step is None:
        lines.append("  -> Scaffold complete. Build the walking skeleton's first slice next.")
    else:
        lines.append(f"  -> {step['label']}: {step['evidence']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan a repo for day-zero SaaS scaffolding and report what is missing.",
        epilog="No input file: this scans a directory tree. Default path is '.'.",
    )
    parser.add_argument("path", nargs="?", default=".", help="repository root to scan (default: .)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.path):
        sys.stderr.write(f"Error: '{args.path}' is not a directory. Pass the repo root to scan.\n")
        return 2

    result = scan(args.path)
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
