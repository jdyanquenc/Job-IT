from datetime import datetime, timedelta
from uuid import UUID
import numpy as np
from sentence_transformers import SentenceTransformer
from db import insert_faiss_index_map, insert_recommendation, load_faiss_index, load_faiss_index_map, persist_faiss_index, upsert_embedding
import faiss


FAISS_INDEX_NAME = "jobit_faiss_index"

model = None
id_map = None
faiss_index = None

persist_interval = 60  # seconds
last_persist_time = datetime.now() - timedelta(seconds=persist_interval)

def init_embedding():
    global model
    global id_map
    global faiss_index
    
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    #model = SentenceTransformer('all-MiniLM-L6-v2')
    
    index_bytes = load_faiss_index(FAISS_INDEX_NAME)

    # Check if FAISS index exists or create a new one
    if index_bytes:
        faiss_index = faiss.deserialize_index(np.frombuffer(index_bytes, dtype=np.uint8))
        id_map = load_faiss_index_map()
        
        print("✅ FAISS index loaded.")
    else:
        faiss_index = faiss.IndexFlatIP(384)
        id_map = []
        print("✅ New FAISS index created.")


def process_job_data(job_data):
    job_id = job_data.get("job_id", "")
    job_expiration = job_data.get("job_expiration", "")
    job_detail = job_data.get("job_detail", "")

    embedding = generate_embedding(job_id, job_expiration, job_detail)
    position = add_faiss_index_entry(embedding)
    add_faiss_index_map_entry(job_id, position)

    update_faiss_index()


def generate_embedding(id: UUID, expires_at: datetime, input_text: str):
    embedding = model.encode(input_text, normalize_embeddings=True)
    upsert_embedding(id, expires_at, embedding)
    return embedding


def add_faiss_index_entry(embedding):
    faiss_index.add(embedding.reshape(1, -1))
    return faiss_index.ntotal - 1


def add_faiss_index_map_entry(job_id, position):
    id_map.append((job_id, position))
    insert_faiss_index_map(job_id, position)


def update_faiss_index():
    global last_persist_time
    if datetime.now() - last_persist_time > timedelta(seconds=persist_interval):
        faiss_bytes = faiss.serialize_index(faiss_index).tobytes()
        persist_faiss_index(faiss_bytes, FAISS_INDEX_NAME)
        last_persist_time = datetime.now()
        print("💾 FAISS index persisted.")


def recommend_jobs(profile_data, k=5):
    user_id = profile_data.get("user_id", "")
    updated_at = profile_data.get("updated_at", "")
    profile_detail = profile_data.get("profile_detail", "")

    profile_embedding = model.encode([profile_detail], normalize_embeddings=True)
    scores, positions = faiss_index.search(profile_embedding, k)

    

    print("\n🔍 Recommended jobs:")
    for position, score in zip(positions[0], scores[0]):
        # Insert only if score is above a threshold
        if score < 0.7:
            continue

        job_id = id_map[position]
        insert_recommendation(user_id, job_id, float(score))
        print(f"Job ID: {job_id}, Score: {score}")
