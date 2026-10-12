# MVP Spec — <product one-liner>

_Scoped <date> · Owner: <you> · ICP: <one narrow segment from founder/context.md> · Target ship date: <date>_

## 1. The core action and the core loop

**Core action:** <a verb phrase a stranger could repeat — e.g. "create and send an invoice">

**Core loop:**

```
trigger: <what makes the user open the product>
   → core action: <the one thing the product exists to do>
   → feedback: <how the user sees it worked>
   → return: <what brings them back>
```

**The one thing we build:** <the core action itself — everything else is bought or rented>.
**Everything else is:** auth <provider>, payments <provider>, database <service>, hosting <service>, email <service>.

## 2. User stories

Keep to the loop. A story outside the core loop belongs in §5 unless the loop breaks without it.

| # | Story |
| :-- | :-- |
| S1 | As a <specific user>, I want to <step toward the core action> so that <outcome>. |
| S2 | As a <specific user>, I want to <the core action> so that <outcome>. |
| S3 | As a <specific user>, I want to <see the feedback signal> so that <outcome>. |

## 3. Acceptance criteria (Given / When / Then)

One criterion per behaviour; include the failure path. These are the coding agent's "done" checks.

- **AC1 —** Given <starting state>, When <the user acts>, Then <observable result>.
- **AC2 —** Given <starting state>, When <the user acts>, Then <observable result>.
- **AC3 (failure path) —** Given <bad input or error state>, When <the user acts>, Then <observable error and no side effect>.

## 4. Exit criteria (written before any code)

v1 is done when all of these are observable on **production**:

- [ ] A new user signs up and completes the core action once, unaided, in under <n> minutes.
- [ ] The core action produces the feedback signal within <time>.
- [ ] The user performs the core action a second time without prompting.
- [ ] The loop runs end-to-end on the production URL, not just locally.

## 5. Out of scope — the anti-scope list

Explicitly NOT in v1. One line each: feature — why not now — the trigger that would pull it in.

- <feature> — <why not in v1> — <trigger>.
- <feature> — <why not in v1> — <trigger>.
- <feature> — <why not in v1> — <trigger>.

> "We'll need it eventually" is not a trigger. Give each feature a real one or move it into v1.

## 6. Stack decisions (build vs buy vs no-code)

| Component | Decision (build / buy / no-code) | Choice | Note |
| :-- | :-- | :-- | :-- |
| Auth | buy | <provider> | never custom |
| Payments | buy | <provider> | never custom |
| Database | buy | <service> | |
| Hosting | buy | <service> | |
| Email | buy | <service> | |
| **Core action** | **build** | — | this is the differentiation |

## 7. Build sequence

**Walking skeleton** — target: <date>. The thinnest end-to-end path through the real stack.

- [ ] Skeleton slice 1: <auth + the crudest possible core action>
- [ ] Skeleton slice 2: <the feedback signal>
- [ ] Skeleton slice 3: <the delivery / payment seam>
- [ ] Skeleton is walking when the core loop runs on production.

**Slices** — each independently shippable, smaller than ~2 days, verified before the next.

- [ ] Slice 1: <feature> — done when <criterion>. Verify: <check>.
- [ ] Slice 2: <feature> — done when <criterion>. Verify: <check>.
- [ ] Slice 3: <feature> — done when <criterion>. Verify: <check>.

## 8. Scope-creep guard

No feature is in v1 without a link to an exit criterion in §4.

| Feature (from §2/§7) | Linked exit criterion | In v1? |
| :-- | :-- | :-- |
| <core action> | <exit criterion> | yes |
| <feedback signal> | <exit criterion> | yes |
| <parked feature> | — | no (parked) |

## 9. Open questions

- <question> — owner: <you> — resolve by: <date>. If unresolved, the default is: <the smaller option>.
