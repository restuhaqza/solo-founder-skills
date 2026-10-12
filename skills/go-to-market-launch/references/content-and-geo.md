# Content & AI-Search (GEO/AEO)

How a solo founder runs a content engine that compounds — and gets cited by AI assistants, not just ranked by Google.

**Contents**
1. One pillar, three to four supporting pieces
2. Programmatic SEO — power and its one real trap
3. GEO/AEO — being found when the answer is zero-click
4. The mechanics: schema, `llms.txt`, platform-native content
5. Atomization — turn one piece of work into ten

---

## 1. One pillar, three to four supporting pieces

You do not need a publishing schedule that requires a team. You need a cadence you can hold alone: **one pillar piece per month, plus three to four supporting pieces**. Everything else is optional.

- **The pillar** answers your buyer's single biggest question completely — the guide they would bookmark and share. It is long, specific, and opinionated. It is also the thing every supporting piece links back to, which is how the cluster gains authority together rather than as scattered orphans.
- **The supporting pieces** are narrower: one specific sub-question each, a comparison, a template, a teardown of a real problem. Each links up to the pillar.
- **Specificity beats volume.** A build-in-public post about *the pricing experiment you ran* or *the churn investigation you did* or *the exact bug a user found* outperforms a dozen generic "we shipped" posts. Three specific posts a month is a real engine; thirty vague ones is noise.

Set the cadence to what you can sustain for a year, not what looks impressive for a month. Compounding only works if you do not stop.

## 2. Programmatic SEO — power and its one real trap

Programmatic SEO generates many pages from structured data — comparison pages, "X for Y" pages, directory entries, location or integration pages. Done well, it is a durable, low-marginal-cost acquisition asset. Done badly, it is the trap.

- **The trap: doorway pages.** Pages that exist only to funnel search traffic — thin, near-duplicate, no unique value — are exactly what search engines demote. The test is simple: *would a real person be glad this page exists if they landed on it?* If the honest answer is no, do not ship it.
- **The healthy version needs real structure.** Treat it as a small data problem: a structured dataset (the axis you vary), human-curated fragments with genuine facts per page, and a clear core page the variants hang from. If all you change between pages is a noun, you have built the trap.
- **Keep the quality bar per page**, not per template. A handful of genuinely useful generated pages beats thousands of thin ones — and the thin ones can drag the strong pages down with them.

When in doubt, generate fewer pages and make each one something you would link to unprompted.

## 3. GEO/AEO — being found when the answer is zero-click

A large and growing share of searches now end without a click — the user reads the AI summary or the snippet and leaves. Industry reporting in 2026 describes search referral traffic declining, AI Overviews cutting click-through for many queries, and a meaningful share of the URLs cited by AI assistants **not ranking in the traditional top ten at all**. That last point is the opportunity: AI search is a partly *parallel* channel, not just a reshuffling of the old one.

The design consequence is that you now optimize for **being quoted**, not only for being ranked. AI systems prefer content that is:

- **Specific** — concrete numbers, named tools, exact steps, real dates. Vague, hedged prose is hard to cite.
- **Structured** — clear question-shaped headings, short answer-first paragraphs, lists and tables the model can lift cleanly.
- **Citable** — a stable, dated, primary source with a clear author and URL, not a copy of someone else's summary.
- **Platform-native** — published where the audience already is. Video platforms and community/forum content show up disproportionately in AI citations; a good how-to video can be cited more readily than the same text on your blog.

Practical implication: write the answer *first*, then the argument. State the fact plainly in a sentence an assistant can quote, then support it.

## 4. The mechanics: schema, `llms.txt`, platform-native content

- **Schema markup** — add structured data (Article, FAQPage, HowTo, Product, BreadcrumbList as appropriate) to your pages. It gives machines an unambiguous description of what the page contains. Keep it accurate; schema that contradicts the visible page is worse than none.
- **`llms.txt`** — a small, plain-text file at your site root that points AI crawlers and agents at your best, most citable pages, in Markdown. It is an emerging convention rather than a guarantee, but it is cheap to add and it removes ambiguity about which of your pages matter.
- **Platform-native content** — do not paste your blog post into every platform. Rewrite for each surface: a video script for YouTube, a thread for X, a discussion post for a community. The same insight, shaped for the room.

## 5. Atomization — turn one piece of work into ten

The gain is in **atomization, not creation**. One solid work item — a customer call, a bug hunt, a pricing change, a launch — contains enough material for a week of distribution if you slice it.

A single work item can become:
- a pillar page (the complete write-up),
- a short video walking through it,
- a thread of the three most surprising findings,
- a newsletter section,
- a community discussion prompt,
- a template or checklist derived from it,
- and a handful of specific build-in-public posts (the number that moved, the mistake, the fix).

Keep a running "one thing → many pieces" log so a good piece of work is never published once and forgotten. Always rewrite for the surface; never cross-post the identical text.
