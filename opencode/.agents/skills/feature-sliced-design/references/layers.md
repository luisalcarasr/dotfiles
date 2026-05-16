# FSD Layers Reference

Seven standardised layers, listed from highest responsibility (most dependencies allowed) to lowest.

Ref: https://feature-sliced.design/docs/reference/layers

---

## Import Rule

> A module in a slice can only import other slices when they are located on **layers strictly below**.

Layers `app` and `shared` are exceptions — they have no slices, so their segments can import each other freely.

---

## `shared/`

The foundation of the app. Framework-agnostic code that has no business logic.

**Has no slices** — goes directly to segments.

Common segments:

| Segment   | Contents |
|-----------|----------|
| `ui`      | Application UI kit — base components (Button, Input, Modal). May be business-themed (logo, layout) but must not contain business logic. |
| `api`     | API client instance, generic request helpers, shared data types |
| `lib`     | Internal libraries, each with a single area of focus (dates, colours, text, validation). Each should have a README. Do not use as a dump for helpers. |
| `config`  | Environment variables, global feature flags |
| `routes`  | Route constants or pattern helpers |
| `i18n`    | Translation setup, global translation strings |

**Rules:**
- No business logic — if it mentions a domain concept, it belongs in `entities/` or higher
- `shared/ui` and `shared/lib` should have **one index per component/library** (not one giant barrel) to avoid broken tree-shaking

```
shared/
├── ui/
│   ├── button/
│   │   └── index.ts     ← separate index per component
│   └── text-field/
│       └── index.ts
├── api/
│   └── index.ts
├── lib/
│   ├── dates/
│   │   └── index.ts
│   └── validation/
│       └── index.ts
└── config/
    └── index.ts
```

---

## `entities/`

Real-world business concepts the project works with. Named using business vocabulary.

**Has slices** — one per domain concept.

Examples: `user`, `product`, `order`, `post`, `comment`, `notification`

Common segments inside an entity slice:

| Segment | Contents |
|---------|----------|
| `ui`    | Visual representation of the entity — reusable across pages, business logic attached through props/slots |
| `model` | Data storage (Zustand store, Redux slice), validation schemas, TypeScript types |
| `api`   | Request functions specific to this entity |

**Rules:**
- Entity slices cannot import from each other directly — use the [`@x` notation](public-api.md#cross-imports-x-notation) for legitimate cross-references
- Business logic for relationships between entities belongs in `features/` or `pages/`

```
entities/
├── user/
│   ├── ui/
│   │   └── UserAvatar.tsx
│   ├── model/
│   │   ├── user.ts        ← TypeScript type / schema
│   │   └── userStore.ts   ← state
│   ├── api/
│   │   └── getUser.ts
│   └── index.ts           ← public API
└── post/
    ├── @x/
    │   └── user.ts        ← cross-import API for entities/user
    ├── model/
    │   └── post.ts
    └── index.ts
```

---

## `features/`

Reused implementations of product interactions — actions that bring **direct business value** to the user.

**Has slices** — one per feature.

Examples: `auth-by-email`, `add-to-cart`, `search`, `comments`, `like-post`

> ⚠️ **Not everything is a feature.** Only put something here when it is reused across multiple pages. Over-populating this layer drowns out the important features.

Common segments:

| Segment  | Contents |
|----------|----------|
| `ui`     | Forms, buttons, interactive components |
| `api`    | Mutations, queries for the action |
| `model`  | Local state, validation, feature flags |
| `config` | Feature flags specific to this feature |

```
features/
├── auth-by-email/
│   ├── ui/
│   │   └── LoginForm.tsx
│   ├── api/
│   │   └── loginByEmail.ts
│   ├── model/
│   │   └── loginForm.ts
│   └── index.ts
└── add-to-cart/
    ├── ui/
    │   └── AddToCartButton.tsx
    ├── api/
    │   └── addToCart.ts
    └── index.ts
```

---

## `widgets/`

Large, self-contained blocks of UI. Typically deliver an entire use case in one block.

**Has slices** — one per widget.

Use `widgets/` when:
- The block is **reused across multiple pages**
- A single page contains **several large independent blocks**

Do _not_ put a block here if it makes up most of the interesting content on exactly one page and is never reused — it belongs inside the page slice.

> In nested-routing setups (Remix, TanStack Router), widgets can serve the same role as pages in flat-routing setups — complete router blocks with data fetching, loading states, and error boundaries.

```
widgets/
├── navbar/
│   ├── ui/
│   │   └── Navbar.tsx
│   └── index.ts
└── sidebar/
    ├── ui/
    │   └── Sidebar.tsx
    └── index.ts
```

---

## `pages/`

Full pages or large parts of a page in nested routing.

**Has slices** — one per page (or group of very similar pages).

Rules:
- No limit on how much code lives inside a page slice as long as the team can navigate it
- Non-reused UI blocks belong **directly inside the page slice**, not in `widgets/`
- Very similar pages (e.g. login + register) can share one slice

Common segments:

| Segment | Contents |
|---------|----------|
| `ui`    | Page component, loading states, error boundaries |
| `api`   | Data fetching and mutation calls for this page |

It is uncommon for pages to have a `model` segment — small state stays in the components.

```
pages/
├── home/
│   ├── ui/
│   │   └── HomePage.tsx
│   └── index.ts
├── article-reader/
│   ├── ui/
│   │   └── ArticleReaderPage.tsx
│   ├── api/
│   │   └── getArticle.ts
│   └── index.ts
└── auth/             ← groups login + register (very similar pages)
    ├── ui/
    │   ├── LoginPage.tsx
    │   └── RegisterPage.tsx
    └── index.ts
```

---

## `app/`

Everything that makes the whole app run.

**Has no slices** — goes directly to segments.

Common segments:

| Segment      | Contents |
|--------------|----------|
| `routes`     | Router configuration and route definitions |
| `store`      | Global store setup (Redux, Zustand root) |
| `styles`     | Global CSS, theme, resets |
| `entrypoint` | Framework entrypoint (main.tsx, _app.tsx, etc.) |

Analytics and monitoring setup also belongs here.

```
app/
├── routes/
│   └── router.tsx
├── store/
│   └── store.ts
├── styles/
│   └── global.css
└── entrypoint/
    └── main.tsx
```

---

## `processes/` (deprecated)

> ❌ **Do not use in new projects.**

This layer was intended for complex multi-page interactions. In v2.1 its contents are split between `features/` and `app/`.

---

## Quick Decision Guide

| Where does this code belong? | Layer |
|------------------------------|-------|
| API client, base UI components, date utilities | `shared` |
| User profile type, product schema, post store | `entities` |
| Login form, add-to-cart button (reused on 2+ pages) | `features` |
| Navigation bar, sidebar (reused on 2+ pages) | `widgets` |
| Home page, product detail page | `pages` |
| Router, global providers, analytics init | `app` |
