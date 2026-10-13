# Billing Spec — <product>

_One page. The contract for how access is granted. The app reads entitlements; this file explains the rules behind them._

## Plans

| Plan | Price | Billing period | Entitlement state when… |
| :-- | :-- | :-- | :-- |
| Free | $0 | n/a | always on (limited) |
| <Starter> | $<…> | monthly / annual | `trialing`/`active` on; `past_due` grace <…> |
| <Pro> | $<…> | monthly / annual | `trialing`/`active` on; `past_due` grace <…> |

Entitlement matrix: see `founder/product/entitlements.csv` (lint with `scripts/entitlements_check.py`).

## Auth (managed provider)

- Provider: <Supabase Auth / Clerk / Auth0 / …>
- App user key: <provider user id> → row in `<users table>`
- Delegated: passwords, email verification, reset, OAuth, sessions
- Kept in-app: user record, entitlement lookup, authorisation rules (tenant-scoped queries)

## Subscription state → access

| Provider state | Access | Duration |
| :-- | :-- | :-- |
| `trialing` | on | until trial end |
| `active` | on | until period end |
| `past_due` | on (grace) | <…> days while retrying |
| `canceled` | on | until paid period ends, then off |
| `incomplete` | off | checkout never finished |

## Webhook (the source of truth)

- Endpoint: `POST /api/billing/webhook`
- Signature verification: <provider secret>, reject on failure
- Idempotency: store `event.id`, ignore repeats
- On event: re-read subscription from provider API → update `<entitlements store>`
- Events handled: <checkout.session.completed, customer.subscription.updated/deleted, invoice.payment_failed, …>

## Gating

- Single source of truth: `<entitlements table / matrix file>`
- Server-side enforcement on: <routes / API handlers>
- Client-side checks are UX only (never the gate)
- Log every entitlement change: who, when, why

## Trials, changes, dunning

- Trial: <length>, time-boxed in the provider
- Upgrade: prorated by provider · Downgrade: at period end, read-only (no deletion)
- Failed payment: provider retries + dunning emails on; in-app pre-expiry prompt; grace <…> days

## Tax

- Merchant-of-record: <yes — provider / no — provider tax feature>
- Tax and accounting output is a **first draft for a professional**, not settled advice.

## Test scenarios to replay before any billing change

- [ ] New subscription (trial → active)
- [ ] Upgrade mid-cycle (prorated)
- [ ] Downgrade at period end
- [ ] Cancellation (access ends at period end)
- [ ] Failed payment → grace → recovery
- [ ] Failed payment → dunning → involuntary churn
