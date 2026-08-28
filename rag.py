from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = None


def get_embedding_model():

    global embedding_model

    if embedding_model is None:

        print("Loading embedding model...")

        embedding_model = SentenceTransformer(
            MODEL_NAME
        )

        print("Embedding model loaded.")

    return embedding_model


def create_embeddings(chunks):

    model = get_embedding_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return np.array(embeddings)


def embed_query(query):

    model = get_embedding_model()

    embedding = model.encode(
        [query]
    )

    return np.array(embedding[0])


def search_similar_chunks(
    query,
    chunks,
    embeddings,
    top_k=4,
    similarity_threshold=0.30
):

    query_embedding = embed_query(query)

    chunk_norms = np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    normalized_chunks = (
        embeddings / chunk_norms
    )

    query_norm = np.linalg.norm(
        query_embedding
    )

    normalized_query = (
        query_embedding / query_norm
    )

    scores = np.dot(
        normalized_chunks,
        normalized_query
    )

    top_indices = np.argsort(
        scores
    )[::-1]

    results = []

    for index in top_indices:

        score = float(
            scores[index]
        )

        if score < similarity_threshold:
            continue

        results.append({

            "chunk_id": chunks[index]["chunk_id"],

            "text": chunks[index]["text"],

            "page": chunks[index]["page"],

            "score": float(scores[index])

        })

        if len(results) >= top_k:
            break

    return results