---
name: experiments-and-growth
description: Run growth as a disciplined series of experiments against the single binding constraint — diagnose which funnel stage is capping throughput, write one falsifiable hypothesis, size the test before running it, log every experiment with a decision, and apply the 60-day channel cut rule. Use this skill whenever a solo founder or indie builder wants to grow faster, pick or double down on a channel, run an A/B or growth experiment, decide whether a test won, fix an activation or retention bottleneck, or stop spreading thin across five channels — even if they only say "growth is flat", "how do I get more users?", "should we scale this?", "let's run an experiment", or "which channel should I focus on?". Outputs land in founder/growth/.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: metrics
---

# Experiments & Growth

Use this skill to grow by running one disciplined experiment at a time against the part of the funnel that is actually holding you back — design the test, size it, log it, and decide scale / iterate / kill on evidence. No experiment is finished until it has a decision. **Outputs land in `founder/growth/`.**

## The one rule

Fix the binding constraint, run one experiment at a time, and measure outcomes, not activity. A channel that produced nothing in 60 days gets cut. Ten honest experiments with decisions beat fifty ideas with none.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Find the binding constraint from the funnel (references/growth-diagnosis.md)
- [ ] Step 2: Write one experiment as a hypothesis with one metric
- [ ] Step 3: Size it (MDE + sample size + duration) and pre-commit a decision rule
- [ ] Step 4: Log it in assets/experiment-log.csv with a status
- [ ] Step 5: Analyse the log (run scripts/experiment_log.py) and act on scale/iterate/kill
- [ ] Step 6: Go deep on one channel; apply the 60-day cut rule
- [ ] Step 7: Review (assets/growth-review.md) and carry only the winner forward
```

**Step 1 — Find the binding constraint from the funnel**
Growth has exactly one binding constraint at a time: the funnel step whose throughput caps everything downstream. Compute the funnel (`acquisition → activation → retention → referral → revenue`) and find the step where the largest fraction leaks — that is usually **activation or retention early**, and **acquisition later** once the product retains. Fix only that step, then re-measure before moving on. Read `references/growth-diagnosis.md` for how to read a funnel against the theory of constraints, and pull the funnel from `product-metrics` if it already has one. The *why*: an experiment against a non-binding step feels productive but cannot move the north star, and running several at once destroys your ability to attribute any of them.

**Step 2 — Write one experiment as a hypothesis**
State the bet in a single falsifiable sentence:

> If we `<change>`, then `<metric>` will `<direction>` by `<amount>`, because `<reason>`.

One metric per experiment — the primary metric you will judge on. If a change is likely to move three numbers, you are testing a bundle and will learn nothing from a mixed result. Reference `references/experiment-design.md` for hypothesis patterns and a list of guardrail metrics to *watch* (without judging on them). The *why*: a hypothesis with one metric and a stated reason is the difference between a test and a change you made and hoped about.

**Step 3 — Size it and pre-commit the decision rule**
Before you run anything, work out the **minimum detectable effect** you care about and the sample size it needs — otherwise you will "win" on noise. For a two-proportion test:

```bash
python3 scripts/experiment_log.py --sample-size \
  --baseline-rate 0.10 --mde 0.20
```

Then pre-commit, in writing: the **decision rule** (what result makes you scale vs discard) and the **duration** (run to full sample, not to the first good-looking day). Pre-committing is the *why*: it is what stops you peeking and stopping early, which inflates false positives. Read `references/experiment-design.md` for the sample-size formula, the peeking problem, and when a test is too small to be worth running.

**Step 4 — Log it**
Add a row to `founder/growth/experiment-log.csv` (copy `assets/experiment-log.csv`) the day you start, not the day you finish. Every experiment carries a `status` (`planned | running | done | abandoned`), and every finished one carries a `result` and a `decision`. The *why*: a log written after the fact is a highlight reel; a log written before it is the record that keeps you honest.

**Step 5 — Analyse the log and act on the calls**

```bash
python3 scripts/experiment_log.py founder/growth/experiment-log.csv
```

It counts experiments by status, checks each finished one against its target *given its direction*, recommends **SCALE / ITERATE / KILL** per experiment, flags hygiene problems (done with no result, running past its end date, missing a decision), and prints the single next action. Act on the calls: a SCALE gets carried forward, an ITERATE gets one more pass with a sharper change, a KILL gets retired without regret.

**Step 6 — Go deep on one channel before adding another**
Channel work is also experiments. Pick the single channel most likely to reach your ICP and go deep — do the unglamorous repetition until you know its real cost per outcome. Apply the **60-day cut rule**: if a channel has produced no qualifying outcome in 60 days, stop it; do not keep it "warming up." Only when one channel reliably produces outcomes do you add a second. The *why*: spreading across channels early gives you five unreadable half-efforts and no compounding advantage.

**Step 7 — Review and carry only the winner forward**
Fill in `founder/growth/growth-review.md` (`assets/growth-review.md`): the constraint you attacked, the experiments run and their decisions, the one winner, and the next single experiment. Then start that next experiment. Keep exactly one experiment in flight. The *why*: a review that lists ten wins is a diary; a review that names one thing to do next is a growth loop.

## Output format

Write `founder/growth/growth-review.md` using this structure (template in `assets/growth-review.md`):

```markdown
# Growth Review — <product>
_Week of <date> · Binding constraint: <activation | retention | acquisition | referral | revenue>_

## Constraint we attacked
<the funnel step and the leak that makes it binding — with the numbers>

## Experiments
| id | hypothesis | metric | result | decision |
| :-- | :-- | :-- | :-- | :-- |
| E1 | If we … | <metric> | <result vs target> | SCALE / ITERATE / KILL |

## The winner
<the one change we carry forward, and the evidence for it>

## Next single experiment
<the next hypothesis, its metric, and when its decision is due>
```

The log itself is `founder/growth/experiment-log.csv`, one row per experiment.

## Gotchas

- **Measuring activity instead of outcome.** "Shipped 12 posts", "ran 5 experiments", "built the funnel dashboard" are activity. The outcome is the metric moving. If a week's work cannot be expressed as a change in one of your numbers, it is not growth work.
- **Peeking and stopping early.** Checking the test daily and stopping the moment it looks significant inflates false positives. Choose the duration and sample size up front and honour them; if you must look, look at guardrails only.
- **Running five experiments at once.** Simultaneous changes make attribution impossible — when the number moves you cannot say which change did it, and when it doesn't you cannot say which to kill. One at a time, unless you have real traffic and a proper test framework.
- **Spreading across channels before one works.** Five channels at 20% effort each is five channels you cannot read. Go deep on one, apply the 60-day cut rule, then expand.
- **Declaring a winner on a tiny sample.** A 3-signup difference is noise, not a winner. If the required sample size is larger than the traffic you have, the honest call is to make a bigger change, not to test a small one.
- **Experiments with no decision recorded.** A test that ran, ended, and was never judged is a cost with no return. The script flags these; close them out.
- **Vanity-metric targets.** Aiming a test at signups, pageviews, or followers when activation and retention are the constraint moves a number that does not compound. Target the metric tied to the constraint.
- **Attribution to the wrong lever.** If a test result contradicts your funnel or retention data, trust the data. One lucky channel spike is not a repeatable outcome.
- **Human boundary.** This skill designs tests, sizes them, and recommends scale/iterate/kill. Shipping the change, changing pricing that affects existing customers, and spending money on a channel remain the founder's call — flag them, do not execute them.

## Available scripts

- **`scripts/experiment_log.py`** — reads the experiment log CSV, prints status counts, per-experiment target checks and a SCALE / ITERATE / KILL recommendation, flags hygiene problems, and ends in the single next action. Add `--sample-size` with `--baseline-rate` and `--mde` to compute the per-variant sample size for a two-proportion test. Supports `--json`. Run `python3 scripts/experiment_log.py --help` for the input schema, the decision thresholds, and the sample-size formula.

## Reference files

- **`references/growth-diagnosis.md`** — theory of constraints applied to a funnel, how to read which stage is binding, retention-first, the go-deep-before-wide channel rule and the 60-day cut rule, and why activity is not outcome. Read at Step 1 and again at Step 6.
- **`references/experiment-design.md`** — the hypothesis format, one metric per test, minimum detectable effect, sample size and duration, the peeking problem, guardrail metrics, and when a test is too small to run. Read at Steps 2–3.
- **`assets/experiment-log.csv`** — the experiment log. Copy to `founder/growth/experiment-log.csv` and add one row per experiment, starting the day you start it.
- **`assets/growth-review.md`** — the weekly/periodic review template that ends in one next experiment.

## Hand-off

When an experiment moves the metric, hand the result to `product-metrics` so the north star and funnel are updated with the new number. When a channel reliably produces qualifying outcomes, hand it to `go-to-market-launch` to turn the one-channel result into a repeatable distribution engine.
