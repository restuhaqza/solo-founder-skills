---
name: product-metrics
description: Define and instrument the few product metrics that actually change decisions — a north-star metric (usually revenue / MRR) plus 2–4 input metrics, a metric tree, one activation event, and the full funnel — then run the weekly business review that ends in exactly one recommended action and split churn into voluntary vs involuntary. Use this skill whenever a solo founder or indie builder wants to set up analytics, choose a north-star or activation metric, build a KPI list or dashboard, run a weekly or monthly business review, diagnose flat or falling growth, investigate churn or failed payments, or make sense of a pile of numbers — even if they only say "what should I track?", "how do I know if I'm growing?", "my churn is bad", or "help me review this month's numbers". Outputs land in founder/metrics/.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: metrics
---

# Product Metrics

Use this skill to run a business on a handful of trustworthy numbers instead of a wall of dashboards. It picks a north star and its inputs, writes the instrumentation plan, produces the weekly digest, and turns churn and activation into specific fixes. Outputs land in `founder/metrics/`.

## The one rule

Track a few numbers that change decisions; revenue is the best single one. If a metric has never caused you to do something different, it is decoration. Five numbers you act on beat forty you only glance at.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Choose the north star (default: revenue / MRR) and 2–4 input metrics
- [ ] Step 2: Define the funnel and the single activation event
- [ ] Step 3: Write the instrumentation plan (events, properties, tool)
- [ ] Step 4: Run the weekly review (fill metrics.csv, run scripts/weekly_digest.py)
- [ ] Step 5: Split churn into voluntary vs involuntary
- [ ] Step 6: Read the retention cohort curve before any vanity metric
- [ ] Step 7: Diagnose the one binding constraint and fix only that
```

**Step 1 — Choose the north star and 2–4 input metrics**
A north star is the single number that best represents delivered value. For almost every early solo business it is **revenue (MRR)**, because it is the hardest to fake and it compounds every other truth. Then pick 2–4 *input* metrics you can actually move — they are the levers under the north star. Build the metric tree in `references/metric-tree.md`: north star at the top, inputs below, each input traceable to a real action. If you cannot name the action a metric would trigger, cut it.

**Step 2 — Define the funnel and the single activation event**
Write the funnel as **acquisition → activation → retention → referral → revenue** and, crucially, pick the *one* event that proves a user reached value — not a signup. An activation event is specific and countable: Slack looked at 2,000 messages sent by a team; Dropbox at a file accessed on a second device; Figma at the first three files. Your version is one sentence ("first report shared with a client"). Activation ≠ signup; the whole funnel is judged by how many people reach this event. Examples are in `references/metric-tree.md`.

**Step 3 — Write the instrumentation plan**
Turn the metric tree into events you will actually log. For each event record: name, trigger, properties, and where it lives. Use `assets/metrics-spec.md` as the template. One tool is enough — connect your billing provider (Stripe/Paddle/Polar) and one product-analytics tool; do not drown in five tools before you have fifty users. The spec is the contract with your future self: when a number looks wrong, this tells you what it is measuring.

**Step 4 — Run the weekly review**
Every week, append one row to `founder/metrics/metrics.csv` (one row per week, first column `date`), then run the digest:

```bash
python3 scripts/weekly_digest.py founder/metrics/metrics.csv
```

The digest computes period-over-period deltas, flags metrics that moved beyond your threshold, ranks the movers by how *adverse* they were, and ends in **exactly one recommended action** — never a chart dump. Fill in `assets/weekly-review.md` for the narrative around it and keep one decision per week. The output is not a dashboard; it is a decision.

**Step 5 — Split churn into voluntary vs involuntary**
Blended churn hides the cheapest win. Separate customers who *chose* to leave from cards that simply failed — involuntary churn is often 20–40% of the total by industry reporting, and it is fixed with dunning (smart retries, a short failed-payment email sequence, a hosted billing portal), which is mostly mechanical. The digest prints an inferred involuntary-churn line whenever your CSV has `churned_mrr` and `failed_payments_mrr`. Read `references/churn-and-activation.md` before you touch retention.

**Step 6 — Read the retention cohort curve first**
Before celebrating signups or pageviews, look at retention by cohort: do later cohorts flatten higher, or does the curve keep sliding to zero? A flat curve means product-market fit is forming; a sloped one means you are filling a leaky bucket. Cohort retention, LTV/CAC, and payback period are defined in `references/metric-tree.md`.

**Step 7 — Diagnose the binding constraint**
Growth has one binding constraint at a time. Use the theory of constraints: find the single step that is capping throughput (usually activation or retention early on, acquisition later), fix only that, and re-measure before moving on. If the digest's worst mover and your retention curve disagree, trust the curve — it looks further back. Do not fix three things at once; you will not know which worked.

## Output format

Write the instrumentation plan to `founder/metrics/metrics-spec.md`. Use `assets/metrics-spec.md` as the starting point:

```markdown
# Metrics Spec — <product>
_North star: <metric> · Review cadence: weekly · Tool: <billing + analytics>_

## Metric tree
North star: <revenue / MRR>
Inputs: <input 1> · <input 2> · <input 3>

## Activation event
<one sentence: the countable action that proves a user reached value>

## Events
| Event | Trigger | Properties | Tool |
| :-- | :-- | :-- | :-- |
| <event_name> | <when it fires> | <key props> | <tool> |

## Weekly review
One row per week in `metrics.csv`; digest via `scripts/weekly_digest.py`.
```

Weekly narrative goes in `founder/metrics/weekly-review.md` (template in `assets/weekly-review.md`), always ending in one decision.

## Gotchas

- **Vanity metrics feel like progress.** Signups, pageviews, and social followers go up when nothing gets better. If a number cannot fall, it cannot tell you anything.
- **Tracking 42 metrics and learning nothing.** More dashboards is not more insight. The failure mode is describing five tools' outputs and still not knowing what moves the product. Cut to the few numbers that change decisions.
- **Blended churn hides failed cards.** A single churn number buries the involuntary share — often 20–40% by industry reporting — which is the highest-ROI lever and mostly automation. Split it out.
- **Activation ≠ signup.** A signup is attention; activation is value delivered. Optimising signups while activation is low just fills a leaky bucket faster.
- **Most churn happens before value.** Users rarely leave because a later feature is missing; they leave because they never reached the aha moment. Look at the first session, not the cancellation survey, first.
- **A digest that ends in a dashboard is not a review.** If the output is charts and no decision, it wasted the meeting. This skill's script is built to end in exactly one action; keep it that way.
- **Human-approval boundary.** This skill drafts the spec, the digest, and the recommended action. Changing pricing or plans that affect existing customers, and moving money, remain the founder's call — flag them, do not execute them.

## Available scripts

- **`scripts/weekly_digest.py`** — reads a metrics CSV (`date` + numeric metric columns), computes period-over-period deltas, flags anomalies beyond a threshold, ranks adverse movers, prints an inferred involuntary-churn line when the columns exist, and ends in exactly one recommended action. Supports `--period wow|mom`, `--threshold`, `--higher-is-better`/`--lower-is-better`, and `--json`. Run `python3 scripts/weekly_digest.py --help` for the input schema and polarity convention.

## Reference files

- **`references/metric-tree.md`** — north-star candidates, input metrics, the AARRR funnel, activation-event examples, cohort retention, LTV/CAC, and payback period. Read at Steps 1–2 and 6.
- **`references/churn-and-activation.md`** — voluntary vs involuntary churn, dunning playbook, onboarding-to-aha email sequence, at-risk detection, and win-backs. Read at Steps 5–6.
- **`assets/metrics-spec.md`** — copy to `founder/metrics/metrics-spec.md` and fill in.
- **`assets/metrics.csv`** — sample weekly data showing the CSV shape (including a `:down` header suffix).
- **`assets/weekly-review.md`** — one-page review template that ends in a single decision.

## Hand-off

When the metrics spec and the weekly cadence are in place, hand the routine to `founder-operating-rhythm` so the digest runs on a fixed weekly slot alongside support, finance, and build time.
