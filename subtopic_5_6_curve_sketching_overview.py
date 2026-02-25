# subtopic_5_6_curve_sketching_overview.py
import math
import importlib
from typing import Callable, Optional, Dict, Any, List

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# LaTeX / "humanised" helpers
# ----------------------------
def _latex_block(tex: str) -> None:
    """Render display math reliably."""
    tex = tex.strip()
    if not tex:
        return
    st.markdown(f"$$\n{tex}\n$$")


def _latex_inline(text: str) -> str:
    """Wrap a string for inline LaTeX inside markdown."""
    return f"${text}$"


def _md(text: str) -> None:
    st.markdown(text)


def _section(title: str) -> None:
    st.markdown(f"### {title}")


def _small_plot(x, y, title: str, vlines=None, hlines=None, xlim=None, ylim=None):
    """Small, readable plot (no huge charts)."""
    fig = plt.figure(figsize=(5.2, 3.2), dpi=160)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
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

    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    st.pyplot(fig, clear_figure=True)


# ---------------------------------------------------
# simulations.py integration (AUTO-DETECT function)
# ---------------------------------------------------
_BOARD_NAME_CANDIDATES = [
    "render_board_simulator",
    "render_blackboard_simulator",
    "board_simulator",
    "blackboard_simulator",
    "render_simulation_board",
    "render_board",
    "render_blackboard",
]


def _find_board_function() -> Optional[Callable[..., Any]]:
    """
    Robustly find the board simulator function inside simulations.py.
    - First tries known names.
    - If not found, searches for ANY callable with 'board' in the name.
    """
    try:
        sims = importlib.import_module("simulations")
    except Exception:
        return None

    # 1) Try known names (backward compatible with your earlier modules)
    for name in _BOARD_NAME_CANDIDATES:
        fn = getattr(sims, name, None)
        if callable(fn):
            return fn

    # 2) Auto-detect: any callable containing 'board' in its name
    for name in dir(sims):
        if "board" in name.lower():
            fn = getattr(sims, name, None)
            if callable(fn):
                return fn

    return None


def _render_board_from_simulations(payload: Dict[str, Any]) -> bool:
    """
    Calls your simulations.py board if available.
    payload: a dict with whatever keys your board expects.
    Returns True if a board was rendered, else False.
    """
    fn = _find_board_function()
    if fn is None:
        st.warning(
            "Board simulator is not available (simulations.py not found or no board function detected)."
        )
        return False

    # We DO NOT assume a strict signature. We try common calling patterns.
    try:
        # Pattern A: board(payload_dict)
        fn(payload)
        return True
    except TypeError:
        pass
    except Exception:
        # If it exists but crashed, show a clean error.
        st.error("Board simulator was found but failed to render for this example.")
        return False

    try:
        # Pattern B: board(**payload)
        fn(**payload)
        return True
    except TypeError:
        pass
    except Exception:
        st.error("Board simulator was found but failed to render for this example.")
        return False

    # If function exists but expects something else
    st.warning(
        "Your simulations.py board function was detected, but its parameters don't match what this subtopic provides."
    )
    return False


# ---------------------------------------
# Guided "no-slider" step visualiser
# ---------------------------------------
def _step_player(key: str, steps_latex: List[str], title: str = "Step-by-step solution"):
    """
    Button-based stepper (no sliders). Shows LaTeX lines gradually.
    """
    if key not in st.session_state:
        st.session_state[key] = 0

    st.markdown(f"**{title}**")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("◀ Previous", key=f"{key}_prev", use_container_width=True):
            st.session_state[key] = max(0, st.session_state[key] - 1)
    with col2:
        if st.button("Next ▶", key=f"{key}_next", use_container_width=True):
            st.session_state[key] = min(len(steps_latex), st.session_state[key] + 1)
    with col3:
        if st.button("Reset", key=f"{key}_reset", use_container_width=True):
            st.session_state[key] = 0

    shown = steps_latex[: st.session_state[key]]
    if not shown:
        st.info("Press **Next** to start the solution.")
        return

    for line in shown:
        _latex_block(line)


# ---------------------------------------
# Content: Objectives (exact scope)
# ---------------------------------------
def _render_objectives():
    st.markdown("### Learning objectives (Subtopic 5.6)")
    st.markdown(
        "- **5.6.1** Recall finding horizontal and vertical asymptotes of a rational function.\n"
        "- **5.6.2** Follow a clear **curve sketching workflow** (domain, \(f'(x)\), \(f''(x)\), asymptotes, key points, sketch).\n"
        "- **5.6.3** Sketch curves for: polynomials, rational functions, fractional powers/radicals, and trig/exp/log components."
    )


# ---------------------------------------
# Examples (from Chapter 3 / Section 3.6)
# ---------------------------------------
def _examples_catalog() -> Dict[str, Dict[str, Any]]:
    """
    Each example provides:
    - label
    - function (as LaTeX)
    - small plot config
    - board_payload: content to feed simulations.py if it supports it
    - stepper steps (fallback if board can't render)
    """
    return {
        "ex6_1_poly": {
            "label": "Example 6.1 (Polynomial)",
            "fx_tex": r"f(x)=x^{4}+6x^{3}+12x^{2}+8x+1",
            "plot": {
                "xmin": -4,
                "xmax": 1,
                "title": "Example 6.1: polynomial shape (small view)",
            },
            "board_payload": {
                "title": "Example 6.1 (Polynomial)",
                "solution_latex": [
                    r"\textbf{Given } f(x)=x^{4}+6x^{3}+12x^{2}+8x+1",
                    r"f'(x)=4x^{3}+18x^{2}+24x+8",
                    r"f''(x)=12x^{2}+36x+24",
                    r"\text{Use } f'(x)=0 \text{ to find critical points.}",
                    r"\text{Use } f''(x)=0 \text{ to find possible inflection points.}",
                    r"\text{Then use sign tests on intervals to determine increasing/decreasing and concavity.}",
                ],
            },
            "steps": [
                r"\textbf{Given } f(x)=x^{4}+6x^{3}+12x^{2}+8x+1",
                r"f'(x)=4x^{3}+18x^{2}+24x+8",
                r"f''(x)=12x^{2}+36x+24",
                r"\text{Solve } f'(x)=0 \text{ (critical points).}",
                r"\text{Solve } f''(x)=0 \text{ (possible inflection points).}",
                r"\text{Make interval sign tests and then sketch with the key points.}",
            ],
        },
        "ex6_2_rational": {
            "label": "Example 6.2 (Rational with asymptotes)",
            "fx_tex": r"f(x)=\dfrac{x^{2}-3}{x^{3}}",
            "plot": {"xmin": -4, "xmax": 4, "title": "Example 6.2: rational (small view)"},
            "board_payload": {
                "title": "Example 6.2 (Rational with asymptotes)",
                "solution_latex": [
                    r"\textbf{Given } f(x)=\dfrac{x^{2}-3}{x^{3}}",
                    r"\textbf{Domain: } x\neq 0",
                    r"\textbf{Vertical asymptote: } x=0",
                    r"\textbf{Horizontal asymptote: } y=0 \quad (\text{degree in numerator }<\text{degree in denominator})",
                    r"\text{Then use } f'(x), f''(x) \text{ to refine the shape and turning/inflection behavior.}",
                ],
            },
            "steps": [
                r"\textbf{Given } f(x)=\dfrac{x^{2}-3}{x^{3}}",
                r"\textbf{Domain: } x\neq 0",
                r"\textbf{Vertical asymptote: } x=0",
                r"\textbf{Horizontal asymptote: } y=0",
                r"\text{Compute } f'(x)\text{ and use sign of } f'(x) \text{ for increasing/decreasing.}",
                r"\text{Compute } f''(x)\text{ and use sign of } f''(x) \text{ for concavity / inflection.}",
            ],
        },
        "ex6_3_two_vasym": {
            "label": "Example 6.3 (Two vertical asymptotes)",
            "fx_tex": r"f(x)=\dfrac{x^{2}}{x^{2}-4}",
            "plot": {
                "xmin": -5,
                "xmax": 5,
                "title": "Example 6.3: two vertical asymptotes (small view)",
                "vlines": [-2, 2],
                "hlines": [1],
            },
            "board_payload": {
                "title": "Example 6.3 (Two vertical asymptotes)",
                "solution_latex": [
                    r"\textbf{Given } f(x)=\dfrac{x^{2}}{x^{2}-4}",
                    r"\textbf{Domain: } x\neq \pm 2",
                    r"\textbf{Vertical asymptotes: } x=-2,\; x=2",
                    r"\textbf{Horizontal asymptote: } y=1",
                    r"\text{Then use } f'(x)\text{ (increasing/decreasing) and } f''(x)\text{ (concavity).}",
                ],
            },
            "steps": [
                r"\textbf{Given } f(x)=\dfrac{x^{2}}{x^{2}-4}",
                r"\textbf{Domain: } x\neq \pm 2",
                r"\textbf{Vertical asymptotes: } x=-2,\; x=2",
                r"\textbf{Horizontal asymptote: } y=1",
                r"\text{Compute } f'(x)\text{ and complete a sign chart.}",
                r"\text{Compute } f''(x)\text{ and complete concavity intervals.}",
                r"\text{Combine all information to produce the final sketch.}",
            ],
        },
        "ex6_4_hidden_behavior": {
            "label": "Example 6.4 (Rational: important feature hidden in default window)",
            "fx_tex": r"f(x)=\dfrac{1}{x^{3}+3x^{2}+3x+3}",
            "plot": {"xmin": -6, "xmax": 6, "title": "Example 6.4: rational (small view)"},
            "board_payload": {
                "title": "Example 6.4 (Rational: hidden behavior)",
                "solution_latex": [
                    r"\textbf{Given } f(x)=\dfrac{1}{x^{3}+3x^{2}+3x+3}",
                    r"\textbf{Domain: } x^{3}+3x^{2}+3x+3\neq 0",
                    r"\textbf{Vertical asymptotes: } \text{real roots of the denominator}",
                    r"\textbf{Horizontal asymptote: } y=0 \quad (\text{degree denominator }>\text{degree numerator})",
                    r"\text{Then use } f'(x), f''(x) \text{ to refine turning and concavity.}",
                ],
            },
            "steps": [
                r"\textbf{Given } f(x)=\dfrac{1}{x^{3}+3x^{2}+3x+3}",
                r"\text{Find where } x^{3}+3x^{2}+3x+3=0 \text{ (vertical asymptote candidates).}",
                r"\textbf{Horizontal asymptote: } y=0",
                r"\text{Compute } f'(x) \text{ for increasing/decreasing.}",
                r"\text{Compute } f''(x) \text{ for concavity/inflection.}",
            ],
        },
        "ex6_5_exponential": {
            "label": "Example 6.5 (Exponential component)",
            "fx_tex": r"f(x)=e^{1/x}",
            "plot": {"xmin": -4, "xmax": 4, "title": "Example 6.5: exponential (small view)"},
            "board_payload": {
                "title": "Example 6.5 (Exponential component)",
                "solution_latex": [
                    r"\textbf{Given } f(x)=e^{1/x}",
                    r"\textbf{Domain: } x\neq 0",
                    r"\textbf{Vertical asymptote behavior near } x=0 \text{ (one-sided)}",
                    r"\textbf{Horizontal asymptote: } y=1 \text{ as } x\to \pm\infty",
                    r"\text{Then use } f'(x), f''(x) \text{ to confirm monotonicity and concavity.}",
                ],
            },
            "steps": [
                r"\textbf{Given } f(x)=e^{1/x}",
                r"\textbf{Domain: } x\neq 0",
                r"\lim_{x\to \infty} e^{1/x}=e^{0}=1 \Rightarrow \textbf{horizontal asymptote } y=1",
                r"\lim_{x\to -\infty} e^{1/x}=1 \Rightarrow \textbf{horizontal asymptote } y=1",
                r"\text{Near } x=0: \; \lim_{x\to 0^{+}} e^{1/x}=+\infty,\;\; \lim_{x\to 0^{-}} e^{1/x}=0",
                r"\text{Compute } f'(x), f''(x) \text{ to refine shape.}",
            ],
        },
        "ex6_6_trig": {
            "label": "Example 6.6 (Trig + polynomial component)",
            "fx_tex": r"f(x)=\cos x - x",
            "plot": {"xmin": -6, "xmax": 6, "title": "Example 6.6: trig + line (small view)"},
            "board_payload": {
                "title": "Example 6.6 (Trig + polynomial component)",
                "solution_latex": [
                    r"\textbf{Given } f(x)=\cos x - x",
                    r"f'(x)=-\sin x - 1 \le 0 \Rightarrow \textbf{decreasing on all } \mathbb{R}",
                    r"f''(x)=-\cos x \Rightarrow \textbf{concavity changes when } \cos x=0",
                    r"\cos x=0 \Rightarrow x=\dfrac{\pi}{2}+k\pi",
                    r"\text{Use these to sketch a smooth decreasing curve crossing the line behavior.}",
                ],
            },
            "steps": [
                r"\textbf{Given } f(x)=\cos x - x",
                r"f'(x)=-\sin x - 1",
                r"-1\le \sin x \le 1 \Rightarrow -2\le -\sin x -1 \le 0 \Rightarrow f'(x)\le 0",
                r"\Rightarrow \textbf{The function is decreasing for all } x",
                r"f''(x)=-\cos x",
                r"\cos x=0 \Rightarrow x=\dfrac{\pi}{2}+k\pi \Rightarrow \textbf{possible inflection points}",
            ],
        },
    }


def _render_board_simulator_block():
    """
    Student-facing board simulator selector.
    - Works even if board function name differs (auto-detect).
    - Uses button (no sliders).
    """
    cat = _examples_catalog()
    st.markdown("### Board simulator (full solution on one board)")
    st.markdown(
        "Choose an example, then press **Play solution** to watch the solution appear on the same board."
    )

    labels = [(k, v["label"]) for k, v in cat.items()]
    key_to_label = {k: lbl for k, lbl in labels}

    # Keep selection stable
    selected = st.radio(
        "Choose an example for the board",
        options=[k for k, _ in labels],
        format_func=lambda k: key_to_label[k],
        horizontal=True,
        key="st56_board_choice",
    )

    colA, colB = st.columns([2, 2])
    with colA:
        play = st.button("Play solution", use_container_width=True, key="st56_board_play")
    with colB:
        reset = st.button("Reset", use_container_width=True, key="st56_board_reset")

    if reset:
        st.session_state["st56_board_played"] = False

    if "st56_board_played" not in st.session_state:
        st.session_state["st56_board_played"] = False

    if play:
        st.session_state["st56_board_played"] = True

    if not st.session_state["st56_board_played"]:
        st.info("Press **Play solution** to display the solution board.")
        return

    ex = cat[selected]
    payload = ex.get("board_payload", {}) or {}

    # If simulations.py board exists, it will render.
    rendered = _render_board_from_simulations(payload)

    # Fallback: show our own step-player board
    if not rendered:
        st.markdown("---")
        st.markdown("#### Solution (step-by-step)")
        _step_player(
            key=f"st56_fallback_{selected}",
            steps_latex=ex.get("steps", []),
            title="Follow the solution step-by-step",
        )


# ---------------------------------------
# Workflow (Objective 5.6.2)
# ---------------------------------------
def _render_workflow():
    _section("Curve sketching workflow (what to do every time)")
    st.markdown(
        "When you sketch a curve in an exam, you are not guessing. You follow a fixed workflow:"
    )

    st.markdown(
        "1) **Domain** (where is the function defined?)  \n"
        "2) **Intercepts** (x- and y-intercepts if they exist)  \n"
        "3) **Asymptotes** (vertical + horizontal/oblique for rational forms)  \n"
        "4) **First derivative** \(f'(x)\): increasing/decreasing → local max/min  \n"
        "5) **Second derivative** \(f''(x)\): concave up/down → inflection points  \n"
        "6) **Combine** all key information → draw a clean final sketch"
    )

    st.markdown("#### Mini checklist (exam-ready)")
    st.markdown(
        "- Write the **domain restrictions** clearly.\n"
        "- Mark **vertical asymptotes** as dashed lines and check left/right behavior.\n"
        "- State the **horizontal asymptote** (if it exists) and how the graph approaches it.\n"
        "- Use sign tests for \(f'(x)\) and \(f''(x)\) on intervals.\n"
        "- Add key points (intercepts, turning points, inflection points).\n"
        "- Sketch with correct end behavior and asymptote behavior."
    )


# ---------------------------------------
# Objective 5.6.1: Asymptotes (rational)
# ---------------------------------------
def _render_asymptotes():
    _section("Asymptotes of rational functions (recall)")
    st.markdown(
        "For a rational function \(f(x)=\\dfrac{p(x)}{q(x)}\), asymptotes come from the denominator and the degrees."
    )

    st.markdown("#### Vertical asymptotes")
    st.markdown(
        "- Solve \(q(x)=0\). Any real solution gives a **vertical asymptote candidate**.\n"
        "- Confirm by checking one-sided limits:"
    )
    _latex_block(r"\lim_{x\to a^-} f(x)\quad \text{and}\quad \lim_{x\to a^+} f(x)")

    st.markdown("#### Horizontal asymptotes (degree comparison)")
    st.markdown(
        "- If \(\deg(p)<\deg(q)\), then \(y=0\).\n"
        "- If \(\deg(p)=\deg(q)\), then \(y=\dfrac{\text{leading coefficient of }p}{\text{leading coefficient of }q}\).\n"
        "- If \(\deg(p)>\deg(q)\), there is **no horizontal asymptote** (you may get an oblique/other asymptote, depending on division)."
    )


# ---------------------------------------
# Examples with SMALL plots
# ---------------------------------------
def _render_examples():
    _section("Worked examples (guided, within the objectives)")

    cat = _examples_catalog()
    for ex_key in ["ex6_1_poly", "ex6_2_rational", "ex6_3_two_vasym", "ex6_5_exponential", "ex6_6_trig"]:
        ex = cat[ex_key]
        st.markdown(f"#### {ex['label']}")
        st.markdown("**Function:**")
        _latex_block(ex["fx_tex"])

        # small plot
        cfg = ex.get("plot", {})
        xmin, xmax = cfg.get("xmin", -4), cfg.get("xmax", 4)
        xs = np.linspace(xmin, xmax, 800)

        # safe y compute
        def safe_f(x):
            if ex_key == "ex6_1_poly":
                return x**4 + 6*x**3 + 12*x**2 + 8*x + 1
            if ex_key == "ex6_2_rational":
                return (x**2 - 3) / (x**3)
            if ex_key == "ex6_3_two_vasym":
                return (x**2) / (x**2 - 4)
            if ex_key == "ex6_5_exponential":
                return np.exp(1/x)
            if ex_key == "ex6_6_trig":
                return np.cos(x) - x
            return np.nan

        ys = np.array([np.nan]*len(xs), dtype=float)
        for i, xv in enumerate(xs):
            try:
                # avoid division by 0 explosions
                if ex_key in ("ex6_2_rational", "ex6_5_exponential") and abs(xv) < 1e-6:
                    ys[i] = np.nan
                elif ex_key == "ex6_3_two_vasym" and abs(xv-2) < 1e-6:
                    ys[i] = np.nan
                elif ex_key == "ex6_3_two_vasym" and abs(xv+2) < 1e-6:
                    ys[i] = np.nan
                else:
                    yv = safe_f(xv)
                    # clamp extreme values so plot stays readable
                    if not np.isfinite(yv) or abs(yv) > 200:
                        ys[i] = np.nan
                    else:
                        ys[i] = yv
            except Exception:
                ys[i] = np.nan

        _small_plot(
            xs,
            ys,
            title=cfg.get("title", ex["label"]),
            vlines=cfg.get("vlines"),
            hlines=cfg.get("hlines"),
            xlim=(xmin, xmax),
        )

        st.markdown("**Guided solution (press Next to reveal steps):**")
        _step_player(
            key=f"st56_steps_{ex_key}",
            steps_latex=ex.get("steps", []),
            title="Step-by-step (no guessing)",
        )

        st.markdown("---")


# ---------------------------------------
# Practice (20+ questions, hint + solution)
# ---------------------------------------
def _practice_questions() -> List[Dict[str, str]]:
    """
    All questions stay within objectives:
    - asymptotes (vertical/horizontal)
    - workflow components (domain, intercepts, f', f'', increasing/concave)
    - sketch different types (poly, rational, exp, trig)
    """
    return [
        {
            "q": r"\text{For } f(x)=\dfrac{x^{2}-3}{x^{3}},\text{ state the domain.}",
            "hint": r"\text{The denominator cannot be }0.",
            "sol": r"\text{Domain: } x\neq 0 \;\Rightarrow\; (-\infty,0)\cup(0,\infty).",
        },
        {
            "q": r"\text{For } f(x)=\dfrac{x^{2}-3}{x^{3}},\text{ find the vertical asymptote.}",
            "hint": r"\text{Vertical asymptotes come from } x^{3}=0.",
            "sol": r"x=0 \text{ is a vertical asymptote.}",
        },
        {
            "q": r"\text{For } f(x)=\dfrac{x^{2}-3}{x^{3}},\text{ find the horizontal asymptote.}",
            "hint": r"\deg(\text{numerator})<\deg(\text{denominator})",
            "sol": r"y=0.",
        },
        {
            "q": r"\text{For } f(x)=\dfrac{x^{2}}{x^{2}-4},\text{ state the domain.}",
            "hint": r"x^{2}-4\neq 0.",
            "sol": r"x\neq \pm 2\;\Rightarrow\; (-\infty,-2)\cup(-2,2)\cup(2,\infty).",
        },
        {
            "q": r"\text{For } f(x)=\dfrac{x^{2}}{x^{2}-4},\text{ list the vertical asymptotes.}",
            "hint": r"x^{2}-4=0\Rightarrow x=\pm 2.",
            "sol": r"x=-2,\; x=2.",
        },
        {
            "q": r"\text{For } f(x)=\dfrac{x^{2}}{x^{2}-4},\text{ find the horizontal asymptote.}",
            "hint": r"\deg(\text{numerator})=\deg(\text{denominator})",
            "sol": r"y=\dfrac{1}{1}=1.",
        },
        {
            "q": r"\text{For } f(x)=e^{1/x},\text{ state the domain.}",
            "hint": r"\text{The exponent }1/x\text{ must be defined.}",
            "sol": r"x\neq 0.",
        },
        {
            "q": r"\text{For } f(x)=e^{1/x},\text{ evaluate } \lim_{x\to \infty} f(x).",
            "hint": r"1/x\to 0.",
            "sol": r"\lim_{x\to \infty} e^{1/x}=e^{0}=1.",
        },
        {
            "q": r"\text{For } f(x)=e^{1/x},\text{ describe } \lim_{x\to 0^{+}} f(x).",
            "hint": r"1/x\to +\infty.",
            "sol": r"\lim_{x\to 0^{+}} e^{1/x}=+\infty.",
        },
        {
            "q": r"\text{For } f(x)=e^{1/x},\text{ describe } \lim_{x\to 0^{-}} f(x).",
            "hint": r"1/x\to -\infty.",
            "sol": r"\lim_{x\to 0^{-}} e^{1/x}=0.",
        },
        {
            "q": r"\text{For } f(x)=\cos x-x,\text{ find } f'(x).",
            "hint": r"\dfrac{d}{dx}(\cos x)=-\sin x.",
            "sol": r"f'(x)=-\sin x-1.",
        },
        {
            "q": r"\text{For } f(x)=\cos x-x,\text{ explain why } f(x)\text{ is decreasing for all }x.",
            "hint": r"-1\le \sin x \le 1.",
            "sol": r"-1\le \sin x\le 1 \Rightarrow -2\le -\sin x-1\le 0 \Rightarrow f'(x)\le 0 \Rightarrow \text{decreasing}.",
        },
        {
            "q": r"\text{For } f(x)=\cos x-x,\text{ find } f''(x).",
            "hint": r"\dfrac{d}{dx}(-\sin x)=-\cos x.",
            "sol": r"f''(x)=-\cos x.",
        },
        {
            "q": r"\text{For } f(x)=\cos x-x,\text{ give the }x\text{-values where concavity can change.}",
            "hint": r"f''(x)=0 \Rightarrow \cos x=0.",
            "sol": r"\cos x=0 \Rightarrow x=\dfrac{\pi}{2}+k\pi,\;k\in\mathbb{Z}.",
        },
        {
            "q": r"\text{For } f(x)=\dfrac{1}{x^{3}+3x^{2}+3x+3},\text{ state the horizontal asymptote.}",
            "hint": r"\deg(\text{denominator})>\deg(\text{numerator})",
            "sol": r"y=0.",
        },
        {
            "q": r"\text{For } f(x)=x^{4}+6x^{3}+12x^{2}+8x+1,\text{ write } f'(x).",
            "hint": r"\text{Differentiate term-by-term.}",
            "sol": r"f'(x)=4x^{3}+18x^{2}+24x+8.",
        },
        {
            "q": r"\text{For } f(x)=x^{4}+6x^{3}+12x^{2}+8x+1,\text{ write } f''(x).",
            "hint": r"\text{Differentiate } f'(x).",
            "sol": r"f''(x)=12x^{2}+36x+24.",
        },
        {
            "q": r"\text{Workflow check: if } f'(c)=0 \text{ and } f''(c)>0,\text{ what do you conclude?}",
            "hint": r"\text{Second Derivative Test.}",
            "sol": r"\text{Local minimum at } x=c.",
        },
        {
            "q": r"\text{Workflow check: if } f'(c)=0 \text{ and } f''(c)<0,\text{ what do you conclude?}",
            "hint": r"\text{Second Derivative Test.}",
            "sol": r"\text{Local maximum at } x=c.",
        },
        {
            "q": r"\text{Workflow check: if } f''(x)>0 \text{ on an interval, what is the concavity?}",
            "hint": r"\text{Think: slopes increasing.}",
            "sol": r"\text{Concave up.}",
        },
        {
            "q": r"\text{Workflow check: if } f''(x)<0 \text{ on an interval, what is the concavity?}",
            "hint": r"\text{Think: slopes decreasing.}",
            "sol": r"\text{Concave down.}",
        },
    ]


def _render_practice():
    st.markdown("### Practice (Hint + Show solution)")
    st.markdown(
        "Work through the questions. Use **Hint** only if needed, then check **Show solution**."
    )

    qs = _practice_questions()
    # Ensure we have at least 20
    if len(qs) < 20:
        st.warning("Practice bank is below 20 questions (please notify).")

    for i, item in enumerate(qs, start=1):
        st.markdown(f"#### Question {i}")
        _latex_block(item["q"])

        c1, c2 = st.columns([1, 1])
        with c1:
            with st.expander("Hint", expanded=False):
                _latex_block(item["hint"])
        with c2:
            with st.expander("Show solution", expanded=False):
                _latex_block(item["sol"])

        st.markdown("---")


# ---------------------------------------
# Main render()
# ---------------------------------------
def render():
    # Only Learn + Practice tabs (as requested)
    tab_learn, tab_practice = st.tabs(["Learn", "Practice"])

    with tab_learn:
        _render_objectives()
        st.markdown("---")

        _render_workflow()
        st.markdown("---")

        _render_asymptotes()
        st.markdown("---")

        # Board simulator FIRST (students see full worked solution quickly)
        _render_board_simulator_block()
        st.markdown("---")

        _render_examples()

    with tab_practice:
        _render_practice()
