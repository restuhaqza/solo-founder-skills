# Go-Live Checklist — Before the First Real User

**Contents**
1. How to use this
2. Secrets and configuration
3. Reliability: errors, health, monitoring, backups, rollback
4. Abuse and cost control
5. Legal and privacy (draft only)
6. The go / no-go
7. What can wait
8. The go-live drill

---

## 1. How to use this

`launch-readiness` runs `scripts/readiness_check.py` to find gaps, then this checklist turns
those gaps into work. Every item is tagged with why it matters and how badly it hurts if
missing. Severity is about **the cost of finding out the hard way**, not about effort:

- **Blocker** — shipping with this risks the business (leaked credentials, chargeable abuse).
- **High** — you will lose money, data, or trust the first week.
- **Medium** — survivable, but it will cost you a bad night.
- **Low** — a good habit, not a launch requirement.

Do not treat a clean scan as proof you are ready; treat it as the floor.

## 2. Secrets and configuration

- **No real secret in the repo (blocker).** Git history keeps a committed key forever, in
  every clone. If one was committed, **rotate it** — deleting the line is not enough.
- **Secrets live in the platform's secret store**, injected at runtime; `.env` stays local
  and gitignored; `.env.example` names every variable with a placeholder.
- **No secret in a log line or an error message.** A stack trace that prints the config is a
  leak into your error tracker.

## 3. Reliability: errors, health, monitoring, backups, rollback

- **Error tracking wired (high).** Without it, production failures are invisible until a
  customer complains, and you cannot tell a spike from a blip.
- **A health route (medium).** One endpoint that returns OK when the app and its database are
  reachable — the thing uptime monitors hit.
- **Uptime monitoring (medium).** An external monitor that pages you; your own app cannot tell
  you it is down.
- **Backups documented (high).** A managed database usually has them on; know the retention
  window and where the button is.
- **Restore tested at least once (medium, but the point of the exercise).** A backup you have
  never restored is a hope. Run one restore end to end, time it, and write down how.
- **A rollback path you have practised (medium).** Know how to promote the previous deploy,
  and know which of your migrations are not reversible — those need a forward fix.
- **Feature flag / kill switch (medium).** The ability to turn a bad feature off without a
  full redeploy turns an outage into a five-second decision.

## 4. Abuse and cost control

- **Rate limiting on sensitive routes (high).** Signup, login, password reset, checkout, and
  any expensive AI call. An unthrottled signup or card-testing endpoint is a bill and a
  security hole.
- **Spend caps on the expensive providers.** Set hard limits on the LLM/API and the hosting
  account so a runaway loop cannot run up a month of revenue in an hour.
- **Alerts on abnormal usage**, even a crude one (a daily email when a counter passes a
  threshold). You want to hear about abuse from your own alert, not your invoice.

## 5. Legal and privacy (draft only)

- **Privacy policy + terms pages (high).** Needed before you store other people's data. These
  are **first drafts flagged for a professional to review** — this skill and the whole pack
  never give legal advice and never finalise these documents.
- **A short data map (medium).** What personal data you collect, where it is stored, and which
  subprocessors (auth, payments, email, analytics, hosting) touch it. Without it you cannot
  answer a privacy question or a customer's deletion request.
- **A deletion path.** If you can collect it, you must be able to delete it. One admin action,
  documented, is enough at this stage.

## 6. The go / no-go

`readiness_check.py` ends in a verdict: `NOT_READY` (a blocker or high gap remains),
`READY_WITH_GAPS` (only medium/low), or `READY`. **The verdict is an input to the decision,
not the decision.** Whether to launch with known gaps is the founder's call — the skill
prepares the evidence and names the risk; it never makes the go/no-go call. If you launch with
a gap, write down which one and why, so future-you can see it was chosen, not missed.

## 7. What can wait

Deliberately out of scope for a first launch, so you do not gold-plate: SOC 2 or ISO
certification, a status page before you have users to notify, multi-region failover, a
bug-bounty programme, a formal incident-response runbook, and load testing at zero scale.
Add each when a paying customer or a real incident demands it — not because a checklist could
go on forever.

## 8. The go-live drill

Run this end to end once, out loud, before you invite anyone:

1. `python3 scripts/readiness_check.py --doc founder/product/launch-readiness.md` — read the
   verdict and the top gap.
2. Deploy to production from a clean `main`. Watch it come up.
3. Confirm the health route and that uptime monitoring is green.
4. Do the core action yourself as a brand-new user, paying with a real card.
5. Confirm the payment webhook landed and entitlement was granted (not just the redirect).
6. Force an error and confirm it appears in error tracking.
7. **Roll back**, then deploy forward again. You have now done it once when it did not matter.
8. Restore the database into a throwaway environment and check the data is there.
9. Write the date and what broke into `founder/product/launch-readiness.md`.
