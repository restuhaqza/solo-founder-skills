---
name: solo-founder-os
description: Route a solo founder to the one skill that answers their real question. It bootstraps the shared founder/ workspace, writes founder/context.md, reads whatever artifacts already exist, diagnoses which lifecycle job is actually at stake, and reports what is done, empty, and missing before handing off to the owning skill. Use this skill whenever a solo founder is unsure where to start, asks an ambiguous question that could belong to validation, product, pricing, launch, metrics, or ops, wants help deciding what to work on next, is setting up the founder/ workspace for the first time, or asks "where do I start?", "what should I do next?", "which skill do I use?", "am I missing anything?", "give me the lay of the land", or "I have an idea, a product, and some users — now what?" — even if they never name this skill or any other.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: operating
---

# Solo Founder OS

Use this skill as the front door to the pack: set up the shared workspace, work out which job the founder actually has, and hand off to the one skill that owns it. It also answers the standing question "what's done and what's missing?" with a status check across the whole lifecycle. **It routes; it does not replace any other skill.**

The routing answer is a short reply, not a file. The only file this skill writes is `founder/context.md` on bootstrap — every other artifact belongs to the skill it routes to.

## The one rule

Route before you act. The founder's first stated question is rarely the real question: "how much should I charge?" is often an activation problem, and "how do I get users?" is often a positioning problem. Diagnose the job behind the words, pick exactly one owner, and hand off. Answering the literal question here is how this skill becomes a worse version of every other skill in the pack.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Bootstrap founder/ and founder/context.md if missing
- [ ] Step 2: Read context.md and the artifacts that already exist
- [ ] Step 3: Diagnose which job is actually at stake (references/routing-table.md)
- [ ] Step 4: Route to ONE skill and name the single next artifact
- [ ] Step 5: Report status with scripts/founder_status.py
- [ ] Step 6: Keep the loop — hand off and expect to be called again
```

**Step 1 — Bootstrap the shared workspace**
If `founder/` or `founder/context.md` is missing, create the folder tree (`validation/ product/ pricing/ gtm/ metrics/ ops/`) and write `founder/context.md` from `assets/context.md`. Fill in what you already know: the product one-liner, the ICP, the stage, the north-star metric, and the stack. Everything downstream reads this file instead of re-asking, so a missing `context.md` is the first gap to close — but keep it to one page. A shared brief that nobody keeps current is worse than no brief.

**Step 2 — Read context.md and whatever already exists**
Read `founder/context.md`, then skim the artifacts that are already on disk. The existing files tell you more than the question does: a founder with a `go-no-go.md` and no `mvp-spec.md` is at a different job than one with a live product and no metrics. Read the context *and* the evidence of what has been done before diagnosing.

**Step 3 — Diagnose the job**
Match the founder's situation — not just their words — to exactly one skill using `references/routing-table.md`. The table maps concrete phrases to the owning skill, but the value is in the middle column: the *job*. Name the job out loud in one line, then pick its owner. If two jobs seem to apply, the earlier one in the lifecycle loop usually comes first ("you can't price what nobody has validated").

**Step 4 — Route**
Name the one skill and the single next artifact it should produce, and say why. One skill, one artifact. If the diagnosis is that the literal question was the wrong one, say so plainly and route to the right job — that correction is the most useful thing this skill does.

**Step 5 — Check status (when asked, or as a default)**
Run `scripts/founder_status.py` to see, per skill, which expected artifacts exist, are empty, or are missing — plus the one next step, chosen by lifecycle order. This is how the founder sees the whole board at a glance. Do not fix the gaps here; report them and let the routing do the work.

**Step 6 — Keep the loop**
The lifecycle is a loop, not a line: validation feeds positioning, distribution feeds product discovery, retention feeds pricing. After the routed skill finishes its artifact, the founder will be back — with a new question, or with the old one restated. Expect to run this diagnosis again; do not try to answer every future question now.

## Output format

Use this as the routing reply:

```markdown
# Where you are
- **Situation:** <the founder's situation in one line, restated as the underlying job>
- **Skill that owns it:** `<skill-name>`
- **Next artifact:** `founder/<area>/<file>`
- **Why:** <the diagnosis — why this job, not the one that was literally asked about>

## Status
<the founder_status.py checklist: present / empty / missing per artifact,
completion %, and the single most-in-need-of-attention next step>
```

Keep it short. The founder wants to know which door to walk through, not a summary of every room.

## Gotchas

- **Routing is a diagnosis, not a menu.** Pick ONE skill. "It depends — here are three options" is the failure mode this skill exists to prevent. If you are torn, choose the earlier job in the lifecycle and say why.
- **`context.md` must stay short or it rots.** It is a shared brief, not a doc. A field a downstream skill never reads does not belong in it. When it stops matching reality, fix it — do not append to it.
- **Do not do the other skills' work here.** This skill writes routing answers and the bootstrap file. No go/no-go scorecards, no MVP specs, no pricing pages, no launch plans, no metrics digests — route to the skill that owns each one.
- **The boundaries still apply after you hand off.** The go / no-go / pivot / kill call belongs to the founder (not to `idea-validation`). Outbound messages are drafted, never sent, by any skill. Legal, tax, and entity decisions are first drafts flagged for a professional. This skill never overrides those; it just points at the skill that respects them.
- **A clear, single-domain question does not need routing.** If the founder already named the job ("help me write the MVP spec"), skip the diagnosis and go straight there — the router is for ambiguity, not a toll booth on every request.

## Available scripts

- **`scripts/founder_status.py`** — scans a `founder/` directory, reports each expected artifact as present / empty / missing, prints a completion percentage, and names the single next step in lifecycle order. Handles a missing `founder/` dir gracefully. Run: `python3 scripts/founder_status.py` (add a path or `--json` to taste).

## Reference files

- **`references/routing-table.md`** — the situation → skill table, the ASCII lifecycle loop, and a note on when *not* to reach for a skill. Read at Step 3 before diagnosing.
- **`assets/context.md`** — the one-page shared brief template. Copy to `founder/context.md` at Step 1.

## Hand-off

Hand off to whichever skill the diagnosis selects — and only that one:

- Uncertain the idea is real → `idea-validation` (next artifact: `founder/validation/go-no-go.md`).
- Idea validated, ready to scope → `mvp-scoping` (next artifact: `founder/product/mvp-spec.md`).
- Spec done, ready to build → `saas-scaffold` (next artifact: `founder/product/scaffold-plan.md`).
- Needs signup, payments, or plan gating → `auth-and-billing` (next artifact: `founder/product/billing-spec.md`).
- About to invite the first users → `launch-readiness` (next artifact: `founder/product/launch-readiness.md`).
- Have a product, need a price → `pricing-strategy` (next artifact: `founder/pricing/pricing.md`).
- Ready to launch or starved for users → `go-to-market-launch` (next artifact: `founder/gtm/launch-plan.md`).
- Need numbers, or growth/churn is puzzling → `product-metrics` (next artifact: `founder/metrics/metrics-spec.md`).
- Wearing too many hats, worried about runway or burnout → `founder-operating-rhythm` (next artifact: `founder/ops/weekly-review.md`).

Pass the routed skill the relevant fields from `founder/context.md` so it does not re-interview the founder.
