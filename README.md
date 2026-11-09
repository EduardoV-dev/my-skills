# My Skills

A collection of reusable agent skills for code generation, review, and task-specific workflows in
any project, plus a catalog of useful skills from other authors. Coding and review share the same
rules: standards apply before implementation, not only when a review is requested.

## Wire skills into a project

1. From the target project, install the setup skill and coding core for your agent:

   ```bash
   npx skills add EduardoV-dev/my-skills \
     --skill ev-project-setup \
     --skill ev-coding-standards \
     --skill ev-code-review
   ```

   Select the technology companions your project needs; see [available companions](#install-review-skills).
   Existing global installations can also supply these skills; a second installation is not required.
2. Quit and restart your agent, then ask: **“Use ev-project-setup to wire the installed skills into
   this project.”** It resolves available skills, checks project guidance, and adds one managed block
   to the project's root `AGENTS.md`, preserving unrelated instructions. It also ensures the project's
   `.gitignore` contains `__pycache__/` and `*.py[cod]` to exclude Python skill artifacts.
3. Start a fresh session (quit and restart OpenCode). Request your normal task: matching skills must
   load before work, including coding standards before edits and relevant rules when scope changes.

The block selects skills by their activation descriptions, so future installed skills can apply to
documentation, testing, or other tasks without rewriting the loader. It does not load every skill
body every session. Project-local skills take precedence; missing required guidance and policy
conflicts are surfaced before affected edits. Setup does not silently install or overwrite skills.

Installed skills are self-contained: the agent loads their bundled rules and references directly.
Normal coding, review, check/fix, and project wiring do not require a clone of this repository,
search for its local path, or inspect its Git state. References resolve relative to each selected
installed skill; unavailable source revisions do not block work.

The helper can also maintain/check the block directly once the core skills are available:

```bash
python3 <installed-ev-project-setup>/assets/setup_project.py "/path/to/project"
python3 <installed-ev-project-setup>/assets/setup_project.py "/path/to/project" --check
```

It requires Python 3 and an existing target directory. `--check` is read-only and returns 1 for
missing/outdated wiring or ignore entries, or errors. The helper manages instructions and these two
ignore entries; it does not verify skill availability or agent compliance.
See [setup and behavioral checks](skills/ev-project-setup/references/setup.md).
This adapter applies to agents that read `AGENTS.md`; other instruction formats need their own adapter.
The global OpenCode setup below is separate and remains useful for personal defaults across projects.

Shared formatting rules include [`general-logical-code-grouping`](skills/ev-code-review/references/logical-code-grouping.md):
separate meaningful processing phases while keeping related statements together. Setup and pre-coding
inspect the target project's existing formatter/linter for compatible enforcement; semantic grouping
uses coding judgment during implementation and is assessed fully during requested reviews.

## Global coding standards

For optional checkout-backed global OpenCode setup, use a stable local checkout of
`EduardoV-dev/my-skills` on `main`. This is a maintenance choice, not a requirement for using skills
installed through the Skills CLI. From the checkout root:

```bash
git pull --ff-only origin main
python3 skills/ev-coding-standards/assets/manage.py setup
```

Setup links every maintained skill into `~/.agents/skills/`, installs three command links under
`~/.config/opencode/commands/`, and maintains one delimited loader block in the existing global
`~/.config/opencode/AGENTS.md`. It preserves unrelated content and refuses installation collisions.
Rerunning setup is safe; it removes only retired skill and command links owned by this checkout,
including broken retired command links in OpenCode's `commands/` and `command/` directories.
The global loader resolves installed skills without embedding this checkout's absolute path.
Python 3 and Git are required; Skills CLI discovery additionally requires Node/npm.

**Quit and restart OpenCode after setup or update.** Skill discovery does not load rule bodies:
the global loader requires `ev-coding-standards` before code edits. It selects complete general,
frontend/backend, and applicable technology rules based on actual scoped usage, including
`ev-api-contracts` for API implementation. The same standards are reused for review.
Project-local same-name skills still take precedence and are reported explicitly; policy conflicts
and missing required guidance must be resolved before affected edits. Unknown technologies are
coverage gaps, not permission to invent rules. Other agents can discover `~/.agents/skills/`, but
need their own global-instruction adapter to require loading before editing.

| OpenCode command | Workflow |
| --- | --- |
| `/ev-check [scope]` | Read-only standards review; defaults to working-tree changes, not the last commit. |
| `/ev-fix [scope]` | Check, minimally fix evidenced scoped violations, verify, and recheck. |
| `/ev-update` | Explicit checkout-backed update: require clean `main`, pull fast-forward only, validate, and reconcile global exposure. Standalone copies need their original installer. |

Natural-language check/fix/update requests use the same skill workflows. Only an explicitly requested
checkout-backed setup/update needs source Git access. Keep that checkout on `main`; setup can expose
uncommitted changes and reports its dirty state. Update refuses dirty, diverged, or unpublished work.
For standalone installed copies, the agent reports that the repository update helper is unavailable
and requests reinstallation through the original installer/scope; it does not search for or clone a
separate checkout. If validation fails after pulling, the revision remains checked out for manual
repair; no automatic reset is performed. Loaded instructions can remain stale until restart.

### Maintain rules manually

1. Edit the owning skill under `skills/`, following `AGENTS.md`. Align affected references, templates,
   examples, contracts, tests, and documentation; preserve existing exceptions and unrelated work.
2. Run the verification commands below and inspect the diff. Commit/publish only when intended.
3. Update installations through their existing installation method, then restart the agent. Existing
   checkout-backed symlinks expose edited files immediately, but running sessions retain loaded text.

### Verify the setup

```bash
python3 skills/ev-coding-standards/assets/manage.py validate
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ev-coding-standards/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ev-code-review/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ev-project-setup/tests
npx skills add . --list
```

The setup tests use temporary homes and local Git remotes. They verify preservation/idempotence,
collision handling, portable loaders, retired-command cleanup, and safe synchronization. Agent rule selection
and semantic conflict resolution require behavioral verification; metadata checks cannot prove them.
Project wiring tests additionally cover byte-preserving updates, malformed markers, symlinks,
paths containing spaces, and read-only drift detection.

## API implementation rules

Install `ev-api-contracts` to standardize first-party JSON API envelopes, optimistic locking, and pagination:

```bash
npx skills add EduardoV-dev/my-skills --skill ev-api-contracts
```

The skill requires shared `ApiError`/`ApiResponse<T>` contracts, wrapped offset/cursor pages, and
validated extensible cursor utilities. Before implementing pagination, it recommends a strategy and
waits for your choice. Review enforcement lives in `ev-code-review`'s backend rules and
`ev-review-typescript`; neither requires this implementation skill to be installed.
Cursor metadata requires `nextCursor: string | null` and `resetCursor: boolean`; true invalidates the
current pagination chain and tells clients to discard accumulated pages/cursors and restart without
a cursor. Ordinary empty/final pages use false; backward navigation adds `prevCursor` only on request.
Health-check endpoints, including liveness/readiness, return the shared `HealthResponse` directly:
`{ status: "ok" | "degraded" | "down", checks: Record<string, "up" | "down"> }`.
All checks up yields HTTP 200; mixed or all-down results yield HTTP 503. Health responses do not use
the ordinary envelope; `ApiResponse<T>` stays strict for ordinary endpoints.

Resource updates, including PATCH, require `lastKnownUpdatedAt` with the last-read resource timestamp.
The database update atomically matches identity, authorization scope, and `updated_at` against that
token; a failed match returns HTTP 409 with a refresh instruction, preserving existing access/not-found
policy. Successful writes advance the server-owned timestamp and return its exact new value. Preserve
microseconds throughout the round trip. See the [optimistic-locking contract](skills/ev-api-contracts/references/optimistic-locking.md)
and [NestJS DTO example](skills/ev-review-nestjs/references/http.md#require-an-optimistic-locking-token-on-updates).

## Install review skills

After publishing this repository on GitHub, run this from the target project for interactive selection:

```bash
npx skills add EduardoV-dev/my-skills
```

Select **`ev-code-review`** and only the technology companions the project needs. The CLI does not
automatically select the core when you select a companion.

| Skill | Coverage |
| --- | --- |
| `ev-code-review` | General code/security rules, frontend/backend rules, scope and review coordination |
| `ev-review-typescript` | TypeScript contracts, narrowing, and environment-module conventions |
| `ev-review-react` | React components, hooks, state, safe rendering, and applicable UI testing |
| `ev-review-nextjs` | Next.js routes, rendering, Server Actions, and client/server environment boundaries |
| `ev-review-nestjs` | NestJS plural grouping, validated body DTOs, optimistic locking, global validation, `/api`, OpenAPI/Scalar at `/docs`, health contracts, injected-service naming, and test ownership |

For explicit selection, for example in a React + TypeScript project:

```bash
npx skills add EduardoV-dev/my-skills \
  --skill ev-code-review \
  --skill ev-review-typescript \
  --skill ev-review-react
```

List skills without installing:

```bash
npx skills add EduardoV-dev/my-skills --list
```

Before publishing, verify discovery locally from this repository with `npx skills add . --list`.

## How reviews select rules

The core always reads general rules, then selects frontend/backend rules per file's behavior and
runtime. It loads installed technology companions only for relevant scoped code—not merely because
a dependency appears in a manifest. Mixed files receive both domain rule sets; tests follow their subject.

Missing companions are reported as technology-specific coverage gaps. The core continues reviewing
with its bundled rules and does not install anything automatically. Add a companion when that coverage
is needed. Keep optional companions alongside the core in the same installation scope when possible.

Reviews run in the current agent thread regardless of size. The coordinator evaluates applicable
general, domain, and technology checks sequentially and consolidates them into one report. Maintained
skills do not spawn subagents or parallel reviewers. Reviews remain read-only unless fixes are
requested.

Explicit review/check/fix requests display every finding directly in chat, ordered by severity, with
location, violated rule, evidence, impact, and minimal fix. Fix reports include fixed/remaining status
and verification evidence. Findings are never limited to five or a top-N subset. During code generation,
standards guide implementation and relevant project checks run without automatic code review;
unresolved blockers, required decisions, and material verification gaps are still surfaced.

### Coding guidance now, complete review on request

Implementation uses the full applicable rules as guidance, without a mandatory review pass:

1. Load complete applicable guidance once per active context; reuse unchanged text and load missing,
   changed, or newly applicable guidance before affected work.
2. Implement the requested behavior and run relevant tests, lint/format checks, type checks, and builds.
   Check affected consumers and integration; reuse results only while they cover the completed state.
3. Report what works, performed checks, and material gaps. Do not require unit-review checkpoints,
   per-rule review-evidence ledgers, or final review-coverage reconciliation.

Request a complete review when the changes meet your expectations and work, or earlier if you want
feedback. Explicit reviews assess their entire requested scope using formal coverage and exhaustive
reporting; implementation checks do not substitute for that review or prove full compliance.
After compaction, verify current sources/changes and retained check results, and reload missing full rules.
See [implementation checks](skills/ev-code-review/references/generation-review.md) and
[behavioral regression and cost checks](skills/ev-code-review/references/generation-verification.md).
Metadata/helper tests do not establish agent compliance, speed gains, or defect-detection parity.

## Repository layout

- `skills/` — skills maintained in this repository. Each skill lives in its own directory and starts with `SKILL.md`.
- `CATALOG.md` — links and install commands for third-party skills; upstream repositories remain the source of truth.

All maintained skills use the `ev-` prefix, with matching directory and frontmatter names.

See [CATALOG.md](CATALOG.md) to add a third-party entry.
