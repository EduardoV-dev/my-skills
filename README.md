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
     --skill ev-code-rules
   ```

   Select the technology companions your project needs; see [available companions](#install-coding-rule-skills).
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

EV skills can be used alongside third-party skills without requiring them. Applicable compatible
instructions compose; instruction hierarchy and project guidance still apply. If instructions cannot
be reconciled, the agent identifies the conflict and requests a decision before the affected action.
Existing EV rules remain in force.

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

Shared formatting rules include [`general-logical-code-grouping`](skills/ev-code-rules/references/logical-code-grouping.md):
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

Setup links every maintained skill into `~/.agents/skills/` and maintains one delimited loader block
in the existing global `~/.config/opencode/AGENTS.md`. It preserves unrelated content and refuses installation collisions.
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

Ask the matching skill in natural language for standards checks, cleanup, simplification, or updates.
Only an explicitly requested checkout-backed setup/update needs source Git access. Keep that checkout on `main`; setup can expose
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
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ev-project-setup/tests
npx skills add . --list
```

The setup tests use temporary homes and local Git remotes. They verify preservation/idempotence,
collision handling, portable loaders, retired-command cleanup, and safe synchronization. Agent rule selection
and semantic conflict resolution require behavioral verification; metadata checks cannot prove them.
Project wiring tests additionally cover byte-preserving updates, malformed markers, symlinks,
paths containing spaces, and read-only drift detection.

## Code cleanup

Install the cleanup skills alongside the EV coding core:

```bash
npx skills add EduardoV-dev/my-skills \
  --skill ev-coding-standards --skill ev-code-rules \
  --skill ev-dead-code --skill ev-code-simplification
```

Ask `ev-dead-code` to find or remove unused code, or `ev-code-simplification` to find or remove
duplication and simplify existing code. Finding candidates is read-only; removal requires a request.
Both retain uncertain cases and report verification gaps. Installed third-party skills are optional.

## API implementation rules

Install `ev-api-contracts` to standardize first-party JSON API envelopes, optimistic locking, and pagination:

```bash
npx skills add EduardoV-dev/my-skills --skill ev-api-contracts
```

The skill requires shared `ApiError`/`ApiResponse<T>` contracts, wrapped offset/cursor pages, and
validated extensible cursor utilities. Before implementing pagination, it recommends a strategy and
waits for your choice. Related coding rules live in `ev-code-rules`'s backend rules and
`ev-typescript-rules`; neither requires this implementation skill to be installed.
Cursor metadata requires `nextCursor: string | null` and `resetCursor: boolean`; true invalidates the
current pagination chain and tells clients to discard accumulated pages/cursors and restart without
a cursor. Ordinary empty/final pages use false; backward navigation adds `prevCursor` only on request.
Health-check endpoints, including liveness/readiness, return the shared `HealthResponse` directly:
`{ status: "ok" | "degraded" | "down", checks: Record<string, "up" | "down"> }`.
All checks up yields HTTP 200; mixed or all-down results yield HTTP 503. Health responses do not use
the ordinary envelope; `ApiResponse<T>` stays strict for ordinary endpoints.

Choose the simplest concurrency mechanism that preserves the business invariant: standard updates for
acceptable last-write-wins, atomic relative or conditional updates for database invariants, optimistic
locking for stale user edits, and transactions with pessimistic locking when needed for dependent work.
For optimistic updates, including PATCH, require a last-read token: prefer a suitable integer version,
otherwise use `lastKnownUpdatedAt`. The database atomically matches identity, authorization scope, and
the token; a failed match returns HTTP 409 with a refresh instruction, preserving existing access/not-found
policy. Successful writes advance and return the exact new token. For JavaScript/PostgreSQL applications,
`ev-postgres` covers `timestamptz(3)`, a monotonic update trigger, and transaction/locking rules. See the
[optimistic-locking contract](skills/ev-api-contracts/references/optimistic-locking.md)
and [NestJS DTO example](skills/ev-nestjs-rules/references/http.md#require-an-optimistic-locking-token-on-updates).

## Install coding rule skills

After publishing this repository on GitHub, run this from the target project for interactive selection:

```bash
npx skills add EduardoV-dev/my-skills
```

Select **`ev-code-rules`** and only the technology companions the project needs. The CLI does not
automatically select the core when you select a companion.

| Skill | Coverage |
| --- | --- |
| `ev-code-rules` | General code/security rules and frontend/backend rules |
| `ev-typescript-rules` | TypeScript contracts, narrowing, and environment-module conventions |
| `ev-react-rules` | React components, hooks, state, safe rendering, and applicable UI testing |
| `ev-nextjs-rules` | Next.js routes, rendering, Server Actions, and client/server environment boundaries |
| `ev-nestjs-rules` | NestJS plural grouping, validated body DTOs, optimistic locking, global validation, `/api`, OpenAPI/Scalar at `/docs`, health contracts, injected-service naming, and test ownership |
| `ev-postgres` | PostgreSQL timestamp precision, optimistic and pessimistic locking, and transaction boundaries |

For explicit selection, for example in a React + TypeScript project:

```bash
npx skills add EduardoV-dev/my-skills \
  --skill ev-code-rules \
  --skill ev-typescript-rules \
  --skill ev-react-rules
```

List skills without installing:

```bash
npx skills add EduardoV-dev/my-skills --list
```

Before publishing, verify discovery locally from this repository with `npx skills add . --list`.

## How coding rules are selected

`ev-coding-standards` loads general rules and applicable frontend, backend, and technology rules based
on the code being changed. Explicit standards checks use the same rules; use other skills for functional
code reviews. Load newly applicable guidance when the scope changes, and run relevant project checks.

See [implementation checks](skills/ev-code-rules/references/generation-review.md) and
[workflow verification](skills/ev-code-rules/references/generation-verification.md).

## Repository layout

- `skills/` — skills maintained in this repository. Each skill lives in its own directory and starts with `SKILL.md`.
- `CATALOG.md` — links and install commands for third-party skills; upstream repositories remain the source of truth.

All maintained skills use the `ev-` prefix, with matching directory and frontmatter names.

See [CATALOG.md](CATALOG.md) to add a third-party entry.
