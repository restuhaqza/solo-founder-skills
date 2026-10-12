# Pricing Models, Value Metrics & Policy

**Contents**
1. Model chooser
2. Value metrics — how to pick one
3. Freemium caveats
4. One-time vs subscription for cold-start indie products
5. Merchant-of-record for global tax
6. Annual discounts
7. Grandfathering and migration
8. A short checklist before you commit

---

## 1. Model chooser

Match the model to how the buyer actually buys, not to what is fashionable. The table below is the decision path; read the skill's Step 2 alongside it.

| Model | Charge for | Fits when | Watch out for |
| :-- | :-- | :-- | :-- |
| **Flat subscription** | ongoing access, one price | the value recurs and is roughly similar across customers | punishes you when a few customers cost a lot to serve; no expansion path |
| **Tiered subscription** | access by value-metric allowance | buyers differ meaningfully in how much value they capture | tiers must map to a metric, not to a feature pile |
| **Per-seat** | each user | the value genuinely scales with the number of people, and the buyer controls the count | misapplied to single-user products; buyer resists adding seats |
| **Usage-based** | consumption (events, calls, GB, requests) | cost-to-serve and value both track consumption, and it is predictable | unpredictable bills; needs caps, alerts, and a dashboard |
| **Credits** | prepaid units of work | usage is bursty or one-off, and you want cash up front | credit expiry rules annoy buyers; accounting is fiddlier |
| **One-time** | a single purchase | the product keeps working without you (self-hosted, template, asset, lifetime tool) | no recurring revenue; must pair with a rising acquisition cost plan |

A common hybrid: a base subscription that includes an allowance, then usage overage. It gives predictable MRR plus expansion — but only ship it once the allowance is genuinely predictable to the buyer.

## 2. Value metrics — how to pick one

The value metric is the unit you charge per. A good one has four properties:

- **Aligned** — it grows only when the customer gets more value. If they grow and you don't, you've capped your upside; if you grow and they don't, you've punished success.
- **Predictable** — the buyer can estimate next month's bill before they commit.
- **Legible** — a non-technical buyer understands what one unit *is*.
- **Controllable by the buyer** — they can take an action that reduces or increases it.

Test a candidate metric against three questions:

1. **What does the customer already count?** (projects, clients, invoices, students, listings). The thing they already track in their own head is usually the right metric.
2. **What increases your cost to serve?** (storage, API calls, seats with support). If value and cost both scale with the same unit, that unit is a strong candidate.
3. **What creates the "aha" and the retention?** (records stored, automations run, integrations live). Charging on the retention driver keeps you paid as long as they stay.

If no single metric fits, start with the simplest one and allow one measured expansion axis later — do not launch usage-based billing on a metric you cannot yet report on.

## 3. Freemium caveats

Freemium is a distribution strategy, not a pricing strategy. It only pays off when the free tier is a *self-serve acquisition engine* and the conversion path is short. Before adding one:

- **Who pays for free users?** If support and infrastructure for free users are carried by a small paying base, freemium is a subsidy. Price the free tier's cost into the paid tiers or cap the free tier hard.
- **Is the free tier a complete product or a demo?** A free tier that solves the whole job leaves no reason to pay. A free tier that gets to the "aha" but gates the ongoing use is what converts.
- **Does it confuse the metric?** A free tier on a per-seat product invites whole teams onto one free seat. Make the free allowance explicit.
- **A cheaper alternative:** a time-boxed trial removes the "is this worth it" objection without permanently adding a non-paying segment. Prefer a trial until you have evidence freemium converts.

## 4. One-time vs subscription for cold-start indie products

Subscription is the default *when the value recurs and you must keep operating the product*. It is not always the default when you are cold-starting.

Choose **one-time** when most of these hold:

- the product keeps working without ongoing intervention (a template, a desktop tool, a self-hosted script, an asset);
- the recurring support overhead would be a large share of a small MRR;
- your audience already expects to buy tools once (many indie/creator markets do);
- you would rather sell to a large occasional-buyer market than to a small high-retention one.

Choose **subscription** when the value is a *relationship*: hosted service, ongoing sync, live data, team collaboration, anything that costs you money to keep running and that stops being useful the moment you stop. If you go one-time, plan the acquisition engine explicitly — you have no MRR "floor" to fund growth from, so each sale must pay for its own cost of acquisition and then some.

A middle path many indie products use: one-time for the core, paid upgrades for major versions, and an optional "support/updates" subscription for people who want it.

## 5. Merchant-of-record for global tax

Selling digital goods across borders means VAT/sales-tax registration in many jurisdictions. A **merchant of record** (MoR) — Lemon Squeezy, Polar, Paddle, and similar — acts as the seller of record: it handles tax collection and remittance, invoices, and often chargebacks and fraud, in exchange for a higher fee than a bare processor.

- **Use an MoR** when you sell one-time digital products or global licenses to consumers and do not want to register for VAT in every country yourself. It is a common indie choice for exactly this reason.
- **Use Stripe (or similar)** when you are comfortable owning tax yourself (or have an accountant), want lower fees, and need the flexibility of a full billing platform (dunning, proration, customer portal).
- Either way, this is a **legal/tax decision** — confirm the specifics with an accountant. Fees, supported countries, and tax rules change; check current terms rather than relying on any written-down number.

## 6. Annual discounts

An annual plan does three useful things: it pulls a year of cash forward, it reduces monthly churn (annual customers decide once a year, not twelve times), and it gives you a reason to have a conversation about the value.

- A "two months free" break (roughly a 15–20% discount) is a common indie pattern — pick the number you can defend, not the one you copy.
- Frame it as **"N months free"**, which reads better than a percentage.
- Do not make the monthly plan punitive to force annual; let annual win on the math and on the "I don't want to think about it again" peace of mind.
- Watch the refund and chargeback exposure that comes with a single large charge.

## 7. Grandfathering and migration

You can change the price for new customers freely. Changing it for people already paying you is the sensitive part, and **the founder owns that call** — this document only lays out the options.

| Policy | What it does | When it fits |
| :-- | :-- | :-- |
| **Grandfather forever** | existing customers keep their old price | small base, low churn risk, goodwill matters more than the delta |
| **Grandfather for a window** | old price holds for N months, then migrates | you want the uplift but want to be fair about the transition |
| **Migrate at renewal with notice** | the new price applies when their term renews | standard, transparent, needs clear comms |
| **Grandfather by tier, migrate the rest** | keep legacy tiers alive for existing users only | you want to keep selling the new tiers without a migration project |

Whatever you choose: notify before the change, give a reason tied to value, offer an easy way to stay (annual, or a downgrade), and never apply it silently. A price increase handled badly costs more in trust than it earns in revenue.

## 8. A short checklist before you commit

- [ ] The value metric is named, and each tier is expressed as an allowance of it.
- [ ] The model matches buying behaviour (not hype), and cost-to-serve is understood.
- [ ] The band came from evidence (survey or interviews), not from a competitor's round number.
- [ ] Tiers are 2–3, good-better-best, and the middle tier is clearly the ICP's default.
- [ ] No tier gates something the customer cannot predict.
- [ ] Freemium (if any) has a defined cost owner and a conversion path.
- [ ] Annual discount shape chosen and defensible.
- [ ] Migration/grandfathering policy drafted — and flagged for the founder to decide.
