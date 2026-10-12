# Metrics Spec — <product>

_Copy to `founder/metrics/metrics-spec.md`. North star: <metric> · Review: weekly · Owner: <you>_
_Tool: <billing provider + product analytics> · Last updated: <date>_

## The rule

Track a few numbers that change decisions; revenue is the best single one. If a metric has never caused you to do something different, cut it.

## Metric tree

- **North star:** <revenue / MRR>
- **Input 1:** <metric> — <action it triggers this week>
- **Input 2:** <metric> — <action>
- **Input 3:** <metric> — <action>
- **Input 4 (optional):** <metric> — <action>

## Activation event

<One sentence: the countable action that proves a user reached value. It is not a signup.>

- **Time-to-value target:** <e.g. within the first session / first 3 days>
- **How we measure it:** <event name + where it is stored>

## Funnel

| Stage | What we track | Where it comes from |
| :-- | :-- | :-- |
| Acquisition | <new customers / signups / visits> | <tool> |
| Activation | <activation rate> | <tool> |
| Retention | <cohort retention / churn> | <tool> |
| Referral | <invites / referrals> | <tool> |
| Revenue | <MRR> | <billing provider> |

## Events

| Event | Trigger | Key properties | Tool |
| :-- | :-- | :-- | :-- |
| `<event_name>` | <when it fires> | <user_id, plan, ...> | <tool> |
| `<activation_event>` | <when a user first reaches value> | <user_id, ...> | <tool> |
| `<core_action>` | <the recurring value action> | <user_id, ...> | <tool> |
| `<payment_failed>` | <billing provider webhook> | <invoice_id, amount> | <billing provider> |

> Convention: keep event names lowercase_snake_case. An event that never fires on a real user is a bug in the spec, not a zero.

## Churn split

- **Voluntary churn:** <how it shows up — cancellation, downgrade>
- **Involuntary churn:** <how it shows up — failed payment / `failed_payments_mrr`>
- **Dunning status:** <on / off — retries, email sequence, billing portal>

Add `churned_mrr` and `failed_payments_mrr` as columns in `metrics.csv` so the digest can infer the involuntary share.

## Weekly review

One row per week in `metrics.csv`; run the digest:

```bash
python3 scripts/weekly_digest.py founder/metrics/metrics.csv
```

Then write the narrative in `weekly-review.md` and end it with exactly one decision.
