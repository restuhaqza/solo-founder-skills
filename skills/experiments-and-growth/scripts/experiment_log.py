#!/usr/bin/env python3
"""Audit a growth experiment log and recommend scale / iterate / kill.

Reads a CSV of experiments against a growth constraint. For each experiment it
checks whether the result met the target given the direction, recommends a
decision for every finished experiment, flags hygiene problems (a finished
experiment with no result, a running experiment past its end date, a finished
experiment with no decision), prints a summary table, and ends in the single
next action to take.

Usage:
    python3 experiment_log.py experiment-log.csv
    python3 experiment_log.py experiment-log.csv --json
    python3 experiment_log.py experiment-log.csv --margin 0.10 --close-factor 0.80
    python3 experiment_log.py --sample-size --baseline-rate 0.10 --mde 0.20
    python3 experiment_log.py --help

Input schema (CSV), header required, one row per experiment:
    id,name,hypothesis,metric,baseline,target,direction,start,end,result,status,decision
    - id          : short unique label, e.g. E1
    - direction   : up | down   ("up" = good when the metric rises)
    - baseline    : the pre-experiment value of the metric (numeric)
    - target      : the value you hoped to reach (numeric)
    - start,end   : ISO dates YYYY-MM-DD
    - result      : the observed metric value; blank until the experiment ends
    - status      : planned | running | done | abandoned
    - decision    : the call you recorded, e.g. SCALE | ITERATE | KILL (blank until decided)

Decision thresholds (recommendation for a finished experiment)
    Let ratio = result/target when direction is up, and target/result when
    direction is down. ratio >= 1 means the target was met.
        SCALE   ratio >= 1 + margin          (met, with margin)
        ITERATE close_factor <= ratio < 1+margin   (close, worth one more pass)
        KILL    ratio < close_factor          (clearly missed)
        KILL    abandoned                     (no outcome to carry forward)
    margin defaults to 0.0, so by default "met" scales. Raise --margin to
    require the result to beat the target by that fraction before you scale.
    close_factor defaults to 0.80 (within 20% of target counts as close).

--sample-size mode (two-proportion test)
    Computes the per-variant sample size for detecting a relative change in a
    rate, using the standard normal-approximation formula for two independent
    proportions with equal allocation:

        n = ceil( (z_{1-alpha/2} + z_{power})^2
                  * (p1*(1-p1) + p2*(1-p2))
                  / (p1 - p2)^2 )

    where p1 = --baseline-rate, p2 = p1 * (1 + --mde), and the z values are
    inverse normal CDFs (stdlib statistics.NormalDist). This is the unpooled
    approximation used to plan sample size; it ignores continuity correction,
    so round up. --alpha defaults to 0.05, --power to 0.80. The printed "total"
    is 2 * n for the two variants.

Exit codes: 0 = ran successfully, 2 = input/usage error.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import date
from statistics import NormalDist

REQUIRED_COLUMNS = [
    "id",
    "name",
    "hypothesis",
    "metric",
    "baseline",
    "target",
    "direction",
    "start",
    "end",
    "result",
    "status",
    "decision",
]

VALID_DIRECTIONS = {"up", "down"}
VALID_STATUSES = {"planned", "running", "done", "abandoned"}

# A finished experiment counts as "close" when the achieved/target ratio is at
# or above this fraction; below it the experiment is a clear miss and gets KILL.
DEFAULT_CLOSE_FACTOR = 0.80
# How far beyond the target a result must land before it is scaled by default.
DEFAULT_MARGIN = 0.0


def die(message: str, code: int = 2) -> None:
    """Print an error to stderr and exit with the given code."""
    sys.stderr.write(f"Error: {message}\n")
    raise SystemExit(code)


def parse_float(value: str, field: str, row_id: str, allow_blank: bool = False):
    text = (value or "").strip()
    if text == "":
        if allow_blank:
            return None
        die(f"experiment '{row_id}': column '{field}' is empty but a number is required")
    try:
        return float(text)
    except ValueError:
        die(f"experiment '{row_id}': column '{field}' value '{text}' is not a number")


def parse_date(value: str, field: str, row_id: str) -> date:
    text = (value or "").strip()
    try:
        return date.fromisoformat(text)
    except ValueError:
        die(f"experiment '{row_id}': column '{field}' value '{text}' is not a YYYY-MM-DD date")


def load_experiments(path: str) -> list[dict]:
    try:
        fh = open(path, "r", encoding="utf-8-sig", newline="")
    except FileNotFoundError:
        die(f"file not found: {path}")

    with fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            die(f"{path} is empty; expected a header row: {','.join(REQUIRED_COLUMNS)}")

        headers = [h.strip() for h in reader.fieldnames]
        missing = [c for c in REQUIRED_COLUMNS if c not in headers]
        if missing:
            die(
                f"{path} is missing required column(s): {', '.join(missing)}. "
                f"Expected: {','.join(REQUIRED_COLUMNS)}"
            )

        experiments: list[dict] = []
        seen_ids: set[str] = set()
        for lineno, raw in enumerate(reader, start=2):
            row = {(k or "").strip(): (v or "").strip() for k, v in raw.items()}
            if all(value == "" for value in row.values()):
                continue  # tolerate blank lines

            row_id = row["id"] or f"(line {lineno})"
            if row["id"] in seen_ids:
                die(f"duplicate experiment id '{row['id']}' on line {lineno}")
            seen_ids.add(row["id"])

            direction = row["direction"].lower()
            if direction not in VALID_DIRECTIONS:
                die(
                    f"experiment '{row_id}': direction '{row['direction']}' is invalid. "
                    f"Options: {', '.join(sorted(VALID_DIRECTIONS))}"
                )
            status = row["status"].lower()
            if status not in VALID_STATUSES:
                die(
                    f"experiment '{row_id}': status '{row['status']}' is invalid. "
                    f"Options: {', '.join(sorted(VALID_STATUSES))}"
                )

            start = parse_date(row["start"], "start", row_id) if row["start"] else None
            end = parse_date(row["end"], "end", row_id) if row["end"] else None

            experiments.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "hypothesis": row["hypothesis"],
                    "metric": row["metric"],
                    "baseline": parse_float(row["baseline"], "baseline", row_id),
                    "target": parse_float(row["target"], "target", row_id),
                    "direction": direction,
                    "start": start.isoformat() if start else "",
                    "end": end.isoformat() if end else "",
                    "end_date": end,
                    "result": parse_float(row["result"], "result", row_id, allow_blank=True),
                    "status": status,
                    "decision": row["decision"],
                }
            )

    if not experiments:
        die(f"{path} has no experiment rows (only a header)")
    return experiments


def achieved_ratio(exp: dict) -> float | None:
    """Return result/target (up) or target/result (down); >=1 means met."""
    result = exp["result"]
    target = exp["target"]
    if result is None:
        return None
    if exp["direction"] == "down":
        if result <= 0:
            # A non-positive result on a down-metric is a total win, not a divide-by-zero.
            return math.inf if target > 0 else None
        return target / result
    if target == 0:
        return None
    return result / target


def recommend(exp: dict, margin: float, close_factor: float) -> str | None:
    """Return SCALE / ITERATE / KILL for a finished experiment, else None."""
    if exp["status"] == "abandoned":
        return "KILL"
    if exp["status"] != "done":
        return None
    ratio = achieved_ratio(exp)
    if ratio is None:
        return None  # no result to judge on
    if ratio >= 1.0 + margin:
        return "SCALE"
    if ratio >= close_factor:
        return "ITERATE"
    return "KILL"


def collect_flags(experiments: list[dict], today: date) -> list[dict]:
    flags: list[dict] = []
    for exp in experiments:
        if exp["status"] == "done" and exp["result"] is None:
            flags.append({"id": exp["id"], "kind": "no-result", "message": "finished (done) but no result recorded"})
        if exp["status"] == "running" and exp["end_date"] and exp["end_date"] < today:
            flags.append(
                {"id": exp["id"], "kind": "overdue", "message": f"still running but its end date {exp['end']} has passed"}
            )
        if exp["status"] in ("done", "abandoned") and not exp["decision"]:
            flags.append({"id": exp["id"], "kind": "no-decision", "message": "finished but no decision recorded"})
    return flags


def next_action(experiments: list[dict], flags: list[dict], recommendations: list[dict]) -> str:
    """Return the single most useful next action, hygiene problems first."""
    no_result = [f for f in flags if f["kind"] == "no-result"]
    if no_result:
        return f"Record the result for {no_result[0]['id']} — a finished experiment is not done until its result is in."

    overdue = [f for f in flags if f["kind"] == "overdue"]
    if overdue:
        return f"Close out {overdue[0]['id']} — it is past its end date; record the result or abandon it with a reason."

    no_decision = [f for f in flags if f["kind"] == "no-decision"]
    if no_decision:
        return f"Decide {no_decision[0]['id']} — record SCALE, ITERATE, or KILL before starting anything new."

    scale = [r for r in recommendations if r["recommendation"] == "SCALE"]
    if scale:
        ids = ", ".join(r["id"] for r in scale)
        return f"Scale {ids} — met the target; carry the winner forward and start the next single experiment."

    running = [e for e in experiments if e["status"] == "running"]
    if running:
        return f"Let {running[0]['id']} run to its end date; do not start a second experiment until it is decided."

    planned = [e for e in experiments if e["status"] == "planned"]
    if planned:
        return f"Start {planned[0]['id']} — it is planned but not yet running."

    iterate = [r for r in recommendations if r["recommendation"] == "ITERATE"]
    if iterate:
        return f"Iterate {iterate[0]['id']} — it came close; sharpen the change and re-run against the same metric."

    return "No experiment is in flight — write the next hypothesis against the binding constraint and log it."


def analyze(experiments: list[dict], today: date, margin: float, close_factor: float) -> dict:
    counts: dict[str, int] = {s: 0 for s in VALID_STATUSES}
    for exp in experiments:
        counts[exp["status"]] += 1

    recommendations = []
    for exp in experiments:
        call = recommend(exp, margin, close_factor)
        if call is None and exp["status"] != "abandoned":
            continue
        ratio = achieved_ratio(exp)
        recommendations.append(
            {
                "id": exp["id"],
                "metric": exp["metric"],
                "direction": exp["direction"],
                "result": exp["result"],
                "target": exp["target"],
                "ratio": None if ratio is None else round(ratio, 3),
                "met": None if ratio is None else ratio >= 1.0,
                "recommendation": call,
            }
        )

    flags = collect_flags(experiments, today)
    return {
        "today": today.isoformat(),
        "counts": counts,
        "recommendations": recommendations,
        "flags": flags,
        "next_action": next_action(experiments, flags, recommendations),
    }


def render(result: dict, path: str) -> str:
    lines: list[str] = []
    lines.append("EXPERIMENT LOG")
    lines.append(f"{path}  -  audited {result['today']}")
    lines.append("=" * 72)
    counts = result["counts"]
    lines.append(
        "status: "
        + "  ".join(f"{s}={counts[s]}" for s in ("planned", "running", "done", "abandoned"))
    )

    lines.append("")
    if result["recommendations"]:
        lines.append("Finished experiments (achieved/target ratio, >=1 means met):")
        lines.append(f"  {'id':<6}{'metric':<18}{'result':>10}{'target':>10}{'ratio':>8}  call")
        for rec in result["recommendations"]:
            ratio = "n/a" if rec["ratio"] is None else f"{rec['ratio']:.3f}"
            res = "n/a" if rec["result"] is None else f"{rec['result']:g}"
            metric = rec["metric"][:17]
            lines.append(
                f"  {rec['id']:<6}{metric:<18}{res:>10}{rec['target']:>10g}{ratio:>8}  {rec['recommendation']}"
            )
    else:
        lines.append("Finished experiments: none yet.")

    lines.append("")
    if result["flags"]:
        lines.append("Flags:")
        for flag in result["flags"]:
            lines.append(f"  - [{flag['id']}] {flag['message']}")
    else:
        lines.append("Flags: none — no hygiene problems found.")

    lines.append("")
    lines.append(f"NEXT ACTION: {result['next_action']}")
    return "\n".join(lines)


def sample_size(baseline: float, mde: float, alpha: float, power: float) -> dict:
    """Per-variant sample size for a two-proportion test (see module docstring)."""
    if not 0.0 < baseline < 1.0:
        die(f"--baseline-rate must be strictly between 0 and 1, got {baseline:g}")
    if mde == 0.0:
        die("--mde must be non-zero (a relative effect to detect, e.g. 0.20 for +20%)")
    if not 0.0 < alpha < 1.0:
        die(f"--alpha must be strictly between 0 and 1, got {alpha:g}")
    if not 0.0 < power < 1.0:
        die(f"--power must be strictly between 0 and 1, got {power:g}")

    p1 = baseline
    p2 = p1 * (1.0 + mde)
    if not 0.0 < p2 < 1.0:
        die(
            f"--baseline-rate {p1:g} with --mde {mde:g} gives a comparison rate of "
            f"{p2:.4g}, which must be between 0 and 1"
        )

    z_alpha = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    z_power = NormalDist().inv_cdf(power)
    variance = p1 * (1.0 - p1) + p2 * (1.0 - p2)
    delta = p1 - p2
    per_variant = math.ceil((z_alpha + z_power) ** 2 * variance / (delta**2))

    return {
        "baseline_rate": p1,
        "relative_mde": mde,
        "comparison_rate": round(p2, 6),
        "absolute_delta": round(abs(delta), 6),
        "alpha": alpha,
        "power": power,
        "z_alpha": round(z_alpha, 4),
        "z_power": round(z_power, 4),
        "per_variant": per_variant,
        "total": per_variant * 2,
    }


def render_sample_size(s: dict) -> str:
    lines: list[str] = []
    lines.append("SAMPLE SIZE — two-proportion test (equal allocation)")
    lines.append("=" * 60)
    lines.append(f"baseline rate    : {s['baseline_rate']:g}")
    lines.append(f"relative MDE     : {s['relative_mde']:+.1%}")
    lines.append(f"comparison rate  : {s['comparison_rate']:g}")
    lines.append(f"absolute delta   : {s['absolute_delta']:g}")
    lines.append(f"alpha / power    : {s['alpha']:g} / {s['power']:g}")
    lines.append(f"z_alpha, z_power : {s['z_alpha']:g}, {s['z_power']:g}")
    lines.append("-" * 60)
    lines.append(f"per variant      : {s['per_variant']:,}")
    lines.append(f"total (both)     : {s['total']:,}")
    lines.append("")
    lines.append(
        "This is a planning estimate (normal approximation, no continuity "
        "correction). If your traffic cannot reach this in the time you are "
        "willing to wait, make a bigger change rather than testing a small one."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a growth experiment log and recommend scale / iterate / kill, "
            "or compute a two-proportion sample size."
        ),
        epilog=(
            "Decision thresholds and the sample-size formula are documented in the "
            "docstring at the top of this file. See also the input schema there."
        ),
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="path to the experiment-log CSV (omit when using --sample-size)",
    )
    parser.add_argument(
        "--sample-size",
        action="store_true",
        help="compute per-variant sample size for a two-proportion test instead of auditing the log",
    )
    parser.add_argument(
        "--baseline-rate",
        type=float,
        metavar="P",
        help="baseline conversion rate, 0-1 (with --sample-size)",
    )
    parser.add_argument(
        "--mde",
        type=float,
        metavar="R",
        help="relative minimum detectable effect, e.g. 0.20 for +20%% (with --sample-size)",
    )
    parser.add_argument("--alpha", type=float, default=0.05, help="significance level (default: 0.05)")
    parser.add_argument("--power", type=float, default=0.80, help="statistical power (default: 0.80)")
    parser.add_argument(
        "--margin",
        type=float,
        default=DEFAULT_MARGIN,
        help=f"extra fraction beyond target required to SCALE (default: {DEFAULT_MARGIN:g})",
    )
    parser.add_argument(
        "--close-factor",
        type=float,
        default=DEFAULT_CLOSE_FACTOR,
        help=f"ratio at or above this counts as close -> ITERATE (default: {DEFAULT_CLOSE_FACTOR:g})",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")
    parser.add_argument(
        "--today",
        metavar="YYYY-MM-DD",
        help="override today's date (default: system date); used for the overdue check",
    )
    args = parser.parse_args(argv)

    if args.sample_size:
        if args.input is not None:
            die("--sample-size does not take an input file; use --baseline-rate and --mde")
        if args.baseline_rate is None or args.mde is None:
            die("--sample-size requires --baseline-rate and --mde")
        result = sample_size(args.baseline_rate, args.mde, args.alpha, args.power)
        if args.json:
            json.dump(result, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(render_sample_size(result))
        return 0

    if args.input is None:
        die("missing input: pass a path to the experiment-log CSV, or use --sample-size")

    if args.margin < 0:
        die("--margin must be zero or greater")
    if not 0.0 <= args.close_factor <= 1.0:
        die("--close-factor must be between 0 and 1")

    if args.today:
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            die(f"--today value '{args.today}' is not a YYYY-MM-DD date")
    else:
        today = date.today()

    experiments = load_experiments(args.input)
    result = analyze(experiments, today, args.margin, args.close_factor)
    result["input"] = args.input

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result, args.input))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
