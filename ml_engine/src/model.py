from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(input_text: str):
    return embedder.encode(input_text, normalize_embeddings=True)

def classify_embedding(embedding):
    # Esto luego se reemplaza con un modelo entrenado
    return "General"
