# My Skills

A personal collection of installable agent skills and a catalog of useful skills from other authors.

## Global coding standards

Use a stable local checkout of `EduardoV-dev/my-skills` on `main` as the global source. From its root:

```bash
git pull --ff-only origin main
python3 skills/ev-coding-standards/assets/manage.py setup
```

Setup links every maintained skill into `~/.agents/skills/`, installs four command links under
`~/.config/opencode/commands/`, and maintains one delimited loader block in the existing global
`~/.config/opencode/AGENTS.md`. It preserves unrelated content and refuses installation collisions.
Rerunning setup is safe; it removes only retired skill links owned by this checkout.
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
| `/ev-update` | Require clean `main`, pull fast-forward only, validate, and reconcile global exposure. |
| `/ev-add-rule <rule>` | Pull before editing; contribute in an isolated worktree and reconcile concurrent upstream changes. |

Natural-language check/fix/update/add-rule requests use the same skill workflows. Keep the active
checkout on `main`; setup can expose uncommitted changes and reports that dirty state. Update and
add-rule refuse dirty work. Never switch the active checkout to an unmerged contribution branch.
If validation fails after an update pulls, report the checked-out revision and repair through a
contribution; no automatic reset is performed. Loaded instructions can remain stale until restart.

### Contribute a standard

1. Invoke `/ev-add-rule <rule>` or follow the [contribution workflow](skills/ev-coding-standards/references/add-rule.md).
   The helper pulls latest and creates a sibling `<repo-name>-worktrees/<slug>` on `rules/<slug>`.
2. Edit the existing rule owner there, preserving exceptions and updating coverage/docs when needed.
3. Validate before publication. Fetch and rebase unpublished work onto current `origin/main`;
   merge upstream into already-published branches. Resolve semantic conflicts and rerun checks.
4. Publish a normal-push PR when authorized. A conflicting policy or two unsuccessful reconciliation
   rounds stops the workflow with work preserved. No force pushes, resets, or auto-stashing.
5. After merge, run `/ev-update` to activate the contribution globally.

### Verify the setup

```bash
python3 skills/ev-coding-standards/assets/manage.py validate
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ev-coding-standards/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/ev-code-review/tests
npx skills add . --list
```

The setup tests use temporary homes and local Git remotes. They verify preservation/idempotence,
collision handling, safe synchronization, and isolated contribution branches. Agent rule selection
and semantic conflict resolution require behavioral verification; metadata checks cannot prove them.

## API implementation rules

Install `ev-api-contracts` to standardize first-party JSON API envelopes and pagination:

```bash
npx skills add EduardoV-dev/my-skills --skill ev-api-contracts
```

The skill requires shared `ApiError`/`ApiResponse<T>` contracts, wrapped offset/cursor pages, and
validated extensible cursor utilities. Before implementing pagination, it recommends a strategy and
waits for your choice. Review enforcement lives in `ev-code-review`'s backend rules and
`ev-review-typescript`; neither requires this implementation skill to be installed.

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
| `ev-review-nestjs` | NestJS injected-service naming, per-category module layout, and local `__tests__/` placement |
| `ev-review-postgres` | PostgreSQL privileged functions, safe resolution paths, and execution grants |
| `ev-review-supabase` | Supabase RLS/policies, cross-account isolation, and PostgREST filters |

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

Small or tightly coupled reviews run directly. Substantial, separable reviews may use up to three
parallel reviewers when the agent supports delegation. The coordinator verifies and deduplicates their
findings into one report; companions never spawn additional reviewers. Parallelism can reduce elapsed
time but generally uses more tokens. Reviews remain read-only unless fixes are requested.

## Repository layout

- `skills/` — skills maintained in this repository. Each skill lives in its own directory and starts with `SKILL.md`.
- `catalog/` — links and install commands for third-party skills; upstream repositories remain the source of truth.

All maintained skills use the `ev-` prefix, with matching directory and frontmatter names.

See [catalog/README.md](catalog/README.md) to add a third-party entry.
