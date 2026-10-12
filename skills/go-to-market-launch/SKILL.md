---
name: go-to-market-launch
description: Plan and run a product launch, then stand up a compounding distribution engine so the product keeps getting found long after launch day. Use this skill whenever a solo founder or indie builder is about to launch, asks how to get the first users, wants Product Hunt or Show HN copy, needs help picking a marketing channel, wants a build-in-public, SEO, or AI-search (GEO) content plan, is drafting cold outreach, or wants consistent UTM tracking that reconciles in analytics — even if they only say "how do I get users?", "I'm launching next month", "nobody is finding my product", or "help me market this". Outputs go to founder/gtm/.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: gtm
---

# Go-to-Market & Launch

Use this skill to turn a launch from a one-day spike into an engine that keeps bringing people in. It produces a dated launch plan, the day-of assets, a content/distribution system, and clean tracking — so you can tell which channel actually works. **The agent plans and drafts; the founder sends every outbound and community message in their own voice.**

Outputs land in `founder/gtm/`. If `founder/context.md` does not exist yet, create it first (product one-liner, ICP, stage, north-star metric, stack) — every skill in this suite reads it.

## The one rule

A launch is a spike; distribution is the engine. The launch gets you the first cohort and a burst of attention, then it fades — that is expected, not failure. In 2026 the bottleneck is being *found*, not building: distribution barely got cheaper while everything around building did, so the winner is the founder who keeps showing up on one channel for a year, not the one with the best launch day.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Name the ICP and the ONE channel to go deep on first
- [ ] Step 2: Build the launch plan (copy assets/launch-plan.md)
- [ ] Step 3: Prepare launch assets (PH copy, Show HN, day-of runbook)
- [ ] Step 4: Stand up the distribution engine (pillar + supporting pieces)
- [ ] Step 5: Plan AI-search visibility (GEO/AEO)
- [ ] Step 6: Draft cold outreach (the founder sends every message)
- [ ] Step 7: Instrument every channel with UTMs (run scripts/utm_builder.py)
- [ ] Step 8: Verify — one channel, one outcome, a 60-day cut rule
```

**Step 1 — Name the ICP and the ONE channel to go deep on first**
Go deep before spreading thin. Pick the single place your *exact* buyer already gathers and you can realistically show up in weekly for 60 days — a subreddit, a niche Slack/Discord, or one social platform. Write it down as a decision, not a wish: the ICP in one sentence, the channel, the **one measurable outcome** you expect from it (e.g. "10 qualified replies", "25 activated signups", "5 booked calls"), and a **60-day cut rule** ("if this channel has not produced the outcome by <date>, I stop and move the same hours to the next one"). Choosing one channel feels risky precisely because it closes doors; a scatter of five half-efforts produces five channels you cannot read and cannot improve. See `references/channel-playbook.md` for the channel-by-channel effort/expectation/etiquette table before you commit.

**Step 2 — Build the launch plan**
Copy `assets/launch-plan.md` to `founder/gtm/launch-plan.md` and fill it in. It is a dated checklist from **T-4 weeks to T+2 weeks**: the assets to build, the list to warm, the community posts, and — critically — the days *after* launch, when most founders go quiet and the compounding actually starts. A launch without a repeatable follow-through plan is just a spike with paperwork. Time-box the build side; the launch is a distribution activity, not another feature.

**Step 3 — Prepare the launch assets**
Draft three things, using the templates: the Product Hunt listing copy (`assets/producthunt-launch.md`), a Show HN post (`assets/show-hn.md`), and a **day-of runbook**. The runbook is the part most people skip: reply to every comment in the first hours, fix the obvious bugs live while people are watching, and hand-onboard the first users rather than pointing them at a docs page. "Do things that don't scale" is a distribution tactic, not just a support one — the first cohort's goodwill is the seed of word of mouth. Aim Product Hunt at a Thursday; read the etiquette notes in `references/channel-playbook.md` before you post to any community.

**Step 4 — Stand up the distribution engine**
The launch is over in a day; this is what runs the other 364. Build one **pillar** piece per month (your best, most complete answer to your buyer's main question) plus **3–4 supporting pieces** that link back to it. Make build-in-public posts **specific** — the pricing experiment, the churn investigation, the exact bug a user found, the number that moved — because three specific posts beat thirty generic "shipped it 🚀" updates. Add **one engineering-as-marketing artifact**: a free tool, a comparison page, a public dashboard. These are permanent, appreciate with age, and keep earning attention without you present. `references/content-and-geo.md` covers the cadence and the atomization trick (turn one work item into many pieces).

**Step 5 — Plan AI-search visibility (GEO/AEO)**
A growing share of searches now end without a click, and AI assistants cite sources that are **specific, structured, and citable** — not the glossiest page. Plan for it deliberately: write answer-shaped content with clear headings and facts, add schema markup, ship an `llms.txt`, and publish platform-native content where the audience already is (video platforms and forums get cited heavily). Read `references/content-and-geo.md` before writing the content plan.

**Step 6 — Draft cold outreach (the founder sends)**
Cold, personalized outreach is uncomfortable but effective when it is genuinely personalized. The agent does the research and the drafting: for each target, find the stated need, map it to a verified capability of the product, and write a short, specific message with no hype. **The founder approves and sends every outbound message — no exceptions.** Bulk or automated sending burns the domain, the account, and the relationship; a drafted message the founder can edit and send in their own voice is the point. Use `assets/outreach-templates.md`.

**Step 7 — Instrument every channel with UTMs**
Tag every link with consistent UTM parameters so analytics reconcile across channels; inconsistent naming is how "twitter" and "X" become two sources and your numbers stop adding up. Run:

```bash
python3 scripts/utm_builder.py --base-url https://example.com/signup --campaign launch-apr-2026 \
  --channel "producthunt:producthunt/social" --channel "x-twitter:twitter/social"
```

The script normalizes names (lowercase, hyphenated), emits the tagged URLs, and warns you about duplicate or inconsistent source/medium pairs before they pollute your data. Save the mapping to `founder/gtm/tracking.md`.

**Step 8 — Verify**
Before you call the GTM plan done, confirm all three: (a) the plan names **exactly one** channel to start with; (b) that channel has **one measurable outcome** with a target and a date; (c) there is an explicit **60-day cut rule** for it. Then check that every link you plan to post carries a UTM, and that the human boundary is written down where you'll see it: *the founder sends every outbound and community message.*

## Output format

Use `assets/launch-plan.md` as the template for `founder/gtm/launch-plan.md`. For the ongoing engine, write `founder/gtm/distribution-engine.md` using this default shape:

```markdown
# Distribution Engine — <product>

## The channel decision
- ICP: <one sentence>
- Channel (ONE): <subreddit / Slack / platform>
- Why here: <where the exact buyer already is, and why you can show up weekly>
- Measurable outcome: <metric> = <target> by <date>
- 60-day cut rule: if <metric> < <target> by <date>, stop and move the hours to <next channel>

## Content cadence (monthly)
- Pillar: <the buyer's main question, answered completely>
- Supporting pieces (3–4): <list, each links to the pillar>
- Build-in-public posts (specific): <the pricing/churn/bug/number story>
- Engineering-as-marketing artifact: <free tool / comparison page / dashboard>

## AI-search (GEO/AEO)
- Citable pages: <list> · schema: <types> · llms.txt: <path>

## Tracking
- UTM map: founder/gtm/tracking.md · campaign: <utm_campaign>

## Boundary
- The founder sends every outbound and community message. The agent drafts only.
```

## Gotchas

- **Launch-as-finish-line.** Treating launch day as the goal is the most common failure. The spike is the *start* of distribution; plan the T+2 weeks to T+12 months with more care than the launch itself.
- **Identical copy across communities.** Copy-pasting the same text to Reddit, HN, and three Discords is spottable and resented; each community has norms and an audience with different context. Rewrite for each place.
- **Hacker News self-promo etiquette.** HN is not a billboard. Post only if it is genuinely interesting *on its own merits*; write a plain, honest title with no marketing voice; disclose that you built it; be present in the comments and answer the technical questions first. A hard pitch gets flagged and buried.
- **Missing UTM hygiene.** Untagged links make channels unattributable, and inconsistent source/medium strings fragment the same channel into several. Normalize before launch, not after. Run `utm_builder.py` and clear its warnings.
- **Spreading across five channels at once.** Five half-efforts give you five unreadable channels and no leverage. One channel deep, with a cut rule, then expand.
- **Human boundary.** The founder sends every outbound, DM, and community post — the agent researches and drafts. Automating the send risks the domain, the account, and the trust you are trying to build. Never auto-post on the founder's behalf.
- **Don't invent numbers.** Channel expectations are directional, not guarantees. Set your own targets from your own first data; do not quote other people's results as yours.

## Available scripts

- **`scripts/utm_builder.py`** — builds consistently named UTM-tagged URLs from a base URL, a campaign, and a list of channels, normalizing names and warning on duplicate or inconsistent source/medium pairs. Run `python3 scripts/utm_builder.py --help` for flags and the input format. Add `--json` for machine-readable output.

## Reference files

- **`references/channel-playbook.md`** — a table of channels (Product Hunt, Show HN, Reddit, niche Slack/Discord, X, LinkedIn, YouTube, newsletters, SEO) with effort, realistic expectation, and etiquette; plus the community-vs-cold-conversion contrast and HN etiquette specifics. Read before Step 1 to choose, and before Step 3 to post.
- **`references/content-and-geo.md`** — pillar + supporting cadence, programmatic-SEO cautions, GEO/AEO mechanics (zero-click search, AI Overviews, `llms.txt`, schema, platform-native content), and atomizing one work item into many. Read at Steps 4–5.
- **`assets/launch-plan.md`** — the T-4-weeks → T+2-weeks launch checklist. Copy to `founder/gtm/launch-plan.md`.
- **`assets/producthunt-launch.md`** — Product Hunt listing copy template (tagline, description, first comment, gallery notes).
- **`assets/show-hn.md`** — Show HN post template with the honesty and etiquette the community expects.
- **`assets/outreach-templates.md`** — cold outreach drafting patterns for the founder to personalize and send.

## Hand-off

When the launch is running and channels are tagged, pass the channel decision, the `utm_campaign` names, and the UTM map to the `product-metrics` skill so it can reconcile signups and activation by source — and tell you which channel is actually working.
