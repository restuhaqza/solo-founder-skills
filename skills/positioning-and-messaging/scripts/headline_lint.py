#!/usr/bin/env python3
"""Lint candidate headlines for deterministic weaknesses, with a score out of 100.

A fast, opinionated coach for landing-page heroes, one-line positioning
statements, and value-proposition copy. It hunts for the predictable ways a
headline goes wrong — hype words, company-first openings, feature-first
phrasing, no audience cue, no verb, shouting, clichés, and plain length — and
prints each with a short suggestion plus a single score.

This is a heuristic, not a verdict. A 100/100 headline can still be wrong for
your market, and a flagged word can be exactly right in the right context.
Use the score to compare candidates, not to certify one.

Usage:
    python3 headline_lint.py "Cut invoice chasing from hours to minutes"
    python3 headline_lint.py "We're building the future of work" "A CRM for photographers"
    python3 headline_lint.py --file candidates.txt
    cat candidates.txt | python3 headline_lint.py
    python3 headline_lint.py "..." --json
    python3 headline_lint.py --help

Input
    Provide headlines three ways (they compose): as positional arguments, via
    --file (one headline per line; blank lines and lines starting with '#' are
    skipped; '-' means stdin), or on stdin when no other input is given.
    Quote each headline so the shell passes it as one argument.

Output
    Human-readable text by default; machine-readable JSON with --json. Data
    goes to stdout, diagnostics to stderr. Exit codes: 0 = ran successfully
    (even if every candidate scored badly — that is the point), 2 = usage or
    input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

# A headline longer than this is hard for a stranger to repeat after one read.
MAX_WORDS_DEFAULT = 12

# Hype words that mean nothing to a buyer and signal generic copy. Matched on
# word boundaries, case-insensitively, so "Seamless" and "seamless" both hit.
BUZZWORDS = [
    "revolutionary",
    "seamless",
    "seamlessly",
    "next-generation",
    "next generation",
    "cutting-edge",
    "cutting edge",
    "game-changing",
    "game changing",
    "game-changer",
    "leverage",
    "synergy",
    "synergies",
    "world-class",
    "world class",
    "best-in-class",
    "best in class",
    "state-of-the-art",
    "state of the art",
    "disruptive",
    "innovative",
    "robust",
    "frictionless",
    "effortless",
    "unparalleled",
    "unmatched",
    "industry-leading",
    "leading-edge",
    "turnkey",
    "bleeding-edge",
    "paradigm",
    "empower",
    "supercharge",
    "revolutionize",
    "transformative",
    "groundbreaking",
    "future-proof",
    "future proof",
    "mission-critical",
    "holistic",
    # "AI" as a filler prefix: only a weakness when it substitutes for a value.
    "ai-powered",
    "ai powered",
    "ai-driven",
    "ai driven",
]

# Phrases so overused they read as filler. The buyer's eye skips them.
CLICHES = [
    "one-stop shop",
    "one stop shop",
    "take it to the next level",
    "think outside the box",
    "best-kept secret",
    "best kept secret",
    "all-in-one solution",
    "all in one solution",
    "end-to-end solution",
    "end to end solution",
    "one size fits all",
    "move the needle",
    "low-hanging fruit",
    "at your fingertips",
    "like never before",
    "reinvent the wheel",
    "say goodbye to",
    "everything you need to",
    "the only tool you'll ever need",
    "the only platform you'll ever need",
    "in today's fast-paced",
    "unlock your potential",
    "the future of work",
    "not just another",
]

# Feature nouns. A headline that OPENS with one of these usually names the
# product instead of the change it creates ("The CRM for...", "A dashboard...").
FEATURE_NOUNS = {
    "dashboard",
    "platform",
    "app",
    "application",
    "tool",
    "software",
    "saas",
    "api",
    "integration",
    "crm",
    "analytics",
    "tracker",
    "extension",
    "plugin",
    "widget",
    "template",
    "framework",
    "system",
    "engine",
    "suite",
    "workspace",
    "spreadsheet",
    "chatbot",
    "automation",
    "pipeline",
    "database",
    "portal",
    "editor",
    "generator",
    "builder",
    "solution",
    "service",
}

# A rough audience lexicon. Presence of any of these, or the word "for", counts
# as an audience cue. A headline with none of them is probably talking to no one.
AUDIENCE_WORDS = {
    "founders",
    "founder",
    "indie",
    "builders",
    "developers",
    "devs",
    "engineers",
    "designers",
    "marketers",
    "managers",
    "teams",
    "team",
    "agencies",
    "agency",
    "freelancers",
    "freelancer",
    "consultants",
    "creators",
    "writers",
    "analysts",
    "operators",
    "owners",
    "retailers",
    "solopreneurs",
    "recruiters",
    "salespeople",
    "teachers",
    "students",
    "doctors",
    "lawyers",
    "accountants",
    "realtors",
    "photographers",
    "coaches",
    "trainers",
    "shops",
    "startups",
    "enterprises",
    "customers",
    "parents",
    "runners",
    "readers",
}

# Action verbs that signal a change or an outcome. Not exhaustive — the lint
# suggestion tells the founder to ignore a false "missing verb" if theirs is
# simply absent from this list.
VERB_HINTS = {
    "cut",
    "cuts",
    "turn",
    "turns",
    "save",
    "saves",
    "ship",
    "ships",
    "run",
    "runs",
    "build",
    "builds",
    "track",
    "tracks",
    "find",
    "finds",
    "fixed",
    "fixes",
    "send",
    "sends",
    "write",
    "writes",
    "grow",
    "grows",
    "launch",
    "launches",
    "automate",
    "automates",
    "replace",
    "replaces",
    "eliminate",
    "eliminates",
    "reduce",
    "reduces",
    "increase",
    "increases",
    "boost",
    "boosts",
    "double",
    "doubles",
    "halve",
    "halves",
    "stop",
    "stops",
    "start",
    "starts",
    "keep",
    "keeps",
    "make",
    "makes",
    "know",
    "knows",
    "see",
    "sees",
    "spend",
    "spends",
    "win",
    "wins",
    "close",
    "closes",
    "convert",
    "converts",
    "publish",
    "publishes",
    "schedule",
    "schedules",
    "manage",
    "manages",
    "organize",
    "organise",
    "organizes",
    "organises",
    "organised",
    "organized",
    "centralize",
    "centralise",
    "monitor",
    "monitors",
    "catch",
    "catches",
    "chase",
    "chases",
    "avoid",
    "avoids",
    "discover",
    "discovers",
    "learn",
    "learns",
    "get",
    "gets",
    "help",
    "helps",
    "answer",
    "answers",
    "collect",
    "collects",
    "invoice",
    "invoices",
    "onboard",
    "onboards",
    "renew",
    "renews",
}

# Well-understood acronyms that are not "shouting".
ACRONYM_ALLOWLIST = {
    "SEO",
    "API",
    "CRM",
    "CMS",
    "AI",
    "SaaS",
    "B2B",
    "B2C",
    "PDF",
    "CSV",
    "SQL",
    "URL",
    "iOS",
    "UI",
    "UX",
    "KPI",
    "MRR",
    "ARR",
    "LTV",
    "ROI",
    "CLI",
    "SDK",
    "JSON",
    "HTML",
    "CSS",
    "QA",
}

# Deductions per issue code. Flat by design: the goal is to rank candidates and
# nudge the obvious fixes, not to model a buyer's attention with false precision.
DEDUCTIONS = {
    "too_long": 20,
    "buzzword": 12,
    "cliche": 10,
    "open_first_person": 15,
    "no_audience": 15,
    "feature_first": 15,
    "missing_verb": 15,
    "all_caps": 6,
}
# Caps on issues that can repeat, so a single headline cannot be buried by one
# category (e.g. five buzzwords).
CAPPED_TOTALS = {
    "buzzword": 36,
    "cliche": 20,
    "all_caps": 12,
}

FIRST_PERSON_OPENERS = {"we", "we're", "we’re", "our", "us", "i", "i'm", "i’m", "my"}
LIST_ARTICLES = {"the", "a", "an"}

WORD_RE = re.compile(r"[A-Za-z0-9'’\-]+")


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def find_phrase(text: str, phrase: str) -> bool:
    return re.search(r"\b" + re.escape(phrase) + r"\b", text, re.IGNORECASE) is not None


def lint_headline(headline: str, max_words: int = MAX_WORDS_DEFAULT) -> dict:
    """Return a dict describing every deterministic issue found in one headline."""
    text = headline.strip()
    tokens = WORD_RE.findall(text)
    lowered = [t.lower() for t in tokens]
    issues: list[dict] = []

    def add(code: str, message: str, suggestion: str) -> None:
        issues.append(
            {"code": code, "message": message, "suggestion": suggestion}
        )

    # 1. Length: a stranger cannot repeat a mouthful of a headline.
    count = len(tokens)
    if count > max_words:
        add(
            "too_long",
            f"{count} words — over the {max_words}-word limit",
            f"cut to {max_words} words or fewer; one idea per headline",
        )

    # 2. Buzzwords: hype that hides what actually changes.
    hits = [w for w in BUZZWORDS if find_phrase(text, w)]
    for w in hits:
        add(
            "buzzword",
            f'buzzword "{w}"',
            "replace the hype with the concrete change the buyer feels",
        )

    # 3. Clichés: phrases the buyer's eye skips.
    for c in CLICHES:
        if find_phrase(text, c):
            add(
                "cliche",
                f'cliché "{c}"',
                "say the specific thing this does, in plain words",
            )

    # 4. Company-first opening: lead with the customer, not yourself.
    if lowered and lowered[0] in FIRST_PERSON_OPENERS:
        add(
            "open_first_person",
            f'opens with "{tokens[0]}"',
            'lead with the customer or the outcome, not "we/our"',
        )

    # 5. Audience cue: does the headline name who it is for?
    has_audience = find_phrase(text, "for") or any(t in AUDIENCE_WORDS for t in lowered)
    if not has_audience:
        add(
            "no_audience",
            "no audience cue",
            'name who it is for — the "for Y" slot of "X for Y who need Z"',
        )

    # 6. Feature-first: opening with a product noun instead of an outcome.
    first = lowered[0] if lowered else ""
    second = lowered[1] if len(lowered) > 1 else ""
    feature_first = first in FEATURE_NOUNS or (
        first in LIST_ARTICLES and second in FEATURE_NOUNS
    )
    if feature_first:
        add(
            "feature_first",
            f'starts by naming a product ("{tokens[0]}"'
            + (f' "{tokens[1]}"' if first in LIST_ARTICLES and len(tokens) > 1 else "")
            + ")",
            "lead with the outcome, not the object; the category can come later",
        )

    # 7. Missing verb: no action means no promise of change.
    has_verb = any(t in VERB_HINTS for t in lowered)
    if not has_verb:
        add(
            "missing_verb",
            "no action verb",
            "add a verb that states what changes (cut, turns, ships, tracks…)",
        )

    # 8. ALL-CAPS words read as shouting (SEO, API and friends are allowed).
    shouts = [
        t
        for t in tokens
        if t.isupper() and len(t) >= 2 and t not in ACRONYM_ALLOWLIST
    ]
    for t in shouts:
        add(
            "all_caps",
            f'ALL-CAPS word "{t}"',
            "use sentence case; reserve caps for established acronyms",
        )

    # Score: start at 100, subtract per-issue deductions, capped per category.
    per_category: dict[str, int] = {}
    for issue in issues:
        per_category[issue["code"]] = per_category.get(issue["code"], 0) + 1
    deduction = 0
    for code, count_in_cat in per_category.items():
        raw = DEDUCTIONS.get(code, 0) * count_in_cat
        cap = CAPPED_TOTALS.get(code)
        deduction += min(raw, cap) if cap is not None else raw
    score = max(0, 100 - deduction)

    if score >= 85:
        band = "strong"
    elif score >= 70:
        band = "solid"
    elif score >= 50:
        band = "shaky"
    else:
        band = "rewrite"

    return {
        "headline": text,
        "word_count": count,
        "score": score,
        "band": band,
        "issues": issues,
    }


def render(results: list[dict], max_words: int) -> str:
    lines = []
    lines.append("Headline lint — heuristic coach, not a verdict")
    lines.append(f"candidates: {len(results)}   length limit: {max_words} words")
    lines.append("score bands: 85+ strong | 70-84 solid | 50-69 shaky | <50 rewrite")
    lines.append("=" * 72)
    for i, r in enumerate(results, start=1):
        lines.append("")
        lines.append(f'[{i}] "{r["headline"]}"')
        lines.append(
            f'    score {r["score"]}/100  ({r["band"]})  ·  {r["word_count"]} words'
        )
        if not r["issues"]:
            lines.append("    no deterministic weaknesses found.")
            continue
        for issue in r["issues"]:
            lines.append(f'    - [{issue["code"]}] {issue["message"]}')
            lines.append(f'      → {issue["suggestion"]}')
    lines.append("")
    lines.append(
        "Read the score as a ranking between candidates, not a pass/fail. "
        "Rewrite the top issues, then re-run."
    )
    return "\n".join(lines)


def collect_headlines(args: argparse.Namespace) -> list[str]:
    headlines = list(args.headlines)
    stdin_used = False

    def read_lines(label: str) -> list[str]:
        stream = sys.stdin if label == "-" else None
        if stream is not None:
            raw = stream.read()
        else:
            try:
                with open(label, "r", encoding="utf-8-sig") as fh:
                    raw = fh.read()
            except FileNotFoundError:
                fail(f"file not found: {label}")
            except UnicodeDecodeError:
                fail(f"{label} is not readable as UTF-8 text.")
        out = []
        for line in raw.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.append(s)
        return out

    for path in args.file:
        if path == "-":
            stdin_used = True
        headlines.extend(read_lines(path))

    # Fall back to stdin only when nothing else was provided and stdin is piped.
    if not headlines and not stdin_used:
        if sys.stdin.isatty():
            fail(
                "no headlines given. Pass one or more quoted headlines, use "
                "--file PATH, or pipe them on stdin (one per line)."
            )
        headlines.extend(read_lines("-"))

    cleaned = [h.strip() for h in headlines if h.strip()]
    if not cleaned:
        fail("no usable headlines found after reading the input.")
    return cleaned


def fail(message: str) -> "None":
    sys.stderr.write(f"Error: {message}\n")
    raise SystemExit(2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Lint candidate headlines for deterministic weaknesses and give each "
            "a score out of 100. A heuristic coach, not a verdict."
        ),
        epilog=(
            "Checks: length (> --max-words), buzzwords, clichés, company-first "
            "openings, missing audience cue, feature-first phrasing, missing verb, "
            "and ALL-CAPS words. Provide headlines as positional args, with "
            "--file (one per line; '-' = stdin), or on stdin. Exit 2 on usage or "
            "input error."
        ),
    )
    parser.add_argument(
        "headlines",
        nargs="*",
        help="one or more candidate headlines (quote each one)",
    )
    parser.add_argument(
        "--file",
        "-f",
        action="append",
        default=[],
        metavar="PATH",
        help="read headlines from a file, one per line; '-' reads stdin (repeatable)",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=MAX_WORDS_DEFAULT,
        help=f"word limit before the too-long flag (default {MAX_WORDS_DEFAULT})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of text",
    )
    args = parser.parse_args(argv)

    if args.max_words < 1:
        fail(f"--max-words must be at least 1, got {args.max_words}.")

    headlines = collect_headlines(args)
    results = [lint_headline(h, args.max_words) for h in headlines]

    if args.json:
        json.dump({"candidates": results}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render(results, args.max_words))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
