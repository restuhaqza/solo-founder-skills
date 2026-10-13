# Support System (Solo Founder)

**Contents**
1. The shared-inbox model
2. Response-time targets
3. Macros and canned responses — and their limits
4. Two triage blocks a day (not thirty checks)
5. When to add a help centre
6. Resist AI chatbots and NPS automation until well past ~200 customers
7. A support review you can run in ten minutes

---

## 1. The shared-inbox model

Support needs one home. For a solo founder that means a single address (`support@…`, `help@…`) that customers can find, that forwards to a place you can open and *close*, and that is not your personal DMs, your Twitter inbox, or a chat thread you can never catch up on. Scattered channels are how support becomes an all-day ambient anxiety instead of a task.

A workable solo inbox model:

- **One address, one queue.** Route every channel you can into it (a form on the help page, the reply-to on product emails). If people reach you on X, answer there but log the substantive ones into the queue so they don't vanish.
- **A real subject → owner state.** Read the queue twice a day and act. "Seen" is not a state; the states are *answered*, *waiting on the customer*, and *needs a change* (a bug, a doc, a feature you logged).
- **Close the tab between blocks.** The inbox is not an open window you glance at; it is a queue you drain and leave.
- **A shared inbox tool is optional.** A single Gmail/HELPSCOUT-style address plus a label is enough for the first hundred customers. Do not buy a helpdesk to feel organised.

The point of the model is not tidiness. It is that a queue you can *finish* is the difference between support as a bounded task and support as a background hum that never stops.

## 2. Response-time targets

Set **one** target and keep it: a **≤24h first response**. Note what this is and is not.

- It is a *first-response* target, not a resolution target. Acknowledging fast and resolving when you can is honest and human; pretending to resolve in an hour is not.
- It is a *promise to yourself*, not a marketing SLA. You are a solo founder; do not publish a number you cannot keep on a bad week.
- **Billing and cancellation requests beat the target.** Money and trust do not wait for the morning block. Acknowledge a cancellation the day it arrives, even if the substantive reply comes after.
- **Weekends and holidays** are allowed to bend the target. Better a real 48h over a weekend than a burnt-out founder answering at midnight.

Why a target at all: without one, "answering support" expands to fill the evening, and the quiet middle of a solo business is exactly where that grind turns into burnout. A bounded target makes support a task you can complete and then go back to building.

## 3. Macros and canned responses — and their limits

A **macro** is a saved reply for a recurring situation: how to reset a password, what a plan includes, how to export data, what to do about a failed card. Macros exist for two reasons — **speed** (a good answer in seconds) and **consistency** (the same careful tone whether you are fresh or exhausted).

Rules that keep macros honest:

- **Few and true.** Start with five to eight macros covering the questions you actually get. A macro that apologises for a known-broken flow is a lie you will repeat at scale; fix the bug or delete the macro.
- **Personalise the first line.** Always greet by name and reference the actual ask. A raw macro reads as a brush-off and costs more trust than it saves time.
- **Never macro a frustrated or billing/cancellation customer past the acknowledgement.** Those get a human sentence.
- **Write macros from real tickets**, not imagination. If no ticket has asked it, no macro is needed.
- **Retire them.** When the underlying issue is fixed or the doc now handles it, delete the macro so it never resurrects an old answer.

**Their limits:** a macro can answer a *question*, but it cannot diagnose a *problem*, and it cannot decide a refund, a plan change, or an exception. Anything that touches money, trust, or a judgement call leaves the macro and becomes a human reply — which you then route into the right playbook.

## 4. Two triage blocks a day (not thirty checks)

The default cadence for solo support is **two short blocks a day** — roughly a 20-minute morning pass and a 10-minute afternoon pass. Triaging in blocks beats checking continuously for one reason that outlasts willpower: **discipline loses, scheduling wins.** A notification is novel and instantly rewarding, which is why the "I'll just check once" promise fails by mid-morning. A fixed block, by contrast, is just a task on the calendar; it starts and it ends.

How to run a block:

1. **Scan for the urgent first** — billing, cancellation, anything from a customer mid-onboarding or mid-outage. Handle those before the routine.
2. **Answer the routine with a macro or a doc link.** If neither fits, that is a signal: write the macro or the doc this time and answer in seconds next time.
3. **Log anything that needs a change** — a bug, a confusing screen, an unclear doc — as a real item, not a mental note.
4. **Stop at the time.** The queue drains twice a day; it never drains *while you keep it open*. Leaving a few messages for the next block costs little and protects the deep-work blocks that actually build the product.

Emergency escape hatch: a true outage or a data-loss report wakes you outside the blocks. Everything else waits.

## 5. When to add a help centre

A help centre is a **deflection** layer: pages that answer the recurring questions so people never email you at all. It earns its place when you can see the same handful of questions repeat in the tickets — not before, because a help centre written ahead of the tickets is guesswork you have to maintain.

Add it in this order:

- **Start with the tickets.** Mine the last 20–50 to find the questions asked most often. Each becomes a doc.
- **Write ten good pages, not a wiki.** One page per recurring question, each with a clear title someone would search, a direct answer at the top, and a screenshot or a step list. Use `assets/help-doc.md`.
- **Link docs from the macro, not instead of it.** The macro still answers; the doc is where you send the curious ones.
- **Re-check quarterly.** Ticket patterns drift. A page that no longer matches the product teaches people the wrong thing.

Resist building a sprawling knowledge base before you have the ticket data to fill it — a stale doc is worse than no doc, because it is a confident wrong answer.

## 6. Resist AI chatbots and NPS automation until well past ~200 customers

Practitioner guidance for solo founders is consistent on this: hold off on AI chatbots and automated survey machinery until you are well past a couple hundred customers. Two reasons.

- **A chatbot hides your best research.** At low volume, every conversation is a direct reading of what confuses people. A bot in front of that data answers the ticket *and deletes the lesson*. The confusion you most need to see is exactly the confusion the bot absorbs.
- **Automation has an accuracy cost you cannot yet afford.** A mis-routed bot on a small, high-value user base does more damage than a slightly slow human reply. And NPS/survey automation at low volume is survey noise — a handful of responses is not a score, it is a feeling with a number attached.

What to do instead early on: do it manually, read everything, and let the volume stay low enough that you can. Revisit the tooling when the ticket volume genuinely exceeds what two triage blocks can drain, and when the recurring questions are stable enough that deflection and light automation will not erase signal. This is a timing judgement, not a prohibition — the point is that the tool follows the pattern, not the other way round.

## 7. A support review you can run in ten minutes

Once a week, spend one short pass reviewing the system itself (not the tickets):

1. **Response time** — did you keep the ≤24h target? If not, which channel leaked?
2. **Top three ticket patterns this week** — are they macro'd or doc'd yet? If still answered by hand, that is this week's fix.
3. **Billing/cancellation** — all handled same-day? Any saved?
4. **One product fix** — name the single change the tickets point at, and hand it to `mvp-scoping`.
5. **Decide one thing** for next week's support, and change nothing else.

Support that is reviewed weekly improves; support that is only *worked* never gets faster.
