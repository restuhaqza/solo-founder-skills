# Launch Readiness — <product / version>

_One page. The record of what was checked before the first real user, and what was knowingly left open. Re-run `scripts/readiness_check.py` as the gating check._

## Verdict

- Scan verdict: <NOT_READY / READY_WITH_GAPS / READY>
- Go / no-go: **<founder's call — not the skill's>**
- If launching with gaps, the gaps knowingly accepted and why:

## Secrets

- [ ] No real secret in the repo (rotate any that were committed)
- [ ] Secrets in the platform secret store; `.env` gitignored; `.env.example` complete
- [ ] No secret printed to logs or error tracker

## Reliability

- [ ] Error tracking wired (provider: <…>)
- [ ] Health route: `<path>`
- [ ] Uptime monitoring + who gets paged
- [ ] Backups on (retention: <…>); where the button is
- [ ] Restore tested once — date: <…>, took <…>
- [ ] Rollback practised — non-reversible migrations: <list / none>
- [ ] Feature flag / kill switch: `<…>`

## Abuse and cost

- [ ] Rate limiting on signup, login, reset, checkout, expensive calls
- [ ] Spend caps set on: <LLM/API, hosting>
- [ ] Alert on abnormal usage: <how>

## Legal / privacy (drafts for a professional)

- [ ] Privacy policy page (draft)
- [ ] Terms page (draft)
- [ ] Data map: what we collect, where stored, subprocessors
- [ ] Deletion path documented

## Go-live drill (run once, out loud)

- [ ] Deploy from clean `main`; health + monitoring green
- [ ] Core action as a brand-new user, real card
- [ ] Payment webhook landed; entitlement granted (not just redirect)
- [ ] Forced an error; it appeared in error tracking
- [ ] Rolled back, then forward again
- [ ] Restored the DB into a throwaway; data present

## Log

| Date | What broke / what was learned |
| :-- | :-- |
| | |
