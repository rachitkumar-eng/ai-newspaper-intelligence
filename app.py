import os
import base64
import html
import fitz
import streamlit as st

from pdf_processor import (
    extract_text_from_pdf,
    create_chunks
)

from rag import create_embeddings

from qa import answer_question

from nlp_processor import analyze_text

from summarizer import summarize_newspaper

from final_editor import create_final_summary


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Newspaper Intelligence",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

PDF_PATH = (
    r"D:\newspaper_ai\data"
    r"\Free-Press-Journal-Mumbai-Epaper-20-08-2026.pdf"
)

BANNER_PATH = (
    r"D:\newspaper_ai\data"
    r"\newspaper_banner.jpg"
)

GENERATED_BANNER_PATH = (
    r"D:\newspaper_ai\data"
    r"\generated_newspaper_banner.jpg"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #f7f7f5 0%,
                #ffffff 45%,
                #f6f6f4 100%
            );
        color: #181818;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    div[data-testid="stAppViewContainer"] > section:first-child {
        padding-top: 0;
    }


    /* ======================================================
       DEFAULT TEXT
       ====================================================== */

    p {
        font-size: 16px;
        line-height: 1.7;
    }

    label {
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    .stCaption {
        font-size: 13px !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0c0c0c 0%,
                #141414 100%
            );

        border-right: 1px solid #292929;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] * {
        color: #f5f5f5;
    }

    section[data-testid="stSidebar"] p {
        font-size: 15px;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #f5f5f5;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #303030;
    }

    section[data-testid="stSidebar"] .stSuccess {
        background: #161616;
        border: 1px solid #343434;
        border-radius: 10px;
        color: #eeeeee;
    }

    section[data-testid="stSidebar"] .stSuccess p {
        font-size: 14px;
        font-weight: 700;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        min-height: 48px;
        border-radius: 10px;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.2px;
        border: 1px solid #222222;
        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 8px 20px rgba(0,0,0,0.12);
    }


    /* ======================================================
       TEXT INPUTS
       ====================================================== */

    div[data-baseweb="input"] {
        border-radius: 10px;
        border-color: #d6d6d6;
    }

    div[data-baseweb="input"] input {
        font-size: 16px !important;
        padding-top: 13px;
        padding-bottom: 13px;
    }

    textarea {
        font-size: 16px !important;
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 700 !important;
        padding-left: 18px;
        padding-right: 18px;
    }

    div[data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #dddddd;
        margin-bottom: 30px;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dedede;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetric"] label {
        font-size: 14px !important;
        color: #777777 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 800 !important;
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #dedede;
        border-radius: 12px;
        margin-bottom: 10px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] summary {
        font-size: 15px;
        font-weight: 700;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 11px;
    }

    div[data-testid="stAlert"] p {
        font-size: 15px;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: #e1e1e1;
    }


    /* ======================================================
       SCROLLBAR
       ====================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f4f4f4;
    }

    ::-webkit-scrollbar-thumb {
        background: #b5b5b5;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #777777;
    }


    /* ======================================================
       CUSTOM CARD HOVER
       ====================================================== */

    .premium-card {
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow:
            0 14px 30px rgba(0,0,0,0.08);
        border-color: #bdbdbd !important;
    }


    /* ======================================================
       RESPONSIVE
       ====================================================== */

    @media (max-width: 900px) {

        .main .block-container {
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BANNER GENERATOR
# ============================================================

def get_banner_image():

    if os.path.exists(BANNER_PATH):
        return BANNER_PATH

    if os.path.exists(PDF_PATH):

        try:

            doc = fitz.open(PDF_PATH)

            if len(doc) > 0:

                page = doc[0]

                matrix = fitz.Matrix(
                    1.5,
                    1.5
                )

                pix = page.get_pixmap(
                    matrix=matrix,
                    alpha=False
                )

                pix.save(
                    GENERATED_BANNER_PATH
                )

                doc.close()

                return GENERATED_BANNER_PATH

        except Exception:
            pass

    return None


banner_image = get_banner_image()


# ============================================================
# HERO SECTION
# ============================================================

if banner_image and os.path.exists(banner_image):

    try:

        with open(
            banner_image,
            "rb"
        ) as image_file:

            image_base64 = base64.b64encode(
                image_file.read()
            ).decode()

        hero_html = f"""

        <div style="
            position:relative;
            width:100%;
            height:400px;
            border-radius:24px;
            overflow:hidden;
            margin-bottom:42px;

            background:#111111;

            box-shadow:
                0 20px 45px rgba(0,0,0,0.16);
        ">

            <img
                src="data:image/jpeg;base64,{image_base64}"
                style="
                    width:100%;
                    height:100%;
                    object-fit:cover;
                    display:block;
                "
            >

            <div style="
                position:absolute;
                inset:0;

                background:
                    linear-gradient(
                        90deg,
                        rgba(0,0,0,0.94) 0%,
                        rgba(0,0,0,0.76) 38%,
                        rgba(0,0,0,0.32) 72%,
                        rgba(0,0,0,0.10) 100%
                    );
            "></div>


            <div style="
                position:absolute;
                left:52px;
                top:50%;
                transform:translateY(-50%);
                max-width:760px;
                color:white;
            ">

                <div style="
                    display:inline-block;
                    padding:7px 12px;

                    border:1px solid
                    rgba(255,255,255,0.28);

                    border-radius:20px;

                    background:
                    rgba(255,255,255,0.08);

                    font-size:12px;
                    font-weight:800;
                    letter-spacing:2px;

                    margin-bottom:17px;
                ">
                    GENAI &nbsp;·&nbsp; RAG &nbsp;·&nbsp; NLP
                </div>


                <div style="
                    font-family:
                        Georgia,
                        'Times New Roman',
                        serif;

                    font-size:48px;
                    font-weight:800;
                    line-height:1.08;

                    letter-spacing:-1px;

                    margin-bottom:16px;
                ">
                    AI Newspaper<br>
                    Intelligence
                </div>


                <div style="
                    font-size:18px;
                    line-height:1.65;

                    color:#e5e5e5;

                    max-width:700px;

                    margin-bottom:23px;
                ">
                    Transforming an entire newspaper into a
                    searchable intelligence system using
                    semantic retrieval, Generative AI and
                    Natural Language Processing.
                </div>


                <div style="
                    display:inline-flex;
                    align-items:center;
                    gap:8px;

                    padding:9px 15px;

                    border-radius:22px;

                    background:
                    rgba(255,255,255,0.10);

                    border:
                    1px solid
                    rgba(255,255,255,0.25);

                    font-size:13px;
                    font-weight:800;

                    letter-spacing:1px;
                ">

                    <span style="
                        width:8px;
                        height:8px;
                        border-radius:50%;
                        background:#ffffff;
                        display:inline-block;
                    "></span>

                    SYSTEM ONLINE

                </div>

            </div>

        </div>

        """

        st.html(hero_html)

    except Exception:

        st.markdown(
            """
            # 📰 AI Newspaper Intelligence

            **GenAI · RAG · NLP**

            ● SYSTEM ONLINE
            """
        )

else:

    st.html(
        """
        <div style="
            background:#111111;
            color:white;

            padding:55px;

            border-radius:24px;

            margin-bottom:42px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#aaaaaa;
            ">
                GENAI · RAG · NLP
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:48px;
                font-weight:800;
                margin-top:14px;
            ">
                AI Newspaper Intelligence
            </div>

            <div style="
                font-size:18px;
                line-height:1.6;
                color:#dddddd;
                margin-top:15px;
                max-width:750px;
            ">
                Transforming an entire newspaper into a
                searchable intelligence system using semantic
                retrieval, Generative AI and Natural Language
                Processing.
            </div>

        </div>
        """
    )


# ============================================================
# LOAD NEWSPAPER
# ============================================================

@st.cache_resource
def load_newspaper():

    pages = extract_text_from_pdf(
        PDF_PATH
    )

    chunks = create_chunks(
        pages,
        chunk_size=3000
    )

    embeddings = create_embeddings(
        chunks
    )

    full_text = ""

    for page in pages:

        full_text += (
            page["text"] + "\n"
        )

    return (
        pages,
        chunks,
        embeddings,
        full_text
    )


# ============================================================
# LOAD DATA
# ============================================================

with st.spinner(
    "Loading newspaper intelligence pipeline..."
):

    (
        pages,
        chunks,
        embeddings,
        full_text
    ) = load_newspaper()


# ============================================================
# NLP
# ============================================================

@st.cache_data
def load_entities(text):

    return analyze_text(
        text
    )


with st.spinner(
    "Running NLP analysis..."
):

    entities = load_entities(
        full_text
    )


# ============================================================
# ENTITY DATA
# ============================================================

people = entities.get(
    "People",
    []
)

organizations = entities.get(
    "Organizations",
    []
)

locations = entities.get(
    "Locations",
    []
)

money = entities.get(
    "Money",
    []
)

dates = entities.get(
    "Dates",
    []
)

percentages = entities.get(
    "Percentages",
    []
)


# ============================================================
# DAILY BRIEF
# ============================================================

@st.cache_data
def generate_daily_brief(pdf_path):

    summaries = summarize_newspaper(
        pdf_path,
        max_chunks=5
    )

    final_summary = create_final_summary(
        summaries
    )

    return final_summary


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div style="
            padding:
            5px 0 24px 0;
        ">

            <div style="
                font-family:Georgia,serif;
                font-size:27px;
                font-weight:800;
                letter-spacing:-0.5px;
            ">
                📰 Newspaper AI
            </div>

            <div style="
                color:#a7a7a7;
                font-size:15px;
                margin-top:6px;
                letter-spacing:0.3px;
            ">
                Intelligence Platform
            </div>

        </div>
        """
    )


    st.success(
        "● System Online"
    )


    st.divider()


    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-size:13px;
            font-weight:800;
            letter-spacing:1.5px;
            color:#999999;
            margin-bottom:12px;
        ">
            DATASET
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        f"📄 **{len(pages)}** Newspaper Pages"
    )

    st.write(
        f"🧩 **{len(chunks)}** Knowledge Chunks"
    )


    st.divider()


    # --------------------------------------------------------
    # AI STACK
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            font-size:13px;
            font-weight:800;
            letter-spacing:1.5px;
            color:#999999;
            margin-bottom:12px;
        ">
            AI STACK
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "✦ Gemini"
    )

    st.write(
        "✦ all-MiniLM-L6-v2"
    )

    st.write(
        "✦ spaCy NLP"
    )

    st.write(
        "✦ Streamlit"
    )


    st.divider()


    st.caption(
        "GENAI · RAG · NLP"
    )

    st.caption(
        "Portfolio Intelligence Platform"
    )


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.html(
    """
    <div style="
        margin-top:8px;
        margin-bottom:22px;
    ">

        <div style="
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            color:#777777;
        ">
            DATASET OVERVIEW
        </div>

        <div style="
            font-family:Georgia,serif;
            font-size:32px;
            font-weight:800;
            color:#171717;
            margin-top:6px;
            letter-spacing:-0.5px;
        ">
            Newspaper Knowledge Base
        </div>

        <div style="
            color:#666666;
            font-size:16px;
            line-height:1.6;
            margin-top:7px;
            margin-bottom:25px;
        ">
            A live overview of the newspaper processed by
            the AI intelligence pipeline.
        </div>

    </div>
    """
)


# ============================================================
# METRIC CARDS
# ============================================================

metric_html = f"""

<div style="
    display:grid;
    grid-template-columns:
        repeat(4,minmax(0,1fr));

    gap:18px;

    margin-bottom:46px;
">


    <!-- DOCUMENT -->

    <div class="premium-card" style="
        background:#ffffff;
        border:1px solid #dedede;
        border-radius:16px;
        padding:25px;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.035);
    ">

        <div style="
            font-size:30px;
            margin-bottom:14px;
        ">
            ◫
        </div>

        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:1.7px;
            color:#888888;
        ">
            DOCUMENT
        </div>

        <div style="
            font-size:34px;
            font-weight:850;
            color:#111111;
            margin-top:5px;
        ">
            {len(pages)}
        </div>

        <div style="
            color:#666666;
            font-size:15px;
            margin-top:2px;
        ">
            Newspaper Pages
        </div>

    </div>


    <!-- RAG -->

    <div class="premium-card" style="
        background:#ffffff;
        border:1px solid #dedede;
        border-radius:16px;
        padding:25px;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.035);
    ">

        <div style="
            font-size:30px;
            margin-bottom:14px;
        ">
            ◈
        </div>

        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:1.7px;
            color:#888888;
        ">
            RETRIEVAL
        </div>

        <div style="
            font-size:34px;
            font-weight:850;
            color:#111111;
            margin-top:5px;
        ">
            {len(chunks)}
        </div>

        <div style="
            color:#666666;
            font-size:15px;
            margin-top:2px;
        ">
            Knowledge Chunks
        </div>

    </div>


    <!-- PEOPLE -->

    <div class="premium-card" style="
        background:#ffffff;
        border:1px solid #dedede;
        border-radius:16px;
        padding:25px;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.035);
    ">

        <div style="
            font-size:30px;
            margin-bottom:14px;
        ">
            ◉
        </div>

        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:1.7px;
            color:#888888;
        ">
            NLP
        </div>

        <div style="
            font-size:34px;
            font-weight:850;
            color:#111111;
            margin-top:5px;
        ">
            {len(people):,}
        </div>

        <div style="
            color:#666666;
            font-size:15px;
            margin-top:2px;
        ">
            People Detected
        </div>

    </div>


    <!-- ORGANIZATIONS -->

    <div class="premium-card" style="
        background:#ffffff;
        border:1px solid #dedede;
        border-radius:16px;
        padding:25px;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.035);
    ">

        <div style="
            font-size:30px;
            margin-bottom:14px;
        ">
            □
        </div>

        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:1.7px;
            color:#888888;
        ">
            NLP
        </div>

        <div style="
            font-size:34px;
            font-weight:850;
            color:#111111;
            margin-top:5px;
        ">
            {len(organizations):,}
        </div>

        <div style="
            color:#666666;
            font-size:15px;
            margin-top:2px;
        ">
            Organizations
        </div>

    </div>

</div>

"""


st.html(metric_html)


# ============================================================
# PLATFORM CAPABILITIES
# ============================================================

st.html(
    """
    <div style="
        margin-bottom:22px;
    ">

        <div style="
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            color:#777777;
        ">
            PLATFORM CAPABILITIES
        </div>

        <div style="
            font-family:Georgia,serif;
            font-size:32px;
            font-weight:800;
            color:#171717;
            margin-top:6px;
        ">
            Intelligence Layer
        </div>

        <div style="
            color:#666666;
            font-size:16px;
            line-height:1.6;
            margin-top:7px;
            margin-bottom:25px;
        ">
            Three core capabilities built on the newspaper
            processing and intelligence pipeline.
        </div>

    </div>
    """
)


# ============================================================
# CAPABILITY CARDS
# ============================================================

capabilities_html = """

<div style="
    display:grid;
    grid-template-columns:
        repeat(3,minmax(0,1fr));

    gap:18px;

    margin-bottom:48px;
">


    <!-- ASK -->

    <div class="premium-card" style="
        background:#111111;
        color:white;

        border:1px solid #111111;

        border-radius:18px;

        padding:28px;

        min-height:220px;

        box-shadow:
            0 10px 25px rgba(0,0,0,0.10);
    ">

        <div style="
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            color:#999999;
        ">
            01
        </div>

        <div style="
            font-size:32px;
            margin-top:16px;
        ">
            ◉
        </div>

        <div style="
            font-family:Georgia,serif;
            font-size:21px;
            font-weight:800;
            margin-top:9px;
        ">
            Ask Newspaper AI
        </div>

        <div style="
            color:#cfcfcf;
            font-size:15px;
            line-height:1.65;
            margin-top:8px;
        ">
            Ask natural-language questions and retrieve
            relevant newspaper evidence before Gemini
            generates a grounded answer.
        </div>

    </div>


    <!-- BRIEF -->

    <div class="premium-card" style="
        background:#ffffff;
        color:#171717;

        border:1px solid #dedede;

        border-radius:18px;

        padding:28px;

        min-height:220px;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.04);
    ">

        <div style="
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            color:#999999;
        ">
            02
        </div>

        <div style="
            font-size:32px;
            margin-top:16px;
        ">
            ≡
        </div>

        <div style="
            font-family:Georgia,serif;
            font-size:21px;
            font-weight:800;
            margin-top:9px;
        ">
            Daily Brief
        </div>

        <div style="
            color:#666666;
            font-size:15px;
            line-height:1.65;
            margin-top:8px;
        ">
            Convert the processed newspaper into a concise
            editorial-style briefing using Generative AI.
        </div>

    </div>


    <!-- NLP -->

    <div class="premium-card" style="
        background:#ffffff;
        color:#171717;

        border:1px solid #dedede;

        border-radius:18px;

        padding:28px;

        min-height:220px;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.04);
    ">

        <div style="
            font-size:12px;
            font-weight:800;
            letter-spacing:2px;
            color:#999999;
        ">
            03
        </div>

        <div style="
            font-size:32px;
            margin-top:16px;
        ">
            ⌁
        </div>

        <div style="
            font-family:Georgia,serif;
            font-size:21px;
            font-weight:800;
            margin-top:9px;
        ">
            NLP Intelligence
        </div>

        <div style="
            color:#666666;
            font-size:15px;
            line-height:1.65;
            margin-top:8px;
        ">
            Explore people, organizations, locations,
            dates, monetary values and percentages
            extracted using spaCy.
        </div>

    </div>

</div>

"""


st.html(capabilities_html)


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "◉  Ask Newspaper AI",
        "≡  Daily Brief",
        "⌁  NLP Intelligence",
        "⌘  System Architecture"
    ]
)


# ============================================================
# TAB 1 — ASK NEWSPAPER AI
# ============================================================

with tab1:

    st.html(
        """
        <div style="
            margin-bottom:25px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                INTELLIGENCE WORKSPACE
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:32px;
                font-weight:800;
                margin-top:6px;
            ">
                Explore the Newspaper
            </div>

            <div style="
                color:#666666;
                font-size:16px;
                line-height:1.6;
                margin-top:7px;
            ">
                Ask questions and retrieve evidence-backed
                answers from the newspaper knowledge base.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # ASK CARD
    # --------------------------------------------------------

    st.html(
        """
        <div class="premium-card" style="
            background:#111111;
            color:white;

            border-radius:18px;

            padding:30px;

            margin-bottom:25px;

            box-shadow:
                0 12px 30px rgba(0,0,0,0.10);
        ">

            <div style="
                font-size:13px;
                font-weight:800;
                letter-spacing:2px;
                color:#999999;
            ">
                RETRIEVAL + GENERATION
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:25px;
                font-weight:800;
                margin-top:8px;
            ">
                Ask Newspaper AI
            </div>

            <div style="
                color:#cccccc;
                font-size:16px;
                line-height:1.65;
                margin-top:8px;
                max-width:900px;
            ">
                The RAG pipeline retrieves semantically relevant
                newspaper chunks before Gemini generates the
                final grounded response.
            </div>

        </div>
        """
    )


    question = st.text_input(
        "Your question",
        placeholder=(
            "Example: What happened with the BEST bus depots?"
        )
    )


    st.markdown(
        """
        <div style="
            font-size:15px;
            font-weight:800;
            margin-top:15px;
            margin-bottom:10px;
        ">
            Suggested questions
        </div>
        """,
        unsafe_allow_html=True
    )


    example_questions = [

        "What are today's most important stories?",

        "What happened in Maharashtra?",

        "What are the major business developments?",

        "What important court cases are discussed?",

        "What are the major international stories?"

    ]


    suggestion_html = """

    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:8px;
        margin-bottom:25px;
    ">
    """


    for q in example_questions:

        safe_question = html.escape(q)

        suggestion_html += f"""

        <div style="
            padding:8px 12px;

            border-radius:20px;

            background:#f2f2f0;

            border:1px solid #dedede;

            color:#444444;

            font-size:13px;
            font-weight:600;
        ">
            {safe_question}
        </div>

        """


    suggestion_html += "</div>"


    st.html(
        suggestion_html
    )


    ask_button = st.button(
        "Search & Ask Newspaper AI",
        type="primary",
        use_container_width=True
    )


    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching newspaper and generating answer..."
            ):

                answer, results = answer_question(
                    question,
                    chunks,
                    embeddings,
                    top_k=4,
                    similarity_threshold=0.35
                )


            st.markdown(
                """
                <div style="
                    font-family:Georgia,serif;
                    font-size:25px;
                    font-weight:800;
                    margin-top:35px;
                    margin-bottom:12px;
                ">
                    ◉ AI Answer
                </div>
                """,
                unsafe_allow_html=True
            )


            st.info(
                answer
            )


            st.markdown(
                """
                <div style="
                    font-family:Georgia,serif;
                    font-size:25px;
                    font-weight:800;
                    margin-top:30px;
                    margin-bottom:10px;
                ">
                    ◇ Retrieved Sources
                </div>
                """,
                unsafe_allow_html=True
            )


            if not results:

                st.warning(
                    "No sufficiently relevant newspaper "
                    "sources found."
                )

            else:

                st.caption(
                    f"{len(results)} relevant sources retrieved."
                )


                for i, result in enumerate(
                    results,
                    start=1
                ):

                    with st.expander(
                        f"Source {i}   ·   "
                        f"Page {result['page']}   ·   "
                        f"Similarity {result['score']:.3f}"
                    ):

                        st.write(
                            f"**Page:** {result['page']}"
                        )

                        st.write(
                            f"**Similarity:** "
                            f"{result['score']:.3f}"
                        )

                        st.write(
                            f"**Chunk ID:** "
                            f"{result['chunk_id']}"
                        )

                        st.divider()

                        st.write(
                            result["text"]
                        )


# ============================================================
# TAB 2 — DAILY BRIEF
# ============================================================

with tab2:

    st.html(
        """
        <div style="
            margin-bottom:25px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                GENERATIVE EDITORIAL INTELLIGENCE
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:32px;
                font-weight:800;
                margin-top:6px;
            ">
                Today's Newspaper Brief
            </div>

            <div style="
                color:#666666;
                font-size:16px;
                line-height:1.6;
                margin-top:7px;
            ">
                Turn the day's newspaper into a concise
                editorial intelligence brief.
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="premium-card" style="
            background:#ffffff;

            border:1px solid #dedede;

            border-radius:18px;

            padding:30px;

            margin-bottom:25px;

            box-shadow:
                0 5px 18px rgba(0,0,0,0.04);
        ">

            <div style="
                font-size:13px;
                font-weight:800;
                letter-spacing:2px;
                color:#888888;
            ">
                EDITORIAL ENGINE
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:25px;
                font-weight:800;
                margin-top:8px;
            ">
                ≡ Editorial Intelligence
            </div>

            <div style="
                color:#666666;
                font-size:16px;
                line-height:1.65;
                margin-top:8px;
            ">
                Gemini analyzes the newspaper content and
                produces a concise briefing focused on the
                most important stories and developments.
            </div>

        </div>
        """
    )


    generate_button = st.button(
        "Generate Daily Brief",
        type="primary",
        use_container_width=True
    )


    if generate_button:

        with st.spinner(
            "Generating today's newspaper brief..."
        ):

            daily_brief = generate_daily_brief(
                PDF_PATH
            )


        st.success(
            "Daily brief generated successfully."
        )


        st.markdown(
            daily_brief
        )

    else:

        st.info(
            "Generate the brief to analyze the newspaper."
        )


# ============================================================
# TAB 3 — NLP INTELLIGENCE
# ============================================================

with tab3:

    st.html(
        """
        <div style="
            margin-bottom:25px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                NATURAL LANGUAGE PROCESSING
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:32px;
                font-weight:800;
                margin-top:6px;
            ">
                Newspaper NLP Intelligence
            </div>

            <div style="
                color:#666666;
                font-size:16px;
                line-height:1.6;
                margin-top:7px;
            ">
                Named entities automatically extracted from
                the newspaper using spaCy.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # NLP METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "People",
            f"{len(people):,}"
        )


    with col2:

        st.metric(
            "Organizations",
            f"{len(organizations):,}"
        )


    with col3:

        st.metric(
            "Locations",
            f"{len(locations):,}"
        )


    col4, col5, col6 = st.columns(3)


    with col4:

        st.metric(
            "Monetary Values",
            f"{len(money):,}"
        )


    with col5:

        st.metric(
            "Dates",
            f"{len(dates):,}"
        )


    with col6:

        st.metric(
            "Percentages",
            f"{len(percentages):,}"
        )


    st.divider()


    # --------------------------------------------------------
    # ENTITY EXPLORER
    # --------------------------------------------------------

    st.html(
        """
        <div style="
            margin-top:25px;
            margin-bottom:20px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                ENTITY EXPLORER
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:27px;
                font-weight:800;
                margin-top:6px;
            ">
                Explore Newspaper Entities
            </div>

            <div style="
                color:#666666;
                font-size:16px;
                margin-top:6px;
            ">
                Search and inspect entities extracted from
                the newspaper corpus.
            </div>

        </div>
        """
    )


    entity_type = st.selectbox(
        "Select entity type",
        [
            "People",
            "Organizations",
            "Locations",
            "Money",
            "Dates",
            "Percentages"
        ]
    )


    selected_entities = entities.get(
        entity_type,
        []
    )


    search_entity = st.text_input(
        "Search entities",
        placeholder=(
            "Search for a person, organization, "
            "location, etc."
        )
    )


    # --------------------------------------------------------
    # CLEAN ENTITY DISPLAY
    #
    # IMPORTANT:
    # We do NOT modify the NLP results.
    # We only clean whitespace for UI rendering.
    # --------------------------------------------------------

    cleaned_entities = []

    for entity in selected_entities:

        entity_text = str(entity).strip()

        entity_text = " ".join(
            entity_text.split()
        )

        if entity_text:

            cleaned_entities.append(
                entity_text
            )


    # --------------------------------------------------------
    # SEARCH FILTER
    # --------------------------------------------------------

    if search_entity.strip():

        search_term = search_entity.strip().lower()

        filtered_entities = [

            entity

            for entity in cleaned_entities

            if search_term in entity.lower()

        ]

    else:

        filtered_entities = cleaned_entities


    # --------------------------------------------------------
    # RESULT COUNT
    # --------------------------------------------------------

    safe_entity_type = html.escape(
        entity_type.lower()
    )

    count_html = f"""
    <div style="
        background:#f3f3f1;
        border:1px solid #dedede;
        border-radius:10px;

        padding:12px 15px;

        margin-top:15px;
        margin-bottom:18px;

        font-size:15px;
        font-weight:700;

        color:#333333;
    ">
        {len(filtered_entities):,}
        matching {safe_entity_type}
    </div>
    """

    st.html(
        count_html
    )


    # --------------------------------------------------------
    # ENTITY CARDS
    # --------------------------------------------------------

    if filtered_entities:

        display_entities = filtered_entities[:100]


        entity_grid_html = """
        <div style="
            display:grid;

            grid-template-columns:
                repeat(3, minmax(0, 1fr));

            gap:10px;

            width:100%;

            margin-top:4px;
            margin-bottom:10px;
        ">
        """


        for entity in display_entities:

            # Escape entity text so NLP output
            # can never break the HTML structure.

            safe_entity = html.escape(
                entity,
                quote=True
            )


            entity_grid_html += f"""
            <div style="
                box-sizing:border-box;

                width:100%;

                min-height:42px;

                display:flex;

                align-items:center;

                padding:10px 13px;

                background:#ffffff;

                border:1px solid #e4e4e4;

                border-radius:9px;

                font-family:
                    -apple-system,
                    BlinkMacSystemFont,
                    'Segoe UI',
                    sans-serif;

                font-size:14px;

                font-weight:500;

                line-height:1.35;

                color:#333333;

                overflow-wrap:anywhere;

                word-break:break-word;

                transition:
                    transform 0.15s ease,
                    box-shadow 0.15s ease,
                    border-color 0.15s ease;
            ">
                {safe_entity}
            </div>
            """


        entity_grid_html += """
        </div>
        """


        st.html(
            entity_grid_html
        )


        if len(filtered_entities) > 100:

            st.caption(
                f"Showing first 100 of "
                f"{len(filtered_entities):,} matching entities."
            )

    else:

        st.warning(
            "No entities found."
        )


# ============================================================
# TAB 4 — SYSTEM ARCHITECTURE
# ============================================================

with tab4:

    st.html(
        """
        <div style="
            margin-bottom:30px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                ENGINEERING DESIGN
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:32px;
                font-weight:800;
                margin-top:6px;
            ">
                System Architecture
            </div>

            <div style="
                color:#666666;
                font-size:16px;
                line-height:1.6;
                margin-top:7px;
            ">
                End-to-end architecture powering the AI
                Newspaper Intelligence platform.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # ARCHITECTURE PIPELINE
    # --------------------------------------------------------

    architecture = [

        (
            "01",
            "▣",
            "PDF Newspaper",
            "Document ingestion",
            "Input newspaper PDF."
        ),

        (
            "02",
            "Aa",
            "PyMuPDF",
            "Text extraction",
            "Extract text page-by-page."
        ),

        (
            "03",
            "≋",
            "Text Processing",
            "Preprocessing",
            "Clean and split text into knowledge chunks."
        ),

        (
            "04",
            "◇",
            "Sentence Transformers",
            "Embedding",
            "Generate semantic vector embeddings."
        ),

        (
            "05",
            "⌕",
            "Semantic Retrieval",
            "RAG",
            "Retrieve relevant chunks using similarity."
        ),

        (
            "06",
            "✦",
            "Gemini",
            "Generation",
            "Generate grounded answers from retrieved context."
        ),

        (
            "07",
            "⊞",
            "Source Attribution",
            "Evidence",
            "Return page numbers, scores and source evidence."
        ),

        (
            "08",
            "⌁",
            "spaCy NLP",
            "Entity extraction",
            "Extract people, organizations and other entities."
        )

    ]


    for (
        step,
        icon,
        title,
        category,
        description
    ) in architecture:

        st.html(
            f"""
            <div class="premium-card" style="
                display:grid;

                grid-template-columns:
                    75px 80px 1fr;

                align-items:center;

                background:#ffffff;

                border:
                    1px solid #dedede;

                border-radius:16px;

                padding:21px 25px;

                margin-bottom:12px;

                box-shadow:
                    0 3px 12px
                    rgba(0,0,0,0.035);
            ">


                <div style="
                    font-size:12px;
                    font-weight:800;
                    letter-spacing:1px;
                    color:#999999;
                ">
                    STEP<br>{step}
                </div>


                <div style="
                    width:52px;
                    height:52px;

                    display:flex;
                    align-items:center;
                    justify-content:center;

                    border-radius:14px;

                    background:#111111;

                    color:#ffffff;

                    font-size:22px;
                    font-weight:700;
                ">
                    {icon}
                </div>


                <div>

                    <div style="
                        font-size:11px;
                        font-weight:800;
                        letter-spacing:1.7px;
                        color:#999999;
                    ">
                        {category.upper()}
                    </div>

                    <div style="
                        font-family:Georgia,serif;
                        font-size:21px;
                        font-weight:800;
                        color:#171717;
                        margin-top:3px;
                    ">
                        {title}
                    </div>

                    <div style="
                        color:#666666;
                        font-size:15px;
                        line-height:1.5;
                        margin-top:3px;
                    ">
                        {description}
                    </div>

                </div>

            </div>
            """
        )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TECHNOLOGY STACK
    # --------------------------------------------------------

    st.html(
        """
        <div style="
            margin-bottom:22px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                TECHNOLOGY STACK
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:30px;
                font-weight:800;
                margin-top:6px;
            ">
                Engineering Components
            </div>

        </div>
        """
    )


    col1, col2 = st.columns(2)


    with col1:

        st.html(
            """
            <div class="premium-card" style="
                background:#111111;
                color:white;

                border-radius:16px;

                padding:27px;

                margin-bottom:18px;
            ">

                <div style="
                    font-size:11px;
                    font-weight:800;
                    letter-spacing:2px;
                    color:#999999;
                ">
                    01 · GENERATION
                </div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:23px;
                    font-weight:800;
                    margin-top:7px;
                ">
                    GenAI
                </div>

                <div style="
                    margin-top:15px;
                    color:#cccccc;
                    font-size:15px;
                    line-height:1.9;
                ">
                    ✦ Gemini<br>
                    ✦ Prompt Engineering<br>
                    ✦ Grounded Generation
                </div>

            </div>
            """
        )


        st.html(
            """
            <div class="premium-card" style="
                background:#ffffff;

                border:1px solid #dedede;

                border-radius:16px;

                padding:27px;

                margin-bottom:18px;
            ">

                <div style="
                    font-size:11px;
                    font-weight:800;
                    letter-spacing:2px;
                    color:#999999;
                ">
                    02 · RETRIEVAL
                </div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:23px;
                    font-weight:800;
                    margin-top:7px;
                ">
                    RAG
                </div>

                <div style="
                    margin-top:15px;
                    color:#555555;
                    font-size:15px;
                    line-height:1.9;
                ">
                    ◇ Sentence Transformers<br>
                    ◇ Vector Embeddings<br>
                    ◇ Cosine Similarity<br>
                    ◇ Top-K Retrieval
                </div>

            </div>
            """
        )


    with col2:

        st.html(
            """
            <div class="premium-card" style="
                background:#ffffff;

                border:1px solid #dedede;

                border-radius:16px;

                padding:27px;

                margin-bottom:18px;
            ">

                <div style="
                    font-size:11px;
                    font-weight:800;
                    letter-spacing:2px;
                    color:#999999;
                ">
                    03 · LANGUAGE
                </div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:23px;
                    font-weight:800;
                    margin-top:7px;
                ">
                    NLP
                </div>

                <div style="
                    margin-top:15px;
                    color:#555555;
                    font-size:15px;
                    line-height:1.9;
                ">
                    ⌁ spaCy<br>
                    ⌁ Named Entity Recognition<br>
                    ⌁ Text Processing
                </div>

            </div>
            """
        )


        st.html(
            """
            <div class="premium-card" style="
                background:#ffffff;

                border:1px solid #dedede;

                border-radius:16px;

                padding:27px;

                margin-bottom:18px;
            ">

                <div style="
                    font-size:11px;
                    font-weight:800;
                    letter-spacing:2px;
                    color:#999999;
                ">
                    04 · APPLICATION
                </div>

                <div style="
                    font-family:Georgia,serif;
                    font-size:23px;
                    font-weight:800;
                    margin-top:7px;
                ">
                    Application
                </div>

                <div style="
                    margin-top:15px;
                    color:#555555;
                    font-size:15px;
                    line-height:1.9;
                ">
                    ◉ Python<br>
                    ◉ Streamlit<br>
                    ◉ Cached Processing<br>
                    ◉ Interactive Dashboard
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # CURRENT DATASET
    # --------------------------------------------------------

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    st.html(
        """
        <div style="
            margin-bottom:22px;
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                letter-spacing:2px;
                color:#777777;
            ">
                DATASET TELEMETRY
            </div>

            <div style="
                font-family:Georgia,serif;
                font-size:30px;
                font-weight:800;
                margin-top:6px;
            ">
                Current Dataset
            </div>

        </div>
        """
    )


    total_entities = sum(
        [
            len(people),
            len(organizations),
            len(locations),
            len(money),
            len(dates),
            len(percentages)
        ]
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "PDF Pages",
            len(pages)
        )


    with col2:

        st.metric(
            "Knowledge Chunks",
            len(chunks)
        )


    with col3:

        st.metric(
            "NLP Entity Detections",
            f"{total_entities:,}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<br><br>",
    unsafe_allow_html=True
)


st.html(
    """
    <div style="
        border-top:1px solid #dddddd;

        padding-top:28px;
        padding-bottom:20px;

        text-align:center;
    ">

        <div style="
            font-family:Georgia,serif;
            font-size:16px;
            font-weight:800;
            color:#222222;
        ">
            AI Newspaper Intelligence
        </div>

        <div style="
            margin-top:8px;
            color:#777777;
            font-size:12px;
            letter-spacing:1.5px;
            font-weight:700;
        ">
            GENAI · RAG · NLP
            &nbsp;&nbsp;·&nbsp;&nbsp;
            PYTHON · STREAMLIT
        </div>

        <div style="
            margin-top:11px;
            color:#999999;
            font-size:13px;
        ">
            Intelligent document analysis & retrieval platform
        </div>

    </div>
    """
)