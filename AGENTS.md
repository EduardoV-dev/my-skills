# Repository guidance

- Put each maintained skill in `skills/<skill-name>/SKILL.md`.
- Keep the directory name and the skill's frontmatter `name` aligned; use lowercase kebab-case.
- Prefix every maintained skill name and directory with `ev-`.
- Make each skill's description state when it should activate and what it does.
- Keep instructions concise. Put skill-specific templates in `assets/` and supporting material in `references/` under that skill.
- Add third-party skills to `catalog/README.md` with their upstream source and install command; do not copy their files into `skills/`.
- Before publishing, verify the Skills CLI can list the repository's skills.

## Maintained review skills

- `skills/ev-code-review/SKILL.md` — review coordinator and general/frontend/backend rules.
- `skills/ev-review-typescript/SKILL.md` — optional TypeScript contract rules.
- `skills/ev-review-react/SKILL.md` — optional React component, hook, and rendering rules.
- `skills/ev-review-nextjs/SKILL.md` — optional Next.js route and client/server boundary rules.
- `skills/ev-review-nestjs/SKILL.md` — optional NestJS injected-service naming rules.
- `skills/ev-review-postgres/SKILL.md` — optional PostgreSQL privileged-function rules.
- `skills/ev-review-supabase/SKILL.md` — optional Supabase RLS and PostgREST filter rules.

Technology companions extend `ev-code-review`; they do not initiate separate reviews or delegate.
