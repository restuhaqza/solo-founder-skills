---
name: auth-and-billing
description: Wire managed authentication and subscription billing into a SaaS skeleton — pick the auth provider, model plans and features as one entitlement matrix, handle trial/active/past_due/canceled states, verify and make webhooks idempotent (the real source of truth, not the checkout redirect), set up trials, proration, downgrades and dunning for failed payments, and gate features server-side. Use this skill whenever a solo founder or indie builder is adding signup, login, sessions, subscriptions, a paywall, a free tier, plan gating, checkout, a customer portal, failed-payment handling, or asks "how do I know when someone paid?", "should I build my own auth?", "how do I gate features by plan?", or "why are people churning after signing up?" — even if they only say "add payments", "add login", or "I want a paid plan".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: product
---

# Auth & Billing

Use this skill to connect the two providers almost every SaaS needs — auth and payments — and to own the one part that is genuinely yours: the entitlement matrix that says who has paid for what. It produces a plan-vs-feature matrix, a linted entitlements file, and a one-page billing spec. Outputs land in `founder/product/`. **You connect; the providers implement.** If you are writing session or card-handling code, you have taken the wrong path.

## The one rule

**Buy auth, buy payments, own only the entitlement mapping.** Authentication and payments
are solved problems with security and tax tails you cannot carry alone; hand-rolling either
is the most expensive mistake available to a solo founder. Your differentiation is the
product, not the login form. So: delegate identity and money to a managed provider, and put
your effort into the small, verifiable matrix that maps plans to features — then gate on the
server, from that one matrix.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Read context + pricing; list the plans and gated features
- [ ] Step 2: Write entitlements.csv and lint it (scripts/entitlements_check.py)
- [ ] Step 3: Wire a managed auth provider (never custom sessions)
- [ ] Step 4: Model the subscription state machine and its access rules
- [ ] Step 5: Wire checkout + customer portal for plan changes
- [ ] Step 6: Implement the webhook: verify signature, be idempotent, update entitlements
- [ ] Step 7: Gate features server-side from the one matrix; log changes
- [ ] Step 8: Set up trials, proration, downgrades, and dunning
- [ ] Step 9: Verify against the test scenarios; write billing-spec.md
```

**Step 1 — List plans and gated features**
Read `founder/context.md` and `founder/pricing/pricing.md` (from `pricing-strategy`). The tiers were decided there; do not invent new ones here. Write down the plans and the handful of features that differ between them — the smallest set that gives each paid plan a reason to exist. If pricing is undecided, run `pricing-strategy` first: you cannot wire a paywall for tiers that do not exist.

**Step 2 — Write and lint the entitlement matrix**
Put the plans and features in `founder/product/entitlements.csv` (shape: first column `feature`, then one column per plan; values `yes`/`no`, an integer limit, or `unlimited`). Then lint it:

```bash
python3 scripts/entitlements_check.py founder/product/entitlements.csv
```

It flags duplicate features, paid plans worse than free, limits that fall as the plan rises, unrecognised values, mixed value styles, and any plan with no feature the free tier lacks. Fix errors before wiring anything — a matrix bug is cheaper to catch as a lint than as a refund. See `references/billing-patterns.md` §3 for the model.

**Step 3 — Wire a managed auth provider**
Delegate passwords, email verification, password reset, OAuth, sessions, and (later) MFA. Keep only the user record your app reads, keyed by the provider's user id. Authorise on the server, and scope every query by the tenant id so one account cannot read another's rows. Detail in `references/billing-patterns.md` §2.

**Step 4 — Model the subscription state machine**
A subscription is `trialing → active → past_due → canceled`, not a boolean. Decide, per state, whether access is on and for how long — the defensible default is on while trialing/active, on during a short past_due grace window, and on through the paid period after cancellation, then off. Write those rules down now; gating code reads a state, never a guess. See §4.

**Step 5 — Wire checkout and the customer portal**
Let the provider host checkout and the billing portal so plan changes, cards, and invoices are
handled without you touching card data. Upgrades prorate in the provider; downgrades apply at period end and should render content read-only rather than delete it. Never store card data. See §6.

**Step 6 — Implement the webhook as the source of truth**
Grant access from the provider's webhook, never from the checkout redirect. Verify the
signature on every request and reject failures; store the event id and ignore repeats so a
retry does not double-apply; do not assume arrival order — re-read the subscription from the
provider when it matters. Keep the handler small and central: one endpoint that updates one
entitlements store. See §5.

**Step 7 — Gate server-side from the one matrix**
Read entitlements from the single matrix at runtime — do not retype rules inside components.
The API enforces the same rule the UI hints at; hiding a button is UX, not security. Log every
entitlement change (who, when, why) so a disputed access question has an answer. See §3 and §10.

**Step 8 — Trials, proration, and dunning**
Time-box the trial in the provider, not in your database. Enable the provider's retry schedule
and dunning emails, add an in-app pre-expiry prompt, and keep a grace period so an expired card
does not silently lose a paying customer — most early "churn" is involuntary. Hand the
voluntary-vs-involuntary split to `product-metrics`. See §6–7.

**Step 9 — Verify against the scenarios, then write the spec**
Replay the fixed scenario list before any billing change ships: new subscription, upgrade,
downgrade, cancellation, failed payment, recovery. Use test keys everywhere but production, and
test clocks to advance time rather than waiting a month. Then fill `assets/billing-spec.md` and
save it to `founder/product/billing-spec.md`.

## Output format

Write two files. `founder/product/entitlements.csv` is the machine-readable matrix the app reads and the linter checks. `founder/product/billing-spec.md` (from `assets/billing-spec.md`) is the human-readable contract: plans, auth provider and what it delegates, the state→access table, the webhook contract, where gating happens, trial/proration/dunning rules, the tax stance, and the test-scenario checklist. Keep it to one page.

## Gotchas

- **The checkout redirect is not proof of payment.** Users close the tab, navigate away, or
  spoof the URL. Grant entitlement from the webhook, and treat the redirect as pure UX.
- **Webhooks arrive more than once and out of order.** Without an idempotency key you will
  double-apply upgrades; without re-reading state you will apply events in the wrong order.
- **Test and live keys must never mix.** One environment, one mode. A live key in a preview
  deploy charges real customers from a test click.
- **Do not compute tax yourself.** Use a merchant-of-record or the provider's tax feature; treat
  any tax or accounting output here as a first draft for a professional, never as settled advice.
- **Never store card data.** If card numbers reach your server you have taken on a compliance
  burden a solo founder cannot carry. Use hosted checkout or the provider's elements.
- **Changing price or plans for existing customers is the founder's call, and it is not silent.**
  This skill models grandfathering and drafts the notice; it never sends the message and never
  decides the change. That boundary is hard.
- **A downgrade is not a deletion.** Keep data, render it read-only, so re-upgrading restores
  access instead of a support ticket.
- **Past-due is not churned.** Most early churn is an expired card; dunning and a grace window
  recover it far more cheaply than acquisition replaces it.

## Available scripts

- **`scripts/entitlements_check.py`** — lints the plan-vs-feature CSV for duplicate features, paid plans worse than free, limits that fall between tiers, unrecognised or mixed values, and plans with no upgrade advantage; prints the normalised matrix and a gate count per plan. `--json` emits structured output; `--strict` treats warnings as failures. Run: `python3 scripts/entitlements_check.py founder/product/entitlements.csv`

## Reference files

- **`references/billing-patterns.md`** — auth delegation, the entitlement model, the subscription state machine, webhooks (signature, idempotency, ordering, replay), trials/proration/downgrades, failed-payment dunning, the tax boundary, testing billing safely, and security boundaries. Read during Steps 2–9.
- **`assets/entitlements.csv`** — the plan-vs-feature matrix template with sample rows; the script reads this shape. Copy to `founder/product/entitlements.csv`.
- **`assets/billing-spec.md`** — the fill-in billing spec template. Copy to `founder/product/billing-spec.md`.

## Hand-off

Money and access are wired — now instrument them. Hand `product-metrics` the subscription states and the voluntary/involuntary churn split so the weekly review sees the real leak, and hand `launch-readiness` the billing-spec so the go-live pass can check the webhook and secrets. If pricing needs revisiting, `pricing-strategy` owns the tiers and this skill re-wires the matrix.
