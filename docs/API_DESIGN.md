# MEMORIA AI — API Design

Last updated: 2026-06-13

This document captures the API surface for public and internal services, authentication patterns, error conventions and example payloads.

## API Fundamentals

- Base path: `/api/v1`
- Auth: Bearer `Authorization: Bearer <jwt>` for user requests; mTLS or service JWT for service-to-service.
- Content type: `application/json` for APIs, `multipart/form-data` for file uploads.
- Errors: use HTTP status codes and structured error body `{code, message, details?}`.

## Common Response Envelope

```
{
  "status": "ok" | "error",
  "data": {...} | null,
  "error": {"code": "string", "message": "string", "details": {...}} | null,
  "meta": {...}
}
```

## Authentication Endpoints

- POST `/api/v1/auth/signup`
- POST `/api/v1/auth/login`
- POST `/api/v1/auth/oauth/start` -> redirects to provider
- POST `/api/v1/auth/token/refresh`

## Notes API

- POST `/api/v1/notes` -> create note
- GET `/api/v1/notes` -> list notes with filtering and pagination
- GET `/api/v1/notes/{id}` -> return note and versions
- PATCH `/api/v1/notes/{id}` -> update note
- DELETE `/api/v1/notes/{id}` -> soft-delete and emit `note.deleted` event

## Documents API

- POST `/api/v1/documents` -> upload file. Response includes `ingestion_job_id`.
- GET `/api/v1/documents/{id}` -> metadata
- GET `/api/v1/documents/{id}/text` -> extracted text

## Search & AI API

- POST `/api/v1/search/query` -> `{q, top_k, filters}` -> returns `hits[]`
- POST `/api/v1/ai/qa` -> `{question, context_ids?}` -> returns answer with `sources[]`

## Agent API

- POST `/api/v1/agents` -> spawn agent
- GET `/api/v1/agents/{id}` -> status
- POST `/api/v1/agents/{id}/cancel` -> cancel agent

## Rate Limiting & Quotas

- Apply per-user and per-service quotas. Use token bucket algorithm via API Gateway.

## Versioning

- Start with `v1`; adopt header-based version negotiation for major changes.

---

Author: MEMORIA AI — API Team
