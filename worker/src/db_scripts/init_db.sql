CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS job_embeddings (
    id UUID PRIMARY KEY,
    expires_at TIMESTAMP,
    embedding VECTOR(384)
);

CREATE TABLE IF NOT EXISTS faiss_index_map (
    position INT PRIMARY KEY,
    job_id UUID REFERENCES job_embeddings(id),
    CONSTRAINT unique_job_id UNIQUE (job_id)
);

CREATE TABLE IF NOT EXISTS faiss_index (
    "name" TEXT PRIMARY KEY,
    index_data BYTEA
);