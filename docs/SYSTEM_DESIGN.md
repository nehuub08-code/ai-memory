# MEMORIA AI — System Design (High-Level)

Last updated: 2026-06-13

## Overview

This document describes the high-level system design for MEMORIA AI. It outlines components, responsibilities, data flow, scaling model, and integration points. The design follows Clean Architecture, Hexagonal boundaries, CQRS where appropriate, event-driven patterns for async processing, and microservice-friendly modularity.

## Major Components

- **API Gateway / Edge**: TLS termination, rate limiting, authentication integration (OAuth/JWT), request routing to services or Next.js frontend.
- **Auth Service**: Handles sign-up, sign-in, OAuth flows (Google, GitHub, Microsoft), JWT issuance, refresh tokens, 2FA, RBAC.
- **User Service**: User profiles, preferences, settings, device sessions and multi-device management.
- **Notes Service**: CRUD for notes (Markdown), versioning, tagging, collections, AI-generated titles/tags.
- **Documents Service**: File upload, storage (object store), OCR and text extraction pipelines, metadata extraction, format converters.
- **Knowledge Service**: Entity extraction, relationship inference, knowledge graph storage (as edges in Postgres + optional graph DB interface).
- **Memory Service**: Short-term / long-term memory store, temporal indexing, episodic memory records.
- **AI Service**: RAG orchestration, prompt management, LLM API adapters (OpenAI, Anthropic, local LLMs), cost controls, caching.
- **Search Service**: Vector indexing (Chroma adapter), hybrid search (keyword + vector), reranking, result scoring and attribution metadata.
- **Agent Service**: Orchestrates autonomous agents (study agent, research agent), manages task queues and safe-execution sandboxing.
- **Task & Project Service**: Task generation, milestones, GitHub integration, progress tracking.
- **Analytics Service**: Aggregates usage, learning progress, knowledge growth metrics.
- **Notification Service**: Email, push, in-app notifications, scheduling.

## Data Stores

- **Primary OLTP**: PostgreSQL for authoritative relational data (users, notes metadata, KG edges, tasks, projects).
- **Vector Store**: ChromaDB adapter for embeddings; design allows swapping to Pinecone/Qdrant/Milvus.
- **Object Storage**: S3-compatible (MinIO locally) for files and media.
- **Cache / Broker**: Redis for caching, sessions, and Celery broker (or Kafka for higher throughput/event sourcing setups).
- **Search Indexes**: Hybrid approach: Postgres full-text for keyword search + vector DB for semantic retrieval.

## Integration & Messaging

- **Synchronous APIs**: FastAPI REST endpoints for user-facing operations and admin APIs.
- **Async Processing**: Celery workers (or Kafka + consumer) for heavy jobs: document processing, embedding generation, OCR, knowledge graph inference, and background agent tasks.
- **Event Bus**: Domain events (note.created, document.ingested, embedding.created, user.deleted) emitted to the message broker and persisted as event logs for audit and replay.

## RAG & Retrieval Flow (Simplified)

1. User issues a query to Search/AI endpoint.
2. Search Service performs hybrid retrieval: keyword filter in Postgres + vector similarity in Chroma.
3. Top-k candidates are reranked and sent to AI Service.
4. AI Service composes context window with citations, compresses if necessary, and calls LLM via provider adapter.
5. Response returned with source attributions and confidence metadata; optionally stored in Conversation Memory.

## Agent Orchestration (High Level)

- Agents are defined by a manifest (goal, tools, allowed scopes). The Agent Service spawns agents as tasks in the queue and tracks their state.
- Agents may call internal services (notes, search, docs) via service-to-service authenticated calls — limited by RBAC and rate-limits.
- Long-running agents checkpoint state into Memory Service and emit events for audit and UI updates.

## Security & Privacy by Design

- JWT + Refresh tokens, RBAC enforcement in each service boundary.
- Encryption in transit (TLS) and at rest (database disk encryption + S3 SSE).
- Secrets in environment managers or secret stores (HashiCorp Vault, cloud KMS).
- Audit logs for sensitive actions (data exports, deletions, connector authorizations).

## Scalability & Availability

- Services are stateless where possible; stateful data held in Postgres / Chroma / S3 / Redis.
- Use horizontal pod autoscaling for CPU-bound services; provisioned instances for vector DB if required.
- Design for graceful degradation: if LLM provider is unavailable, return cached summaries or degrade to keyword search.

## Observability

- Distributed tracing with OpenTelemetry to instrument user requests across services.
- Metrics exported to Prometheus; dashboards in Grafana for latency, error rates, LLM cost per request, ingestion throughput.
- Structured logging (JSON) with correlation IDs for request tracing.

## Cost & Provider Routing

- Implement a Model Router in the AI Service to choose between local LLMs and hosted providers based on cost/latency/accuracy.
- Cache embeddings and LLM responses where safe to reduce repeated provider calls.

## Deployment Model

- Development: Docker Compose with local Postgres, Redis, MinIO, and Chroma (or in-memory adapter).
- Staging/Production: Kubernetes clusters, managed cloud services for Postgres (RDS), Redis (Elasticache), S3, and managed vector DBs optionally.

## Next Steps

- Produce Low-Level Architecture with ER diagrams and per-service API contracts.
- Design database schema and indexes for core entities.
- Define the async event contract and message envelope format.

---

Author: MEMORIA AI — Architecture Team
