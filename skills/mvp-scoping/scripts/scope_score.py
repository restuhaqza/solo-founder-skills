#!/usr/bin/env python3
"""Score candidate MVP features and draw a v1 cut line (the 90/10 rule).

Reads a CSV of candidate features, scores each with a RICE-ish formula, sorts
them, guarantees every must-have is in v1, then adds the next-highest scores
until the included set has kept `--target` (default 0.90) of the total score.
Prints an in/out table with the share of value retained, and flags items that
are likely to wreck a solo build (high effort, low confidence).

Usage:
    python3 scope_score.py features.csv
    python3 scope_score.py features.csv --target 0.80
    python3 scope_score.py features.csv --json
    python3 scope_score.py --help

Input schema (CSV, header required):
    id,name,impact,confidence,effort,must_have
    F1,"Create + send an invoice",5,4,3,yes

    id          short stable key for the feature
    name        human label (quote it if it contains a comma)
    impact      1-5  value to the customer if shipped
    confidence  1-5  how sure you are the impact is real (1 = a guess)
    effort      1-5  build + maintain cost for ONE person (5 = a weekend-less month)
    must_have   yes/no — the product does not function without it
    Extra columns (e.g. notes) are ignored.

Scoring
    score = impact * confidence / effort
    Dividing by effort is the whole point: a high-impact feature that eats your
    month can lose to a modest one you can ship this week. Confidence is a
    multiplier, not a footnote — an unvalidated 5-impact guess should not
    out-rank a proven 3.

V1 cut
    All must_have=yes features are included unconditionally, then remaining
    features are added in descending score until the included score reaches
    `--target` (default 0.90) of the total score. target=0.90 encodes the
    Buchheit rule: keep the slice of features that carries ~90% of the value.

Flags
    [effort]     effort >= 4 — too big for a first slice; split or defer it.
    [confidence] confidence <= 2 — you are guessing; test it before building it.

Exit codes: 0 = ran successfully, 2 = input/usage error.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys

REQUIRED_COLUMNS = ["id", "name", "impact", "confidence", "effort", "must_have"]
YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
DEFAULT_TARGET = 0.90

# Effort at or above this is a red flag for a solo first slice (1-5 scale).
EFFORT_FLAG_THRESHOLD = 4
# Confidence at or below this means the impact is a guess (1-5 scale).
CONFIDENCE_FLAG_THRESHOLD = 2


def fail(message: str) -> "None":
    sys.stderr.write(f"Error: {message}\n")
    raise SystemExit(2)


def parse_int(raw: str, column: str, row_number: int, row_id: str) -> int:
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        fail(
            f"row {row_number} (id '{row_id}') column '{column}' is '{raw}', "
            f"expected an integer 1-5."
        )
    if not 1 <= value <= 5:
        fail(
            f"row {row_number} (id '{row_id}') column '{column}' is {value}, "
            f"expected 1-5."
        )
    return value


def parse_must_have(raw: str, row_number: int, row_id: str) -> bool:
    token = str(raw).strip().lower()
    if token in YES:
        return True
    if token in NO:
        return False
    fail(
        f"row {row_number} (id '{row_id}') column 'must_have' is '{raw}', "
        f"expected yes/no."
    )


def load_features(path: str) -> list[dict]:
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None:
                fail(f"{path} is empty; expected a header row: {','.join(REQUIRED_COLUMNS)}")
            header = [(name or "").strip().lower() for name in reader.fieldnames]
            missing = [c for c in REQUIRED_COLUMNS if c not in header]
            if missing:
                fail(
                    f"{path} is missing column(s): {', '.join(missing)}. "
                    f"Expected header: {','.join(REQUIRED_COLUMNS)}"
                )
            features = []
            seen_ids: set[str] = set()
            for i, row in enumerate(reader, start=2):  # row 1 is the header
                norm = {(k or "").strip().lower(): (v or "") for k, v in row.items()}
                row_id = norm.get("id", "").strip()
                name = norm.get("name", "").strip()
                if not row_id and not name:
                    continue  # skip blank lines
                if not row_id:
                    fail(f"row {i} has a name but no id.")
                if row_id in seen_ids:
                    fail(f"row {i} repeats id '{row_id}'; ids must be unique.")
                seen_ids.add(row_id)
                features.append(
                    {
                        "id": row_id,
                        "name": name or row_id,
                        "impact": parse_int(norm.get("impact"), "impact", i, row_id),
                        "confidence": parse_int(
                            norm.get("confidence"), "confidence", i, row_id
                        ),
                        "effort": parse_int(norm.get("effort"), "effort", i, row_id),
                        "must_have": parse_must_have(
                            norm.get("must_have"), i, row_id
                        ),
                    }
                )
    except FileNotFoundError:
        fail(f"file not found: {path}")
    except UnicodeDecodeError:
        fail(f"{path} is not readable as UTF-8 text.")
    if not features:
        fail(f"{path} has a valid header but no feature rows.")
    return features


def score_features(features: list[dict], target: float) -> dict:
    for f in features:
        f["score"] = f["impact"] * f["confidence"] / f["effort"]

    total_score = sum(f["score"] for f in features)

    # Rank by score descending; id is a stable tiebreaker so runs are reproducible.
    ranked = sorted(features, key=lambda f: (-f["score"], f["id"]))

    included_ids = {f["id"] for f in ranked if f["must_have"]}
    included_score = sum(f["score"] for f in ranked if f["must_have"])

    target_score = total_score * target
    for f in ranked:
        if included_score >= target_score:
            break
        if f["id"] in included_ids:
            continue
        included_ids.add(f["id"])
        included_score += f["score"]

    kept = included_score / total_score if total_score > 0 else 0.0

    for f in features:
        f["in_v1"] = f["id"] in included_ids
        f["flags"] = []
        if f["effort"] >= EFFORT_FLAG_THRESHOLD:
            f["flags"].append("effort")
        if f["confidence"] <= CONFIDENCE_FLAG_THRESHOLD:
            f["flags"].append("confidence")

    return {
        "total_score": round(total_score, 3),
        "target": target,
        "target_score": round(target_score, 3),
        "included_score": round(included_score, 3),
        "value_retained": round(kept, 3),
        "in_v1_count": sum(1 for f in features if f["in_v1"]),
        "out_v1_count": sum(1 for f in features if not f["in_v1"]),
        "features": ranked,
    }


def render(result: dict) -> str:
    lines = []
    lines.append("MVP scope score")
    lines.append("=" * 78)
    lines.append(
        f"score = impact * confidence / effort   |   v1 target = "
        f"{result['target']:.0%} of total score"
    )
    lines.append(
        f"features: {len(result['features'])}   "
        f"in v1: {result['in_v1_count']}   "
        f"parked: {result['out_v1_count']}   "
        f"value retained: {result['value_retained']:.0%}"
    )
    lines.append("")
    lines.append(
        f"{'v1':<3} {'id':<6} {'imp':>3} {'conf':>4} {'eff':>3} {'score':>6} "
        f"{'must':<4} {'flags':<18} name"
    )
    lines.append("-" * 78)
    for f in result["features"]:
        mark = "IN" if f["in_v1"] else "--"
        flags = ",".join(f["flags"]) if f["flags"] else ""
        must = "yes" if f["must_have"] else ""
        name = f["name"]
        if len(name) > 30:
            name = name[:27] + "..."
        lines.append(
            f"{mark:<3} {f['id']:<6} {f['impact']:>3} {f['confidence']:>4} "
            f"{f['effort']:>3} {f['score']:>6.2f} {must:<4} {flags:<18} {name}"
        )
    lines.append("-" * 78)

    flagged = [f for f in result["features"] if f["flags"] and f["in_v1"]]
    if flagged:
        lines.append("")
        lines.append("Watch these even though they are in v1:")
        for f in flagged:
            reasons = []
            if "effort" in f["flags"]:
                reasons.append("effort >= 4 — split it into smaller slices")
            if "confidence" in f["flags"]:
                reasons.append("confidence <= 2 — test the impact before building")
            lines.append(f"  - [{f['id']}] {f['name']}: " + "; ".join(reasons))

    parked = [f for f in result["features"] if not f["in_v1"]]
    if parked:
        lines.append("")
        lines.append("Parked (the anti-scope list) — revisit only after v1 ships:")
        for f in parked:
            lines.append(f"  - [{f['id']}] {f['name']}  (score {f['score']:.2f})")

    lines.append("")
    lines.append(
        "The cut is a proposal, not a verdict. Every IN feature should trace to an "
        "exit criterion; if one does not, move it out."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score candidate MVP features and draw a v1 cut line (90/10 rule).",
        epilog=(
            "Score = impact * confidence / effort. Must-haves are always in v1; "
            "then features are added top-score-first until --target of the total "
            "score is retained. Exit 2 on usage/input error."
        ),
    )
    parser.add_argument("input", help="path to a features CSV (id,name,impact,confidence,effort,must_have)")
    parser.add_argument(
        "--target",
        type=float,
        default=DEFAULT_TARGET,
        help=f"fraction of total score v1 must retain (default {DEFAULT_TARGET}); 0 < target <= 1",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON instead of text"
    )
    args = parser.parse_args(argv)

    if not (0.0 < args.target <= 1.0):
        fail(f"--target must be greater than 0 and at most 1, got {args.target}.")

    features = load_features(args.input)
    result = score_features(features, args.target)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
