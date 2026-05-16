# FSD Public API Reference

Ref: https://feature-sliced.design/docs/reference/public-api

---

## What Is a Public API?

A public API is the **contract** between a slice and the rest of the application. It acts as a gate: only explicitly exported members are accessible; internal file structure is hidden.

In practice it is an `index.ts` (or `index.js`) file at the root of each slice that re-exports only what should be public.

---

## What Makes a Good Public API?

Three goals:

1. **Protect the rest of the app from internal structural changes.** Refactoring files inside a slice must not break other slices.
2. **Signal breaking behaviour changes.** When a slice's behaviour changes in a way that breaks callers, the public API should change too.
3. **Expose only the necessary parts.** Do not leak implementation details.

---

## Correct Pattern

```ts
// features/comments/index.ts
export { CommentForm } from "./ui/CommentForm";
export { CommentList } from "./ui/CommentList";
export { addComment } from "./api/addComment";
export type { Comment } from "./model/types";
```

External code imports only from the root:

```ts
// pages/article/ui/ArticlePage.tsx
import { CommentList, addComment } from "@/features/comments";
```

---

## Anti-Patterns

### ❌ Wildcard re-exports

```ts
// BAD — features/comments/index.ts
export * from "./ui/CommentForm";
export * from "./model/comments";
```

Problems:
- You cannot tell what the slice's interface is without reading every internal file
- You accidentally expose internal types and utilities
- Refactoring becomes hard because callers might depend on internals

### ❌ Importing internal paths

```ts
// BAD — importing an internal file directly
import { CommentForm } from "@/features/comments/ui/CommentForm";
```

Always import from the slice root:

```ts
// GOOD
import { CommentForm } from "@/features/comments";
```

To catch accidental direct imports, use [Steiger](https://github.com/feature-sliced/steiger).

---

## Cross-Imports: The `@x` Notation

The import rule forbids slices from importing sibling slices on the same layer. However, entities in the real world often reference each other — a Post belongs to a User, an Order contains Products.

For these cases, FSD provides the **`@x` notation**: a separate public API that one slice exposes exclusively for another slice.

### Structure

```
entities/
├── artist/
│   ├── @x/
│   │   └── song.ts    ← public API for entities/song to use
│   ├── model/
│   │   └── artist.ts
│   └── index.ts       ← regular public API for everyone else
└── song/
    ├── model/
    │   └── song.ts
    └── index.ts
```

### Usage

```ts
// entities/artist/@x/song.ts
export type { Artist } from "../model/artist";
```

```ts
// entities/song/model/song.ts
import type { Artist } from "entities/artist/@x/song";

export interface Song {
  title: string;
  artist: Artist;
}
```

The notation `A/@x/B` reads as "A crossed with B".

### Rules for `@x`

- **Only use `@x` on the Entities layer.** For features and widgets, business logic connecting two slices should be lifted to a higher layer (features, widgets, or pages).
- Keep cross-imports minimal — they represent tight coupling between domain concepts.
- Both entities involved in a cross-import should be refactored together.

---

## Index File Pitfalls

### Circular Imports

A circular import occurs when files import each other in a cycle. Index files (barrel files) make this easy to create by accident.

**Classic trap:**

```ts
// pages/home/ui/HomePage.jsx
// Imports from the barrel of its own slice — creates a circular dependency!
import { loadUserStatistics } from "../"; // → pages/home/index.js
```

```ts
// pages/home/index.js
export { HomePage } from "./ui/HomePage";
export { loadUserStatistics } from "./api/loadUserStatistics";
```

`index.js` imports `HomePage`, and `HomePage` imports `index.js` → circular.

**Fix:** Within a slice, use **direct relative imports**, never import from the slice's own index.

```ts
// pages/home/ui/HomePage.jsx — CORRECT
import { loadUserStatistics } from "../api/loadUserStatistics";
```

Rule of thumb:
- **Same slice** → relative import to the full file path
- **Different slice** → absolute import using a path alias (e.g. `@/features/comments`)

---

### Broken Tree-Shaking in `shared/`

`shared/ui` and `shared/lib` are collections of **unrelated** things. A single barrel file for all of them forces the bundler to include everything when any component is imported.

**Problem:**

```ts
// shared/ui/index.ts — ONE BIG BARREL
export * from "./button";
export * from "./text-field";
export * from "./syntax-highlighter"; // heavy dependency!
```

Importing `Button` drags in the syntax highlighter too.

**Fix:** One index file per component or library:

```
shared/
└── ui/
    ├── button/
    │   └── index.ts   ← export { Button } from "./Button"
    └── syntax-highlighter/
        └── index.ts   ← export { SyntaxHighlighter } from "./SyntaxHighlighter"
```

```ts
// Import only what you need
import { Button } from "@/shared/ui/button";
import { TextField } from "@/shared/ui/text-field";
```

---

### Bundler Performance on Large Projects

Many index files slow down the dev server (the Vite HMR graph grows). Strategies to mitigate:

1. Separate indexes per component in `shared/ui` and `shared/lib` (see above)
2. Avoid segment-level index files inside slices — `features/comments/ui/index.ts` is unnecessary on top of `features/comments/index.ts`
3. For very large apps, split into a monorepo where each package is an independent FSD root with its own layer set

---

## Enforcing Public API

There is no language-level enforcement — anyone can import from an internal path. Use tooling to catch violations:

- **[Steiger](https://github.com/feature-sliced/steiger)** — FSD architectural linter
- **ESLint `import/no-internal-modules`** — can be configured to forbid non-index imports within a layer
- **TypeScript path aliases** — configure `@/features/*` to discourage internal paths (does not fully prevent them)
