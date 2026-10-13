#!/usr/bin/env python3
"""Compute dilution, price per share, and a before/after cap table for a raise.

Takes the three numbers a founder negotiates first — pre-money valuation, the
amount raised, and (optionally) the option-pool target — and returns the
post-money valuation, what the new investor owns, what existing holders give up,
the price per share, the shares issued, and a small cap table. It can also model
the standard *option-pool shuffle* and a *second round* ("cascade") to show the
cumulative founder ownership after both rounds.

Usage:
    python3 raise_math.py --pre-money 8000000 --raise 2000000
    python3 raise_math.py --pre-money 8000000 --raise 2000000 --option-pool 10
    python3 raise_math.py --pre-money 8000000 --raise 2000000 --option-pool 10 \\
        --cascade 20000000 5000000
    python3 raise_math.py --pre-money 8000000 --raise 2000000 --json
    python3 raise_math.py --help

The math
--------
Post-money valuation:
    post_money = pre_money + raise
A priced round is just arithmetic on these two numbers.

Ownership (no option pool):
    investor_pct   = raise / post_money
    founder_pct    = pre_money / post_money        (= 1 - investor_pct)
    price_per_share = pre_money / existing_shares
    shares_issued  = raise / price_per_share

Option-pool shuffle (the "created pre-money" convention):
    An option-pool target is normally quoted as a percentage of the *post-money*
    company, and it is created *before* the round, so it dilutes existing holders
    but not the new investor. If pool_pct is the target:
        founder_pct = 1 - investor_pct - pool_pct
        total_shares = existing_shares / founder_pct
        pool_shares  = pool_pct * total_shares
        price_per_share = pre_money / (existing_shares + pool_shares)
    The pool comes out of the founders' side, which is why the limit to watch is
    founder_pct > 0. This is the common US convention; your term sheet may say
    something else, so confirm which side the pool dilutes.

Cascade (a second round):
    A second priced round sets a new pre-money on the fully-diluted cap table
    left by the first round. Existing holders (founder, old pool, round-1
    investor) are diluted by pre2 / post2:
        founder_pct_after = founder_pct_after_round1 * (pre2 / post2)
    The script reports cumulative founder ownership after both rounds. It models
    the second round without a new pool top-up; add one if your term sheet does.

Exit codes: 0 = ran successfully, 2 = usage/input error.

Planning estimate only — not investment, legal, or tax advice. Term-sheet terms,
SAFE/note mechanics, and tax are for your lawyer and accountant.
"""

from __future__ import annotations

import argparse
import json
import sys

# Default shares outstanding for an illustrative cap table. Any number works
# because a priced round only cares about the *ratio* of ownership; this is just
# a round figure that keeps the per-share numbers legible. Override with
# --existing-shares.
DEFAULT_EXISTING_SHARES = 10_000_000


def positive(value: str) -> float:
    """argparse type: a number > 0, else a usage error."""
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a number, got '{value}'")
    if number <= 0:
        raise argparse.ArgumentTypeError(f"expected a number > 0, got '{value}'")
    return number


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a whole number, got '{value}'")
    if number <= 0:
        raise argparse.ArgumentTypeError(f"expected a whole number > 0, got '{value}'")
    return number


def money(amount: float) -> str:
    return f"${amount:,.0f}"


def pct(fraction: float) -> str:
    return f"{fraction * 100:.2f}%"


def shares(n: float) -> str:
    return f"{n:,.0f}"


def price(value: float) -> str:
    """Format a per-share price, trimming trailing zeros (0.800000 -> $0.8)."""
    text = f"{value:,.6f}".rstrip("0").rstrip(".")
    return f"${text}"


def compute(args: argparse.Namespace) -> dict:
    pre = args.pre_money
    raised = args.raise_amount
    existing = args.existing_shares
    post = pre + raised

    investor_pct = raised / post
    pool_pct = (args.option_pool / 100.0) if args.option_pool is not None else 0.0

    # Guard rail: existing holders can give away at most all of their stake.
    if investor_pct + pool_pct >= 1.0:
        raise ValueError(
            f"raise of {money(raised)} at {money(pre)} pre-money ({pct(investor_pct)} to the "
            f"new investor) plus a {pct(pool_pct)} option pool leaves nothing for existing "
            "holders. Lower the pool, lower the raise, or raise the pre-money."
        )

    if pool_pct > 0:
        # Pool created pre-money: solve for the shares that make the pool exactly
        # pool_pct of the post-money company.
        founder_pct = 1.0 - investor_pct - pool_pct
        total_shares = existing / founder_pct
        pool_shares = pool_pct * total_shares
        price_per_share = pre / (existing + pool_shares)
        shares_issued = raised / price_per_share
    else:
        founder_pct = pre / post
        price_per_share = pre / existing
        shares_issued = raised / price_per_share
        pool_shares = 0.0
        total_shares = existing + shares_issued

    existing_dilution_pct = 1.0 - founder_pct

    cap_table_after = [
        {"holder": "Founder / existing", "shares": existing, "pct": founder_pct},
    ]
    if pool_pct > 0:
        cap_table_after.append(
            {"holder": "Option pool", "shares": pool_shares, "pct": pool_pct}
        )
    cap_table_after.append(
        {"holder": "New investor", "shares": shares_issued, "pct": investor_pct}
    )

    result = {
        "inputs": {
            "pre_money": pre,
            "raise": raised,
            "option_pool_pct_of_post": pool_pct,
            "existing_shares": existing,
        },
        "post_money": round(post, 2),
        "new_investor_pct": round(investor_pct, 6),
        "founder_pct": round(founder_pct, 6),
        "existing_dilution_pct": round(existing_dilution_pct, 6),
        "price_per_share": round(price_per_share, 6),
        "shares_issued": round(shares_issued, 2),
        "total_shares_after": round(total_shares, 2),
        "cap_table_before": [
            {"holder": "Founder / existing", "shares": existing, "pct": 1.0},
        ],
        "cap_table_after": cap_table_after,
    }

    if args.cascade is not None:
        result["cascade"] = compute_cascade(
            next_pre=args.cascade[0],
            next_raise=args.cascade[1],
            founder_pct=founder_pct,
            pool_pct=pool_pct,
            investor_pct=investor_pct,
            total_shares_after=total_shares,
        )

    return result


def compute_cascade(
    next_pre: float,
    next_raise: float,
    founder_pct: float,
    pool_pct: float,
    investor_pct: float,
    total_shares_after: float,
) -> dict:
    """Model a second priced round on top of the first round's cap table."""
    post2 = next_pre + next_raise
    inv2_pct = next_raise / post2
    factor = next_pre / post2  # dilution applied to everyone from round 1

    founder2 = founder_pct * factor
    pool2 = pool_pct * factor
    inv1_2 = investor_pct * factor

    # Round-2 price is set on the round-1 fully-diluted share count.
    price2 = next_pre / total_shares_after
    shares2 = next_raise / price2

    return {
        "next_pre_money": next_pre,
        "next_raise": next_raise,
        "next_post_money": round(post2, 2),
        "round2_investor_pct": round(inv2_pct, 6),
        "round2_price_per_share": round(price2, 6),
        "round2_shares_issued": round(shares2, 2),
        "founder_pct_after": round(founder2, 6),
        "pool_pct_after": round(pool2, 6),
        "round1_investor_pct_after": round(inv1_2, 6),
        "total_founder_dilution_pct": round(1.0 - founder2, 6),
    }


def render(result: dict) -> str:
    i = result["inputs"]
    lines = []
    lines.append("Raise summary")
    lines.append("=" * 56)
    lines.append(f"Pre-money valuation:  {money(i['pre_money'])}")
    lines.append(f"Amount raised:        {money(i['raise'])}")
    lines.append(f"Post-money valuation: {money(result['post_money'])}")
    lines.append("")
    lines.append(f"New investor owns:    {pct(result['new_investor_pct'])}")
    lines.append(f"Founder owns:         {pct(result['founder_pct'])}")
    lines.append(f"Existing dilution:    {pct(result['existing_dilution_pct'])}"
                 + ("  (includes the option pool)" if i["option_pool_pct_of_post"] > 0 else ""))
    lines.append(f"Price per share:      {price(result['price_per_share'])}")
    lines.append(f"Shares issued:        {shares(result['shares_issued'])}")
    lines.append("")
    lines.append("Cap table (before -> after)")
    lines.append(f"  {'holder':<18}{'before shares':>16}{'before %':>10}"
                 f"{'after shares':>16}{'after %':>10}")
    before = {row["holder"]: row for row in result["cap_table_before"]}
    after = {row["holder"]: row for row in result["cap_table_after"]}
    order = ["Founder / existing", "Option pool", "New investor"]
    for holder in order:
        b = before.get(holder, {"shares": 0.0, "pct": 0.0})
        a = after.get(holder)
        if holder == "Option pool" and a is None:
            continue
        lines.append(
            f"  {holder:<18}{shares(b['shares']):>16}{pct(b['pct']):>10}"
            f"{shares(a['shares']):>16}{pct(a['pct']):>10}"
        )

    if "cascade" in result:
        c = result["cascade"]
        lines.append("")
        lines.append("Cascade: a second round on top of this one")
        lines.append("-" * 56)
        lines.append(f"Round 2 pre-money:    {money(c['next_pre_money'])}")
        lines.append(f"Round 2 raise:        {money(c['next_raise'])}")
        lines.append(f"Round 2 post-money:   {money(c['next_post_money'])}")
        lines.append(f"Round 2 investor owns:{pct(c['round2_investor_pct']):>8}")
        lines.append(f"Founder after round2: {pct(c['founder_pct_after'])}")
        lines.append(f"Total founder dilution: {pct(c['total_founder_dilution_pct'])}")

    lines.append("")
    lines.append("Planning estimate only — not investment, legal, or tax advice. Confirm")
    lines.append("terms, instruments, and tax with your lawyer and accountant before quoting")
    lines.append("anything to an investor.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="raise_math.py",
        description="Compute dilution, price per share, and a before/after cap table for a raise.",
        epilog=(
            "Input schema: --pre-money and --raise are amounts (any currency); "
            "--option-pool is a percent of the post-money company (e.g. 10 = 10%) "
            "created pre-money; --existing-shares is the pre-round share count "
            "(default 10000000, only the ownership ratio matters); --cascade takes "
            "TWO numbers, the next round's pre-money and raise. See the module "
            "docstring at the top of this file for the full math."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--pre-money", type=positive, required=True, help="pre-money valuation")
    parser.add_argument(
        "--raise",
        dest="raise_amount",
        type=positive,
        required=True,
        help="amount being raised in this round",
    )
    parser.add_argument(
        "--option-pool",
        type=float,
        default=None,
        help="option-pool target as a percent of post-money (e.g. 10), created pre-money",
    )
    parser.add_argument(
        "--existing-shares",
        type=positive_int,
        default=DEFAULT_EXISTING_SHARES,
        help="shares outstanding before the round",
    )
    parser.add_argument(
        "--cascade",
        type=float,
        nargs=2,
        metavar=("NEXT_PRE", "NEXT_RAISE"),
        default=None,
        help="model a second round: its pre-money and its raise",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of text")

    args = parser.parse_args(argv)

    # argparse can't bound a single value with two types, so check the pool range.
    if args.option_pool is not None and not 0.0 <= args.option_pool < 100.0:
        parser.error(
            f"--option-pool {args.option_pool:g} is invalid: expected a percent in [0, 100)."
        )
    if args.cascade is not None and (args.cascade[0] <= 0 or args.cascade[1] <= 0):
        parser.error(
            f"--cascade {args.cascade[0]:g} {args.cascade[1]:g} is invalid: both the "
            "next pre-money and the next raise must be greater than 0."
        )

    try:
        result = compute(args)
    except ValueError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 2

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
