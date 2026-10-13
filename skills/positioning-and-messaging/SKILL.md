---
name: positioning-and-messaging
description: Turns a validated idea into sharp positioning and copy — choose a market category, name the narrow best-fit buyer, then produce a one-line positioning statement, a landing hero (headline, subhead, CTA), value propositions, and a short messaging guide, and lint the headlines with a deterministic scorer. Use this skill whenever a solo founder or indie builder needs to position a product, write or fix a landing-page hero, differentiate from competitors, pick a market category, craft a value proposition, or say what they do in one sentence — even if they only say "my landing page isn't converting", "what category am I in?", "nobody gets what my product does", "help me write my homepage", or "how do I stand out from competitors?".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: gtm
---

# Positioning & Messaging

Use this skill to make your product *obvious* to the one buyer who should care — then write the words that carry it. It walks April Dunford's five-component method, produces a one-line positioning statement, a landing hero, value props, and a short messaging guide. **Positioning is the founder's call; this skill lays out the options, argues for the strongest frame, and drafts the copy.**

Outputs land in `founder/gtm/positioning/` so `go-to-market-launch` and `pricing-strategy` can pick them up.

## The one rule

**Positioning is the context that makes the product obvious to the right buyer; the headline is 90% of the marketing.** If a stranger cannot repeat what you do after five seconds, the positioning is wrong — not the stranger. Every other choice (category, segment, value) exists to make that one sentence land.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: List the competitive alternatives (incl. spreadsheet, group chat, do nothing)
- [ ] Step 2: Extract unique attributes — what you have that alternatives don't
- [ ] Step 3: Translate attributes into value (outcome, not feature)
- [ ] Step 4: Name the best-fit customer — the narrow segment that cares most
- [ ] Step 5: Choose the market category that makes the value obvious
- [ ] Step 6: Write the one-line positioning ("X for Y who need Z, unlike W")
- [ ] Step 7: Write the hero, value props, and top objections
- [ ] Step 8: Lint the candidates (run scripts/headline_lint.py)
- [ ] Step 9: Cold-read test with a stranger (human step)
```

**Step 1 — List the competitive alternatives**
Your real competitors are rarely the funded startups you found on Google. Write down what your buyer actually does today: a spreadsheet, a Slack group, a junior hire, a stack of tools glued together, and **"do nothing."** Interview the buyer about what they use *now*, not what products exist. Without an honest alternatives list every later step points at the wrong target, because positioning is always relative to a choice the buyer is already making.

**Step 2 — Extract unique attributes**
For each alternative, list what you have that it doesn't. Attributes are facts, not adjectives: "syncs to the accounting ledger automatically", "runs locally", "no per-seat pricing", "works offline". This is where you discover whether you have any differentiation at all. If your list is empty, stop and fix the product or pick a narrower buyer — no headline can rescue an undifferentiated product. Copy `assets/positioning-canvas.md` into `founder/gtm/positioning/positioning.md` and fill in rows 1–2.

**Step 3 — Translate attributes into value**
An attribute is what you built; value is the outcome the buyer cares about. "Automated bank reconciliation" (attribute) becomes "close your books two days earlier without a weekend" (value). Always ask "so what?" until you reach something a buyer would repeat to their boss. Features live in the product tour; value lives in the headline. Draft the value column of the canvas here.

**Step 4 — Name the best-fit customer**
The buyer who values that outcome *most* — not "small businesses" or "everyone". Narrow until it feels uncomfortable: an industry, a role, a workflow, a stage. "Freelance illustrators who invoice five-plus clients a month" is a segment; "creatives" is a wish. A narrower segment is what makes the value feel urgent and the headline feel custom. "Everyone" as the ICP is the fastest way to be obvious to nobody.

**Step 5 — Choose the market category**
The category is the frame that tells the buyer what this is and who else plays here. Pick the existing category your buyer already has budget and vocabulary for, and position *within* it — that is usually the cheapest path. Read `references/positioning-method.md` for how to choose, and when creating a **new category** is worth its high cost (you must teach the market the problem exists). Record the choice and one sentence of reasoning in the canvas.

**Step 6 — Write the one-line positioning**
Fill the pattern: **"<Product> is a <category> for <best-fit customer> who need <value>, unlike <alternative>, which <gap>."** This is an internal alignment tool, not the headline — it forces every component to agree. If any slot is vague, go back a step. Keep it to one sentence; if it needs two, the positioning isn't decided yet.

**Step 7 — Write the hero, value props, and top objections**
Now write to the buyer. Three headline candidates minimum (one plain, one outcome-led, one bold), plus a subhead that adds the mechanism, a single primary CTA, 3–4 value props (value first, feature as proof), and the top 3 objections with honest answers. Use `assets/messaging-guide.md` → `founder/gtm/positioning/messaging.md`. The hero must survive Step 8 and Step 9 before you treat it as final.

**Step 8 — Lint the candidates**
Run every headline and value-prop line through the scorer:

```bash
python3 scripts/headline_lint.py \
  "Cut invoice chasing from hours to minutes for freelance designers" \
  "The CRM for wedding photographers" \
  --file founder/gtm/positioning/hero-candidates.txt
```

It flags the predictable faults — too long, buzzwords, company-first openings, no audience cue, feature-first phrasing, no verb, shouting, clichés — and scores each 0–100. Use it to rank candidates and find the obvious fixes, then rewrite and re-run. It is a coach, not a verdict: a flagged word can be right in your context. Never let the score overrule a founder's taste.

**Step 9 — Cold-read test (human step)**
Hand the hero to a stranger — someone outside your market and outside your head. Give them **five seconds**, then ask: "What does this do, and who is it for?" If they cannot say it back in their own words, the positioning has failed and you go back to Step 6. **The founder finds and runs the stranger**; this skill only prepares the copy and the exact question to ask. Correct a headline you cannot explain in one breath, not one you cannot explain in ten.

## Output format

Write two files. Use these as the default structure (the matching assets in `assets/` are the fill-in versions — copy them, don't retype):

`founder/gtm/positioning/positioning.md`

```markdown
# Positioning: <product>

## Alternatives
| Alternative | Who it serves | Why it wins | Where it fails for us |
| :-- | :-- | :-- | :-- |

## Unique attributes → value
| Attribute (fact) | So what? (value to buyer) |
| :-- | :-- |

## Best-fit customer
<narrow segment, in one sentence>

## Market category
<chosen category> — <one line on why; note if proposing a new category and its cost>

## One-line positioning
<X> is a <category> for <Y> who need <Z>, unlike <W>, which <gap>.

## Change we create
<the before → after state for the buyer, one line>
```

`founder/gtm/positioning/messaging.md`

```markdown
# Messaging: <product>

## Hero
- Headline: <chosen candidate>  (lint score: <n>/100)
- Subhead: <the mechanism, one sentence>
- CTA: <one primary action>

## Headline candidates
1. <plain> — lint <n>
2. <outcome-led> — lint <n>
3. <bold> — lint <n>

## Value propositions
- **<value>** — <feature as proof>
- **<value>** — <feature as proof>
- **<value>** — <feature as proof>

## Top objections
| Objection | Honest answer |
| :-- | :-- |

## Voice notes
<tone, words we use, words we avoid>
```

## Gotchas

- **Jargon and internal language.** Names of your own features and architecture mean nothing to the buyer. If a term only makes sense after a demo, it does not belong in the hero. The cold-read test catches this.
- **Feature-first copy.** "A dashboard that…" names the object; buyers pay for the change. Lead with the outcome; let the feature be the proof underneath.
- **"Everyone" as the ICP.** Positioning to everyone positions to no one. The narrower the segment, the more the value and headline feel personal — and the easier the sale.
- **Copying a competitor's category and copy.** Borrowing their frame inherits their strengths and your weakness (you are the new, smaller one). Start from your alternatives and attributes, then pick your own frame.
- **A headline that describes what the product is, not the change it creates.** "AI-powered note-taking app" says nothing a buyer repeats. State the before → after.
- **Positioning drift after month one.** The first customer segment, a competitor's move, or a new feature quietly outgrows the copy. Re-run the lint and the cold-read test after any material change — treat positioning as versioned, with a date.
- **Claims, comparisons, and proof points are the founder's to approve.** This skill never invents testimonials, metrics, or "better than X" claims. Any comparative or numeric claim must be supplied and verified by the founder before it ships.

## Available scripts

- **`scripts/headline_lint.py`** — heuristically lints one or more candidate headlines (positional args, `--file`, or stdin), flags length, buzzwords, clichés, company-first openings, missing audience cues, feature-first phrasing, missing verbs, and ALL-CAPS words, and prints each issue with a suggestion plus a score out of 100. `--json` for machine-readable output. Run `python3 scripts/headline_lint.py --help`.

## Reference files

- **`references/positioning-method.md`** — the Dunford five components, how to choose a market category, when creating a new one is worth it (and its cost), and worked before/after examples of weak vs strong positioning. Read at Steps 1–6.
- **`assets/positioning-canvas.md`** — fill-in canvas: alternatives, attributes, value, customer, category. Copy to `founder/gtm/positioning/positioning.md` at Step 2.
- **`assets/messaging-guide.md`** — fill-in template: one-liner, hero, value props, objections, voice notes. Copy to `founder/gtm/positioning/messaging.md` at Step 7.

## Hand-off

When positioning and the hero hold up to the cold-read test, pass `positioning.md` and `messaging.md` to **`go-to-market-launch`** (channel copy, launch assets) and to **`pricing-strategy`** (positioning sets the frame for how price is anchored and justified).
