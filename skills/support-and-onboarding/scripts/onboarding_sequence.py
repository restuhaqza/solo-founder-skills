#!/usr/bin/env python3
"""Generate a dated onboarding-to-aha email sequence scaffold as Markdown.

Given a product name and the single activation event that proves a user reached
value, this emits one block per day of the sequence. Each block has a subject
line, the ONE action it drives (toward the activation event), a short body
skeleton with placeholders, and a goal line. It is a scaffold to copy and edit,
not finished copy — the founder writes the voice.

Usage:
    python3 onboarding_sequence.py --product "Acme Reports" \
        --activation-event "first report shared with a client"
    python3 onboarding_sequence.py --product "Acme" \
        --activation-event "first report shared" --days "0,1,3,7,14,30"
    python3 onboarding_sequence.py --product "Acme" \
        --activation-event "first report shared" --tone "warm and plain"
    python3 onboarding_sequence.py --product "Acme" \
        --activation-event "first report shared" --json
    python3 onboarding_sequence.py --help

Arguments:
    --product           required; the product name the emails speak for
    --activation-event  required; the one countable action that = value reached
    --days              comma-separated relative days, ascending
                        (default "0,1,3,7,30")
    --tone              optional descriptor of the voice to keep consistent
                        (default "warm, concise, plain-spoken")
    --json              emit a structured JSON object instead of Markdown

The day list is assigned slot archetypes in order: the first day is the
welcome, the second drives the single activation action, the third spotlights
the feature that makes it click, the fourth checks in, the fifth marks a
milestone, and any further days become generic nudges. With the default days
this lines up with the familiar Day 0/1/3/7/30 shape.

Placeholders to replace: [USER_NAME], [PRODUCT], [ACTIVATION_EVENT], [LOGIN_LINK].
Output goes to stdout; diagnostics go to stderr. Exit 0 on success, 2 on a
usage or input error.
"""

from __future__ import annotations

import argparse
import json
import sys

DEFAULT_DAYS = "0,1,3,7,30"
DEFAULT_TONE = "warm, concise, plain-spoken"

# Slot archetypes, assigned to the days in order. Each is a callable that takes
# the product, activation event, and day and returns the block fields. Keeping
# them ordered lets a custom --days list stay useful instead of erroring.
SLOT_ORDER = [
    "welcome",
    "first-action",
    "feature-spotlight",
    "check-in",
    "milestone",
    "nudge",
]


def die(message: str) -> None:
    """Print an error to stderr and exit with the input-error code."""
    sys.stderr.write(f"Error: {message}\n")
    raise SystemExit(2)


def parse_days(raw: str) -> list[int]:
    """Parse and validate a comma-separated list of relative day numbers."""
    days: list[int] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            day = int(token)
        except ValueError:
            die(
                f"--days token '{token}' is not an integer. "
                "Expected comma-separated days like '0,1,3,7,30'."
            )
        if day < 0:
            die(f"--days token '{day}' is negative; days must be 0 or greater.")
        days.append(day)
    if not days:
        die("--days must contain at least one day, e.g. '0,1,3,7,30'.")
    return days


def slot_for(index: int) -> str:
    """Map a position in the sequence to a slot archetype (clamped)."""
    if index < len(SLOT_ORDER):
        return SLOT_ORDER[index]
    return SLOT_ORDER[-1]


def build_block(slot: str, day: int, product: str, activation: str) -> dict:
    """Return the subject/action/goal/body for one sequence block."""
    if slot == "welcome":
        return {
            "day": day,
            "slot": "welcome",
            "label": "Welcome & first step",
            "subject": f"Welcome to [PRODUCT] — here is your first step",
            "action": "Sign in and take the smallest first step toward "
            f"[ACTIVATION_EVENT].",
            "goal": "Turn the signup into an active first session, so the next "
            "email has something real to build on.",
            "body": (
                "Hi [USER_NAME],\n\n"
                "Thanks for signing up to [PRODUCT]. The fastest way to see why "
                "it matters is to try the first step now while it is fresh:\n\n"
                "  -> [LOGIN_LINK]\n\n"
                "It takes about two minutes. If you hit anything confusing, "
                "just reply to this email — it comes straight to me.\n\n"
                "— [FOUNDER_NAME]"
            ),
        }
    if slot == "first-action":
        return {
            "day": day,
            "slot": "first-action",
            "label": "The one action that reaches the aha",
            "subject": "The one thing to do in [PRODUCT] today",
            "action": f"Complete [ACTIVATION_EVENT] — this single action is the aha.",
            "goal": "Drive the exact activation event, not a tour. One action, one link.",
            "body": (
                "Hi [USER_NAME],\n\n"
                "If you only do one thing in [PRODUCT] this week, make it this: "
                "get to [ACTIVATION_EVENT].\n\n"
                "  -> [LOGIN_LINK]\n\n"
                "That is the moment the product starts paying you back. "
                "Everything else can wait.\n\n"
                "Stuck on a step? Reply and tell me where — I read every reply.\n\n"
                "— [FOUNDER_NAME]"
            ),
        }
    if slot == "feature-spotlight":
        return {
            "day": day,
            "slot": "feature-spotlight",
            "label": "The feature that makes it click",
            "subject": "A shortcut most people miss in [PRODUCT]",
            "action": "Use the one feature that retained users adopt first, in the "
            "context of the action they already took.",
            "goal": "Deepen the habit formed by the activation action so the value "
            "compounds.",
            "body": (
                "Hi [USER_NAME],\n\n"
                "Now that you have started with [PRODUCT], here is the feature "
                "that people who stick around use first: [KEY_FEATURE].\n\n"
                "It saves you [CONCRETE_OUTCOME]. Try it on the work you already "
                "started:\n\n"
                "  -> [LOGIN_LINK]\n\n"
                "— [FOUNDER_NAME]"
            ),
        }
    if slot == "check-in":
        return {
            "day": day,
            "slot": "check-in",
            "label": "Check-in",
            "subject": "Did [PRODUCT] actually help?",
            "action": "Reply with how it is going (this is the check-in, not a "
            "call to a new feature).",
            "goal": "Surface blocking confusion early and collect the best "
            "qualitative signal you will get.",
            "body": (
                "Hi [USER_NAME],\n\n"
                "Quick check-in: have you had a chance to reach "
                "[ACTIVATION_EVENT] in [PRODUCT]?\n\n"
                "If yes — I would love to hear what it helped with. "
                "If no — what is getting in the way? A one-line reply is plenty, "
                "and it shapes what we build next.\n\n"
                "— [FOUNDER_NAME]"
            ),
        }
    if slot == "milestone":
        return {
            "day": day,
            "slot": "milestone",
            "label": "Milestone & next step",
            "subject": "You are [MILESTONE] in — here is what is next",
            "action": "Take the next natural step beyond activation (a second "
            "workflow, or a plan that fits the usage).",
            "goal": "Convert early value into a durable habit and the natural next "
            "commitment.",
            "body": (
                "Hi [USER_NAME],\n\n"
                "You have reached [MILESTONE] with [PRODUCT] — nice. The next "
                "natural step is [NEXT_STEP], which is where teams like yours "
                "usually go deeper.\n\n"
                "  -> [LOGIN_LINK]\n\n"
                "Any questions, reply anytime.\n\n"
                "— [FOUNDER_NAME]"
            ),
        }
    # Generic nudge for any extra days beyond the five archetypes.
    return {
        "day": day,
        "slot": "nudge",
        "label": "Still here to help",
        "subject": "Still getting value from [PRODUCT]?",
        "action": f"Return and complete [ACTIVATION_EVENT] if it is still open.",
        "goal": "Re-surface the sequence for anyone who has not yet activated.",
        "body": (
            "Hi [USER_NAME],\n\n"
            "Checking back in on [PRODUCT]. If you have not reached "
            "[ACTIVATION_EVENT] yet, it is still the best two minutes you can "
            "spend here:\n\n"
            "  -> [LOGIN_LINK]\n\n"
            "Tell me what is blocking you and I will help.\n\n"
            "— [FOUNDER_NAME]"
        ),
    }


def build_sequence(days: list[int], product: str, activation: str) -> list[dict]:
    """Build every block in the sequence, in day order."""
    sequence = []
    for index, day in enumerate(days):
        sequence.append(build_block(slot_for(index), day, product, activation))
    return sequence


def render(result: dict) -> str:
    """Render the sequence as copy-paste-ready Markdown."""
    lines = []
    lines.append(f"# Onboarding-to-aha sequence — {result['product']}")
    lines.append(
        f"_Activation event: {result['activation_event']} · Tone: {result['tone']}_"
    )
    lines.append("")
    lines.append(
        "Every step below drives ONE action toward the activation event. "
        "Replace the bracketed placeholders, keep one call to action per email, "
        "and suppress anyone who activates early."
    )
    lines.append("")
    lines.append(f"Sequence days: {', '.join(str(d) for d in result['days'])}")
    lines.append("")

    for block in result["sequence"]:
        lines.append(f"## Day {block['day']} — {block['label']}")
        lines.append(f"- **Subject:** {block['subject']}")
        lines.append(f"- **The one action:** {block['action']}")
        lines.append(f"- **Goal:** {block['goal']}")
        lines.append("- **Body skeleton:**")
        lines.append("")
        for body_line in block["body"].split("\n"):
            lines.append(f"  {body_line}" if body_line else "")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(
        "Reminder: this is a scaffold. The founder writes the final voice, and "
        "no email sends itself — approve the copy first."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a dated onboarding-to-aha email sequence scaffold "
            "(Day 0/1/3/7/30 by default) as Markdown."
        ),
        epilog="See the docstring at the top of this file for the placeholders used.",
    )
    parser.add_argument("--product", required=True, help="product name the emails speak for")
    parser.add_argument(
        "--activation-event",
        required=True,
        help="the one countable action that proves a user reached value",
    )
    parser.add_argument(
        "--days",
        default=DEFAULT_DAYS,
        help=f"comma-separated relative days (default \"{DEFAULT_DAYS}\")",
    )
    parser.add_argument(
        "--tone",
        default=DEFAULT_TONE,
        help=f"voice to keep consistent (default \"{DEFAULT_TONE}\")",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a structured JSON object instead of Markdown",
    )
    args = parser.parse_args(argv)

    days = parse_days(args.days)
    sequence = build_sequence(days, args.product, args.activation_event)

    result = {
        "product": args.product,
        "activation_event": args.activation_event,
        "tone": args.tone,
        "days": days,
        "sequence": sequence,
    }

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
