#!/usr/bin/env python3
"""Analyse Van Westendorp Price Sensitivity Meter (PSM) survey responses.

The Price Sensitivity Meter (Van Westendorp, 1976) asks every survey
respondent four price questions about one product:

  1. too_cheap      - so inexpensive you would doubt its quality
  2. cheap          - a real bargain: great value, and you would still buy
  3. expensive      - priced high, but you would still consider buying
  4. too_expensive  - so expensive you would not buy it

For each candidate price p the tool builds four cumulative curves over the
respondents (n = number of respondents):

  too cheap      descending : share whose answer is >= p  (near p=0, ~everyone
                              says "too cheap")
  cheap          descending : share whose answer is >= p  (still a bargain)
  expensive      ascending  : share whose answer is <= p
  too expensive  ascending  : share whose answer is <= p

The classic intersections of these curves are:

  OPP  Optimal Price Point          too cheap    x too expensive
  IDP  Indifference Price Point     expensive    x cheap        (a.k.a. IPP)
  PMC  Point of Marginal Cheapness  too cheap    x expensive
  PME  Point of Marginal Expensiveness  cheap    x too expensive

OPP is the price at which the fewest respondents are pushed away for being
either too cheap or too expensive. IDP is where as many respondents find the
price expensive as find it a bargain. The acceptable price range is
[PMC, PME]; the tool also prints its midpoint as a sanity anchor, because a
single intersection is noisier than the band around it. Treat all of these as
a band to test, never as a number to hardcode.

Input
  A JSON file, a CSV file, or "-" for stdin.
  JSON: an array of objects, or {"responses": [ ... ]}.
  CSV : a header row plus one row per respondent.
  Each record needs the four numeric answers under these names (aliases in
  brackets are accepted):
      too_cheap, cheap [bargain], expensive, too_expensive

  Example JSON:
    [{"too_cheap": 5, "cheap": 12, "expensive": 40, "too_expensive": 60}, ...]

  Example CSV:
    too_cheap,cheap,expensive,too_expensive
    5,12,40,60

Usage
  python3 van_westendorp.py responses.json
  python3 van_westendorp.py responses.csv --json
  cat responses.json | python3 van_westendorp.py - --currency "EUR "

Notes
  - Non-interactive: every input comes from the file argument or stdin.
  - A warning is written to stderr below 15 responses; the intersections are
    too noisy to act on with a small sample (see the companion survey asset).
  - Exit codes: 0 = ran successfully, 2 = usage or input error.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import sys

# The four PSM questions, in report order. First name is the canonical field;
# the rest are accepted aliases so hand-built CSV/JSON rarely needs editing.
FIELDS = [
    ("too_cheap", {"too_cheap", "toocheap", "too_low"}),
    ("cheap", {"cheap", "bargain", "cheap_bargain"}),
    ("expensive", {"expensive", "pricey", "high"}),
    ("too_expensive", {"too_expensive", "tooexpensive", "too_high"}),
]

# The standard method treats a sample below this size as too thin for stable
# intersections. It is a warning threshold, not a hard gate.
MIN_RECOMMENDED = 15


def _normalise_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _canonical_field(key: str) -> str | None:
    normalised = _normalise_key(key)
    for canonical, aliases in FIELDS:
        if normalised in aliases:
            return canonical
    return None


def _coerce_number(value: object, where: str, field: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{where} '{field}' is a boolean, not a price.")
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        text = value.strip().replace(",", "").replace("$", "").replace("€", "").replace("£", "")
        try:
            number = float(text)
        except ValueError:
            raise ValueError(f"{where} '{field}' = {value!r} is not a number.")
    else:
        raise ValueError(f"{where} '{field}' = {value!r} is not a number.")
    if number != number or number in (float("inf"), float("-inf")):
        raise ValueError(f"{where} '{field}' = {value!r} is not a finite number.")
    if number < 0:
        raise ValueError(f"{where} '{field}' = {number} is negative; prices must be >= 0.")
    return number


def _records_from_json(raw: object) -> list[dict]:
    if isinstance(raw, dict) and isinstance(raw.get("responses"), list):
        raw = raw["responses"]
    if not isinstance(raw, list):
        raise ValueError("JSON must be an array of response objects, or {\"responses\": [...]}.")
    if not raw:
        raise ValueError("no responses found in the JSON input.")
    out = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"response[{i}] is not an object.")
        out.append({_normalise_key(k): v for k, v in item.items()})
    return out


def _records_from_csv(text: str) -> list[dict]:
    rows = list(csv.DictReader(text.splitlines()))
    if not rows:
        raise ValueError("the CSV has no data rows (expected a header plus rows).")
    return [{_normalise_key(k): v for k, v in row.items() if k is not None} for row in rows]


def load_responses(path: str) -> dict[str, list[float]]:
    """Read responses and return {field: [sorted numbers]}."""
    if path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
        except FileNotFoundError:
            sys.stderr.write(f"Error: file not found: {path}\n")
            raise SystemExit(2)
        except OSError as exc:
            sys.stderr.write(f"Error: could not read {path}: {exc}\n")
            raise SystemExit(2)

    if not text.strip():
        sys.stderr.write(f"Error: {path} is empty.\n")
        raise SystemExit(2)

    try:
        if path == "-" or text.lstrip()[:1] in "[{":
            records = _records_from_json(json.loads(text))
        else:
            records = _records_from_csv(text)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Error: {path} is not valid JSON: {exc}\n")
        raise SystemExit(2)
    except ValueError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        raise SystemExit(2)

    columns: dict[str, list[float]] = {name: [] for name, _ in FIELDS}
    for i, record in enumerate(records):
        where = f"response[{i}]"
        for name, _aliases in FIELDS:
            present = next((record[k] for k in record if _canonical_field(k) == name), None)
            if present is None:
                sys.stderr.write(
                    f"Error: {where} is missing the '{name}' answer. "
                    f"Each response needs all four: "
                    f"{', '.join(f for f, _ in FIELDS)}.\n"
                )
                raise SystemExit(2)
            try:
                columns[name].append(_coerce_number(present, where, name))
            except ValueError as exc:
                sys.stderr.write(f"Error: {exc}\n")
                raise SystemExit(2)

    for name in columns:
        columns[name].sort()
    return columns


def _desc(curve: list[float], n: int, price: float) -> float:
    """Descending curve: share of respondents whose answer is >= price."""
    return (n - bisect.bisect_left(curve, price)) / n


def _asc(curve: list[float], n: int, price: float) -> float:
    """Ascending curve: share of respondents whose answer is <= price."""
    return bisect.bisect_right(curve, price) / n


def _crossing(grid: list[float], diff) -> float | None:
    """Find a price where diff(price) crosses zero, interpolating linearly.

    grid is sorted and unique. Curves are step functions, so the difference
    changes only at grid points; linear interpolation across the bracketing
    interval gives a stable estimate even when many responses are tied.
    """
    if not grid:
        return None
    prev_price = grid[0]
    prev_diff = diff(prev_price)
    if prev_diff == 0:
        return prev_price
    for price in grid[1:]:
        current = diff(price)
        if current == 0:
            return price
        if (prev_diff > 0) != (current > 0):
            # Solve prev_diff + t * (current - prev_diff) = 0 for t, where t
            # runs from 0 at prev_price to 1 at price. span is non-zero here
            # because the two diffs straddle zero.
            span = prev_diff - current
            t = prev_diff / span
            return prev_price + t * (price - prev_price)
        prev_price, prev_diff = price, current
    return None


def _median(values: list[float]) -> float:
    n = len(values)
    mid = n // 2
    if n % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def analyse(columns: dict[str, list[float]]) -> dict:
    too_cheap = columns["too_cheap"]
    cheap = columns["cheap"]
    expensive = columns["expensive"]
    too_expensive = columns["too_expensive"]
    n = len(too_cheap)

    # The curves are step functions: they only change at a response value, so a
    # genuine crossing always lies between two adjacent values. Inserting the
    # midpoint of each gap lets the scan land inside the gap rather than jump to
    # its far edge when both curves are flat there (common with ties, or when
    # two of the four question ranges do not overlap in a small sample).
    base = sorted({*too_cheap, *cheap, *expensive, *too_expensive})
    grid: list[float] = []
    for i, value in enumerate(base):
        grid.append(value)
        if i + 1 < len(base):
            grid.append((value + base[i + 1]) / 2)

    def opp_diff(p: float) -> float:
        return _desc(too_cheap, n, p) - _asc(too_expensive, n, p)

    def idp_diff(p: float) -> float:
        return _asc(expensive, n, p) - _desc(cheap, n, p)

    def pmc_diff(p: float) -> float:
        return _desc(too_cheap, n, p) - _asc(expensive, n, p)

    def pme_diff(p: float) -> float:
        return _asc(too_expensive, n, p) - _desc(cheap, n, p)

    opp = _crossing(grid, opp_diff)
    idp = _crossing(grid, idp_diff)
    pmc = _crossing(grid, pmc_diff)
    pme = _crossing(grid, pme_diff)

    missing = [name for name, val in
               (("OPP", opp), ("IDP", idp), ("PMC", pmc), ("PME", pme)) if val is None]

    range_mid = None
    if pmc is not None and pme is not None:
        range_mid = (pmc + pme) / 2

    warnings = []
    if n < MIN_RECOMMENDED:
        warnings.append(
            f"only {n} response(s); below {MIN_RECOMMENDED} the intersections are "
            f"unstable — collect more, or lean on interview evidence instead."
        )
    if missing:
        warnings.append(
            "no crossing found for " + ", ".join(missing) +
            " (curves never meet in this sample, often too few or too uniform responses)."
        )
    if pmc is not None and pme is not None and pmc > pme:
        warnings.append(
            "PMC is above PME — the acceptable range is inverted; widen the sample "
            "or check the answers for obvious errors."
        )

    return {
        "responses": n,
        "medians": {name: round(_median(columns[name]), 2) for name, _ in FIELDS},
        "opp": opp,
        "idp": idp,
        "ipp": idp,  # IPP is the same indifference point under the classic method
        "pmc": pmc,
        "pme": pme,
        "acceptable_range": [pmc, pme],
        "range_midpoint": range_mid,
        "warnings": warnings,
    }


def _fmt(value: float | None, currency: str) -> str:
    if value is None:
        return "n/a"
    if abs(value - round(value)) < 1e-9:
        return f"{currency}{int(round(value))}"
    return f"{currency}{value:.2f}"


def render(result: dict, currency: str) -> str:
    lines = []
    lines.append("Van Westendorp Price Sensitivity Meter")
    lines.append("=" * 42)
    lines.append(f"Responses:                 {result['responses']}")
    med = result["medians"]
    lines.append("Median answers:")
    lines.append(f"  too cheap                {_fmt(med['too_cheap'], currency)}")
    lines.append(f"  cheap (bargain)          {_fmt(med['cheap'], currency)}")
    lines.append(f"  expensive                {_fmt(med['expensive'], currency)}")
    lines.append(f"  too expensive            {_fmt(med['too_expensive'], currency)}")
    lines.append("")
    lines.append("Intersections:")
    lines.append(f"  PMC  cheap edge          {_fmt(result['pmc'], currency)}  (too cheap x expensive)")
    lines.append(f"  PME  expensive edge      {_fmt(result['pme'], currency)}  (cheap x too expensive)")
    lines.append(f"  IDP  indifference        {_fmt(result['idp'], currency)}  (expensive x cheap; a.k.a. IPP)")
    lines.append(f"  OPP  optimal price       {_fmt(result['opp'], currency)}  (too cheap x too expensive)")
    lines.append("")
    if result["pmc"] is not None and result["pme"] is not None:
        lines.append(
            f"Acceptable range:          {_fmt(result['pmc'], currency)} "
            f"– {_fmt(result['pme'], currency)}"
        )
        lines.append(f"Range midpoint:            {_fmt(result['range_midpoint'], currency)}")
    else:
        lines.append("Acceptable range:          n/a (PMC and/or PME could not be found)")
    lines.append("")
    lines.append("Read this as a band to test, not a price to set. Triangulate against")
    lines.append("competitor prices and interviews before you change what you charge.")

    if result["warnings"]:
        lines.append("")
        lines.append("Warnings:")
        for warning in result["warnings"]:
            lines.append(f"  - {warning}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compute Van Westendorp Price Sensitivity Meter intersections "
            "(OPP, IDP/IPP, PMC, PME) from survey responses."
        ),
        epilog=(
            "Input is a JSON array / {\"responses\": [...]} (or a CSV with a header) "
            "where each record carries the four numeric answers: too_cheap, cheap, "
            "expensive, too_expensive. Use '-' to read from stdin. "
            "The acceptable range is [PMC, PME]. Exit 2 on usage/input error."
        ),
    )
    parser.add_argument("input", help="path to a JSON or CSV response file, or '-' for stdin")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")
    parser.add_argument("--currency", default="$", help="currency symbol used in text output (default: $)")
    args = parser.parse_args(argv)

    columns = load_responses(args.input)
    result = analyse(columns)

    for warning in result["warnings"]:
        sys.stderr.write(f"Warning: {warning}\n")

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result, args.currency))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
