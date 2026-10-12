# Boring Stack — Build vs Buy vs No-Code

**Contents**
1. The rule
2. The decision matrix
3. The 2026 default stack
4. The boring extreme
5. Component-by-component defaults
6. Stack red flags

---

## 1. The rule

**Every tool you add is a future debugging session.** A solo founder is the only person who will ever page themselves at 2am, so the stack's job is to have as few moving parts as possible while still shipping the core loop. "Boring" is not a lack of ambition — it is the choice that keeps the *uninteresting* parts uninteresting, so your attention stays on the one thing that is genuinely yours.

Two consequences follow. First, **prefer managed services over anything you host and operate yourself** — you are buying back maintenance time, which is the scarcest resource you have. Second, **never hand-roll what is a commodity**: authentication, payments, email delivery, and file storage are solved problems with security and compliance tails you do not want to own.

## 2. The decision matrix

Walk each component in the v1 spec and pick the leftmost option that works:

| Component | Buy (managed service) | No-code / existing tool | Build (only if…) |
| :-- | :-- | :-- | :-- |
| **Auth, login, sessions** | Managed auth provider | — | Never for v1 |
| **Payments, subscriptions, tax** | Stripe / merchant-of-record | — | Never for v1 |
| **Database** | Managed Postgres (e.g. Supabase) | Airtable / Google Sheets for a throwaway | Only if access patterns are genuinely exotic |
| **Hosting, deploy, TLS** | PaaS (e.g. Vercel) | Static host | Only for hard runtime constraints |
| **Transactional email** | Email API | — | Never for v1 |
| **Scheduling, booking** | — | Calendly-style link | Only if scheduling *is* the product |
| **Forms, surveys** | — | Form tool | Only if the form is the product |
| **Analytics** | Managed product analytics | A spreadsheet | Only for a metric the tools cannot express |
| **Support inbox** | Shared inbox + macros | — | Never for v1 |
| **The core action** | — | — | **Yes — this is your differentiation** |

The last row is the point of the whole table: **you build exactly one thing, the core action**, and you rent everything around it. If two rows in the "Build" column are filled, re-read the spec and cut one.

A useful test for the Build column: *"If a competitor shipped this tomorrow, would my product stop being worth using?"* If no, it is not differentiation and it should not be built. Auth and payments fail this test every time.

## 3. The 2026 default stack

This is the practitioner-consensus default for a solo web product in 2026 (see the research report's stack section). It is not the only good answer, but it is the one with the most accumulated answers to "how do I do X", which matters when you are alone:

| Layer | Default | Why |
| :-- | :-- | :-- |
| **Framework** | Next.js (or similar React meta-framework) | Huge ecosystem, one codebase for UI + API |
| **Database + auth** | Supabase | Managed Postgres, auth, and storage in one; no servers |
| **Hosting** | Vercel | Deploy from git; TLS, previews, scaling for free |
| **Payments** | Stripe | Card + subscription + tax plumbing you do not build |
| **Coding agent** | Claude Code (or Cursor) | The default build partner in 2026 |
| **Analytics** | Plausible/Fathom or PostHog | One dashboard, not five |
| **Support** | A shared inbox + macros | Resist AI chatbots until well past 100 customers |

Adoption is lopsided enough to matter: the coding agent you use is a near-default, and the four layers above are the ones most solo products land on. The value of the default is not that it is optimal — it is that when you hit a problem, someone else has already hit it and written the answer down.

## 4. The boring extreme

Boring has a floor, and it is lower than most founders assume. The **PHP + SQLite + one VPS + Cloudflare** setup is a legitimate 2026 choice: a tiny VM, a single-file database, no framework churn, no vendor sprawl, and a monthly bill measured in dollars. It has shipped real revenue products. Its advantages are total control and near-zero dependency risk; its costs are that you operate more yourself and you solve problems in a smaller community.

Reach for the boring extreme when:
- The product is CRUD-shaped and read-heavy, not real-time or media-heavy.
- You personally know the stack and enjoy it — familiarity beats fashion.
- You want to be able to hold the *entire* system in your head, which is the real goal.

Do not reach for it just to be contrarian, and do not reach for it if you have never deployed a VPS — the maintenance tail is exactly what you were trying to avoid. The default stack and the boring extreme are both "boring"; a novel architecture is neither.

## 5. Component-by-component defaults

When a decision is genuinely close, choose the option that:

1. **Has a free or cheap tier that covers a solo MVP.** You should not be paying enterprise prices before you have revenue.
2. **Can be replaced without a rewrite.** Managed services are swappable; a service you forked is not.
3. **Has a first-party SDK in your language** — fewer hand-written HTTP clients, fewer bugs.
4. **Shortens the path to the first real user.** Time to the core action in front of a person beats every other metric early.
5. **You already know.** The best tool is usually the one you will not have to learn while shipping.

Write the chosen stack into `founder/context.md` so every later skill (pricing, launch, metrics) inherits the same assumptions.

## 6. Stack red flags

- **A component you must operate, patch, and monitor yourself** before you have users.
- **A "we'll need it at scale" choice** made at zero scale. Scale problems are good problems; they arrive later, with revenue.
- **Two tools that do the same job** (two analytics, two auth, two databases). Pick one; the second is pure maintenance.
- **Anything on the critical path that you cannot explain in one sentence to a non-engineer.** That is complexity you have not yet noticed you own.
- **Custom auth or custom payments** — the two most expensive mistakes on this list, because they are also the two most likely to leak.
- **A stack you chose to impress someone.** Nobody who matters is looking; they are looking at whether the product works.
