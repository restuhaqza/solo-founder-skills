# Routing Table

**Contents**
1. How to read this table
2. Situation → skill
3. The lifecycle loop
4. When NOT to reach for a skill

---

## 1. How to read this table

Read the *middle* column, not the left one. Founders describe symptoms ("how much
should I charge?"); the table maps symptoms to the underlying **job**, then to the
one skill that owns it and the artifact that proves the job is done. Find the row
that matches the job, not the wording, then route.

If two rows fit, take the earlier job in the lifecycle loop (§3) — you cannot price
what nobody has validated, and you cannot measure a launch that hasn't happened.

## 2. Situation → skill

| Situation / what they say | The job underneath | Owning skill | Next artifact |
| :-- | :-- | :-- | :-- |
| "Is this idea worth building?" · "Should I build this?" · "Is anyone going to pay for this?" | Decide whether real demand exists before writing code | `idea-validation` | `founder/validation/go-no-go.md` |
| "Help me validate this" · "I want to talk to customers" · "Here are my interview notes" | Turn scattered evidence into a case for and against | `idea-validation` | `founder/validation/go-no-go.md` |
| "What do I build first?" · "This is getting too big" · "V1 keeps growing" | Cut to the smallest thing that proves the value | `mvp-scoping` | `founder/product/mvp-spec.md` |
| "Help me write the spec" · "I keep adding features" · "Which stack should I use?" | Scope, cut, and sequence the build | `mvp-scoping` | `founder/product/mvp-spec.md` |
| "How much do I charge?" · "Is my price too low?" · "Should this be a subscription?" | Set value-based pricing and packaging | `pricing-strategy` | `founder/pricing/pricing.md` |
| "Should I add a free tier?" · "Design my pricing page" | Shape tiers and the page that sells them | `pricing-strategy` | `founder/pricing/pricing.md` |
| "How do I get users?" · "Nobody's finding my product" · "I'm launching next month" | Stand up distribution, not just a launch-day spike | `go-to-market-launch` | `founder/gtm/launch-plan.md` |
| "Help me market this" · "Write my Product Hunt post" · "Plan my content" | Run the launch and the channel that follows it | `go-to-market-launch` | `founder/gtm/launch-plan.md` |
| "What should I measure?" · "How do I know if I'm growing?" · "I have data but no idea" | Choose the few numbers that change decisions | `product-metrics` | `founder/metrics/metrics-spec.md` |
| "My churn is high" · "Failed payments everywhere" · "Review my month's numbers" | Split churn, find the leak, run the weekly review | `product-metrics` | `founder/metrics/metrics-spec.md` |
| "I'm overwhelmed" · "What should I focus on this week?" · "I'm wearing too many hats" | Pick the one thing and protect the week | `founder-operating-rhythm` | `founder/ops/weekly-review.md` |
| "Am I default alive or default dead?" · "Am I running out of money?" · "Do I need to set up a company? (legal/tax)" | Read the runway honestly and keep the business unencumbered | `founder-operating-rhythm` | `founder/ops/weekly-review.md` |

## 3. The lifecycle loop

The stages are loops, not a line — validation feeds positioning, distribution feeds
product discovery, retention feeds pricing. Follow the arrow, then come back.

```
      ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
      │   VALIDATE   │───>│    SCOPE     │───>│    PRICE     │
      │idea-validation│   │  mvp-scoping │    │pricing-strategy│
      └──────────────┘    └──────────────┘    └──────────────┘
             ^                                        │
             │                                        v
      ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
      │   OPERATE    │<───│   MEASURE    │<───│    LAUNCH    │
      │founder-ops-  │    │product-metrics│   │go-to-market- │
      │rhythm        │    │              │    │launch        │
      └──────────────┘    └──────────────┘    └──────────────┘
             │
             └────────────> back to VALIDATE (new idea, pivot, or the next loop)
```

## 4. When NOT to reach for a skill

- **The job is already obvious.** If the founder names the domain ("help me write
  the MVP spec"), go straight to that skill. The router is for ambiguity, not a
  toll booth on every request.
- **It is a build task.** Writing, reviewing, testing, deploying, or migrating code
  belongs to a coding agent, not to any skill in this pack.
- **It is a human-only decision.** The go / no-go / pivot / kill call, sending an
  outbound message, legal/tax/entity sign-off, and the sell-or-hold choice are the
  founder's. The skills *prepare* the evidence or the draft; they never make the call.
- **The founder just wants to understand the options.** Answer directly, in plain
  language. Not every question needs an artifact — sometimes the right output is a
  short explanation, not a routed hand-off.
