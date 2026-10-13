# Raising Basics for the Solo Founder

**Contents**
1. Raise vs bootstrap: the honest trade
2. What capital actually buys
3. Runway-to-milestone thinking
4. Instrument choice: equity vs SAFE vs convertible note
5. Dilution basics
6. The "raise for a milestone" rule
7. What to route to a professional

---

## 1. Raise vs bootstrap: the honest trade

Raising is not a level-up; it is a trade. You exchange a slice of the company, a measure of control, and a permanent expectation of *growth* for cash you can spend now. Bootstrapping keeps the whole pie and the whole decision, but caps the speed at what you can fund yourself or reinvest. Neither is correct in the abstract — the question is which one fits the next step.

Ask three questions before choosing:

- **Is the bottleneck money or attention?** If the thing between you and the milestone is a hiring, infrastructure, or land-grab cost you cannot self-fund in time, capital helps. If it is that you have not found distribution or that customers do not yet pay, more money usually just funds a longer search at a higher burn — and a small, lean stack plus time is the cheaper way to find out.
- **Could an agent-and-tools stack plus time reach the milestone for less?** For a small product, much of what used to require a first hire — coding, support, content, ops — increasingly runs on a few hundred dollars a month of tooling. If the milestone is a product and retention threshold rather than a headcount threshold, "buy time, not people" is often the honest answer. This does not make a raise wrong; it raises the bar for why you need one.
- **Do you want the incentives that come with it?** Outside money brings a board, reporting, and the expectation to grow at venture pace. That can be exactly the forcing function a solo founder needs, or it can be a weight. Decide before, not after.

**The default for a small solo product is bootstrap until a milestone proves the model, then raise (if at all) to compress time toward the next one.** Raise because the milestone is expensive and time-sensitive — not because fundraising feels like progress.

## 2. What capital actually buys

Capital buys exactly two things, and founders routinely confuse them:

- **Time** — months of runway at a given burn. This is the honest unit.
- **Compressed time** — the same milestone reached sooner by spending money on people, tools, or distribution in parallel rather than sequentially.

It does **not** buy product-market fit, a working go-to-market, or retention. Those are learned, not purchased. A round handed to a product that customers will not pay for accelerates the discovery that they will not pay — which is useful but expensive information.

So the useful question is never "how much can I raise?" but "what is the smallest amount that removes the specific bottleneck standing between me and the milestone?" Size the round to the bottleneck, plus a margin for slippage, and no more. An oversized round is a higher burn than the milestone requires, which shortens the runway you thought you were buying.

## 3. Runway-to-milestone thinking

Runway is how many months of cash you have left at the current net burn. The discipline that keeps a raise honest is tying it to a *provable* milestone:

> "This round buys **N months** to reach **[milestone]**, which unlocks **[the next round / default alive]**."

A milestone is provable when it is a threshold you either cross or do not: a revenue or usage number sustained for a period, a working product in a real customer's hands, a signed distribution channel, a retention curve that flattens. "More traction" and "get to the next stage" are not milestones; they cannot be reached or missed, so they cannot guide how much you raise or how you spend it.

Then do the arithmetic the old-fashioned way: estimate the burn the milestone *forces* on you (hiring, tools, travel, contractors — costs you do not have today), divide the amount you intend to raise by that burn, and see whether the resulting months are enough to credibly reach the milestone with a margin. If they are not, you have three honest moves: raise more (more dilution), shrink the milestone to the largest thing the money *can* buy, or do not raise yet. `scripts/raise_math.py` handles the ownership side; the runway arithmetic belongs to `founder-operating-rhythm` and its runway script — use both, and keep the milestone sentence at the top of the memo.

## 4. Instrument choice: equity vs SAFE vs convertible note

There are three common instruments, and the differences that matter to a founder are *who sets the price and when*, and *what the document obliges you to do*. This is a conceptual map; the actual terms and the legally correct choice for your jurisdiction and round are a lawyer's call.

- **Priced equity round.** A negotiated price now: you and the investor agree a pre-money valuation, shares are issued at a price per share, and the new investor knows their exact ownership from day one. It is the most work up front (a term sheet, legal documents, often a lead investor) and the most clarity after. Typically used once there is enough traction to justify a negotiated price and a new lead.
- **SAFE (simple agreement for future equity).** Money now, price later. It converts into shares at a future priced round, usually with a **valuation cap** (the most the SAFE values the company at conversion) and often a **discount** on the future round's price. It is fast, cheap, and founder-friendly to raise — and easy to *stack* carelessly. Several SAFEs with different caps and discounts can convert at different prices and produce a cap table that surprises everyone at the next round.
- **Convertible note.** Like a SAFE, but it is debt: it carries interest and a maturity date, and if no qualified financing happens by maturity it can come due — a real obligation. Used when a bridge or a specific tax treatment calls for it; the maturity is the clause to read.

Two practical cautions:

- **The cap is the price you did not set.** A SAFE with a low cap can hand over more ownership than a priced round with the same headline amount would have. Run `scripts/raise_math.py --cascade` to see where a stack of conversions lands you before you sign another one.
- **Keep a running stack.** Track every SAFE and note — amount, cap, discount, and any most-favored-nation clause — in one file, because the next lead investor will ask, and a confusing stack is a reason to walk.

## 5. Dilution basics

Dilution is simply the share of the company you no longer own after new shares are created. Two things get confused:

- **The investor's share** is `raise / (pre-money + raise)` — the raise divided by the post-money. At $8M pre-money and a $2M raise, the investor owns 20% and the post-money is $10M. The higher the pre-money, the less you give away for the same money.
- **Existing holders' dilution** includes not just the investor but everything created alongside the round — most importantly the **option pool**. Pools are usually quoted as a percentage of the *post-money* company and created *before* the round, so they dilute the founders, not the new investor. A 10% pool on top of a 20% new investor leaves the founder with 70% of the post-money, not 80%.

The two distortions a founder misses:

- **The option-pool shuffle.** "We'll need a 10% pool" sounds like a future cost; created pre-money, it is a present cost to *you*. Always model it with the round.
- **The second round.** Your ownership after round one is not where you finish. A second round dilutes the round-one cap table by `pre2 / post2`. Founders justify round one by round two and then discover, too late, how little of round two they still own. See it with `--cascade` before you commit.

None of this is a reason not to raise; it is a reason to *know the number* before you quote a term. Never let an investor's "industry standard" substitute for running your own cap table. `scripts/raise_math.py` does the arithmetic; keep the output next to the memo so the decision is made on numbers, not nerves.

## 6. The "raise for a milestone" rule

The whole file reduces to one rule: **the raise must be defined by the milestone it buys, not by the amount you can get.** A round is a means to a specific, provable end. If the end is fuzzy, the round becomes a timer, the burn becomes the story, and the next conversation with investors is about runway instead of progress. The founders who make raising look easy are the ones who could say, on the way in and on the way out, exactly what the money was for — and then reported against it every month.

Corollary: the milestone sentence is also your filter for *which* investors to take. Someone who believes in the same next step is a partner; someone shopping for a different trajectory is a source of pressure. Match on the milestone, not just the check.

## 7. What to route to a professional

Everything above is a decision aid. These are not, and must go to a lawyer, accountant, or tax advisor before you act:

- **The instrument and its wording** — term sheets, SAFE/note documents, conversion mechanics, board and governance rights, liquidation preferences, pro-rata and information rights.
- **Securities compliance** — how and to whom you may offer securities in your jurisdiction; this is where well-meaning founders get into real trouble.
- **Tax** — how the raise, any conversion, and equity compensation are treated, and what filings follow.
- **Entity and structure** — whether your current entity can cleanly take the round, and what (if anything) to change first.

The skill drafts, computes, and organises. The founder signs, sends, and decides — with professional review where the stakes are real.

---

*Planning guidance only — not investment, legal, or tax advice. This file is intentionally conceptual; the specifics of any instrument, jurisdiction, or term must be confirmed by a qualified professional.*
