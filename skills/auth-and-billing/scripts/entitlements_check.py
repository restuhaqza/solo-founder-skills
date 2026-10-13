#!/usr/bin/env python3
"""Lint the entitlement matrix that maps plans to features.

Reads the CSV written for `auth-and-billing` (columns: `feature` plus one column
per plan, e.g. `feature,free,starter,pro`) and checks it for the mistakes that
turn into billing bugs or refund requests: duplicate features, plans with no real
upgrade path, paid plans that are worse than free, numeric limits that fall as the
plan rises, unrecognised values, and mixed boolean/numeric value styles.

Usage:
    python3 entitlements_check.py founder/product/entitlements.csv
    python3 entitlements_check.py --json founder/product/entitlements.csv
    python3 entitlements_check.py --strict founder/product/entitlements.csv

Accepted cell values:
    yes/no            (also y/n, true/false, included/none, on/off, ✓/-)
    unlimited         (also inf, ∞, -1)
    a positive integer limit (e.g. 3, 25, 1000)

The first plan column is treated as the baseline (the free/trial tier) unless a
column literally named `free` or `trial` exists, which is then used as baseline.

Output: errors, warnings, the normalised matrix, and a per-plan gate count, each
followed by the single next thing to fix. Exit 0 = no errors (warnings allowed),
1 = errors found, 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys

YES_TOKENS = {"yes", "y", "true", "included", "include", "on", "✓", "✔"}
NO_TOKENS = {"no", "n", "false", "none", "-", "—", "off", ""}
UNLIMITED_TOKENS = {"unlimited", "inf", "infinite", "∞", "-1", "unmetered"}
BASELINE_NAMES = {"free", "trial", "hobby"}

# Value kinds, in the order they rank for "is this plan better than the baseline".
KIND_NO = "no"
KIND_NUM = "num"
KIND_YES = "yes"
KIND_UNLIMITED = "unlimited"
KIND_TEXT = "text"


def classify(raw: str) -> tuple[str, object]:
    """Return (kind, value) for a cell. Unknown values come back as text."""
    token = raw.strip().lower()
    if token in YES_TOKENS:
        return KIND_YES, True
    if token in NO_TOKENS:
        return KIND_NO, False
    if token in UNLIMITED_TOKENS:
        return KIND_UNLIMITED, None
    if re.fullmatch(r"\d+", token):
        return KIND_NUM, int(token)
    return KIND_TEXT, raw.strip()


def level(kind: str, value: object) -> float:
    """A comparable 'how much does this plan give' score for monotonicity."""
    if kind == KIND_NO:
        return -1.0
    if kind == KIND_UNLIMITED:
        return float("inf")
    if kind == KIND_YES:
        return 1.0        # a boolean feature the plan has, above absence
    if kind == KIND_NUM:
        return float(value)
    return -2.0           # text values are not orderable


def load(path: str) -> tuple[list[str], list[str], list[list[str]]]:
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        rows = [r for r in csv.reader(fh) if any(cell.strip() for cell in r)]
    if not rows:
        raise ValueError("the CSV is empty")
    header = [h.strip() for h in rows[0]]
    if header and header[0].lower() not in {"feature", "features", "capability"}:
        raise ValueError("first column must be 'feature' (the row label)")
    plans = header[1:]
    if not plans:
        raise ValueError("need at least one plan column after 'feature'")
    body = rows[1:]
    for i, r in enumerate(body, start=2):
        if len(r) != len(header):
            raise ValueError(f"row {i} has {len(r)} cells but the header has {len(header)}")
    return plans, header, body


def lint(plans: list[str], header: list[str], body: list[list[str]]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    baseline_idx = 1
    for i, p in enumerate(plans, start=1):
        if p.strip().lower() in BASELINE_NAMES:
            baseline_idx = i
            break
    baseline_name = plans[baseline_idx - 1]

    seen: dict[str, int] = {}
    normalised_rows: list[dict] = []

    for rownum, raw_row in enumerate(body, start=2):
        feature = raw_row[0].strip()
        if not feature:
            errors.append(f"row {rownum}: empty feature name")
            continue
        key = feature.lower()
        if key in seen:
            errors.append(f"row {rownum}: duplicate feature '{feature}' (first seen row {seen[key]})")
            continue
        seen[key] = rownum

        kinds: list[str] = []
        values: list[object] = []
        cells: list[str] = []
        for plan, raw in zip(plans, raw_row[1:]):
            kind, value = classify(raw)
            kinds.append(kind)
            values.append(value)
            cells.append(raw.strip())
            if kind == KIND_TEXT:
                warnings.append(
                    f"row {rownum} ('{feature}', plan '{plan}'): unrecognised value "
                    f"'{raw.strip()}' — use yes/no, unlimited, or an integer"
                )

        # Mixing numeric limits with a plain yes/no in one row is ambiguous; a numeric
        # limit that ends in "unlimited" is idiomatic and must NOT be flagged.
        kindset = {k for k in kinds if k not in (KIND_TEXT,)}
        if KIND_NUM in kindset and KIND_YES in kindset:
            warnings.append(
                f"row {rownum} ('{feature}'): mixes numeric limits and yes/no — "
                f"pick one style so upgrades are comparable"
            )

        base_kind, base_val = kinds[baseline_idx - 1], values[baseline_idx - 1]

        # A paid plan worse than the baseline on any feature is a bug.
        for i, plan in enumerate(plans, start=1):
            if i == baseline_idx or plan.strip().lower() in BASELINE_NAMES:
                continue
            kind, val = kinds[i - 1], values[i - 1]
            if base_kind in (KIND_YES, KIND_UNLIMITED) and kind == KIND_NO:
                errors.append(
                    f"row {rownum} ('{feature}'): plan '{plan}' is NO but baseline "
                    f"'{baseline_name}' has it — a paid plan worse than free"
                )
            if base_kind == KIND_NUM and kind == KIND_NUM and level(kind, val) < level(base_kind, base_val):
                warnings.append(
                    f"row {rownum} ('{feature}'): '{plan}' limit {val} is below baseline "
                    f"'{baseline_name}' limit {base_val} — limits should rise with the plan"
                )

        # Numeric limits should rise across a tier sequence.
        nums = [(plans[i], values[i]) for i, k in enumerate(kinds) if k == KIND_NUM]
        for (p1, v1), (p2, v2) in zip(nums, nums[1:]):
            if v2 < v1:
                warnings.append(
                    f"row {rownum} ('{feature}'): limit falls from {v1} ('{p1}') "
                    f"to {v2} ('{p2}')"
                )

        normalised_rows.append({
            "feature": feature,
            "cells": cells,
            "kinds": kinds,
            "baseline": {"kind": base_kind, "value": base_val},
        })

    # Every paid plan should have at least one feature the baseline does NOT have,
    # otherwise there is no reason to upgrade.
    for i, plan in enumerate(plans, start=1):
        if i == baseline_idx or plan.strip().lower() in BASELINE_NAMES:
            continue
        advantage = False
        for raw_row in body:
            if len(raw_row) <= i:
                continue
            bkind, bval = classify(raw_row[baseline_idx])
            ckind, cval = classify(raw_row[i])
            if bkind in (KIND_NO, KIND_TEXT) and ckind in (KIND_YES, KIND_UNLIMITED, KIND_NUM):
                advantage = True
                break
            if bkind == KIND_NUM and ckind == KIND_UNLIMITED:
                advantage = True
                break
            if bkind == KIND_NUM and ckind == KIND_NUM and isinstance(bval, int) and isinstance(cval, int) and cval > bval:
                advantage = True
                break
        if not advantage:
            warnings.append(
                f"plan '{plan}' has no feature its baseline '{baseline_name}' lacks — "
                f"no reason for anyone to upgrade to it"
            )

    gate_counts: dict[str, int] = {}
    for i, plan in enumerate(plans):
        count = 0
        for row in normalised_rows:
            k = row["kinds"][i]
            if k == KIND_NO:
                count += 1
        gate_counts[plan] = count

    return {
        "baseline": baseline_name,
        "plans": plans,
        "errors": errors,
        "warnings": warnings,
        "rows": normalised_rows,
        "gate_counts": gate_counts,
    }


def render(result: dict) -> str:
    lines = []
    lines.append("Entitlement matrix check — baseline: '%s'" % result["baseline"])
    lines.append("=" * 60)
    for err in result["errors"]:
        lines.append(f"  ERROR   {err}")
    for warn in result["warnings"]:
        lines.append(f"  WARN    {warn}")
    if not result["errors"] and not result["warnings"]:
        lines.append("  No problems found.")

    lines.append("")
    lines.append("Normalised matrix:")
    lines.append("  " + " | ".join(result["plans"]))
    for row in result["rows"]:
        lines.append(f"  {row['feature']:<20} " + " | ".join(str(c) for c in row["cells"]))

    lines.append("")
    lines.append("Gated features per plan (features set to 'no'):")
    for plan, count in result["gate_counts"].items():
        lines.append(f"  {plan:<20} {count} gate(s)")

    lines.append("")
    lines.append("Next step:")
    if result["errors"]:
        lines.append("  -> Fix the errors first — they are entitlement bugs users would hit.")
    elif result["warnings"]:
        lines.append("  -> Review the warnings; each one is a package decision worth making on purpose.")
    else:
        lines.append("  -> Matrix is consistent. Wire it into the app and mirror it in the pricing page.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint a plan-vs-feature entitlement CSV for billing bugs.",
        epilog="Input schema: a CSV whose first column is 'feature' and whose remaining "
               "columns are plans. See assets/entitlements.csv for the shape.",
    )
    parser.add_argument("path", help="path to the entitlements CSV")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--strict", action="store_true",
        help="treat warnings as failures (exit 1 if any warning is present)",
    )
    args = parser.parse_args(argv)

    try:
        plans, header, body = load(args.path)
    except OSError:
        sys.stderr.write(f"Error: cannot read '{args.path}'.\n")
        return 2
    except ValueError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 2

    result = lint(plans, header, body)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))

    if result["errors"]:
        return 1
    if args.strict and result["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
