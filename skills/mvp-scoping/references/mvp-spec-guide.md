# MVP Spec Guide

**Contents**
1. Naming the core action and the core loop
2. User stories
3. Acceptance criteria (Given/When/Then)
4. Exit criteria
5. The anti-scope list
6. The walking skeleton
7. Slicing into small verifiable increments
8. Spec anti-patterns

---

## 1. Naming the core action and the core loop

The **core action** is the one thing a user does that the product exists to make possible. Write it as a verb phrase a stranger could repeat after one reading: *"send an invoice and get paid"*, *"turn a photo into a shareable page"*, *"log a workout in under ten seconds"*. If it takes a paragraph, or a paragraph of "ands", you have several features wearing one name.

The **core loop** is the action plus what surrounds it:

```
trigger  →  core action  →  feedback signal  →  reason to return
(a client   (create +       (invoice marked     (more invoices to send,
 needs        send an         paid)               next month's batch)
 paying)      invoice)
```

Three questions name the loop honestly:
- **Trigger** — what situation makes the user open the product at all?
- **Feedback** — how does the user *see* that the action worked? No visible feedback, no habit.
- **Return** — what brings them back without you emailing them?

Everything in v1 either *is* the loop or is load-bearing for it (auth, payment plumbing, the delivery mechanism). Everything else is a candidate for the anti-scope list. A product whose v1 contains a loop plus four things that are neither the loop nor load-bearing is a product that will not ship.

## 2. User stories

A user story is one sentence of intent, not a specification. Format:

> **As a** <specific user>, **I want to** <do the core action or a step toward it>, **so that** <the outcome they get>.

Rules that keep stories useful for a solo build:
- **One user, one action, one outcome.** If a story has two "ands", split it.
- **Name a real role**, not "user". "A freelance designer" tells you what to build; "a user" tells you nothing.
- **The "so that" must be an outcome, not an internal state.** "…so that I can share the link" is testable; "…so that it's easy" is not.
- **Write the stories for the core loop first**, then stop. Stories for anything outside the loop belong in the anti-scope list until v1 ships.
- **Include the boring requirement stories** that v1 genuinely needs — sign in, pay, receive an email — because leaving them implicit is how they turn into surprises during the build.

Keep the v1 story count small. A solo MVP with fifteen stories is usually a v2 spec; the loop typically needs three to six. Story count is the first scope signal, and the second is how many of them are "so that it's nicer" stories.

## 3. Acceptance criteria (Given/When/Then)

Acceptance criteria turn a story into something you can *check*. Use the Given/When/Then shape:

```
Given <a starting state>,
When  <the user takes the action>,
Then  <an observable, checkable result>.
```

Example for "send an invoice":
- **Given** a signed-in user with a saved client, **When** they create an invoice with one line item and click Send, **Then** the client receives an email within 60 seconds containing a link to the invoice.
- **Given** an invoice that has been sent, **When** the client opens the link and pays by card, **Then** the invoice shows as Paid in the sender's list within 5 seconds.

Rules:
- **"Then" must be observable** — a visible state, a row in the database, an email that arrives. If you cannot watch it, it is not a criterion.
- **Include the failure path** where the loop can break ("**Then** an invalid amount shows an inline error and no invoice is sent"). Most bugs live on paths no criterion described.
- **One criterion per behaviour.** Bundled criteria hide the ones that silently fail.
- **These are the agent's "done" check.** Each acceptance criterion is what a coding agent verifies before you accept a slice.

## 4. Exit criteria

Exit criteria are the smallest set of *observable* facts that prove v1 works, at the level of one user doing one full pass. They sit above acceptance criteria: acceptance criteria say "this step behaves"; exit criteria say "the product delivered its value to a real person".

Write three to five, each a binary check:

```
- [ ] A new user signs up and completes the core action once, unaided, in under <n> minutes.
- [ ] The action produces the feedback signal within <time> (invoice shows as paid, link resolves, page loads).
- [ ] The user performs the core action a second time without prompting.
- [ ] The whole pass works on the production URL, not just locally.
```

Why write them **before** coding:
- They convert "done" from a feeling into a checklist, so the build can actually end.
- They make scope creep visible: a feature that moves no exit criterion is optional by construction.
- They become the launch's success signal — if v1 hits its exit criteria, you have something to show, price, and distribute.

If a criterion is unobservable ("feels fast", "users like it"), rewrite it until a stranger with a stopwatch or a database query could check it. Unobservable criteria never retire a feature and never end a build.

## 5. The anti-scope list

The anti-scope list is the explicit record of **what v1 is not**. It is a deliverable, not a scrap heap, and it has three jobs: it stops the same tempting feature being re-litigated every week, it lets you say no without forgetting, and it is the seed of v2.

For each parked feature, one line with three parts:

```
<feature> — <why not in v1> — <the trigger that would pull it in>
```

Examples:
- *Recurring invoices — v1 proves one invoice can be sent and paid; scheduling adds a whole job engine — pull in when 3+ users ask.*
- *Team seats — solo buyers are the ICP; roles are v2 — pull in when a paying customer needs a second seat.*
- *Multi-currency — real FX and tax edge cases; no evidence anyone needs it — pull in when someone pays for it specifically.*

Two rules keep the list honest. First, **"we'll need it eventually" is not a trigger** — it is the sentence the list exists to answer. Second, **a feature with no trigger is a feature you have not decided about**; give it a trigger or move it into v1 with an exit-criteria link. The list should be longer than v1, and that is the point.

## 6. The walking skeleton

Build the **walking skeleton** first: the thinnest possible end-to-end path through the *real* stack. A real user signs up with the real auth provider, performs the core action against the real database, sees the real feedback, and pays with the real payment provider — even if every step is crude and every edge case is unhandled.

Why the skeleton and not "the hardest part first" or "the UI first":
- **Integration is where solo builds die**, not individual features. The skeleton forces every seam (auth → database → payment → email) to connect while the code is small and the error messages are still readable.
- It gives you a **demonstrable thing in days**, which is motivation insurance against the marathon.
- It makes the remaining work obviously *additive*: once the path walks, each slice thickens a step you have already proven.

A skeleton is "walking" when the core loop runs end-to-end on production. It is not walking when you have three polished pieces that do not yet talk to each other — that is the most common way a solo founder spends three weeks and ships nothing.

## 7. Slicing into small verifiable increments

After the skeleton, add features as **small verifiable slices**. A slice qualifies when:

1. **It is independently shippable** — it can go live without the next slice existing.
2. **It has a "done" check** — one or two acceptance criteria the agent verifies before you move on.
3. **It is small** — roughly a day or two of agent work. If it is bigger, the slice is really a project; split it.
4. **It thickens the loop** — it improves a step the skeleton already walks, rather than adding a new path.

Verification discipline is what makes slicing work with a coding agent:
- Give the agent the slice *and its acceptance criteria*, not a paragraph of intent.
- **Verify before starting the next slice.** Unverified slices stack into a debugging swamp where you cannot tell which change broke what.
- Keep a regression check on the core loop — the skeleton path — and re-run it after each slice. Agents break working things; a five-line check catches it.
- When a slice turns out bigger than expected, **cut it smaller** rather than extending the timeline. Extending timelines is how v1 becomes a marathon.

Sequence the slices so the riskiest *integration* is early and the cosmetic work is last. Polish is the only work that can be deferred without blocking the exit criteria, so defer it.

## 8. Spec anti-patterns

- **The spec that describes the product you want, not the one you need.** If every story is "and it also…", you wrote a v2 spec. Cut to the loop.
- **Criteria that are adjectives.** "Responsive", "intuitive", "fast" cannot be checked. Convert each to a number or an observable state.
- **No failure paths.** A spec with only happy paths ships a product that breaks the first time a user does something unusual.
- **The implicit stack.** A spec that does not say "managed auth, Stripe, hosted on X" invites the agent to build auth from scratch. State the boring choices.
- **The undated build.** A build sequence with no ship date drifts forever. Put a date on the skeleton and a date on the exit criteria.
- **Length as thoroughness.** A long spec reads as rigor and functions as scope. One page that is wrong is easier to fix than ten that are vague.
- **No exit criteria.** The spec with no observable definition of "done" is the spec that is never done.
