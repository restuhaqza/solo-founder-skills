---
name: idea-validation
description: Pressure-test a product idea before any production code is written — surface the riskiest assumptions, design cheap pre-validation tests, run The Mom Test customer-discovery interviews, scan competitors and current alternatives, and turn scattered evidence into a go/no-go scorecard. Use this skill whenever a solo founder or indie builder wants to validate an idea, decide whether something is worth building, prepare or synthesize customer interviews, or write up what they learned from users — even if they only say "is this a good idea?", "help me validate this", "I want to talk to customers", or "should I build this?".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: validation
---

# Idea Validation

Use this skill to decide whether an idea deserves to be built — with evidence, not enthusiasm. It turns a vague idea into a short list of *testable assumptions*, a cheap validation plan, and a scorecard that ends in a recommendation. **The founder makes the go/no-go call; this skill assembles the case and argues both sides honestly.**

Outputs land in a working folder so later skills can pick them up. Default: `founder/validation/`.

## The one rule

Real money beats signups. Past behaviour beats opinions. Silence beats politeness. If your evidence is compliments and waitlist emails, you have *interest*, which is not the same thing as *validation*. A person who says "I'd definitely use that" owes you nothing; a person who pre-pays has told you the truth.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Convert the idea into risky assumptions
- [ ] Step 2: Pre-validate on paper and kill weak ideas early
- [ ] Step 3: Design and run Mom Test interviews
- [ ] Step 4: Map competitors and the alternatives people use today
- [ ] Step 5: Test willingness to pay, not willingness to click
- [ ] Step 6: Score the evidence (run scripts/evidence_scorecard.py)
- [ ] Step 7: Write the go/no-go brief (the human decides)
- [ ] Step 8: Verify the brief against references/quality-bar.md
```

**Step 1 — Convert the idea into risky assumptions**
An idea is not one bet, it is several stacked bets. Split it into assumptions and label each by type:

- **Value** — the problem is real, frequent, and painful enough that someone will pay to fix it.
- **Viability** — the economics work: the price clears the cost to serve and acquire.
- **Usability** — people can figure out how to get the value without being taught.
- **Feasibility** — you can actually build and operate it with the time and tools you have.

Write each assumption as a falsifiable claim ("freelance graphic designers already pay ≥$30/mo for invoicing tools"). Record them with `assets/validation-plan.md`. Value and viability assumptions are the ones that kill projects; test those first. Feasibility is usually the founder's least risky bet — do not spend validation time proving you can write code.

**Step 2 — Pre-validate on paper and kill weak ideas early**
Before talking to anyone, spend a couple of hours pressure-testing the plan itself. Run the **2/20/200** ladder from `references/prevalidation-framework.md`: a 2-hour desk rubric, a 20-hour market/problem check (who has this pain, where do they gather, is there proof anyone pays today), and only then the 200-hour customer-validation phase. The goal here is to *disqualify fast*. Most ideas should die cheaply, and that is a success, not a failure — it saved you months.

**Step 3 — Design and run Mom Test interviews**
Interviews are for learning about their life, not pitching your idea. Read `references/mom-test-interview-guide.md` before drafting questions. The core moves: ask about what they *did* last time the problem occurred, ask for numbers ("what does that cost you?"), and treat any compliment as noise. Aim for 15–30 conversations inside one narrow segment; stop when answers stop surprising you. The founder runs the interviews — this skill writes the guide, captures verbatim quotes, and finds the patterns.

**Step 4 — Map competitors and the alternatives people use today**
Your real competitor is usually a spreadsheet, a group chat, or "we just live with it." Capture, for each alternative: who it serves, its price, its positioning, and the complaints in its reviews. Build the battle card in `founder/validation/competitors.md` and **timestamp it** — this field ages fast. Mine 1-star reviews of adjacent products; they are free, pre-written problem statements.

**Step 5 — Test willingness to pay, not willingness to click**
Design the cheapest honest commitment test you can: a pre-order, a deposit, a paid pilot, or a landing page that takes a card (not just an email). A waitlist is a weak signal in a world where signups are free. Even a "no" is valuable here. Record what people actually did, with amounts, in the evidence log.

**Step 6 — Score the evidence**
Consolidate every assumption and its status into a JSON file (see the script's `--help` and `assets/evidence-log.csv` for the shape), then run:

```bash
python3 scripts/evidence_scorecard.py founder/validation/evidence.json
```

The script weights value/viability assumptions above usability/feasibility, refuses to return "proceed" while any value/viability assumption is untested, and prints the strongest evidence **against** the idea as well as for it. Do not edit the script's thresholds to make an idea pass — move assumptions to `strong` only when real evidence earns it.

**Step 7 — Write the go/no-go brief (the human decides)**
Use the output format below. Present the case for *and* against, name the single most dangerous unresolved assumption, and recommend the *next cheapest test* rather than a verdict. Then stop and hand the decision to the founder. This is the one call this skill must never make for them — it is their bet, their money, and their time.

**Step 8 — Verify**
Run the quality bar in `references/quality-bar.md`. At minimum: every assumption has a status, no value/viability assumption is `untested` while the brief claims validation, and every "supported" claim cites a specific behaviour (a payment, a number, a repeated action) rather than a sentiment.

## Output format

Write `founder/validation/go-no-go.md` using this structure:

```markdown
# Go / No-Go: <idea one-liner>
_Assessed <date> · Stage: pre-build_

## Recommendation
<Proceed | Keep validating | Pivot the assumption | Kill> — and the single next cheapest test.

## The case FOR
- <assumption> — <evidence: behaviour/amount, not sentiment>

## The case AGAINST
- <assumption> — <evidence>

## Riskiest unresolved assumption
<the one thing most likely to sink this, and how you'd test it in <1 week>

## What we still don't know
- <unknown>

## Evidence appendix
<pointer to evidence.json and interview notes>
```

## Gotchas

- **Waitlist ≠ validation.** Signups are free; treat them as interest until money moves.
- **Compliments are the enemy.** "Sounds interesting" is pity politeness. Discount it to zero.
- **Segment drift.** If your 12 interviews are with 12 different kinds of customer, you have 12 shallow data points, not a validated segment. One narrow ICP at a time.
- **Confirmation bias in scoring.** The founder who built the idea is the worst judge of its evidence. Score the evidence *before* writing the recommendation, and let the script's gates stand.
- **Stale competitor data.** Always timestamp the battle card; pricing and positioning change monthly.

## Available scripts

- **`scripts/evidence_scorecard.py`** — reads an assumptions/evidence JSON file, prints a weighted scorecard, coverage, the strongest counter-evidence, and a verdict band. Run `python3 scripts/evidence_scorecard.py --help` for the input schema.

## Reference files

- **`references/mom-test-interview-guide.md`** — question patterns that survive "even your mom couldn't lie to you", plus anti-patterns. Read before writing any interview script.
- **`references/prevalidation-framework.md`** — the 2/20/200 ladder and a red-flag checklist. Read at Step 2.
- **`references/quality-bar.md`** — what "enough evidence" looks like per assumption type. Read at Step 8 before writing the brief.
- **`assets/validation-plan.md`** — template for the assumption list. Copy to `founder/validation/plan.md`.
- **`assets/evidence-log.csv`** — columns for logging each data point with its source and commitment level.

## Hand-off

When the brief says *proceed* or *keep validating with a build-ready core*, move to the `mvp-scoping` skill and pass it the winning assumption, the target ICP, and the evidence appendix.
