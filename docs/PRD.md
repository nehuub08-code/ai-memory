# MEMORIA AI — Product Requirements Document (PRD)

Version: 0.1
Last updated: 2026-06-13

## 1. Vision

MEMORIA AI is a personal AI operating system and second brain that remembers, organizes, and helps the user act on their personal knowledge and experience. It combines long-term memory, knowledge graph capabilities, multimodal ingestion, advanced retrieval (RAG), and autonomous agents to become the user's memory, study coach, project manager, and personal research assistant — while keeping data ownership and privacy centralized with the user.

## 2. Target Users & Personas

- **Student (CS/Engineering)**: Studies algorithms and systems; wants to track learning progress, generate revision plans, and prepare for interviews.
- **Knowledge Worker (PM/Researcher)**: Collects articles, meeting notes, and research; needs cross-document search and summarization.
- **Developer**: Tracks project decisions, code snippets, and task history; wants code-specific search and agent-assisted refactor suggestions.
- **Career Seeker**: Prepares resumes, interview practice, skill-gap analysis, and application tracking.
- **Everyday User**: Wants a private memory of their life events, receipts, and voice notes accessible via natural language.

## 3. Problem Statement

Users are overwhelmed by fragmented information across apps (notes, email, documents, chat, audio) and lack a single private system that:

- Remembers their past activities and learnings.
- Answers natural language questions using their own data.
- Helps plan and act (revision plans, project milestones).
- Ensures data privacy and user ownership.

## 4. Core Principles

- **User-Owned Data**: All answers are derived from user-owned data unless they explicitly request external web search.
- **Composable Architecture**: Services must be modular, testable, and swappable (e.g., vector DB adapters).
- **Privacy by Design**: Defaults emphasize local control, encryption, and opt-in sharing.
- **Explainability & Attribution**: Responses must reference sources (documents, notes) and show confidence.
- **Progressive Disclosure**: Start with a lean MVP and expand into multimodal, agent orchestration, and advanced analytics.

## 5. MVP Scope (Phase 1)

Goal: Provide personal knowledge ingestion, semantic search, note/document queries, and basic study & project assistance.

Must-have features:

- User authentication (email/password, OAuth: Google, GitHub, Microsoft).
- Notes: create, edit (Markdown), tag, and version history.
- Document ingestion: PDF, DOCX, TXT upload with OCR for images.
- Vector search using ChromaDB adapter; semantic search + keyword fallback.
- RAG pipeline for question answering with source citations.
- Basic memory timelines and simple knowledge graph (entities + links).
- Study Assistant: generate summary, flashcards, simple revision plan from notes.
- Privacy: user data stored in their account, encryption in transit; configurable retention.

Out of scope for MVP:

- Autonomous multi-agent orchestration, real-time multimodal streaming, enterprise SSO, full analytics dashboards, mobile clients.

## 6. Key Use Cases & User Stories

- As a student, I can ask “What DSA topics did I study last month?” and get a list of sessions, notes, and resources.
- As a researcher, I can upload a set of PDFs and ask, “Summarize everything about X with sources.”
- As a developer, I can search across code snippets and notes for “database schema for payments”.
- As a user, I can ask “What were my goals in January?” and get my written goals and associated tasks.

## 7. Success Metrics

- Activation: % of new users who ingest at least 3 documents or 10 notes in the first week.
- Retention: 30-day retention of active search or notebook queries.
- Latency: 95th percentile for simple semantic query responses < 1.5s (without heavy LLM calls).
- Accuracy & Trust: User-reported helpfulness score > 4/5 in beta.
- Cost Efficiency: Average LLM token cost per query below budget targets.

## 8. Non-Functional Requirements

- Scalability: Microservice-ready; able to scale reading/writing services independently.
- Availability: Target 99.9% uptime for core query paths.
- Security: OWASP top 10 mitigations, RBAC, rate-limiting, and encrypted secrets.
- Observability: Tracing with OpenTelemetry, metrics via Prometheus, dashboards in Grafana.
- Portability: Deployable to major clouds and Kubernetes.

## 9. Data & Privacy Model

- Users own their data. Default: data stored in user's project/account in encrypted storage.
- Option: export/import full data bundle (notes, embeddings, KG) in standard formats.
- Access: fine-grained consent for third-party connectors and shared links.
- Retention: configurable retention & deletion; audit logs for deleted/restored content.

## 10. Compliance & Legal

- GDPR and CCPA considerations for personal data; provide data export and deletion APIs.
- Ensure external connectors (Google Drive, GitHub) obey OAuth scopes and only access allowed scopes.

## 11. Monetization & Business Model (High Level)

- Freemium: limited storage, limited queries per month, small models for free.
- Paid tiers: more storage, enterprise integrations, advanced agent credits, team sharing, SSO.
- Enterprise: on-prem or VPC deployment, advanced governance, audit logs, SLA.

## 12. Risks & Mitigations

- Risk: High LLM costs. Mitigation: model routing, caching, summarization to reduce context size.
- Risk: Privacy concerns. Mitigation: strict defaults, audit logs, clear privacy UI.
- Risk: Poor attribution/accuracy. Mitigation: RAG with citation and confidence scoring; human-in-the-loop correction.

## 13. Acceptance Criteria for MVP

- User can sign up and connect at least one OAuth provider.
- User can create notes and upload documents; documents are indexed and searchable.
- Semantic search returns relevant documents and shows at least one source citation.
- Study Assistant can generate a 1-week revision plan from a selected topic.

## 14. Timeline & Next Steps

Phase 0 (Week 0): Detailed PRD sign-off and architecture overview.
Phase 1 (Weeks 1–6): Core backend services (Auth, User, Notes, Documents), ingestion, Chroma adapter, basic RAG, frontend MVP.
Phase 2 (Weeks 7–14): Knowledge graph, Memory service, Study Assistant improvements, connectors (Drive, GitHub), token cost optimizations.
Phase 3 (Weeks 15–26): Agents, analytics, autoscaling deployment, enterprise features, security hardening.

## 15. TODOS (near term)

- Finalize API contracts for Auth, Notes, Documents, and Search.
- Define the DB schema for core entities (users, notes, documents, embeddings, KG edges).
- Implement Chroma adapter and a retriever proof-of-concept.

---

Author: MEMORIA AI — Product Team
