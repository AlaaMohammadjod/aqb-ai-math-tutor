# pdf_helper.py
from __future__ import annotations

import os
import re
import math
from dataclasses import dataclass
from typing import Dict, List

import streamlit as st


@dataclass
class PdfHit:
    filename: str
    page_number: int  # 1-based
    score: float
    text: str


_WORD = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")


def _tokenize(s: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD.finditer(s or "")]


def list_pdf_files(pdf_dir: str) -> list[str]:
    """
    Lists PDFs in pdfs/ and sorts them in a meaningful order:
    Chapter 2, Chapter 3, then Answer Key.
    """
    if not os.path.isdir(pdf_dir):
        return []

    files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]

    # Match your exact filenames (case-insensitive)
    priority = [
        "chapter 2.pdf",
        "chapter 3.pdf",
        "chapter 2&3 answer key.pdf",
    ]

    def rank(p: str):
        name = os.path.basename(p).lower().strip()
        if name in priority:
            return (0, priority.index(name))
        # fallback: answer key last
        is_key = 1 if ("answer" in name and "key" in name) else 0
        return (1, is_key, name)

    return sorted(files, key=rank)


@st.cache_data(show_spinner=False)
def extract_pdf_pages(pdf_path: str) -> list[str]:
    """
    Extract per-page text using PyPDF2.
    Streamlit Cloud-friendly (no system deps).
    """
    try:
        from PyPDF2 import PdfReader
    except Exception:
        return []

    reader = PdfReader(pdf_path)
    pages: list[str] = []
    for pg in reader.pages:
        txt = pg.extract_text() or ""
        txt = re.sub(r"\s+", " ", txt).strip()
        pages.append(txt)
    return pages


def _chunk_text(text: str, chunk_chars: int = 1100, overlap: int = 220) -> list[str]:
    if not text:
        return []
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= chunk_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(n, start + chunk_chars)
        chunk = text[start:end].strip()

        # merge tiny tail into previous to avoid weak chunks
        if chunks and (n - start) < 260:
            chunks[-1] = (chunks[-1] + " " + chunk).strip()
            break

        chunks.append(chunk)
        if end >= n:
            break
        start = max(0, end - overlap)

    return chunks


@st.cache_data(show_spinner=True)
def build_chunks(pdf_dir: str) -> list[dict]:
    """
    Build text chunks across all PDFs:
    { filename, page_number, chunk_id, text }
    """
    chunks: list[dict] = []
    for pdf_path in list_pdf_files(pdf_dir):
        base = os.path.basename(pdf_path)
        pages = extract_pdf_pages(pdf_path)
        for i, page_txt in enumerate(pages):
            page_no = i + 1
            for cid, c in enumerate(_chunk_text(page_txt)):
                if not c:
                    continue
                chunks.append(
                    {
                        "filename": base,
                        "page_number": page_no,
                        "chunk_id": cid,
                        "text": c,
                    }
                )
    return chunks


@st.cache_resource(show_spinner=False)
def build_bm25_index(pdf_dir: str) -> dict:
    """
    Dependency-free BM25 index over chunks.
    Cached as a resource (fast on reruns).
    """
    chunks = build_chunks(pdf_dir)
    docs_tokens = [_tokenize(c["text"]) for c in chunks]

    df: Dict[str, int] = {}
    for toks in docs_tokens:
        for t in set(toks):
            df[t] = df.get(t, 0) + 1

    N = len(docs_tokens)
    avgdl = (sum(len(t) for t in docs_tokens) / N) if N else 0.0

    return {"chunks": chunks, "docs_tokens": docs_tokens, "df": df, "N": N, "avgdl": avgdl}


def search_pdfs(pdf_dir: str, query: str, top_k: int = 6, allow_files: list[str] | None = None) -> list[PdfHit]:
    """
    BM25 search with optional file filtering (by basename).
    """
    q = (query or "").strip()
    if not q:
        return []

    idx = build_bm25_index(pdf_dir)
    chunks = idx["chunks"]
    docs_tokens = idx["docs_tokens"]
    df = idx["df"]
    N = idx["N"]
    avgdl = idx["avgdl"]

    if N == 0:
        return []

    q_tokens = _tokenize(q)
    if not q_tokens:
        return []

    k1 = 1.5
    b = 0.75

    scores = [0.0] * N
    for i, toks in enumerate(docs_tokens):
        if not toks:
            continue

        c = chunks[i]
        if allow_files is not None and c["filename"] not in allow_files:
            continue

        dl = len(toks)
        tf: Dict[str, int] = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1

        s = 0.0
        for qt in q_tokens:
            if qt not in tf:
                continue
            n_q = df.get(qt, 0)
            idf = math.log(1 + (N - n_q + 0.5) / (n_q + 0.5))
            f = tf[qt]
            denom = f + k1 * (1 - b + b * (dl / (avgdl + 1e-9)))
            s += idf * (f * (k1 + 1)) / (denom + 1e-9)

        scores[i] = s

    ranked = sorted(range(N), key=lambda i: scores[i], reverse=True)

    hits: list[PdfHit] = []
    for i in ranked:
        if scores[i] <= 0:
            continue
        c = chunks[i]
        if allow_files is not None and c["filename"] not in allow_files:
            continue

        snippet = c["text"]
        if len(snippet) > 620:
            snippet = snippet[:620].rstrip() + "…"

        hits.append(
            PdfHit(
                filename=c["filename"],
                page_number=c["page_number"],
                score=float(scores[i]),
                text=snippet,
            )
        )
        if len(hits) >= top_k:
            break

    return hits
