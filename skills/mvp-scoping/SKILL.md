---
name: mvp-scoping
description: Turn a validated idea into the smallest shippable MVP plus a build plan — define the one core action, write observable exit criteria before any code, break the idea into features, score and cut them with a RICE-ish 90/10 rule, write the anti-scope list, choose a boring stack, and sequence a walking skeleton into small verifiable slices. Use this skill whenever a solo founder or indie builder is ready to scope or cut features, decide what version 1 actually contains, write an MVP spec or PRD, choose a stack, or hand a build to a coding agent — even if they only say "what should I build first?", "this is getting too big", "help me write the spec", or "I keep adding features".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: product
---

# MVP Scoping

Use this skill to turn a validated idea into the *smallest thing that proves the value* — and a sequence for building it — instead of the thing you secretly want to build. It produces a scored, cut feature list, a one-page MVP spec, and a build order a coding agent can pick up. Outputs land in `founder/product/`.

## The one rule

**90% of the value for 10% of the work.** Every feature you keep must defend its place against a shippable alternative that is smaller. And **exit criteria come before code**: you decide what "v1 works" *observes* — before a single line is written. If you cannot state the behaviour that proves v1 works, you are not ready to build; you are ready to scope.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Name the single core action / core loop
- [ ] Step 2: Write exit criteria BEFORE any coding
- [ ] Step 3: Break the idea into candidate features (assets/feature-backlog.csv)
- [ ] Step 4: Score and cut with scripts/scope_score.py; draw the 90/10 line
- [ ] Step 5: List what is NOT in v1 (the anti-scope list) and park it
- [ ] Step 6: Decide build vs buy vs no-code per component; pick the boring stack
- [ ] Step 7: Write the MVP spec (assets/mvp-spec.md)
- [ ] Step 8: Sequence a walking skeleton then small verifiable slices
- [ ] Step 9: Verify — no feature in v1 without an exit-criteria link
```

**Step 1 — Name the single core action / core loop**
A product exists to deliver one action to one user. Write it as a verb phrase a stranger could repeat: *"send an invoice and get paid"*, *"turn a screenshot into a shareable link"*. Then name the **core loop**: the action, its feedback signal, and what brings the user back (create → send → see paid → repeat). Everything in v1 either *is* that loop or is load-bearing for it. If you cannot name the core action in one sentence, you have a bundle of features, not a product — that is the first thing to fix. See `references/mvp-spec-guide.md` §1 for how to name it.

**Step 2 — Write the exit criteria (before any coding)**
Exit criteria are the **observable** behaviour that proves v1 works — the thing you can watch happen, not the thing you feel. "Users find it useful" is not observable; "a new user completes one invoice in under 3 minutes without help, and it is visible as paid within 24 hours" is. Write them as binary checks a person could tick, tied to the core loop, at the level of a single user and a single pass. Doing this *first* is what stops the build from expanding to fill the time available: once the criteria are written, features that do not move a criterion are visibly optional. Use the exit-criteria section of `assets/mvp-spec.md`.

**Step 3 — Break the idea into candidate features**
List every feature the product *could* have, generously and without judging — capture is not commitment. Log them in `assets/feature-backlog.csv` with the columns the script expects: `id,name,impact(1-5),confidence(1-5),effort(1-5),must_have(yes/no)`. Be honest about **confidence**: a feature whose impact you believe but have not seen evidence for is a 2, not a 5. Be honest about **effort**, especially the ongoing maintenance cost a solo founder pays forever — a feature is not "done" when it ships. Keep `must_have` strict: it means "the core loop does not function without this". If the loop works without it, it is not a must-have.

**Step 4 — Score and cut**
Run the scorer, which computes `score = impact × confidence / effort` and draws the cut:

```bash
python3 scripts/scope_score.py founder/product/feature-backlog.csv
```

Must-haves are included unconditionally; the rest are added highest-score-first until v1 retains `--target` of the total score (default `0.90`). The output is a table of what is IN and OUT of v1, the share of value retained, and flags for items that are too big or too speculative. Treat the cut as a *proposal* — the script ranks, the founder decides. If a non-must-have keeps surviving every cut, that is a signal it is really part of the core loop, and your Step 1 definition is wrong. Do not edit the formula to force a feature in; change the impact/confidence/effort inputs only when you can justify the change.

**Step 5 — Write the anti-scope list (what is NOT in v1)**
The OUT list is a deliverable, not a leftover. For each parked feature, write one line of *why later* and the trigger that would pull it into v2 ("when 3+ users ask for it", "when someone pays for it"). This is the difference between saying no and forgetting; the parked list is what you point at in six weeks when the same tempting feature resurfaces. Keep it in the MVP spec's out-of-scope section.

**Step 6 — Decide build vs buy vs no-code, and pick the boring stack**
Walk each component of the v1 spec and choose **buy** (managed service), **no-code** (a tool that already exists), or **build** (only the thing that is genuinely your differentiation). Default hard toward buy and no-code. Then pick a stack from `references/boring-stack.md`: the 2026 default is Next.js + Supabase + Vercel + Stripe, and the boring extreme (PHP + SQLite + one VPS) is a legitimate choice. **Zero custom auth, zero custom payments** — these are solved problems that cost you weeks and leak security when hand-rolled. Log the stack decision in `founder/context.md` so later skills inherit it.

**Step 7 — Write the MVP spec**
Fill `assets/mvp-spec.md`: the core action, user stories, acceptance criteria in Given/When/Then form, the exit criteria from Step 2, the out-of-scope list from Step 5, and the stack decisions from Step 6. The spec is the contract between you and the coding agent — write it so a capable agent could build v1 from it without asking what you meant. Keep it to one page; length here is a scope smell, not thoroughness.

**Step 8 — Sequence a walking skeleton, then small verifiable slices**
Build order matters more than build speed. Start with the **walking skeleton**: the thinnest end-to-end path through the real stack (a real user signs up, does the core action once, sees the feedback) — even if each step is crude. A skeleton that runs end-to-end de-risks the integration, which is where solo builds actually die. Then add **small verifiable slices**, each one: (a) independently shippable, (b) verified against an acceptance criterion before the next begins, (c) never larger than a day or two of agent work. Hand each slice to the coding agent with its acceptance criteria and a "done" check. See `references/mvp-spec-guide.md` §5–6.

**Step 9 — Verify against the scope-creep guard**
Read the completed spec back against one test: **no feature is in v1 without a link to an exit criterion.** Every IN feature from Step 4 should trace to a criterion, and every criterion to a feature. Anything orphaned on either side is a scope leak — either an untested feature or a missing criterion. As you build, re-run this check whenever a new feature appears; the honest answer to most "should this be in v1?" questions is the anti-scope list.

## Output format

Write `founder/product/mvp-spec.md` using `assets/mvp-spec.md` as the template. Keep the six load-bearing sections: core action + core loop, user stories, acceptance criteria, exit criteria, out-of-scope, build sequence. A spec that omits the out-of-scope or exit-criteria sections is not done — those two are what hold the scope.

Also persist the ranked backlog as `founder/product/feature-backlog.csv` (the input the script already consumes), and record the chosen stack in `founder/context.md`.

## Gotchas

- **The MVP marathon.** Solo failure mode #1: weeks become months, motivation drains, and no feedback ever arrives because nothing shipped. The tell is a build with no exit criteria and no ship date. Fix: define exit criteria first (Step 2) and set a hard shipping date you treat as real. *"Ideas don't die. Execution momentum does."*
- **Scope creep, dressed as thoroughness.** "While I'm in there…" is how a one-week MVP becomes a quarter. The anti-scope list is the defence; keep it written down and point at it.
- **Building v2 features into v1.** Any feature whose value only shows up *after* other people are using the product belongs in v2. Recurring invoices, team seats, roles, and integrations are almost always v2 — v1 needs to prove one person gets value once.
- **Custom auth and custom payments.** These look like 2-day tasks and are month-long ones with real security and compliance risk. Buy them. If you find yourself writing session or card-handling code, stop and pick a managed provider.
- **Exit criteria that are not observable.** "Feels fast", "users like it", "it's polished" cannot be checked, so they never retire a feature. Rewrite every criterion as something you could watch a stranger do or read in a log.
- **"We'll need it eventually."** Almost everything is needed eventually; that is not a reason for now. The only question is whether the *core loop* breaks without it. If it doesn't, it is parked.
- **Effort is not just build effort.** The score divides by effort, and for a solo founder effort includes the maintain-and-support tail. A feature you can build in a day but must babysit for a year scores worse than its build time suggests.

## Available scripts

- **`scripts/scope_score.py`** — reads the feature-backlog CSV, computes `impact × confidence / effort`, draws the v1 cut at a `--target` fraction of total score, flags high-effort and low-confidence items, and reports the % of value retained. `--json` emits structured output. Run `python3 scripts/scope_score.py --help` for the input schema and the formula.

## Reference files

- **`references/boring-stack.md`** — the build/buy/no-code decision matrix, the 2026 default stack, and the boring extreme. Read at Step 6 when choosing what to build on.
- **`references/mvp-spec-guide.md`** — how to write user stories, acceptance criteria (Given/When/Then), exit criteria, the anti-scope list, the walking skeleton, and how to slice into small verifiable increments. Read at Steps 1–2 and 8.
- **`assets/mvp-spec.md`** — the fill-in MVP spec template. Copy to `founder/product/mvp-spec.md`.
- **`assets/feature-backlog.csv`** — the feature-backlog template with sample rows; the script reads this shape.

## Hand-off

When the MVP spec and the build sequence are done, hand the sequence to `saas-scaffold` to stand up the runnable skeleton and package the first slice for a coding agent, then `auth-and-billing` to wire signup and plan gating into it. After that, move to `pricing-strategy` (to decide what v1 costs before launch) and `go-to-market-launch` (to plan how the first users hear about it) — and `launch-readiness` is the gate before the first real users. Pass them the core action, the exit criteria (they become the launch's success signal), the ICP from `founder/context.md`, and the stack. The actual product code still belongs to a coding agent — `saas-scaffold` sets up the workshop; it does not build the product.
