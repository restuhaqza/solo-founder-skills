# Experiment Design

**Contents**
1. The hypothesis format
2. One metric per test
3. Minimum detectable effect
4. Sample size and duration
5. The peeking problem
6. Guardrail metrics
7. When a test is too small to be worth running

---

## 1. The hypothesis format

A change is not an experiment until it is stated as a falsifiable bet. Use one sentence:

> If we `<change>`, then `<metric>` will `<direction>` by `<amount>`, because `<reason>`.

Each part earns its place:

- **`<change>`** — the specific thing you will do differently, small enough to ship and reverse.
- **`<metric>`** — the one number you will judge on (see §2).
- **`<direction>`** — up or down. Writing it down is what stops you rationalising a miss later.
- **`<amount>`** — the size you would call a win. A vague "better" cannot be met or missed.
- **`<reason>`** — why you believe it. The reason is what you are really testing; if the number moves for another reason, the reason was wrong even if the direction was right.

Examples of the shape:

- *If we move the activation step into the first session, then day-1 activation rate will rise by 10 percentage points, because users currently drop off before seeing the value.*
- *If we add social proof above the signup form, then signup-to-trial conversion will rise by 15% relative, because visitors don't yet trust the product.*

A hypothesis you cannot falsify is not a hypothesis. If no result could make you say "that failed", rewrite it.

## 2. One metric per test

Every experiment has exactly **one primary metric**. It is the only number you judge the test on. Everything else is watched, not judged (§6).

Why one: a change that moves three numbers gives a mixed result, and a mixed result teaches nothing. When the primary metric wins and a secondary loses, you still have a decision — scale the primary win and promote the secondary to a guardrail. When two primaries both move, you have an argument instead of an answer.

Pick the primary from the constraint (see `growth-diagnosis.md`). If the constraint is activation, the primary is activation rate — not revenue, even though revenue is the north star. The north star moves because the constraint moved.

## 3. Minimum detectable effect

The **minimum detectable effect (MDE)** is the smallest change you would actually act on. You set it before the test, and it drives everything else. Two ways to express it:

- **Absolute** — e.g. activation from 10% to 12% is a +2 percentage-point effect.
- **Relative** — the same change is +20% relative.

Relative MDE is the more useful framing for a rate because it scales with the baseline: a +20% relative lift needs a similar sample size whether the baseline is 5% or 50%.

Set the MDE from the decision, not from your hope. Ask: *what is the smallest lift that would change what we do next?* If a +2% relative lift would not change any decision, do not spend sample size detecting it — set the MDE larger and the test gets cheaper. A test powered for an effect too small to act on is a waste; a test that cannot detect the effect you would act on is worse, because it will "fail" and you will kill a good change on noise.

## 4. Sample size and duration

Sample size follows from the MDE, the baseline, and how much certainty you want. For a two-proportion test (a rate in a control and a variant), the standard normal-approximation estimate for equal allocation is:

```text
n = ceil( (z_{1-alpha/2} + z_{power})^2
          * (p1*(1-p1) + p2*(1-p2))
          / (p1 - p2)^2 )
```

where `p1` is the baseline rate, `p2 = p1 * (1 + MDE)` is the rate you want to detect, and the `z` values are inverse normal CDFs (alpha 0.05 → `z_alpha` ≈ 1.96; power 0.80 → `z_power` ≈ 0.84). The script computes this for you:

```bash
python3 scripts/experiment_log.py --sample-size --baseline-rate 0.10 --mde 0.20
```

The output is the **per-variant** sample size; you need that many in each arm. A worked sanity check: to detect a 10% → 12% rate change at 95% confidence and 80% power, the formula gives about 3,840 per variant — the figure most sample-size calculators report for that case.

It is a planning estimate: it uses the normal approximation, ignores continuity correction, and assumes a clean 50/50 split with one primary metric. Round up, and treat it as the floor, not the answer.

**Duration = sample size ÷ your rate of acquiring units.** If you get 40 qualified units a week and the test needs 3,840 per variant, the test needs about 96 weeks per arm — which tells you the honest thing: *this effect is too small to test, change something bigger.* Duration follows from the sample you need; you do not get to choose a short duration and then pretend the test was powered.

## 5. The peeking problem

Peeking is looking at the result repeatedly and stopping the moment it crosses significance. It feels diligent; it breaks the test. Each look is another chance to catch a random fluctuation on the favoured side of the line, so the true false-positive rate climbs far above the 5% you set — tests that "win" on a peek frequently do not replicate.

Rules that keep the test honest:

- Fix the **duration and sample size in advance**, and stop when you reach them — not on the first good day.
- Do not decide based on a partial read. If you must look, look only at **guardrails** (are we breaking something?), not at the primary.
- If you genuinely need to stop early — a guardrail breach, or the test is clearly harmful — stop and record it as a stopped experiment with the reason, not as a win.
- When a result is borderline, the honest call is **ITERATE**, not SCALE. The script's thresholds are built this way: met-with-margin scales, close iterates, a clear miss kills.

## 6. Guardrail metrics

A guardrail is a metric the change must **not** break, watched but not judged on. One primary, one or two guardrails, no more.

Good guardrails for growth experiments:

- **Support load** — did the change generate tickets or confusion?
- **Churn or refunds** — did we win the metric by degrading the experience?
- **Latency or error rate** — did the change cost reliability?
- **Downstream conversion** — did a lift in activation survive to payment, or is it hollow activation?

Guardrails exist because you can hit any single metric by cheating on another. If a guardrail breaches, stop the experiment and record why — a guardrail breach is itself a decision.

## 7. When a test is too small to be worth running

Not every idea deserves an A/B test. A test is **not** worth running when:

- **The required sample exceeds your traffic in a reasonable window.** You will never reach power, so any result is noise. Make a bigger change that would be visible even at low volume, or ship it as a bet and measure the outcome in your product metrics.
- **You cannot randomise.** One-channel marketing, a pricing change for everyone, a new onboarding flow with no control — these are not tests with a clean control. Run them as **one-at-a-time changes** against your time series instead, and be honest that the attribution is weaker.
- **The change is reversible and cheap and clearly right.** If everything points one way, ship it and watch the funnel; do not spend sample size proving the obvious.
- **You have no metric for it.** No primary metric means no test — that is a change, not an experiment.

The alternative when a test is too small is not "run it anyway." It is a **bigger change**: raise the MDE by making the intervention bolder, so the effect is large enough to see. Small tweaks need large samples; bold changes do not.
