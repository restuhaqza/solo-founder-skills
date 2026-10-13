# Onboarding to the Aha Moment

**Contents**
1. What an activation event is
2. Why activation ≠ signup
3. The Day 0/1/3/7/30 sequence shape
4. At-risk detection (no core action in 14–21 days)
5. The four save playbooks
6. Win-back timing
7. A first-session review you can run in ten minutes

---

## 1. What an activation event is

An **activation event** is the single countable action that proves a user reached value — the moment the product starts paying them back. It is not a signup, not a login, not a page view. It is specific, measurable, and it correlates with people staying.

Well-known examples (illustrative, not targets for your product): Slack looked at a team sending a meaningful volume of messages; Dropbox looked at a file accessed on a second device; Figma looked at the first few files created. The pattern is the same every time: **one action, observable in your data, that separates users who stay from users who leave.**

How to pick yours:

- **Name the outcome, not the feature.** "Shared a report with a client", not "opened the report editor".
- **Make it countable.** You must be able to query it: did this account do X, when, how many times.
- **Make it early.** If it only happens weeks in, it is a retention milestone, not an activation event — keep looking for a smaller, earlier proof of value.
- **One event only.** Two competing definitions make both meaningless. If `product-metrics` already defined it, reuse that one; do not invent a second.

Then measure **time-to-value**: the median time from signup to the activation event. That number is the honest score of your onboarding. It falls, or onboarding is broken.

## 2. Why activation ≠ signup

A signup is attention; activation is value delivered. Confusing the two is the most expensive onboarding mistake a solo founder makes, because it points all effort at the wrong number.

- **Signups go up when marketing works and the product doesn't.** Optimising acquisition while activation is low just fills a leaky bucket faster — you pay to acquire people who leave before value, and churn eats the growth.
- **Most churn happens before value.** Customers rarely cancel because a *later* feature is missing. They cancel because they never reached the moment the product was obviously worth paying for. That makes churn, most of the time, an **activation problem wearing a retention costume**.
- **A cancellation reason lies, gently.** "Too expensive" and "not using it enough" almost always trace back to value never landing in the first session. Trust the behaviour (did they activate? how long did it take?) over the stated reason.

Practical consequence: when churn rises, look at **first-session behaviour and onboarding before you read the cancellation survey.** The two questions worth asking are "did they reach the activation event?" and "how long did it take?".

## 3. The Day 0/1/3/7/30 sequence shape

The onboarding email sequence exists to move a new signup to the activation event. Keep it short, **one action per email**, and stop the moment they activate. The default shape:

- **Day 0 — Welcome & first step.** Get them into the product for a real first session. The action is the smallest possible step, not a tour.
- **Day 1 — The one action that reaches the aha.** Drive the exact activation event, with one link straight into the product. This is the load-bearing email; if you keep only one, keep this.
- **Day 3 — The feature that makes it click.** Spotlight the feature retained users adopt first, shown in the context of the action they just took.
- **Day 7 — Check-in.** Ask whether they got value and offer to help. This is also your best qualitative signal — reply to every response.
- **Day 30 — Milestone & next step.** Celebrate a real usage milestone, or prompt the natural next step (a second workflow, an upgrade when they hit a value limit).

Rules that keep it from becoming spam:

- **One call to action per email.** Multiple CTAs fragment attention and reduce the click-through on the one that matters.
- **Segment by activation status and suppress anyone who already activated.** A nudge sent to someone who already got value reads as broken automation.
- **Track which email moves the activation rate**, not just open rates. If Day 1 does not lift activation, the copy or the target action is wrong.
- **Short beats clever.** Three focused emails that reach the aha beat seven that get filtered.

Generate the scaffold with `scripts/onboarding_sequence.py` (see the SKILL.md), then edit the copy into your own voice.

## 4. At-risk detection (no core action in 14–21 days)

The cleanest early-warning signal for churn is **absence of the core action**. Flag any active customer with **no core action in 14–21 days** — while there is still time to intervene, *before* they cancel. By the time a cancellation arrives, the decision is often already made; the quiet stretch before it is the window.

Combine two inputs:

- **Product usage** — no core action in 14–21 days; a fall in session frequency; a former power user gone quiet; activation attempted but never completed.
- **Billing** — a failed payment; an approaching renewal; a trial that lapsed without converting.

You can script this on your billing provider (Stripe, Paddle, Polar) plus one product-analytics tool; a dedicated churn tool is not needed until well past a couple hundred customers. Keep the thresholds tuned to your product — a daily-use tool needs a shorter window than a monthly-report tool, because "14 days" is relative to the natural rhythm of the core action.

Then match the signal to a playbook (next section). Do not save everyone with the same email: a never-activated user and a formerly active user need different messages, and a failed card needs plumbing, not encouragement.

## 5. The four save playbooks

**Onboarding-rescue — signed up, never activated.**
Re-run the shortest path to the activation event. One clear action, one link, and an offer of a short call for your best-fit accounts ("do things that don't scale" is exactly right here). This is the highest-priority playbook, because the cause is usually your onboarding, not the customer.

**Silent-quitter — was active, went quiet.**
A short, human email: *"noticed you haven't [core action] in a while — anything blocking you?"* This often surfaces a real bug or a buried feature, and it doubles as product research. Keep it one question, no pitch.

**Payment-saver — a failed card.**
This is the dunning sequence, and it is plumbing, not persuasion: smart retries on your provider's schedule, a short email sequence that fires on the first failure (plain language + a one-click link to update the card), a hosted billing portal, and a short grace period. Involuntary churn is a large share of total churn by industry reporting, and it is mechanical to recover. See `product-metrics` for the full dunning setup.

**7-day reactivation — after a lapse.**
A short sequence after the cancellation or lapsed trial, offering a **concrete reason to return** — a new capability that solves their original job, or a fix for what they reported — not a generic discount. Discounts train people to wait; a real fix earns the return.

## 6. Win-back timing

Win-backs are worth running, but sequence them so you do not burn goodwill or your own time:

- **Days 0–7 after a lapse:** let the payment-saver and the reactivation sequence run. Offer the fix, not a discount.
- **Around 30 days:** one more touch *only if* there is a genuinely new reason — the feature they asked for shipped, or a fix landed. If nothing changed, silence is better than a pretend-news email.
- **Beyond ~90 days:** treat them as a new signup, not a win-back. Their context and needs have moved on; a stale "we miss you" reads as desperate.

Two cautions. First, **recovering a never-activated user is harder than making the next signup activate** — put energy into the front of the funnel. Second, **weight behaviour over stated reasons**: usage and activation data tell you why someone left more honestly than a one-question survey, which is useful but secondary.

## 7. A first-session review you can run in ten minutes

Once a week, review onboarding itself, not the whole business:

1. **Activation rate this week** — of new signups, how many reached the activation event?
2. **Time-to-value** — median days from signup to activation. Up or down?
3. **Where people stall** — the single step where most drop off. That is next week's onboarding fix.
4. **At-risk list** — who has had no core action in 14–21 days? Fire the right playbook.
5. **One change** — name the single onboarding change to make, and make only that.

Onboarding improves when it is measured as a funnel with one stall point at a time, not when it is "polished" by feel.
