---
name: pricing-strategy
description: Design value-based pricing and packaging for a product — choose the value metric, choose a model (subscription, one-time, credits, or usage), shape 2–3 good-better-best tiers, run willingness-to-pay research with the Van Westendorp method, stress-test the band, and write the pricing page with an objection-handling FAQ. Use this skill whenever a solo founder or indie builder needs to price a product, repackage tiers, decide between subscription and one-time/credits/usage billing, raise or lower a price, design a free plan, or explain why conversions are weak — even if they only say "how much should I charge?", "is my price too low?", "should this be a subscription?", "should I add a free tier?", or "help me write my pricing page". Outputs land in founder/pricing/.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: pricing
---

# Pricing Strategy

Use this skill to design value-based pricing and packaging for a product: the metric you charge on, the model that fits how people buy, the tiers, the evidence for the band, and the page that sells it. It produces a pricing brief, a survey you can send, and a pricing-page draft. **Prices that affect existing customers are the founder's call; this skill prepares the analysis and drafts the change.**

Outputs land in a working folder so later skills can pick them up. Default: `founder/pricing/`. If `founder/context.md` is missing, create it first (product one-liner, ICP, stage, north-star metric, stack) — it is the shared brief every skill reads.

## The one rule

Price on the value created, not on your costs. Cost-plus pricing ("my server bill is $3, so $9 feels safe") anchors your floor to your expenses and your ceiling to nothing. The better question is what the outcome is worth to the buyer — hours saved, revenue enabled, risk removed — and what alternatives they already pay for. Your costs only tell you whether a price is *viable*, never what it should be.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Choose the value metric
- [ ] Step 2: Choose the model (read references/pricing-models.md)
- [ ] Step 3: Define 2–3 good-better-best tiers
- [ ] Step 4: Run willingness-to-pay research (run scripts/van_westendorp.py)
- [ ] Step 5: Stress-test the band (including the ~$20 support floor)
- [ ] Step 6: Write the pricing page and the objection FAQ (assets/pricing-page.md)
- [ ] Step 7: Plan migration, grandfathering, and an annual discount
- [ ] Step 8: Verify every tier rests on the value metric
```

**Step 1 — Choose the value metric**
The value metric is the thing you charge per, and it should grow as the customer succeeds — seats, projects, events, volume, connected accounts, storage. A good metric scales with the value the buyer gets, is easy for them to predict before they commit, and doesn't punish them for using the product more. A bad one punishes the exact behaviour that creates value ("per report sent" taxes success). Name the metric before you name any price; a price without a metric is a number with no logic. Read `references/pricing-models.md` §2 for how to pick one against your business.

**Step 2 — Choose the model**
Decide *how* you charge using the model-chooser in `references/pricing-models.md` §1: subscription (recurring team value), one-time (a product that keeps working without upkeep), credits (bursty or unpredictable usage), or usage-based (the bill tracks consumption). Match the model to buying behaviour rather than to hype — for cold-start indie products, a one-time price can beat a subscription when the recurring support overhead would swamp the MRR (a common indie pattern). If you are unsure, read that section before committing.

**Step 3 — Define 2–3 tiers, good-better-best**
Ship two or three tiers, not five. A $29 / $99 / $299 scaffold is a common starting shape, not a rule — let the value metric set the rungs and the willingness-to-pay research (Step 4) set the numbers. Good-better-best means the middle tier is the one you actually designed for (it should be the obvious choice for your ICP), the lower tier removes the "too expensive to try" objection, and the top tier captures buyers whose value scales faster. Every tier must be described by its **value metric allowance** (e.g. "5 projects"), not a vague "more". Do not gate anything customers can't predict — see Gotchas.

**Step 4 — Run willingness-to-pay research**
If you can get 15+ responses from your actual ICP, run the Van Westendorp survey (`assets/pricing-survey.md`) and analyse it with the script:

```bash
python3 scripts/van_westendorp.py founder/pricing/responses.csv
```

It returns the four classic intersections — OPP, IDP/IPP, PMC, PME — and the acceptable range `[PMC, PME]`. Read the *band*, not a single number. With a smaller or noisier sample, fall back to interview-based willingness-to-pay: ask what they pay for the alternative today, what the problem costs them, and what they'd expect a tool like this to cost — then triangulate. Never treat interest as demand; the scare quotes in the survey only become real signal when the numbers are consistent across a real segment.

**Step 5 — Stress-test the band**
Before committing, pressure-test the number from both sides. Below roughly $20/mo, a solo founder's support, billing, and maintenance burden often exceeds what the price covers — flag any tier near that floor and either justify it as a loss-leader/one-time price or raise it (a common indie observation, not a law). At the top, check the price still reads as a round, defensible number against the alternatives you mapped. And sanity-check the model choice from Step 2 against the band: a subscription is a promise of ongoing value, so if the product is mostly "set up and forget", a recurring price will churn.

**Step 6 — Write the pricing page and the objection FAQ**
Turn the tiers into copy with `assets/pricing-page.md`. The page is where pricing objections are won or lost, so give every tier a one-line "who it's for", state the value metric plainly, and answer the four objections that actually block a purchase (usually: "is it worth it", "what if it's not for me", "can I get out", "why not the cheaper tier"). Hiding the price is a false economy — it filters out the buyers you want and invites tire-kickers.

**Step 7 — Plan migration, grandfathering, and an annual discount**
Pricing changes are agreements. For **new** customers, the new prices just apply. For **existing** customers, decide policy before you ship the page: grandfather them on their current price, migrate them at renewal, or give a notice window. Offer an annual plan as a discount (a "two months free"-style break is a common indie pattern — confirm the exact number yourself) to pull forward cash and reduce churn. **This is where the skill stops: moving prices for existing customers is the founder's call** and should never be applied automatically.

**Step 8 — Verify**
Re-read the brief against both gates: (1) every tier rests on the value metric and is expressed as an allowance of it; (2) no tier gates something the customer cannot predict (a variable bill they can't estimate, an unpredictable "fair use" cap, an add-on they can't price without a call). If either gate fails, fix the packaging before writing the page.

## Output format

Write `founder/pricing/pricing.md` using this structure:

```markdown
# Pricing: <product one-liner>
_Designed <date> · Stage: <pre-launch | launched | repricing>_

## Value metric
<the thing you charge per, and why it grows with customer success>

## Model
<subscription | one-time | credits | usage> — one line on why it fits buying behaviour.

## Tiers
| Tier | Price | Allowance | Who it's for | What changes |
| :-- | :-- | :-- | :-- | :-- |
| <Starter> | $<x>/mo | <n metric> | <ICP segment> | <the unlock> |
| <Pro> | $<y>/mo | <n metric> | <your main ICP> | <the unlock> |
| <Scale> | $<z>/mo | <n metric> | <bigger buyer> | <the unlock> |

> Prices are a hypothesis to test, not a commitment.

## Willingness-to-pay evidence
<Van Westendorp band [PMC–PME], OPP/IDP, medians, sample size; or the interview evidence and what it implies>

## Annual plan
<discount shape and why — confirm the exact percentage yourself>

## Migration & grandfathering
<what happens to existing customers — the founder decides>

## Open questions
- <what still needs testing and how>
```

## Gotchas

- **Pricing too low.** The most common solo pricing mistake. Below roughly $20/mo a price often does not cover the solo support and maintenance burden, and a cheap price can actively signal low quality. Charge for the value, not for how little you can get away with.
- **Cost-plus thinking.** Deriving the price from your costs caps you at your expenses plus a small margin. Anchor on the value created and the price of the alternative instead; use costs only to check viability.
- **Per-seat pricing for a non-team product.** If the buyer is one person, per-seat is just a confusing flat fee. Seats only pay off when the value genuinely scales with the number of people, and when the buyer controls the count.
- **Hiding the price.** "Contact us" and "request a demo" on a self-serve product filters out exactly the buyers you can serve and invites tire-kickers. Show the number.
- **Not testing.** A price you set once and never revisit is a guess with tenure. Run the survey or the interviews, then change one thing and watch the conversion, not the vibe.
- **Gating unpredictable things.** Caps on a metric the customer can't forecast, vague "fair use", or add-ons with no published price create support load and churn. Let people predict their bill before they buy.
- **The ~$20 support-burden floor.** Treat it as a flag to justify, not a hard rule — a one-time price or a deliberate loss-leader can sit below it, but a recurring price near the floor deserves a hard look at what support actually costs.
- **Human boundary — existing customers.** Changing the price for people already paying you is the founder's call, not the skill's. Always present the policy options and notify before applying anything.

## Available scripts

- **`scripts/van_westendorp.py`** — reads Van Westendorp survey responses (JSON array or CSV; four numeric answers per record: `too_cheap`, `cheap`, `expensive`, `too_expensive`) and prints the classic intersections — OPP, IDP/IPP, PMC, PME — plus the acceptable range `[PMC, PME]` and a warning below ~15 responses. Use `--json` for machine-readable output. Run `python3 scripts/van_westendorp.py --help` for the method and input schema.

## Reference files

- **`references/pricing-models.md`** — model-chooser table (subscription vs one-time vs credits vs usage), how to pick a value metric, freemium caveats, merchant-of-record for global tax, annual discounts, and grandfathering. Read at Steps 1–2.
- **`assets/pricing-survey.md`** — the four Van Westendorp questions verbatim, in a form you can send, plus recruitment guidance. Copy at Step 4.
- **`assets/pricing-page.md`** — tier + objection-handling template. Copy at Step 6.

## Hand-off

When the pricing brief is written, hand the tiers, the value metric, and the annual/positioning story to `go-to-market-launch`, so the landing page and launch copy quote the same numbers the pricing page does.
