import pymupdf


def extract_text_from_pdf(pdf_path):

    doc = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(
        doc,
        start=1
    ):

        text = page.get_text()

        pages.append({
            "page": page_number,
            "text": text
        })

    doc.close()

    return pages


def clean_text(text):

    if not text:
        return ""

    text = text.replace(
        "\n",
        " "
    )

    text = " ".join(
        text.split()
    )

    return text


def create_chunks(
    pages,
    chunk_size=3000
):

    chunks = []

    for page in pages:

        page_number = page["page"]

        text = clean_text(
            page["text"]
        )

        if not text:
            continue

        for start in range(
            0,
            len(text),
            chunk_size
        ):

            chunk_text = text[
                start:start + chunk_size
            ]

            chunks.append({

                "text": chunk_text,

                "page": page_number,

                "chunk_id": len(chunks)

            })

    return chunks