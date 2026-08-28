from rag import search_similar_chunks


def retrieve_chunks(
    query,
    chunks,
    embeddings,
    top_k=4,
    similarity_threshold=0.35
):
    """
    Retrieve the most relevant newspaper chunks.

    Chunks below the similarity threshold are removed.
    This helps the RAG system avoid answering unrelated questions.
    """

    results = search_similar_chunks(
        query,
        chunks,
        embeddings,
        top_k=top_k
    )

    # Remove weakly related results
    filtered_results = [
        result
        for result in results
        if result["score"] >= similarity_threshold
    ]

    return filtered_results