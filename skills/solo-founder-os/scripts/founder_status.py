#!/usr/bin/env python3
"""Report which solo-founder workspace artifacts exist, are empty, or are missing.

Scans a `founder/` directory (or a path you pass) and prints a checklist of the
expected artifacts in lifecycle order, a completion percentage, and the single
most-in-need-of-attention next step. Something that exists but has no content is
reported as "empty", not "present" — a copied-but-unfilled template is not progress.

Usage:
    python3 founder_status.py                 # scan ./founder
    python3 founder_status.py path/to/founder
    python3 founder_status.py --json
    python3 founder_status.py --help

Expected artifacts (lifecycle order):
    context.md                 shared brief   (all skills / solo-founder-os)
    validation/go-no-go.md     go/no-go brief (idea-validation)
    product/mvp-spec.md        MVP spec       (mvp-scoping)
    pricing/pricing.md         pricing brief  (pricing-strategy)
    gtm/launch-plan.md         launch plan    (go-to-market-launch)
    metrics/metrics-spec.md    metrics spec   (product-metrics)
    ops/weekly-review.md       weekly review  (founder-operating-rhythm)

Statuses: present | empty (exists but no content) | missing.
The directory itself being absent is not an error: it just means the bootstrap
has not run yet, and the next step says so.

Exit codes: 0 = ran successfully, 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# Lifecycle-ordered expected artifacts. Order matters: the "next step" is the
# first gap in this sequence, so the list doubles as the recommended build order.
ARTIFACTS = [
    {
        "id": "context",
        "skill": "solo-founder-os",
        "path": "context.md",
        "label": "shared brief",
        "action": "Bootstrap: create founder/ and copy assets/context.md to founder/context.md, filled in.",
    },
    {
        "id": "validation",
        "skill": "idea-validation",
        "path": "validation/go-no-go.md",
        "label": "go/no-go brief",
        "action": "Run idea-validation to produce founder/validation/go-no-go.md.",
    },
    {
        "id": "product",
        "skill": "mvp-scoping",
        "path": "product/mvp-spec.md",
        "label": "MVP spec",
        "action": "Run mvp-scoping to produce founder/product/mvp-spec.md.",
    },
    {
        "id": "pricing",
        "skill": "pricing-strategy",
        "path": "pricing/pricing.md",
        "label": "pricing brief",
        "action": "Run pricing-strategy to produce founder/pricing/pricing.md.",
    },
    {
        "id": "gtm",
        "skill": "go-to-market-launch",
        "path": "gtm/launch-plan.md",
        "label": "launch plan",
        "action": "Run go-to-market-launch to produce founder/gtm/launch-plan.md.",
    },
    {
        "id": "metrics",
        "skill": "product-metrics",
        "path": "metrics/metrics-spec.md",
        "label": "metrics spec",
        "action": "Run product-metrics to produce founder/metrics/metrics-spec.md.",
    },
    {
        "id": "ops",
        "skill": "founder-operating-rhythm",
        "path": "ops/weekly-review.md",
        "label": "weekly review",
        "action": "Run founder-operating-rhythm to produce founder/ops/weekly-review.md.",
    },
]

STATUS_MARK = {"present": "[x]", "empty": "[~]", "missing": "[ ]"}


def status_of(workspace: str, rel_path: str) -> str:
    """Return present | empty | missing for one artifact (rel_path uses '/')."""
    full = os.path.join(workspace, *rel_path.split("/"))
    if not os.path.isfile(full):
        return "missing"
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except OSError:
        return "missing"
    if content.strip() == "":
        return "empty"
    return "present"


def scan(workspace: str) -> dict:
    rows = []
    for spec in ARTIFACTS:
        rows.append({**spec, "status": status_of(workspace, spec["path"])})

    present = sum(1 for r in rows if r["status"] == "present")
    total = len(rows)
    percent = round(100 * present / total) if total else 0

    next_step = next((r for r in rows if r["status"] != "present"), None)

    return {
        "workspace": workspace,
        "exists": os.path.isdir(workspace),
        "completion": {"present": present, "total": total, "percent": percent},
        "artifacts": rows,
        "next_step": next_step,
    }


def render(result: dict) -> str:
    lines = []
    workspace = result["workspace"]
    lines.append(f"Founder workspace status — {workspace}")
    lines.append("=" * 60)

    if not result["exists"]:
        lines.append("")
        lines.append(f"'{workspace}/' does not exist yet. Nothing is set up — run the")
        lines.append("solo-founder-os bootstrap to create the folder tree and context.md.")

    lines.append("")
    lines.append("Checklist (lifecycle order):")
    for r in result["artifacts"]:
        mark = STATUS_MARK[r["status"]]
        lines.append(
            f"  {mark} {r['path']:<24} {r['status']:<7} — {r['label']} ({r['skill']})"
        )

    c = result["completion"]
    lines.append("")
    lines.append(f"Completion: {c['present']}/{c['total']} artifacts present ({c['percent']}%)")

    lines.append("")
    lines.append("Most in need of attention:")
    step = result["next_step"]
    if step is None:
        lines.append("  -> All expected artifacts are present. Keep them current —")
        lines.append("     re-run this check after each lifecycle pass.")
    else:
        lines.append(f"  -> [{step['skill']}] {step['action']}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report which solo-founder workspace artifacts exist, are empty, or are missing.",
        epilog="No input file: this scans a directory. Default path is './founder'.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="founder",
        help="founder/ directory to scan (default: founder)",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON instead of text"
    )
    args = parser.parse_args(argv)

    if os.path.exists(args.path) and not os.path.isdir(args.path):
        sys.stderr.write(
            f"Error: '{args.path}' is not a directory. Pass the founder/ folder "
            f"(e.g. 'python3 founder_status.py founder').\n"
        )
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
