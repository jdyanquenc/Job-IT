from db import init_db, count_jobs_without_embedding, load_jobs



from concurrent.futures import ProcessPoolExecutor, as_completed
from psycopg2.pool import SimpleConnectionPool
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os
import psycopg2
from dotenv import load_dotenv

# --- Variables globales por proceso ---
model = None
db_pool = None

def init_resources():
    """Inicializa el modelo y el pool de conexiones en cada proceso."""
    global model, db_pool

    if model is None:
        model = SentenceTransformer(
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
            device='cpu'
        )

    if db_pool is None:
        db_pool = SimpleConnectionPool(
            minconn=1,
            maxconn=4,
            dsn=os.getenv("DATABASE_URL")
        )

def save_embeddings_to_db(batch):
    """Guarda un lote de embeddings con job_expiration en la base de datos."""
    init_resources()
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            args_str = ",".join(
                cur.mogrify("(%s, %s, %s)", (job_id, embedding.tolist(), job_exp)).decode("utf-8")
                for job_id, embedding, job_exp in batch
            )
            cur.execute(f"""
                INSERT INTO job_embeddings (id, embedding, expires_at)
                VALUES {args_str}
                ON CONFLICT (id) DO UPDATE 
                SET embedding = EXCLUDED.embedding,
                    expires_at = EXCLUDED.expires_at
            """)
        conn.commit()
    finally:
        db_pool.putconn(conn)

def generate_embeddings_batch(batch):
    """Procesa un batch de jobs en paralelo, incluyendo job_expiration."""
    init_resources()
    job_ids = [job["job_id"] for job in batch]
    texts = [job.get("job_detail", "") for job in batch]
    expirations = [job.get("job_expiration", None) for job in batch]

    embeddings = model.encode(texts, batch_size=64, show_progress_bar=False, normalize_embeddings=True)
    save_embeddings_to_db(list(zip(job_ids, embeddings, expirations)))
    return len(batch)

def main():
    load_dotenv()
    # init_db() # si tienes una función para inicializar la DB
    BATCH_SIZE = 2000
    NUM_WORKERS = 4  # Ajusta según CPU

    total = count_jobs_without_embedding()
    print(f"Total a procesar: {total}")

    with tqdm(total=total, desc="Procesando documentos", dynamic_ncols=True) as pbar:
        while True:
            rows = load_jobs(BATCH_SIZE)
            if not rows:
                break

            # Dividir en sub-batches para multiprocessing
            chunk_size = 100  # puedes ajustar
            chunks = [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)]

            with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
                futures = [executor.submit(generate_embeddings_batch, chunk) for chunk in chunks]
                for f in as_completed(futures):
                    pbar.update(f.result())

    print("\n✅ Procesamiento completado con éxito.")

if __name__ == "__main__":
    main()
