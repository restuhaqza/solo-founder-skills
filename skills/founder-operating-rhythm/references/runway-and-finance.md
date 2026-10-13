# Runway and Simple Finance for the Solo Founder

**Contents**
1. Runway, defined precisely
2. The default alive / default dead test
3. The tax set-aside habit
4. The monthly bookkeeping rhythm
5. The quarterly reconciliation
6. Keep personal and business money separate
7. Keep exit-ready books

---

## 1. Runway, defined precisely

**Runway is how many months of cash you have left at the current burn rate.** If you hold $120,000 and your net monthly burn (costs minus revenue) is $6,000, you have 20 months. If revenue covers costs, you are not burning and runway is not really the right frame — cash only shrinks if costs rise or revenue falls.

Two things trip founders up:

- **Runway uses net burn, not gross costs.** If you spend $14,000/mo and collect $8,000/mo, you burn $6,000 — not $14,000. Using gross costs understates your runway and creates needless panic. Use revenue *you have collected*, not booked or invoiced, and subtract costs that have actually left the account.
- **Runway is a rear-view number.** It assumes this month repeats. The moment costs or revenue change, recompute. A single month is a data point; three months is a trend.

**How much runway is enough?** There is no universal number, and it depends on whether you are raising, profitable, or building toward an exit. The useful discipline is not the target — it is *knowing the number this month and comparing it to last month*. A founder who knows they have 6 months behaves differently from one who thinks they have "a while." Know the number before it forces the decision for you.

## 2. The default alive / default dead test

Paul Graham's framing for a startup without a certain next round: **given your current cash, your current growth rate, and your current spending, are you default alive or default dead?** Default alive means you can reach profitability (revenue covering costs) before the money runs out, at the growth rate you actually have — without needing to raise. Default dead means you cannot, and you will need to raise, cut, or grow faster *before* the cash forces the issue.

The test is deliberately blunt. It is a *forecast*, not a verdict on the idea:

1. Take current cash on hand.
2. Take the net monthly burn, and how fast revenue is growing.
3. Ask: does growing revenue reach the cost line *before* cash hits zero?

`scripts/runway.py` computes exactly this. The reason it matters: the number is honest about *time*, and time is what converts a solvable problem into a forced one. A business that is default dead with 18 months of runway has a plan; the same business discovered at 3 months has a crisis. Run the test while there is still room to act.

**The flip rate turns the verdict into a target.** Because break-even moves earlier as growth rises, there is a minimum monthly growth rate at which the test flips from default dead to default alive. `scripts/runway.py` reports it. At $120k cash, $8k revenue, and $14k costs, the flip is about **2.8%/mo** against the 20-month pre-tax runway — and about **4.0%/mo** against the 14.3-month after-tax runway, a higher bar because the tax set-aside shrinks the revenue that reaches the cost line. Always quote the rate with the basis it is measured against, and treat it as the number to hold, not as a forecast.

**When you are default dead, the four levers** are: raise revenue (price, retention — usually the fastest), cut costs, raise money, or accept a smaller business on purpose. Notice that "work harder" is not on the list; it rarely moves the arithmetic in time.

## 3. The tax set-aside habit

Set aside a slice of every payment you collect, in a separate place, the moment it arrives. **A common solo range is 25–30% of revenue**, and many founders start at the higher end until an accountant tells them their real rate. This is a *habit*, not a tax calculation: what you actually owe depends on your entity, your jurisdiction, deductions, and whether you have paid quarterly estimates. `scripts/runway.py` models the set-aside as `--tax-rate` (default 0.30) of gross revenue — a planning buffer, nothing more.

Two rules that save founders from a bad quarter:

- **Set it aside on money received, not money earned.** The bill arrives later than the cash; if the cash is already spent, the bill is a shock.
- **Move it out of the operating account.** Money you can see is money you spend. A separate savings account or sub-account makes the set-aside real.

If you are unsure of your rate, if you have non-US or multi-jurisdiction exposure, or if this is your first year, **ask an accountant before your first estimated payment** — the cost of the question is far below the cost of the surprise.

## 4. The monthly bookkeeping rhythm

Bookkeeping is a monthly ritual, not an annual scramble. Once a month, in one sitting:

1. **Reconcile the business account** — every transaction accounted for, nothing missing, nothing personal. (See §6.)
2. **Categorise expenses** — software, contractors, hosting, ads, and so on. Consistent categories now make the year-end handoff trivial.
3. **Capture receipts** as they land, not in a shoebox in April. Photograph them into the same place every time.
4. **Record revenue** as collected, and note anything invoiced-but-unpaid (chase it — see §7).
5. **Run `scripts/runway.py`** and log the numbers to `assets/runway.csv`, so each month is a comparison to the last.

Choose one boring tool and stay with it (a spreadsheet is fine early; QuickBooks/Wave-style tools once volume or a customer requires it). The goal is not accounting sophistication — it is **never being surprised**, and handing a clean file to an accountant so you pay for review, not for cleanup.

## 5. The quarterly reconciliation

Every quarter, spend an hour doing what monthly bookkeeping cannot do:

- **Reconcile revenue to the payment processor.** Does what Stripe (or your merchant of record) says you collected match your books? Differences usually mean refunds, fees, or a missed chargeback.
- **Check the tax set-aside against what you have actually paid or reserved.** Adjust the rate if it has drifted.
- **Review subscriptions and tools.** Cancel anything you did not open this quarter — over-tooling compounds silently.
- **Re-run the default alive/dead test** and compare break-even month to last quarter. The trend matters more than the level.
- **Note anything a professional should see** (a new jurisdiction, a new contract type, a first hire or contractor) and book that conversation.

## 6. Keep personal and business money separate

Use **separate bank accounts and separate cards** for the business and for you, and move money between them only on purpose (an owner draw, a capital contribution, a reimbursement). This is not bookkeeping neatness — for a single-member LLC it is the thing that keeps the liability shield meaningful. **Commingling funds** (paying a personal expense from the business account, or running business costs through your personal card) is a classic way courts and counterparties treat the business and the owner as one and the same, which is often the entire reason the entity exists. It also makes tax time and any future sale dramatically harder.

The habit: business money only touches business accounts; you pay yourself a clear, labelled draw; you keep receipts for anything that could be questioned.

## 7. Keep exit-ready books

Even if you have no plan to sell, run your books as if a buyer could look at them — because the cost of making them clean *later* is far higher than keeping them clean now. When someone does eventually look, they rarely just want MRR. They look at:

- **Churn quality** — how much churn is voluntary vs involuntary, who leaves, and whether the retained customers actually expand. Clean books let you answer this; messy ones hide it.
- **Revenue concentration** — how much revenue comes from one customer or one channel. Heavy concentration is a discount on any offer; knowing it early lets you diversify while it is cheap.
- **Whether profit survives someone else running it** — can the business function without founder-specific heroics? Books that separate the business from the founder make that visible.
- **Invoices actually collected** — chase overdue invoices politely and automatically; uncollected revenue is not revenue.

The through-line for all of this: **know your numbers, keep them honest, and keep the business separate from you.** That is the whole discipline. This file is a starting point — your accountant decides how your specific entity, jurisdiction, and situation should be handled.

---

*Planning guidance only, not tax, legal, or accounting advice. Confirm your entity, set-aside, and filings with a qualified professional.*
