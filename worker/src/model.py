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
        id_map = load_faiss_index_map(FAISS_INDEX_NAME)
        
        print("FAISS index loaded.")
    else:
        faiss_index = faiss.IndexFlatIP(384)
        id_map = []
        print("New FAISS index created.")


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
    insert_faiss_index_map(job_id, position, FAISS_INDEX_NAME)


def update_faiss_index():
    global last_persist_time
    if datetime.now() - last_persist_time > timedelta(seconds=persist_interval):
        faiss_bytes = faiss.serialize_index(faiss_index).tobytes()
        persist_faiss_index(faiss_bytes, FAISS_INDEX_NAME)
        last_persist_time = datetime.now()
        print("FAISS index persisted.")


def recommend_jobs(profile_data, k=10):
    user_id = profile_data.get("user_id", "")
    updated_at = profile_data.get("updated_at", "")
    profile_detail = profile_data.get("profile_detail", "")

    profile_embedding = model.encode([profile_detail], normalize_embeddings=True)
    scores, positions = faiss_index.search(profile_embedding, k)
    
    for position, score in zip(positions[0], scores[0]):
        # Insert only if score is above a threshold

        job_id = id_map[position]
        # "job_id" is of type uuid but expression is of type record
        job_id = job_id[0]
        #print(f"Job ID: {job_id}, Score: {score}")
        insert_recommendation(user_id, job_id, float(score))


def get_related_jobs(job_id, k=5):
    # Find the position of the job_id in the id_map
    position = next((pos for jid, pos in id_map if jid == job_id), None)
    if position is None:
        return []

    # Get the embedding of the job at that position
    job_embedding = faiss_index.reconstruct(position).reshape(1, -1)

    # Search for similar jobs
    scores, positions = faiss_index.search(job_embedding, k + 1)  # +1 to exclude itself

    related_jobs = []
    for pos, score in zip(positions[0], scores[0]):
        if pos != position:  # Exclude the original job
            related_job_id = id_map[pos][0]
            related_jobs.append((related_job_id, float(score)))

    return related_jobs