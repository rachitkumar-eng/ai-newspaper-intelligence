import spacy


# ============================================================
# LOAD SPACY MODEL
# ============================================================

nlp = spacy.load("en_core_web_sm")


# ============================================================
# DISABLE UNNECESSARY COMPONENTS
# We only need NER for this project.
# ============================================================

for component in ["parser", "tagger", "lemmatizer"]:

    if component in nlp.pipe_names:

        nlp.disable_pipe(component)


# ============================================================
# EXTRACT ENTITIES FROM LARGE NEWSPAPER
# ============================================================

def extract_entities(text, chunk_size=5000):

    if not text:

        return {
            "People": [],
            "Organizations": [],
            "Locations": [],
            "Money": [],
            "Dates": [],
            "Percentages": []
        }


    # --------------------------------------------------------
    # Split newspaper into small pieces
    # --------------------------------------------------------

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunk = text[
            i:i + chunk_size
        ]

        if chunk.strip():

            chunks.append(chunk)


    print(
        f"Processing NLP in "
        f"{len(chunks)} smaller chunks..."
    )


    # --------------------------------------------------------
    # Storage
    # --------------------------------------------------------

    people = []

    organizations = []

    locations = []

    money = []

    dates = []

    percentages = []


    # --------------------------------------------------------
    # Process small batches
    # --------------------------------------------------------

    for doc in nlp.pipe(
        chunks,
        batch_size=4
    ):

        for ent in doc.ents:

            entity = ent.text.strip()

            if not entity:

                continue


            # ------------------------------------------------
            # PERSON
            # ------------------------------------------------

            if ent.label_ == "PERSON":

                people.append(entity)


            # ------------------------------------------------
            # ORGANIZATION
            # ------------------------------------------------

            elif ent.label_ == "ORG":

                organizations.append(entity)


            # ------------------------------------------------
            # LOCATION
            # ------------------------------------------------

            elif ent.label_ in [
                "GPE",
                "LOC",
                "FAC"
            ]:

                locations.append(entity)


            # ------------------------------------------------
            # MONEY
            # ------------------------------------------------

            elif ent.label_ == "MONEY":

                money.append(entity)


            # ------------------------------------------------
            # DATE
            # ------------------------------------------------

            elif ent.label_ == "DATE":

                dates.append(entity)


            # ------------------------------------------------
            # PERCENTAGE
            # ------------------------------------------------

            elif ent.label_ == "PERCENT":

                percentages.append(entity)


    # ========================================================
    # RETURN THE EXACT FORMAT EXPECTED BY app.py
    # ========================================================

    return {

        "People": people,

        "Organizations": organizations,

        "Locations": locations,

        "Money": money,

        "Dates": dates,

        "Percentages": percentages

    }


# ============================================================
# ANALYZE NEWSPAPER
# ============================================================

def analyze_text(text):

    print(
        "Starting newspaper NLP analysis..."
    )

    entities = extract_entities(
        text,
        chunk_size=5000
    )

    print(
        "NLP analysis completed."
    )

    print(
        f"People: {len(entities['People'])}"
    )

    print(
        f"Organizations: {len(entities['Organizations'])}"
    )

    print(
        f"Locations: {len(entities['Locations'])}"
    )

    print(
        f"Money: {len(entities['Money'])}"
    )

    print(
        f"Dates: {len(entities['Dates'])}"
    )

    print(
        f"Percentages: {len(entities['Percentages'])}"
    )

    return entities