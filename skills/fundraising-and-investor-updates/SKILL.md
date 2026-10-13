---
name: fundraising-and-investor-updates
description: Decide whether to raise at all, then prepare the raise (narrative, pitch deck, data room, dilution math) and run the monthly investor update that compounds trust. Use this skill whenever a solo founder or indie builder is weighing fundraising, venture capital, angels, SAFEs, convertible notes, or a priced round; wants to build an investor pitch deck, a data room, or an investor-update email; needs to work out dilution, valuation, price per share, cap-table impact, or how much runway a round actually buys; or is about to report to existing investors — even if they only say "should I raise?", "help me with my pitch", "what does my cap table look like after this round?", "I need to write my monthly investor update", or "an investor asked for my metrics".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: fundraising
---

# Fundraising and Investor Updates

Use this skill to make the raise a deliberate decision and a disciplined process: decide whether to raise, define the milestone the money buys, build the narrative, deck, and data room, check the dilution math before quoting terms, and ship the monthly investor update that turns a check into a relationship. It produces files you fill in and one number-check you run — not advice.

Outputs land in `founder/fundraising/`. If `founder/context.md` is missing, create it first (product one-liner, ICP, stage, north-star metric, stack).

## The one rule

**Raise against a milestone, not a mood — and if you raise, the monthly update is the product you ship to investors.** Money without a milestone to reach is a timer, not a strategy: it buys months, and months without a defined target burn down to the same place faster and with more people watching. The raise exists to reach a *specific, provable* next state. And once money is in, the update is the relationship: same shape every month, honest about misses, one clear ask. Founders who go quiet after the close are the ones nobody follows on.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Decide whether to raise at all
- [ ] Step 2: Define the milestone and the runway it must buy
- [ ] Step 3: Write the narrative and the deck (assets/pitch-deck-outline.md)
- [ ] Step 4: Build the data room (assets/data-room-checklist.md)
- [ ] Step 5: Check dilution and cap table (run scripts/raise_math.py)
- [ ] Step 6: Draft the monthly investor update (assets/investor-update.md)
- [ ] Step 7: Verify — claims trace to data, ask ties to milestone
```

**Step 1 — Decide whether to raise at all**
Before you optimise a deck, decide whether a round is the right move. Match the thing you actually need against what capital buys. A round is worth it when the next milestone is *expensive and time-sensitive*: a hiring or infrastructure step, a market land-grab, a regulatory or go-to-market push that a competitor is also running. It is usually a bad trade when the bottleneck is founder attention, distribution learning, or a product that has not yet earned its first paying customers — because for a small product a lean agent-and-tooling stack plus time often reaches the milestone for less than the dilution, the reporting, and the loss of control a round costs. Read `references/raising-basics.md` for the honest bootstrap-vs-raise framing and the instrument choice (equity vs SAFE vs convertible note) at a high level. Frame it as a trade, then let the founder own the call. Why: a raise is a commitment to *grow*, and it is very hard to un-commit — it changes your incentives, your board, and your pace. The most common solo mistake is raising for validation rather than for a milestone.

**Step 2 — Define the milestone and the runway it must buy**
Write one sentence: *"This round buys <runway in months> to reach <milestone>, which unlocks <next round or default alive>."* The milestone must be **provable** — a revenue or usage threshold, a product in market, a signed channel, a retention curve that holds — not "get more traction." Then compute the runway honestly (that is `founder-operating-rhythm`'s runway script, not this one): what the money buys after the costs it forces on you (hiring, tools, travel). Why: this sentence is the spine of the whole pitch, and it is also your own decision tool. If the raise does not buy enough runway to reach the milestone at a credible burn, the round as scoped is the wrong size — resize the round, shrink the milestone, or don't raise. Everything in the deck descends from this line.

**Step 3 — Write the narrative and the deck**
Open `assets/pitch-deck-outline.md` and fill it in order: problem, insight, product, traction (real numbers only), market, business model, go-to-market, team, ask, use of funds. Lead with the *insight* — the non-obvious thing you understand about the problem that your competitors do not. Why: investors fund a belief about the future, and the deck's job is to make that belief feel inevitable, not to list features. Keep it short; a solo founder's advantage is a crisp, unfakeable story about a real problem, not a 40-slide investor-book. Read `references/pitch-and-updates.md` for the narrative structure and what traction to show at each stage. Every number on a slide must trace to something real — a Stripe export, a cohort, a signed pilot. If you cannot source it, cut it.

**Step 4 — Build the data room**
Work `assets/data-room-checklist.md` so that when diligence starts you are handing over a folder, not scrambling. Why: a clean, indexed data room sends two signals at once — that the business is real and that you are easy to work with. Both matter more to a small solo round than any single metric. Complete the *essential* items (company docs, cap table, financials, the product and its metrics, key contracts) and mark the *as-asked* items (e.g. detailed IP assignments, security questionnaires) so you are not blocked. Never put anything in the data room you have not read — you are the one accountable for it.

**Step 5 — Check dilution and the cap table before quoting terms**
Run the math before you say a number to an investor:

```bash
python3 scripts/raise_math.py --pre-money 8000000 --raise 2000000 --option-pool 10
```

It returns post-money valuation, the new investor's ownership, founder/existing dilution, price per share, shares issued, and a before/after cap table; add `--option-pool` to model the pool shuffle and `--cascade <next_pre> <next_raise>` to see cumulative founder ownership after a second round. Why: founders quote a pre-money without mentally running the dilution and the option-pool shuffle, then discover after signing that they gave away more than they thought. Run the cascade view so you can see where a second round lands *you* — the round you are raising is often justified by the round after it.

**Step 6 — Draft the monthly investor update**
Copy `assets/investor-update.md` to `founder/fundraising/updates/<YYYY-MM>.md` and fill it in the same shape every month: the numbers (from `product-metrics`, not re-derived here), what went well, what went badly, what you are doing about it, and **one clear ask**. Send it on the same day each month, good news or bad. Why: the update is the product you ship to investors, and its consistency is the signal. Reporting a miss early, with a plan, buys credibility; disappearing until the good news arrives spends it. `references/pitch-and-updates.md` covers the template, the cadence, and the golden rule of updating on bad news too. **The founder writes the note in their own voice and sends it; this skill only drafts it.**

**Step 7 — Verify**
Before the deck goes out or the update is sent, check three things: every claim in the deck traces to real data (name the source next to the number); the ask ties to the milestone from Step 2 (not to a round size someone told you was normal); and the update stands on its own — an investor can read it without the founder re-explaining the business. If any of those fails, fix it before shipping, not after an investor asks.

## Output format

Write `founder/fundraising/raise-memo.md` as the one-page internal decision and tracking doc:

```markdown
# Raise Memo — <company>
_Drafted <date> · Stage: <pre-seed | seed | ...>_

## Decision
<Raise | Bootstrap | Not yet> — and the one-line reason.

## The milestone this round buys
"This round buys <N months> of runway to reach <provable milestone>, which unlocks
<next round / default alive>."

## The ask
- Raising: <amount> at <pre-money> pre-money  (post-money: <amount>)
- Instrument: <priced equity | SAFE | convertible note>
- Use of funds: <hiring | product | GTM | infra> — with the split
- Dilution (from scripts/raise_math.py): new investor <x>%, founder keeps <y>%

## Narrative spine
<problem -> insight -> product -> traction -> market -> model -> GTM -> team>

## Data room status
- Ready: <items>
- In progress: <items>
- As asked: <items>

## Open questions for a professional
<term-sheet terms, tax, or entity questions a lawyer/accountant must answer>
```

Then draft the deck into `founder/fundraising/deck.md` (from `assets/pitch-deck-outline.md`), keep the data room in `founder/fundraising/data-room/`, and send updates from `founder/fundraising/updates/`.

## Gotchas

- **Raising without a milestone.** Money that buys runway toward nothing buys a faster deadline. If you cannot finish the sentence in Step 2, you are not ready to raise — you are anxious.
- **Optimising the deck over the business.** A better deck does not make a better company, and investors can tell. If the traction slide is thin, the fix is usually in the product and customers, not the font.
- **Hiding bad news in updates.** Skipping the miss, burying it in paragraph six, or going quiet until good news arrives is the fastest way to lose the investors you have. Report misses early, with the plan.
- **SAFE stacking and unclear terms.** Several SAFEs with different caps and discounts can turn an easy "raise" into a confusing cap table that spooks the next lead — and a "simple" document you did not read can carry a valuation cap, a discount, or a most-favored-nation clause you did not intend. Keep a running stack, read every term, and route the wording to a lawyer.
- **Dilution blindness.** Quoting pre-money without running the option-pool shuffle and the second-round cascade is how founders give away more than they think. Run `scripts/raise_math.py` before you say a number.
- **Treating investor communication as optional after the close.** The monthly update is not a courtesy; it is how the relationship and the next round's social proof are built. Consistency beats eloquence.
- **A raise changes your incentives.** Once you have outside money, growth expectations and a board arrive with it. Decide whether you want that *before* you sign, not after.
- **This is not investment, legal, or tax advice.** Everything here is a first draft or a decision aid. Terms, instruments, securities compliance, and tax are for a qualified professional — and the founder makes every term and legal decision and sends every investor communication.

## Available scripts

- **`scripts/raise_math.py`** — gives pre-money, raise, optional `--option-pool` (post-money %, created pre-money) and `--existing-shares`, and prints post-money valuation, the new investor's ownership, founder/existing dilution, price per share, shares issued, and a before/after cap table. `--cascade NEXT_PRE NEXT_RAISE` adds the cumulative founder ownership after a second round; `--json` for structured output. Run `python3 scripts/raise_math.py --help` for the math and input schema.

## Reference files

- **`references/raising-basics.md`** — raise vs bootstrap, instrument choice (equity vs SAFE vs convertible note) at a high level, runway-to-milestone thinking, dilution basics, and the "raise for a milestone" rule. Read at Steps 1–2.
- **`references/pitch-and-updates.md`** — the deck narrative structure, what traction to show at each stage, the monthly update template and cadence, the golden rule of updating on bad news, and the data-room contents. Read at Steps 3, 4, and 6.
- **`assets/pitch-deck-outline.md`** — fill-in deck outline. Copy to `founder/fundraising/deck.md`.
- **`assets/investor-update.md`** — the same-shape-every-month update template. Copy to `founder/fundraising/updates/<YYYY-MM>.md`.
- **`assets/data-room-checklist.md`** — essential vs as-asked diligence items. Work it into `founder/fundraising/data-room/`.

## Hand-off

The raise's numbers rest on two siblings. When the milestone sentence needs a runway figure — how many months the money buys, whether you are default alive or dead — hand off to `founder-operating-rhythm` and its runway script, and bring the result back into the memo. The update's numbers come from `product-metrics`; do not re-derive MRR, churn, or activation here — pull them, and hand back when a number's meaning is in question. Once the round is closed and the cash is on the runway, the operating rhythm takes over.
