#!/usr/bin/env python3
"""Score idea-validation evidence and produce a go/no-go scorecard.

Reads a JSON file describing an idea's risky assumptions and the evidence
collected for each, then prints a weighted scorecard, the coverage of testing,
the strongest counter-evidence, and a verdict band.

Usage:
    python3 evidence_scorecard.py assumptions.json
    python3 evidence_scorecard.py assumptions.json --json
    python3 evidence_scorecard.py --help

Input schema (JSON):
{
  "idea": "one-line description",
  "assumptions": [
    {
      "id": "V1",
      "type": "value | viability | usability | feasibility",
      "claim": "freelance designers already pay >= $30/mo for invoicing",
      "status": "untested | refuted | weak | supported | strong",
      "note": "optional: 3 of 8 interviewees pre-paid $49"
    }
  ]
}

Scoring
  status -> score : untested 0.0 | refuted 0.0 | weak 0.33 | supported 0.66 | strong 1.0
  type weight     : value 3 | viability 3 | usability 1 | feasibility 1
  The weighted score is computed over *tested* assumptions only; coverage is the
  fraction of weighted assumptions that have been tested.

Verdict bands
  INSUFFICIENT EVIDENCE  any value/viability assumption is still untested (cannot proceed)
  PROCEED                weighted score >= 0.70 and coverage >= 0.75
  KEEP VALIDATING        weighted score >= 0.45
  PIVOT THE ASSUMPTION   weighted score >= 0.25
  KILL                   otherwise

Exit codes: 0 = ran successfully, 2 = input/usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter

STATUS_SCORE = {
    "untested": 0.0,
    "refuted": 0.0,
    "weak": 0.33,
    "supported": 0.66,
    "strong": 1.0,
}

TYPE_WEIGHT = {
    "value": 3.0,
    "viability": 3.0,
    "usability": 1.0,
    "feasibility": 1.0,
}

# Assumption types that gate the verdict: while any of these is untested the
# evidence is too thin to proceed, no matter how good the other scores look.
GATING_TYPES = {"value", "viability"}


def load_assumptions(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        sys.stderr.write(f"Error: file not found: {path}\n")
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Error: {path} is not valid JSON: {exc}\n")
        raise SystemExit(2)

    if not isinstance(data, dict) or not isinstance(data.get("assumptions"), list):
        sys.stderr.write("Error: expected a JSON object with an 'assumptions' array.\n")
        raise SystemExit(2)

    for i, item in enumerate(data["assumptions"]):
        if not isinstance(item, dict):
            sys.stderr.write(f"Error: assumptions[{i}] is not an object.\n")
            raise SystemExit(2)
        atype = str(item.get("type", "")).lower()
        status = str(item.get("status", "")).lower()
        if atype not in TYPE_WEIGHT:
            sys.stderr.write(
                f"Error: assumptions[{i}].type '{item.get('type')}' is invalid. "
                f"Options: {', '.join(TYPE_WEIGHT)}\n"
            )
            raise SystemExit(2)
        if status not in STATUS_SCORE:
            sys.stderr.write(
                f"Error: assumptions[{i}].status '{item.get('status')}' is invalid. "
                f"Options: {', '.join(STATUS_SCORE)}\n"
            )
            raise SystemExit(2)
    return data


def score(data: dict) -> dict:
    assumptions = data["assumptions"]
    tested_weight = 0.0
    total_weight = 0.0
    earned = 0.0
    by_type: dict[str, Counter] = {}
    gating_untested = []
    counter_evidence = []
    supporting_evidence = []

    for a in assumptions:
        atype = str(a["type"]).lower()
        status = str(a["status"]).lower()
        weight = TYPE_WEIGHT[atype]
        total_weight += weight
        by_type.setdefault(atype, Counter())[status] += 1

        if status == "untested":
            if atype in GATING_TYPES:
                gating_untested.append(a)
            continue

        tested_weight += weight
        earned += weight * STATUS_SCORE[status]

        if status in ("refuted", "weak"):
            counter_evidence.append(a)
        elif status == "strong":
            supporting_evidence.append(a)

    weighted = (earned / tested_weight) if tested_weight > 0 else 0.0
    coverage = (tested_weight / total_weight) if total_weight > 0 else 0.0

    if gating_untested:
        verdict = "INSUFFICIENT EVIDENCE"
    elif weighted >= 0.70 and coverage >= 0.75:
        verdict = "PROCEED"
    elif weighted >= 0.45:
        verdict = "KEEP VALIDATING"
    elif weighted >= 0.25:
        verdict = "PIVOT THE ASSUMPTION"
    else:
        verdict = "KILL"

    return {
        "idea": data.get("idea", "(untitled)"),
        "verdict": verdict,
        "weighted_score": round(weighted, 3),
        "coverage": round(coverage, 3),
        "counts": {t: dict(c) for t, c in sorted(by_type.items())},
        "gating_untested": gating_untested,
        "counter_evidence": counter_evidence,
        "supporting_evidence": supporting_evidence,
    }


def render(result: dict) -> str:
    lines = []
    lines.append(f"Idea: {result['idea']}")
    lines.append("=" * 60)
    lines.append(f"Verdict:        {result['verdict']}")
    lines.append(f"Weighted score: {result['weighted_score']:.3f}  (tested assumptions only)")
    lines.append(f"Coverage:       {result['coverage']:.0%} of weighted assumptions tested")
    lines.append("")
    lines.append("Assumptions by type:")
    for atype, counts in result["counts"].items():
        pretty = ", ".join(f"{k}={v}" for k, v in counts.items())
        lines.append(f"  {atype:<12} {pretty}")

    if result["gating_untested"]:
        lines.append("")
        lines.append("BLOCKING — value/viability assumptions still untested:")
        for a in result["gating_untested"]:
            lines.append(f"  - [{a.get('id', '?')}] {a.get('claim', '')}")

    if result["counter_evidence"]:
        lines.append("")
        lines.append("Strongest evidence AGAINST:")
        for a in result["counter_evidence"]:
            note = f" — {a['note']}" if a.get("note") else ""
            lines.append(f"  - [{a.get('id', '?')}] ({a['status']}) {a.get('claim', '')}{note}")

    if result["supporting_evidence"]:
        lines.append("")
        lines.append("Strongest evidence FOR:")
        for a in result["supporting_evidence"]:
            note = f" — {a['note']}" if a.get("note") else ""
            lines.append(f"  - [{a.get('id', '?')}] {a.get('claim', '')}{note}")

    lines.append("")
    lines.append("Reminder: this scorecard informs a decision, it does not make it. The")
    lines.append("founder owns the go/no-go call.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score idea-validation evidence into a go/no-go scorecard.",
        epilog="See the docstring at the top of this file for the input schema.",
    )
    parser.add_argument("input", help="path to the assumptions/evidence JSON file")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")
    args = parser.parse_args(argv)

    data = load_assumptions(args.input)
    result = score(data)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
