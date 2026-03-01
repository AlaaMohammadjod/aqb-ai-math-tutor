# ai_helper.py
from __future__ import annotations

import os
import re
import streamlit as st

from pdf_helper import list_pdf_files, search_pdfs, build_bm25_index, PdfHit


def _normalize(s: str) -> str:
    return (s or "").strip().lower()


def _scope_keywords(selected_topic: str, selected_subtopic: str) -> list[str]:
    s = _normalize(selected_subtopic)

    if "curve sketch" in s or "curve sketching" in s:
        return [
            "domain", "vertical asymptote", "horizontal asymptote",
            "first derivative", "second derivative",
            "critical values", "first derivative test",
            "inflection", "concavity", "second derivative test",
            "table of values", "sketch",
        ]
    if "concavity" in s or "second derivative" in s or "2nd derivative" in s:
        return ["concavity", "concave up", "concave down", "inflection", "second derivative", "f''"]
    if "increasing" in s or "decreasing" in s:
        return ["increasing", "decreasing", "first derivative", "f'", "critical values", "sign table"]
    if "maximum" in s or "minimum" in s:
        return ["maximum", "minimum", "critical values", "first derivative test", "second derivative test"]
    if "lhopital" in s or "hospital" in s or "indeterminate" in s:
        return ["indeterminate", "0/0", "infinity/infinity", "l'hospital", "differentiate numerator", "differentiate denominator"]

    return []


def _answer_builder(selected_topic: str, selected_subtopic: str) -> tuple[str, list[str]]:
    s = _normalize(selected_subtopic)

    if "curve sketch" in s or "curve sketching" in s:
        return (
            "Answer Builder (Curve Sketching)",
            [
                "Step 1 — Domain: identify where the function exists.",
                "Step 2 — Asymptotes (if rational): vertical + horizontal.",
                "Step 3 — Compute f′(x): critical values + first derivative test.",
                "Step 4 — Compute f″(x): concavity + inflection points.",
                "Step 5 — Overlap variation + concavity summaries (intervals).",
                "Step 6 — Small table of values (few anchor points).",
                "Step 7 — Final sketch based on all features.",
            ],
        )

    if "concavity" in s or "second derivative" in s:
        return (
            "Answer Builder (Concavity & Inflection)",
            [
                "Step 1 — Compute f″(x).",
                "Step 2 — Solve f″(x)=0 (candidates).",
                "Step 3 — Test sign of f″ on intervals (concave up/down).",
                "Step 4 — Confirm inflection when concavity changes.",
            ],
        )

    return (
        "Answer Builder (Using the PDF sources)",
        [
            "Step 1 — Use the citations: open the page(s) shown.",
            "Step 2 — Copy the rule/definition exactly from the PDF.",
            "Step 3 — Apply it step-by-step to the question.",
            "Step 4 — If stuck, ask a follow-up using the exact keyword from the PDF.",
        ],
    )


def _education_guardrails() -> list[str]:
    return [
        "This AI Helper is controlled: it does NOT invent new information.",
        "It only searches your course PDFs and shows citations (PDF + page).",
        "If no match appears, rewrite your question using textbook keywords.",
    ]


def _render_hit(hit: PdfHit, idx: int) -> None:
    st.sidebar.markdown(f"**{idx}. {hit.filename} — page {hit.page_number}**")
    st.sidebar.caption(hit.text)


def _suggested_questions(selected_subtopic: str) -> list[str]:
    s = _normalize(selected_subtopic)
    if "curve sketch" in s:
        return [
            "How do I find vertical and horizontal asymptotes?",
            "What are the exact steps for curve sketching?",
            "How do critical values help in curve sketching?",
            "How do I find inflection points and concavity?",
        ]
    return [
        "Where in the PDF is this topic explained?",
        "What is the definition of the key term in this subtopic?",
        "What are the steps to solve a typical question here?",
        "Show an example from the PDF (with page number).",
    ]


def render_sidebar_ai_helper(selected_term: str, selected_topic: str, selected_subtopic: str):
    st.sidebar.markdown("## 🤖 AI Helper")
    st.sidebar.caption("Smart Course Assistant (Free • PDF-Based • Controlled)")

    pdf_dir = "pdfs"
    if not os.path.isdir(pdf_dir):
        st.sidebar.error("Missing folder: **pdfs/**")
        st.sidebar.info("Create **pdfs/** in the repo and upload your Chapter PDFs.")
        return

    pdf_paths = list_pdf_files(pdf_dir)
    if not pdf_paths:
        st.sidebar.warning("No PDFs found in **pdfs/**")
        st.sidebar.info("Upload: Chapter 2.pdf, Chapter 3.pdf, Chapter 2&3 Answer key.pdf")
        return

    pdf_files = [os.path.basename(p) for p in pdf_paths]

    with st.sidebar.expander("✅ Detected course PDFs", expanded=False):
        for f in pdf_files:
            st.sidebar.write("• " + f)

    # -------------------------
    # PERFORMANCE: Warm up index
    # -------------------------
    # First run can be slow because PDFs are being read and indexed.
    # Do it here with a clear spinner so the FIRST user question isn’t painfully slow.
    if "pdf_index_ready" not in st.session_state:
        with st.sidebar.spinner("Preparing AI Helper (indexing PDFs — first time only)…"):
            build_bm25_index(pdf_dir)
        st.session_state.pdf_index_ready = True

    st.sidebar.markdown("---")

    with st.sidebar.expander("📌 Controlled AI rules", expanded=True):
        for g in _education_guardrails():
            st.sidebar.write("• " + g)

    st.sidebar.markdown("---")

    # Filters
    st.sidebar.markdown("### Sources to search")
    default_sources = [f for f in pdf_files if "answer" not in f.lower()] or pdf_files
    selected_sources = st.sidebar.multiselect(
        "Select PDFs",
        options=pdf_files,
        default=default_sources,
        help="Tip: include Answer Key if you want worked solutions/checking.",
        key="pdf_sources_select",
    )

    st.sidebar.markdown("---")

    # Chat history
    if "pdf_chat" not in st.session_state:
        st.session_state.pdf_chat = [
            {"role": "assistant", "text": "Hi! Ask your question. I will search the PDFs and show citations + an Answer Builder."}
        ]

    # Input value (NOT the widget key)
    if "pdf_input_value" not in st.session_state:
        st.session_state.pdf_input_value = ""

    # Suggested questions (buttons)
    st.sidebar.markdown("### Suggested questions")
    sq = _suggested_questions(selected_subtopic)
    c1, c2 = st.sidebar.columns(2)
    for i, q in enumerate(sq[:4]):
        btn = (c1 if i % 2 == 0 else c2).button(q, use_container_width=True, key=f"suggest_{selected_subtopic}_{i}")
        if btn:
            st.session_state.pdf_input_value = q
            st.sidebar.success("Inserted into the question box ↓")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### Chat")
    for msg in st.session_state.pdf_chat[-10:]:
        if msg["role"] == "user":
            st.sidebar.markdown(f"**You:** {msg['text']}")
        else:
            st.sidebar.markdown(f"**Tutor:** {msg['text']}")

    st.sidebar.markdown("---")

    # IMPORTANT: widget key is different from the stored value key
    q = st.sidebar.text_area(
        "Your question",
        value=st.session_state.pdf_input_value,
        height=90,
        placeholder="Type your question here…",
        key="pdf_assistant_input_widget",
    )

    col1, col2 = st.sidebar.columns(2)
    ask = col1.button("🔎 Search & Guide", use_container_width=True, key="pdf_ask_btn")
    clear = col2.button("🧹 Clear", use_container_width=True, key="pdf_clear_btn")

    if clear:
        st.session_state.pdf_chat = [
            {"role": "assistant", "text": "Hi! Ask your question. I will search the PDFs and show citations + an Answer Builder."}
        ]
        st.session_state.pdf_input_value = ""
        st.rerun()

    if not ask:
        return

    user_q = (q or "").strip()
    if not user_q:
        st.sidebar.warning("Type a question first.")
        return

    # Expand query with subtopic keywords (retrieval boost)
    extra = _scope_keywords(selected_topic, selected_subtopic)
    expanded_query = user_q + (" " + " ".join(extra[:10]) if extra else "")

    st.session_state.pdf_chat.append({"role": "user", "text": user_q})

    with st.sidebar.spinner("Searching your course PDFs…"):
        hits = search_pdfs(pdf_dir, expanded_query, top_k=6, allow_files=selected_sources)

    if hits:
        st.session_state.pdf_chat.append(
            {"role": "assistant", "text": "I found the best matches in your PDFs. Use the citations below and follow the Answer Builder steps."}
        )
    else:
        st.session_state.pdf_chat.append(
            {"role": "assistant", "text": "No strong match found. Rephrase using keywords like: asymptote, domain, first derivative test, concavity, inflection."}
        )

    st.sidebar.markdown("### 📚 Best matches (with citations)")
    if hits:
        for i, h in enumerate(hits, start=1):
            _render_hit(h, i)
    else:
        st.sidebar.info("No matching snippets found.")

    st.sidebar.markdown("---")
    title, steps = _answer_builder(selected_topic, selected_subtopic)
    st.sidebar.markdown(f"### ✅ {title}")
    for s in steps:
        st.sidebar.write("- " + s)

    # Clear input safely (NOT widget key)
    st.session_state.pdf_input_value = ""
    st.rerun()
