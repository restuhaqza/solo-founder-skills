# SKILL-STANDARDS.md — the house style for this collection

This file is the contract every skill in this repo follows. The `idea-validation`
skill is the reference implementation — read it before writing a new skill.

---

## 1. Repo layout

```
solo-founder-skills/
├── README.md                     # human catalog + install
├── LICENSE
├── .claude-plugin/marketplace.json
├── docs/
│   ├── SKILL-STANDARDS.md         # this file
│   └── research/                  # the two source research reports
├── template/SKILL.md              # copy-paste scaffold
└── skills/<name>/
    ├── SKILL.md                   # required
    ├── scripts/                   # deterministic, stdlib-only where possible
    ├── references/                # docs loaded on demand, one level deep, TOC if >100 lines
    ├── assets/                    # templates the founder copies and fills in
    └── evals/evals.json           # >= 3 realistic prompts
```

Do **not** put a `SKILL.md` at the repo root — the root is a catalog, not a skill.

## 2. Frontmatter (portable — exactly these six keys)

```yaml
---
name: <kebab-case, must equal the folder name, no leading/trailing/double hyphens>
description: <what it does + when to use it; third person; pushy; <= 1024 chars>
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: <validation | product | pricing | gtm | metrics | operating>
---
```

Optional `compatibility:` only when a real environment constraint exists. No other
top-level keys — anything else breaks claude.ai / Skills API uploads (hard error).

**Description rules.** State **what** + **when**, in the third person ("Validates…",
never "I can help…"). Be specific and a little pushy: list the concrete phrases and
situations that should trigger it, including cases where the user does *not* name the
domain ("even if they only say …"). Lead with the outcome, since the description is the
entire trigger mechanism.

## 3. Body shape

Keep the body **under ~500 lines**. Use these sections, in this order, dropping any that
genuinely do not apply:

1. Title + 1–2 sentence promise, including where output goes.
2. **The one rule** (optional) — the single principle that keeps the skill honest.
3. **Workflow** — a copyable checkbox list, then each step with the *why* explained.
4. **Output format** — an exact template for the file(s) produced (or "use as a default").
5. **Gotchas** — environment facts that defy a reasonable assumption.
6. **Available scripts** — name, what it does, one-line run command.
7. **Reference files** — name, what it covers, and *when* to read it.
8. **Hand-off** — which sibling skill takes the baton next.

## 4. Progressive disclosure

- SKILL.md = the table of contents + what is needed on *every* run.
- `references/` = detail read on demand. **One level deep only.** Any reference over
  100 lines starts with a `Contents` list.
- `scripts/` = deterministic logic. The code never enters context; only its output does.
- `assets/` = templates the founder copies into their workspace and edits.

Always say whether to **run** or **read** a file ("Run `scope_score.py`…" vs
"See `boring-stack.md` for the decision table").

## 5. Script rules

- **Python 3, standard library only** so it runs anywhere with `python3`. No network,
  no installs, no third-party imports.
- **Non-interactive.** Never prompt for input; take everything via argv/stdin/flags.
  (A prompt in a non-interactive agent shell hangs forever.)
- `argparse` with a real `--help`: description, flags, an input-schema note.
- **Data to stdout, diagnostics to stderr.** Support `--json` for machine-readable output
  on anything another skill or a human might consume.
- Helpful, specific error messages that say what was expected ("`assumptions[0].type`
  'nope' is invalid. Options: value, viability, usability, feasibility").
- Sensible exit codes: `0` success, `2` usage/input error.
- No magic constants without a comment explaining them.
- Forward slashes in all paths.

## 6. Human-approval boundaries (non-negotiable)

These are the founder's to own. The skill prepares; the human decides or sends:

- The go / no-go / pivot / kill call.
- Sending any outbound message (cold email, community post, investor update) — draft only.
- Legal, tax, entity, and accounting decisions — first drafts only, flagged for review.
- Moving money and pricing/plan changes that affect existing customers.

Every skill that touches these must say so explicitly in its Gotchas or a boundary note.

## 7. Writing style

- Imperative voice. Explain the **why** so the model can generalise past the example.
- No heavy-handed ALL-CAPS MUST/NEVER. Reasoning-based instructions are followed better.
- Teach the *method*, not a single answer. Never hardcode a specific product's numbers.
- One default with an escape hatch, not a menu of five options.
- Assume the reader is smart; cut anything an LLM already knows.

## 8. Shared workspace convention

Skills read and write a `founder/` folder at the project root so they compose:

```
founder/
├── context.md          # product, ICP, stage, north star, stack — shared by all skills
├── validation/         # idea-validation
├── product/            # mvp-scoping
├── pricing/            # pricing-strategy
├── gtm/                # positioning-and-messaging, go-to-market-launch, content-and-seo-engine
├── metrics/            # product-metrics
├── growth/             # experiments-and-growth
├── support/            # support-and-onboarding
├── ops/                # founder-operating-rhythm
└── fundraising/        # fundraising-and-investor-updates
```

If `founder/context.md` is missing, create it (product one-liner, ICP, stage, north-star
metric, stack) before writing other outputs. Keep it short — it is a shared brief, not a doc.

## 9. Ship checklist

- [ ] Folder name == `name` field; only the six frontmatter keys.
- [ ] Description states what + when, third person, includes non-obvious triggers.
- [ ] Body under ~500 lines; detail lives in one-level-deep references.
- [ ] Every script runs: `python3 scripts/<x>.py --help` exits 0.
- [ ] Every script run at least once on the bundled sample input, output checked.
- [ ] Output templates present in `assets/`; human-approval boundaries called out.
- [ ] `evals/evals.json` has >= 3 realistic prompts with expectations.
- [ ] No time-sensitive claims stated as permanent; no invented statistics.
