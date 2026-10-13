# SEO & GEO/AEO

The mechanics of being found — in classic search and, increasingly, in the AI
answers that now end a growing share of searches before anyone clicks.

**Contents**
1. Search intent — the first thing to get right
2. On-page basics
3. Internal linking
4. Programmatic SEO — power and its one real trap
5. GEO/AEO — being found when the answer is zero-click
6. The mechanics: schema, `llms.txt`, platform-native content

---

> For the broader, launch-oriented treatment of these topics see
> `go-to-market-launch/references/content-and-geo.md`. This file goes deeper on the
> ongoing program: the per-piece mechanics and the loop you keep running.

## 1. Search intent — the first thing to get right

Before optimising anything, name the **intent** behind the query — what the searcher
actually wants to do. The four useful buckets:

- **Informational** — "how do I…", "what is…". They want to understand. Answer
  first, then explain.
- **Commercial** — "best…", "X vs Y", "alternatives to…". They are comparing options
  and are close to a decision. Be specific and honest about trade-offs.
- **Navigational** — they are looking for a specific brand or page. Rarely your
  opportunity unless it is your brand.
- **Transactional** — "buy", "download", "pricing". They want to act. Remove friction.

Match the format to the intent, not to your preference. A commercial query wants a
comparison table and a clear verdict; an informational one wants a definition up
top and a step list below. The most common mismatch is a founder writing a
sales-flavoured page for an informational query, or a sprawling essay for someone
who wanted a one-line answer.

Read intent from the phrasing: "vs", "best", "how to", "cost", "template". The
shape of the query tells you the shape of the page.

## 2. On-page basics

These are the floor, not the strategy — do them so nothing else is wasted:

- **One page, one primary query.** Each piece owns one target query. If you cannot
  name it in one line, the page is trying to do too much; split it.
- **Title and H1 aligned with the query.** Use the buyer's phrasing, not jargon.
- **Answer-first opening.** State the answer to the query in the first paragraph, in
  a sentence someone could quote. The argument and detail follow.
- **Question-shaped headings.** H2/H3s phrased as the sub-questions people ask make
  the page scannable for humans and parseable for machines.
- **Concrete facts over adjectives.** Named tools, exact steps, real numbers, dates.
  Hedged, vague prose is hard to trust and hard to cite.
- **A clear author and a date.** Machine readers and humans both weight a page that
  says who wrote it and when.
- **Mobile-clean and fast.** A page that loads slowly on a phone loses before it is
  read.

## 3. Internal linking

Internal links are how a cluster becomes an authority instead of a pile of pages.

- Every **supporting piece links up to the pillar** — usually in the first screen,
  contextually ("this is part of our complete guide to X").
- The **pillar links down** to each supporting piece where the sub-topic appears.
- **Siblings link across** when a piece genuinely helps understand another (the
  comparison links to the cost guide).
- Use **descriptive anchor text**, not "click here" — the anchor tells the reader
  and the crawler what the target is about.

The rule of thumb: if a reader finishing a supporting piece has an obvious next
question, there should be a link to where it is answered. Orphan pages — no inbound
internal links — are treated as unimportant, because you have said they are.

## 4. Programmatic SEO — power and its one real trap

Programmatic SEO generates many pages from structured data: comparison pages, "X
for Y" pages, directory entries, integration or location pages. Done well it is a
durable, low-marginal-cost asset; done badly it is the trap.

- **The trap: doorway pages.** Pages that exist only to funnel search traffic —
  thin, near-duplicate, no unique value — are exactly what search engines demote,
  and a run of them can drag your strong pages down with it. The test is plain:
  *would a real person be glad this page exists if they landed on it?* If not, do
  not ship it.
- **The healthy version needs real structure.** Treat it as a small data problem: a
  structured dataset (the axis you vary), human-curated fragments with genuine
  facts per page, and a clear core page the variants hang from. If the only thing
  that changes between pages is a noun, you have built the trap.
- **Keep the quality bar per page**, not per template. A handful of genuinely
  useful generated pages beats thousands of thin ones.

At real scale, programmatic SEO becomes a small systems problem: separate the data
and template layer from the app, keep the curated facts in the data, and rate-limit
how fast you ship variants so quality does not slip. For a solo founder, the
practical version is: generate **fewer** pages and make each one you would link to
unprompted.

## 5. GEO/AEO — being found when the answer is zero-click

Generative-engine optimisation (GEO), also called answer-engine optimisation (AEO),
is optimising to be **quoted in an AI answer**, not only ranked in a list of links.

Industry reporting in 2026 describes a large and growing share of searches ending
without a click, AI Overviews cutting click-through on many queries, and publisher
referral traffic declining year over year. The same reporting notes that a
meaningful share of the URLs cited by AI assistants do **not** rank in the
traditional top ten at all. That last point is the opportunity: AI search is a
partly *parallel* channel, not just a reshuffling of the old one. (Treat these
figures as directional signals from industry reporting, not as fixed truths — they
move, and you should re-check them.)

What AI systems tend to prefer, and therefore what to build:

- **Specific** — concrete numbers, named tools, exact steps, real dates. Vague,
  hedged prose is hard to cite.
- **Structured** — question-shaped headings, short answer-first paragraphs, lists
  and tables a model can lift cleanly.
- **Citable** — a stable, dated, primary source with a clear author and URL, not a
  copy of someone else's summary. Be the origin, not the echo.
- **Platform-native** — published where the audience already is. Video platforms
  and community/forum content show up disproportionately in AI citations; a good
  how-to video can be quoted more readily than the same text on your blog.

The practical move is to **write the answer first, then the argument**: state the
fact plainly in a sentence an assistant can quote, then support it with detail. That
one change to how you open a piece does most of the AEO work.

## 6. The mechanics: schema, `llms.txt`, platform-native content

- **Schema markup** — add structured data (Article, FAQPage, HowTo, Product,
  BreadcrumbList as appropriate) so a machine gets an unambiguous description of the
  page. Keep it accurate: schema that contradicts the visible page is worse than
  none.
- **`llms.txt`** — a small plain-text file at your site root that points AI crawlers
  and agents at your best, most citable pages, in Markdown. It is an emerging
  convention rather than a guarantee, but it is cheap and it removes ambiguity about
  which pages matter.
- **Platform-native content** — do not paste your post into every platform. Rewrite
  for each surface: a video script for YouTube, a thread for X, a discussion answer
  for a community. The same insight, shaped for the room.

**The loop, not the setup.** SEO and GEO are not set-and-forget: AI answers keep
changing which formats get surfaced and which sources get cited, so revisit this
quarterly. Check what your pieces are being cited for, update the answer-first
paragraphs when the question's wording shifts, and retire pages that have become
thin. Optimisation is a recurring pass over the program, not a launch-day task.
