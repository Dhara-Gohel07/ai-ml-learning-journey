from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = 'all-MiniLM-L6-v2'

def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)

def generate_embeddings(model, texts):
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings)

