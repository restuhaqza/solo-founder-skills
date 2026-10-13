# Growth Review — <product>

_Week of <YYYY-MM-DD> · Binding constraint: <activation | retention | acquisition | referral | revenue>_

## Constraint we attacked

<The funnel step that is capping throughput, with the numbers that make it
binding. Pull from `founder/metrics/` if a funnel already exists; otherwise
compute the transition rates and name the worst leak.>

- acquisition -> activation: <rate>
- activation -> retention (week 4): <rate>
- retention -> revenue: <rate>
- **Binding:** <the step, and the leak that makes it binding>

## Experiments

| id | hypothesis | metric | result | decision |
| :-- | :-- | :-- | :-- | :-- |
| E1 | If we <change>, then <metric> will <direction> by <amount>, because <reason> | <metric> | <result vs target> | SCALE / ITERATE / KILL |
| E2 | | | | |

_One experiment in flight at a time. Full log in `experiment-log.csv`; audit it
with `python3 scripts/experiment_log.py founder/growth/experiment-log.csv`._

## The winner

<The single change we carry forward this period, and the evidence for it: the
metric, the result, and how it beat the target. If nothing met the target,
write "none" and say which experiment iterates instead.>

## Channel check

- Channel we are going deep on: <channel> — started <date>, qualifying outcome defined as <outcome>
- Days elapsed: <n> / 60
- Any channel past 60 days with no outcome: <cut it, or "none">

## Next single experiment

<The next hypothesis against the current constraint, its one metric, its target,
the decision rule, and the date its decision is due.>

- Hypothesis: If we <change>, then <metric> will <direction> by <amount>, because <reason>
- Metric / target: <metric> -> <target>
- Decision due: <YYYY-MM-DD>
