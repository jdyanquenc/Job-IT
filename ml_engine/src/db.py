import os
import psycopg2
from psycopg2.extras import register_uuid
from dotenv import load_dotenv

load_dotenv()
register_uuid()

DB_CONN = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DB_CONN)
conn.autocommit = True

def init_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;

            CREATE TABLE IF NOT EXISTS embeddings_jobs (
                uuid UUID PRIMARY KEY,
                category TEXT,
                embedding VECTOR(384)
            );
        """)
    print("✅ Table 'embeddings_jobs' ready.")

def upsert_embedding(uuid, category, embedding):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO embeddings_jobs (uuid, category, embedding)
            VALUES (%s, %s, %s)
            ON CONFLICT (uuid) DO UPDATE 
            SET category = EXCLUDED.category,
                embedding = EXCLUDED.embedding;
        """, (uuid, category, embedding.tolist()))
