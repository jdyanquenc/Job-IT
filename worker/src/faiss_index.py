import ast
import os
import faiss
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from psycopg2.extras import RealDictCursor, execute_batch
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime

# --- Configuración ---
FAISS_INDEX_NAME = "jobit_faiss_index"
FAISS_DIM = 384  # para MiniLM-L12-v2
BATCH_SIZE = 2000

load_dotenv()

# --------------------------------------------------------
# 🔧 Funciones auxiliares de base de datos
# --------------------------------------------------------

def get_db_connection():
    """Crea una conexión a PostgreSQL."""
    return psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)


def load_all_embeddings():
    """Carga todos los embeddings desde la tabla job_embeddings."""
    conn = get_db_connection()
    embeddings = []
    job_ids = []
    expirations = []

    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM job_entry je
            JOIN job_embeddings jb ON jb.id = je.id
            WHERE je.country_id = 'c7e69a65-f1b8-4390-b71b-ad43424794de'
        """)
        total = cur.fetchone()["count"]

        print(f"📦 Total embeddings a procesar: {total}")
        offset = 0

        with tqdm(total=total, desc="Cargando embeddings", dynamic_ncols=True) as pbar:
            while True:
                cur.execute("""
                    SELECT jb.id, jb.expires_at, jb.embedding
                    FROM job_entry je
                    JOIN job_embeddings jb ON jb.id = je.id
                    WHERE je.country_id = 'c7e69a65-f1b8-4390-b71b-ad43424794de'
                    ORDER BY id
                    LIMIT %s OFFSET %s
                """, (BATCH_SIZE, offset))

                rows = cur.fetchall()
                if not rows:
                    break

                for row in rows:
                    
                    try:
                        emb = np.array(ast.literal_eval(row["embedding"]), dtype=np.float32)
                        embeddings.append(emb)
                        job_ids.append(row["id"])
                        expirations.append(row["expires_at"])
                    except (ValueError, SyntaxError):
                        print(f"Skipping row with bad embedding: {row['id']}")
                    

                offset += BATCH_SIZE
                pbar.update(len(rows))

    conn.close()
    return np.vstack(embeddings), job_ids, expirations


# --------------------------------------------------------
# 🧱 Funciones para reconstruir y guardar el índice FAISS
# --------------------------------------------------------

def rebuild_faiss_index(embeddings):
    """Crea un índice FAISS nuevo desde todos los embeddings."""
    print("\n🧱 Creando nuevo índice FAISS...")
    index = faiss.IndexFlatIP(FAISS_DIM)
    index.add(embeddings)
    print(f"✅ Índice FAISS construido con {index.ntotal} vectores.")
    return index


def save_faiss_index_to_db(index_bytes):
    """Guarda el índice FAISS serializado en la base de datos."""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO faiss_index (name, index_data, updated_at)
            VALUES (%s, %s, NOW())
            ON CONFLICT (name) DO UPDATE
            SET index_data = EXCLUDED.index_data,
                updated_at = NOW()
        """, (FAISS_INDEX_NAME, psycopg2.Binary(index_bytes)))
        conn.commit()
    conn.close()
    print(f"💾 Índice FAISS '{FAISS_INDEX_NAME}' guardado en la base de datos.")


def save_faiss_map_to_db(job_ids):
    """Guarda el mapa id → posición en la base de datos."""
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM faiss_index_map WHERE index_name = %s", (FAISS_INDEX_NAME,))
        data = [(FAISS_INDEX_NAME, job_id, i) for i, job_id in enumerate(job_ids)]
        execute_batch(cur, """
            INSERT INTO faiss_index_map (index_name, job_id, position)
            VALUES (%s, %s, %s)
        """, data, page_size=5000)
        conn.commit()
    conn.close()
    print(f"🗺️ Mapa de {len(job_ids)} IDs guardado en faiss_index_map.")


# --------------------------------------------------------
# 🚀 Script principal
# --------------------------------------------------------

def main():
    start = datetime.now()
    print("🚀 Iniciando reconstrucción completa del índice FAISS...\n")

    embeddings, job_ids, expirations = load_all_embeddings()
    index = rebuild_faiss_index(embeddings)

    # Serializar y guardar
    faiss_bytes = faiss.serialize_index(index).tobytes()
    save_faiss_index_to_db(faiss_bytes)
    save_faiss_map_to_db(job_ids)

    print(f"\n✅ Reconstrucción completa en {datetime.now() - start}.\n")


if __name__ == "__main__":
    main()
