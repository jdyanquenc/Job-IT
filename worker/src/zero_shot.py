from transformers import pipeline
from db import count_profiles, init_db, load_recommendations, update_recommendation_relevance



from dotenv import load_dotenv
from tqdm import tqdm




# -------------------------------
# 1. Zero-shot model
# -------------------------------
clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def infer_label(perfil, oferta):
    text = f"Perfil: {perfil}\nOferta: {oferta}"
    labels = ["relevante", "no relevante"]

    result = clf(text, labels)
    pred = result["labels"][0]

    return 1 if pred == "relevante" else 0



def process_chunk(chunk):
    for recommendation_data in chunk:
        label = infer_label(recommendation_data.get("profile"), recommendation_data.get("job_summary"))
        update_recommendation_relevance(recommendation_data.get("job_id"), recommendation_data.get("user_id"), label)


def main():
    load_dotenv()
    init_db()
    
    
    BATCH_SIZE = 2000
    NUM_WORKERS = 4  # Ajusta según CPU

    total = count_profiles()
    print(f"Total a procesar: {total}")


    with tqdm(total=total, desc="Procesando documentos", dynamic_ncols=True) as pbar:
        while True:
            rows = load_recommendations(BATCH_SIZE)
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