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
            INSERT INTO faiss_index ("name", index_data, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (name) DO UPDATE
            SET index_data = EXCLUDED.index_data,
                updated_at = NOW()
        """, (index_name, faiss_bytes))


def load_faiss_index(index_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT index_data
            FROM faiss_index
            WHERE name = 'jobit_faiss_index'
        """)
        row = cur.fetchone()
        if row:
            return row[0]
        return None


# Functions related to FAISS index map

def insert_faiss_index_map(job_id, position, index_name):
    # Get the next position
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO faiss_index_map (position, job_id, index_name)
            VALUES (%s, %s, %s)
        """, (position, job_id, index_name))


def load_faiss_index_map(index_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT position, job_id
            FROM faiss_index_map
            WHERE index_name = 'jobit_faiss_index'
            ORDER BY position
        """)
        rows = cur.fetchall()

        return [(job_id, position) for position, job_id in rows]
    return []

def clear_recommendations(user_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM job_recommendation WHERE user_id = %s", (user_id,))
    pass

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


def count_jobs_without_embedding():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(1)
            FROM job_entry je
            LEFT JOIN job_embeddings jb ON jb.id = je.id
            WHERE jb.id IS NULL
            
        """)
        row = cur.fetchone()
        if row:
            return row[0]
        return None


def load_jobs(batch_size: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                je.id AS job_id, 
                je.expires_at AS job_expiration,
                je.job_title || ' ' ||
                jd.job_description || ' ' ||
                jd.responsibilities || ' ' ||
                jd.skills as job_detail
            FROM job_entry je
            JOIN job_detail jd ON jd.id = je.id
            LEFT JOIN job_embeddings jb ON jb.id = je.id
            WHERE jb.id IS NULL
            
            ORDER BY je.id
            LIMIT %s
        """, (batch_size,)) 

        rows = cur.fetchall()

        colnames = [desc[0] for desc in cur.description]

        jobs = [dict(zip(colnames, row)) for row in rows]

        return jobs
    
def count_profiles():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(1)
            FROM user_profile up
        """)
        row = cur.fetchone()
        if row:
            return row[0]
        return None

def load_profiles(batch_size: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                up.id as user_id, 
                up.title as profile_title,
                up.description as profile_detail
            FROM user_profile up
            ORDER BY up.id
            LIMIT %s
        """, (batch_size,)) 

        rows = cur.fetchall()

        colnames = [desc[0] for desc in cur.description]

        profiles = [dict(zip(colnames, row)) for row in rows]

        return profiles