import streamlit as st
from ppt_generator import generate_ppt
from pdf_processor import extract_text_from_pdf
from embedder import chunk_text, create_embeddings
from vector_store import VectorStore
from analyzer import (
    summarize_paper,
    extract_contributions,
    extract_methodology,
    ask_question,
    find_similar_papers,
    detect_research_gaps,
)
from citation_graph import extract_citations, build_graph, plot_graph


# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsightPaper Pro",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL STYLES ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

    /* ── Reset & Base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: #E8EAF0;
    }

    .stApp {
        background: #080B14;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(56, 100, 255, 0.18) 0%, transparent 70%),
            radial-gradient(ellipse 40% 30% at 90% 80%, rgba(0, 200, 160, 0.08) 0%, transparent 60%);
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2.5rem 3rem 4rem 3rem; max-width: 1300px; }

    /* ── Hero ── */
    .hero-wrap {
        display: flex;
        align-items: flex-end;
        gap: 1rem;
        margin-bottom: 0.25rem;
        padding-top: 0.5rem;
    }
    .hero-icon {
        font-size: 2.2rem;
        line-height: 1;
        color: #3E7FFF;
        filter: drop-shadow(0 0 12px rgba(62,127,255,0.7));
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        letter-spacing: -0.03em;
        color: #FFFFFF;
        line-height: 1;
        margin: 0;
    }
    .hero-title span { color: #3E7FFF; }
    .hero-sub {
        font-size: 1rem;
        font-weight: 300;
        color: #7B84A3;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
    }
    .hero-divider {
        height: 1px;
        background: linear-gradient(90deg, #3E7FFF 0%, rgba(62,127,255,0) 60%);
        margin-bottom: 2.2rem;
        border: none;
    }

    /* ── Upload zone ── */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.025);
        border: 1.5px dashed rgba(62,127,255,0.35);
        border-radius: 14px;
        padding: 1rem 1.5rem;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(62,127,255,0.7);
    }
    [data-testid="stFileUploader"] label {
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        color: #C5CADF !important;
        font-size: 0.95rem !important;
    }
    .uploadedFileName { color: #7BFFD4 !important; font-weight: 500 !important; }

    /* ── Success / info / spinner ── */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        border: 1px solid rgba(62,127,255,0.25) !important;
        background: rgba(62,127,255,0.08) !important;
        color: #A8C4FF !important;
        font-weight: 500;
    }
    .stSpinner > div { border-top-color: #3E7FFF !important; }

    /* ── Analysis Buttons ── */
    .stButton > button {
        width: 100%;
        background: rgba(255,255,255,0.04) !important;
        border: 1.5px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #C8CFEA !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.65rem 0.5rem !important;
        transition: all 0.18s ease !important;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        background: rgba(62,127,255,0.15) !important;
        border-color: rgba(62,127,255,0.55) !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(62,127,255,0.2) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Section card ── */
    .result-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.6rem 2rem;
        margin-top: 1.5rem;
        backdrop-filter: blur(4px);
    }
    .result-card-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #3E7FFF;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .result-card-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(62,127,255,0.2);
        margin-left: 0.5rem;
    }

    /* ── Section headers (native st.subheader) ── */
    h2, h3 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.01em !important;
    }

    /* ── Body text ── */
    p, li, .stMarkdown p {
        color: #C4CAE0 !important;
        line-height: 1.75 !important;
        font-size: 0.95rem !important;
    }

    /* ── Text inputs ── */
    .stTextInput > label {
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
        color: #7B84A3 !important;
    }
    .stTextInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1.5px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #E8EAF0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1rem !important;
        transition: border-color 0.18s;
    }
    .stTextInput input:focus {
        border-color: rgba(62,127,255,0.6) !important;
        box-shadow: 0 0 0 3px rgba(62,127,255,0.12) !important;
    }
    .stTextInput input::placeholder { color: #4A5270 !important; }

    /* ── Divider ── */
    hr {
        border: none !important;
        height: 1px !important;
        background: rgba(255,255,255,0.07) !important;
        margin: 2.5rem 0 !important;
    }

    /* ── Similar results ── */
    .similar-card {
        background: rgba(62,127,255,0.05);
        border: 1px solid rgba(62,127,255,0.15);
        border-left: 3px solid #3E7FFF;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        color: #C4CAE0;
        font-size: 0.9rem;
        line-height: 1.65;
    }
    .similar-num {
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #3E7FFF;
        margin-bottom: 0.3rem;
    }

    /* ── Stat badge ── */
    .badge {
        display: inline-block;
        background: rgba(0,200,160,0.12);
        border: 1px solid rgba(0,200,160,0.3);
        color: #00C8A0;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.3rem 0.75rem;
        border-radius: 100px;
    }

    /* ── Columns gap ── */
    [data-testid="column"] { padding: 0 0.3rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── HERO HEADER ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-icon">✦</div>
        <div class="hero-title">Insight<span>Paper</span> Pro</div>
    </div>
    <div class="hero-sub">AI-powered research paper analyzer — summarize, interrogate, and map knowledge.</div>
    <hr class="hero-divider">
    """,
    unsafe_allow_html=True,
)

# ── FILE UPLOAD ───────────────────────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Drop your research papers here (PDF)",
    type="pdf",
    accept_multiple_files=True,
)

if uploaded_files:

    with st.spinner("Indexing papers…"):

        all_chunks = []
        all_embeddings = []
        combined_text = ""

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            combined_text += text
            chunks = chunk_text(text)
            embeddings = create_embeddings(chunks)
            all_chunks.extend(chunks)
            all_embeddings.extend(embeddings)

        store = VectorStore()
        store.build_index(all_embeddings, all_chunks)

    st.markdown(
        f'<span class="badge">✓ &nbsp;{len(uploaded_files)} paper{"s" if len(uploaded_files) > 1 else ""} indexed</span>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top:1.8rem'></div>", unsafe_allow_html=True)

    # ── ANALYSIS BUTTONS ──────────────────────────────────────────────────────
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        run_summary = st.button("📑  Summary")

    with col2:
        run_contrib = st.button("⭐  Contributions")

    with col3:
        run_method = st.button("⚙  Methodology")

    with col4:
        run_citation = st.button("🕸  Citation Map")

    with col5:
        run_gap = st.button("🔬  Research Gaps")

    with col6:
        run_ppt = st.button("📊  Generate PPT")

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    if run_summary:
        with st.spinner("Generating summary…"):
            summary = summarize_paper(combined_text)
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-card-title">📑 &nbsp;Paper Summary</div>
                <p>{summary}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── CONTRIBUTIONS ─────────────────────────────────────────────────────────
    if run_contrib:
        with st.spinner("Extracting contributions…"):
            contrib = extract_contributions(combined_text)
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-card-title">⭐ &nbsp;Key Contributions</div>
                <p>{contrib}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── METHODOLOGY ───────────────────────────────────────────────────────────
    if run_method:
        with st.spinner("Analyzing methodology…"):
            method = extract_methodology(combined_text)
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-card-title">⚙ &nbsp;Methodology</div>
                <p>{method}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── CITATION GRAPH ────────────────────────────────────────────────────────
    if run_citation:
        with st.spinner("Building citation graph…"):
            citations = extract_citations(combined_text)
            G = build_graph(citations)
            fig = plot_graph(G)

        # Dark-theme tweaks for the Plotly figure
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#C4CAE0",
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── RESEARCH GAPS ─────────────────────────────────────────────────────────
    if run_gap:
        with st.spinner("Detecting research gaps…"):
            gaps = detect_research_gaps(store)
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-card-title">🔬 &nbsp;Research Gap Analysis</div>
                <p>{gaps}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # ── PPT GENERATOR ─────────────────────────────────────────────────────────
if run_ppt:

    with st.spinner("Generating presentation slides…"):

        ppt_file = generate_ppt(combined_text)

    with open(ppt_file, "rb") as f:

        st.download_button(
            label="⬇ Download Presentation",
            data=f,
            file_name="research_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    # ── CHAT ──────────────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='font-family:"Syne",sans-serif;font-weight:700;font-size:1.15rem;
                     color:#FFFFFF;margin-bottom:0.8rem;letter-spacing:-0.01em;'>
            💬 &nbsp;Chat with your Papers
        </div>
        """,
        unsafe_allow_html=True,
    )

    q_input = st.text_input(
        "YOUR QUESTION",
        placeholder="e.g. What algorithm does this paper propose?",
    )

    if q_input:
        with st.spinner("Thinking…"):
            answer = ask_question(q_input, store, all_chunks)
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-card-title">Answer</div>
                <p>{answer}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── SIMILAR PAPERS ────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='font-family:"Syne",sans-serif;font-weight:700;font-size:1.15rem;
                     color:#FFFFFF;margin-bottom:0.8rem;letter-spacing:-0.01em;'>
            🔍 &nbsp;Find Similar Research
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "RESEARCH TOPIC",
        placeholder="e.g. edge computing scheduling",
    )

    if st.button("Search"):
        results = find_similar_papers(query, store)
        for i, r in enumerate(results, 1):
            st.markdown(
                f"""
                <div class="similar-card">
                    <div class="similar-num">Result {i}</div>
                    {r[:300]}…
                </div>
                """,
                unsafe_allow_html=True,
            )

else:
    st.markdown(
        """
        <div style="
            margin-top: 2rem;
            padding: 3rem 2rem;
            border: 1.5px dashed rgba(255,255,255,0.08);
            border-radius: 16px;
            text-align: center;
            color: #4A5270;
        ">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;filter:grayscale(0.4);">📄</div>
            <div style="font-family:'Syne',sans-serif;font-weight:600;font-size:1rem;
                         color:#5A6380;letter-spacing:0.02em;">
                Upload research papers above to get started
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )