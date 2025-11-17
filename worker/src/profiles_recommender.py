from db import count_profiles, init_db, load_profiles

from concurrent.futures import ProcessPoolExecutor, as_completed
from psycopg2.pool import SimpleConnectionPool
from model import recommend_jobs
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


def main():
    load_dotenv()
    # init_db() # si tienes una función para inicializar la DB
    BATCH_SIZE = 2000
    NUM_WORKERS = 4  # Ajusta según CPU

    total = count_profiles()
    print(f"Total a procesar: {total}")

    with tqdm(total=total, desc="Procesando documentos", dynamic_ncols=True) as pbar:
        while True:
            rows = load_profiles(BATCH_SIZE)
            if not rows:
                break

            # Dividir en sub-batches para multiprocessing
            chunk_size = 100  # puedes ajustar
            chunks = [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)]

            with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
                futures = [executor.submit(recommend_jobs, chunk) for chunk in chunks]
                for f in as_completed(futures):
                    pbar.update(f.result())

    print("\n✅ Procesamiento completado con éxito.")

if __name__ == "__main__":
    main()
