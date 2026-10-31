---
name: ev-review-react
description: "Trigger: implementing or reviewing React components, hooks, or JSX. Supply structure, state, rendering, and testing rules before coding or with ev-code-review."
license: Apache-2.0
metadata:
  author: "eduardovdev"
  version: "1.0"
---

# EV React Review Rules

## Activation Contract

Use before implementing React components/hooks/JSX/tests, or as an optional `ev-code-review` companion.
Load general/domain rules through `ev-coding-standards` for implementation; do not start another review
or delegate. Review output/check assignments apply only during reviews.

## Hard Rules

- Preserve coordinator scope, baseline, read-only constraints, and general/domain rules.
- Declare one React component per production `.tsx` file. Declare props readonly using `Readonly<Props>`
  or readonly properties when TypeScript is used.
- Use a kebab-case component folder with an `index.tsx` entry point and colocated CSS module in
  TypeScript projects; use the language-appropriate JSX extension otherwise.
- Components describe UI. Move non-trivial form handling, requests, navigation, effects, and
  interaction state into a custom hook beside the component.
- A page-only hook belongs beside its page; feature-shared hooks belong in `feature/hooks`;
  cross-feature hooks belong in `src/hooks`. Expose domain-oriented state/actions, not implementation details.
- Do not create a hook merely to wrap a simple derived value or trivial toggle. Derive values during
  render instead of synchronizing duplicate state with effects.
- Prefix hooks with `use`, callback props with `on`, and internal event handlers with `handle`.
- Tightly coupled compound primitives under `src/components/ui` may share a file when intentionally
  consumed as one family. This exception does not apply to feature components.
- Render untrusted text through normal JSX interpolation so React escapes it. Do not use
  `dangerouslySetInnerHTML` with user-controlled content unless product-required HTML is sanitized at
  the final render boundary and tested as required by frontend rules.
- When Testing Library is used, prefer accessible queries such as `getByRole` with a name.

## Decision Gates

| Scoped code | Action |
| --- | --- |
| React component/hook/JSX or its tests | Apply relevant React rules. |
| Plain domain utility in a React package | Do not impose component/hook structure. |
| Non-React JSX | Do not infer React from the extension alone. |
| Approved compound primitive family | Apply the one-component exception. |

## Execution Steps

1. Verify actual React usage, component ownership, hook consumers, and applicable test tooling.
2. Check component count/props, collocation, hook responsibilities, derived state, and safe rendering.
3. Verify exceptions and behavioral impact; report assigned check results without duplicating shared runs.

## Output Contract

Return candidates with severity, `path:line`, rule wording, evidence/impact, and smallest fix, plus a
result for each assigned coverage ID: `RE-001` component ownership/props; `RE-002` hooks, state, and
derived values; `RE-003` safe rendering, accessibility, and testing. Each result must use the shared
status/evidence contract in `ev-code-review/references/coverage.md`. The coordinator consolidates findings.
