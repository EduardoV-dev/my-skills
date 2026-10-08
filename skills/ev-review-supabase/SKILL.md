---
name: ev-review-supabase
description: "Trigger: Supabase or PostgREST code review with ev-code-review. Supply exposed-table RLS, policy, and client-filter rules."
license: Apache-2.0
metadata:
  author: "eduardovdev"
  version: "1.0"
---

# EV Supabase And PostgREST Review Rules

## Activation Contract

Use as an optional `ev-code-review` companion for Supabase access, exposed-table policies, PostgREST
filtering, and their tests. Supply rules to the active review; do not start another review or delegate.

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

Return candidates with severity, `path:line`, rule wording, evidence/impact, and smallest fix, plus gaps.
Checklist: exposed-table RLS, operation policies, cross-account isolation, safe filters, and private
credentials. The coordinator consolidates findings.
