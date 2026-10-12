# Pricing Survey — Van Westendorp (send-ready)

Copy this into a form, an email, or a DM. Keep the four questions together and
in this order so the answers don't anchor each other. Replace the bracketed
bits, and put a one-paragraph description of the product at the top so people
are pricing the same thing.

The goal is *willingness to pay*, not approval. Do not ask "would you buy
this?" and do not hint at the "right" answer.

---

## What to send

**Subject / opener:** Quick pricing question about [product] — 2 minutes

Hi [name],

I'm building [one-line description of the product and the outcome it creates].
Before I settle on a price, I'd rather hear it from people who'd actually use
it than guess.

If you have two minutes, please answer these four questions with a specific
number in your currency (a rough figure is fine — you can go low or high):

**1. At what price would you consider [product] to be so expensive that you
would not consider buying it?**
> [ your answer ]

**2. At what price would you consider [product] to be priced so cheaply that
you would doubt its quality?**
> [ your answer ]

**3. At what price would you consider [product] to be a bargain — a great buy
for the money?**
> [ your answer ]

**4. At what price would you consider [product] to be expensive, but you would
still buy it?**
> [ your answer ]

Two optional follow-ups that make the numbers usable:

- What do you use to solve this today, and what does that cost you (money or
  time)?
- Would you expect to pay for this monthly, once, or per [usage unit]?

Thanks — this genuinely changes what I build and charge.

---

## How the four questions map to the analysis

Keep the wording above; when you log the responses, use these column names so
`scripts/van_westendorp.py` reads them directly:

| Question | Field name | The price at which… |
| :-- | :-- | :-- |
| 1 | `too_expensive` | they would **not** buy |
| 2 | `too_cheap` | they doubt the quality |
| 3 | `cheap` | it's a genuine bargain |
| 4 | `expensive` | it's high, but they'd still buy |

Log one row per respondent, like:

```csv
too_cheap,cheap,expensive,too_expensive
12,25,60,90
10,20,55,80
```

`too_cheap`, `cheap`, `expensive`, `too_expensive` — all four required, all
numeric, per row. Then run `python3 scripts/van_westendorp.py responses.csv`.

---

## Recruitment guidance

- **Recruit your actual buyer, not your audience.** The right respondents are
  people who match your ICP and would make or influence the buying decision.
  Fans who will never pay give you fan-shaped numbers.
- **Aim for 15–30 responses in one narrow segment.** Below ~15 the
  intersections are noisy (the script warns you); above ~30 you usually stop
  learning. Averaging across several segments hides the real signal — run one
  segment at a time.
- **Avoid friends and family, and avoid leading.** Compliments corrupt price
  data. If you must include someone close, weight their answer down and never
  tell them your target price.
- **Offer a small incentive** (a discount at launch, a coffee) to lift response
  rate — the sample size matters more than saving a few dollars.
- **Don't let respondents see each other's numbers** before answering; that is
  the whole reason to ask all four questions of everyone.
- **Ask about the alternative too.** "What do you pay for this today?" turns an
  abstract number into a comparable one, and it's the least-fakeable question in
  the set.

## Reading the results

- Report the **band**, not a point: the acceptable range `[PMC, PME]` from the
  script. A single intersection is noisier than the range around it.
- Cross-check against **competitor prices and interview answers**. If the
  band sits far above what the alternatives cost, either your value story is
  stronger than you can yet prove, or the sample was not your real buyer.
- Treat a number as a **hypothesis to test on the page**, not a decision. The
  only honest confirmation is people paying it.
