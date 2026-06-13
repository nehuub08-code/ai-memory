# MEMORIA AI — Agent Architecture

Last updated: 2026-06-13

This document outlines the design of autonomous agents in MEMORIA AI: manifests, lifecycle, tools, safety controls, orchestration and integration points.

## Agent Types (initial)

- Study Agent: generates study plans, flashcards, spaced repetition schedules.
- Research Agent: ingests documents, extracts claims, and compiles annotated summaries.
- Career Agent: performs resume optimization, tracks applications and suggests opportunities.
- Coding Agent: reviews code snippets, suggests improvements, and can open PR drafts.

## Agent Manifest

An agent is defined by a manifest JSON describing:

- `id`, `owner` (user_id), `type`, `goal` (natural language), `inputs` (documents/notes references), `allowed_tools` (list), `max_runtime`, `budget_limits`, `consent_scopes`.

## Tools

- Internal tools: Notes API, Search API, Documents API, Task API.
- External tools: GitHub, Calendar, Email (require explicit user consent and OAuth tokens).

## Lifecycle & Orchestration

1. User spawns agent via Agent Service.
2. Agent Service validates manifest, checks RBAC/consent, and enqueues a task.
3. Worker picks up the job and spawns an isolated execution environment (lightweight sandbox/container).
4. Agent performs steps, emits progress events, checkpoints intermediate state to Memory Service.
5. On completion, Agent emits `agent.completed` with results and suggested actions.

## State & Checkpointing

- Checkpoints stored in Memory Service as `agent.checkpoint` events (allow resume and audit).

## Safety & Governance

- Agents operate under `allowed_tools` whitelist; critical actions (e.g., sending email, creating or deleting tasks) require explicit user confirmation unless pre-authorized.
- Rate limit agent API calls and enforce budget constraints per agent.
- Logging and audit trail for every agent action; users can revoke agent permissions.

## Collaboration & Multi-Agent Flows

- Agents can spawn sub-agents (e.g., research agent delegates summarization to a document agent). Communication happens via event bus and shared Memory Service.

## Observability

- Agents produce structured logs and metrics (runtime, API calls count, LLM cost estimates) visible in Analytics Service.

## Next Steps

- Implement a simple agent runner that can run predefined tasks (e.g., summarize a set of documents) and return structured results.

---

Author: MEMORIA AI — Agents Team
