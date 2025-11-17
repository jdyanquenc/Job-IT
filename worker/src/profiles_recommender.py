from db import count_profiles, init_db, load_profiles

from concurrent.futures import ProcessPoolExecutor, as_completed
from model import init_embedding, recommend_jobs
from dotenv import load_dotenv
from tqdm import tqdm



def process_chunk(chunk):
    for profile_data in chunk:
        recommend_jobs(profile_data)


def main():
    load_dotenv()
    init_db()
    init_embedding()
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

            for chunk in chunks:
                process_chunk(chunk)
                pbar.update(len(chunk))

    print("\n✅ Procesamiento completado con éxito.")

if __name__ == "__main__":
    main()
