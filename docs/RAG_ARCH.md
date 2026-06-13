# MEMORIA AI — RAG & Vector Retrieval Architecture

Last updated: 2026-06-13

This document explains the Retrieval-Augmented Generation (RAG) pipeline, vector DB abstraction, chunking and indexing strategies, and citation handling.

## Objectives

- Deliver accurate answers using user-owned data with clear citations.
- Keep LLM context minimal via compression and relevance filtering to control cost.

## Pipeline Steps

1. Ingestion: Document/text is chunked and normalized (language detection, cleaning).
2. Embedding: Chosen embedding model produces vectors per chunk; metadata stored in `embeddings` table and vector DB.
3. Indexing: Vector DB (Chroma in MVP) stores vectors and provides similarity search.
4. Retrieval: For a query, retrieve top-N by vector similarity and apply keyword filtering via Postgres/full-text.
5. Reranking: Apply lightweight reranker (BM25 or small model) to reorder candidates.
6. Context Assembly: Compose top-K passages with provenance; apply context compression if needed.
7. LLM Call: Send to provider with instruction template and citations.
8. Response: Return answer and attach source list (doc IDs, passages, confidence).

## Chunking Strategy

- Use semantic chunking by paragraph and sentence boundaries with configurable chunk size (tokens or characters).
- Overlap chunks to preserve context (10-20% overlap by tokens).

## Vector DB Abstraction

- Provide an adapter interface supporting Chroma, Pinecone, Qdrant, and Milvus.
- Store a `vector_reference` in the relational DB to link chunks to documents and note owners.

## Context Compression & Summarization

- For long document sets, perform iterative compression: summarize groups of passages into concise abstracts and index both passes.

## Citation & Attribution

- Each retrieved passage includes `source_id`, `doc_id`, `page_number`, `offset`, `score`.
- Responses include numbered citations mapping to original documents and passages; UI displays expand-to-source.

## Multi-query & Parent-child Retrieval

- Support multi-phase retrieval: initial coarse retrieval, followed by targeted child queries to gather supporting evidence.

## Evaluation & Quality Metrics

- Precision@k, Recall@k measured on labeled QA datasets created from user test data.
- Monitor hallucination rate using human-in-the-loop checks and user feedback.

## Cost Controls

- Cache frequent queries, use smaller (cheaper) models for reranking, and only call large LLMs for final synthesis.

---

Author: MEMORIA AI — Retrieval Team
