#!/usr/bin/env python3
"""Build consistently named UTM-tagged URLs for launch and distribution channels.

Given a base URL, a campaign name, and a list of channels, this emits one tagged
URL per channel plus warnings about duplicate or inconsistent source/medium
pairs — the kind of naming drift that quietly fragments a channel in analytics.

Usage:
    python3 utm_builder.py --base-url https://example.com/signup --campaign launch-apr-2026 \
        --channel "producthunt:producthunt/social" \
        --channel "x-twitter:twitter/social|hero-cta"
    python3 utm_builder.py --base-url https://example.com --campaign launch-2026 \
        --channels-file channels.csv --json
    python3 utm_builder.py --help

Channel syntax (repeatable):
    --channel "NAME:SOURCE/MEDIUM"            utm_content defaults to NAME
    --channel "NAME:SOURCE/MEDIUM|CONTENT"    explicit utm_content

Channels file (CSV, header required):
    name,source,medium,content
    producthunt,producthunt,social,
    x-twitter,twitter,social,hero-cta

Normalization: every value is lowercased, trimmed, and spaces/underscores are
collapsed to single hyphens, so "Product Hunt" and "product_hunt" both become
"product-hunt". Source/medium pairs are the unit analytics reads, so the script
warns when the same pair is reused across different channels, or when one
channel name is pinned to two different pairs.

Output: data (the URLs) to stdout, diagnostics (warnings) to stderr. `--json`
emits the full structured result on stdout.

Exit codes: 0 = built successfully (warnings allowed), 2 = usage/input error.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

# Collapse any run of whitespace or separators into a single hyphen.
_SEP_RE = re.compile(r"[\s_]+")
_MULTI_HYPHEN_RE = re.compile(r"-{2,}")


def normalize(value: str) -> str:
    """Lowercase and hyphenate a UTM value consistently."""
    text = _SEP_RE.sub("-", str(value).strip().lower())
    text = _MULTI_HYPHEN_RE.sub("-", text)
    return text.strip("-")


def parse_channel(spec: str) -> tuple[str, str, str, str]:
    """Parse 'NAME:SOURCE/MEDIUM[|CONTENT]' into (name, source, medium, content)."""
    if ":" not in spec:
        raise ValueError(
            f"channel '{spec}' is missing the ':' separator. "
            "Expected NAME:SOURCE/MEDIUM (e.g. producthunt:producthunt/social)."
        )
    raw_name, rest = spec.split(":", 1)
    if "|" in rest:
        source_medium, raw_content = rest.split("|", 1)
    else:
        source_medium, raw_content = rest, ""
    if "/" not in source_medium:
        raise ValueError(
            f"channel '{spec}' source/medium '{source_medium}' is missing the '/'. "
            "Expected NAME:SOURCE/MEDIUM (e.g. reddit:reddit/community)."
        )
    source, medium = source_medium.split("/", 1)

    name = normalize(raw_name)
    source = normalize(source)
    medium = normalize(medium)
    content = normalize(raw_content) if raw_content.strip() else name

    if not name:
        raise ValueError(f"channel '{spec}' has an empty name before ':'; expected NAME:SOURCE/MEDIUM.")
    if not source:
        raise ValueError(f"channel '{spec}' has an empty source; expected NAME:SOURCE/MEDIUM.")
    if not medium:
        raise ValueError(f"channel '{spec}' has an empty medium; expected NAME:SOURCE/MEDIUM.")
    return name, source, medium, content


def load_channels_file(path: str) -> list[str]:
    """Read a CSV of name,source,medium[,content] and return channel specs."""
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames is None:
                raise ValueError("file is empty")
            fields = [f.strip().lower() for f in reader.fieldnames]
            missing = [c for c in ("name", "source", "medium") if c not in fields]
            if missing:
                raise ValueError(
                    f"CSV header is missing required column(s): {', '.join(missing)}. "
                    "Expected a header row: name,source,medium,content"
                )
            specs = []
            for i, row in enumerate(reader, start=2):  # row 1 is the header
                row = {(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
                if not any(row.get(c) for c in ("name", "source", "medium")):
                    continue  # skip blank lines
                if not row.get("name") or not row.get("source") or not row.get("medium"):
                    raise ValueError(
                        f"{path} line {i}: name, source, and medium are all required. "
                        f"Got name='{row.get('name')}', source='{row.get('source')}', "
                        f"medium='{row.get('medium')}'."
                    )
                spec = f"{row['name']}:{row['source']}/{row['medium']}"
                if row.get("content"):
                    spec += f"|{row['content']}"
                specs.append(spec)
    except FileNotFoundError:
        sys.stderr.write(f"Error: channels file not found: {path}\n")
        raise SystemExit(2)
    except ValueError as exc:
        sys.stderr.write(f"Error: {path}: {exc}\n")
        raise SystemExit(2)
    if not specs:
        sys.stderr.write(
            f"Error: {path} contained no channel rows. "
            "Add at least one row with name, source, and medium.\n"
        )
        raise SystemExit(2)
    return specs


def build_url(base_url: str, params: dict[str, str]) -> str:
    """Append UTM params to base_url, preserving any existing query string."""
    parsed = urlparse(base_url)
    existing = parse_qsl(parsed.query, keep_blank_values=True)
    merged = existing + list(params.items())
    return urlunparse(parsed._replace(query=urlencode(merged)))


def collect_warnings(rows: list[dict]) -> list[str]:
    """Flag duplicate and inconsistent source/medium naming."""
    warnings: list[str] = []
    pairs_to_names: dict[tuple[str, str], set[str]] = {}
    name_to_pairs: dict[str, set[tuple[str, str]]] = {}
    seen_triples: dict[tuple[str, str, str], str] = {}

    for row in rows:
        pair = (row["source"], row["medium"])
        triple = (row["name"], row["source"], row["medium"])
        pairs_to_names.setdefault(pair, set()).add(row["name"])
        name_to_pairs.setdefault(row["name"], set()).add(pair)
        if triple in seen_triples:
            warnings.append(
                f"duplicate channel '{row['name']}' with source/medium "
                f"'{row['source']}/{row['medium']}' appears more than once — "
                "the URLs are identical, so the second adds nothing."
            )
        else:
            seen_triples[triple] = row["name"]

    for pair, names in sorted(pairs_to_names.items()):
        if len(names) > 1:
            warnings.append(
                f"source/medium '{pair[0]}/{pair[1]}' is shared by multiple channels "
                f"({', '.join(sorted(names))}) — analytics will blend them. "
                "Give each channel its own pair, or merge them intentionally."
            )
    for name, pairs in sorted(name_to_pairs.items()):
        if len(pairs) > 1:
            pretty = ", ".join(f"{s}/{m}" for s, m in sorted(pairs))
            warnings.append(
                f"channel '{name}' maps to more than one source/medium ({pretty}) — "
                "pick one so the channel reports as a single line in analytics."
            )
    return warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build consistently named UTM-tagged URLs for launch and distribution "
            "channels, and warn about duplicate or inconsistent source/medium naming."
        ),
        epilog=(
            "Channel syntax: NAME:SOURCE/MEDIUM or NAME:SOURCE/MEDIUM|CONTENT "
            "(repeatable). Or pass a CSV with header name,source,medium,content via "
            "--channels-file. Values are lowercased and hyphenated. "
            "See the docstring at the top of this file for the full schema."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--base-url", required=True,
                        help="https:// page the campaign points at (e.g. https://example.com/signup)")
    parser.add_argument("--campaign", required=True,
                        help="campaign name, e.g. launch-apr-2026 (normalized to lowercase-hyphens)")
    parser.add_argument("--channel", action="append", default=[], metavar="NAME:SOURCE/MEDIUM",
                        help="a channel, repeatable; NAME:SOURCE/MEDIUM or NAME:SOURCE/MEDIUM|CONTENT")
    parser.add_argument("--channels-file", metavar="PATH",
                        help="CSV file with header name,source,medium,content (content optional)")
    parser.add_argument("--json", action="store_true",
                        help="emit machine-readable JSON instead of the text list")
    args = parser.parse_args(argv)

    base_url = args.base_url.strip()
    parsed = urlparse(base_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        sys.stderr.write(
            f"Error: --base-url '{args.base_url}' must be an absolute http(s) URL, "
            "e.g. https://example.com/signup\n"
        )
        return 2

    campaign = normalize(args.campaign)
    if not campaign:
        sys.stderr.write("Error: --campaign must contain at least one letter or digit.\n")
        return 2

    specs = list(args.channel)
    if args.channels_file:
        specs.extend(load_channels_file(args.channels_file))
    if not specs:
        sys.stderr.write(
            "Error: no channels given. Pass at least one --channel NAME:SOURCE/MEDIUM, "
            "or --channels-file PATH.\n"
        )
        return 2

    rows: list[dict] = []
    for spec in specs:
        try:
            name, source, medium, content = parse_channel(spec)
        except ValueError as exc:
            sys.stderr.write(f"Error: {exc}\n")
            return 2
        params = {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": campaign,
            "utm_content": content,
        }
        rows.append({
            "name": name,
            "source": source,
            "medium": medium,
            "content": content,
            "params": params,
            "url": build_url(base_url, params),
        })

    warnings = collect_warnings(rows)
    for warning in warnings:
        sys.stderr.write(f"warning: {warning}\n")

    if args.json:
        result = {
            "base_url": base_url,
            "campaign": campaign,
            "channels": [
                {
                    "name": r["name"],
                    "source": r["source"],
                    "medium": r["medium"],
                    "content": r["content"],
                    "url": r["url"],
                }
                for r in rows
            ],
            "warnings": warnings,
        }
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Campaign: {campaign}")
        print(f"Base URL: {base_url}")
        print(f"Channels: {len(rows)}")
        print("")
        width = max((len(r["name"]) for r in rows), default=7)
        for r in rows:
            print(f"{r['name']:<{width}}  {r['url']}")
        if warnings:
            print("")
            print(f"{len(warnings)} warning(s) — see stderr. Fix naming before you post.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
