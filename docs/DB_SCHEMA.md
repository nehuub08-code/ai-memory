# MEMORIA AI — Database Schema (Design Notes)

Last updated: 2026-06-13

This document explains the core relational schema for MEMORIA AI, index strategy, and rationale for storage choices.

## Goals

- Support fast write/read for notes and documents.
- Efficient semantic retrieval via vector DB (Chroma) with references in Postgres.
- Support auditability and event replay.

## Core tables (summary)

- `users`: accounts and settings.
- `sessions`: refresh tokens and session metadata.
- `notes`, `note_versions`: authorable content with version history.
- `documents`, `document_texts`: ingest and page-level extracted text.
- `embeddings`: metadata linking owner (note/document) to vector store reference and optional local vector (pgvector).
- `kg_nodes`, `kg_edges`: knowledge graph nodes and relations.
- `tasks`, `projects`: project and task management.
- `events_log`: durable event storage for domain events and audit.

## Indexing & Performance

- Full-text search: use `to_tsvector` on `document_texts.text` with GIN index for keyword fallback.
- JSONB: use GIN indexes on `metadata` and `settings` fields for flexible queries.
- Embeddings: prefer vector DB for similarity; include `pgvector` column for small-scale local testing or fallback.
- Time series queries: indexes on `created_at` and `user_id` for efficient timelines.

## Partitioning & Growth

- For very large stores (documents, embeddings), partition `document_texts` by time or by `document_id` range.
- Archival: older embeddings and derived caches can be moved to cold storage.

## Retention & Deletion

- Soft-delete pattern with `deleted_at` timestamp where needed; provide deletion jobs to scrub user data on request.

## Migration strategy

- Start with single-node Postgres and Alembic-managed migrations.
- After load testing, add read replicas, partitioning, and tuning (connection pool size, prepared statements, vacuum schedules).

---

See `infra/db/schema.sql` for the initial DDL used to create core tables.
