# The Metric Tree

**Contents**
1. North-star candidates
2. Input metrics (the levers)
3. The AARRR funnel
4. Choosing and defining your activation event
5. Cohort retention
6. LTV, CAC, and payback period
7. A worked metric tree

---

## 1. North-star candidates

The north star is the single number that best represents value delivered to customers. Pick **one**; everything else is an input to it.

| Candidate | Best when | Watch out for |
| :-- | :-- | :-- |
| **Revenue / MRR** | Almost always — hardest to fake, compounds with everything | Lagging; pair it with an input you can move this week |
| Weekly active teams hitting the core action | Collaboration products where usage precedes payment | Can rise while revenue is flat (unpaid usage) |
| Messages / files / records created | Marketplace or usage-priced products | Can be gamed by a single power user |
| Time-to-value (how fast a new user reaches the aha) | Early-stage products with a leaky onboarding | A speed metric, not a volume metric — do not confuse the two |

**Default: revenue / MRR.** For a solo founder it is the most honest and the most decision-relevant. YC's blunt version: the best metric is old-fashioned revenue.

## 2. Input metrics (the levers)

The north star tells you *what* happened; inputs tell you *why* and what to do. Keep 2–4. Each input must trace to a concrete action you can take this week. If you cannot name the action, it is not an input, it is trivia.

Good inputs early on:

- **New paying customers** (per week) — action: fix the worst-performing channel.
- **Activation rate** — % of new signups who reach the activation event. Action: shorten onboarding.
- **Voluntary churn / MRR churn** — action: at-risk outreach, onboarding rescue.
- **Involuntary churn** (failed payments) — action: turn on dunning.
- **Expansion MRR** — action: prompt an upgrade at a value milestone.

## 3. The AARRR funnel

A metric tree is just a funnel with ownership. Track where each stage leaks.

- **Acquisition** — how people arrive. Inputs: visits, signups, new customers, CAC by channel.
- **Activation** — the first time they get value. Input: activation rate, time-to-value.
- **Retention** — they come back and keep paying. Inputs: cohort retention, churn (split voluntary/involuntary), core-action recurrence.
- **Referral** — they bring others. Inputs: invite rate, NPS-style referral asks (do not over-invest here before retention is flat).
- **Revenue** — the north star. Inputs: MRR, ARPU, expansion.

The classic solo mistake is over-attending to acquisition while activation and retention leak. Distribution is the 2026 bottleneck, but a leaky bucket wastes whatever you pour in.

## 4. Choosing and defining your activation event

Activation is the single action that correlates with a user staying. It is specific, countable, and reachable in the first session or first few days. Illustrations (use these to *reason by analogy*, not to copy):

- **Slack** treats a team as activated around a volume of messages sent — the value shows up once a team is actually talking.
- **Dropbox** treats a file accessed on a second device as the signal — "your files are everywhere now."
- **Figma** treats the first few files created as the signal — collaboration value appears once there is real work in the file.

How to find yours: list the actions your retained users took in week one that churned users did not, and pick the earliest one that predicts staying. Write it as one sentence ("first report shared with a client") and instrument it exactly. Activation ≠ signup. Signup is attention; activation is value.

Then track **time-to-value** — how long from signup to the activation event. Shrinking that gap is usually cheaper than adding features.

## 5. Cohort retention

Group users by signup week (or month) and plot how many are still active over time. This is the single most diagnostic chart an early business has.

- **A curve that flattens** (approaches a horizontal line above zero) means a real segment sticks — product-market fit forming.
- **A curve that keeps sloping to zero** means product-market fit is absent, no matter how good the top-of-funnel looks.
- **Later cohorts flatter than earlier ones** means onboarding or the product is genuinely improving.

Report retention by cohort, not as a single blended average. A blended number mixes your best and worst cohorts and hides the trend.

## 6. LTV, CAC, and payback period

Use these to sanity-check whether growth is worth funding, but remember: they are estimates and they lie when churn is high or cohorts are young.

- **LTV** ≈ ARPU ÷ churn rate (monthly), or ARPU × average customer lifetime. Treat as a rough multiple, not a precise number.
- **CAC** = total sales+marketing cost ÷ new customers acquired, in the same period.
- **LTV:CAC** — a common rule of thumb is 3:1 or better, but early on a channel that "works" on paper with a two-year payback can still starve you for cash.
- **Payback period** = CAC ÷ monthly gross profit per customer. Shorter is safer for a solo founder with no capital cushion; a payback under a few months keeps you out of a cash hole.

Do not present LTV:CAC with false precision. State the assumptions (churn, ARPU, period) alongside the number.

## 7. A worked metric tree

```
North star: MRR
├── New MRR
│   ├── New customers            ← action: fix the weakest channel
│   └── Activation rate          ← action: shorten signup → activation
└── Retained MRR (the flip side)
    ├── Voluntary churn          ← action: at-risk outreach, onboarding rescue
    └── Involuntary churn        ← action: dunning, retries, billing portal
```

Read the tree top-down when you need the headline, and bottom-up when you need to decide what to do this week. The digest in Step 4 of the skill ranks the adverse movers so the bottom-up read drives the decision.
