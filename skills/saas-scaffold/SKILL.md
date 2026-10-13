---
name: saas-scaffold
description: Turn an MVP spec into a runnable day-zero scaffold for a solo SaaS build — repo layout, environment variables and the .env.example contract, local/preview/production environments, CI gates, a git-based deploy with a rollback path, migrations and multi-tenant schema hygiene, and a walking skeleton defined end to end. Use this skill whenever a solo founder or indie builder is about to start building, says their spec is done and asks how to set up the project, wants the codebase structured before handing work to a coding agent, asks about environments, env vars, secrets, CI, migrations, or deploys, or hits a "works locally but not in production" / "no way to roll back" problem — even if they only say "I'm ready to build now", "set up my repo", "where do I put config?", or "how should I hand this to Claude Code?".
license: MIT
metadata:
  author: Restu Haqza
  version: "1.0.0"
  category: product
---

# SaaS Scaffold

Use this skill to turn a finished MVP spec into a repository that can actually ship — the boring plumbing that every later slice depends on. It produces a one-page scaffold plan, a repo scan of what is present versus missing, and a walking-skeleton definition of done. Outputs land in `founder/product/`. **It sets up the workshop; it does not build the product.** Writing the feature code is a coding agent's job, and each slice is handed off with its acceptance criteria.

## The one rule

**The skeleton must walk before anything is polished.** Day zero is done when a fresh clone reaches the running app on a new machine in one command, config comes from the environment, the database rebuilds from migrations, deploys come from git, and rollback has been tried once. Judge the scaffold by whether a slice can then land safely — not by how complete the setup feels. A tool you add before a slice needs it is a tool you maintain forever.

## Workflow

Copy this checklist and tick items off as you go:

```
Task progress:
- [ ] Step 1: Read the MVP spec and context; confirm stack (from mvp-scoping)
- [ ] Step 2: Scan the current repo (scripts/repo_scan.py) and list the gaps
- [ ] Step 3: Fix the blocking gaps: manifest, .gitignore/.env, .env.example, deploy, CI
- [ ] Step 4: Stand up three environments and per-branch databases
- [ ] Step 5: Set up migrations and multi-tenant schema hygiene
- [ ] Step 6: Define the walking skeleton's definition of done
- [ ] Step 7: Write founder/product/scaffold-plan.md
- [ ] Step 8: Re-scan and hand the first slice to the coding agent
```

**Step 1 — Read the spec and confirm the stack**
Open `founder/product/mvp-spec.md` (from `mvp-scoping`) and `founder/context.md`. The stack was already decided there — do not re-litigate it here. If no spec exists, stop and run `mvp-scoping` first: scaffolding without a named core action and exit criteria is just tidying. The three things you need from the spec are the core action, the stack, and the build sequence.

**Step 2 — Scan the repo and list the gaps**
Run the scanner from the repository root:

```bash
python3 scripts/repo_scan.py .
```

It reports each day-zero piece as found or missing, a coverage percentage, and the single next piece to add in priority order. Read the missing list as your work queue, and read the *found* list skeptically — a file being present is not a file being configured (a `.gitignore` that does not exclude `.env` is reported as missing for exactly this reason).

**Step 3 — Fix the blocking gaps first**
Attack in dependency order: the package manifest, then `.gitignore` covering `.env`, then `.env.example`, then the deploy config, then CI. These block everything else — you cannot test a slice without a deploy, and you cannot deploy safely without config out of code and a CI run. For the detail behind each, read `references/scaffold-guide.md` §4 (config and secrets), §6 (CI), and §7 (deploy).

**Step 4 — Stand up the environments**
Create exactly three: local, preview, production — each with its **own** database. The non-negotiable rule is that preview and production never share one; pointing a preview deploy at production is how a test account emails real customers. Most PaaS platforms give per-branch databases for free. Record the three environment names in the scaffold plan so the coding agent uses them consistently.

**Step 5 — Migrations and multi-tenant hygiene**
Set up the migration tooling now, before there is a schema worth migrating, so every change is a replayable file rather than a hand-edit in a dashboard. Add a `tenant_id` / `workspace_id` column and row-level isolation policy on the first table, even with one tenant — the cheapest time to add tenancy is before there is data to backfill. See `references/scaffold-guide.md` §5.

**Step 6 — Define the walking skeleton's done**
Write the skeleton's definition of done as binary checks (core action works for one real user, real DB via real migrations, one-command local run, deploy from git with rollback tried, health route up, CI green). This is the milestone that de-risks integration, which is where solo builds die. Use the checklist in `references/scaffold-guide.md` §8.

**Step 7 — Write the scaffold plan**
Fill `assets/scaffold-plan.md` and save it to `founder/product/scaffold-plan.md`: environments, required env vars, CI gates, deploy and rollback path, migration approach, and the skeleton's definition of done. Keep it to one page — the coding agent reads this, not a novel.

**Step 8 — Re-scan, then hand off the first slice**
Re-run `scripts/repo_scan.py` until the blocking items are green, then package the first slice for the coding agent using `references/scaffold-guide.md` §9: the acceptance criterion verbatim from the spec, the files it may touch, the done check, and any migration it needs. Then move to `auth-and-billing` to wire signup and payments into the skeleton.

## Output format

Write `founder/product/scaffold-plan.md` using `assets/scaffold-plan.md`. Keep these sections: stack (inherited), environments, config/env-var contract, CI gates, deploy + rollback, migration approach, and the skeleton's definition of done. Also paste the `repo_scan.py` summary (found/missing + coverage %) so the plan starts with an honest measure of day zero.

## Gotchas

- **A present file is not a configured file.** The scanner reports a `.gitignore` that does not exclude `.env` as *missing* deliberately. When you review, check configuration, not existence.
- **Preview and production must never share a database.** This is the single most common way a solo deploy leaks test data into real customer data, and it is invisible until it isn't.
- **Names differ per platform.** Preview environments are "deploy previews" on one host, "previews" on another, and per-branch databases are "branching" or "database branches". Map the concept to the platform's word in the plan.
- **Secrets never enter the repo, a chat prompt, or a shared doc.** They live in the platform's env/secret store. If a real secret is ever committed, rotate it — deleting the line leaves it in every clone's history.
- **Some migrations are not reversible.** Know which of yours are, and record the forward-fix plan for the ones that are not, before the first bad deploy.
- **Do not scaffold more than the skeleton needs.** A queue, a cache, and a second service added "while we're here" are three future 2am pages you now own. Add each when a slice demands it.
- **Scaffolding is not building.** This skill stops at a plan and a runnable skeleton. If you find yourself writing feature logic, you have crossed into the coding agent's job — hand it the slice instead.

## Available scripts

- **`scripts/repo_scan.py`** — scans a repository for day-zero scaffold pieces (manifest, lockfile, `.gitignore`/`.env`, `.env.example`, deploy config, CI, migrations, health route, tests, one-command dev, README setup, seed data), reports found/missing with a coverage %, and names the next piece to add in priority order. `--json` emits structured output. Run: `python3 scripts/repo_scan.py .`

## Reference files

- **`references/scaffold-guide.md`** — the day-zero playbook: repo layout, the three environments, config and secrets discipline, migrations and multi-tenant hygiene, the four CI gates, git-based deploy with rollback, the walking-skeleton definition of done, how to package a slice for a coding agent, and the day-zero mistakes that cost weeks. Read during Steps 3–8.
- **`assets/scaffold-plan.md`** — the fill-in scaffold plan template. Copy to `founder/product/scaffold-plan.md`.

## Hand-off

When the skeleton walks and the scaffold plan is written, hand the first slice to a coding agent, then move to `auth-and-billing` to wire managed signup and subscription billing into it. Pass along the stack from `founder/context.md`, the environments, the required env vars, and the core action. After the product is buildable, `launch-readiness` is the pass that hardens it for the first real users.
