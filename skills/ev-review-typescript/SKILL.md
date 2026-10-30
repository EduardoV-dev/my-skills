---
name: ev-review-typescript
description: "Trigger: TypeScript code review with ev-code-review. Supply TypeScript contract and environment-module rules for scoped TypeScript code."
license: Apache-2.0
metadata:
  author: "eduardovdev"
  version: "1.0"
---

# EV TypeScript Review Rules

## Activation Contract

Use as an optional `ev-code-review` companion for TypeScript source, declarations, and their tests.
Supply technology rules to the active review; do not start an independent review or delegate.

## Hard Rules

- Preserve the coordinator's scope, baseline, read-only constraints, and general/domain rules.
- Use strict TypeScript and explicit types at exported boundaries.
- Consume first-party API responses using documented response types. Avoid speculative response-shape
  parsers for repository-owned contracts; handle HTTP and domain errors. This does not remove runtime
  validation of untrusted input required by general rules.
- Require shared exported `ApiError = { code: string; message: string; field?: string }` and
  `ApiResponse<T> = { ok: true; data: T; error: []; message: string } | { ok: false; data: null; error: ApiError[]; message: string }`.
  Use these types across first-party JSON API producers/consumers, including paginated payloads;
  do not redefine endpoint-local envelopes. Preserve protocol-defined non-JSON/bodyless responses.
- Check offset/cursor page types against backend metadata rules. Infer cursor types from extendable
  Zod object schemas; require schema-aware shared encode/decode methods without unchecked assertions.
- Avoid `any`. Preserve established TypeScript contracts throughout the call chain: accept and use
  concrete interfaces and types directly. Do not widen known values to `unknown`, replace them with
  generic records, repeat checks guaranteed by their contracts, or add handwritten parsers that
  reconstruct the same guarantees.
- Use `unknown` and runtime validation where values genuinely lack an established contract, such as
  untrusted external input. Type annotations alone do not validate that input. Preserve checks for
  conditions the declared contract does not guarantee, including decoded content, business invariants,
  and authorization. Avoid assertions unless runtime validation or a documented invariant justifies them.
- Avoid double assertions such as `value as unknown as Memory`. When an assertion is justified, use a
  direct assertion such as `value as Memory`; if it is rejected, fix or validate the value rather
  than bypassing the type compatibility check.
- Use discriminated unions for mutually exclusive states instead of combinations of optional fields.
- Prefer one object parameter destructured directly in the function signature over multiple positional
  parameters. Do not name the object parameter `options` or `params` and access its properties in the body.
  Use an inline object type for parameter or return objects with one or two properties; use a named `<FunctionName>Params`
  or `<FunctionName>Return` type for three or more properties. Use a named type at any size when
  another function reuses or extends that contract. Assess parameter and return objects separately.
- If the owning application/package has no environment constants module, recommend
  `src/constants/environment-variables.ts`. Reuse an established module even at another path; preserve
  the general configuration-boundary exceptions and evaluation timing.

## Decision Gates

| Scoped code | Action |
| --- | --- |
| TypeScript source/declarations or related configuration/tests | Apply relevant type/contract rules. |
| JavaScript-only code or TypeScript merely installed | Do not apply TypeScript requirements. |
| Untrusted runtime input | Apply general validation rules; static types are not validation. |
| Value with an established concrete contract | Preserve its type; flag redundant widening, validation, and parsing without removing checks outside its guarantees. |

## Execution Steps

1. Read scoped contracts, consumers, owning TypeScript configuration, and relevant tests.
2. Check exported types, contract preservation, necessary narrowing, state modeling, response/page contracts and cursor schemas, function parameter/return
   object shapes, and environment ownership.
3. Use the project's documented non-writing typecheck when assigned by the coordinator; report gaps.

## Output Contract

Return evidence-backed candidates with severity, `path:line`, rule wording, impact, and smallest fix,
plus checks/gaps. Checklist: strictness, exported contracts, contract preservation, necessary narrowing, discriminated states, object
parameter/return type reuse and size, and environment-module ownership. Let `ev-code-review`
consolidate the report.
