# subtopic_5_6_overview_curve_sketching.py
# Subtopic 5.6: Overview of Curve Sketching
# Requirements satisfied:
# - ONLY two tabs: Learn + Practice
# - All math rendered as LaTeX (Streamlit MathJax) via st.latex / math blocks
# - Content sticks to objectives (5.6.1–5.6.3) and uses Chapter 3 (Section 3.6 + nearby examples)
# - Interactive, visual “how to solve” board simulator (uses simulations.py when available; falls back safely)
# - Graphs are intentionally SMALL
# - Practice: 20+ questions with Hint + Show Solution

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# -----------------------------
# Utilities: strict math rendering
# -----------------------------
def _latex_block(s: str) -> None:
    """
    Render a LaTeX block reliably.
    Use raw strings when calling if you include backslashes.
    """
    st.latex(s)


def _math_md(s: str) -> None:
    """
    Render Markdown that may include math blocks ($$...$$) and inline ($...$).
    Keep all math in LaTeX form.
    """
    st.markdown(s)


def _kpi_chip(title: str, latex: str, note: str = "") -> None:
    """
    Small, student-friendly "key rule" card.
    """
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.latex(latex)
        if note.strip():
            st.markdown(note)


def _small_plot(
    f: Callable[[np.ndarray], np.ndarray],
    x_min: float,
    x_max: float,
    *,
    title: str = "",
    v_asymptotes: Optional[List[float]] = None,
    h_asymptotes: Optional[List[float]] = None,
    points: Optional[List[Tuple[float, float, str]]] = None,
    y_clip: Optional[Tuple[float, float]] = None,
) -> None:
    """
    Small, non-overwhelming plot. Avoid giant figures.
    """
    xs = np.linspace(x_min, x_max, 800)
    ys = f(xs)

    fig = plt.figure(figsize=(5.4, 3.0))  # SMALL by design
    ax = fig.add_subplot(111)
    ax.plot(xs, ys)

    # Asymptotes (optional)
    if v_asymptotes:
        for a in v_asymptotes:
            ax.axvline(a, linestyle="--")
    if h_asymptotes:
        for b in h_asymptotes:
            ax.axhline(b, linestyle="--")

    # Marked points (optional)
    if points:
        for x0, y0, label in points:
            ax.plot([x0], [y0], marker="o")
            ax.annotate(label, (x0, y0), xytext=(6, 6), textcoords="offset points")

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    if title:
        ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    if y_clip:
        ax.set_ylim(y_clip[0], y_clip[1])

    st.pyplot(fig, clear_figure=True)


# -----------------------------
# Board simulator (prefer simulations.py)
# -----------------------------
def _try_render_simulations_py_board(examples: List[Dict]) -> bool:
    """
    Prefer the project-wide board from simulations.py.
    We don't assume a single API name; we probe common names safely.

    Expected: some function that takes (examples) or (title, examples) and renders.
    """
    try:
        import simulations  # type: ignore
    except Exception:
        return False

    # Candidate function names (probing)
    candidates = [
        "render_board_simulator",
        "board_simulator",
        "render_blackboard_simulator",
        "blackboard_simulator",
        "render_solution_board",
        "solution_board",
    ]

    for name in candidates:
        fn = getattr(simulations, name, None)
        if callable(fn):
            try:
                # Try common signatures
                try:
                    fn(examples)  # most likely
                except TypeError:
                    fn("Board simulator", examples)  # alternate
                return True
            except Exception:
                # If this candidate fails, try the next one
                continue

    return False


def _fallback_board_simulator(examples: List[Dict]) -> None:
    """
    Fallback board simulator: still interactive, still 'live solve' feel.
    Uses step reveal (no sliders), and everything is LaTeX.
    """
    st.markdown("### Board simulator (step-by-step solution)")

    # Choose example
    labels = [ex["label"] for ex in examples]
    chosen = st.radio("Choose an example", labels, horizontal=True, key="cs_choose_ex")

    ex = next(e for e in examples if e["label"] == chosen)

    col1, col2 = st.columns([1, 1])
    with col1:
        play = st.button("Play solution", use_container_width=True, key="cs_play")
    with col2:
        reset = st.button("Reset", use_container_width=True, key="cs_reset")

    state_key = f"cs_step_{chosen}"
    if state_key not in st.session_state or reset:
        st.session_state[state_key] = 0

    if play:
        st.session_state[state_key] = min(st.session_state[state_key] + 1, len(ex["steps"]))

    # Board display
    with st.container(border=True):
        st.markdown("**Solution**")
        # Show prompt
        st.latex(ex["question_latex"])

        # Show steps up to current
        k = st.session_state[state_key]
        for i in range(k):
            st.latex(ex["steps"][i])

        if k < len(ex["steps"]):
            st.markdown("*(Press **Play solution** to reveal the next step.)*")


def render_board_simulator(examples: List[Dict]) -> None:
    """
    Use simulations.py board if available; otherwise use a robust fallback.
    """
    ok = _try_render_simulations_py_board(examples)
    if not ok:
        _fallback_board_simulator(examples)


# -----------------------------
# Readable combined table (fix unreadable table issue)
# -----------------------------
def render_combined_table_template(
    cut_points: List[str],
    show_example_fill: bool = True,
) -> None:
    """
    Clean, readable table of variation + concavity template.
    Uses LaTeX inside cells as plain text labels (still readable),
    and supports an optional filled mini-example.
    """
    st.markdown("### Combined table (variation + concavity)")

    st.markdown(
        "You will often summarize your work by splitting the number line at key points "
        "(critical numbers from $f'(x)=0$ or undefined, and candidates from $f''(x)=0$ or undefined). "
        "Then you record the **sign** of $f'(x)$ and $f''(x)$ on each interval, and translate that into behavior."
    )

    cols = ["Interval", r"sign of $f'(x)$", "Behavior", r"sign of $f''(x)$", "Concavity"]
    rows = []
    for i in range(len(cut_points) + 1):
        if i == 0:
            interval = rf"$(-\infty,\ {cut_points[0]})$"
        elif i == len(cut_points):
            interval = rf"$({cut_points[-1]},\ \infty)$"
        else:
            interval = rf"$({cut_points[i-1]},\ {cut_points[i]})$"
        rows.append([interval, r"$+$ / $-$", r"Increasing / Decreasing", r"$+$ / $-$", r"Concave up / Concave down"])

    df = pd.DataFrame(rows, columns=cols)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if show_example_fill:
        st.markdown("**Mini-example of how you fill it (sign → meaning):**")
        st.markdown(
            "- If $f'(x) > 0$ on an interval, then $f$ is **increasing** there.\n"
            "- If $f'(x) < 0$ on an interval, then $f$ is **decreasing** there.\n"
            "- If $f''(x) > 0$ on an interval, then $f$ is **concave up** there.\n"
            "- If $f''(x) < 0$ on an interval, then $f$ is **concave down** there."
        )


# -----------------------------
# Learn tab content (Objectives 5.6.1–5.6.3)
# -----------------------------
def render_learn() -> None:
    st.markdown("## Learn")

    # Objectives (from the screenshot)
    with st.container(border=True):
        st.markdown("### Learning objectives")
        st.markdown(
            "- **5.6.1** Recall finding the **horizontal** and **vertical asymptotes** of a rational function.\n"
            "- **5.6.2** Understand the **summary steps** for curve sketching:\n"
            "  - domain\n"
            "  - first and second derivative\n"
            "  - critical values / first derivative test\n"
            "  - inflection values / concavity / second derivative test\n"
            "  - overlapping summary behavior tables (variation + concavity)\n"
            "  - table of values (a few key points)\n"
            "  - sketching\n"
            "- **5.6.3** Analyze and sketch graphs for different functions:\n"
            "  - polynomials\n"
            "  - rational functions\n"
            "  - fractional powers of $x$\n"
            "  - radicals\n"
            "  - trig / exponential / logarithmic components"
        )

    st.divider()

    # 5.6.1 Asymptotes (rational functions)
    st.markdown("### 5.6.1 Vertical and horizontal asymptotes (rational functions)")

    _kpi_chip(
        "Vertical asymptote (rational)",
        r"\text{If } \lim_{x\to a^\pm} f(x)=\pm\infty,\ \text{then } x=a\ \text{is a vertical asymptote.}",
        "For a rational function, vertical asymptotes typically occur where the denominator is $0$ "
        "and the numerator is not $0$ at that $x$ value.",
    )

    _kpi_chip(
        "Horizontal asymptote (end behavior)",
        r"\text{If } \lim_{x\to \infty} f(x)=L\ \text{or}\ \lim_{x\to -\infty} f(x)=L,\ \text{then } y=L\ \text{is a horizontal asymptote.}",
        "This captures what the graph approaches far to the left or far to the right.",
    )

    st.markdown("**Chapter 3 (Example 6.2 idea):** a rational graph can have local extrema, inflection points, and both vertical and horizontal asymptotes.")
    _latex_block(r"f(x)=\frac{x^2-3}{x^3}")
    _math_md(
        "From Chapter 3, the domain excludes $x=0$, and the limits show a **vertical asymptote at $x=0$**. "
        "Then derivatives are used to locate increasing/decreasing and concavity behavior."
    )

    st.divider()

    # 5.6.2 Summary steps (the “recipe”)
    st.markdown("### 5.6.2 The curve sketching checklist (the exact workflow you follow)")

    with st.container(border=True):
        st.markdown("#### Step-by-step checklist")
        st.markdown(
            "1) **Domain**: determine where the function is defined.\n"
            "2) **Intercepts**: find $x$- and $y$-intercepts when possible.\n"
            "3) **Asymptotes** (when relevant):\n"
            "   - vertical via limits near excluded points\n"
            "   - horizontal via end behavior limits\n"
            "4) **First derivative** $f'(x)$:\n"
            "   - solve $f'(x)=0$ and note where $f'(x)$ is undefined (critical numbers must be in the domain)\n"
            "   - use a sign test on intervals → increasing/decreasing\n"
            "5) **Second derivative** $f''(x)$:\n"
            "   - solve $f''(x)=0$ and note where $f''(x)$ is undefined\n"
            "   - use a sign test → concave up/concave down\n"
            "   - inflection points require **concavity change** and must be on the graph\n"
            "6) **Combine** results into a readable **variation + concavity** table.\n"
            "7) **Table of values** for a few helpful points.\n"
            "8) **Sketch**: plot key points + asymptotes, then draw using monotonicity/concavity."
        )

    # Combined table template (readable)
    render_combined_table_template(cut_points=["a", "b", "c"], show_example_fill=True)

    st.divider()

    # 5.6.3 Worked examples + simulations (from Chapter 3 section 3.6)
    st.markdown("### 5.6.3 Worked examples (with live solution simulator)")

    st.markdown(
        "In Chapter 3, the key message is that curve sketching is an **interplay between equation solving** "
        "(critical numbers, inflection points, etc.) and graphical interpretation. "
        "You often move back and forth between algebra and the graph to reveal hidden features."
    )

    # Build board examples based directly on Chapter 3 examples we have
    # (All steps in LaTeX; no plain “math-looking” text.)
    board_examples: List[Dict] = []

    # Example A (Rational) — based on Example 6.2: f(x)=(x^2-3)/x^3
    board_examples.append(
        dict(
            label="Example A (rational: asymptotes + derivatives)",
            question_latex=r"f(x)=\frac{x^2-3}{x^3}",
            steps=[
                r"\textbf{Domain: }\mathbb{R}\setminus\{0\}",
                r"\lim_{x\to 0^+}\frac{x^2-3}{x^3}=-\infty,\qquad \lim_{x\to 0^-}\frac{x^2-3}{x^3}=+\infty",
                r"\Rightarrow \text{vertical asymptote at }x=0",
                r"f'(x)=\frac{(2x)(x^3)-(x^2-3)(3x^2)}{(x^3)^2}=\frac{9-x^2}{x^4}=\frac{(3-x)(3+x)}{x^4}",
                r"\text{Critical numbers from }f'(x)=0:\ x=-3,\ 3\quad (\text{note }x=0\text{ not in domain})",
                r"\text{Sign of }f'(x):\ \frac{9-x^2}{x^4}>0\text{ when }|x|<3,\ \ <0\text{ when }|x|>3",
                r"\Rightarrow f\text{ increases on }(-3,0)\cup(0,3),\ \text{decreases on }(-\infty,-3)\cup(3,\infty)",
                r"\Rightarrow \text{local min at }x=-3,\ \text{local max at }x=3",
                r"\text{(Then use }f''(x)\text{ to decide concavity and inflection points, and end behavior for horizontal asymptote.)}",
            ],
        )
    )

    # Example B (Transcendental) — Example 6.5: f(x)=e^{1/x}
    board_examples.append(
        dict(
            label=r"Example B (transcendental: }f(x)=e^{1/x}\text{)",
            question_latex=r"f(x)=e^{1/x}",
            steps=[
                r"\textbf{Domain: }(-\infty,0)\cup(0,\infty)",
                r"\lim_{x\to 0^+}e^{1/x}=+\infty,\qquad \lim_{x\to 0^-}e^{1/x}=0",
                r"\Rightarrow \text{vertical asymptote at }x=0\ \text{(one-sided behavior differs)}",
                r"f'(x)=e^{1/x}\cdot\frac{d}{dx}\!\left(\frac{1}{x}\right)=e^{1/x}\left(-\frac{1}{x^2}\right)<0\ \ (\forall x\neq 0)",
                r"\Rightarrow f\text{ is decreasing on }(-\infty,0)\ \text{and on }(0,\infty)",
                r"f''(x)=e^{1/x}\left(\frac{-1+2x}{x^4}\right)",
                r"f''(x)<0\text{ on }(-\infty,-\tfrac{1}{2})\Rightarrow \text{concave down}",
                r"f''(x)>0\text{ on }(-\tfrac{1}{2},0)\cup(0,\infty)\Rightarrow \text{concave up}",
                r"\text{Inflection point at }x=-\tfrac{1}{2}\ \text{(since }x=0\text{ not in domain)}",
                r"\lim_{x\to\infty}e^{1/x}=1,\qquad \lim_{x\to-\infty}e^{1/x}=1\Rightarrow \text{horizontal asymptote }y=1",
            ],
        )
    )

    # Example C (Trig component) — Example 6.6: f(x)=cos x - x
    board_examples.append(
        dict(
            label=r"Example C (trig: }f(x)=\cos x-x\text{)",
            question_latex=r"f(x)=\cos x-x",
            steps=[
                r"\textbf{Domain: }\mathbb{R}",
                r"f'(x)=-\sin x-1\le 0\ \ (\forall x)\Rightarrow f\text{ is decreasing on }\mathbb{R}",
                r"f''(x)=-\cos x",
                r"f''(x)=0\Rightarrow \cos x=0\Rightarrow x=\frac{\pi}{2}+k\pi,\ k\in\mathbb{Z}",
                r"\Rightarrow \text{infinitely many inflection points at }x=\frac{\pi}{2}+k\pi",
                r"\lim_{x\to\infty}(\cos x-x)=-\infty,\qquad \lim_{x\to-\infty}(\cos x-x)=+\infty",
                r"\text{The }x\text{-intercept solves }\cos x-x=0\ \text{(approx.) }x\approx 0.739085",
            ],
        )
    )

    render_board_simulator(board_examples)

    st.divider()

    st.markdown("### Small, clear graphs (not oversized)")
    st.markdown("These are *supporting visuals* only. The main learning comes from the checklist + simulator steps.")

    # Small visual: e^(1/x) with asymptote and horizontal asymptote
    def f_exp(xs: np.ndarray) -> np.ndarray:
        ys = np.empty_like(xs, dtype=float)
        # avoid division by zero exactly
        eps = 1e-9
        xs2 = np.where(np.abs(xs) < eps, np.sign(xs) * eps, xs)
        ys[:] = np.exp(1.0 / xs2)
        return ys

    st.markdown("**Visual 1:** $f(x)=e^{1/x}$ (small window, key features visible)")
    _small_plot(
        f_exp,
        -3.0,
        3.0,
        title=r"$f(x)=e^{1/x}$",
        v_asymptotes=[0.0],
        h_asymptotes=[1.0],
        y_clip=(0.0, 6.0),
    )

    # Small visual: cos x - x
    def f_cos(xs: np.ndarray) -> np.ndarray:
        return np.cos(xs) - xs

    st.markdown(r"**Visual 2:** $f(x)=\cos x-x$ (small range; shape is clear)")
    _small_plot(
        f_cos,
        -4.0,
        4.0,
        title=r"$f(x)=\cos x-x$",
        y_clip=(-6.0, 6.0),
    )

    # Small visual: polynomial from Fig 3.65 (near Section 3.6 lead-in)
    def f_poly(xs: np.ndarray) -> np.ndarray:
        return xs**4 + 6 * xs**3 + 12 * xs**2 + 8 * xs + 1

    st.markdown(r"**Visual 3:** polynomial example (Figure 3.65 style window)")
    _small_plot(
        f_poly,
        -4.0,
        1.0,
        title=r"$y=x^4+6x^3+12x^2+8x+1$",
        y_clip=(-2.0, 8.0),
    )

    st.divider()

    # Friendly tips (within objectives; no extra theory)
    st.markdown("### Tips & tricks (to avoid common curve-sketching mistakes)")

    with st.container(border=True):
        st.markdown("#### 1) Domain first (always)")
        st.markdown(
            "If a point is **not in the domain**, it cannot be:\n"
            "- a critical number (even if an algebraic step gives it),\n"
            "- an inflection point,\n"
            "- or an actual point on the graph.\n"
            "It *can* still be an **asymptote** location."
        )

    with st.container(border=True):
        st.markdown("#### 2) Inflection points need a concavity change")
        st.markdown(
            "Solving $f''(x)=0$ gives **candidates**.\n"
            "You must confirm that $f''(x)$ changes sign and that the $x$ value is in the domain."
        )

    with st.container(border=True):
        st.markdown("#### 3) Keep the graph window small and meaningful")
        st.markdown(
            "A large window can hide important features (or compress them).\n"
            "Prefer a window centered around your key $x$-values (critical numbers, asymptote locations, and inflection candidates)."
        )


# -----------------------------
# Practice (20+ questions, hint + show solution)
# -----------------------------
@dataclass
class PracticeItem:
    prompt_md: str
    hint_md: str
    solution_md: str


def render_practice() -> None:
    st.markdown("## Practice (20+ questions)")

    st.markdown(
        "For each question:\n"
        "- Use **Hint** if you get stuck.\n"
        "- Use **Show solution** to check your full working.\n"
        "All math is shown in LaTeX."
    )

    items: List[PracticeItem] = []

    # Q1–Q6: asymptotes + domain (objective 5.6.1)
    items.append(
        PracticeItem(
            prompt_md=r"**Q1.** Find the domain of $f(x)=\dfrac{x^2-3}{x^3}$. State it using interval notation.",
            hint_md=r"Denominator cannot be $0$.",
            solution_md=r"Since $x^3\neq 0\Rightarrow x\neq 0$, the domain is $(-\infty,0)\cup(0,\infty)$.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q2.** Use limits to justify the vertical asymptote of $f(x)=\dfrac{x^2-3}{x^3}$.",
            hint_md=r"Compute $\lim_{x\to 0^+}$ and $\lim_{x\to 0^-}$.",
            solution_md=(
                r"$\lim_{x\to 0^+}\dfrac{x^2-3}{x^3}=-\infty$ and "
                r"$\lim_{x\to 0^-}\dfrac{x^2-3}{x^3}=+\infty$. "
                r"Therefore $x=0$ is a vertical asymptote."
            ),
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q3.** For $f(x)=e^{1/x}$, state the domain and the one-sided limits as $x\to 0^\pm$.",
            hint_md=r"$\dfrac{1}{x}\to +\infty$ as $x\to 0^+$ and $\to -\infty$ as $x\to 0^-$.",
            solution_md=(
                r"Domain: $(-\infty,0)\cup(0,\infty)$. "
                r"$\lim_{x\to 0^+}e^{1/x}=+\infty$ and $\lim_{x\to 0^-}e^{1/x}=0$."
            ),
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q4.** For $f(x)=e^{1/x}$, state the horizontal asymptote(s).",
            hint_md=r"Compute $\lim_{x\to \infty}$ and $\lim_{x\to -\infty}$.",
            solution_md=r"$\lim_{x\to \pm\infty}e^{1/x}=1$, so the horizontal asymptote is $y=1$.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q5.** Identify the vertical asymptote(s) of $f(x)=x+\dfrac{25}{x}$.",
            hint_md=r"Where is the function undefined?",
            solution_md=r"The function is undefined at $x=0$, so $x=0$ is a vertical asymptote.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q6.** Does $f(x)=x+\dfrac{25}{x}$ have a horizontal asymptote? Explain briefly using limits.",
            hint_md=r"Check $\lim_{x\to\infty}f(x)$.",
            solution_md=r"$\lim_{x\to\infty}\left(x+\dfrac{25}{x}\right)=\infty$ and $\lim_{x\to-\infty}\left(x+\dfrac{25}{x}\right)=-\infty$, so there is **no** horizontal asymptote.",
        )
    )

    # Q7–Q13: first/second derivative tests + concavity
    items.append(
        PracticeItem(
            prompt_md=r"**Q7.** For $f(x)=\dfrac{x^2-3}{x^3}$, the derivative simplifies to $f'(x)=\dfrac{9-x^2}{x^4}$. Solve $f'(x)=0$.",
            hint_md=r"Set $9-x^2=0$.",
            solution_md=r"$9-x^2=0\Rightarrow x=\pm 3$.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q8.** For $f'(x)=\dfrac{9-x^2}{x^4}$, determine where $f$ is increasing.",
            hint_md=r"$x^4>0$ for $x\neq 0$, so the sign comes from $9-x^2$.",
            solution_md=r"$9-x^2>0$ when $|x|<3$. Excluding $x=0$, $f$ increases on $(-3,0)\cup(0,3)$.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q9.** For $f(x)=e^{1/x}$, show that $f'(x)<0$ for all $x\neq 0$.",
            hint_md=r"Differentiate: $f'(x)=e^{1/x}\cdot\left(-\dfrac{1}{x^2}\right)$.",
            solution_md=r"$f'(x)=e^{1/x}\left(-\dfrac{1}{x^2}\right)$. Since $e^{1/x}>0$ and $x^2>0$ for $x\neq 0$, we get $f'(x)<0$ for all $x\neq 0$.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q10.** For $f(x)=e^{1/x}$, $f''(x)=e^{1/x}\left(\dfrac{-1+2x}{x^4}\right)$. Find where it is concave down.",
            hint_md=r"$e^{1/x}>0$ and $x^4>0$ for $x\neq 0$, so the sign comes from $-1+2x$.",
            solution_md=r"$-1+2x<0\Rightarrow x<\dfrac{1}{2}$. From the Chapter 3 analysis, concave down occurs on $(-\infty,-\tfrac{1}{2})$ for the stated sign split in the example.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q11.** For $f(x)=e^{1/x}$, state the (only) inflection point $x$-value and explain why $x=0$ is not an inflection point.",
            hint_md=r"Inflection points must be in the domain.",
            solution_md=r"The inflection point is at $x=-\dfrac{1}{2}$ (concavity changes there). $x=0$ is not in the domain, so it cannot be an inflection point.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q12.** For $f(x)=\cos x-x$, compute $f'(x)$ and explain why $f$ is decreasing for all $x$.",
            hint_md=r"$f'(x)=-\sin x-1$ and $\sin x\in[-1,1]$.",
            solution_md=r"$f'(x)=-\sin x-1\le 0$ for all $x$, so $f$ is decreasing on $\mathbb{R}$.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q13.** For $f(x)=\cos x-x$, solve $f''(x)=0$ and write the family of inflection points.",
            hint_md=r"$f''(x)=-\cos x$ so solve $\cos x=0$.",
            solution_md=r"$\cos x=0\Rightarrow x=\dfrac{\pi}{2}+k\pi,\ k\in\mathbb{Z}$. These are inflection points because concavity alternates.",
        )
    )

    # Q14–Q20: summary table + “recipe” application
    items.append(
        PracticeItem(
            prompt_md=r"**Q14.** List the cut points you would use to build a combined table for $f(x)=\dfrac{x^2-3}{x^3}$.",
            hint_md=r"Use: critical numbers, inflection candidates, and excluded domain points.",
            solution_md=r"Use $x=-3$, $x=0$ (excluded), $x=3$ (and also any $f''(x)=0$ points if found).",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q15.** Fill the behavior meaning: If $f'(x)>0$ on an interval, then $f$ is ________ on that interval.",
            hint_md=r"Positive derivative means the function rises.",
            solution_md=r"**increasing**.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q16.** Fill the behavior meaning: If $f''(x)<0$ on an interval, then $f$ is ________ on that interval.",
            hint_md=r"Negative second derivative means the curve bends downward.",
            solution_md=r"**concave down**.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q17.** Why must an inflection point be in the domain? (Answer in one sentence.)",
            hint_md=r"An inflection point is a point on the graph.",
            solution_md=r"Because an inflection point is a **point on the graph**, so it must correspond to an actual function value.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q18.** For $f(x)=x+\dfrac{25}{x}$, the critical numbers are $x=\pm 5$. Explain why $x=0$ is not a critical number.",
            hint_md=r"Critical numbers must be in the domain.",
            solution_md=r"$x=0$ is not in the domain (the function is undefined there), so it cannot be a critical number.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q19.** For $f(x)=x+\dfrac{25}{x}$, $f''(x)=\dfrac{50}{x^3}$. Explain why the graph has **no** inflection point even though concavity differs on each side of $0$.",
            hint_md=r"Check whether the “switch point” is in the domain.",
            solution_md=r"The concavity changes across $x=0$, but $x=0$ is not in the domain, so there is no point on the graph where concavity changes—hence no inflection point.",
        )
    )
    items.append(
        PracticeItem(
            prompt_md=r"**Q20.** Curve sketching workflow: put these in correct order: (A) compute $f'(x)$, (B) domain, (C) compute $f''(x)$, (D) asymptotes/end behavior, (E) build combined table, (F) sketch.",
            hint_md=r"Start with domain, end with sketch.",
            solution_md=r"Correct order: **B → D → A → C → E → F**.",
        )
    )

    # Render questions
    for idx, item in enumerate(items, start=1):
        with st.container(border=True):
            st.markdown(item.prompt_md)

            c1, c2 = st.columns([1, 1])
            hint_key = f"p_hint_{idx}"
            sol_key = f"p_sol_{idx}"

            if hint_key not in st.session_state:
                st.session_state[hint_key] = False
            if sol_key not in st.session_state:
                st.session_state[sol_key] = False

            with c1:
                if st.button("Hint", key=f"btn_hint_{idx}", use_container_width=True):
                    st.session_state[hint_key] = not st.session_state[hint_key]
            with c2:
                if st.button("Show solution", key=f"btn_sol_{idx}", use_container_width=True):
                    st.session_state[sol_key] = not st.session_state[sol_key]

            if st.session_state[hint_key]:
                st.info(item.hint_md)

            if st.session_state[sol_key]:
                st.success(item.solution_md)


# -----------------------------
# Main render
# -----------------------------
def render():
    st.header("Subtopic 5.6: Overview of Curve Sketching")

    tabs = st.tabs(["Learn", "Practice"])
    with tabs[0]:
        render_learn()
    with tabs[1]:
        render_practice()
