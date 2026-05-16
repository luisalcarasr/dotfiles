---
name: feature-sliced-design
description: Implement Feature-Sliced Design (FSD) v2.1 architectural methodology for frontend applications. Scaffold projects, organise code by layers/slices/segments, enforce import rules and public API contracts. Works with any framework (React, Vue, Angular, Next.js, etc.).
---

# Feature-Sliced Design (FSD) v2.1

Official skill for applying Feature-Sliced Design, an architectural methodology for front-end applications. FSD organises code by business domains and user needs rather than purely technical concerns, making projects easier to navigate, scale, and maintain.

Reference: https://feature-sliced.design/

## When to Use FSD

FSD is the right choice when:

- You are building a **frontend application** (web, mobile, desktop)
- The project is **growing in complexity** — multiple pages, features, teams
- You need **parallel development** across features without merge conflicts
- **New team members** need to onboard quickly

FSD is _not_ recommended for:
- Simple landing pages or one-page apps
- UI component libraries (no application logic)
- Backend or server-only code

FSD has **no restrictions on language or framework** — use it with React, Vue, Angular, Next.js, Remix, etc.

## Canonical Folder Structure

```
src/
├── app/          ← app-wide setup: router, global styles, providers, analytics
├── pages/        ← full pages or large nested routing blocks
├── widgets/      ← large self-contained UI blocks, reused across pages
├── features/     ← reused product interactions that bring business value
├── entities/     ← real-world business concepts (user, product, order)
└── shared/       ← framework-agnostic utilities, UI kit, API client, config
```

> `processes/` exists in legacy codebases but is **deprecated** in v2.1. Do not create it in new projects.

All layer folders use **lowercase names**. Do not add custom layers — their semantics are standardised.

## The Three Levels: Layer → Slice → Segment

### Layers (top level)

Seven fixed layers, ordered from most responsibility (top) to least (bottom):

| Layer    | Has Slices? | Purpose |
|----------|-------------|---------|
| app      | No          | App-wide setup — routing, providers, global styles, analytics |
| pages    | Yes         | One slice per page or group of very similar pages |
| widgets  | Yes         | Large, self-contained, reusable UI blocks |
| features | Yes         | Reused product interactions (only what is reused!) |
| entities | Yes         | Business domain objects — User, Post, Order, etc. |
| shared   | No          | Reusable utilities, UI kit, API client, i18n, config |

See [layers reference](references/layers.md) for detailed per-layer guidance.

### Slices (second level)

Slices partition a layer by **business domain**. Their names come from the business, not from technical roles.

```
features/
├── auth/           ← a slice
├── comments/       ← a slice
└── search/         ← a slice
```

Rules:
- Slices are **independent from each other** on the same layer — no cross-imports unless using the `@x` notation
- Slices must expose a **public API** (`index.ts` / `index.js`) — no external code may import internal files directly
- `app` and `shared` have **no slices** — they go straight to segments

See [slices and segments reference](references/slices-segments.md).

### Segments (third level)

Segments group code inside a slice by **technical purpose**:

| Segment  | Contents |
|----------|----------|
| `ui`     | Components, formatters, styles |
| `api`    | Request functions, data types, mappers |
| `model`  | Stores, schemas, business logic |
| `lib`    | Internal library code used only within this slice |
| `config` | Feature flags, local configuration |

You can create custom segments, but name them by **purpose** (e.g. `hooks`, `types` are bad names — `animation`, `validation` are good names).

## The Import Rule

> **A module in a slice may only import from slices on layers strictly below its own.**

```
app     ← can import from pages, widgets, features, entities, shared
pages   ← can import from widgets, features, entities, shared
widgets ← can import from features, entities, shared
features← can import from entities, shared
entities← can import from shared
shared  ← imports nothing from the app
```

Violations of the import rule are the most common source of FSD bugs. Use the [Steiger linter](https://github.com/feature-sliced/steiger) to enforce this automatically.

## Public API Rule

Every slice must define a public API at its top level:

```ts
// features/comments/index.ts
export { CommentForm } from "./ui/CommentForm";
export { CommentList } from "./ui/CommentList";
export { addComment } from "./api/addComment";
```

Rules:
- ✅ Use explicit named re-exports
- ❌ Never use wildcard re-exports (`export * from "./ui/Comment"`)
- ❌ Never import from internal paths (`features/comments/ui/Comment`) — always import from the slice root (`features/comments`)
- Within a slice, use **relative imports**; between slices, use **absolute imports** (path alias)

See [public API reference](references/public-api.md) for index file pitfalls (circular imports, broken tree-shaking).

## Cross-Imports Between Entities (`@x` notation)

When two entities need to reference each other, use the `@x` notation instead of breaking isolation:

```
entities/
├── artist/
│   ├── @x/
│   │   └── song.ts    ← public API exposed specifically to entities/song
│   └── index.ts
└── song/
    └── index.ts
```

```ts
// entities/song/model/song.ts
import type { Artist } from "entities/artist/@x/song";
```

**Only use `@x` on the Entities layer.**

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Business logic in `shared/` | Move it to `entities/` or `features/` |
| Every interaction is a feature | Features layer is only for **reused** interactions |
| Wildcard public API exports | Use explicit named exports |
| Importing internal slice paths | Always import from the slice's `index` file |
| Adding custom layers | Work within the 7 standardised layers |
| Putting non-reused UI in `widgets/` | Keep it directly in the page slice |
| Cross-imports without `@x` | Use `@x` notation on entities, lift to higher layer otherwise |

## Incremental Adoption

When migrating an existing project to FSD:

1. **Shape `shared/` and `app/` first** — move utilities, the UI kit, providers, router config
2. **Distribute existing UI** into `pages/` and `widgets/` in broad strokes, even if imports violate FSD rules temporarily
3. **Resolve import violations** gradually, extracting `entities/` and `features/` as you go
4. **Avoid large new features** during migration — stabilise the structure first

## Tooling

- **[Steiger](https://github.com/feature-sliced/steiger)** — architectural linter, enforces FSD rules automatically
- **Folder generators** — see [FSD awesome list](https://github.com/feature-sliced/awesome?tab=readme-ov-file#tools) for CLI and IDE plugins
- **Path aliases** — configure `@/` or similar to point to `src/` for clean cross-layer imports

## Additional References

- [Layers reference](references/layers.md) — per-layer purpose, allowed segments, examples
- [Slices and segments reference](references/slices-segments.md) — naming, cohesion, slice groups
- [Public API reference](references/public-api.md) — index file patterns, `@x` notation, pitfalls
- [Official documentation](https://feature-sliced.design/docs/get-started/overview)
- [Official examples](https://feature-sliced.design/examples)
