# Launch Plan — <product one-liner>

_Launch target: <Thursday, date> · Owner: <you> · ICP: <one narrow segment> · Primary channel: <ONE channel>_

> A launch is a spike; distribution is the engine. Fill this in from four weeks out, and keep working the two weeks *after* launch — that is where the compounding starts.

## The decision (fill this first)

- **The one channel we go deep on:** <e.g. r/SideProject + one niche Slack>
- **Why here:** <where the exact buyer already gathers, and why we can show up weekly>
- **Measurable outcome:** <e.g. 25 activated signups / 10 qualified replies> by <date>
- **60-day cut rule:** if <outcome metric> is below <target> by <date>, stop and move the hours to: <next channel>
- **UTM campaign name:** <e.g. launch-apr-2026> (see `tracking.md`)

---

## T-4 weeks — foundations

- [ ] Re-read `founder/context.md`; confirm the ICP in one sentence and the outcome metric
- [ ] Choose and commit to the ONE channel (see `../references/channel-playbook.md`)
- [ ] Decide the launch date (Product Hunt aims for a Thursday) and block the whole day
- [ ] Draft the landing/hero copy so a stranger can repeat what the product does
- [ ] Set up or confirm analytics and a signup/activation event you can count
- [ ] Build the launch list: people who asked, waiting contacts, past users, friendly communities
- [ ] Create `founder/gtm/tracking.md` and generate UTM URLs (run `../scripts/utm_builder.py`)

## T-3 weeks — build the assets

- [ ] Gallery screenshots / short demo clip (show the outcome, not the UI chrome)
- [ ] Product Hunt copy drafted (`producthunt-launch.md`)
- [ ] Show HN post drafted if relevant (`show-hn.md`)
- [ ] One comparison page or free tool (the engineering-as-marketing artifact)
- [ ] Pick the ONE outcome number and write it where you'll see it every day

## T-2 weeks — warm the room

- [ ] Post *usefully* in the chosen community — no pitch attached
- [ ] Line up 3–5 people who will genuinely try it on launch day (not just upvote)
- [ ] Draft the launch-day posts for each place, rewritten for that room's norms
- [ ] Prepare the day-of runbook (below) and a bug triage list

## T-1 week — rehearse

- [ ] Dry-run the signup flow as a stranger; fix anything that breaks
- [ ] Schedule the Product Hunt listing; check timezone (PH days are Pacific)
- [ ] Write the launch-day reply templates (thanks, bug acknowledgment, onboarding offer)
- [ ] Prepare a "hand-onboard the first 10 users" task — calendar time, not a docs link
- [ ] Freeze features. Only bug fixes from here.

## T-0 — launch day (the whole day)

- [ ] Post on the primary channel at the right hour (PH: just after midnight PT; HN: morning US Eastern)
- [ ] Reply to **every** comment, fast — especially the skeptical ones, with substance
- [ ] Fix obvious bugs live while people are watching; narrate the fix
- [ ] Hand-onboard the first users personally ("want me to set it up with you?")
- [ ] Do not ask for upvotes — ever (HN especially)
- [ ] Log the real numbers as they land (visits, signups, comments, replies)

## T+1 to T+3 days — catch the stragglers

- [ ] Reply to anything you missed; answer late questions late but answer them
- [ ] Onboard signups that never activated — a direct, personal message
- [ ] Publish a **specific** build-in-public post on what the launch actually did (real numbers)
- [ ] Thank the people who helped, individually
- [ ] Note which community/person drove the most real signups (check UTMs)

## T+1 to T+2 weeks — turn the spike into a slope

- [ ] Review: did the measurable outcome land? Log the answer, hit or miss
- [ ] Double down on whatever worked; write down what you'll stop
- [ ] Ship the first pillar content piece + one supporting piece
- [ ] Add the engineering-as-marketing artifact to the channel where the buyer is
- [ ] Re-check `tracking.md`: every new link carries a UTM
- [ ] Rehearse the day-60 cut rule: is this channel earning its hours?

---

## Day-of runbook (keep this open)

1. **Post** on the primary channel at the planned hour.
2. **Watch the first hour.** Momentum early decides the outcome.
3. **Reply to every comment**, newest-first, in your own voice.
4. **Triage bugs:** anything that blocks signup gets fixed live; everything else goes on a list.
5. **Onboard personally** the first handful of users; ask what they were trying to do.
6. **Log numbers** into the metrics file as they come in (this feeds `product-metrics`).
7. **Close the day** with a short, honest note to yourself: what worked, what surprised you.

## Boundary

- The **founder** sends every outbound, DM, and community post. The agent drafts and prepares; it never posts, comments, or sends on the founder's behalf.
