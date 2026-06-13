-- MEMORIA AI initial schema
-- Requires PostgreSQL 14+ and the pgvector extension for local embedding storage (optional)

-- Enable pgvector (optional)
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- USERS
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  name TEXT,
  hashed_password TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  settings JSONB DEFAULT '{}'::JSONB
);

-- SESSIONS / REFRESH TOKENS
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  device_info JSONB,
  refresh_token_hash TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  expires_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);

-- NOTES
CREATE TABLE IF NOT EXISTS notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT,
  body_markdown TEXT,
  body_html TEXT,
  visibility TEXT DEFAULT 'private',
  version INT DEFAULT 1,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  metadata JSONB DEFAULT '{}'::JSONB
);
CREATE INDEX IF NOT EXISTS idx_notes_user_id_created_at ON notes(user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS note_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  note_id UUID REFERENCES notes(id) ON DELETE CASCADE,
  body_markdown TEXT,
  author_id UUID,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- DOCUMENTS
CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  filename TEXT,
  mime TEXT,
  size BIGINT,
  object_key TEXT,
  ingestion_status TEXT DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_texts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
  page_number INT DEFAULT 0,
  text TEXT,
  lang TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Full-text index for document_texts
CREATE INDEX IF NOT EXISTS idx_document_texts_tsv ON document_texts USING GIN (to_tsvector('english', coalesce(text, '')));

-- EMBEDDINGS (metadata stored here, vectors stored in vector DB; optional local vector column)
CREATE TABLE IF NOT EXISTS embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID,
  owner_type TEXT,
  vector_reference TEXT, -- id or key in vector DB (Chroma)
  dims INT,
  metadata JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  -- optional local vector column for small-scale use
  vector vector
);
CREATE INDEX IF NOT EXISTS idx_embeddings_owner ON embeddings(owner_id, owner_type);

-- KNOWLEDGE GRAPH
CREATE TABLE IF NOT EXISTS kg_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  type TEXT,
  label TEXT,
  metadata JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS kg_edges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  from_node UUID REFERENCES kg_nodes(id) ON DELETE CASCADE,
  to_node UUID REFERENCES kg_nodes(id) ON DELETE CASCADE,
  relation TEXT,
  weight FLOAT DEFAULT 1.0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- TASKS & PROJECTS
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT,
  description TEXT,
  metadata JSONB DEFAULT '{}'::JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT,
  description TEXT,
  status TEXT DEFAULT 'todo',
  priority INT DEFAULT 3,
  due_date TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- EVENTS LOG
CREATE TABLE IF NOT EXISTS events_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type TEXT,
  aggregate_id TEXT,
  payload JSONB,
  meta JSONB,
  occurred_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_events_log_type ON events_log(event_type);

-- Useful indexes
CREATE INDEX IF NOT EXISTS idx_docs_user ON documents(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_doc_texts_doc_page ON document_texts(document_id, page_number);

-- Note: For production, ensure appropriate connection pool sizing, VACUUM tuning, and migration-based index changes.
