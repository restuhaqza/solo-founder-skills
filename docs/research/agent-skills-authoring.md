# Agent Skills Authoring — Research Report

For building a suite of skills for solo founders. Covers the SKILL.md format, progressive
disclosure, triggering, skills-repo layout, common mistakes, and skills vs MCP vs plain prompts.

**Spec version note:** Agent Skills were released by Anthropic (Oct 16, 2025) and published as an
open standard on Dec 18, 2025 at [agentskills.io](https://agentskills.io). The format is now
supported by 25+ clients (Claude, Claude Code, OpenAI Codex/ChatGPT, Gemini CLI, Cursor, VS Code /
GitHub Copilot, OpenCode, Amp, Goose, Roo Code, etc.). Where Claude Code diverges from the base
spec, that is called out explicitly.

---

## 1. The exact `SKILL.md` structure

A skill is **a directory containing a `SKILL.md` file**. That is the entire mandatory surface area.

```
skill-name/
├── SKILL.md          # REQUIRED: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation loaded on demand
├── assets/           # Optional: templates, images, data files
└── ...               # Any additional files or directories
```

The `SKILL.md` file must have **YAML frontmatter** followed by a **Markdown body**. The opening
`---` must be the very first line of the file (Claude Code otherwise treats the whole file,
markers included, as content).

### Frontmatter fields (base Agent Skills spec)

| Field | Required | Constraints |
| :-- | :-- | :-- |
| `name` | **Yes** | Max 64 chars. Lowercase letters, numbers, hyphens only. Must not start/end with `-`. No consecutive `--`. Must match the parent directory name. No XML tags. No reserved words `anthropic` or `claude`. |
| `description` | **Yes** | 1–1024 chars, non-empty. No XML tags. Must state **what** the skill does **and when** to use it. |
| `license` | No | License name (SPDX, e.g. `MIT`, `Apache-2.0`) or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements (intended product, system packages, network access). Most skills don't need it. |
| `metadata` | No | A map of **string keys → string values**. Client-specific / arbitrary extra properties (author, version, category...). Use reasonably unique keys. |
| `allowed-tools` | No | **Experimental.** Space-separated string of pre-approved tools, e.g. `Bash(git:*) Bash(jq:*) Read`. Support varies by client. |

Minimal valid file:

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Example with optional fields:

```yaml
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
compatibility: Requires Python 3.14+ and uv
---
```

### Naming conventions

The `name` field is the identifier. Anthropic recommends **gerund form** (verb + -ing) because it
clearly describes the activity:

- **Good:** `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`, `testing-code`, `writing-documentation`
- **Acceptable:** noun phrases (`pdf-processing`, `spreadsheet-analysis`) or action-oriented (`process-pdfs`, `analyze-spreadsheets`)
- **Avoid:** `helper`, `utils`, `tools`, `documents`, `data`, `files`, `anthropic-helper`, `claude-tools`; and inconsistent patterns within one collection.

Valid name regex (OpenCode enforces this; matches the spec): `^[a-z0-9]+(-[a-z0-9]+)*$`

For a **solo-founder suite**, consistency matters more than the specific convention: pick gerund
form (or noun form) and apply it to every skill so the `/` menu reads as a coherent library.

### Length limits and token budgets

- **Frontmatter description:** hard cap 1024 chars (spec). (An older claude.ai help article says
  200 chars — that is a legacy/simplified guide; the spec and Claude docs say 1024. Treat 1024 as
  canonical but write tight.)
- **SKILL.md body:** keep **under ~500 lines** and **~5,000 tokens**. Move detail out when you
  approach this.
- **Level 1 metadata cost:** ~100 tokens per skill, always loaded. This is why you can install many
  skills cheaply — but each description competes for attention in the trigger decision.

### Where the description lives vs. "when to use"

Anthropic's own guidance (skill-creator): *all "when to use" information goes in the `description`,
not the body.* The body is instructions for once you're already activated.

### Claude Code vs the base spec (important for portability)

Claude Code **accepts the six spec fields** and adds many extensions. If you ever upload to
claude.ai / use the Skills API / package with `package_skill.py`, **only these six are allowed** —
any extra field is a *hard error*, not a warning:

> `Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name`

| Distribution path | Allowed frontmatter |
| :-- | :-- |
| Claude Code skills (any level) & plugin skills | Every field below |
| claude.ai upload, Skills API, `package_skill.py` | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` only |

Claude Code extras (portable skills should avoid these in the frontmatter and use `metadata`
instead, per the OpenCode guidance): `when_to_use`, `argument-hint`, `arguments`,
`disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`
(`fork`), `agent`, `background`, `hooks`, `paths`, `shell`. Note: Claude Code truncates the combined
`description` + `when_to_use` text at **1,536 chars** in the skill listing.

---

## 2. Progressive disclosure: SKILL.md vs references/ vs scripts/ vs assets/

Progressive disclosure is **the core design principle** of skills. It has three levels:

| Level | When loaded | Token cost | Content |
| :-- | :-- | :-- | :-- |
| **1. Metadata** | Always, at startup | ~100 tokens/skill | `name` + `description` from frontmatter |
| **2. Instructions** | When the skill is triggered | < 5k tokens recommended | The SKILL.md body |
| **3. Resources** | As needed | None until accessed | Bundled files. Reference files load into context when read; **scripts run through bash and only their output enters context.** |

Because files aren't loaded until accessed, there is **no practical limit on bundled content** —
you can ship comprehensive docs, datasets, and scripts that cost zero context until needed.

### What goes where

- **`SKILL.md`** — the table of contents + the core instructions the agent needs on *every* run.
  Keep it a "well-organized manual": overview, quick start, then pointers.
- **`references/`** — additional Markdown read on demand: `REFERENCE.md` (API reference),
  `FORMS.md` (structured formats), domain files (`finance.md`, `legal.md`, `aws.md`). Organize by
  domain so a task about sales doesn't load finance.
- **`scripts/`** — executable code for deterministic / repetitive tasks. Python, Bash, JS are
  common. The script's *code* never enters context; only its output does.
- **`assets/`** — static resources used in output: document templates, config templates, images,
  lookup tables, schemas.

### When to bundle a script vs write inline instructions

**Bundle a tested script when:**
- The operation is **deterministic / fragile** and must be consistent (sorting, PDF form filling, validation, chart building).
- The agent **reinvents the same logic across runs**. Anthropic's own heuristic: *"If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script."* Write it once, put it in `scripts/`, tell the skill to use it.
- It saves tokens (the code stays out of context) and time (no generation).

**Write inline instructions when:**
- The task is flexible / heuristic and multiple approaches are valid ("code review process").
- It's a short snippet the agent will run once.
- It's guidance/reference, not an operation.

**Write a one-off command (no `scripts/`) when** an existing CLI already does the job — prefer
version-pinned runners: `uvx ruff@0.8.0 check .`, `npx eslint@9 --fix .`, `pipx run 'black==24.10.0' .`,
`deno run npm:create-vite@6`, `go run ...@v0.28.0`. Only move to a bundled script when the command
becomes "hard to get right on the first try."

**Make the intent explicit.** Tell the agent whether to *execute* or *read* a file:

- Execute (most common): "Run `analyze_form.py` to extract fields."
- Read as reference: "See `analyze_form.py` for the field-extraction algorithm."

### Rules that keep progressive disclosure working

1. **Keep references one level deep** from SKILL.md. Agents may `head -100` previews of nested
   references and get incomplete info. `SKILL.md → advanced.md → details.md` is an anti-pattern.
2. **Put a table of contents at the top of reference files > 100 lines**, so a partial read still
   shows the full scope.
3. **Name files descriptively**: `form_validation_rules.md`, not `doc2.md`.
4. **Tell the agent *when* to load each file**: "Read `references/api-errors.md` if the API returns
   a non-200 status code" beats "see references/ for details."
5. **Use forward slashes** in all paths, relative to the skill root (`scripts/helper.py`).

### Scripts designed for agents

When an agent runs a script, it reads stdout/stderr to decide what to do next. Design for that:

- **No interactive prompts** — hard requirement; non-interactive shells hang forever waiting for input. Take input via flags/env/stdin, and error clearly: `Error: --env is required. Options: development, staging, production.`
- **`--help` output is the interface** — brief description, flags, usage examples.
- **Helpful error messages** — say what went wrong, what was expected, what to try ("Field
  'signature_date' not found. Available fields: ..."). Error text directly shapes the next attempt.
- **Structured output** — JSON/CSV/TSV. **Data → stdout, diagnostics → stderr.**
- **Self-contained dependencies** — Python [PEP 723](https://peps.python.org/pep-0723/) inline
  metadata run via `uv run scripts/x.py`; Deno `npm:`/`jsr:` imports; Bun auto-install; Ruby
  `bundler/inline`.
- **Idempotency, `--dry-run`, meaningful exit codes, safe defaults, predictable output size.**
- **Handle errors in-script ("solve, don't defer")** — don't `return open(path).read()` and let the
  agent figure it out.
- **No "voodoo constants"** — document why `TIMEOUT = 30`, not `TIMEOUT = 47`.

---

## 3. Writing descriptions that trigger reliably

### The undertriggering problem

Anthropic's own skill-creator states it plainly:

> *"currently Claude has a tendency to 'undertrigger' skills — to not use them when they'd be
> useful. To combat this, please make the skill descriptions a little bit 'pushy'."*

The description carries **the entire burden of triggering**. It is injected into the system prompt
and is what the model matches a request against. If it doesn't convey when the skill is useful, the
skill won't fire.

### Four principles (from agentskills.io)

1. **Use imperative phrasing.** Frame it as an instruction to the agent: *"Use this skill when…"*
   rather than *"This skill does…"*
2. **Focus on user intent, not implementation.** Describe what the *user* is trying to achieve.
3. **Err on the side of being pushy.** Explicitly list contexts where it applies, including cases
   where the user doesn't name the domain: *"even if they don't explicitly mention 'CSV' or 'analysis'."*
4. **Keep it concise.** A few sentences to a short paragraph. Hard limit 1024 chars.

Also: **write in third person.** The description is injected into the system prompt; inconsistent
point of view causes discovery problems.

> **Good:** "Processes Excel files and generates reports"
> **Avoid:** "I can help you process Excel files" / "You can use this to process Excel files"

### The "pushy" pattern — concrete before/after

**Before (undertriggers):**
```yaml
description: Process CSV files.
```

**After (pushy + specific + broad scope):**
```yaml
description: >
  Analyze CSV and tabular data files — compute summary statistics, add derived columns,
  generate charts, and clean messy data. Use this skill when the user has a CSV, TSV, or
  Excel file and wants to explore, transform, or visualize the data, even if they don't
  explicitly mention "CSV" or "analysis."
```

**Anthropic's own example of pushiness:**
> instead of *"How to build a simple fast dashboard to display internal Anthropic data."* →
> *"How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this
> skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to
> display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"*

### Good vs bad descriptions

**Good (what + when + key terms):**
```yaml
# PDF
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Excel
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.

# Git commit
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**Bad (vague — no trigger signal):**
```yaml
description: Helps with documents
description: Processes data
description: Does stuff with files
```

**Bad (too technical, no user triggers):**
```yaml
description: Implements the Project entity model with hierarchical relationships.
```

### A critical nuance

> *"Agents typically only consult skills for tasks that require knowledge or capabilities beyond
> what they can handle alone. A simple, one-step request like 'read this PDF' may not trigger a PDF
> skill even if the description matches perfectly."*

So a good description can't rescue a task the agent thinks it can do alone. **Test with substantive,
multi-step prompts**, not trivial ones.

### How to test and optimize triggering

1. **Build ~20 trigger eval queries** — 8–10 `should_trigger: true`, 8–10 `false`:
   ```json
   [
     {"query": "I've got a spreadsheet in ~/data/q4_results.xlsx with revenue in col C and expenses in col D — can you add a profit margin column and highlight anything under 10%?", "should_trigger": true},
     {"query": "whats the quickest way to convert this json file to yaml", "should_trigger": false}
   ]
   ```
2. **Make them realistic** — file paths, column names, backstory, casual language, typos, abbreviations.
   - Good: *"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx')..."*
   - Bad: *"Format this data"*, *"Extract text from PDF"*, *"Create a chart"*.
3. **Make negatives true near-misses.** `"Write a fibonacci function"` tests nothing. Strong negatives
   share keywords but need something else (e.g., "update the formulas in my Excel budget spreadsheet"
   for a CSV-analysis skill; "write a python script that reads a csv and uploads each row to postgres").
4. **Run each query 3×** and compute a **trigger rate** (fraction of runs where SKILL.md was loaded).
   A should-trigger query passes above ~0.5; a should-not-trigger query passes below ~0.5.
5. **Split 60% train / 40% validation.** Optimize on train failures only; select the best iteration
   by **validation** pass rate to avoid overfitting. Don't add keywords from failed queries — find the
   general concept and address that.
6. **Expect ~5 iterations.** If stuck, try a structurally different framing, not incremental tweaks.
7. **Fresh holdout** (5–10 never-used queries) as an honest final check.

The `skill-creator` skill automates this loop end-to-end (`scripts/run_loop.py`, `run_eval.py`).

---

## 4. Structuring a multi-skill collection / "skills repo"

### Repository layout (follows `anthropics/skills`)

```
my-solo-founder-skills/
├── README.md                       # human-facing catalog + install instructions
├── LICENSE                         # leave licensing unambiguous
├── .claude-plugin/
│   └── marketplace.json            # enables /plugin marketplace add owner/repo
├── skills/
│   ├── pricing-strategy/
│   │   └── SKILL.md
│   ├── fundraising-deck/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── investor-faq.md
│   │   └── assets/
│   │       └── deck-template.md
│   ├── customer-discovery/
│   │   └── SKILL.md
│   └── runway-forecasting/
│       ├── SKILL.md
│       └── scripts/
│           └── forecast.py
├── spec/                           # optionally vendor the standard
└── template/                       # a copy-paste starting point
```

One folder per skill, each self-contained, with `SKILL.md` at its root. Do **not** put a `SKILL.md`
directly at repo root — for a collection, the root is a catalog, not a skill.

### How they're installed and discovered

**Install as a marketplace (Claude Code):**
```
/plugin marketplace add <owner>/<repo>
/plugin install <plugin-name>@<marketplace-name>
```
Then the user invokes a skill by mention or by name (`/plugin-name:skill-name`).

**Discovery paths by client** (the spec defines the *format*, not the *installation path*):

| Client | Project path | Global path |
| :-- | :-- | :-- |
| Claude Code | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| OpenCode | `.opencode/skills/<name>/SKILL.md`, `.claude/skills/…`, `.agents/skills/…` | `~/.config/opencode/skills/…`, `~/.claude/skills/…`, `~/.agents/skills/…` |
| OpenAI Codex | `.agents/skills/` | — |
| Gemini CLI | `~/.gemini/...` | — |
| Cursor / VS Code / Copilot | per-client `.claude/skills` or client-specific | — |

OpenCode walks up from the CWD to the git worktree root, loading matching skills along the way.
Claude Code loads `.claude/skills/` from the start directory up to the repo root, plus nested
`.claude/skills/` once the agent touches files in a subdirectory.

**Marketplace manifest** — `.claude-plugin/marketplace.json` (pattern from `anthropics/skills`):
```json
{
  "name": "solo-founder-skills",
  "owner": { "name": "Your Name", "email": "you@example.com" },
  "metadata": { "description": "Skills for solo founders", "version": "1.0.0" },
  "plugins": [
    {
      "name": "founder-core",
      "description": "Pricing, fundraising, discovery, and runway workflows",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/pricing-strategy",
        "./skills/fundraising-deck",
        "./skills/customer-discovery",
        "./skills/runway-forecasting"
      ]
    }
  ]
}
```
Rules that trip people up: `source` paths are **relative to the marketplace root** (the dir
containing `.claude-plugin/`), must not contain `..`, and the entry `name` must match the plugin's
`plugin.json` name. Validate with `claude plugin validate ./dir`.

### Versioning

There is **no built-in `version` field** in the base spec, and none in Claude Code frontmatter.
Version via `metadata.version` string and/or git tags/releases on the repo. Review skill updates by
diff, like dependencies.

### README conventions for a skills repo

A good collection README (see `anthropics/skills`, `VoltAgent/awesome-agent-skills`) has:

1. Title + one-line positioning + a "hand-picked, not AI-slop" quality signal.
2. Badges (skills count, last-updated, license).
3. **Install** section (marketplace add + install, plus manual copy paths).
4. **What are skills** / compatibility table (which clients, which paths).
5. **Catalog** grouped by category (each entry: name, one-line description, link).
6. **Contributing** (how to add a skill, quality bar, naming rules).
7. **Security** warning (audit third-party skills, no permission bypasses, worktrees).
8. License / disclaimer.

See §7 for a fill-in template.

---

## 5. Common mistakes and how to avoid them

**Content & clarity**
- **Vague descriptions / missing triggers.** Always state what + when; be specific and pushy. Test trigger rates.
- **Too verbose.** The default assumption: *Claude is already smart*. Cut anything Claude already knows ("PDFs are a common file format..."). Ask of each line: *"Does this justify its token cost?"*
- **Over-explaining (Opus) vs under-explaining (Haiku).** Test with all models you'll use.
- **Menu of options instead of a default.** Pick one default + an escape hatch, not "you can use pypdf, pdfplumber, PyMuPDF...".
- **Declaring a specific answer instead of a general method.** Teach the *approach*, not the output for one instance.
- **Time-sensitive information.** Put it in an `<details>` "Old patterns" section, not the main content.
- **Inconsistent terminology** (endpoint/URL/route/path). Pick one term and stick to it.
- **Deeply nested references.** Keep one level deep; add a TOC to long files.
- **Heavy-handed ALL-CAPS MUSTs.** Explain the *why*; models follow reasoning-based instructions more reliably than rigid directives. If you're writing ALWAYS/NEVER in all caps, that's a yellow flag.
- **Overfit to test cases.** Generalize from feedback; don't bolt on satisfiers for three examples.

**Code & scripts**
- **Scripts that defer to Claude** instead of handling errors.
- **Voodoo constants** with no justification.
- **Assuming packages are installed.** List dependencies; verify availability. API containers have **no network and no runtime installs** — pre-installed only. Claude.ai can install from npm/PyPI; Claude Code has full network access (install locally only).
- **Windows-style paths** (`scripts\helper.py`) — always forward slashes.
- **Interactive scripts** — they hang in non-interactive agent shells.
- **No validation / feedback loops** for quality-critical or destructive work. Use plan-validate-execute.

**Distribution**
- **Non-spec frontmatter fields** on claude.ai upload / Skills API → hard error. Keep to the six fields for portability; put client extras in `metadata`.
- **Directory name ≠ `name` field.** They must match.
- **No evals.** Create at least three test cases; run with-skill vs baseline.
- **Ignoring security.** *"Install skills only from trusted sources."* Audit third-party SKILL.md, scripts, images; watch for unexpected network calls, data exfiltration, and instructions telling Claude to reach untrusted sources. Skills can invoke tools/execute code.
- **Everything in one giant skill.** *"Multiple focused skills compose better than one large skill."* But don't over-fragment either — too narrow forces many skills to co-load and can conflict.

**Evaluation anti-patterns**
- Assertions that always pass regardless of skill (non-discriminating) — remove them.
- Assertions that always fail — broken assertion or too-hard case.
- Subjective qualities (writing style, design) shouldn't be forced into pass/fail assertions; review those with a human.

---

## 6. Claude Skills vs OpenCode skills vs MCP servers/tools

### Format differences

| Dimension | Claude Skills / Agent Skills | OpenCode skills | MCP servers/tools |
| :-- | :-- | :-- | :-- |
| What it is | A folder + `SKILL.md` (metadata + instructions + optional scripts/assets) | Same format (implements the open standard) | A server exposing tools/resources/prompts over a protocol |
| Frontmatter | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` | Same spec fields + OpenCode keys in `metadata` (`opencode/slash`, `opencode/autoinvoke`) | N/A (tool schemas instead) |
| Loading | Progressive disclosure: metadata always, body on trigger, resources on demand | Same; `skill` tool description lists `<available_skills>`; agent calls `skill({name})` | Tools registered up-front; schemas consume context always |
| Discovery paths | `.claude/skills/`, `~/.claude/skills/`, plugins | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` (+ global) | Client MCP config |
| Extras | Claude Code adds `when_to_use`, `context: fork`, `allowed-tools`, `hooks`, `paths`, `disable-model-invocation`, dynamic context injection `` !`cmd` `` | `metadata["opencode/autoinvoke"]="false"` hides from auto-selection; `metadata["opencode/slash"]="true"` exposes `/name` | N/A |
| Permissions | Claude Code permission flows; `allowed-tools` pre-approval | `opencode.json` `permission.skill` patterns (`allow`/`deny`/`ask`, wildcards) | Server-level scopes |

### Skill vs MCP tool vs plain prompt — when to use which

- **Plain prompt** — one-off, conversation-level instruction. No reuse, no filesystem, no code.
  Use for a single task. *"Unlike prompts, Skills load on demand, so you don't have to repeat the
  same guidance across conversations."*
- **Skill** — **procedural knowledge / domain expertise**: workflows, conventions, checklists,
  project-specific context, and deterministic bundled code. Filesystem-based, portable across
  clients, composable. Use when you keep pasting the same instructions or a CLAUDE.md section has
  grown into a *procedure*. Anthropic: *"Skills are passive: they don't decide when to fire or in
  what order."*
- **MCP tool** — **connectivity**: reaching external systems (databases, APIs, SaaS) that the agent
  can't otherwise access. Tools are stateless capabilities; schemas load into context every time.
  Use when you need to *do* something in an external system.

**They compose.** Anthropic: *"Skills can complement MCP servers by teaching agents more complex
workflows that involve external tools."* A skill can contain the *workflow/policy* and call MCP
tools via **fully qualified names** (`ServerName:tool_name`, e.g. `GitHub:create_issue`) to avoid
"tool not found."

Decision heuristic for a solo-founder suite:
- Repeating a *procedure/convention* → **skill**.
- Need to *read/write an external service* → **MCP server**, possibly wrapped by a skill that
  explains *when* and *how* to use it.
- A one-time instruction → **prompt**.

**Where each runs (same skill, different surfaces):**
- **Claude API:** sandboxed container, **no network, no runtime installs**, needs the code-execution tool. Not ZDR-covered.
- **claude.ai:** network varies by settings; can install npm/PyPI packages; individual-user only.
- **Claude Code:** filesystem-based, often full network; prefers local-only installs. Not synced across surfaces.
- Custom skills do **not** sync across surfaces — manage per surface.

---

## 7. Templates

### 7.1 Template `SKILL.md`

Keep the frontmatter to the six portable fields for a distributable collection. Put everything
else in the body or in `metadata`.

```markdown
---
name: <gerund-or-noun-form-kebab-case>
description: <What it does, in third person, with key terms.> Use this skill when <specific trigger contexts, including cases where the user doesn't name the domain directly>. <Optional pushy clause: "even if they don't explicitly ask for X".>
license: MIT
compatibility: <Optional. e.g. "Requires Python 3.11+ and uv". Omit if none.>
metadata:
  author: <you>
  version: "1.0.0"
  category: <e.g. finance | gtm | product>
allowed-tools: <Optional/experimental, e.g. "Read Bash(python:*)">
---

# <Skill Name>

<One or two sentences on the outcome this skill produces and the situation it fits.>

## Quick start

<The shortest path to a good result. Include a concrete default command or snippet.>

```bash
python scripts/<script>.py --input <path> --output <path>
```

## When to use this

<Bullet list of concrete user situations. Redundant with the description is fine — it reinforces.>

## Workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: <verb + object>
- [ ] Step 2: <verb + object (run scripts/validate.py)>
- [ ] Step 3: <verb + object>
- [ ] Step 4: Verify (<run scripts/verify.py> or compare to references/<doc>.md)
```

**Step 1: <Name>**
<What to do and why it matters.>

**Step 2: <Name>**
<What to do. If validation fails, fix and repeat before moving on.>

**Step 3: <Name>**
<What to do.>

**Step 4: Verify**
<How to confirm success. State what "good" looks like.>

## Gotchas

- <Environment-specific fact that defies reasonable assumptions, e.g. "The `users` table uses soft deletes; always include `WHERE deleted_at IS NULL`.">
- <One field's name differs across services.>
- <A "healthy" signal that is misleading, plus the correct one to use.>

## Output format

ALWAYS use this exact structure (or "Use this as a sensible default, adapting as needed"):

```markdown
# <Title>
## Executive summary
<...>
## Key findings
- <...>
## Recommendations
1. <...>
```

## Examples

**Example 1:**
Input: <realistic input>
Output:
```
<desired output>
```

## Available scripts

- **`scripts/<script>.py`** — <what it does>. Run: `python scripts/<script>.py <args>`
- **`scripts/validate.py`** — <what it checks>. Returns "OK" or lists conflicts.

## Reference files

- **`references/<doc>.md`** — <what it covers>. Read when <precise trigger>.
- **`assets/<template>`** — <what it is>. Use when <precise trigger>.
```

**Checklist before shipping a skill** (from Anthropic):
- [ ] Description is specific, includes key terms, and states what + when
- [ ] SKILL.md body < 500 lines; extra detail in separate files
- [ ] No time-sensitive info (or in an "Old patterns" section)
- [ ] Consistent terminology; concrete examples; file references one level deep
- [ ] Workflows have clear steps; validation/feedback loops for critical ops
- [ ] Scripts solve problems, handle errors, no magic numbers, forward slashes
- [ ] Required packages listed and verified
- [ ] ≥3 evals created; tested with the models you'll use; tested on real scenarios
- [ ] Description trigger-tested (should/shouldn't fire)

### 7.2 Template: skills-repo `README.md`

```markdown
<h1 align="center">Solo Founder Skills</h1>
<p align="center"><em>Agent Skills that turn a general-purpose agent into a solo-founder operator.</em></p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/Skills-12-blue?style=flat-square">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green?style=flat-square">
  <img alt="Last update" src="https://img.shields.io/github/last-commit/<owner>/<repo>?style=flat-square">
</p>

A focused collection of [Agent Skills](https://agentskills.io) for founders who run everything
alone — pricing, fundraising, customer discovery, runway, launch, and more. Built on the open
Agent Skills standard, so they work across Claude Code, Codex, Gemini CLI, Cursor, VS Code, and
OpenCode.

## Install

**Claude Code (marketplace):**
```
/plugin marketplace add <owner>/<repo>
/plugin install founder-core@solo-founder-skills
```

**Manual (any Agent Skills client):** copy a skill folder into your skills directory.
```
# Claude Code / Cursor / Copilot
cp -r skills/pricing-strategy ~/.claude/skills/
# OpenCode
cp -r skills/pricing-strategy ~/.config/opencode/skills/
# Codex / generic
cp -r skills/pricing-strategy ~/.agents/skills/
```

## What are Agent Skills?

A skill is a folder with a `SKILL.md` file: YAML metadata (`name`, `description`) plus Markdown
instructions and optional `scripts/`, `references/`, and `assets/`. Agents load only the name and
description at startup, activate the full skill when a task matches, and load bundled resources
on demand — so you can install many skills at almost no context cost.

## Catalog

### Strategy & Finance
| Skill | What it does |
| :-- | :-- |
| [`pricing-strategy`](skills/pricing-strategy) | Design and pressure-test pricing/packaging for a new or existing product. |
| [`runway-forecasting`](skills/runway-forecasting) | Build and stress-test a runway model from revenue and burn inputs. |

### Fundraising
| Skill | What it does |
| :-- | :-- |
| [`fundraising-deck`](skills/fundraising-deck) | Draft and refine an investor deck narrative, section by section. |

### Go-to-Market
| Skill | What it does |
| :-- | :-- |
| [`customer-discovery`](skills/customer-discovery) | Turn raw interview notes into themes, evidence, and next questions. |

*(Add one table per category. Each row: linked folder name + one-line outcome.)*

## Skill format at a glance

```
skills/<name>/
├── SKILL.md        # required: frontmatter (name, description) + instructions
├── references/     # optional: docs loaded on demand
├── scripts/        # optional: executable code (runs without loading into context)
└── assets/         # optional: templates, images, data
```

## Contributing

1. Create `skills/<kebab-case-name>/SKILL.md` (directory name must match the `name` field).
2. Frontmatter: `name` + `description` (what + when, in third person). Optional portable fields:
   `license`, `compatibility`, `metadata`, `allowed-tools`.
3. Keep the body under ~500 lines; move detail into `references/` with a "read when…" pointer.
4. Add `evals/evals.json` with ≥3 realistic prompts; test trigger rates (should/shouldn't fire).
5. Run `skills-ref validate ./skills/<name>` and open a PR describing the gap it fills.

Quality bar: a skill must capture **project-specific expertise** (a real workflow, real edge
cases), not generic advice an LLM already knows.

## Security

Skills can include instructions and executable code. Install only from trusted sources; audit
third-party `SKILL.md`, scripts, and assets before enabling them; never disable permission
prompts outside a sandbox; run agents in isolated git worktrees; review skill updates by diff
like dependencies.

## License

MIT (see `LICENSE`). Individual skills may carry their own `license` frontmatter.
```

---

## 8. Source URLs

**Primary (Anthropic / standard)**
- Engineering blog — *Equipping agents for the real world with Agent Skills*: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Agent Skills overview (Claude Platform Docs): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **Skill authoring best practices** (canonical): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Agent Skills open standard: https://agentskills.io
  - Specification: https://agentskills.io/specification
  - Best practices for skill creators: https://agentskills.io/skill-creation/best-practices
  - Optimizing descriptions (triggering): https://agentskills.io/skill-creation/optimizing-descriptions
  - Evaluating skill output quality: https://agentskills.io/skill-creation/evaluating-skills
  - Using scripts in skills: https://agentskills.io/skill-creation/using-scripts
- `anthropics/skills` repo (reference skills, spec, template, marketplace.json): https://github.com/anthropics/skills
  - `template/SKILL.md`: https://github.com/anthropics/skills/blob/main/template/SKILL.md
  - `skill-creator` (authoring/eval automation): https://github.com/anthropics/skills/tree/main/skills/skill-creator
  - Marketplace manifest: https://github.com/anthropics/skills/blob/main/.claude-plugin/marketplace.json
- Claude Code — Extend Claude with skills (frontmatter reference, paths, extensions): https://code.claude.com/docs/en/skills
- Claude Code — Create a marketplace: https://code.claude.com/docs/en/plugin-marketplaces
- Help Center — How to create custom skills: https://support.claude.com/en/articles/12512198-creating-custom-skills
- The Complete Guide to Building Skills for Claude (PDF): https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Skills API quickstart: https://docs.claude.com/en/api/skills-guide

**OpenCode**
- Agent Skills docs: https://opencode.ai/docs/skills/

**Community collections / meta**
- VoltAgent `awesome-agent-skills`: https://github.com/VoltAgent/awesome-agent-skills
- `obviousworks/Claude-AI-skills-collection-2026`: https://github.com/obviousworks/Claude-AI-skills-collection-2026
- GitHub topic `skills`: https://github.com/topics/skills
- `skills.sh` / `officialskills.sh` — skill index referenced by `anthropics/skills`

**Deep-dives used for corroboration**
- Claude Skills Deep Dive (leehanchung): https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive
- hidekazu-konishi complete guide: https://hidekazu-konishi.com/entry/claude_code_skills_complete_guide.html
- Agent Skills open standard interoperability: https://www.paperclipped.de/en/blog/agent-skills-open-standard-interoperability
