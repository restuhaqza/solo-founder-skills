---
name: support-and-onboarding
description: Run solo customer support without burning out and build onboarding that reaches the aha moment, so customers stop leaving before they ever get value. Sets up the support system (shared inbox, ≤24h response target, macros, batched triage), writes help docs and canned replies from real ticket patterns, defines the activation event and time-to-value, generates a Day 0/1/3/7/30 onboarding email sequence, adds at-risk detection and save playbooks, and triages feedback by Impact × Votes ÷ Effort. Use this skill whenever a solo founder is drowning in support email, losing customers before they activate, needs an onboarding sequence or activation metric, wants to know why people churn right after signing up, or is setting up help docs, macros, or a win-back — even if they only say "I'm spending all day answering emails", "users sign up and disappear", or "why is my churn so high?". Outputs land in founder/support/.
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: support
---

# Support & Onboarding

Use this skill to run support as a **system** rather than an inbox you check all day, and to fix the onboarding that gets customers to value — because most churn happens *before* anyone ever gets value, not because a later feature is missing. It produces a support system, macro/help-doc templates from your real ticket patterns, an onboarding-to-aha sequence, and the at-risk detection that saves accounts before they cancel. Outputs land in `founder/support/`.

## The one rule

**Support is a system before it is a tool, and most churn happens before value — fix onboarding before you answer more tickets.** An inbox you check thirty times a day is not support; it is a interruption generator that fragments your deep work. And if people never reach the aha moment, every extra ticket you answer is someone asking about a product that never delivered. Build the loop (inbox → batch → macro → doc), then fix activation, *then* add tools.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Build the support system (inbox, ≤24h target, macros, two triage blocks/day)
- [ ] Step 2: Write the top help docs and macros from real ticket patterns
- [ ] Step 3: Define the single activation event and time-to-value (hand-off from product-metrics)
- [ ] Step 4: Generate the onboarding-to-aha sequence (run scripts/onboarding_sequence.py)
- [ ] Step 5: Set up at-risk detection and the four save playbooks
- [ ] Step 6: Triage feedback and feature requests (Impact × Votes ÷ Effort)
- [ ] Step 7: Verify — every ticket has a macro or a doc, every step drives activation
```

**Step 1 — Build the support system first**
Before any automation, build the plumbing that keeps support from eating your day. Four pieces: a **shared inbox** (one address, never your personal DMs, so support has a home you can close); a **≤24h first-response target** (not an SLA you advertise — a promise you keep to yourself so support never becomes anxiety); **macros** (canned replies, see `assets/support-macros.md`); and **two short triage blocks a day** (roughly 20 minutes morning, 10 minutes afternoon) instead of checking the inbox thirty times. Batching beats discipline: the discipline always loses to the novelty of a new message, but a fixed block is just a task. Handle **billing and cancellation requests immediately** — those are money and trust, and they never wait for the afternoon block. Read `references/support-system.md` before you set this up. The single highest-leverage move for a solo founder is to stop treating the inbox as a place to sit and start treating it as a queue to drain twice a day.

**Step 2 — Write the top help docs and macros from real ticket patterns**
Do not write documentation from imagination; write it from the tickets you actually received. Read your last ~20–50 tickets, count the recurring questions, and fix the top handful. Each recurring question becomes either a **macro** (a canned reply that answers it, so you send a good answer in seconds) or a **doc** (a page that deflects it entirely, so they never email). Start with the fill-in templates: `assets/support-macros.md` and `assets/help-doc.md`. Docs deflect tickets; macros keep tone consistent when you are tired. Keep the macro set small and honest — a macro that apologises on your behalf for an unfixed bug is a lie you will repeat, so fix the bug or retire the macro. **Macros have limits**: they are for the routine and the reassuring, never for a frustrated customer who needs a human sentence, and never for anything billing- or cancellation-related beyond an acknowledgement.

**Step 3 — Define the single activation event and time-to-value**
Activation is the one countable action that proves a user reached value — not a signup, not a login. Slack looked at messages sent by a team; Dropbox at a file accessed on a second device; Figma at the first three files. Yours is one sentence ("first report shared with a client"). This is a **hand-off from the `product-metrics` skill** — if it already defined the activation event under `founder/metrics/`, reuse it verbatim rather than inventing a second definition; two competing activation events make both useless. Then measure **time-to-value**: the median delay between signup and the activation event. If that number is not improving, onboarding is the problem, and it is the highest-leverage thing you can fix. See `references/onboarding-to-aha.md` for how to pick the event and the time-to-value signal.

**Step 4 — Generate the onboarding-to-aha sequence**
Build the email sequence that walks a new signup from welcome to value, one action per step. Generate the scaffold, then edit the copy into your own voice:

```bash
python3 scripts/onboarding_sequence.py \
  --product "Acme Reports" \
  --activation-event "first report shared with a client"
```

The default shape is **Day 0 (welcome) / Day 1 (the single action that reaches the aha) / Day 3 (the feature that makes it click) / Day 7 (check-in) / Day 30 (milestone and next step)**, and every step drives **one specific action toward the activation event** (use `--days` for a different schedule, `--tone` for the voice, `--json` for structured output). The output is a dated scaffold with subject lines, the one action, a body skeleton with placeholders, and a goal line. **Trim it and ship it** — three focused emails that reach the aha beat seven that get filtered, and suppress anyone who activates early so you never send a nudge to someone who already got value.

**Step 5 — Set up at-risk detection and the four save playbooks**
The cleanest early-warning signal is **absence of the core action**: flag any active customer with no core action in **14–21 days**, while there is still time to intervene *before* they cancel. Combine product usage (no core action, a session-frequency drop, a power user gone quiet) with billing signals (a failed payment, an approaching renewal, a lapsed trial). Then fire the matching save playbook from `references/onboarding-to-aha.md`:

- **Onboarding-rescue** — signed up, never activated: re-run the shortest path to the activation event.
- **Silent-quitter** — was active, went quiet: a short, human "anything blocking you?" nudge.
- **Payment-saver** — a failed card: the dunning sequence (see `product-metrics`).
- **7-day reactivation** — after a lapse: a concrete reason to return, not a generic discount.

You can script this on your billing provider plus one product-analytics tool; you do not need a dedicated churn tool until you are well past a couple hundred customers.

**Step 6 — Triage feedback and feature requests**
Support email is your cheapest source of product truth — treat it as research, not overhead. Capture every request, then **score each by Impact × Votes ÷ Effort**: how much value it unlocks, how many customers asked, divided by the ongoing build-and-maintain cost to a solo founder (effort includes the support tail, not just the build). Two habits keep this honest: **mine ticket patterns** (a question asked ten times is a UX bug, not ten support tasks — fix the screen or the doc), and **synthesise trends rather than chasing the loudest voice** (the one angry email is a data point, not a backlog; the feature that quietly 67% of users adopt beats the dashboard 4% asked for). Log it in `founder/support/feedback.md` and feed the patterns to `mvp-scoping`.

**Step 7 — Verify**
Two checks before you call support "handled". First, **every ticket in your last batch has a macro or a doc behind it** — if you answered the same question twice from scratch, it needs a macro or a doc, not more effort. Second, **every onboarding step drives toward the activation event** — if a step does not move the reader closer to that one action, cut it. A sequence step that only says "we're excited!" is noise.

## Output format

Write to `founder/support/`. The core deliverable is the support system plus the onboarding sequence:

```markdown
# Support System — <product>
_Activation event: <the one countable action> · Time-to-value target: <median days>_

## Inbox & response
- Shared inbox: <address>
- First-response target: <= 24h
- Triage blocks: <morning time> / <afternoon time>

## Top ticket patterns (from real tickets)
| Pattern | Frequency | Fix (macro or doc) | Status |
| :-- | :-- | :-- | :-- |
| <question> | <n/wk> | macro: <name> | sent |

## Onboarding-to-aha sequence
Source: scripts/onboarding_sequence.py · See onboarding-sequence.md

## At-risk detection
- Signal: no core action in <14-21> days
- Playbooks: onboarding-rescue · silent-quitter · payment-saver · 7-day reactivation
```

Support emails drafted here are **drafts for the founder to send** — this skill writes and scores; it does not send.

## Gotchas

- **Adding a chatbot too early.** A bot in front of a small, high-value user base hides the very confusion you most need to read, and it deflects the wrong tickets. For a solo founder, the first few hundred conversations are product research. Resist AI chatbots and NPS automation until you are well past ~200 customers.
- **The inbox breaks deep work — batching beats discipline.** Checking mail 30× a day means no task ever gets a full block of attention, and the burnout research ties the quiet middle to exactly this fragmentation. Two fixed triage blocks beat heroic willpower every time.
- **Billing and cancellation first.** These are money and trust, not support volume. Handle them the moment they land, never "in the afternoon block", and never with a generic macro past the acknowledgement.
- **Optimising signups while activation is low.** More signups into a leaky onboarding is a faster bucket, not growth. If time-to-value is not falling, acquisition turns into churn.
- **Support as a cost, not truth.** The founder who treats every ticket as an interruption never hears the roadmap the tickets are spelling out. A question asked ten times is a product bug.
- **Churn happening before value.** Customers rarely leave over a later feature; they leave because they never reached the aha moment. Look at first-session behaviour and onboarding before you read a cancellation survey.
- **Macros that lie.** A canned apology for a known-broken flow scales the lie. Fix it or drop the macro.
- **Human-approval boundary.** This skill drafts replies, macros, docs, and sequences. **Sending any customer-facing message is the founder's call**, and refunds, plan changes, and moving money remain the founder's decision — flag them, never execute them.

## Available scripts

- **`scripts/onboarding_sequence.py`** — given `--product` and `--activation-event`, emits a dated Day 0/1/3/7/30 onboarding email scaffold as Markdown: one block per day with a subject line, the ONE action it drives toward activation, a body skeleton with `[USER_NAME]`/`[PRODUCT]` placeholders, and a goal line. Supports `--days`, `--tone`, and `--json`. Run `python3 scripts/onboarding_sequence.py --help` for the arguments.

## Reference files

- **`references/support-system.md`** — the shared-inbox model, response-time targets, macros and canned responses (and their limits), the two-triage-blocks/day cadence, when to add a help centre, and why to resist chatbots/NPS automation until well past ~200 customers. Read at Step 1.
- **`references/onboarding-to-aha.md`** — what an activation event is, why activation ≠ signup, the Day 0/1/3/7/30 sequence shape, at-risk detection (no core action in 14–21 days), the four save playbooks, and win-back timing. Read at Steps 3–5.
- **`assets/support-macros.md`** — fill-in canned-reply templates for the common ticket types. Copy to `founder/support/macros.md` and edit.
- **`assets/help-doc.md`** — fill-in help-article template. Copy per recurring question so the doc deflects the ticket.

## Hand-off

When the support system and onboarding sequence are live, feed the numbers back to `product-metrics` (activation rate, time-to-value, churn split), and hand the patterns the tickets reveal — the repeated confusion and the missing core action — back to `mvp-scoping` so the product fixes the cause instead of the support team absorbing it.
