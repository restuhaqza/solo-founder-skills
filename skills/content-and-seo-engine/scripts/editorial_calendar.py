#!/usr/bin/env python3
"""Generate a dated editorial calendar for a pillar-and-cluster content program.

Given a start date, a cadence, one pillar topic, and any number of supporting
piece topics, this emits one scheduled row per piece: date, type
(pillar|supporting), title, a target-query placeholder, and status. Output is
deterministic and sorted by date.

Usage:
    python3 editorial_calendar.py --start 2026-11-03 --cadence monthly \
        --pillar "How to invoice freelance design clients" \
        --piece "Freelance invoice template that clients pay" \
        --piece "Invoice vs contract: what designers need"

    python3 editorial_calendar.py --start 2026-11-03 --cadence weekly \
        --pillar "Topic" --piece "A" --piece "B" --weeks 6 --format csv

    python3 editorial_calendar.py --help

Input schema
    --start    YYYY-MM-DD   first publish date (the pillar lands here)
    --cadence  weekly | biweekly | monthly
                           gap between consecutive pieces. weekly = 7 days,
                           biweekly = 14 days, monthly = one calendar month.
    --pillar   "..."        the single pillar topic (exactly one)
    --piece    "..."        a supporting topic; repeat for each piece
    --weeks    N            optional. Total program length in weeks. When set,
                           all pieces are spread evenly across N weeks instead
                           of using the cadence gap. The pillar still lands on
                           the start date.

Output columns: date, type, title, target_query, status.

Exit codes: 0 = ran successfully, 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import calendar
import csv
import io
import json
import sys
from datetime import date, timedelta

# Days between consecutive pieces for the day-based cadences. "monthly" is
# handled separately with real calendar arithmetic so it never drifts.
CADENCE_DAYS = {
    "weekly": 7,
    "biweekly": 14,
}
CADENCES = ("weekly", "biweekly", "monthly")


def parse_start(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        sys.stderr.write(
            f"Error: --start '{value}' is not a valid date. Expected YYYY-MM-DD "
            f"(e.g. 2026-11-03).\n"
        )
        raise SystemExit(2)


def add_months(day: date, months: int) -> date:
    """Return `day` shifted forward by `months`, clamping to month end."""
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day.day, last_day))


def build_rows(args, start: date) -> list[dict]:
    topics = [(args.pillar, "pillar")]
    topics.extend((piece, "supporting") for piece in args.piece)

    if args.weeks is not None:
        # Spread every piece evenly across N weeks so the last one lands inside
        # the horizon. The pillar stays on the start date.
        span_days = args.weeks * 7
        count = len(topics)
        step = span_days / count if count else 0.0
        dates = [start + timedelta(days=round(i * step)) for i in range(count)]
    elif args.cadence == "monthly":
        dates = [add_months(start, i) for i in range(len(topics))]
    else:
        step = CADENCE_DAYS[args.cadence]
        dates = [start + timedelta(days=step * i) for i in range(len(topics))]

    rows = []
    for (topic, kind), day in zip(topics, dates):
        rows.append(
            {
                "date": day.isoformat(),
                "type": kind,
                "title": topic,
                "target_query": f"{topic} — target query TBD",
                "status": "planned",
            }
        )
    # Deterministic order: by date, then pillar before supporting, then title.
    rows.sort(key=lambda r: (r["date"], 0 if r["type"] == "pillar" else 1, r["title"]))
    return rows


def render_markdown(rows: list[dict]) -> str:
    header = ["Date", "Type", "Title", "Target query", "Status"]
    lines = [
        "# Editorial Calendar",
        "",
        f"_{len(rows)} piece(s) scheduled._",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for r in rows:
        cells = [r["date"], r["type"], r["title"], r["target_query"], r["status"]]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_csv(rows: list[dict]) -> str:
    buffer = io.StringIO()
    fields = ["date", "type", "title", "target_query", "status"]
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().rstrip("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a dated editorial calendar for a content program.",
        epilog="See the docstring at the top of this file for the input schema.",
    )
    parser.add_argument("--start", required=True, help="first publish date, YYYY-MM-DD")
    parser.add_argument(
        "--cadence",
        required=True,
        choices=CADENCES,
        help="gap between consecutive pieces: weekly, biweekly, or monthly",
    )
    parser.add_argument("--pillar", required=True, help="the single pillar topic")
    parser.add_argument(
        "--piece",
        action="append",
        default=[],
        metavar="TOPIC",
        help="a supporting topic; repeat the flag for each piece",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=None,
        metavar="N",
        help="optional: spread all pieces evenly across N weeks total",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "csv"),
        default="markdown",
        help="output format (default: markdown)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of the chosen text format",
    )
    args = parser.parse_args(argv)

    if args.weeks is not None and args.weeks < 1:
        parser.error("--weeks must be a positive integer number of weeks")

    start = parse_start(args.start)
    rows = build_rows(args, start)

    if args.json:
        json.dump(rows, sys.stdout, indent=2)
        sys.stdout.write("\n")
    elif args.format == "csv":
        sys.stdout.write(render_csv(rows) + "\n")
    else:
        sys.stdout.write(render_markdown(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
