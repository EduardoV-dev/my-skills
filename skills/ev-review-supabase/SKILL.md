---
name: ev-review-supabase
description: "Trigger: implementing or reviewing Supabase or PostgREST. Apply RLS, policy, and client-filter rules before coding or with ev-code-review."
license: Apache-2.0
metadata:
  author: "eduardovdev"
  version: "1.0"
---

# EV Supabase And PostgREST Review Rules

## Activation Contract

Use before implementing Supabase access/policies/PostgREST filters/tests, or as an optional
`ev-code-review` companion. Load general/domain rules through `ev-coding-standards` for implementation;
do not start another review or delegate. Review output/check assignments apply only during reviews.

## Hard Rules

- Preserve coordinator scope, baseline, read-only constraints, and general/domain rules.
- When using Supabase, enable Row Level Security on every exposed table and write policies for each
  permitted operation. Inspect policy enforcement, not merely the presence of an RLS declaration.
- Test that users cannot read or change another account's rows, as required by backend rules.
- Validate filter, pagination, and ordering input before query construction. Do not accept arbitrary
  PostgREST filter syntax from clients.
- Keep privileged credentials server-only and enforce backend identity/ownership checks. Client SDK
  access must rely on server-enforced policies, not hidden controls or client permission flags.

## Decision Gates

| Scoped code | Action |
| --- | --- |
| Supabase exposed tables/access policies | Apply RLS and per-operation policy rules. |
| PostgREST filters, including without Supabase | Apply validated-input and filter-syntax rules. |
| Client SDK queries | Apply frontend/general rules; inspect backend policy enforcement as context. |
| PostgreSQL function/grant changes | Request installed PostgreSQL rules through the coordinator. |
| Package installed but no scoped usage | Do not apply Supabase requirements. |

## Execution Steps

1. Verify scoped Supabase/PostgREST usage and inspect relevant schema, policies, session handling, and consumers.
2. Check exposed-table RLS, permitted operations, identity boundaries, filter construction, and isolation tests.
3. Record unavailable schema/policy evidence and assigned check results; never change remote configuration.

## Output Contract

Return candidates with severity, `path:line`, rule wording, evidence/impact, and smallest fix, plus a
result for each assigned coverage ID: `SB-001` exposed-table RLS and operation policies; `SB-002`
identity boundaries and cross-account isolation; `SB-003` PostgREST filters and credentials. Each
result must use the shared status/evidence contract in `ev-code-review/references/coverage.md`.
The coordinator consolidates findings.
