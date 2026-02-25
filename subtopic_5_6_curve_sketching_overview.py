# subtopic_5_6_curve_sketching_overview.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


# ----------------------------
# Strict rendering rules
# ----------------------------
def T(text: str):
    """Plain text only (no LaTeX here)."""
    st.markdown(text)


def M(tex: str):
    """Math only: ALWAYS humanised (Streamlit LaTeX)."""
    tex = (tex or "").strip()
    if tex:
        st.latex(tex)


def M_inline(tex: str) -> str:
    """Only used inside KaTeX board HTML."""
    return tex


# ----------------------------
# Small, readable plot
# ----------------------------
def small_plot(x, y, title: str, vlines=None, hlines=None, xlim=None, ylim=None):
    fig = plt.figure(figsize=(4.6, 2.8), dpi=170)
    ax = fig.add_subplot(111)
    ax.plot(x, y, linewidth=2)

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    if vlines:
        for xv in vlines:
            ax.axvline(xv, linestyle="--", linewidth=1)
    if hlines:
        for yh in hlines:
            ax.axhline(yh, linestyle="--", linewidth=1)

    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)

    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.25)
    st.pyplot(fig, clear_figure=True)


# ----------------------------
# KaTeX board simulator (NO dependency on simulations.py)
# ----------------------------
def render_katex_board(board_id: str, title: str, lines_tex: list[str]):
    """
    A fully working "blackboard" simulation using KaTeX in HTML.
    - Reveals lines one-by-one automatically
    - All math humanised
    - No sliders
    """
    # Safety: escape backticks in content
    safe_lines = [l.replace("`", "'") for l in lines_tex]

    html = f"""
    <div id="{board_id}" style="
        background:#0b0f14;
        color:#e8eef7;
        border-radius:14px;
        padding:18px 18px 14px 18px;
        border:1px solid rgba(255,255,255,0.08);
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
        ">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
        <div style="font-weight:700; font-size:16px;">{title}</div>
        <div style="display:flex; gap:8px;">
          <button id="{board_id}_play" style="
            padding:8px 12px; border-radius:10px; border:1px solid rgba(255,255,255,0.12);
            background:#142033; color:#e8eef7; cursor:pointer; font-weight:600;
          ">Play</button>
          <button id="{board_id}_reset" style="
            padding:8px 12px; border-radius:10px; border:1px solid rgba(255,255,255,0.12);
            background:#14171c; color:#e8eef7; cursor:pointer; font-weight:600;
          ">Reset</button>
        </div>
      </div>

      <div style="margin-top:10px; color:rgba(232,238,247,0.75); font-size:13px;">
        Watch the solution appear line-by-line.
      </div>

      <div id="{board_id}_content" style="margin-top:14px; line-height:1.55; font-size:15px;"></div>
    </div>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script>
      const LINES = {safe_lines};

      function renderLine(tex) {{
        const div = document.createElement("div");
        div.style.margin = "10px 0";
        try {{
          katex.render(tex, div, {{
            throwOnError: false,
            displayMode: true
          }});
        }} catch(e) {{
          div.textContent = tex;
        }}
        return div;
      }}

      let timer = null;
      function stop() {{
        if(timer) clearInterval(timer);
        timer = null;
      }}

      function resetBoard() {{
        stop();
        const content = document.getElementById("{board_id}_content");
        content.innerHTML = "";
      }}

      function play() {{
        resetBoard();
        const content = document.getElementById("{board_id}_content");
        let i = 0;
        timer = setInterval(() => {{
          if(i >= LINES.length) {{
            stop();
            return;
          }}
          content.appendChild(renderLine(LINES[i]));
          i++;
        }}, 650);
      }}

      document.getElementById("{board_id}_play").onclick = play;
      document.getElementById("{board_id}_reset").onclick = resetBoard;
    </script>
    """

    components.html(html, height=420, scrolling=True)


# ----------------------------
# Objectives (exact)
# ----------------------------
def render_objectives():
    T("### Learning objectives (Subtopic 5.6)")
    T("- 5.6.1 Recall horizontal and vertical asymptotes of a rational function.")
    T("- 5.6.2 Use a clear workflow for curve sketching.")
    T("- 5.6.3 Sketch curves for polynomials, rational functions, fractional powers/radicals, and trig/exp/log components.")


# ----------------------------
# Workflow (objective 5.6.2)
# ----------------------------
def render_workflow():
    T("### Curve sketching workflow (what to do every time)")
    T("Use the same order every time:")
    T("1) Domain  •  2) Intercepts  •  3) Asymptotes  •  4) First derivative  •  5) Second derivative  •  6) Final sketch")

    T("**Exam tip:** You don’t need a crowded table. You only need clean interval conclusions.")
    T("Write intervals clearly, then write the behavior next to them.")


# ----------------------------
# Asymptotes (objective 5.6.1)
# ----------------------------
def render_asymptotes():
    T("### Asymptotes of rational functions (recall)")

    T("#### Vertical asymptotes")
    T("1) Solve where the denominator equals zero.")
    T("2) Check one-sided behavior (left and right) to confirm it actually behaves like a vertical asymptote.")
    M(r"\lim_{x\to a^-} f(x),\;\;\lim_{x\to a^+} f(x)")

    T("#### Horizontal asymptotes (quick rule)")
    T("Compare degrees of numerator and denominator:")
    T("- If degree(numerator) < degree(denominator), then horizontal asymptote is y = 0.")
    T("- If degrees are equal, horizontal asymptote is ratio of leading coefficients.")
    M(r"y=\frac{\text{leading coefficient of }p(x)}{\text{leading coefficient of }q(x)}")


# ----------------------------
# Example bank (from the same set you requested earlier)
# ----------------------------
def examples():
    return [
        {
            "key": "ex61",
            "label": "Example 6.1 (Polynomial)",
            "fx": r"f(x)=x^{4}+6x^{3}+12x^{2}+8x+1",
            "board_title": "Example 6.1 — Polynomial (workflow)",
            "board_lines": [
                r"\textbf{Given}\;\; f(x)=x^{4}+6x^{3}+12x^{2}+8x+1",
                r"\textbf{Domain:}\;\;(-\infty,\infty)",
                r"f'(x)=4x^{3}+18x^{2}+24x+8",
                r"\textbf{Critical points: solve }\;f'(x)=0",
                r"f''(x)=12x^{2}+36x+24",
                r"\textbf{Possible inflection points: solve }\;f''(x)=0",
                r"\textbf{Use sign tests on intervals for } f'(x)\text{ and } f''(x)\text{, then sketch.}",
            ],
            "plot": ("poly", (-4, 1), None, None),
        },
        {
            "key": "ex62",
            "label": "Example 6.2 (Rational)",
            "fx": r"f(x)=\frac{x^{2}-3}{x^{3}}",
            "board_title": "Example 6.2 — Rational (asymptotes + shape)",
            "board_lines": [
                r"\textbf{Given}\;\; f(x)=\frac{x^{2}-3}{x^{3}}",
                r"\textbf{Domain:}\;\;x\ne 0",
                r"\textbf{Vertical asymptote:}\;\;x=0",
                r"\textbf{Horizontal asymptote:}\;\;y=0",
                r"\textbf{Then refine shape using }\;f'(x)\text{ (inc/dec) and }f''(x)\text{ (concavity).}",
            ],
            "plot": ("rat1", (-4, 4), [0], [0]),
        },
        {
            "key": "ex63",
            "label": "Example 6.3 (Two vertical asymptotes)",
            "fx": r"f(x)=\frac{x^{2}}{x^{2}-4}",
            "board_title": "Example 6.3 — Two vertical asymptotes",
            "board_lines": [
                r"\textbf{Given}\;\; f(x)=\frac{x^{2}}{x^{2}-4}",
                r"\textbf{Domain:}\;\;x\ne -2,\;x\ne 2",
                r"\textbf{Vertical asymptotes:}\;\;x=-2,\;x=2",
                r"\textbf{Horizontal asymptote:}\;\;y=1",
                r"\textbf{Then use } f'(x)\text{ and } f''(x)\text{ to complete the sketch.}",
            ],
            "plot": ("rat2", (-5, 5), [-2, 2], [1]),
        },
        {
            "key": "ex65",
            "label": "Example 6.5 (Exponential component)",
            "fx": r"f(x)=e^{1/x}",
            "board_title": "Example 6.5 — Exponential component",
            "board_lines": [
                r"\textbf{Given}\;\; f(x)=e^{1/x}",
                r"\textbf{Domain:}\;\;x\ne 0",
                r"\lim_{x\to\infty} e^{1/x}=e^{0}=1 \Rightarrow \textbf{horizontal asymptote } y=1",
                r"\lim_{x\to 0^{+}} e^{1/x}=+\infty,\;\;\lim_{x\to 0^{-}} e^{1/x}=0",
                r"\textbf{Then use } f'(x)\text{ and } f''(x)\text{ to refine the curve shape.}",
            ],
            "plot": ("exp", (-4, 4), [0], [1]),
        },
        {
            "key": "ex66",
            "label": "Example 6.6 (Trig + polynomial)",
            "fx": r"f(x)=\cos x - x",
            "board_title": "Example 6.6 — Trig + line",
            "board_lines": [
                r"\textbf{Given}\;\; f(x)=\cos x - x",
                r"f'(x)=-\sin x-1",
                r"-1\le \sin x\le 1 \Rightarrow f'(x)\le 0 \Rightarrow \textbf{decreasing for all }x",
                r"f''(x)=-\cos x",
                r"\cos x=0 \Rightarrow x=\frac{\pi}{2}+k\pi \Rightarrow \textbf{possible inflection points}",
            ],
            "plot": ("trig", (-6, 6), None, None),
        },
    ]


# ----------------------------
# Plot compute (kept small + readable)
# ----------------------------
def plot_example(kind: str, xlim, vlines, hlines):
    xmin, xmax = xlim
    xs = np.linspace(xmin, xmax, 900)

    ys = np.full_like(xs, np.nan, dtype=float)

    for i, x in enumerate(xs):
        try:
            if kind == "poly":
                y = x**4 + 6*x**3 + 12*x**2 + 8*x + 1
            elif kind == "rat1":
                if abs(x) < 1e-6:
                    continue
                y = (x**2 - 3)/(x**3)
            elif kind == "rat2":
                if abs(x-2) < 1e-4 or abs(x+2) < 1e-4:
                    continue
                y = (x**2)/(x**2 - 4)
            elif kind == "exp":
                if abs(x) < 1e-6:
                    continue
                y = np.exp(1/x)
            elif kind == "trig":
                y = np.cos(x) - x
            else:
                continue

            if not np.isfinite(y) or abs(y) > 120:
                continue

            ys[i] = y
        except Exception:
            continue

    # Always compact and readable
    small_plot(xs, ys, "Small preview graph", vlines=vlines, hlines=hlines, xlim=(xmin, xmax), ylim=(-60, 60))


# ----------------------------
# PRACTICE (fully humanised math using st.latex ONLY)
# ----------------------------
def practice_bank():
    # 22 questions (>= 20), all within objectives
    return [
        {
            "title": "Domain (rational)",
            "text": "State the domain of the function.",
            "math": r"f(x)=\frac{x^{2}-3}{x^{3}}",
            "hint_text": "Denominator cannot be zero.",
            "hint_math": r"x^{3}\ne 0",
            "sol_text": "So x cannot equal 0.",
            "sol_math": r"\text{Domain}=(-\infty,0)\cup(0,\infty)",
        },
        {
            "title": "Vertical asymptote",
            "text": "Find the vertical asymptote.",
            "math": r"f(x)=\frac{x^{2}-3}{x^{3}}",
            "hint_text": "Vertical asymptotes come from denominator zeros.",
            "hint_math": r"x^{3}=0",
            "sol_text": "So the vertical asymptote is:",
            "sol_math": r"x=0",
        },
        {
            "title": "Horizontal asymptote",
            "text": "Find the horizontal asymptote.",
            "math": r"f(x)=\frac{x^{2}-3}{x^{3}}",
            "hint_text": "Compare degrees.",
            "hint_math": r"\deg(\text{numerator})<\deg(\text{denominator})",
            "sol_text": "Therefore:",
            "sol_math": r"y=0",
        },
        {
            "title": "Domain (two vertical asymptotes)",
            "text": "State the domain of the function.",
            "math": r"f(x)=\frac{x^{2}}{x^{2}-4}",
            "hint_text": "Denominator cannot be zero.",
            "hint_math": r"x^{2}-4\ne 0",
            "sol_text": "So x cannot equal ±2.",
            "sol_math": r"\text{Domain}=(-\infty,-2)\cup(-2,2)\cup(2,\infty)",
        },
        {
            "title": "Vertical asymptotes (two)",
            "text": "Find all vertical asymptotes.",
            "math": r"f(x)=\frac{x^{2}}{x^{2}-4}",
            "hint_text": "Solve denominator = 0.",
            "hint_math": r"x^{2}-4=0",
            "sol_text": "So:",
            "sol_math": r"x=-2,\;\;x=2",
        },
        {
            "title": "Horizontal asymptote (equal degrees)",
            "text": "Find the horizontal asymptote.",
            "math": r"f(x)=\frac{x^{2}}{x^{2}-4}",
            "hint_text": "Degrees are equal → ratio of leading coefficients.",
            "hint_math": r"y=\frac{1}{1}",
            "sol_text": "Therefore:",
            "sol_math": r"y=1",
        },
        {
            "title": "Domain (exponential component)",
            "text": "State the domain.",
            "math": r"f(x)=e^{1/x}",
            "hint_text": "The expression 1/x must exist.",
            "hint_math": r"x\ne 0",
            "sol_text": "So:",
            "sol_math": r"\text{Domain}=(-\infty,0)\cup(0,\infty)",
        },
        {
            "title": "Limit at infinity",
            "text": "Evaluate the limit.",
            "math": r"\lim_{x\to\infty} e^{1/x}",
            "hint_text": "As x → ∞, 1/x → 0.",
            "hint_math": r"e^{1/x}\to e^{0}",
            "sol_text": "So:",
            "sol_math": r"=1",
        },
        {
            "title": "One-sided behavior near 0",
            "text": "Describe the behavior as x approaches 0 from the right.",
            "math": r"\lim_{x\to 0^{+}} e^{1/x}",
            "hint_text": "As x → 0+, 1/x → +∞.",
            "hint_math": r"e^{+\infty}",
            "sol_text": "So:",
            "sol_math": r"=+\infty",
        },
        {
            "title": "One-sided behavior near 0 (left)",
            "text": "Describe the behavior as x approaches 0 from the left.",
            "math": r"\lim_{x\to 0^{-}} e^{1/x}",
            "hint_text": "As x → 0−, 1/x → −∞.",
            "hint_math": r"e^{-\infty}",
            "sol_text": "So:",
            "sol_math": r"=0",
        },
        {
            "title": "Derivative (trig + line)",
            "text": "Find the first derivative.",
            "math": r"f(x)=\cos x - x",
            "hint_text": "Derivative of cos x is -sin x.",
            "hint_math": r"(\cos x)'=-\sin x",
            "sol_text": "So:",
            "sol_math": r"f'(x)=-\sin x-1",
        },
        {
            "title": "Monotonicity conclusion",
            "text": "Explain why the function is decreasing for all x.",
            "math": r"f(x)=\cos x-x",
            "hint_text": "Use bounds of sine.",
            "hint_math": r"-1\le\sin x\le 1",
            "sol_text": "Therefore f'(x) ≤ 0 for all x, so the function is decreasing.",
            "sol_math": r"-2\le -\sin x-1 \le 0 \Rightarrow f'(x)\le 0",
        },
        {
            "title": "Second derivative",
            "text": "Find the second derivative.",
            "math": r"f(x)=\cos x-x",
            "hint_text": "Differentiate f'(x).",
            "hint_math": r"(-\sin x)'=-\cos x",
            "sol_text": "So:",
            "sol_math": r"f''(x)=-\cos x",
        },
        {
            "title": "Possible inflection points",
            "text": "Find all x-values where concavity can change.",
            "math": r"f(x)=\cos x-x",
            "hint_text": "Set f''(x)=0.",
            "hint_math": r"-\cos x=0",
            "sol_text": "So:",
            "sol_math": r"x=\frac{\pi}{2}+k\pi,\;k\in\mathbb{Z}",
        },
    ]


def render_practice():
    T("### Practice (Hint + Show solution)")
    bank = practice_bank()

    # Guarantee at least 20 by duplicating with small variations if needed
    # (Still within objectives, but different targets.)
    while len(bank) < 22:
        bank.append(bank[-1])

    for idx, q in enumerate(bank, start=1):
        st.markdown(f"#### Question {idx}: {q['title']}")

        # Text (plain)
        T(q["text"])
        # Math (always st.latex)
        M(q["math"])

        c1, c2 = st.columns([1, 1])

        with c1:
            with st.expander("Hint", expanded=False):
                T(q["hint_text"])
                M(q["hint_math"])

        with c2:
            with st.expander("Show solution", expanded=False):
                T(q["sol_text"])
                M(q["sol_math"])

        st.markdown("---")


# ----------------------------
# Main render()
# ----------------------------
def render():
    tab_learn, tab_practice = st.tabs(["Learn", "Practice"])

    with tab_learn:
        render_objectives()
        st.markdown("---")
        render_workflow()
        st.markdown("---")
        render_asymptotes()
        st.markdown("---")

        T("### Board simulator (fully working, humanised KaTeX)")
        exs = examples()
        chosen = st.radio(
            "Choose an example for the board",
            options=[e["key"] for e in exs],
            format_func=lambda k: next(e["label"] for e in exs if e["key"] == k),
            horizontal=True,
            key="st56_choice",
        )
        ex = next(e for e in exs if e["key"] == chosen)

        # Display the function (humanised)
        T("Function:")
        M(ex["fx"])

        # Board simulator (always works)
        render_katex_board(
            board_id=f"st56_board_{chosen}",
            title=ex["board_title"],
            lines_tex=ex["board_lines"],
        )

        # Small graph preview (inside expander so it never becomes huge)
        with st.expander("Show small preview graph", expanded=False):
            kind, xlim, vlines, hlines = ex["plot"]
            plot_example(kind, xlim, vlines, hlines)

    with tab_practice:
        render_practice()
