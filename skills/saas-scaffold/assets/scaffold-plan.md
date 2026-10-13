# Scaffold Plan — <product / core action>

_One page. Fill this in after `scripts/repo_scan.py` and keep it current. This is what a coding agent reads to know how to run and ship the project._

## Stack (inherited — do not re-decide here)

| Layer | Choice | Note |
| :-- | :-- | :-- |
| Framework | | from `founder/context.md` |
| Database + auth | | managed provider |
| Hosting | | |
| Payments | | managed provider (see `auth-and-billing`) |

## Environments

| Env | Database | Deploy trigger | URL |
| :-- | :-- | :-- | :-- |
| Local | | you run it | http://localhost:3000 |
| Preview | branch/throwaway DB, seeded | every push / PR | |
| Production | real DB, backed up | merge to main after CI | |

Rule: **preview and production never share a database.**

## Config / env-var contract

Every variable below must appear in `.env.example` with a placeholder. `.env` is gitignored; real values live in the platform secret store.

| Variable | Used by | Local | Preview/Prod |
| :-- | :-- | :-- | :-- |
| `DATABASE_URL` | app + migrations | local DB | managed DB |
| `APP_URL` | links, redirects | localhost | public URL |
| `<auth keys>` | auth provider | test project | live project |
| `<payment keys>` | billing | test keys | live keys |
| | | | |

## CI gates (fast → slow)

- [ ] Install + build from a clean clone
- [ ] Lint / typecheck
- [ ] Migrations apply against an empty database
- [ ] Tests (the acceptance checks for shipped slices)

## Deploy + rollback

- Deploy source: git commit on `main` (never a laptop directory)
- Rollback: <promote previous deployment / command> — **tried once?** [ ]
- Migrations on deploy: <ordered, replayable>
- Non-reversible migrations and their forward-fix: <list or "none yet">

## Migrations + tenancy

- Migration tool: <choice>
- Tenancy column on first table: `<tenant_id / workspace_id>` [ ]
- Row-level isolation policy: [ ]

## Walking skeleton — definition of done

- [ ] Core action works for one real user in production
- [ ] Reads/writes the real DB through real migrations
- [ ] Config from environment; fresh clone runs in one command
- [ ] Deploy from git; rollback tried once
- [ ] Health route up; CI green on main

## Repo scan snapshot

```
<paste the output of scripts/repo_scan.py — found/missing + coverage %>
```

## First slice for the coding agent

- **Acceptance criterion (verbatim from the spec):** <…>
- **Files/area it may touch:** <…>
- **Done check:** <command or observable behaviour>
- **Migration needed:** <file or none>
