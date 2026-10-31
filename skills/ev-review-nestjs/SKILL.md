---
name: ev-review-nestjs
description: "Trigger: NestJS or Nest.js code review with ev-code-review. Check injected-service naming, module layout, and local test folders."
license: Apache-2.0
metadata:
  author: "eduardovdev"
  version: "1.0"
---

# EV NestJS Review Rules

## Activation Contract

Use as an optional `ev-code-review` companion for scoped NestJS modules, classes, injection contracts,
and tests. Supply technology rules to the active review; do not start an independent review or delegate.

## Hard Rules

- Preserve the coordinator's scope, baseline, read-only constraints, and general/backend rules.
- Require every injected service property or constructor parameter to end in `Service`, such as
  `private readonly usersService: UsersService`. Apply the rule to constructor and property injection,
  including services injected through custom tokens or factory providers.
- Identify services by their actual provider contract and use, not merely an injection token or type
  name. Do not require a `Service` suffix for non-service dependencies such as repositories,
  configuration values, or clients; preserve framework-required names and external contracts.
- Prefer a flat module directory for categories containing one production file. When a category has
  two or more production files, group it in a dedicated plural folder such as `dtos/`, `docs/`,
  `services/`, `controllers/`, `types/`, `utils/`, `decorators/`, or `guards/`. Count files, not symbols,
  per category within its owning module; exclude tests and preserve nested module boundaries.
- Prefer tests in a `__tests__/` directory inside the production file's containing folder, even for
  one test: `users/users.service.ts` pairs with `users/__tests__/users.service.test.ts`, and
  `users/dtos/create-user.dto.ts` with `users/dtos/__tests__/create-user.dto.test.ts`.
  Preserve test filenames and existing `.test.ts` or `.spec.ts` conventions.
- Keep test fixtures directly beside their tests in the corresponding local `__tests__/` directory,
  such as `users/__tests__/users.fixture.ts`; do not add a `fixtures/` subfolder. Update fixture imports
  when recommending moves.

## Decision Gates

| Scoped code | Action |
| --- | --- |
| NestJS class with injected services | Check injected service identifiers for the `Service` suffix. |
| Custom injection token or factory provider | Trace the provider contract before classifying the dependency. |
| Non-service dependency or plain utility | Do not impose the injected-service naming rule. |
| One production file in a module category | Prefer the file at the module root; tests do not justify a category folder. |
| Multiple production files in a module category | Prefer a dedicated plural folder for that category only. |
| Test beside a production file | Prefer the containing folder's `__tests__/`, preserving the filename. |
| Test fixture outside its corresponding test folder or in a nested subfolder | Place it directly beside its tests in the local `__tests__/` directory. |

## Execution Steps

1. Identify scoped NestJS modules, file categories, tests, classes, injection points, and providers.
2. Trace ambiguous tokens and contracts; check service identifiers and their references, including tests.
3. Inspect owning folders to count production files per category and check local test and fixture placement.
4. Report naming and layout violations as low-severity style findings with the smallest consistent
   rename or move. Account for imports, exports, and test discovery when recommending moves; record
   unresolved contracts or discovery configuration as verification gaps.

## Output Contract

Return evidence-backed candidates with severity, `path:line`, rule wording, impact, and smallest fix,
plus a result for each assigned coverage ID: `NJ-001` injected provider classification/naming;
`NJ-002` per-category module layout; `NJ-003` local tests and fixtures. Each result must use the shared
status/evidence contract in `ev-code-review/references/coverage.md`. Let `ev-code-review` consolidate
the report.
