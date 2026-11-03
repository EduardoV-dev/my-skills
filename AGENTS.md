# Repository guidance

- Put each maintained skill in `skills/<skill-name>/SKILL.md`.
- Keep the directory name and the skill's frontmatter `name` aligned; use lowercase kebab-case.
- Prefix every maintained skill name and directory with `ev-`.
- Make each skill's description state when it should activate and what it does.
- Keep instructions concise. Put skill-specific templates in `assets/` and supporting material in `references/` under that skill.
- Add third-party skills to `catalog/README.md` with their upstream source and install command; do not copy their files into `skills/`.
- Before publishing, verify the Skills CLI can list the repository's skills.

## Maintained setup skills

- `skills/ev-project-setup/SKILL.md` — portable project `AGENTS.md` wiring for session/task skill activation.

## Maintained implementation skills

- `skills/ev-coding-standards/SKILL.md` — pre-coding rule selection and global check/fix/update/add-rule workflows.
- `skills/ev-api-contracts/SKILL.md` — first-party JSON response contracts, pagination decision gate, and validated extensible cursors.

## Maintained review skills

- `skills/ev-code-review/SKILL.md` — review coordinator and general/frontend/backend rules.
- `skills/ev-review-typescript/SKILL.md` — optional TypeScript contract rules.
- `skills/ev-review-react/SKILL.md` — optional React component, hook, and rendering rules.
- `skills/ev-review-nextjs/SKILL.md` — optional Next.js route and client/server boundary rules.
- `skills/ev-review-nestjs/SKILL.md` — optional NestJS plural grouping, DTO/global validation, API/docs setup, health contracts, injected-service naming, and test ownership rules.

Technology companions apply before implementation through `ev-coding-standards` and extend
`ev-code-review` during reviews; they do not initiate separate reviews or delegate. Maintained skills
run in one agent thread: do not spawn subagents or parallel reviewers; perform applicable checks
sequentially.

<!-- ev-project-skills:start -->
## Skill activation

At the start of every session, inspect the harness's available skill names and descriptions.
If unavailable or incomplete, inspect `SKILL.md` metadata in the project's `.agents/skills/`,
`.opencode/skills/`, and `.claude/skills/`, then the equivalent user locations, including
`~/.agents/skills/` and `~/.config/opencode/skills/`. Use any project registry only after checking
that its entries still resolve. Prefer project-local copies of the same skill and report shadowing
or incompatible sources; do not silently mix versions.

Before each task, match its intent, target files, and actual technology usage to available skill
activation descriptions. Load the complete matching `SKILL.md` files and their required references
before acting; reuse unchanged full guidance already available in the active context rather than
reloading it per file or edit. Reload missing/changed guidance and load newly applicable rules.
Apply this to implementation, debugging, review, documentation, setup, and other
workflows, including newly installed skills. Reevaluate when task scope changes. Discovery alone
does not load rules; do not load unrelated skill bodies or limit selection to a fixed skill list.

Before generating or changing code, load `ev-coding-standards`. Follow its pre-coding workflow to
read complete general, applicable frontend/backend, technology, and implementation rules. Reuse
`ev-code-review` rules while generating code; do not defer standards until an explicit review.
Follow the selected review core's incremental generation workflow: review coherent work units, retain
compact evidence, invalidate it when relevant code/rules/dependencies/configuration change, and finish
with final-diff reconciliation and integration checks. Do not launch a formal review per edit or repeat
still-valid checks at completion. Before compaction retain recoverable continuation evidence; afterward
verify sources/current changes and reload missing full rules. Generation requires no formal coverage
JSON or validator run. Record selected rule paths, source revision/dirty state, and results internally;
do not emit a separate review report or standards summary. Surface unresolved blockers,
required decisions, and material verification gaps. For explicit review/check/fix requests, display
every finding in chat with severity, location, rule, evidence, impact, minimal fix, and fixed/remaining
status when applicable. Use the full formal workflow over the entire requested scope; generation
checkpoints do not replace it. Never truncate findings to five or another top-N subset.

Use the skill tool when available; otherwise read the resolved local `SKILL.md` directly and follow
its references. If a required core skill or required reference is missing, name the exact gap and
resolve it before affected edits. A technology with no maintained companion is a coverage gap:
apply available core rules without inventing technology rules or claiming full coverage.

Preserve the instruction hierarchy, applicable nested project guidance, skill exceptions, and plan
mode. Surface unresolved policy conflicts before affected changes. Keep maintained EV workflows
in the current agent thread; never spawn subagents or parallel reviewers. A skill match does not
authorize installation, unrelated edits, commits, publication, or destructive operations.
<!-- ev-project-skills:end -->
