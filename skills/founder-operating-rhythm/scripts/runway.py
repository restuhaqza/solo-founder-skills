#!/usr/bin/env python3
"""Project cash runway, break-even, and the default-alive/default-dead verdict.

Takes the four numbers a solo founder actually knows — cash on hand, current
monthly revenue, monthly costs, and the monthly revenue growth rate — and
returns how many months of cash are left, when (if ever) revenue covers costs,
how much to set aside for tax, and whether the business is *default alive* or
*default dead*.

Usage:
    python3 runway.py --cash 120000 --revenue 8000 --costs 14000 --growth 6
    python3 runway.py --cash 20000 --revenue 5000 --costs 9000 --growth 0 --json
    python3 runway.py --help

Definitions
    net monthly burn  = costs - revenue      (positive means you are burning)
    runway (months)    = cash / net monthly burn
    break-even month   = first month where growing revenue >= monthly costs
                         (0 = already there; "never" = flat or declining)
    default alive      = revenue reaches costs within the cash runway
                         (Paul Graham's test; a company with no burn is alive)
    default dead       = it does not
    flip growth rate   = the smallest monthly growth (%) that pulls break-even
                         inside the runway. Hold at or above it and the verdict
                         is default alive; fall below it and it is default dead.
                         Reported on both the pre-tax and after-tax runway,
                         because the after-tax basis needs a faster growth rate.

Tax set-aside assumption
    The set-aside is modelled as --tax-rate (default 0.30) of *gross monthly
    revenue*, reserved in the month it is collected — a planning buffer, not a
    filing or a liability calculation. "Runway (after tax)" re-runs the runway
    with only revenue * (1 - tax-rate) available to cover costs. What you
    actually owe is decided by you and your accountant, not by this script.

Exit codes: 0 = ran successfully, 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import json
import math
import sys

# Default share of gross revenue kept aside for tax. A habit, not law: 25-30%
# is the range most solo founders use. Override with --tax-rate.
DEFAULT_TAX_RATE = 0.30

# Default projection horizon in months. Long enough to see a break-even, short
# enough that the projection stays honest.
DEFAULT_MONTHS = 24


def positive(value: str) -> float:
    """argparse type: a number >= 0, else a usage error."""
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a number, got '{value}'")
    if number < 0:
        raise argparse.ArgumentTypeError(f"expected a number >= 0, got '{value}'")
    return number


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a whole number, got '{value}'")
    if number < 1:
        raise argparse.ArgumentTypeError(f"expected a whole number >= 1, got '{value}'")
    return number


def money(amount: float) -> str:
    return f"${amount:,.0f}"


def months_str(value: float | None) -> str:
    return "no burn" if value is None else f"{value:.1f} months"


def growth_pct_str(value: float | None) -> str:
    return "unreachable" if value is None else f"{value:.1f}%"


def growth_to_flip(cash: float, revenue: float, costs: float, tax_rate: float, after_tax: bool) -> float | None:
    """Smallest monthly revenue growth (%) that makes the business default alive.

    The verdict flips from default dead to default alive the moment break-even
    lands inside the runway, and faster growth pulls break-even earlier. Solving
    ``ln(costs/revenue) / ln(1 + g/100) <= runway`` for ``g`` gives that rate.
    Returns ``0.0`` when any non-negative growth keeps you alive (already
    break-even, or too little burn to matter), ``None`` when no growth rate can
    save you (no revenue, or no cash and not yet profitable), else the rate.
    """
    if revenue >= costs:
        return 0.0  # already break-even; nothing to grow into
    if revenue <= 0:
        return None  # zero revenue stays zero however fast it "grows"
    collectable = revenue * (1.0 - tax_rate) if after_tax else revenue
    net_burn = costs - collectable
    if net_burn <= 0:
        return 0.0  # the burn you can fund is already covered
    if cash <= 0:
        return None
    runway = cash / net_burn
    ratio = costs / revenue
    return max(0.0, 100.0 * (ratio ** (1.0 / runway) - 1.0))


def compute(args: argparse.Namespace) -> dict:
    cash = args.cash
    revenue = args.revenue
    costs = args.costs
    growth = args.growth  # percent per month, may be 0 or negative
    tax_rate = args.tax_rate
    horizon = args.months

    growth_factor = 1.0 + (growth / 100.0)
    net_burn = costs - revenue  # > 0 means burning cash

    # Runway: infinite when revenue already covers costs.
    if net_burn <= 0:
        runway_months = None
    elif cash <= 0:
        runway_months = 0.0
    else:
        runway_months = cash / net_burn

    # After-tax view: reserve tax_rate of revenue before it can cover costs.
    reserve = tax_rate * max(revenue, 0.0)
    net_burn_after_tax = costs - revenue * (1.0 - tax_rate)
    if net_burn_after_tax <= 0:
        runway_after_tax = None
    elif cash <= 0:
        runway_after_tax = 0.0
    else:
        runway_after_tax = cash / net_burn_after_tax

    # Break-even: first month (from now) that revenue >= costs.
    if revenue >= costs:
        break_even_month = 0
    elif revenue <= 0 or growth <= 0:
        # Zero revenue stays zero however fast it "grows", and flat or shrinking
        # revenue never closes the gap; both mean revenue never reaches costs.
        break_even_month = None
    else:
        exact = math.log(costs / revenue) / math.log(growth_factor)
        break_even_month = max(1, math.ceil(exact - 1e-9))

    # Default alive / dead (Paul Graham's test).
    if net_burn <= 0:
        default_alive = True
        verdict = "NO BURN — DEFAULT ALIVE"
    elif break_even_month is not None and runway_months is not None and break_even_month <= runway_months:
        default_alive = True
        verdict = "DEFAULT ALIVE"
    else:
        default_alive = False
        verdict = "DEFAULT DEAD"

    # The growth rate at which the verdict would flip, on both runway bases. The
    # pre-tax rate is the one that binds the verdict above; the after-tax rate is
    # stricter, because tax reserves shrink the revenue that reaches the cost line.
    flip_pretax = growth_to_flip(cash, revenue, costs, tax_rate, after_tax=False)
    flip_after_tax = growth_to_flip(cash, revenue, costs, tax_rate, after_tax=True)

    result = {
        "inputs": {
            "cash": cash,
            "revenue": revenue,
            "costs": costs,
            "growth_pct_per_month": growth,
            "tax_rate": tax_rate,
            "months": horizon,
        },
        "net_monthly_burn": round(net_burn, 2),
        "runway_months": None if runway_months is None else round(runway_months, 2),
        "tax_set_aside_monthly": round(reserve, 2),
        "net_monthly_burn_after_tax": round(net_burn_after_tax, 2),
        "runway_months_after_tax": None if runway_after_tax is None else round(runway_after_tax, 2),
        "break_even_month": break_even_month,
        "default_alive": default_alive,
        "verdict": verdict,
        "flip_growth_pct_pretax": None if flip_pretax is None else round(flip_pretax, 1),
        "flip_growth_pct_after_tax": None if flip_after_tax is None else round(flip_after_tax, 1),
    }
    result["verdict_sentence"] = verdict_sentence(result)

    if args.project:
        result["projection"] = project(cash, revenue, costs, growth_factor, tax_rate, horizon)

    return result


def project(cash: float, revenue: float, costs: float, factor: float, tax_rate: float, horizon: int) -> list:
    rows = []
    remaining = cash
    for month in range(1, horizon + 1):
        rev = revenue * (factor ** month)
        burn = costs - rev * (1.0 - tax_rate)
        remaining -= burn
        if remaining < 0:
            remaining = 0.0
        rows.append(
            {
                "month": month,
                "revenue": round(rev, 2),
                "costs": round(costs, 2),
                "cash_remaining": round(remaining, 2),
            }
        )
    return rows


def verdict_sentence(result: dict) -> str:
    i = result["inputs"]
    rev, cost, growth = i["revenue"], i["costs"], i["growth_pct_per_month"]
    runway = result["runway_months"]
    be = result["break_even_month"]

    if result["verdict"].startswith("NO BURN"):
        return (
            f"Revenue of {money(rev)}/mo already covers costs of {money(cost)}/mo, "
            f"so you are default alive — cash only falls if costs rise. "
            f"Keep setting aside about {money(result['tax_set_aside_monthly'])}/mo for tax."
        )

    runway_txt = f"{runway:.1f} months" if runway is not None else "no burn"
    if result["default_alive"]:
        sentence = (
            f"At {money(rev)}/mo growing {growth:g}%/mo, revenue passes "
            f"{money(cost)}/mo costs in month {be} — inside your {runway_txt} of runway. "
            f"Hold the growth rate and you reach break-even before the cash runs out."
        )
        flip = result["flip_growth_pct_pretax"]
        if flip is not None and flip > 0:
            after = result["flip_growth_pct_after_tax"]
            sentence += (
                f" The verdict flips to default dead below {flip:.1f}%/mo growth "
                f"(below {after:.1f}%/mo on an after-tax basis) — that is the line to watch."
            )
        return sentence
    if be is None:
        cause = "revenue is flat or shrinking, so it never reaches costs"
    else:
        cause = f"even at {growth:g}%/mo growth, costs are not reached until month {be} — past your {runway_txt} of runway"
    sentence = (
        f"Costs of {money(cost)}/mo exceed revenue of {money(rev)}/mo and {cause}. "
        f"Cut costs, raise price, or grow revenue now — cash runs out in {runway_txt}."
    )
    flip = result["flip_growth_pct_pretax"]
    if flip is not None:
        after = result["flip_growth_pct_after_tax"]
        sentence += (
            f" Growing about {flip:.1f}%/mo (or {after:.1f}%/mo after tax) or more would "
            f"pull break-even inside the runway and flip you to default alive."
        )
    return sentence


def render(result: dict) -> str:
    i = result["inputs"]
    lines = []
    lines.append(f"Cash on hand:        {money(i['cash'])}")
    lines.append(f"Monthly revenue:     {money(i['revenue'])}")
    lines.append(f"Monthly costs:       {money(i['costs'])}")
    lines.append(f"Net monthly burn:    {money(result['net_monthly_burn'])}")
    lines.append(f"Revenue growth:      {i['growth_pct_per_month']:g}%/mo")
    lines.append("-" * 56)
    lines.append(f"Runway (pre-tax):    {months_str(result['runway_months'])}")
    be = result["break_even_month"]
    be_txt = "already break-even" if be == 0 else ("never at this growth" if be is None else f"month {be}")
    lines.append(f"Break-even:          {be_txt}")
    lines.append(
        f"Tax set-aside:       {money(result['tax_set_aside_monthly'])}/mo "
        f"({i['tax_rate']:.0%} of revenue)"
    )
    lines.append(f"Runway (after tax):  {months_str(result['runway_months_after_tax'])}")
    lines.append(
        f"Flip growth rate:    {growth_pct_str(result['flip_growth_pct_pretax'])}/mo (pre-tax) · "
        f"{growth_pct_str(result['flip_growth_pct_after_tax'])}/mo after tax"
    )
    lines.append("-" * 56)
    lines.append(f"Verdict: {result['verdict']}")
    lines.append(result["verdict_sentence"])

    if "projection" in result:
        lines.append("")
        lines.append("Projection (revenue vs cash, after-tax set-aside):")
        lines.append(f"  {'mo':>3}  {'revenue':>12}  {'cash left':>12}")
        for row in result["projection"]:
            lines.append(
                f"  {row['month']:>3}  {money(row['revenue']):>12}  {money(row['cash_remaining']):>12}"
            )

    lines.append("")
    lines.append("Planning estimate only — not tax, legal, or accounting advice. Confirm")
    lines.append("your set-aside and filings with an accountant.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="runway.py",
        description="Project cash runway, break-even, and the default-alive/default-dead verdict.",
        epilog=(
            "Input schema: --cash, --revenue, --costs and --growth are per-month "
            "figures; --growth is a percent per month and may be 0 or negative "
            "(e.g. --growth -4). Tax set-aside is a planning buffer of "
            "--tax-rate of gross revenue, not a filing. See the module docstring "
            "at the top of this file for the full definitions."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--cash", type=positive, required=True, help="cash currently in the bank")
    parser.add_argument("--revenue", type=positive, required=True, help="current monthly revenue")
    parser.add_argument("--costs", type=positive, required=True, help="monthly costs / burn (all-in)")
    parser.add_argument(
        "--growth",
        type=float,
        required=True,
        help="monthly revenue growth, percent (may be 0 or negative, e.g. -4)",
    )
    parser.add_argument(
        "--tax-rate",
        type=float,
        default=DEFAULT_TAX_RATE,
        help="fraction of revenue to set aside for tax",
    )
    parser.add_argument(
        "--months",
        type=positive_int,
        default=DEFAULT_MONTHS,
        help="projection horizon in months",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")
    parser.add_argument("--project", action="store_true", help="include a month-by-month projection table")

    args = parser.parse_args(argv)

    # Validate ranges argparse can't express with a single type.
    if args.growth <= -100:
        parser.error(
            f"--growth {args.growth:g} is invalid: a rate of -100%/mo or lower "
            "makes revenue zero or negative. Use a value greater than -100."
        )
    if not 0.0 <= args.tax_rate < 1.0:
        parser.error(f"--tax-rate {args.tax_rate:g} is invalid: expected a fraction in [0, 1).")

    result = compute(args)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
