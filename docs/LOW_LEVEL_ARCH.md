# MEMORIA AI — Low-Level Architecture & API Contracts

Last updated: 2026-06-13

This document provides per-service API sketches, event envelope definitions, and an initial list of database tables and indexes to be implemented in migrations.

## 1. API Patterns & Conventions

- All services expose RESTful JSON endpoints under `/api/v1`.
- Use JWT bearer tokens for service-to-service and user-to-service calls. Service tokens use short-lived mTLS or signed JWTs.
- Standard response envelope: `{ "status": "ok" | "error", "data": ..., "meta": {...} }`.

## 2. Auth Service (sample endpoints)

- POST `/api/v1/auth/signup` — body: `{email, password, name?}` — returns `{user, access_token, refresh_token}`.
- POST `/api/v1/auth/login` — body: `{email, password}` — returns tokens.
- POST `/api/v1/auth/oauth/callback` — handles provider callback, issues tokens.
- POST `/api/v1/auth/token/refresh` — body: `{refresh_token}` — rotate tokens.

## 3. User Service

- GET `/api/v1/users/{user_id}` — profile & preferences.
- PATCH `/api/v1/users/{user_id}` — update preferences (privacy, retention).

## 4. Notes Service

- POST `/api/v1/notes` — create note `{title, body_markdown, tags[], collection_id}`.
- GET `/api/v1/notes/{id}` — returns note, versions metadata.
- GET `/api/v1/notes` — query with filters, pagination.
- POST `/api/v1/notes/{id}/summarize` — request AI-generated summary, enqueued.

## 5. Documents Service

- POST `/api/v1/documents` — multipart file upload. Returns document id and ingestion job id.
- GET `/api/v1/documents/{id}/text` — raw extracted text.
- GET `/api/v1/documents/{id}/pdf` — original download.

## 6. Search & AI Service

- POST `/api/v1/search/query` — `{q: string, top_k:int=10, filters: {...}}` -> returns `hits[]` with `score` and `source_refs`.
- POST `/api/v1/ai/qa` — `{question, contextIds?}` -> returns `{answer, sources[], costEstimates}`.

## 7. Agent Service

- POST `/api/v1/agents` — spawn agent with manifest `{type, goal, inputs, allowed_tools}`.
- GET `/api/v1/agents/{id}` — status and logs.

## 8. Event Envelope

All domain events follow a common envelope:

```
{
  "event_id": "uuid",
  "type": "note.created|document.ingested|embedding.created|agent.started",
  "occurred_at": "ISO8601",
  "aggregate_id": "user|note|document id",
  "payload": { ... },
  "meta": { "source": "service-name", "trace_id": "..." }
}
```

## 9. Initial Database Tables (high level)

- `users` (id, email, name, hashed_password, created_at, updated_at, settings JSONB)
- `sessions` (id, user_id, device_info, refresh_token_hash, created_at, expires_at)
- `notes` (id, user_id, title, body_markdown, body_html, created_at, updated_at, visibility, version)
- `note_versions` (id, note_id, body_markdown, created_at, author)
- `documents` (id, user_id, filename, mime, size, object_key, ingestion_status, created_at)
- `document_texts` (id, document_id, page_number, text, lang)
- `embeddings` (id, owner_id, owner_type, vector, dims, created_at) — vector stored in vector DB or as references
- `kg_nodes` (id, user_id, type, label, metadata JSONB)
- `kg_edges` (id, from_node, to_node, relation, weight, created_at)
- `tasks` (id, user_id, project_id, title, status, due_date, created_at)
- `projects` (id, user_id, title, description, metadata JSONB)
- `events_log` (id, event_type, payload JSONB, occurred_at)

Indexes: add GIN on JSONB where needed, full-text indexes on `document_texts.text`, and indexes for timestamp fields and FK columns used in queries.

## 10. Migration Strategy

- Use Alembic for versioned migrations. Start with `users`, `notes`, `documents`, `embeddings` and `events_log`.
- Add migration scripts for indexing and performance tuning after initial load testing.

## 11. Tests and Contract Validation

- Create OpenAPI specs for user-facing services and use contract tests (schemathesis or Dredd) in CI.
- Add unit tests for embedding generation, search ranking, and AI service prompt builders.

---

Author: MEMORIA AI — Engineering
