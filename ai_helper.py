from __future__ import annotations

import os
import streamlit as st

from pdf_helper import search_pdfs, list_pdf_files


def render_sidebar_ai_helper(selected_term: str, selected_topic: str, selected_subtopic: str):
    st.sidebar.markdown("## AI Helper (From PDFs)")
    st.sidebar.caption("Search inside PDFs placed in the **pdfs/** folder.")

    # Graceful fallback if PyPDF2 missing
    try:
        import PyPDF2  # noqa
        pypdf2_ok = True
    except Exception:
        pypdf2_ok = False

    if not pypdf2_ok:
        st.sidebar.warning("PyPDF2 not installed. Run: `pip install PyPDF2`")
        return

    pdf_dir = "pdfs"
    if not os.path.isdir(pdf_dir):
        st.sidebar.info("Folder **pdfs/** not found yet. Create it and place PDFs inside.")
        return

    pdfs = list_pdf_files(pdf_dir)
    if pdfs:
        names = [os.path.basename(p) for p in pdfs]
        st.sidebar.markdown("**Detected PDFs:**")
        st.sidebar.write("• " + "\n• ".join(names))
    else:
        st.sidebar.warning("No PDFs found in **pdfs/** yet.")
        return

    q_key = "ai_pdf_query"
    if q_key not in st.session_state:
        st.session_state[q_key] = ""

    st.sidebar.text_input(
        "Ask a question (search PDFs)",
        key=q_key,
        placeholder="e.g., chain rule, composite function, du/dx, example…",
    )

    colA, colB = st.sidebar.columns([1, 1])
    with colA:
        do_search = st.button("Search PDFs", key="ai_pdf_search_btn")
    with colB:
        clear = st.button("Clear", key="ai_pdf_clear_btn")

    if clear:
        st.session_state[q_key] = ""
        st.sidebar.success("Cleared.")
        return

    if do_search:
        query = st.session_state[q_key].strip()
        if not query:
            st.sidebar.warning("Type a question first.")
            return

        with st.sidebar.spinner("Searching PDFs…"):
            hits = search_pdfs(pdf_dir, query, top_k=6)

        if not hits:
            st.sidebar.info("No strong matches found. Try different keywords.")
            return

        st.sidebar.markdown("### Top matches")
        for h in hits:
            st.sidebar.markdown(
                f"**{h.filename}** • page **{h.page_number}**  \n"
                f"<div style='font-size:12px; color:#51606f;'>{h.text}</div>",
                unsafe_allow_html=True,
            )
            st.sidebar.markdown("---")
