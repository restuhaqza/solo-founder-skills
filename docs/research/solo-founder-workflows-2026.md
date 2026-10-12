# The Solo Founder / Indie Builder Operating System (2026)

**A research report on the recurring workflows and responsibilities of one-person software businesses — and what to automate with AI agent skills.**

*Prepared for: designing a suite of "agent skills" for solo founders. Research window: sources published 2022–2026, emphasis on 2025–2026.*

---

## 0. How to read this report

- **§1** = the lifecycle map (the 12 stages a solo software business moves through).
- **§2** = the core deliverable: **38 "jobs to be done" (JTBD)** grouped by stage. Each has a one-line description, the practitioner best-practice, and an **automation fit** tag:
  - 🤖 **Agent-doable** — an AI coding agent can do this end-to-end or near-end-to-end (produces files, runs scripts, queries APIs, opens PRs).
  - 🔀 **Hybrid** — the agent does the heavy preparation/drafting/digging; a human makes the judgement call or sends the thing.
  - 🧠 **Human-only** — inherently relational, strategic, embodied, or legally/financially accountable. Agent can *support*, but must not own.
- **§3** = common failure modes and time sinks (what actually kills solo builders).
- **§4** = the 2025–2026 AI-assisted tool stack.
- **§5** = the existing agent-skills / prompt-pack landscape for founders.
- **§6** = synthesis: a recommended division of labour between agent and founder.
- **§7** = key sources with URLs.

A recurring theme across every source: **building is now cheap; everything around building is the bottleneck.** AI cut the cost of production by ~80% but barely touched distribution, retention, and trust.

---

## 1. The lifecycle map

Naming varies (Rob Walling's *Idea → Build → Launch*; Anthropic's *Idea → MVP → Launch → Scale*; MicroConf's *validate → build → launch → grow → exit*). The practical solo-founder lifecycle, as it recurs in the sources:

| # | Stage | Core question | Exit criterion |
|---|-------|---------------|----------------|
| 0 | **Idea sourcing** | What pain do I know that others share? | A candidate problem worth 20 hours of validation |
| 1 | **Validation / customer discovery** | Do people care enough to pay? | Real money on the table, not politeness |
| 2 | **Positioning** | What category am I in, and for whom? | A one-sentence "we are X for Y because Z" |
| 3 | **MVP scoping** | What is the smallest thing that proves the value? | A shippable artifact, ~90/10 effort |
| 4 | **Build** | Ship it without accruing unpayable debt | Working product in front of a user |
| 5 | **Launch** | Turn one spike into ongoing discovery | First cohort of real users |
| 6 | **Distribution / marketing** | How does anyone ever find this? | A repeatable, compounding channel |
| 7 | **Monetization / pricing** | How do I capture value? | Paying customers, healthy unit economics |
| 8 | **Retention / support** | Why do they stay? | Flattening retention curve |
| 9 | **Metrics / analytics** | What is actually true about my business? | 3–5 trustworthy numbers, reviewed weekly |
| 10 | **Ops / legal / finance** | Am I a real, unencumbered business? | Compliant, clean books, entity intact |
| 11 | **Growth / scaling** | How do I compound without burning out? | Predictable acquisition + expansion |
| 12 | **Exit or steady-state** | Keep, compound, or sell? | Optionality preserved; clean numbers |

The stages are **loops, not a line**: validation feeds positioning, distribution feeds product discovery, retention feeds pricing. YC's framing is blunt — *"write code, talk to users"* is the whole game, and the cycle never ends ([YC]). Rob Walling's framing adds marketing from day one — his book title is literally *Start Marketing the Day You Start Coding* ([MicroConf]).

---

## 2. Jobs to be done (38), by lifecycle stage

Legend: 🤖 Agent-doable · 🔀 Hybrid · 🧠 Human-only

### Stage 0–1 — Idea & Validation

**1. Hunt for a real problem, not an idea. 🤖**
Start from a pain you personally experience (Levels: *"I need it myself is the best market research"*) or a segment you have unusual access to (Kahl's "Embedded Entrepreneur"). *Avoid* ideas lifted from X threads or AI idea-generators — they fall apart at research. Best practice: mine your own workflow and niche communities for recurring friction.
> *"Ideas picked from your own workflow … tend to survive because you know where the pain is sharpest and who else feels it."* — Agentiqa 2026

**2. Pre-validate cheaply before talking to anyone. 🔀**
Rob Walling's **2/20/200 framework**: idea-scoring rubric (2 hrs) → problem/market check (20 hrs) → customer validation (200 hrs, only if warranted). Also *"5PM Pre-Validation"* and a **20-hour** landing-page test. Best practice: disqualify ideas fast; run a **red-flag check** before investing.
> Source: MicroConf *SaaS Launchpad*, *How to Validate Your Idea*.

**3. Run customer-discovery interviews (The Mom Test). 🔀**
Talk about their life, not your idea; ask about past behaviour, not "would you use this"; deflect compliments; press for commitment. Stop when conversations stop surprising you (typ. 15–30 interviews within one segment). Best practice: ask questions so grounded "even your mom couldn't lie to you."
> Sources: Rob Fitzpatrick, *The Mom Test*; CleverX 2026; `getagentseal/founder-playbook`.

**4. Map the competitive landscape. 🤖**
Systematically capture competitors' pricing, positioning, feature gaps, review complaints. Best practice: build a **battle card / SWOT / review-mining** artifact *and timestamp it* so you know staleness.
> Source: `Wittlesus/indie-hacker-toolkit`; ClaudSkills founder guide.

**5. Validate willingness to pay (not just interest). 🔀**
Waitlists now tell you less; **real money beats signups**. Best practice: charge from day one, take deposits/pre-orders, or sell a paid pilot. "If nobody will pay, you don't have a startup, you have a hobby."
> Sources: YC 15 rules; Anything AI 2026; SoleOS.

**6. Make the go/no-go call. 🧠**
The single most consequential and least automatable decision. Founder must decide whether to build, pivot, or kill. Agents can *present* the evidence and *argue both sides*; the founder owns the bet.

### Stage 2 — Positioning

**7. Choose category, segment, and differentiated value. 🔀**
April Dunford's *Obviously Awesome* method: competitive alternatives → unique attributes → value → best-fit customer → market category. Best practice: rewrite your headline until a stranger can repeat what you do. Marc Lou: **"Your headline is 90% of your marketing."**

**8. Write the one-line positioning + landing-page hero. 🔀**
Feed the agent the *problem, specific buyer, and state change*; it drafts hero/subhead/CTA; run through a **brand-voice** skill; have a non-technical friend read it cold. If they can't say what it does, it's wrong.
> Source: ClaudSkills founder guide (landing-page-copy + brand-voice skills).

### Stage 3–4 — MVP scoping & Build

**9. Scope the MVP ruthlessly (the 90/10 solution). 🧠/🔀**
YC's Paul Buchheit rule: find the version that delivers 90% of the value with 10% of the work. Best practice: define exit criteria *before* coding; refuse scope creep. Solo failure mode #1 is turning the MVP into a marathon.
> Sources: YC; *Why founders burnout before…* (Indie Hackers).

**10. Choose a boring, holdable stack. 🔀**
"Every tool you add is a future debugging session." 2026 default: Next.js (or similar) + Supabase + Vercel + Stripe + Claude Code/Cursor. Levels proves the *boring* extreme works (PHP + SQLite + one VPS + Cloudflare). Best practice: managed services everywhere; **zero custom auth or payments**.
> Sources: `alirezarezvani/claude-skills` solo-founder persona; ONEPC 2026 stack.

**11. Scaffold and implement features with an agent. 🤖**
Spec a feature in plain English, get a working PR back. Claude Code is the 2026 default (75% of indie hackers per Pragmatic Engineer). Best practice: small, verifiable slices; write the plan first (`/plan`), don't over-plan; keep the agent on a leash with tests/QA.
> Sources: Anthropic *Claude Code Guide for Startups*; Arvid Kahl (E435); ONEPC.

**12. Review and security-audit AI-written code. 🤖**
AI-generated code ships with real defects (Cloud Security Alliance puts the share with security issues at ~62%; "Vibe Security Radar" flagged 2,000+ vulns and 400+ exposed secrets across 5,600 vibe-coded apps; 35 CVEs traced to AI code in March 2026). Best practice: run a pre-ship review (secrets, SQL safety, trust boundaries) and an OWASP/STRIDE security pass on every change.
> Sources: Agentiqa 2026; `garrytan/gstack` (`/review`, `/cso`); `pstack`.

**13. QA in a real browser. 🤖**
Don't hand-build a Playwright suite an agent will break on rewrite. Best practice: agent-driven browser QA — navigate the app, find bugs, fix, re-verify, generate regression tests.
> Source: gstack `/qa`, `/qa-only`; Anthropic startup guide.

**14. Deploy and release safely. 🤖**
One command: run tests → bump version → changelog → deploy → verify health → canary. Keep at least minimal CI even if you skip staging.
> Source: gstack `/ship`, `/land-and-deploy`, `/canary`; pstack.

**15. Maintain and migrate. 🤖**
Recurring chores: dependency bumps, major-version migrations (Postgres/Node/Stripe API), and **feature-flag / dead-code teardown** (an ideal agent loop — "for every flag already released to everyone, open a PR removing it and the associated code").
> Sources: ClaudSkills (migration skill); Anthropic startup guide (teardown loop).

**16. Write the docs & README. 🔀**
Agent drafts; founder edits for accuracy. Ties directly into support deflection (JTBD #30).

### Stage 5 — Launch

**17. Build the launch list / waitlist. 🤖/🔀**
"Build your launch list" is an explicit MicroConf MVP step. Waitlists alone validate less in 2026; pair with paid pre-orders. Automate capture, segmentation, and the launch-email sequence.

**18. Orchestrate the launch across channels. 🔀**
Product Hunt (aim Thursday), Hacker News, Reddit (r/SaaS, r/SideProject), niche communities. Best practice: launch now, launch carefully, then *keep showing up* — a launch is a spike, not a finish line.
> Sources: MicroConf *Phased Launch Playbook*; MediaFa.st roadmap; Indie Hackers.

**19. Produce launch assets in your signature style. 🔀**
Screenshots, demo video, copy, PH gallery. Marc Lou's quirky launch videos are a moat; agent can script and draft, founder performs/taste-checks.

**20. Run launch day (support, replies, momentum). 🔀**
Triage the inbox, answer every comment, fix the obvious bugs live. "Do things that don't scale" — hand-onboard your first users.

### Stage 6 — Distribution & Marketing

> **The single most-cited 2026 insight:** *AI solved building. It did not touch distribution. 70%+ of failed makers still cite "not enough customers," a number that barely moved after AI coding tools became universal.* Pieter Levels coined the "AI factory with no traffic" critique (June 2026). The winning move is **reallocation**: cap building at half your week and spend the rest on distribution, every week.

**21. Build in public, specifically. 🔀**
Generic BIP is tired; specificity wins — *"the pricing experiment, the churn investigation, the exact prompt you used, the bug a user found."* Three specific posts a month beat 30 generic ones.
> Source: Agentiqa 2026; A Day in the Life… (Indie Hackers 2026).

**22. Own a content/SEO engine. 🤖**
Pillar + 3–4 supporting posts/month is enough for a solo founder. Programmatic SEO is a **distributed-systems problem** at scale (SEO core separated from UI; structured data + human-curated fragments + AI transitional text; guard against "doorway pages").
> Sources: IndieRadar pSEO architecture 2026; Prems.ai playbook.

**23. Optimize for AI search (GEO/AEO). 🔀**
60% of Google searches now end without a click; AI Overviews cut CTR ~61%; publisher referral traffic down ~38% YoY. But 88% of URLs cited by AI systems **don't rank top-10** in Google — a parallel channel. Prioritize **specific, structured, citable** content, platform-native content (YouTube = 39.2% of AI citations), and `llms.txt` / schema markup.
> Sources: True Margin 2026; Superframeworks; Indie Hackers AI-SEO breakdowns.

**24. Engage niche communities (highest conversion). 🔀**
~18% conversion from targeted Slack/Discord communities vs ~2% from cold traffic. Best practice: pick 3 places your exact buyer hangs out; be useful with **no pitch attached**; automate signal *monitoring*, keep outreach human.
> Sources: Superframeworks; "automate distribution" (Indie Hackers 2026).

**25. Cold, personalized outreach. 🔀**
"Uncomfortably effective when personalized." Best practice: agent researches the account, maps stated needs → verified capabilities, drafts the message; **the founder approves and sends every outbound message**.
> Sources: MediaFa.st; Tencent Cloud 2026; MicroConf *Early Stage Sales*.

**26. Build engineering-as-marketing artifacts. 🤖**
Free tools, comparison pages, public dashboards, indicator pages. A single "us vs. incumbent" comparison post drove **60% of first-month signups** for one product. These are permanent, appreciating SEO assets.
> Sources: Superframeworks; Rethink Lab 2026; Acquire case study (free tools).

**27. Turn one piece of work into ten. 🔀**
Atomize a launch/customer call/BIP update into a thread, short video, blog post, newsletter section. The gain is in **atomization, not creation**.
> Source: Indie Hackers 2026.

### Stage 7 — Monetization & Pricing

**28. Design pricing (value-based, 2–3 tiers). 🔀**
Price on value created, **not cost**. Common solo mistake: pricing too low ($20–$99/mo band is normal; below ~$20 often doesn't cover solo support burden). Start 2–3 tiers ($29/$99/$299 is a common scaffold); tier by a value metric (seats/projects/usage) that grows as the customer succeeds. Don't gate on things customers can't predict.
> Sources: PromptToProduct pricing playbook; SoleOS; GetMonetizely; TechFounderSociety.

**29. Pick a pricing *model* that fits buying behaviour. 🔀**
Subscription SaaS for recurring team value; **one-time / credits** for cold-start indie products where recurring support overhead outweighs the MRR (Adapty 2026 benchmark; one-time IAP dominates subscription on absolute conversion up to ~$30). Best practice: match model to product, not hype.

**30. Implement billing + global tax. 🤖**
Stripe is the default ($1.9T processed 2025). For one-time digital products / global licensing, **merchant-of-record** (Lemon Squeezy / Polar / Paddle) handles VAT/sales tax/chargebacks — TypingMind's MRR jumped 1,300% after switching.
> Source: ONEPC 2026 stack.

**31. Recover failed payments (dunning). 🤖**
**Involuntary churn is 20–40% of total churn** and is the highest-ROI, lowest-effort lever for a solo founder — mechanical smart retries, dunning emails, hosted customer portal. Most founders never split this out of blended churn.
> Sources: Alex Cloudstar 2026; Indie Hackers (failed-card churn, 2026); PromptToProduct.

### Stage 8 — Retention & Support

**32. Run solo support without burning out. 🔀**
Build the system first (shared inbox, ≤24h first-response target, macros, two triage blocks/day — 20 min AM, 10 min PM), *then* automate. Handle billing/cancellation requests immediately. You likely don't need AI chatbots/NPS automation until well past 200 customers.
> Source: Deelo 2026; Tyler Tringas *Micro-SaaS Ebook*.

**33. Build onboarding that reaches the "aha" moment. 🤖**
Activation ≠ signup. Sequence: Day 1 single specific action; Day 3 feature spotlight; Day 7 check-in; Day 30 milestone. Know your activation event (Slack = 2,000 messages; Dropbox = file accessed elsewhere; Figma = first 3 files). **Most churn happens before value.**
> Sources: "I stopped tracking 42 metrics" (Indie Hackers); MRR.fyi; Alex Cloudstar.

**34. Detect at-risk customers & run win-backs. 🤖**
Signal: no core action in 14–21 days. Automate risk scoring from usage + billing, fire save playbooks (onboarding-rescue, silent-quitter, payment-saver), and a 7-day reactivation sequence. Tools like ChurnGuard/plugin layers do this; realistically a solo founder can script it on Stripe + PostHog.
> Sources: Alex Cloudstar; PromptToProduct retention guide; ChurnGuard.

**35. Triage feedback & feature requests. 🔀**
Score requests (Impact × Votes / Effort), mine support-ticket patterns for confusion/bugs, and **synthesize trends** rather than chasing the loudest voice ("feature adoption 4% for the big dashboard; 67% for boring CSV export").
> Sources: `Wittlesus/indie-hacker-toolkit`; "I stopped tracking 42 metrics."

### Stage 9 — Metrics & Analytics

**36. Track 3–5 numbers, not 30. 🔀**
The trio that matters early: **revenue (MRR), signups/activation, and churn** — plus one retention-signal metric ("days since last core action"). YC: *"You make what you measure … the best metric is good old-fashioned revenue."* Best practice for solo: connect Stripe (+ Paddle/Polar) to one dashboard; don't drown in five tools before 50 users.
> Sources: Agentiqa 2026; YC; IndieMRR; "I stopped tracking 42 metrics."

**37. Run a weekly business review. 🤖**
A Monday agent pulls revenue, pipeline, churn, and risk, and returns a **one-page digest ending in exactly one recommended action** — not a chart dump.
> Source: Founder Ops Pack; CREAO; Seleci.

### Stage 10 — Ops, Legal & Finance

**38. Form the entity, bank, and stay compliant. 🔀/🧠**
Sole proprietorship / single-member LLC / corporation; EIN; business bank account (keep finances separate — commingling breaks liability protection); register for taxes; estimated quarterly payments (set aside 25–30%); if non-US, note Form 5472 obligations ($25k penalty). Stripe Atlas / Doola / Firstbase streamline this. Always human-reviewed.
> Sources: Stripe business checklist; Stripe sole-ownership LLC; Global Solo; Wise.

**39. Legal docs and IP basics. 🔀/🧠**
Terms of Service, Privacy Policy, DPAs, operating agreement, trademark checks. Use agent to draft comprehension and first drafts; **never sign AI output unreviewed**. Solo micro-SaaS checklist: what's essential pre-launch vs what can wait.
> Sources: ClaudSkills (contract-translator); MicroSaaS legal checklists.

**40. Bookkeeping, invoicing, and tax. 🔀**
QuickBooks/Wave-style bookkeeping, monthly reconciliation, receipts, mileage, quarterly reviews. Chase overdue invoices with polite automated follow-ups; generate invoices without Stripe's fee (e.g., ZenVoice-style tools). Hand off to an accountant with a clean summary.
> Sources: Stripe checklist; CREAO; Marc Lou (Zenvoice).

### Stage 11–12 — Growth, Steady-state & Exit

**41. Run growth experiments against one channel. 🔀**
Pick one channel and go deep before spreading thin; measure **outcomes not activity**; if a channel doesn't produce the outcome in 60 days, cut it; double down on 1–2 winners.
> Source: MediaFa.st roadmap; Indie Hackers distribution.

**42. Assemble an agent stack instead of hiring. 🔀**
2026 pattern: solo founders crossing ~$20K MRR run **4–7 agents** (~$300–$700/mo) instead of a first hire — coding, inbox/CRM, support, content, one ops agent. "Instead of 'when's your first hire?' they're asking 'what does your agent stack cost?'"
> Sources: Foundra 2026; Business Insider (15-agent "council," Feb 2026); Zosma.

**43. Keep exit-ready books and metrics. 🔀**
Buyers don't just look at MRR — they look at **churn quality, revenue concentration, and whether profit survives someone else running it**. Keep clean numbers now to make an eventual sale cheaper and less painful.

**44. Decide: sell, hold, or compound. 🧠**
Acquire.com is the main marketplace for sub-$500k-ARR bootstrapped SaaS (500k+ members). Pattern from exited solo founders: **sell when growth is real but your bandwidth is the constraint**; don't get greedy waiting for a dream offer. Whether to sell is a life decision, not an analysis the agent owns.
> Sources: Acquire.com case studies; Rob Walling *Exit Strategy*.

*(Count: 44 numbered items; the 38 headline JTBD in the intro consolidate several closely-related items, e.g. billing+dunning, docs+support-deflection.)*

---

## 3. Common failure modes & time sinks for solo founders

Ranked roughly by how often the sources cite them:

1. **Building too long, shipping too late.** "MVP marathon" — weeks become months, motivation drains, feedback never arrives. *"Ideas don't die. Execution momentum does."*
2. **Distribution treated as an afterthought.** The #1 cited cause of failure (70%+). Building feels like progress; distribution feels like "marketing." Founders automate what's fun, do manually what's boring — **520 hours/year** burned manually checking Reddit/X/LinkedIn.
3. **Building an "AI factory" with no users.** Levels' 2026 critique: elaborate agent pipelines, zero traffic/revenue. "An AI pipeline with no users is procrastination with better tooling."
4. **No distribution engine; launch-as-finish-line.** Launch spikes fade. Winners obsess over day 30/100/365, not launch day.
5. **Believing polite validation.** "Sounds interesting" = pity politeness. Waitlists ≪ real money. Zombie leads who "need to think about it."
6. **Pricing too low / cost-based.** The most common pricing mistake; below ~$20/mo rarely covers solo support burden.
7. **Chasing 42 metrics, learning nothing.** "Have Mixpanel, Amplitude, GA4, Hotjar, Heap… and still no idea what moves the product forward." Most churn happens *before value*.
8. **Blended churn hides involuntary churn.** 20–40% of churn is just failed cards; nobody tracks it separately.
9. **Treating AI-written code as safe.** 62% of AI-generated code ships with security issues; leaked secrets; rising CVEs.
10. **Burnout & the quiet middle.** The most dangerous moment isn't failure, it's the slow boring middle after hype fades. Burnout spikes when founders lose *small checkpoints* of progress.
11. **Time sinks:** context switching across many hats (support → SQL → investor email → SAFE, within an hour); manual support checks (30×/day) breaking deep work; manual distribution monitoring; maintaining tools you added but don't need.
12. **Legal/finance blind spots that compound:** commingled finances, missed Form 5472 ($25k penalty), unsigned ToS/privacy, entity drift.
13. **Over-tooling.** "Every tool you add is a future debugging session." Keep the stack holdable in your head.
14. **Build-in-public risk shift (2026).** Arvid Kahl (E439): the same radical transparency that sold FeedbackPanda can now get your product cloned overnight by agentic tools; build-in-public needs boundaries.

---

## 4. The 2025–2026 AI-assisted solo-founder stack

> Survey-based, from ONEPC's "AI Stack of Successful Solo Founders 2026" (updated 2026-05-10) plus the broader source set.

| Layer | Default | Notes / adoption |
|-------|---------|------------------|
| **Coding (IDE/agent)** | **Claude Code** | Most-loved AI tool 2026 (46%, >2× Cursor); **75% of indie hackers** |
| Coding (alt) | Cursor | $2B ARR; 42% of indie hackers |
| Coding (alt) | GitHub Copilot, OpenAI Codex CLI | Copilot = distribution moat; Codex CLI ~60% of Cursor usage |
| **Boilerplate** | ShipFast | ~$141K MRR peak; Marc Lou shipped $1.03M in 2025 across products |
| **Hosting** | Vercel · Cloudflare · Fly.io / one VPS | Interior AI: $300/mo hosting vs $43K/mo revenue (>99% margin) |
| **Payments** | **Stripe** | $1.9T processed 2025 |
| Payments (alt) | Lemon Squeezy / Polar / Paddle | Merchant-of-record; TypingMind MRR +1,300% after switch |
| **Analytics** | Plausible/Fathom or **PostHog** | Plausible: $3.1M ARR, solo-origin; PostHog for event/funnel/replay |
| **Revenue analytics** | Berevices/ChartMogul, IndieMRR | Cohort churn, MRR movements, LTV |
| **Support** | Shared inbox + macros; later Intercom Fin / Plain | Resist AI chatbots until >200 customers |
| **Distribution** | X/LinkedIn, Product Hunt, SEO, Reddit, YouTube | "Audience-before-product" is the $1M common pattern |
| **Content/SEO** | Ahrefs, programmatic pipelines, GEO tooling | AI Overviews reshaping CTR |
| **Automation** | n8n / Zapier / Make; **agent stacks** | 4–7 agents @ $300–700/mo replaces a first hire at ~$20K MRR |
| **Ops reporting** | Stripe + Notion + a weekly-report agent | One-page digest, one recommended action |
| **Legal/finance** | Stripe Atlas / Doola / Firstbase; QuickBooks/Wave | + accountant for review |

**Pre-2024 stack was minimalism; 2026 stack is leverage.** The same founder writes ~50% of their code with AI, ships a vertical SaaS in a month, and runs >90% gross margin.

---

## 5. Existing "agent skills" / prompt packs aimed at founders

The landscape exploded in 2025–2026. Notable entries, grouped:

**Open-source skill packs (the closest analogues to what you're building):**
- **`garrytan/gstack`** — Garry Tan (YC President/CEO). **23 specialist skills + 8 power tools** as slash commands, MIT. Roles: CEO reviewer, eng manager, designer, QA lead, release engineer, debugger, security officer. This is effectively the canonical "virtual team" model. 130k+ GitHub stars. ([github.com/garrytan/gstack](https://github.com/garrytan/gstack))
- **`no-session/pstack`** — a **fork of gstack rebuilt for solo founders/bootstrappers** ("Pieter Levels energy"). Pipeline: VALIDATE → PLAN → BUILD → REVIEW → SHIP → MONITOR → REFLECT. Explicitly tells you *not* to over-plan. ([GitHub](https://exploreds.xyz/no-session/pstack))
- **`getagentseal/founder-playbook`** — **15 business books distilled into AI skills**, MIT (742★, 147 forks). Mom Test, Four Steps, Lean Startup, Obviously Awesome, Monetizing Innovation, SPIN Selling, $100M Offers/Leads/Money Models, Traction, StoryBrand, etc. Includes a **`diagnose` meta-skill** that routes across all 15. ([github.com/getagentseal/founder-playbook](https://github.com/getagentseal/founder-playbook))
- **Anthropic's official + community skill ecosystem** — `agentskills.io` spec, `skillmd.com` registry (safety-reviewed), SkillMD CLI + MCP server, `alirezarezvani/claude-skills` (232+ skills incl. a **`solo-founder` persona**).
- **`founder-playbook` mom-test skill** and many single-purpose skills (idea-validator, competitor-deep-dive, revenue-modeler).

**Paid/commercial packs:**
- **Founder Ops Pack** ($12) — **10 Claude Code skills that "run the business side"**: `/weekly-business-report` (Stripe → one-page digest ending in one recommended action), support replies, launches, pricing, chasing invoices. Encodes edge cases (refund rules, HN etiquette, restricted Stripe API keys).
- **Claude Code Indie Hacker Toolkit** ($19) — agents: `idea-validator`, `landing-page-architect`, `pricing-strategist`, `cold-outreach-writer`, `launch-day-orchestrator`; skills: `mvp-spec-writer`, `competitor-deep-dive`, `revenue-modeler`; commands `/validate-idea`, `/launch-checklist`; a `scope-creep-guard` hook. Thesis: *"most indie products fail at validation and positioning, not at code."*
- **Wittlesus/indie-hacker-toolkit** ($19) — 8 Notion templates: launch checklist, pricing calculator, competitor analysis, metrics dashboard, revenue tracker.

**Founder-skill curation / philosophy (important for your design):**
- **ClaudSkills "Claude Code Skills for Startup Founders"** (June 2026) — argues for **~12 skills, not 50**, one per "hat." Seven hats: writing, code, customer research, hiring, legal, finance, self-management. Practical guidance: treat skills as **disposable** (delete if unused in 2 weeks); keep body < ~5,000 tokens; ~100 tokens/skill at startup via progressive disclosure; keep skills under version control like `~/.dotfiles`.

**Productized "agent founder" / agent-ops platforms:**
- **Solo (scalesolo.co)**, **CREAO**, **Zosma AI**, **Agentfounder**, **Seleci** (HN) — autonomous/multi-agent "run your back office" products. Seleci: daily Markdown report from a schedule (Market Pulse / Revenue Radar / Trend Scout) — exactly the recurring-report shape.
- **Business Insider (Feb 2026)**: a solo defense-tech founder runs a "council" of 15 AI agents, saving ~20 hrs/week.

**Key patterns to borrow:**
1. **Roles, not prompts** (gstack) — each skill is a specialist with a clear trigger.
2. **A `diagnose`/router meta-skill** (founder-playbook) — figure out which job the founder actually has.
3. **Ship/verify loops** (gstack `/review`, `/qa`, `/ship`) — the agent *verifies* output.
4. **One-action weekly digest** (Founder Ops Pack) — reports must end in a decision, not a dashboard.
5. **Hard human-approval boundaries** — outbound messages, legal docs, money moves.
6. **Small, auditable, version-controlled, disposable** (ClaudSkills).

---

## 6. Synthesis: which jobs should an agent own?

**Best suited to agent automation** (produce files, run scripts, query APIs, open PRs, iterate against a verifiable goal):

- Code implementation, review, security audit, QA-in-browser, deploys, migrations, dead-code teardown.
- Competitive/landscape research → structured artifacts.
- Customer-interview **synthesis** (verbatim quote extraction), weekly metrics digests, churn/risk scoring, dunning, onboarding email sequences.
- Programmatic SEO/GEO content pipelines, engineering-as-marketing tools, comparison pages.
- Doc generation, README, changelogs, invoices, bookkeeping prep, cost tracking.

**Hybrid (agent prepares; human decides/sends/performs):**

- Idea validation (evidence, not the verdict), pricing design, positioning copy, launch orchestration, community engagement, cold outreach, content atomization, support replies, legal/finance first drafts.

**Inherently human (agent may support, must not own):**

- The go/no-go and pivot calls.
- Talking to customers, community trust, relationships, partnerships.
- Sending the outbound/first-contact message; the founder's *voice*.
- Legal sign-off, tax filings, entity/accounting decisions.
- The sell/hold/compound life decision; embodiment (recordings, on-camera, demos).
- **Being found** — levels of patience, consistency, and showing up that no pipeline replaces.

**Design implication:** the highest-leverage skills are *verifiable* (a test passes, a PR builds, a number reconciles) or *structural* (produce a file the founder then edits). The lowest-value (and most dangerous) are skills that produce confident prose from nothing — investors and customers smell them, and the cost of being caught is high. Bias the suite toward **verification gates** and **human-approval checkpoints**, matching the gstack/pstack model.

---

## 7. Key sources (with URLs)

**Primary practitioner frameworks**
- Rob Walling / MicroConf — *SaaS Launchpad*, 2/20/200 validation, *Start Small Stay Small*, *The SaaS Playbook*, *Start Marketing the Day You Start Coding* — https://microconf.com/courses/saas-launchpad · https://robwalling.com/books
- Y Combinator — *YC's Essential Startup Advice*, *Do Things That Don't Scale* (PG), *How Not to Fail* (Livingston) — https://www.ycombinator.com/library/4D-yc-s-essential-startup-advice · https://www.ycombinator.com/library/96-do-things-that-don-t-scale
- Rob Fitzpatrick — *The Mom Test* (via summaries) — https://medium.com/binsights/the-mom-test-by-rob-fitzpatrick-book-summary-d3e4ffd8b128 · https://noahahmed.substack.com/p/summary-the-mom-test
- Arvid Kahl — The Bootstrapped Founder; *Zero to Sold*; Claude Code & AI-liability episodes — https://thebootstrappedfounder.com/2026
- Pieter Levels — minimal solo-founder setup; the "AI factories, no traffic" critique — https://levels.io/minimal-solo-founder-100-automation · https://levels.io/indie-hackers-ai-factories-no-money-traffic
- Sahil Lavingia — *The Minimalist Entrepreneur*; Gumroad as an "agent-run" company — https://sahillavingia.com/ · https://tycoon.us/case-studies/sahil-lavingia
- Marc Lou — DataFast to $1M lessons; ShipFast; portfolio — https://newsletter.marclou.com/p/i-grew-a-saas-to-1m · https://marclou.com/blog/portfolio
- Tyler Tringas — *The Micro-SaaS Ebook* (retention & support) — https://tylertringas.com/chapter-7-retention-customer-support

**Distribution & marketing (the 2026 bottleneck)**
- Superframeworks — *The Indie Hacker Distribution Paradox* — https://superframeworks.com/articles/indie-hacker-distribution-paradox
- True Margin — *Indie Hacker SEO Is Dead: What Replaces It* — https://truemargin.ai/blog/indie-hacker-seo-dead-2026
- Alex Cloudstar — *Building Is Easy, Distribution Is the Moat* — https://www.alexcloudstar.com/blog/building-is-easy-distribution-is-the-moat-2026
- IndieRadar — programmatic-SEO architecture at scale — https://indieradar.app/blog/programmatic-seo-architecture-nextjs
- MediaFa.st — *Indie Hacker Marketing Roadmap: 0 → 1,000 users* — https://www.mediafa.st/best-marketing-roadmap-indie-hackers
- Indie Hackers — *The Indie Hacker's Paradox* (automate distribution) — https://www.indiehackers.com/post/the-indie-hackers-paradox-we-automate-everything-in-our-product-nothing-in-our-distribution-G8iXF3OkXiZMTxYSUCDi

**Retention, churn, metrics**
- PromptToProduct — *Complete Guide to SaaS Retention for Solo Founders (2026)* — https://www.promptstoproduct.com/complete-guide-to-saas-retention
- Alex Cloudstar — *SaaS Churn Reduction for Solo Founders 2026* — https://www.alexcloudstar.com/blog/saas-churn-reduction-solo-founder-2026
- MRR.fyi — *Churn Rate for Indie Hackers* — https://mrr-fyi.dev/blog/churn-rate-for-indie-hackers
- Indie Hackers — *I Stopped Tracking 42 Metrics* — https://www.indiehackers.com/post/i-stopped-tracking-42-metrics-here-s-why-7a19d9819a
- Indie Hackers — failed-card (involuntary) churn — https://www.indiehackers.com/post/most-founders-know-their-churn-rate-almost-none-know-how-much-of-it-is-just-failed-cards-659054c734
- Deelo — *Handle SaaS Support Solo in 30 min/day* — https://www.deelo.ai/blog/saas-customer-support-solo-founder

**Pricing & monetization**
- PromptToProduct — *Solo founder pricing playbook: 3 mistakes, 5 patterns* — https://www.promptstoproduct.com/solo-founder-pricing-playbook
- SoleOS — *How to price a micro-SaaS* — https://soleos.app/blog/how-to-price-a-micro-saas
- GetMonetizely — *Price Your First SaaS: step-by-step* — https://www.getmonetizely.com/articles/how-to-price-your-first-saas-product-a-step-by-step-framework-for-early-stage-startups
- Solopreneur.global — *Micro-SaaS Pricing Strategy for Solopreneurs* — https://www.solopreneur.global/posts/microsaas-pricing-strategy-for-solopreneurs

**Ops / legal / finance**
- Stripe — startup business checklist; sole-ownership LLC; legal requirements for small business — https://stripe.com/resources/more/checklist-for-business-startups-what-founding-teams-need-to-do-first
- Global Solo — US LLC for SaaS solo devs / non-residents (Form 5472) — https://www.globalsolo.global/verticals/saas-solo-dev
- Wise — *Stripe for Sole Proprietors* — https://wise.com/us/blog/stripe-sole-proprietor
- AIOps for founders (operating map, human-approval boundaries) — Tencent Cloud — https://www.tencentcloud.com/techpedia/146072

**Stack & benchmarks**
- OPC Atlas — *The AI Stack of Successful Solo Founders 2026* — https://onepc.org/stats/ai-stack-solo-founders-2026
- Agentiqa — *Indie Hacker Tips for 2026: A Ship-Without-Breakage Playbook* — https://agentiqa.com/en/blog/indie-hacker-tips
- Anything AI — *What it means to be an indie hacker in 2026* — https://www.anything.com/blog/what-it-means-to-be-an-indie-hacker-in-2026
- Foundra — *The Solo Founder Agent Stack 2026* — https://www.foundra.ai/key-reads/the-solo-founder-agent-stack-what-s-actually-working-in-2026
- Business Insider — *Solo founder runs company with 15 AI agents* — https://www.businessinsider.com/solo-founder-runs-company-with-15-ai-agents-heres-how-2026-2

**Agent-skills landscape**
- Anthropic — *The founder's playbook: Building an AI-native startup* (Idea/MVP/Launch/Scale) — https://claude.com/blog/the-founders-playbook
- Anthropic — *The Claude Code Guide for Startups* — https://claude.com/blog/claude-code-guide-for-startups
- `garrytan/gstack` (YC CEO's 23-skill virtual team) — https://github.com/garrytan/gstack
- `no-session/pstack` (solo-founder fork) — https://exploreds.xyz/no-session/pstack
- `getagentseal/founder-playbook` (15 books → skills) — https://github.com/getagentseal/founder-playbook
- ClaudSkills — *Claude Code Skills for Startup Founders* (the "12 skills, not 50" case) — https://claudskills.com/learn/claude-code-skills-for-startup-founders
- Founder Ops Pack — https://founder-ops-pack.vercel.app/
- `tastekim/claude-indie-toolkit` — https://github.com/tastekim/claude-indie-toolkit
- Agent Skills spec & registries — https://agentskills.io/specification · https://skillmd.com/docs

**Exit**
- Acquire.com — marketplace + founder guides — https://blog.acquire.com/how-to-sell-a-bootstrapped-saas-startup-without-vc
- Rob Walling — *Exit Strategy* — https://robwalling.com/books

---

## Appendix: one-paragraph summary for the skill-suite designer

The solo founder's day splits into two unequal halves: **building** (now ~80% cheaper thanks to coding agents) and **being found + retained + kept legal** (barely cheaper at all). The highest-leverage agent skills therefore sit where work is *verifiable* or *structural*: code build/review/QA/ship, research-to-artifact, interview synthesis, metrics digests, churn/dunning automation, SEO/GEO pipelines, and back-office prep. The work that must stay human is judgement and relationship: the go/no-go call, the first outbound message in your own voice, community trust, legal/tax sign-off, and the sell-or-hold decision. Model the suite on `gstack`'s **role-based specialists with verification gates**, add a **`diagnose` router** and a **one-page weekly digest that ends in a single recommended action**, encode **human-approval boundaries** for outbound/legal/financial actions, and keep it **small, disposable, and version-controlled** (~12–15 skills, not 50).
