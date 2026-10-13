# Growth Diagnosis

**Contents**
1. The theory of constraints, applied to a funnel
2. Reading which stage is binding
3. Retention first
4. The go-deep-before-wide channel rule
5. The 60-day cut rule
6. Why activity is not outcome

---

## 1. The theory of constraints, applied to a funnel

A funnel is a chain of steps, and a chain carries only as much as its weakest link. A business has exactly **one binding constraint at a time**: the step whose throughput caps the whole system. Improving any other step while the constraint is unchanged produces no increase in the outcome — the extra throughput just piles up at the bottleneck or leaks out of it.

For a product business, the chain is the funnel:

```text
acquisition -> activation -> retention -> referral -> revenue
```

The binding constraint is the step where the largest share of value is lost relative to the next step — the leak that dominates. Diagnosing it means computing each transition rate and comparing leaks, not staring at the top-line number.

Two consequences that decide how you work:

- **Fix one thing.** Changing two steps at once means you cannot attribute the result to either. When the number moves you do not know why, which is worse than not moving it.
- **Re-diagnose after every fix.** Fixing the constraint moves it. The next experiment targets whatever is now the weakest link — often the same step, sometimes a new one.

## 2. Reading which stage is binding

Compute the funnel as counts, then as ratios between consecutive steps, and look for the smallest ratio (or the largest absolute drop in units — sometimes a 90% step is fine because it starts with 10,000 people and a 60% step on 200 people kills you).

| Stage | Transition to measure | What a low number means |
| :-- | :-- | :-- |
| Acquisition | target-ICP visitors -> signups | The wrong people arrive, or the promise is unclear |
| Activation | signups -> first value event | Onboarding is too long, or the value is unclear (see `product-metrics`) |
| Retention | actives in week 1 -> actives in week 4 | The product does not deliver recurring value; growth leaks as fast as it arrives |
| Referral | actives -> invites or word-of-mouth | Not usually binding early; do not chase it before retention |
| Revenue | activated -> paying | Pricing or willingness-to-pay, not a growth problem |

**Early on, the constraint is almost always activation or retention.** Acquisition is cheap to spike (a launch, a post) and useless if the product leaks. Chasing acquisition while retention slopes to zero is filling a leaky bucket faster.

**Later, once the funnel holds, the constraint moves to acquisition.** When cohorts flatten and activated users stay, the number of new people you can reach becomes the cap. That is when channel work — Step 6 of the skill — becomes the experiment.

Do not guess: pull the actual funnel. If `product-metrics` has already produced one in `founder/metrics/`, use it rather than recomputing. If there is no funnel, build a rough one from your analytics before designing any experiment — an experiment against the wrong constraint wastes the whole cycle.

## 3. Retention first

Retention is the ceiling on everything else. A product that loses users quickly makes every acquisition dollar a recurring cost with no compounding; a product that retains turns each acquired user into a stream. So the ordering rule is simple:

1. If retention is low or sloping to zero, fix retention before spending on acquisition. The fix is usually earlier than you think — most churn happens **before value**, in the first session, not at the cancellation screen.
2. If retention is flat or improving, activation is usually the next lever (more users reaching the value event compounds into retention).
3. Only when cohorts flatten and activated users stay do you invest in acquisition as the constraint.

This is why the skill hands the *metric* to `product-metrics` — retention and activation are its territory, and its definitions (the one activation event, cohort curves) are the input to your diagnosis. Your job is not to redefine them; it is to run experiments against whichever one the data says is binding.

## 4. The go-deep-before-wide channel rule

Channels are not additive at low effort. Five channels at 20% effort each give you five channels you cannot read, five sets of etiquette to learn, and no compounding advantage in any of them. One channel at 100% effort gives you a readable signal, a real cost-per-outcome, and a skill that compounds.

The rule:

- Pick **one** channel most likely to reach your narrow ICP.
- Go deep: do the unglamorous repetition until you know the true cost per qualifying outcome (not per click, not per follower).
- Judge it on outcomes, not on how busy it kept you.
- Only when one channel reliably produces qualifying outcomes do you add a second.

Going wide early feels like more shots on goal. In practice it produces five half-signals, and you cannot tell a channel that failed from one you never really ran.

## 5. The 60-day cut rule

A channel gets **60 days** to produce a qualifying outcome. If it has not, cut it. The rationale is that 60 days is long enough to have learned the channel's basics and run real effort, and short enough that you do not sink a quarter into something that is not working.

How to apply it:

- Define the "qualifying outcome" for the channel **before** you start (a paying customer, an activated signup, a qualified reply) — otherwise "no outcome" is arguable forever.
- Track the start date. When 60 days pass with no qualifying outcome, stop the channel and write down why.
- A cut is not a failure; it is the information that buys the next channel its depth. Retiring a dead channel frees the focus the winning channel needs.
- Do not "keep it warm." A channel kept half-alive because it felt promising is not producing and is still costing you attention.

When a channel *does* work, the failure mode flips: founders stop the thing that is working to chase novelty. Double down on the 1–2 winners before exploring a third.

## 6. Why activity is not outcome

Activity is what you did; outcome is what changed. The two diverge constantly, and the divergence is the most common way a growth loop quietly dies.

- "Shipped 12 posts this week", "ran 5 experiments", "set up the funnel dashboard" — all activity. None of them is a number moving.
- The outcome is the metric the constraint implicates: activation rate up, week-4 retention up, qualified signups up.
- If a week of growth work cannot be expressed as a change in one of your numbers, it was not growth work — it was motion.

The test is blunt: **if the activity stopped, would any outcome change?** If not, it is not the experiment. This is also why every experiment needs one primary metric and a recorded decision — so that "we ran experiments" cannot substitute for "a number moved and we acted on it."
