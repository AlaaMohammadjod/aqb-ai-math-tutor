from __future__ import annotations

import os
from dataclasses import dataclass
import streamlit as st


@dataclass
class PdfSnippet:
    filename: str
    page_number: int  # 1-based
    score: float
    text: str


def _safe_import_pypdf2():
    try:
        import PyPDF2  # noqa
        return True, None
    except Exception as e:
        return False, str(e)


def list_pdf_files(pdf_dir: str) -> list[str]:
    if not os.path.isdir(pdf_dir):
        return []

    files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]

    # Prioritize your two main PDFs if present
    priority = [
        "chapter 2.pdf",
        "chapter 2 answer key.pdf",
    ]

    def rank(path: str):
        name = os.path.basename(path).lower().strip()
        if name in priority:
            return (0, priority.index(name))
        return (1, name)

    return sorted(files, key=rank)


@st.cache_data(show_spinner=False)
def extract_pdf_pages(pdf_path: str) -> list[str]:
    ok, _ = _safe_import_pypdf2()
    if not ok:
        return []
    from PyPDF2 import PdfReader

    reader = PdfReader(pdf_path)
    pages = []
    for p in reader.pages:
        txt = p.extract_text() or ""
        pages.append(txt)
    return pages


def _simple_score(query: str, text: str) -> float:
    q = query.lower().strip()
    if not q:
        return 0.0
    t = (text or "").lower()

    tokens = [w for w in q.replace(",", " ").replace(".", " ").split() if len(w) >= 2]
    if not tokens:
        return 0.0

    score = 0.0
    for w in tokens:
        c = t.count(w)
        score += min(12, c) * 1.0
        if c > 0:
            score += 1.5
    if q in t:
        score += 8.0
    return score


def search_pdfs(pdf_dir: str, query: str, top_k: int = 6) -> list[PdfSnippet]:
    ok, _ = _safe_import_pypdf2()
    if not ok:
        return []

    pdfs = list_pdf_files(pdf_dir)
    results: list[PdfSnippet] = []

    for pdf_path in pdfs:
        pages = extract_pdf_pages(pdf_path)
        for idx, page_txt in enumerate(pages):
            s = _simple_score(query, page_txt)
            if s <= 0:
                continue

            snippet = (page_txt or "").strip().replace("\n", " ")
            snippet = " ".join(snippet.split())
            if len(snippet) > 420:
                snippet = snippet[:420] + "…"

            results.append(
                PdfSnippet(
                    filename=os.path.basename(pdf_path),
                    page_number=idx + 1,
                    score=s,
                    text=snippet,
                )
            )

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_k]
