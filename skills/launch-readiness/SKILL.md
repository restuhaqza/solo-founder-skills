---
name: launch-readiness
description: Harden a SaaS product for its first real users — find committed secrets, wire error tracking and a health route, set up uptime monitoring, document and test a database restore, practise a rollback, add rate limiting and spend caps, and prepare privacy/terms drafts flagged for a professional. Use this skill whenever a solo founder or indie builder is about to invite their first users, asks "am I ready to launch?", "what do I check before going live?", "what happens if my database dies?", "how do I roll back a bad deploy?", or is worried about security, secrets, abuse, or a charge they cannot afford — even if they only say "I'm nervous about shipping this", "going live tomorrow", or "someone found a bug in production".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: product
---

# Launch Readiness

Use this skill to answer the question every solo founder should ask before the first stranger touches the product: **is this safe to put in front of people, and can I recover when it breaks?** It runs a go-live scan, turns the gaps into a prioritised checklist, walks the go/no-go evidence, and records a one-page readiness file. Outputs land in `founder/product/`. **It prepares the evidence; the go / no-go call stays yours.**

## The one rule

**A clean scan is the floor, not the verdict.** Readiness is not "no findings" — it is knowing which risks you have closed, which you are knowingly accepting, and that you *can recover* from the ones you cannot prevent. Two things carry more weight than the rest: **no secret in the repo or its history, and a backup you have actually restored.** Everything else is a gap you can rank and choose.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Read context + scaffold/billing plans; note the stack and providers
- [ ] Step 2: Run the go-live scan (scripts/readiness_check.py)
- [ ] Step 3: Close the blockers, then the high-severity gaps
- [ ] Step 4: Prove recovery — rollback and a real restore
- [ ] Step 5: Add abuse and cost controls
- [ ] Step 6: Prepare legal/privacy drafts, flagged for a professional
- [ ] Step 7: Write founder/product/launch-readiness.md and run the go-live drill
- [ ] Step 8: Verdict + hand the go/no-go to the founder
```

**Step 1 — Read what exists**
Read `founder/context.md`, `founder/product/scaffold-plan.md`, and `founder/product/billing-spec.md`. They name the stack, the deploy target, and the billing provider — the scan reasons about those, and the recovery drills depend on them. If there is no scaffold plan, the product is probably not built yet; run `saas-scaffold` first.

**Step 2 — Run the scan**
From the repository root:

```bash
python3 scripts/readiness_check.py --doc founder/product/launch-readiness.md .
```

It groups gaps by severity (blocker / high / medium / low) and prints a verdict plus the single next thing to fix. Read the *blockers* as stop-ship items and the *high* gaps as things that cost money, data, or trust in week one. See `references/go-live-checklist.md` for why each item matters and what "done" looks like.

**Step 3 — Close the blockers, then the highs**
Order matters: a committed secret is rotated before anything else ships, because it is already exposed. Then no loose `.env`, then error tracking, rate limiting, backups, and privacy/terms drafts. Fix in severity order; a medium gap is not worth a late night while a blocker is open. For each, the checklist section tells you the concrete action, not just the label.

**Step 4 — Prove recovery**
Ranking gaps is theory; recovery is tested. Do two drills and record them: **roll back the last deploy** (and note which migrations are not reversible, because those need a forward fix), and **restore the database into a throwaway environment**, timing it and confirming the data is there. A backup you have never restored is a hope, and finding out during an incident is the expensive way to learn it. See `references/go-live-checklist.md` §3 and §8.

**Step 5 — Abuse and cost controls**
A solo product is one bad actor away from a bill you cannot pay. Rate-limit signup, login, password reset, checkout, and any expensive AI call, and set hard spend caps on the LLM/API and hosting accounts so a runaway loop cannot burn a month of revenue in an hour. A crude alert — a daily email when a counter crosses a threshold — beats none. See §4.

**Step 6 — Legal and privacy drafts**
Add a privacy policy and terms page before you store anyone's data, and a short data map of what you collect, where it lives, and which subprocessors (auth, payments, email, analytics, hosting) touch it. **These are first drafts flagged for a professional to review** — this skill never gives legal advice and never finalises them. Include a documented deletion path: if you collect it, you must be able to delete it. See §5.

**Step 7 — Write the file and run the drill**
Fill `assets/launch-readiness.md` and save it to `founder/product/launch-readiness.md`: the verdict, each closed item, and the gaps you are **knowingly** accepting and why. Then run the go-live drill in §8 once, out loud — deploy from clean `main`, do the core action as a brand-new paying user, confirm the webhook granted entitlement, force an error and see it tracked, roll back and forward, restore the database. Record what broke.

**Step 8 — Verdict, then hand over the call**
State the verdict plainly: `NOT_READY`, `READY_WITH_GAPS`, or `READY`. Name the remaining risks in one line each. Then stop — **the go / no-go decision belongs to the founder.** If they launch with a gap, it goes in the file as a chosen risk, not a missed one.

## Output format

Write `founder/product/launch-readiness.md` from `assets/launch-readiness.md`. Keep the sections: verdict + knowingly-accepted gaps, secrets, reliability (errors/health/monitoring/backups/rollback/flags), abuse and cost, legal/privacy drafts, the go-live drill checklist, and a short dated log. Start the file with the `readiness_check.py` summary so the doc and the scan agree. One page — this is a decision record, not an audit report.

## Gotchas

- **A committed secret is already leaked.** Removing the line does not un-leak it; it is in every clone's history. Rotate the key, then fix how it got there.
- **Backups are not a plan until a restore has run.** Managed databases turn backups on by default, which is exactly why nobody tests them. Do the restore once, on purpose.
- **Some migrations do not roll back.** Rolling back code while a migration has already run can leave the app and schema disagreeing. Know which of yours are irreversible before you need to.
- **The redirect is not the payment.** During the drill, confirm the *webhook* granted entitlement, not that the browser landed on a success page. See `auth-and-billing`.
- **Rate limiting is a cost control, not just security.** The endpoint that gets abused is usually the expensive one; cap it before someone finds out for you.
- **Legal output here is a draft, never advice.** Privacy, terms, and data handling are flagged for a professional. The pack prepares; it does not sign off.
- **Do not gold-plate.** SOC 2, multi-region failover, and a status page are for later, when a paying customer or an incident asks for them. Gold-plating a launch is its own failure mode.
- **The verdict is not the decision.** `readiness_check.py` informs the go / no-go; it never makes it. Launching with a known, written-down gap is a founder's call — launching with an unknown one is a mistake.

## Available scripts

- **`scripts/readiness_check.py`** — scans a repo for go-live gaps (committed secrets, loose `.env`, missing error tracking, rate limiting, backups, restore drill, rollback, uptime monitoring, legal pages, data map, lockfile, feature flags, debug mode, dependency audit) grouped by severity with a verdict and next step. `--doc` counts the boxes in the readiness markdown; `--strict` fails on any gap; `--json` emits structured output. Run: `python3 scripts/readiness_check.py --doc founder/product/launch-readiness.md .`

## Reference files

- **`references/go-live-checklist.md`** — the checklist behind the scan: what each item is, why it matters, its severity, the go/no-go framing, what can wait, and the numbered go-live drill. Read during Steps 3–8.
- **`assets/launch-readiness.md`** — the fill-in readiness template with the drill checklist and a dated log. Copy to `founder/product/launch-readiness.md`.

## Hand-off

Once the product is live, the loop reopens: hand the launch date and the core-action result to `go-to-market-launch` and `product-metrics` (the first cohort and its activation are now measurable), and keep `founder/product/launch-readiness.md` current as you ship. A new external integration, a new data type, or a first enterprise question each pulls this skill back in for a fresh pass.
