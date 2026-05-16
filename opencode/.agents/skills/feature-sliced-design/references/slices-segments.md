# FSD Slices and Segments Reference

Ref: https://feature-sliced.design/docs/reference/slices-segments

---

## Slices

Slices are the **second level** of the FSD hierarchy. They partition a layer by **business domain**.

### Naming

Slice names are **not standardised** — they come directly from the business domain of the application.

Good examples:

| App type     | Slice names |
|--------------|-------------|
| E-commerce   | `product`, `cart`, `checkout`, `order`, `review` |
| Social network | `post`, `comment`, `user-profile`, `news-feed`, `notifications` |
| SaaS dashboard | `workspace`, `billing`, `analytics`, `team-members` |

Bad examples (too technical, not domain-driven):

- `helpers`, `utils`, `common`, `base`, `misc`

### Zero Coupling, High Cohesion

An ideal slice is:
- **Zero coupling** — independent of other slices on the same layer
- **High cohesion** — contains most of the code related to its primary goal

The import rule enforces zero coupling: a slice may only import from slices on **layers strictly below** — never from sibling slices on the same layer.

### Public API Rule

Every slice must expose a public API at its root:

```
features/
└── comments/
    ├── ui/
    │   └── CommentForm.tsx
    ├── api/
    │   └── addComment.ts
    ├── model/
    │   └── commentsStore.ts
    └── index.ts             ← public API (only this file is importable from outside)
```

Code outside the slice must import from `features/comments`, never from `features/comments/ui/CommentForm`.

### Slice Groups

Closely related slices may be **visually grouped** in a sub-folder, but the isolation rules still apply — there must be no shared code inside the group folder.

```
features/
└── post/              ← group folder (no index.ts here!)
    ├── compose/       ← a slice
    │   └── index.ts
    ├── like/          ← a slice
    │   └── index.ts
    └── delete/        ← a slice
        └── index.ts
```

> ⚠️ Do not put shared code in the group folder. If `compose`, `like`, and `delete` need common code, extract it to `entities/post/` or `shared/`.

---

## Segments

Segments are the **third and final level** — they group code inside a slice by **technical purpose**.

### Standardised Segment Names

| Segment  | Purpose | Examples |
|----------|---------|---------|
| `ui`     | UI display | React components, formatters, styles, Storybook stories |
| `api`    | Backend interactions | Fetch/axios functions, React Query hooks, data types, mappers |
| `model`  | Data model | Zustand stores, Redux slices, Zod schemas, TypeScript interfaces, business logic |
| `lib`    | Internal library code | Utilities used only within this slice |
| `config` | Configuration | Feature flags, local environment config |

### Naming Rules

Name segments by **purpose** (what the code does), not by **essence** (what the code is):

| ❌ Bad (essence)         | ✅ Good (purpose) |
|--------------------------|------------------|
| `components/`            | `ui/`            |
| `hooks/`                 | `model/` or `lib/` |
| `types/`                 | `model/` or `api/` |
| `utils/`, `helpers/`     | `lib/` (with focused scope) |
| `constants/`             | `config/` or `lib/` |

### Custom Segments

You may create custom segments, but the same naming rule applies. The most common places for custom segments are `app/` and `shared/`, where slices do not exist.

Examples of reasonable custom segments:
- `shared/animations/` — animation presets and utilities
- `app/sentry/` — error monitoring setup
- `shared/testing/` — test utilities and mocks

### Segment Structure Inside a Slice

A segment folder may contain one file or many — there is no required internal structure. Avoid creating index files for segments on layers that have slices (pages, widgets, features, entities) — having `features/comments/ui/index.ts` on top of `features/comments/index.ts` only adds noise.

```
features/
└── comments/
    ├── ui/
    │   ├── CommentForm.tsx    ← no index.ts needed here
    │   └── CommentList.tsx
    ├── api/
    │   └── commentsApi.ts
    ├── model/
    │   └── commentsStore.ts
    └── index.ts               ← the only public API entry point
```

### Layers Without Slices (`app` and `shared`)

On `app/` and `shared/`, there are no slices — segments are created directly:

```
shared/
├── ui/          ← segment (no slice above it)
├── api/         ← segment
├── lib/         ← segment
└── config/      ← segment
```

Segments in `shared/` and `app/` can import each other freely — the cross-import restriction is between slices, not between segments on sliceless layers.

---

## Choosing the Right Layer for a Slice

| Question | Answer |
|----------|--------|
| Is this a business entity the app works with? | `entities/` |
| Is this a user interaction reused in multiple places? | `features/` |
| Is this a large UI block reused across pages? | `widgets/` |
| Is this a full page or screen? | `pages/` |
| Is this app-wide setup (router, global state, providers)? | `app/` |
| Is this generic, framework-agnostic, with no business logic? | `shared/` |
