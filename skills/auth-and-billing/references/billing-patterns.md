# Billing & Auth Patterns for a Solo SaaS

**Contents**
1. The two things you never hand-roll
2. Auth: what to delegate, what you keep
3. The entitlement model
4. The subscription state machine
5. Webhooks: the part that actually matters
6. Trials, proration, upgrades, downgrades
7. Failed payments and involuntary churn
8. Tax, merchant-of-record, and what you do not compute
9. Testing billing without charging anyone
10. Security and data boundaries

---

## 1. The two things you never hand-roll

Authentication and payments are the two most expensive things a solo founder can build
from scratch, and the two most likely to leak. Both are solved problems with security,
compliance, and tax tails that a managed provider has already paid to solve. Your job is
not to implement them — it is to **connect** them and to own the one part that is genuinely
yours: the mapping from "who is this user and what have they paid for" to "what features
they can use". If you are writing session-handling code or touching a raw card number, stop
and wire a provider instead.

## 2. Auth: what to delegate, what you keep

Delegate: password storage and hashing, email verification, password reset, OAuth/social
login, session issuance and revocation, and (later) MFA. A managed auth provider does all of
this correctly out of the box.

You keep: the **user record your app reads** (usually a row keyed by the provider's user id),
the **entitlement lookup** for that user, and any **authorisation rules** the provider cannot
know ("this user may edit this workspace"). Keep the provider's user id as the foreign key
and never re-implement identity around a guessed key.

Two rules that prevent most auth bugs: **authorise on the server**, never by hiding a button,
and **scope every query by the tenant id** so one account cannot read another's rows.

## 3. The entitlement model

An entitlement model is a small table with three ideas: **plans** (free, starter, pro),
**features** (the things a plan can include or limit), and the **matrix** connecting them. The
matrix is the single source of truth for gating, and it should live in one file you edit
deliberately — the CSV linted by `scripts/entitlements_check.py` is exactly that file.

Guidelines that keep the matrix honest:

- **Every paid plan must have at least one feature the free plan does not.** If it does not,
  there is no reason to upgrade, and the linter will say so.
- **A paid plan is never worse than free on any feature.** Downgrades are billing bugs users
  find before you do.
- **Limits rise with the plan.** 3 → 25 → unlimited is fine; 25 → 10 is a mistake.
- **Gate the smallest number of things that matter.** A long gate list is hard to explain on
  a pricing page and hard to keep in sync.
- **The matrix is code-adjacent, not decoration.** Read entitlements from it at runtime; do
  not retype the rules inside components, where they drift.

## 4. The subscription state machine

A subscription is not a boolean; it is a small state machine, and modelling it as a boolean is
how apps give away paid features or lock out paying customers. The states that matter:

`trialing → active → past_due → canceled → (expired)`, plus `incomplete` for a checkout that
never finished. Decide, for each state, whether the entitlement is **on** (and for how long).
The common, defensible default: `trialing` and `active` are on; `past_due` stays on during a
short grace window while the provider retries; `canceled` stays on until the paid period ends,
then off. Write those rules down in `billing-spec.md` so gating code reads a state, not a guess.

## 5. Webhooks: the part that actually matters

**The webhook is the source of truth, not the checkout redirect.** A success redirect is a
browser event a user can close, spoof, or never reach; it is a hint, not proof of payment.
The provider's webhook is a server-to-server fact. Never grant entitlement from the redirect
alone — grant it from the webhook, and treat the redirect as pure UX.

Non-negotiables for the webhook handler:

- **Verify the signature** on every request using the provider's secret, and reject anything
  that fails. An unsigned webhook endpoint is an open door that hands out paid features.
- **Be idempotent.** Providers retry, and the same event can arrive more than once. Store the
  event id and ignore a repeat, so a retry does not double-apply an upgrade.
- **Do not trust arrival order.** Events can land out of order; re-read the current
  subscription state from the provider's API when it matters rather than assuming sequence.
- **Acknowledge fast, process safely.** Return 2xx quickly, do the work idempotently, and keep
  a record of what you processed so you can replay after a bug.
- **Keep the handler tiny and central.** One endpoint that updates one entitlements store —
  not logic scattered across pages.

## 6. Trials, proration, upgrades, downgrades

- **Time-box the trial in the provider, not in your database.** A trial with an end date is a
  subscription state; a trial you count yourself will drift.
- **Let the provider prorate.** Upgrades mid-cycle, downgrades at period end, and credit
  handling are fiddly arithmetic you should not reproduce.
- **A downgrade is not a cancellation.** Model it as a plan change the provider applies; do not
  delete anything on downgrade that you would have to rebuild on re-upgrade (use read-only,
  not deletion).
- **Grandfathering a price change is a decision, not a default.** Changing price for existing
  customers is the founder's call and can be a support event; model the grandfather state
  cleanly so you *can* honour the old price, but do not decide it in code.

## 7. Failed payments and involuntary churn

Most "churn" a solo founder sees early is **involuntary**: the card expired, and the customer
never knew. Treat failed payment as a product flow, not an email you forget:

- Rely on the provider's **retry schedule** and enable its **dunning** emails.
- Show **in-app, pre-emptive** prompts before a card expires.
- Keep a **grace period** where the account still works, so a Tuesday expiry does not lose a
  Monday-happy customer.
- Track past-due → recovered as a metric; it is one of the cheapest revenue uplifts available.

Hand the split between voluntary and involuntary churn to `product-metrics` so the weekly
review sees the real leak.

## 8. Tax, merchant-of-record, and what you do not compute

**You do not compute tax.** VAT, sales tax, and their two-thousand-jurisdiction rules are a
professional-domain problem. Use a merchant-of-record (the provider sells on your behalf and
handles tax) or the provider's tax feature, and let it be the authority. Treat any tax or
accounting output here as a **first draft flagged for a professional** — never as settled
advice. This is one of the human-approval boundaries the whole pack respects.

## 9. Testing billing without charging anyone

- Use the provider's **test mode keys** everywhere except production, and never mix test and
  live keys in one environment.
- Use **test clocks / time simulation** to advance a trial, hit a renewal, and trigger a
  failure on purpose — do not wait a month to learn your dunning is broken.
- Write down, in `billing-spec.md`, the small set of scenarios to replay before any billing
  change ships: new subscription, upgrade, downgrade, cancellation, failed payment, recovery.
- Verify the **entitlement matrix** itself with `scripts/entitlements_check.py` before wiring
  it in — a matrix bug is cheaper to catch as a lint than as a refund.

## 10. Security and data boundaries

- **Never store card data.** If card numbers reach your server, you have taken on a compliance
  burden you cannot carry alone; use the provider's hosted checkout or elements.
- **Server-side gating only.** Client-side checks are UX; the API must enforce the same rule.
- **Least privilege on keys.** The app holds as few provider scopes as possible; the webhook
  secret is separate from the API key and lives in the platform secret store.
- **Log entitlement changes**, not just payments: who gained or lost access and why. When a
  customer disputes access, the log is the answer.
