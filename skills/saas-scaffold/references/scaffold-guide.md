# Scaffold Guide — Day Zero for a Solo SaaS Build

**Contents**
1. What "day zero" means
2. The repo layout that survives
3. Environments: local, preview, production
4. Config and secrets discipline
5. The data layer: migrations first
6. CI: the four gates that earn their keep
7. Deploy: from git, with a way back
8. The walking skeleton's definition of done
9. Packaging a slice for a coding agent
10. Day-zero mistakes that cost weeks

---

## 1. What "day zero" means

Day zero is the work that must exist **before** the first feature slice, because every
later slice depends on it and retrofitting it is expensive. It is small and it is boring:
a repo that runs, config that is not hardcoded, a database that can be rebuilt, a deploy
that comes from git, and a CI run that fails loudly. None of it is the product; all of it
is what lets the product be built in slices instead of one long, unreviewable push.

The test for whether day zero is done: **can a fresh clone reach the running app on a
new machine in one command, with no secrets in the repo and no manual dashboard clicks?**
If yes, slices can fly. If no, every slice starts with archaeology.

Do not confuse day zero with "finish setup". The scaffold is done when it is *sufficient*,
not when it is *complete* — a service you add before it is needed is a service you now
maintain for free, forever.

## 2. The repo layout that survives

A solo product does not need a monorepo framework; it needs a layout where the seams are
obvious. Two shapes cover almost everything:

- **Single app** (default for v1): one codebase holding UI and API — e.g. a Next.js app
  with `app/`, `lib/`, `db/`, `tests/`, `migrations/`. One deploy target, one lockfile.
- **App + thin worker**: the same, plus a `worker/` or `jobs/` entry point for anything
  that must run on a schedule or off the request path. Add it only when a slice needs it.

Put the things that change together in the same place, and keep the top level shallow.
Deep nesting is where a solo founder loses an afternoon looking for a file they wrote.

## 3. Environments: local, preview, production

Three environments, and only three, each with its own config and its own database:

| Env | Purpose | Database | Deploy trigger |
| :-- | :-- | :-- | :-- |
| **Local** | Build and test a slice | Local or a dedicated branch DB | You run it |
| **Preview** | See a change before users do | A branch/throwaway DB, seeded | Every push or PR |
| **Production** | Real users, real money | The real DB, backed up | Merge to main, after CI |

The one rule that prevents most disasters: **never let preview and production share a
database.** Pointing a preview deploy at production is how a test account emails real
customers. Most PaaS platforms give you per-branch databases for free; use them.

## 4. Config and secrets discipline

- **Config lives in the environment, not in code.** Every value that differs between
  local, preview, and production is an environment variable. No `if production:` branches
  with hardcoded hosts.
- **`.env.example` lists every variable name with a placeholder.** It is the contract for
  what a working environment needs; if a variable is missing from it, the app is relying
  on something invisible.
- **`.env` is gitignored, always.** A secret in git history is not deleted by deleting the
  file — it is in every clone anyone ever made. If a real secret is ever committed, rotate
  it; do not just remove the line.
- **Secrets live in the platform's secret store** (the PaaS env settings or a secrets
  manager), not in a shared doc and not pasted into the coding agent's prompt.

## 5. The data layer: migrations first

Create the migration tooling on day zero, before there is a schema worth migrating.

- **Every schema change is a migration file** that can be replayed from an empty database.
  A schema edited by hand in a dashboard console is a schema no other environment can
  reproduce.
- **Migrations run in CI and on deploy, in order, and are idempotent-safe.** A migration
  that can only run once, by you, on a good day, is a future outage.
- **Design for multi-tenant isolation from the first table**, even before you have a second
  tenant. The cheapest moment to add a `tenant_id`/`workspace_id` column and a row-level
  policy is before there is data to backfill. Retrofitting tenancy means touching every
  query you have written.
- **Write down how you would restore.** If the managed database has backups but you have
  never restored one, you have a hope, not a backup. The restore drill itself belongs to
  `launch-readiness`; the migration/schema hygiene belongs here.

## 6. CI: the four gates that earn their keep

A solo CI pipeline is not a quality religion; it is the thing that stops a bad merge while
you are asleep. Four gates, in this order, fast ones first:

1. **Install + build** — the repo compiles from a clean clone. This catches the "works on
   my machine because of a global install" class of bug.
2. **Lint / typecheck** — cheap and mechanical; it deletes whole categories of review.
3. **Migrations apply** — the schema replays against an empty database, so a broken
   migration fails here instead of in production.
4. **Tests** — the acceptance checks for shipped slices, run against a real (ephemeral)
   database, not mocks of one.

Everything else (coverage theatre, a dozen matrix jobs) can wait until there is a reason.
The goal is a pipeline that runs in minutes and that you trust enough to merge behind.

## 7. Deploy: from git, with a way back

- **Every production deploy comes from a git commit**, never from a laptop directory. The
  commit is the record of what is live.
- **Rollback is a first-class action you have practised once**, before you need it. On most
  PaaS platforms that is "promote the previous deployment"; know where the button is and
  what happens to a migration that already ran. Some migrations are not reversible — those
  need a forward fix, and knowing that in advance is the whole point of the drill.
- **A deploy is not done until it is verified.** The health route returns OK, the core
  action still works, and error tracking sees no new spike. See `launch-readiness` for the
  pre-first-user hardening pass.

## 8. The walking skeleton's definition of done

The walking skeleton is the thinnest real path through the real stack: a real user can
sign up, perform the core action once, and see the feedback — crude at every step, but
connected end to end. Its definition of done:

- [ ] The core action works for one real user in production (not a demo account).
- [ ] It reads and writes the real database through real migrations.
- [ ] Config comes from the environment; a fresh clone runs locally in one command.
- [ ] Deploy is from git and rollback has been tried once.
- [ ] The health route is up and CI runs green on main.

Notice what is *not* on the list: styling, edge cases, the second feature, or anything a
polish pass would touch. A skeleton is judged by whether the integration holds, because
integration — not features — is where solo builds die. Polish is a slice, later.

## 9. Packaging a slice for a coding agent

The scaffold exists so slices can be handed off cleanly. Each slice given to a coding agent
carries four things:

1. **The acceptance criterion** it must satisfy, copied verbatim from the MVP spec.
2. **The files or area** it may touch — a clear boundary so the agent does not wander.
3. **The "done" check** — the command or the observable behaviour that proves it works.
4. **The migrations** it needs, written as a replayable file, not an ad-hoc console edit.

One slice should never need more than a day or two of agent work, and must be independently
shippable — a slice that only makes sense once three others land is not a slice, it is a
rewrite in disguise.

## 10. Day-zero mistakes that cost weeks

- **Building features before the skeleton walks.** A beautiful feature on a stack that
  cannot deploy end to end is a demo, not progress.
- **Custom auth or custom payments.** Both are solved problems with security tails you do
  not want to own; wire the managed providers instead (see `auth-and-billing`).
- **A schema that only exists in one environment** because it was edited by hand.
- **Secrets in the repo**, or secrets pasted into chat, "just for now".
- **No rollback path**, discovered during the first bad deploy.
- **Preview and production sharing a database** — the configuration that turns a test into
  an incident.
- **A scaffold that keeps growing** because each new tool felt prudent. Every added moving
  part is a future 2am page; add one only when a slice needs it.
