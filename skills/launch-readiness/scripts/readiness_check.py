#!/usr/bin/env python3
"""Check whether a repository is safe to put in front of its first real users.

Goes past "does it build?" and looks at go-live risk: secrets committed to the
repo, a stray .env in the tree, missing error tracking, no rate limiting, backups
that are never restored, no rollback path, missing legal pages, absent monitoring,
feature flags, debug mode left on, and dependency governance.

Usage:
    python3 readiness_check.py                    # scan the current directory
    python3 readiness_check.py path/to/repo
    python3 readiness_check.py --json [path]
    python3 readiness_check.py --doc founder/product/launch-readiness.md [path]
    python3 readiness_check.py --strict [path]

Output: gaps grouped by severity (blocker / high / medium / low), a verdict, and
the single next thing to fix. Exit 0 = ready (or ready-with-gaps), 1 = a blocker or
high-severity gap remains (so CI can gate a launch), 2 = usage/input error. With
--strict, any gap fails the run.

--doc reads the launch-readiness markdown and reports how many of its checklist
boxes are ticked, so the document and the scan stay in sync.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

EXCLUDE_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", ".output", "dist", "build", "out",
    "coverage", ".turbo", ".vercel", ".cache", "vendor", "target", "__pycache__",
    ".venv", "venv", "env", ".idea", ".vscode", "tmp", ".pytest_cache",
}
MAX_FILES = 6000
MAX_BYTES = 256_000
GREP_CAP = 800

CODE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".rb", ".php",
    ".java", ".rs", ".sql", ".sh", ".yml", ".yaml", ".json", ".toml", ".ini",
    ".cfg", ".conf", ".env", ".html", ".vue", ".svelte", ".tf",
}
DOC_EXTS = {".md", ".mdx", ".txt", ".rst"}

# Real-secret shapes. High-precision on purpose: these do not match placeholders.
SECRET_PATTERNS = [
    r"sk_live_[0-9A-Za-z]{16,}",
    r"rk_live_[0-9A-Za-z]{16,}",
    r"AKIA[0-9A-Z]{16}",
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    r"xox[baprs]-[0-9A-Za-z-]{10,}",
    r"ghp_[0-9A-Za-z]{30,}",
    r"github_pat_[0-9A-Za-z_]{30,}",
    r"AIza[0-9A-Za-z_-]{30,}",
    r"(?i)(?:api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*['\"][0-9A-Za-z/_+.\-]{24,}['\"]",
]
# Values that look like secrets but are placeholders.
PLACEHOLDER = re.compile(
    r"(?i)your[_-]|example|sample|placeholder|changeme|xxx|<[a-z_]+>|"
    r"process\.env|os\.environ|import\.meta\.env|getenv|redacted|dummy|test[_-]?key"
)


def collect(root: str) -> list[str]:
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


def grep(root, files, pattern, exts=None, skip_names_re=None):
    rx = re.compile(pattern, re.IGNORECASE)
    skip = re.compile(skip_names_re, re.IGNORECASE) if skip_names_re else None
    hits, scanned = [], 0
    for rel in files:
        if exts is not None and os.path.splitext(rel)[1].lower() not in exts:
            continue
        if skip and skip.search(rel):
            continue
        scanned += 1
        if scanned > GREP_CAP:
            break
        if rx.search(read_text(root, rel)):
            hits.append(rel)
    return hits


def any_named(files, names):
    return next((r for r in files if os.path.basename(r) in names), None)


def any_match(files, pattern):
    rx = re.compile(pattern)
    return next((r for r in files if rx.search(r)), None)


# --- checks: each returns (ok: bool, detail: str) ---------------------------

def c_secrets(root, files):
    skip = r"example|sample|\.test\.|\.spec\.|fixture|template|docs/"
    for pat in SECRET_PATTERNS:
        rx = re.compile(pat)
        for rel in grep(root, files, pat, exts=CODE_EXTS, skip_names_re=skip):
            text = read_text(root, rel)
            for m in rx.finditer(text):
                snippet = m.group(0)
                if PLACEHOLDER.search(snippet):
                    continue
                return False, f"possible real secret in {rel} ({snippet[:24]}…) — rotate it and move it to the secret store"
    return True, "no hard-coded secrets matched"


def c_env_in_tree(root, files):
    hit = any_named(files, {".env", ".env.local", ".env.production", ".env.prod"})
    if hit:
        return False, f"{hit} is present in the tree — confirm it is gitignored and was never committed"
    return True, "no loose .env file in the tree"


def c_error_tracking(root, files):
    hits = grep(root, files, r"sentry|bugsnag|rollbar|honeybadger|opentelemetry|"
                              r"@sentry|ErrorBoundary|global-error|app/error",
                exts=CODE_EXTS | DOC_EXTS)
    return (bool(hits), hits[0] if hits else "no error tracking wired — production errors will be invisible")


def c_health(root, files):
    hits = grep(root, files, r"/health\b|healthz|/api/health|/status\b", exts=CODE_EXTS)
    return (bool(hits), hits[0] if hits else "no health/status route — uptime checks have nothing to hit")


def c_rate_limit(root, files):
    hits = grep(root, files, r"ratelimit|rate[-_]?limit|throttle|slowapi|upstash",
                exts=CODE_EXTS)
    return (bool(hits), hits[0] if hits else "no rate limiting — auth and billing routes are open to abuse")


def c_backups(root, files):
    hits = grep(root, files, r"backup", exts=DOC_EXTS | CODE_EXTS, skip_names_re=r"node_modules")
    return (bool(hits), hits[0] if hits else "no backup plan documented — a lost database loses the business")


def c_restore_drill(root, files):
    hits = grep(root, files, r"restore", exts=DOC_EXTS | CODE_EXTS)
    if not hits:
        return False, "no restore documented — backups you have never restored are a hope, not a backup"
    drilled = grep(root, hits, r"(restore|recovery).{0,40}(test|drill|practice|walkthrough)|"
                                r"(test|drill|practice).{0,40}restore", exts=DOC_EXTS | CODE_EXTS)
    if drilled:
        return True, f"restore drill documented in {drilled[0]}"
    return False, f"restore mentioned in {hits[0]} but no drill recorded — run and record one"


def c_rollback(root, files):
    hits = grep(root, files, r"rollback|roll back|revert", exts=DOC_EXTS | CODE_EXTS)
    return (bool(hits), hits[0] if hits else "no rollback path documented — the first bad deploy has no way back")


def c_uptime(root, files):
    hits = grep(root, files, r"uptime|better ?stack|betteruptime|healthchecks\.io|"
                              r"pingdom|statuspage|/status\b",
                exts=CODE_EXTS | DOC_EXTS)
    return (bool(hits), hits[0] if hits else "no uptime monitoring — you will learn about downtime from a customer")


def c_legal(root, files):
    privacy = grep(root, files, r"privacy", exts=CODE_EXTS | DOC_EXTS)
    terms = grep(root, files, r"terms", exts=CODE_EXTS | DOC_EXTS)
    if privacy and terms:
        return True, f"privacy ({privacy[0]}) and terms ({terms[0]}) present — drafts flagged for a professional"
    missing = "privacy" if not privacy else "terms"
    return False, f"no {missing} page — needed before taking data; a draft flagged for a professional, never final"


def c_data_map(root, files):
    hits = grep(root, files, r"data map|subprocessor|sub-processor|\bDPA\b|GDPR|"
                              r"personal data|data processing",
                exts=DOC_EXTS | CODE_EXTS)
    return (bool(hits), hits[0] if hits else "no data/subprocessor note — you cannot answer a privacy question")


def c_lockfile(root, files):
    hit = any_named(files, {
        "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "poetry.lock",
        "uv.lock", "Pipfile.lock", "go.sum", "composer.lock", "Gemfile.lock", "Cargo.lock",
    })
    return (bool(hit), hit or "no committed lockfile — dependency versions are unowned")


def c_feature_flags(root, files):
    hits = grep(root, files, r"feature[_ -]?flag|featureflag|kill[_ -]?switch|"
                              r"FEATURE_[A-Z]|flags\.", exts=CODE_EXTS)
    return (bool(hits), hits[0] if hits else "no feature flag / kill switch — a bad release needs a redeploy to undo")


def c_debug_off(root, files):
    hits = grep(root, files, r"(debug\s*[:=]\s*true|DEBUG\s*=\s*True|"
                              r"DEBUG\s*=\s*1)",
                exts=CODE_EXTS, skip_names_re=r"example|sample|test|dev")
    return (not hits, "debug mode appears enabled in production code" if hits else "no obvious debug=true in non-dev code")


def c_dep_audit(root, files):
    hit = any_named(files, {"dependabot.yml", "dependabot.yaml", "renovate.json"})
    if hit:
        return True, hit
    wf = grep(root, files, r"npm audit|pip-audit|govulncheck|composer audit|osv-scanner",
              exts={".yml", ".yaml", ".sh"})
    return (bool(wf), wf[0] if wf else "no dependency audit / update bot — known CVEs go unwatched")


def c_sitemap(root, files):
    hit = any_named(files, {"robots.txt", "sitemap.xml"})
    return (bool(hit), hit or "no robots.txt / sitemap — optional for an app, needed if you are also a site")


CHECKS = [
    # (id, label, severity, fn)
    ("secrets", "No secrets in the repo", "blocker", c_secrets),
    ("env_in_tree", "No loose .env committed", "high", c_env_in_tree),
    ("error_tracking", "Error tracking wired", "high", c_error_tracking),
    ("rate_limit", "Rate limiting on sensitive routes", "high", c_rate_limit),
    ("backups", "Backups documented", "high", c_backups),
    ("legal", "Privacy + terms pages", "high", c_legal),
    ("restore_drill", "Restore tested at least once", "medium", c_restore_drill),
    ("rollback", "Rollback path documented", "medium", c_rollback),
    ("uptime", "Uptime monitoring", "medium", c_uptime),
    ("data_map", "Data map / subprocessors", "medium", c_data_map),
    ("lockfile", "Dependency lockfile committed", "medium", c_lockfile),
    ("feature_flags", "Feature flag / kill switch", "medium", c_feature_flags),
    ("debug_off", "Debug mode off in prod", "medium", c_debug_off),
    ("health", "Health/status route", "low", c_health),
    ("dep_audit", "Dependency audit / update bot", "low", c_dep_audit),
    ("sitemap", "robots.txt / sitemap", "low", c_sitemap),
]

SEVERITY_ORDER = ["blocker", "high", "medium", "low"]
SEVERITY_MARK = {"blocker": "BLOCKER", "high": "HIGH   ", "medium": "MEDIUM ", "low": "LOW    "}


def count_checkboxes(root: str, doc_path: str) -> dict | None:
    full = doc_path if os.path.isabs(doc_path) else os.path.join(root, doc_path)
    if not os.path.isfile(full):
        return None
    text = _read(full)
    done = len(re.findall(r"(?m)^\s*[-*]\s*\[[xX]\]", text))
    todo = len(re.findall(r"(?m)^\s*[-*]\s*\[\s\]", text))
    return {"path": doc_path, "ticked": done, "open": todo, "total": done + todo}


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def scan(root: str, strict: bool, doc_path: str | None) -> dict:
    files = collect(root)
    checks = []
    for cid, label, severity, fn in CHECKS:
        ok, detail = fn(root, files)
        checks.append({"id": cid, "label": label, "severity": severity,
                       "status": "pass" if ok else "gap", "detail": detail})

    gaps = [c for c in checks if c["status"] == "gap"]
    blockers = [c for c in gaps if c["severity"] == "blocker"]
    highs = [c for c in gaps if c["severity"] == "high"]

    if blockers or highs:
        verdict = "NOT_READY"
    elif gaps:
        verdict = "READY_WITH_GAPS"
    else:
        verdict = "READY"

    next_step = blockers[0] if blockers else (highs[0] if highs else (gaps[0] if gaps else None))

    return {
        "root": root,
        "files_scanned": len(files),
        "checks": checks,
        "counts": {s: sum(1 for c in gaps if c["severity"] == s) for s in SEVERITY_ORDER},
        "verdict": verdict,
        "next_step": next_step,
        "readiness_doc": count_checkboxes(root, doc_path) if doc_path else None,
    }


def render(result: dict) -> str:
    lines = [f"Launch readiness — {result['root']}", "=" * 60,
             f"({result['files_scanned']} files walked)", ""]
    for sev in SEVERITY_ORDER:
        group = [c for c in result["checks"] if c["severity"] == sev]
        if not group:
            continue
        lines.append(f"{sev.upper()}")
        for c in group:
            mark = "ok " if c["status"] == "pass" else "gap"
            lines.append(f"  [{mark}] {c['label']:<38} — {c['detail']}")
        lines.append("")

    counts = result["counts"]
    lines.append("Gap summary: "
                 f"{counts['blocker']} blocker, {counts['high']} high, "
                 f"{counts['medium']} medium, {counts['low']} low")
    doc = result["readiness_doc"]
    if doc:
        lines.append(f"Readiness doc: {doc['ticked']}/{doc['total']} boxes ticked ({doc['path']})")
    lines.append("")
    lines.append(f"Verdict: {result['verdict']}")
    step = result["next_step"]
    if step is None:
        lines.append("  -> No gaps left. Ship it, then keep the doc and this scan in sync.")
    else:
        lines.append(f"  -> Next: [{step['severity']}] {step['label']}: {step['detail']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Assess a repo's go-live readiness and list gaps by severity.",
        epilog="No input file: this scans a directory tree. Default path is '.'.",
    )
    parser.add_argument("path", nargs="?", default=".", help="repository root to scan (default: .)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--doc", metavar="PATH", help="launch-readiness markdown to count checkboxes in")
    parser.add_argument("--strict", action="store_true", help="fail (exit 1) on any gap, not just blocker/high")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.path):
        sys.stderr.write(f"Error: '{args.path}' is not a directory. Pass the repo root to scan.\n")
        return 2
    if args.doc:
        full = args.doc if os.path.isabs(args.doc) else os.path.join(args.path, args.doc)
        if not os.path.isfile(full) and not os.path.isfile(args.doc):
            sys.stderr.write(f"Error: --doc '{args.doc}' was not found.\n")
            return 2

    result = scan(args.path, args.strict, args.doc)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))

    if result["verdict"] == "NOT_READY":
        return 1
    if args.strict and any(c["status"] == "gap" for c in result["checks"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
