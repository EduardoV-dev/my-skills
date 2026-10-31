# Review Coverage Contract

Build the plan before assigning review work. Select only applicable checks; record why a category is
`NOT_APPLICABLE` rather than omitting it. IDs are stable categories, not a claim that every individual
rule was mechanically proven.

## Check inventory

| Reviewer | Check IDs and scope |
| --- | --- |
| `core` | `GEN-001` ownership/structure; `GEN-002` correctness/naming/boundaries; `GEN-003` configuration/async/side effects; `GEN-004` errors/trust boundaries/security; `GEN-005` tests and deterministic checks |
| `frontend` | `FE-001` UI boundaries/state/rendering; `FE-002` XSS/URL/browser security; `FE-003` accessibility; `FE-004` performance |
| `backend` | `BE-001` input validation/errors; `BE-002` API contracts/pagination; `BE-003` injection/query construction; `BE-004` authorization/data isolation; `BE-005` browser-facing security; `BE-006` service/operational resilience |
| `typescript` | `TS-001` exported and API contracts; `TS-002` trust/narrowing/state types; `TS-003` function signatures and object types; `TS-004` imports/configuration/environment boundary |
| `react` | `RE-001` component ownership/props; `RE-002` hooks/state/derived values; `RE-003` safe rendering/accessibility/testing |
| `nextjs` | `NX-001` routes/rendering/client boundaries; `NX-002` server-only imports/environment exposure; `NX-003` server entry-point validation/authorization |
| `nestjs` | `NJ-001` injected provider classification/naming; `NJ-002` module layout; `NJ-003` tests and fixtures |
| `postgres` | `PG-001` privileged functions/resolution/grants; `PG-002` SQL/data privileges/isolation |
| `supabase` | `SB-001` exposed-table RLS/operation policies; `SB-002` identity and cross-account isolation; `SB-003` PostgREST filters/credentials |

Select `core` for every review, plus applicable domain and installed technology companions. A check may
be split into multiple assigned checks only when different files or reviewers need separate evidence.
Do not mark a reviewer selected merely because its technology is installed.

## Check result statuses

- `PASS`: the prescribed check was performed; include concrete evidence such as `path:line` or a
  command and result. This is scoped evidence, not a guarantee of correctness.
- `FAIL`: include evidence and one or more finding IDs present in the findings list.
- `NOT_APPLICABLE`: include a short reason grounded in the reviewed scope.
- `UNVERIFIED`: include the missing evidence or limitation. Revisit high-risk cases or report them as
  open coverage gaps.

Each reviewer returns its ID and files reviewed, plus exactly one result for every planned check ID.
Each finding has a unique ID, severity, file/line, evidence, impact, and minimal fix. Consolidation may
deduplicate findings, but must preserve all related check IDs and affected sites.

## Validator files

The plan JSON has `reviewers`, each with a unique `id` and its `check_ids`. The results JSON has
`reviewers` (each with `id` and `files_reviewed`), `checks` (each with `reviewer_id`, `id`, `status`,
and status-specific `evidence`, `reason`, or `finding_ids`), and `findings` (each with a unique `id`).
Findings also carry severity, file/line, evidence, impact, and a minimal fix. Example:

```bash
{"reviewers":[{"id":"core","check_ids":["GEN-004"]}]}
{"reviewers":[{"id":"core","files_reviewed":["src/auth.ts"]}],"checks":[{"reviewer_id":"core","id":"GEN-004","status":"FAIL","evidence":"src/auth.ts:42: ownership is not checked before the read","finding_ids":["F-001"]}],"findings":[{"id":"F-001","severity":"HIGH","file":"src/auth.ts","line":42,"evidence":"...","impact":"...","fix":"..."}]}
```

See the validator's error messages for required fields. Run `python <path-to-ev-code-review>/assets/validate_coverage.py
--plan /path/to/plan.json --results /path/to/results.json` from any directory.

The validator checks completeness and referential consistency only; it cannot establish that the plan
selected every relevant reviewer or that evidence supports the reviewer's judgment.
