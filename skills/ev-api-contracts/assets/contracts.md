# API Contract Template

Export these types from the owning application's or package's shared contract module. Reuse them in
handlers, services exposing API contracts, client calls, and related tests.

```ts
export type ApiError = {
  code: string;
  message: string;
  field?: string;
};

export type ApiResponse<T> =
  | { ok: true; data: T; error: []; message: string }
  | { ok: false; data: null; error: ApiError[]; message: string };

export type OffsetPage<T> = {
  data: T[];
  meta: {
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    total: number;
    page: number;
    pageSize: number;
  };
};

export type CursorPage<T> = {
  data: T[];
  meta: {
    nextCursor: string | null;
  };
};

// Use only when backward navigation is explicitly requested.
export type BidirectionalCursorPage<T> = {
  data: T[];
  meta: CursorPage<T>["meta"] & {
    prevCursor: string | null;
  };
};
```

Use `ApiResponse<OffsetPage<Item>>`, `ApiResponse<CursorPage<Item>>`, or the explicitly requested
`ApiResponse<BidirectionalCursorPage<Item>>`. The outer `data` holds the page; its `data` holds items.
Success always includes `error: []`; failure always includes `data: null` and an `ApiError[]`.
Both branches include a string `message`. Keep client errors free of internal details.

## Pagination Semantics

- Use one-based offset pages. Validate positive integer `page` and bounded positive integer `pageSize`.
  Compute `total` over the authorized, filtered dataset before pagination. Derive flags from that total
  and the requested page; apply deterministic ordering with a unique tie-breaker.
- Emit `nextCursor: null` at the end, including empty pages. When requested, emit `prevCursor: null`
  at the beginning. Determine whether another page exists; do not infer it from a full page alone.
- Keep filters, authorization, and ordering consistent across page queries. Cursors never grant access.

## Cursor Utility Contract

- Export a Zod object base schema containing `id` and `createdAt` when the dataset provides both.
  Match the actual ID format and timestamp precision; do not assume UUIDs or round timestamps.
  With only one field available, use it and add an available unique tie-breaker if needed.
- Support extending that schema with additional ordering fields using Zod object composition.
  Infer cursor payload types from schemas instead of maintaining separate unchecked types.
- Expose shared `encodeCursor` and `decodeCursor` methods that accept the selected schema and infer
  its payload type. Validate before encoding and after decoding; reuse the base schema by default.
- Use a consistent URL-safe encoding supported by the target runtime. Normalize malformed encoding,
  JSON, or Zod failures into the API validation-error contract; never let them become unhandled errors.
- Match payload fields, sort direction, and query comparisons. For descending `(createdAt, id)`,
  advance with `createdAt < cursor.createdAt OR (createdAt = cursor.createdAt AND id < cursor.id)`;
  invert comparisons for ascending traversal. Implement reverse traversal only when requested,
  restoring the documented item order before responding.
