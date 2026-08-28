from pdf_processor import (
    extract_text_from_pdf,
    create_chunks
)

from llm import generate_response
from prompts import chunk_summary_prompt


def summarize_newspaper(
    pdf_path,
    max_chunks=5
):

    print("Reading newspaper...")

    pages = extract_text_from_pdf(
        pdf_path
    )

    print("Creating chunks...")

    chunks = create_chunks(
        pages,
        chunk_size=6000
    )

    # -------------------------------------------------
    # LIMIT NUMBER OF CHUNKS
    # -------------------------------------------------

    chunks = chunks[:max_chunks]

    print(
        "Total chunks to process:",
        len(chunks)
    )

    summaries = []

    for i, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"Processing chunk "
            f"{i}/{len(chunks)}..."
        )

        text = chunk["text"]

        prompt = chunk_summary_prompt(
            text
        )

        summary = generate_response(
            prompt
        )

        summaries.append({

            "page": chunk["page"],

            "summary": summary

        })

    return summaries