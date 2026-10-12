# Churn and Activation

**Contents**
1. Why most churn happens before value
2. Voluntary vs involuntary churn
3. Dunning — the highest-ROI solo lever
4. The onboarding-to-aha email sequence
5. At-risk detection
6. Win-back playbooks
7. A churn review you can run in fifteen minutes

---

## 1. Why most churn happens before value

Customers rarely leave because a later feature is missing. They leave because they never reached the moment where the product was obviously worth paying for. That means churn is usually an **activation** problem wearing a retention costume.

Practical consequence: when churn rises, look at first-session behaviour and onboarding before you look at the cancellation survey. The two best questions are *"did they reach the activation event, and how long did it take?"* A cancellation reason of "too expensive" or "not using it enough" almost always traces back to value never landing.

## 2. Voluntary vs involuntary churn

Track these as two separate numbers. A single blended churn figure hides the fact that a large share of churn has nothing to do with the product.

- **Voluntary churn** — the customer deliberately cancelled or downgraded. This is about value: pricing, fit, a missing job, or a competitor.
- **Involuntary churn** — the payment failed and the subscription lapsed without anyone deciding to leave: expired cards, insufficient funds, a bank decline, an SCA/authentication failure. By industry reporting this is commonly in the 20–40% range of total churn, and most founders never split it out.

Why split them: they have completely different fixes. Voluntary churn needs product, onboarding, or pricing work. Involuntary churn needs plumbing — and the plumbing is largely automated. Mixing them means you spend expensive effort on retention experiments when a retry schedule would have recovered the revenue for free.

The `weekly_digest.py` script prints an inferred involuntary-churn line whenever your CSV carries both `churned_mrr` and `failed_payments_mrr`: it reports failed payments as a share of total churned MRR.

## 3. Dunning — the highest-ROI solo lever

Dunning is the process of recovering failed payments. For a solo founder it is the best effort-to-revenue ratio available, because it is mechanical and does not require winning anyone over.

A minimum viable dunning setup:

1. **Smart retries.** Let your billing provider (Stripe, Paddle, Polar) retry the charge on a sensible schedule rather than once. Note that card networks limit how many times you may retry, so let the provider manage the timing.
2. **A short dunning email sequence.** Trigger on the first failure, not the last. Plain language: *the payment didn't go through; here is a one-click link to update the card.* Confirm the update and the successful charge.
3. **A hosted billing portal.** Give customers a self-serve way to update a card or change a plan without emailing you.
4. **A recovery report.** After a month, count recovered MRR vs permanently failed MRR. If recovery is low, your sequence is wrong, not your luck.
5. **Grace period.** A few days of continued access while the card is being fixed converts far more than an instant hard cutoff.

This is not a legal, tax, or pricing decision — it is plumbing you can switch on. But any change that alters what existing customers are charged stays the founder's call.

## 4. The onboarding-to-aha email sequence

Emails exist to move a new signup to the activation event. Keep it short, one action per email, and stop once they activate. A default outline:

- **Day 1 — one specific action.** The single step that gets them closest to the aha ("create your first report"). Link straight into the product, not to a help article.
- **Day 3 — one feature that makes it click.** The feature that retained users adopt first. Show it in context of the action they just took.
- **Day 7 — check-in.** Ask if they got value; offer to help. This is also your best qualitative signal — reply to every response.
- **Day 30 — milestone.** Celebrate a real usage milestone, or prompt the next natural step (an upgrade when they hit a value limit).

Rules that keep it from becoming spam: segment by whether they have activated, suppress anyone who already did, and keep one call to action per email. If a user activates before Day 1's email has sent, they should leave the sequence.

## 5. At-risk detection

The cleanest early-warning signal is **absence of the core action**. Flag any active customer with no core action in 14–21 days — before they cancel, while there is still time to intervene. Combine two inputs:

- **Product usage** — no core action in 14–21 days; a drop in session frequency; a power user who went quiet.
- **Billing** — a failed payment, an approaching renewal, or a lapsed trial that never converted.

You can script this on your billing provider plus a product-analytics tool; you do not need a dedicated tool until you have well past a couple hundred customers. Then fire the matching save playbook: onboarding-rescue for a never-activated user, silent-quitter nudge for a formerly active one, payment-saver for a billing-triggered one.

## 6. Win-back playbooks

- **Silent-quitter nudge.** A short, human email: *"noticed you haven't [core action] in a while — anything blocking you?"* Often resurfaces a real bug or a buried feature.
- **Onboarding rescue.** For users who signed up but never activated: re-run the shortest path to the activation event, offer a 15-minute call for your best-fit accounts.
- **Payment saver.** For failed cards: the dunning sequence in section 3.
- **Post-cancel survey.** One question, "what would have kept you?" — but weight the *behaviour* data (usage, activation) above the stated reason.
- **Reactivation sequence.** A 7-day sequence after a lapse, offering a concrete reason to return (a new feature that solves their original job, not a generic discount).

Win-backs are worth running, but do not let them dominate: recovering a user who never activated is harder than making the next signup activate.

## 7. A churn review you can run in fifteen minutes

1. Pull this week's cancellations and failed payments **separately** (the digest does this if your CSV has the columns).
2. For voluntary churn, check activation status and time-to-value for each account — how many never reached the activation event?
3. For involuntary churn, check whether the dunning sequence fired and how many cards were recovered.
4. Name the **one** dominant cause across the accounts this week.
5. Decide one action for next week. One. The weekly review ends in a decision, not a discussion.
