---
name: content-and-seo-engine
description: Run a compounding content program that gets a product found in both classic search and AI answers — one pillar piece plus three or four supporting pieces a month, each briefed, optimised for search and generative-engine (GEO/AEO) citations, and atomised across channels. Use this skill whenever a solo founder or indie builder wants an ongoing content engine, an editorial calendar, a SEO or AI-search (GEO/AEO) content plan, a content brief, blog post outlines, a repeatable publishing cadence, or wants to stop relying on one-off launches and start compounding attention — even if they only say "how do I get traffic?", "my blog gets no visitors", "how do I get cited by ChatGPT?", "plan my content for next month", or "what should I write about?". Outputs go to founder/gtm/content/.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: gtm
---

# Content & SEO Engine

Use this skill to run the ongoing program that keeps a product found — not a one-off campaign. It turns the single biggest question your buyer asks into a pillar piece, plans three or four supporting pieces around it, briefs each one so it does not drift, generates a dated calendar, and sets up the AI-search and distribution mechanics that make the work compound. **The founder publishes in their own voice and approves every claim and comparison; this skill drafts the plan and the briefs.**

Outputs land in `founder/gtm/content/`. If `founder/context.md` does not exist yet, create it first (product one-liner, ICP, stage, north-star metric, stack) — every skill in this suite reads it.

## The one rule

One pillar, three or four supporting pieces, every month, forever. Consistency and specificity beat volume. A content program is a *compounding* asset: it only works if you do not stop, which means the cadence has to be one a single founder can actually hold for a year — not a burst that looks impressive for a month and then goes quiet. Three specific pieces a month beats thirty vague ones, every time.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Pick the ONE question your buyer asks most — that is the pillar
- [ ] Step 2: Plan 3–4 supporting pieces, each answering a sub-question
- [ ] Step 3: Write a brief per piece (copy assets/content-brief.md)
- [ ] Step 4: Generate the dated editorial calendar (run scripts/editorial_calendar.py)
- [ ] Step 5: Optimise for AI answers (GEO/AEO) — headings, facts, schema, llms.txt
- [ ] Step 6: Repurpose: atomise each piece into thread, video, newsletter, community answer
- [ ] Step 7: Add one engineering-as-marketing artifact (a permanent asset)
- [ ] Step 8: Verify every piece — target query, internal link, distribution step
```

**Step 1 — Pick the ONE question your buyer asks most; that is the pillar**
The pillar is the piece you would bookmark and send to a colleague: your most complete, specific, opinionated answer to the single biggest question your buyer has. Find it in the words they actually use — the question they ask on the first sales call, the one repeated in support email, the one that opens every onboarding conversation. Not the question you wish they asked. If you cannot name the question in their language, you are about to write content nobody searches for. Write the question down verbatim; that phrasing becomes the target query.

**Step 2 — Plan 3–4 supporting pieces that each answer a sub-question**
Decompose the pillar into the narrower questions it implies: a comparison ("X vs Y"), a how-to for one step, a template, a teardown of a real problem, a "what does it cost" answer. Each supporting piece must **link up to the pillar**, and the pillar should link down to each. That cross-linking is how a cluster earns authority together instead of publishing as scattered orphans. Keep it to three or four; a pillar plus ten half-finished posts is a pile, not a cluster.

**Step 3 — Write a brief per piece (name the intent, query, outline, internal links)**
A brief prevents drift. Before writing a word, fill in `assets/content-brief.md` for each piece: the search **intent** (informational / commercial / navigational / transactional), the **target query** and the answer in one sentence, the outline, the internal links (up to the pillar, across to siblings), and where it will be distributed. Without a named target query you are writing a diary entry, not a search asset. See `references/content-strategy.md` for how to read a query's intent from its phrasing.

**Step 4 — Generate the dated editorial calendar**
Turn the plan into real dates so it becomes a schedule you can hold:

```bash
python3 scripts/editorial_calendar.py --start 2026-11-03 --cadence monthly \
  --pillar "How to invoice freelance design clients" \
  --piece "Freelance invoice template that clients pay" \
  --piece "Invoice vs contract: what designers need" \
  --piece "How much to charge for a logo" \
  --piece "Late-paying client: a polite escalation script"
```

The script emits one row per scheduled piece (date, type, title, target-query placeholder, status), sorted by date. Save it to `founder/gtm/content/calendar.csv` and keep the pre-filled version in `assets/content-calendar.csv` as the shape to match. A calendar in a tool you never open is theatre — put it where your weekly review will see it.

**Step 5 — Optimise for AI answers (GEO/AEO)**
A large and growing share of searches now end without a click: the user reads the AI summary or the snippet and leaves. So you optimise to be **quoted**, not only ranked. Write the answer first, then the argument: question-shaped headings, a plain one-sentence answer an assistant can lift, concrete facts and named tools, and lists or tables a model can parse cleanly. Add accurate schema markup, ship an `llms.txt` pointing at your best citable pages, and publish platform-native content where the audience already is. Read `references/seo-and-geo.md` before finalising the brief — the mechanics matter more here than classic keyword density.

**Step 6 — Repurpose: atomise each piece**
The gain is in **atomisation, not creation**. One finished piece contains enough material for a week of distribution. Slice each into: a thread of the three most surprising points, a short video script, a newsletter section, and a genuine answer to a community question (where the answer stands on its own, no pitch). Rewrite for each surface — the same insight shaped for the room. Never cross-post identical text. Track the slices in `references/content-strategy.md`'s "one thing → many pieces" pattern.

**Step 7 — Add one engineering-as-marketing artifact**
Alongside the written program, ship one **permanent** asset that keeps earning attention without you: a free tool (a calculator, a checker, a generator), a comparison page, or a public dashboard. These appreciate with age and are durable search assets, unlike a post that peaks and fades. One good artifact per quarter is enough; quality over quantity.

**Step 8 — Verify**
Before you call a piece done, confirm all three: (a) it names a **target query or answer**, (b) it has at least one **internal link** (up to the pillar or across to a sibling), and (c) it has a **distribution step** (which thread, video, newsletter, or community it becomes). Content nobody sees is a diary. If any of the three is missing, the piece is not finished — it is drafted.

## Output format

Use `assets/content-brief.md` as the template for each piece (save to `founder/gtm/content/briefs/<slug>.md`) and `assets/content-calendar.csv` as the calendar shape. Write the program summary to `founder/gtm/content/engine.md`:

```markdown
# Content Engine — <product>

## The program
- Cadence: one pillar + <N> supporting pieces, <weekly|biweekly|monthly>
- The buyer's #1 question (the pillar): <verbatim question in their words>

## This cycle
| Date | Type | Title | Target query | Status |
|------|------|-------|--------------|--------|
| <date> | pillar | <title> | <query/answer> | planned |
| <date> | supporting | <title> | <query/answer> | planned |

## Distribution per piece
- <piece> → thread: <angle> · video: <angle> · newsletter: <angle> · community: <where>

## AI-search (GEO/AEO)
- Citable pages: <list> · schema: <Article / FAQPage / HowTo / Product> · llms.txt: <path>

## Engineering-as-marketing artifact
- <free tool / comparison page / dashboard> — <what it answers, why it stays useful>

## Boundary
- The founder approves every claim and comparison and publishes in their own voice. The agent drafts only.
```

## Gotchas

- **Publishing without a target query.** The single most common failure: a post that answers a question nobody searches for, in words nobody uses. Name the query (and the intent) in the brief *before* writing.
- **Doorway and thin pages.** Pages that exist only to funnel search traffic — near-duplicate, no unique value — are exactly what search engines demote, and they can drag your good pages down with them. The test: *would a real person be glad this page exists if they landed on it?* If no, do not ship it.
- **Content with no distribution step.** A piece that is written and never atomised, linked, or posted is a diary entry. Distribution is not an afterthought; budget as much time for it as for writing.
- **Chasing volume over specificity.** Twenty generic "we shipped it" posts lose to three specific ones — the pricing experiment, the churn investigation, the exact bug a user found, the number that moved. Specificity is the differentiator, not output.
- **Duplicating launch copy.** Launch assets (Product Hunt, Show HN, cold outreach) are one-time spikes with a different voice and audience. Do not republish them as content; the ongoing engine answers questions and compounds, it does not re-announce. See `go-to-market-launch` for the launch side.
- **SEO as set-and-forget.** AI answers keep changing the SERP: click-through falls, citations come from URLs that do not even rank top-ten, and formats shift. Re-check the plan each quarter; treat optimisation as a loop, not a one-time setup.
- **Human boundary.** Claims, comparisons ("X vs Y"), and any statistic are the founder's to approve — the skill drafts, the founder verifies and publishes. Do not invent numbers; attribute any borrowed figure loosely ("industry reporting") or omit it.

## Available scripts

- **`scripts/editorial_calendar.py`** — given a start date, a cadence, one pillar, and repeatable supporting pieces, emits a dated editorial calendar (date, type, title, target-query placeholder, status) sorted by date. Markdown by default, `--format csv` or `--json` for machines. Run `python3 scripts/editorial_calendar.py --help` for flags and the input format.

## Reference files

- **`references/content-strategy.md`** — the pillar-and-cluster model, cadence for a solo founder, choosing topics from real customer language, build-in-public specificity, and the atomisation pattern. Read at Steps 1–3 and Step 6.
- **`references/seo-and-geo.md`** — search intent, on-page basics, internal linking, programmatic-SEO cautions, and the GEO/AEO mechanics (zero-click search, AI Overviews, `llms.txt`, schema, platform-native content). Read at Step 5 before finalising the brief.
- **`assets/content-brief.md`** — the fill-in brief template (intent, target query/answer, outline, internal links, distribution). Copy to `founder/gtm/content/briefs/<slug>.md`.
- **`assets/content-calendar.csv`** — the editorial-calendar shape with sample rows, matching the script's output.

## Hand-off

When the first cycle is scheduled and the launch window arrives, pass the pillar and supporting pieces to `go-to-market-launch` for launch amplification. Once traffic is flowing, hand the per-channel numbers to `product-metrics` to trace traffic → signup → activation and tell you which piece actually earned users.
