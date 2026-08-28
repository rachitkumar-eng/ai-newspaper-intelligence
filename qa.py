from retriever import retrieve_chunks
from llm import generate_response


def answer_question(
    question,
    chunks,
    embeddings,
    top_k=4,
    similarity_threshold=0.35
):

    results = retrieve_chunks(
        question,
        chunks,
        embeddings,
        top_k=top_k,
        similarity_threshold=similarity_threshold
    )

    # No sufficiently relevant information
    if not results:

        return (
            "I couldn't find sufficient information about "
            "this in today's newspaper.",
            []
        )

    context_parts = []

    for i, result in enumerate(results, start=1):

        text = result.get("text", "")
        page = result.get("page", "Unknown")
        score = result.get("score", 0)

        context_parts.append(
            f"""
SOURCE {i}
Page: {page}
Similarity: {score:.3f}

{text}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are an AI newspaper assistant.

Answer the user's question using ONLY the information
contained in the retrieved newspaper sources below.

If the answer is not present in the sources, say:

"I couldn't find sufficient information about this in today's newspaper."

Do not use outside knowledge.

Do not invent facts.

USER QUESTION:
{question}

RETRIEVED NEWSPAPER SOURCES:
{context}

Give a clear and concise answer.
"""

    answer = generate_response(prompt)

    return answer, results