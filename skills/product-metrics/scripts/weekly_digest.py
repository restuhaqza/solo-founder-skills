#!/usr/bin/env python3
"""Build a one-page weekly business-review digest from a metrics CSV.

Reads a CSV whose first column is `date` (YYYY-MM-DD) and whose remaining
columns are numeric metrics (e.g. mrr, new_customers, churned_mrr,
active_users, activation_rate). It computes period-over-period deltas, flags
metrics that moved beyond a threshold, ranks metrics by ADVERSE movement, and
prints a digest whose FINAL line is exactly ONE recommended action derived
from the worst-moving metric.

Usage:
    python3 weekly_digest.py metrics.csv
    python3 weekly_digest.py metrics.csv --period mom --threshold 15
    python3 weekly_digest.py metrics.csv --higher-is-better mrr,active_users
    python3 weekly_digest.py metrics.csv --json
    python3 weekly_digest.py --help

Metric polarity -- which direction counts as "good":
    1. A header suffix wins. `name:up` or `name:+` is good when the value
       rises; `name:down` or `name:-` is good when the value falls (churn,
       support load, CAC). Example: `churned_mrr:down`.
    2. Otherwise a metric named in --lower-is-better is good when it falls,
       and a metric named in --higher-is-better is good when it rises.
    3. Otherwise the default is "good when up" (revenue, users, conversion).
    A metric may not be in both lists, and a suffix may not contradict a list.

--period:
    wow (default) compares the latest row with the previous row.
    mom compares the latest row with the row 4 rows earlier. This assumes the
    CSV is weekly; on monthly rows use wow to mean "month over month".

Input schema (CSV):
    date,mrr,new_customers,churned_mrr:down,failed_payments_mrr:down
    2026-02-16,3120,6,180,60
    2026-02-23,3240,7,150,55
    Rows are read in file order; the last row is "latest".

Output:
    Text digest on stdout (or a JSON object with --json). Diagnostics go to
    stderr. Exit 0 on success, 2 on a usage or input error.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys

# A period is expressed as a number of rows to step back from the latest row.
PERIOD_STEPS = {"wow": 1, "mom": 4}

# Header suffixes that declare polarity explicitly.
SUFFIX_UP = (":up", ":+", ":higher")
SUFFIX_DOWN = (":down", ":-", ":lower")
DEFAULT_THRESHOLD = 10.0  # percent; a move this large is worth flagging


def die(message: str, code: int = 2) -> None:
    """Print an error to stderr and exit with the given code."""
    sys.stderr.write(f"Error: {message}\n")
    raise SystemExit(code)


def split_header(name: str) -> tuple[str, bool | None]:
    """Return (base_name, polarity). polarity True = good up, False = good down."""
    low = name.strip().lower()
    for suffix in SUFFIX_UP:
        if low.endswith(suffix):
            return name[: len(name) - len(suffix)].strip(), True
    for suffix in SUFFIX_DOWN:
        if low.endswith(suffix):
            return name[: len(name) - len(suffix)].strip(), False
    return name.strip(), None


def parse_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def load_rows(path: str) -> tuple[list[str], list[dict]]:
    """Read and validate the CSV. Returns (metric_headers, rows)."""
    try:
        fh = open(path, "r", encoding="utf-8-sig", newline="")
    except FileNotFoundError:
        die(f"file not found: {path}")

    with fh:
        reader = csv.reader(fh)
        try:
            header = [h.strip() for h in next(reader)]
        except StopIteration:
            die(f"{path} is empty; expected a header row starting with 'date'")

        if not header or header[0].lower() != "date":
            got = header[0] if header else "(nothing)"
            die(f"first column must be 'date', found '{got}'")

        metrics = header[1:]
        if not metrics:
            die("no metric columns found after 'date'")

        rows: list[dict] = []
        for lineno, raw in enumerate(reader, start=2):
            if not raw or all(cell.strip() == "" for cell in raw):
                continue  # tolerate blank lines between weeks
            if len(raw) != len(header):
                die(f"line {lineno}: expected {len(header)} columns, found {len(raw)}")
            record: dict = {"date": raw[0].strip()}
            for name, value in zip(metrics, raw[1:]):
                try:
                    record[name] = float(value)
                except ValueError:
                    die(f"line {lineno}: column '{name}' value '{value}' is not numeric")
            rows.append(record)

    if len(rows) < 2:
        die(f"need at least 2 data rows to compute a delta, found {len(rows)}")
    return metrics, rows


def resolve_polarity(
    metrics: list[str], higher: list[str], lower: list[str]
) -> dict[str, bool]:
    """Map each metric header to True (good when up) or False (good when down)."""
    overlap = set(higher) & set(lower)
    if overlap:
        die(f"metric(s) listed as both higher- and lower-is-better: {', '.join(sorted(overlap))}")

    polarity: dict[str, bool] = {}
    for raw in metrics:
        base, suffix = split_header(raw)
        if suffix is not None:
            if base in lower and suffix is True:
                die(f"'{raw}' has an 'up' suffix but is listed in --lower-is-better")
            if base in higher and suffix is False:
                die(f"'{raw}' has a 'down' suffix but is listed in --higher-is-better")
            polarity[raw] = suffix
        elif base in lower or raw in lower:
            polarity[raw] = False
        elif base in higher or raw in higher:
            polarity[raw] = True
        else:
            polarity[raw] = True  # default: more is better
    return polarity


def analyze(
    metrics: list[str],
    rows: list[dict],
    polarity: dict[str, bool],
    step: int,
    threshold: float,
) -> dict:
    """Compute deltas, flags and adverse ranking for every metric."""
    latest, previous = rows[-1], rows[-1 - step]
    items = []
    for raw in metrics:
        cur = latest[raw]
        prev = previous[raw]
        base, _ = split_header(raw)
        good_up = polarity[raw]
        if prev == 0:
            pct = None
            adverse = None
            flagged = False
        else:
            pct = (cur - prev) / abs(prev) * 100.0
            # Adverse movement is positive when things got worse.
            adverse = (-pct) if good_up else pct
            flagged = abs(pct) > threshold
        items.append(
            {
                "metric": base,
                "header": raw,
                "latest": cur,
                "previous": prev,
                "change_pct": None if pct is None else round(pct, 2),
                "good_when_up": good_up,
                "adverse_pct": None if adverse is None else round(adverse, 2),
                "anomaly": flagged,
            }
        )

    ranked = sorted(
        (i for i in items if i["adverse_pct"] is not None),
        key=lambda i: i["adverse_pct"],
        reverse=True,
    )
    worst = ranked[0] if ranked and ranked[0]["adverse_pct"] > 0 else None

    # Inferred involuntary-churn line, only when both columns are present.
    involuntary = None
    by_base = {i["metric"].lower(): i for i in items}
    if "churned_mrr" in by_base and "failed_payments_mrr" in by_base:
        churned = by_base["churned_mrr"]["latest"]
        failed = by_base["failed_payments_mrr"]["latest"]
        if churned:
            involuntary = {
                "churned_mrr": churned,
                "failed_payments_mrr": failed,
                "share_pct": round(failed / churned * 100.0, 1),
            }

    return {
        "latest_date": latest["date"],
        "previous_date": previous["date"],
        "items": items,
        "ranked": ranked,
        "worst": worst,
        "involuntary_churn": involuntary,
    }


def _playbook(metric: str) -> str:
    """Return the tailored fix for a metric, or '' for the generic fallback."""
    return {
        "mrr": "recover {m} by pulling this week's downgrades and cancellations and talking to the accounts that dropped",
        "revenue": "recover {m} by pulling this week's downgrades and cancellations and talking to the accounts that dropped",
        "arr": "recover {m} by pulling this week's downgrades and cancellations and talking to the accounts that dropped",
        "churned_mrr": "attack {m} by exporting the accounts that cancelled this week, splitting voluntary from involuntary, and starting a dunning sequence on the failed cards today",
        "churn_rate": "attack {m} by exporting the accounts that cancelled this week and naming the top reason before the next review",
        "failed_payments_mrr": "switch on dunning for {m}: enable smart retries plus a 3-email failed-payment sequence in your billing tool",
        "new_customers": "diagnose {m}: find which channel stopped producing and ship one fix against your single best channel this week",
        "signups": "diagnose {m}: find which channel stopped producing and ship one fix against your single best channel this week",
        "trials": "diagnose {m}: check the top-of-funnel step that changed before touching the product",
        "activation_rate": "fix {m}: confirm the one activation event, then remove the steps between signup and reaching it",
        "active_users": "re-engage at-risk accounts behind {m}: find users with no core action in 14-21 days and send the win-back sequence",
    }.get(metric.lower(), "")


def recommend(worst: dict | None, window: str) -> str:
    """Build the single recommended action. Always returns one sentence."""
    if worst is None:
        return (
            "No metric moved adversely beyond noise this week -- hold the current "
            "plan and re-check next week."
        )
    metric = worst["metric"]
    trend = "rose" if worst["change_pct"] > 0 else "fell"
    mag = abs(worst["change_pct"])
    template = _playbook(metric)
    if template:
        return template.format(m=metric) + f" (it {trend} {mag:.1f}% {window})."
    return (
        f"investigate {metric}: it {trend} {mag:.1f}% {window} -- find the cause "
        "before changing anything else."
    )


def render(result: dict, period: str, threshold: float) -> str:
    window = "week over week" if period == "wow" else "over the last 4 periods"
    lines: list[str] = []
    lines.append("WEEKLY DIGEST")
    lines.append(
        f"latest {result['latest_date']} vs {result['previous_date']} "
        f"({period})  -  threshold {threshold:g}%"
    )
    lines.append("=" * 66)
    lines.append(f"{'metric':<20}{'latest':>11}{'prev':>11}{'change':>11}  flag")
    for item in result["ranked"]:
        change = item["change_pct"]
        change_txt = "n/a" if change is None else f"{change:+.1f}%"
        flag = "ANOMALY" if item["anomaly"] else ""
        lines.append(
            f"{item['metric']:<20}{item['latest']:>11.2f}{item['previous']:>11.2f}"
            f"{change_txt:>11}  {flag}"
        )
    lines.append("")
    lines.append("Ranked by adverse movement (worst first):")
    adverse_only = [i for i in result["ranked"] if i["adverse_pct"] > 0]
    if adverse_only:
        for rank, item in enumerate(adverse_only, start=1):
            pol = "good when up" if item["good_when_up"] else "good when down"
            lines.append(
                f"  {rank}. {item['metric']:<18} {item['change_pct']:+.1f}%  ({pol})"
            )
    else:
        lines.append("  none - every metric moved in a favourable or flat direction")

    if result["involuntary_churn"]:
        inv = result["involuntary_churn"]
        lines.append("")
        lines.append(
            f"Involuntary churn share: {inv['share_pct']:.1f}% of churned MRR "
            f"(failed_payments_mrr {inv['failed_payments_mrr']:g} / "
            f"churned_mrr {inv['churned_mrr']:g}) -- dunning is the fastest lever."
        )

    lines.append("")
    decision = recommend(result["worst"], window)
    lines.append(f"RECOMMENDATION: {decision[0].upper()}{decision[1:]}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Turn a metrics CSV into a one-page weekly digest ending in one action.",
        epilog=(
            "Metric polarity: a header suffix (name:up / name:down) wins; else "
            "--lower-is-better / --higher-is-better name it; else the default is "
            "'good when up'. See the docstring at the top of this file for the "
            "full input schema and period semantics."
        ),
    )
    parser.add_argument("input", help="path to the metrics CSV (first column 'date')")
    parser.add_argument(
        "--period",
        choices=sorted(PERIOD_STEPS),
        default="wow",
        help="comparison window: wow = previous row, mom = 4 rows back (default: wow)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"percent move that flags an anomaly (default: {DEFAULT_THRESHOLD:g})",
    )
    parser.add_argument(
        "--higher-is-better",
        default="",
        metavar="A,B",
        help="comma-separated metrics that are good when they rise",
    )
    parser.add_argument(
        "--lower-is-better",
        default="",
        metavar="A,B",
        help="comma-separated metrics that are good when they fall (e.g. churn)",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON instead of text"
    )
    args = parser.parse_args(argv)

    if args.threshold < 0:
        die("--threshold must be zero or greater")

    metrics, rows = load_rows(args.input)
    polarity = resolve_polarity(
        metrics, parse_list(args.higher_is_better), parse_list(args.lower_is_better)
    )

    step = PERIOD_STEPS[args.period]
    if len(rows) <= step:
        die(f"--period {args.period} needs at least {step + 1} data rows, found {len(rows)}")

    result = analyze(metrics, rows, polarity, step, args.threshold)
    window = "week over week" if args.period == "wow" else "over the last 4 periods"
    result["period"] = args.period
    result["threshold"] = args.threshold
    result["recommendation"] = recommend(result["worst"], window)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result, args.period, args.threshold))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
