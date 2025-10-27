from datetime import datetime
import os
import psycopg2
from psycopg2.extras import register_uuid
from dotenv import load_dotenv

load_dotenv()
register_uuid()

DB_CONNECTION = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DB_CONNECTION)
conn.autocommit = True

def init_db():
    # read init_db.sql and execute it
    with open("src/db_scripts/init_db.sql", "r") as f:
        schema = f.read()
    with conn.cursor() as cur:
        cur.execute(schema)
    print("✅ Database initialized.")


# Functions related to embeddings

def upsert_embedding(job_id, expires_at, embedding):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO job_embeddings (id, expires_at, embedding)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE 
            SET expires_at = EXCLUDED.expires_at,
                embedding = EXCLUDED.embedding;
        """, (job_id, expires_at, embedding.tolist()))


# Functions related to FAISS index

def persist_faiss_index(faiss_bytes, index_name):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO faiss_index ("name", index_data)
            VALUES (%s, %s)
            ON CONFLICT (name) DO UPDATE SET index_data = EXCLUDED.index_data;
        """, (index_name, faiss_bytes))


def load_faiss_index(index_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT index_data
            FROM faiss_index
            WHERE name = %s
        """, (index_name,))
        row = cur.fetchone()
        if row:
            return row[0]
        return None


# Functions related to FAISS index map

def insert_faiss_index_map(job_id, position):
    # Get the next position
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO faiss_index_map (position, job_id)
            VALUES (%s, %s)
            ON CONFLICT (job_id) DO NOTHING
        """, (position, job_id))


def load_faiss_index_map():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT position, job_id
            FROM faiss_index_map
            ORDER BY position
        """)
        rows = cur.fetchall()

        return [job_id for _, job_id in rows]
    return []


def insert_recommendation(user_id, recommended_job_id, score):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO job_recommendation (user_id, job_id, similarity_score, recommended_at) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, job_id) DO UPDATE 
            SET similarity_score = EXCLUDED.similarity_score,
                recommended_at = EXCLUDED.recommended_at;
        """,
         (user_id, recommended_job_id, score, datetime.now()))
    pass
        