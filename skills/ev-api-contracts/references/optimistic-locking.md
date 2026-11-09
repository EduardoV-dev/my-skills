# Optimistic Locking For Resource Updates

Require `lastKnownUpdatedAt` in resource-update request bodies, including partial updates. The client
must send the resource's last-read `updatedAt`, not its current local time. Reject missing or malformed
tokens as validation errors before mutation. Keep creates outside this precondition.

## Perform One Conditional Write

Keep the timestamp comparison inside the database update alongside resource identity, ownership/tenant
scope, and applicable domain predicates. Bind all values; never interpolate request values into SQL.
An earlier read may establish authorization or domain rules, but cannot replace the atomic comparison.

```sql
-- Schematic bound-parameter SQL; adapt binding and result retrieval to the installed database.
UPDATE resources
SET name = :name,
    updated_at = :nextUpdatedAt
WHERE id = :id
  AND tenant_id = :authorizedTenantId
  AND updated_at = :lastKnownUpdatedAt;
```

Here `authorizedTenantId` comes from verified authorization, and `nextUpdatedAt` is server-owned and
strictly later than the matched timestamp at the column's precision. Whitelist writable fields;
`lastKnownUpdatedAt` is comparison metadata, never an entity field or the value assigned to `updated_at`.
Never spread the whole request body into a persistence update.

| Database outcome | Required behavior |
| --- | --- |
| Exactly one row updated | Continue normally; return the persisted resource's new `updatedAt`. |
| Zero rows updated | Return HTTP 409 using the ordinary failure envelope and a safe refresh instruction. |
| Unexpected database error or multiple rows updated for one resource | Treat as an internal failure; never mislabel it as a stale-token conflict. |

Use the database's affected-row count or returned-row result, not a separate existence check, as proof
of success. Never retry a failed write without its timestamp predicate, silently fetch a new token to
overwrite newer changes, or emit success side effects after a failed match. Keep related database writes
in the same transaction so a conflict rolls back the entire operation.

Zero matches alone do not prove another update occurred: the resource may be deleted, inaccessible, or
fail another predicate. Preserve established authorization and not-found handling, including non-disclosure
policy. For an authorized update that fails the timestamp precondition, use a conflict message such as
"This resource was updated elsewhere. Refresh it and try again." Clients must refresh and reconcile
their edits before resubmitting, rather than automatically replaying the stale patch.

## Preserve An Exact, Changing Token

- Validate a timezone-qualified ISO-8601 string. For the NestJS microsecond contract, accept no fractional
  part or 1–6 fractional digits, with `Z` or an explicit `+/-HH:MM` offset; reject impossible dates.
- Preserve database precision in reads, response serialization, client storage, request validation,
  database binding, and comparison. Do not pass microsecond tokens through JavaScript `Date`, truncate
  them to milliseconds, or compare formatted timestamp text instead of database timestamp values.
- Advance `updated_at` atomically for every accepted update, including no-op patches. Do not assume
  clock resolution or transaction-stable `now()` guarantees a different value. Use a database-compatible
  mechanism that produces a strictly later value at stored precision; verify driver/ORM behavior.
- Ensure every writer to the protected resource advances the same timestamp, including background jobs
  and administrative paths. If the schema or driver cannot preserve and advance the token, surface the
  limitation before claiming optimistic-lock protection; do not silently weaken the comparison.

## Verification Scenarios

Verify behavior through the real persistence boundary, not only mocked query calls:

1. A matching token updates one authorized resource and returns its new, precisely serialized timestamp.
2. A stale token returns 409, leaves persisted fields unchanged, and produces no success side effects.
3. Two concurrent updates using the same token yield exactly one success and one conflict. Also check
   rapid successive/no-op updates: the timestamp advances and the previous token cannot be reused.
4. Missing/null tokens, non-strings, impossible dates, absent timezones, and excess fractional digits
   fail validation. Valid `Z`/offset tokens and microseconds survive a full read-update round trip.
5. Missing/deleted resources and unauthorized or cross-tenant attempts retain the existing safe policy;
   database failures remain internal errors and transactional related writes roll back on conflict.
