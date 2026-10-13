---
name: founder-operating-rhythm
description: Run the solo founder's personal operating system — the weekly review ritual, ruthless prioritisation, runway and simple finance, a decision journal, burnout guardrails, and an ops/legal checklist. Use this skill whenever a solo founder or indie builder wants to plan their week, decide what to work on next, check how many months of runway they have or whether they are default alive or default dead, keep a decision log, set up bookkeeping or a tax set-aside, get a pre-launch legal/ops checklist, or guard against burnout and the quiet middle — even if they only say "what should I focus on this week?", "am I running out of money?", "I'm wearing too many hats", or "what do I actually need to set up legally?".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: operating
---

# Founder Operating Rhythm

Use this skill to run the founder's side of a one-person business: a weekly rhythm that keeps attention on the ONE thing that matters, a runway number that tells the truth about cash, a decision log that stops you re-litigating the same call, and ops/legal guardrails that keep the business unencumbered. It produces files you fill in, not a report you read once.

Outputs land in `founder/ops/` so later skills and future you can pick them up. If `founder/context.md` is missing, create it first (product one-liner, ICP, stage, north-star metric, stack).

## The one rule

**The founder is the scarcest resource. Protect attention and cash.** Every step below exists to spend one of those two more carefully. Time you spend switching hats is time not spent on the ONE thing; money you do not watch is runway you cannot see disappearing. When a step tempts you to do *more*, the right answer is usually *less, chosen on purpose*.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Run the weekly review ritual (assets/weekly-review.md)
- [ ] Step 2: Prioritise — pick the ONE thing, then now/next/later
- [ ] Step 3: Check runway and finance (run scripts/runway.py)
- [ ] Step 4: Log decisions as Type 1 or Type 2 (assets/decision-log.md)
- [ ] Step 5: Work the ops/legal checklist (references/ops-legal-checklist.md)
- [ ] Step 6: Set the sustainability guardrails
- [ ] Step 7: Decide agent stack vs first hire, at the margin
```

**Step 1 — Run the weekly review ritual**
One page, once a week, at a fixed time. The review is not a dashboard; it ends in a decision. Open `assets/weekly-review.md`, copy it to `founder/ops/weekly-review.md`, and fill in: the numbers you already track (revenue, churn, signups — pulled from `product-metrics`, do not re-derive them here), what moved, what stalled, **three priorities for next week**, and **one action you will take before the next review**. Why: a weekly checkpoint is the smallest unit of accountability a solo founder can keep, and it is the antidote to the slow drift described in Step 6. Keep it under a page — a ritual you dread is a ritual you skip.

**Step 2 — Prioritise: pick the ONE thing**
Most weeks you have a dozen plausible tasks and capacity for one. Decide the ONE thing that, if finished, would make the other tasks smaller or moot. Then sort the rest into a **now / next / later** list and forget `later` until the next review. For a short menu of scoring: **ICE** (Impact × Confidence × Ease) when you have little data, **RICE** (Reach × Impact × Confidence ÷ Effort) when you are choosing between features with traceable usage. Do not over-invest in the score — its job is to force a ranking, not to be right.

Then protect the ONE thing against the day. **Time-block two or three hours of deep work** and defend that block the way you would a customer call. Track the cost of context switching: each time you jump between hats (support → SQL → pricing → legal) you pay a re-orientation tax. **Cap the number of hat switches per day** — log them in the weekly review and count them. If the count is high, the fix is usually batching (all support at two set times, all code in the deep block), not more discipline.

**Step 3 — Check runway and finance**
Finance is four numbers and a projection. Feed what you know to the script:

```bash
python3 scripts/runway.py --cash 120000 --revenue 8000 --costs 14000 --growth 6
```

It returns **net monthly burn**, **runway in months**, the **break-even month** (if revenue growth closes the gap), a **tax set-aside per month**, the **growth rate at which the verdict flips** (the monthly revenue growth you must hold to stay default alive, reported on both a pre-tax and an after-tax basis), and Paul Graham's **default alive / default dead** verdict — does revenue reach costs within the cash the business has, given the growth rate? Run the flat or declining case too (`--growth 0`, or negative) so you see the downside honestly; the script handles zero and negative growth without dividing by zero. Log the outputs into `assets/runway.csv` so next month is a comparison, not a cold start. When you report to the founder, lead with the flip growth rate — "am I going to make it?" is answered by "hold X%/mo or more," which is a number they can act on this week. Read `references/runway-and-finance.md` for the definitions, the 25–30% set-aside habit, the monthly bookkeeping and quarterly reconciliation rhythm, and why separate personal/business money matters.

**Step 4 — Log decisions as Type 1 or Type 2**
Keep a running decision journal. For each meaningful decision, record the options considered, the reasoning, and — the part most people skip — **what would change your mind**, plus a date to revisit it. Mark each one **Type 1 (irreversible, or very expensive to undo)** or **Type 2 (reversible, cheap to undo)**. Why the label matters: Type 1 decisions (entity choice, a pricing change that affects existing customers, killing a channel) deserve slow, deliberate thought; Type 2 decisions (most feature choices, an experiment, a copy change) should be made fast and cheaply, because the cost of deliberating exceeds the cost of being wrong. Founders grind hardest on the reversible calls and rush the irreversible ones — the label flips that. Use `assets/decision-log.md`.

**Step 5 — Work the ops/legal checklist**
Read `references/ops-legal-checklist.md` and separate **essential pre-launch** (entity if you have liability exposure, a business bank account separate from personal, basic ToS and privacy policy once you collect data or money, tax registration) from **can wait** (trademarks, elaborate contracts, a full DPA until a customer asks). This step produces a first draft and a to-do list — **it never signs, files, or decides.** Entity choice, tax filings, and document wording are human-reviewed and, where stakes are real, reviewed by a professional. If you are a non-US owner of a US LLC, that reference flags the **Form 5472** information return and its penalty; treat it as a prompt to talk to a professional, not as a filing instruction.

**Step 6 — Set the sustainability guardrails**
The most dangerous moment for a solo founder is not failure — it is the **quiet middle**: the long stretch after the launch hype fades and before the compounding shows up, when progress stops producing dopamine and starts producing doubt. Burnout spikes when founders lose their **small checkpoints**. So agree, in advance, on guardrails: a floor on hours and a ceiling on them, one non-work day that is actually non-work, a named person or ritual to check in with, and a definition of a "good week" that does not depend on a launch. Break big goals into weekly checkpoints (Step 1 is the engine for this) so progress is visible between quarterly milestones. If two review cycles pass with the same stuck item, treat that as data, not as a personal failure.

**Step 7 — Decide agent stack vs first hire, at the margin**
By the time a solo business nears roughly $20K MRR, the old default question — "when do I make my first hire?" — increasingly has a sibling: "what does an agent stack cost?" Many solo founders now run several specialised agents (coding, inbox/CRM, support, content, an ops agent) for a few hundred dollars a month instead of making a first hire. This skill does not tell you to buy agents or to hire. It frames the trade: an agent stack is cheap, fast to change, and does not onboard; a first hire adds judgement, relationships, and accountability that agents do not carry, plus a fixed cost you cannot un-commit in a bad month. Decide at the margin — what is the next bottleneck, and which option removes it for the least cash and least founder attention? Both routes still leave the founder owning strategy, outbound, and the relationships.

## Output format

Write `founder/ops/weekly-review.md` (from the asset) using this structure:

```markdown
# Weekly Review — <week of date>
_Owner: <you> · Time spent: <min>_

## Numbers (from product-metrics, not re-derived here)
- Revenue / MRR: <value> (<+/- change>)
- New signups / activation: <value>
- Churn: <value> (<voluntary / involuntary if known>)

## What moved
- <outcome, not activity>

## What stalled
- <item> — <why> — <will I keep, cut, or reframe it?>

## The ONE thing next week
<the single outcome that makes other tasks smaller>

## Three priorities
1. <priority>
2. <priority>
3. <priority>

## One action before next review
<the concrete, checkable action, with a date>

## Hat switches today / this week
<count + the worst offender>

## Energy
<1–5, one line on what drove it>
```

Keep a separate running `founder/ops/decision-log.md` and `founder/ops/runway.csv`.

## Gotchas

- **This skill never gives binding legal or tax advice.** Everything legal or financial here is a first draft or a checklist for a professional to review. Entity choice, filings, and contract wording are the founder's, with an accountant or lawyer where stakes are real.
- **Commingled money breaks liability protection.** Paying personal expenses from the business account (or vice versa) is the classic way a single-member LLC loses the separation it exists for. Separate accounts, separate cards, clean transfers.
- **Activity is not progress.** A full calendar of "shipped a little of everything" can hide zero movement on the metric that matters. Write outcomes in the review, not a task log.
- **The quiet middle is the real risk, not the launch.** Plan for week 30, not launch week. Burnout comes from lost checkpoints, not from a single hard sprint.
- **Over-tooling is a hidden tax.** Every tool is a future debugging session, an integration to maintain, and a new place to look. Keep the stack holdable in your head; cut anything you did not open this month.
- **Do not hire before you have priced the agents.** At the margin, a first hire is a fixed cost you cannot undo in a bad month; an agent stack is variable and swappable. Frame the decision before defaulting to either.
- **A projection is not a promise.** The runway script assumes today's costs and growth hold. They rarely do — re-run it monthly and keep the input honest.

## Available scripts

- **`scripts/runway.py`** — takes cash, monthly revenue, monthly costs, and monthly growth (percent, may be 0 or negative), optional `--tax-rate` and `--months`, and prints net burn, runway in months, break-even month, tax set-aside, the flip growth rate (the minimum monthly growth to stay default alive, pre-tax and after-tax), and the default-alive/default-dead verdict. `--json` for structured output, `--project` for a month-by-month table. Run `python3 scripts/runway.py --help` for the input schema.

## Reference files

- **`references/runway-and-finance.md`** — the default alive/dead test and runway definition, the tax set-aside habit, and the monthly/quarterly bookkeeping rhythm. Read at Step 3.
- **`references/ops-legal-checklist.md`** — essential pre-launch vs can-wait, entity and EIN basics, the commingling trap, ToS/privacy/DPA basics, and the Form 5472 note. Read at Step 5.
- **`assets/weekly-review.md`** — the one-page weekly template. Copy to `founder/ops/weekly-review.md`.
- **`assets/decision-log.md`** — decision journal with the Type 1 / Type 2 column. Copy to `founder/ops/decision-log.md`.
- **`assets/runway.csv`** — month-by-month finance log so each review is a comparison.

## Hand-off

This skill consumes the numbers; it does not produce them. When a review surfaces a question about *what the numbers mean* — why churn moved, which activation event predicts retention — hand back to `product-metrics` and bring the answer into next week's review. When a decision is a go/no-go on the product itself, that belongs to `idea-validation`, not here.
