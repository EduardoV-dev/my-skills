# My Skills

A personal collection of installable agent skills and a catalog of useful skills from other authors.

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
