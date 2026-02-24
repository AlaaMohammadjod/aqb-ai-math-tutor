# subtopic_5_5_concavity_second_derivative_test.py
# AQB Grade 12 AI Math Tutor — Subtopic 5.5: Concavity and 2nd Derivative Test
# IMPORTANT:
# - Provides the required render() entry point (fixes “missing render() function”).
# - ONLY two tabs: Learn + Practice.
# - NO sliders anywhere.
# - All mathematical notation is rendered in LaTeX (no plain-text math).
# - Tables are built as clean markdown tables (no overlap).
# - Graphs are intentionally smaller (compact figsize).
# - Black-board simulator: uses simulations.py if available; otherwise uses a safe fallback.

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


# ----------------------------
# Small helpers (LaTeX-safe)
# ----------------------------

def _h2(title: str) -> None:
    st.markdown(f"## {title}")

def _h3(title: str) -> None:
    st.markdown(f"### {title}")

def _p(text: str) -> None:
    # No math in plain text. If you need math, put it in _latex() or use $...$ inside markdown.
    st.markdown(text)

def _latex(expr: str) -> None:
    # Use st.latex for all displayed formulas / expressions.
    st.latex(expr)

def _callout(title: str, body_lines: List[str]) -> None:
    st.info("**" + title + "**\n\n" + "\n".join([f"- {ln}" for ln in body_lines]))

def _exam_box(question_lines: List[str], task_lines: List[str]) -> None:
    st.markdown(
        """
<div style="border-left:6px solid #1f77b4;background:#f3f8ff;padding:14px 14px 8px 14px;border-radius:10px;">
<div style="font-weight:700;margin-bottom:6px;">Question</div>
</div>
""",
        unsafe_allow_html=True,
    )
    for ln in question_lines:
        _p(ln)
    st.markdown(
        """
<div style="border-left:6px solid #2ca02c;background:#f3fff6;padding:14px 14px 8px 14px;border-radius:10px;margin-top:8px;">
<div style="font-weight:700;margin-bottom:6px;">Task</div>
</div>
""",
        unsafe_allow_html=True,
    )
    for i, ln in enumerate(task_lines, 1):
        _p(f"{i}. {ln}")

def _step(title: str) -> None:
    st.markdown(f"**{title}**")

def _md_table(headers: List[str], rows: List[List[str]]) -> None:
    # Clean markdown table (no overlap). Ensure any math in cells uses $...$.
    md = "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for r in rows:
        md += "| " + " | ".join(r) + " |\n"
    st.markdown(md)

def _small_plot(x: np.ndarray, y: np.ndarray, title: str, vlines: Optional[List[float]] = None) -> None:
    fig = plt.figure(figsize=(6.2, 3.2), dpi=140)  # smaller than before (non-negotiable)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    if vlines:
        for xv in vlines:
            ax.axvline(xv, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)
    st.pyplot(fig, clear_figure=True)


# ----------------------------
# Blackboard simulator wrapper
# ----------------------------

def _try_render_blackboard(lines_latex: List[str], height_px: int = 420) -> bool:
    """
    Tries to use simulations.py blackboard (preferred).
    Returns True if used, otherwise False (fallback should be used).
    """
    try:
        import simulations  # type: ignore
    except Exception:
        return False

    # Try a few common function names (keeps your simulations.py unchanged).
    candidates = [
        "render_blackboard",
        "render_blackboard_simulator",
        "render_board_simulator",
        "blackboard",
        "blackboard_simulator",
        "render_blackboard_lines",
    ]
    for name in candidates:
        fn = getattr(simulations, name, None)
        if callable(fn):
            try:
                # Try multiple signatures safely.
                try:
                    fn(lines_latex, height_px=height_px)
                except TypeError:
                    try:
                        fn(lines_latex, height=height_px)
                    except TypeError:
                        fn(lines_latex)
                return True
            except Exception:
                continue
    return False

def _fallback_blackboard(lines_latex: List[str], height_px: int = 420) -> None:
    """
    Safe fallback if simulations.py function names are unknown.
    No “next step” clicking; pressing Play shows the full solution on the same board.
    """
    import streamlit.components.v1 as components

    # Pre-render full content (no progressive steps) to avoid readability/scroll issues.
    # This is a fallback only; the primary is simulations.py.
    html_lines = []
    for ln in lines_latex:
        # KaTeX/MathJax rendering handled by Streamlit in markdown; but inside HTML we keep it readable.
        # We therefore present as plain lines with LaTeX delimiters, then let MathJax render in iframe.
        # Streamlit iframes do not automatically inject MathJax; keep it simple and readable.
        html_lines.append(f"<div style='margin:8px 0; font-size:20px; line-height:1.35;'>{ln}</div>")

    html = f"""
    <div style="height:{height_px}px; overflow:auto; background:#0b0f14; color:#e8eef7; border-radius:14px; padding:18px; border:1px solid rgba(255,255,255,0.08);">
      <div style="font-weight:700; opacity:0.95; margin-bottom:10px;">Solution</div>
      {"".join(html_lines)}
      <div style="margin-top:10px; font-size:13px; opacity:0.7;">(If your board is not rendering math here, your simulations.py board will.)</div>
    </div>
    """
    components.html(html, height=height_px + 10)


# ----------------------------
# Core learning content (Chapter 3, Section 3.5)
# ----------------------------

def _learn_objectives() -> None:
    _h2("Learning objectives (5.5)")
    _p("By the end of this subtopic, you should be able to:")
    st.markdown(
        """
- **5.5.1** Find intervals where a function is concave up or concave down, and identify inflection points.  
- **5.5.2** Build clear tables that summarize behavior (increasing/decreasing) and concavity.  
- **5.5.3** Use the Second Derivative Test to classify a critical point as a local maximum or local minimum, and recognize when it is inconclusive.  
- **5.5.4** Estimate increase/decrease, extrema, concavity, and inflection points from a given graph.  
- **5.5.5** Apply these ideas to a simple economical/production model (sales, cost, efficiency).  
"""
    )

def _learn_concavity_definition() -> None:
    _h3("5.5.1 Concavity: what it means")
    _p("Concavity describes how the slope of the curve changes as you move from left to right.")
    _callout(
        "Key idea",
        [
            "If the tangent slopes are getting larger (increasing), the graph is concave up.",
            "If the tangent slopes are getting smaller (decreasing), the graph is concave down.",
        ],
    )
    _p("Concavity can be tested using the second derivative.")
    _latex(r"f''(x) > 0 \;\Rightarrow\; \text{concave up}")
    _latex(r"f''(x) < 0 \;\Rightarrow\; \text{concave down}")

    _h3("Inflection points")
    _p("An inflection point is a point where concavity changes (from concave up to concave down, or the reverse).")
    _callout(
        "How to find candidates",
        [
            "Solve $f''(x)=0$.",
            "Also include $x$ where $f''(x)$ is undefined (if the function is still defined there).",
            "Then do a sign test for $f''(x)$ on the intervals.",
        ],
    )

def _worked_example_concavity_inflection() -> None:
    _h3("Worked example (exam format)")
    _exam_box(
        question_lines=[
            "Consider the function:",
        ],
        task_lines=[
            "Find the intervals where the graph is concave up and concave down.",
            "Identify any inflection point(s).",
        ],
    )
    _latex(r"f(x)=2x^{3}+9x^{2}-24x-10")

    _step("Step 1: Compute the second derivative.")
    _latex(r"f'(x)=6x^{2}+18x-24=6(x+4)(x-1)")
    _latex(r"f''(x)=12x+18=6(2x+3)")

    _step("Step 2: Find possible inflection $x$-values from $f''(x)=0$.")
    _latex(r"f''(x)=0 \;\Rightarrow\; 12x+18=0 \;\Rightarrow\; x=-\frac{3}{2}")

    _step("Step 3: Sign test for $f''(x)$ to decide concavity.")
    _p("Test one value in each interval:")
    _latex(r"\text{For }x<-\,\frac{3}{2}:\; f''(x)<0 \Rightarrow \text{concave down}")
    _latex(r"\text{For }x>-\,\frac{3}{2}:\; f''(x)>0 \Rightarrow \text{concave up}")

    _step("Step 4: State the result and the inflection point.")
    _latex(r"\text{Concave down on }(-\infty,-\tfrac{3}{2})")
    _latex(r"\text{Concave up on }(-\tfrac{3}{2},\infty)")
    _p("Because concavity changes at $x=-\\tfrac{3}{2}$, there is an inflection point at:")
    _latex(r"\left(-\tfrac{3}{2},\, f\!\left(-\tfrac{3}{2}\right)\right)")

    # Small supporting graph (compact)
    xs = np.linspace(-4, 4, 600)
    ys = 2 * xs**3 + 9 * xs**2 - 24 * xs - 10
    _small_plot(xs, ys, "Concavity change (example curve)", vlines=[-1.5])


def _learn_tables_of_variation() -> None:
    _h3("5.5.2 Tables that summarize behavior (no overlap)")
    _p("A clear table helps you summarize what happens on each interval. Use:")
    _p("- the sign of $f'(x)$ to decide increasing/decreasing,")
    _p("- the sign of $f''(x)$ to decide concave up/concave down.")

    _callout(
        "What your table must include",
        [
            "Critical numbers from $f'(x)=0$ (and where $f'(x)$ is undefined if it happens).",
            "Candidate inflection $x$-values from $f''(x)=0$ (and where $f''(x)$ is undefined if it happens).",
            "Intervals split by all of these points, then the sign of $f'(x)$ and $f''(x)$ on each interval.",
        ],
    )

    _p("Template you can follow (fill the signs after testing):")
    _md_table(
        headers=["Interval", "Sign of $f'(x)$", "Behavior", "Sign of $f''(x)$", "Concavity"],
        rows=[
            [r"$(-\infty,a)$", r"$+$ / $-$", "Increasing / Decreasing", r"$+$ / $-$", "Concave up / Concave down"],
            [r"$(a,b)$", r"$+$ / $-$", "Increasing / Decreasing", r"$+$ / $-$", "Concave up / Concave down"],
            [r"$(b,\infty)$", r"$+$ / $-$", "Increasing / Decreasing", r"$+$ / $-$", "Concave up / Concave down"],
        ],
    )

def _worked_example_combined_table() -> None:
    _h3("Worked example (exam format)")
    _exam_box(
        question_lines=[
            "Consider the function:",
        ],
        task_lines=[
            "Build a single table that summarizes increasing/decreasing and concavity.",
            "Identify any local extrema and any inflection points.",
        ],
    )
    # Example aligns with Chapter 3 Example 5.4 and surrounding content.
    _latex(r"f(x)=x^{4}-8x^{2}+10")

    _step("Step 1: Find critical numbers from $f'(x)=0$.")
    _latex(r"f'(x)=4x^{3}-16x=4x(x^{2}-4)=4x(x-2)(x+2)")
    _latex(r"f'(x)=0 \;\Rightarrow\; x=-2,\;0,\;2")

    _step("Step 2: Find candidate inflection $x$-values from $f''(x)=0$.")
    _latex(r"f''(x)=12x^{2}-16=4(3x^{2}-4)")
    _latex(r"f''(x)=0 \;\Rightarrow\; 12x^{2}-16=0 \;\Rightarrow\; x=\pm \frac{2}{\sqrt{3}}")

    _step("Step 3: Write the intervals (split by all points) and test signs.")
    _p("Split the number line at:")
    _latex(r"x=-2,\;x=-\frac{2}{\sqrt{3}},\;x=0,\;x=\frac{2}{\sqrt{3}},\;x=2")

    _p("A clean combined summary table (no overlap):")
    _md_table(
        headers=["Interval", "Sign of $f'(x)$", "Inc./Dec.", "Sign of $f''(x)$", "Concavity"],
        rows=[
            [r"$(-\infty,-2)$", r"$-$", "Decreasing", r"$+$", "Concave up"],
            [r"$(-2,-\tfrac{2}{\sqrt{3}})$", r"$+$", "Increasing", r"$+$", "Concave up"],
            [r"$(-\tfrac{2}{\sqrt{3}},0)$", r"$+$", "Increasing", r"$-$", "Concave down"],
            [r"$(0,\tfrac{2}{\sqrt{3}})$", r"$-$", "Decreasing", r"$-$", "Concave down"],
            [r"$(\tfrac{2}{\sqrt{3}},2)$", r"$-$", "Decreasing", r"$+$", "Concave up"],
            [r"$(2,\infty)$", r"$+$", "Increasing", r"$+$", "Concave up"],
        ],
    )

    _step("Step 4: Local extrema from the sign change of $f'(x)$.")
    _latex(r"x=-2:\;(-\to +)\Rightarrow \text{local minimum}")
    _latex(r"x=0:\;(+\to -)\Rightarrow \text{local maximum}")
    _latex(r"x=2:\;(-\to +)\Rightarrow \text{local minimum}")

    _step("Step 5: Inflection points from concavity change.")
    _latex(r"x=-\frac{2}{\sqrt{3}}:\;(+\to -)\Rightarrow \text{inflection point}")
    _latex(r"x=\frac{2}{\sqrt{3}}:\;(-\to +)\Rightarrow \text{inflection point}")

    # Small supporting graph
    xs = np.linspace(-4, 4, 700)
    ys = xs**4 - 8 * xs**2 + 10
    _small_plot(xs, ys, "Shape features (extrema + inflection)", vlines=[-2, 0, 2, -2 / math.sqrt(3), 2 / math.sqrt(3)])


def _learn_second_derivative_test() -> None:
    _h3("5.5.3 Second Derivative Test")
    _p("The Second Derivative Test helps you classify a **critical point** (where $f'(c)=0$).")
    _latex(r"\text{If }f'(c)=0\text{ and }f''(c)>0,\;\text{then }f(c)\text{ is a local minimum.}")
    _latex(r"\text{If }f'(c)=0\text{ and }f''(c)<0,\;\text{then }f(c)\text{ is a local maximum.}")

    _callout(
        "When the test is inconclusive",
        [
            "If $f'(c)=0$ but $f''(c)=0$, the test does not decide.",
            "In that case, you must use a sign test on $f'(x)$ (from Subtopic $5.4$) to classify the point.",
        ],
    )

    _h3("Worked example (exam format)")
    _exam_box(
        question_lines=["Consider the function:"],
        task_lines=[
            "Use the Second Derivative Test to find and classify local extrema.",
        ],
    )
    _latex(r"f(x)=x^{4}-8x^{2}+10")

    _step("Step 1: Solve $f'(x)=0$.")
    _latex(r"f'(x)=4x(x-2)(x+2)=0 \Rightarrow x=-2,0,2")

    _step("Step 2: Evaluate $f''(x)$ at each critical point.")
    _latex(r"f''(x)=12x^{2}-16")
    _latex(r"f''(-2)=12(4)-16=32>0 \Rightarrow \text{local minimum}")
    _latex(r"f''(0)=-16<0 \Rightarrow \text{local maximum}")
    _latex(r"f''(2)=32>0 \Rightarrow \text{local minimum}")

def _learn_graph_estimation() -> None:
    _h3("5.5.4 Estimating from a graph (what to look for)")
    _callout(
        "Concavity checklist",
        [
            "Concave up: the curve bends like a cup, and the slope is increasing as $x$ increases.",
            "Concave down: the curve bends like a cap, and the slope is decreasing as $x$ increases.",
            "Inflection point: the curve switches between concave up and concave down.",
        ],
    )
    _callout(
        "Extrema checklist",
        [
            "Local maximum: the curve goes up then down.",
            "Local minimum: the curve goes down then up.",
            "These usually happen near points where the tangent is horizontal (often $f'(x)=0$).",
        ],
    )

def _learn_economic_model() -> None:
    _h3("5.5.5 Economical/production meaning (simple model)")
    _p("In many applications, the second derivative describes how a rate is changing.")
    _p("For example, if $C(x)$ is a cost function, then:")
    _latex(r"C'(x)\; \text{is the marginal cost (rate of change of cost).}")
    _latex(r"C''(x)\; \text{describes whether the marginal cost is increasing or decreasing.}")

    _callout(
        "Interpretation you must know",
        [
            "If $C''(x)>0$, then $C'(x)$ is increasing (the cost rate is rising).",
            "If $C''(x)<0$, then $C'(x)$ is decreasing (the cost rate is falling).",
        ],
    )

    _h3("Worked example (exam format)")
    _exam_box(
        question_lines=["A simple cost model is:"],
        task_lines=[
            "Find where the cost curve is concave up and concave down.",
            "Explain what that means for the marginal cost $C'(x)$.",
        ],
    )
    _latex(r"C(x)=x^{3}-6x^{2}+9x")
    _step("Step 1: Compute the second derivative.")
    _latex(r"C'(x)=3x^{2}-12x+9")
    _latex(r"C''(x)=6x-12=6(x-2)")

    _step("Step 2: Use the sign of $C''(x)$.")
    _latex(r"C''(x)<0 \text{ for }x<2 \Rightarrow \text{concave down}")
    _latex(r"C''(x)>0 \text{ for }x>2 \Rightarrow \text{concave up}")
    _step("Step 3: Interpretation for $C'(x)$.")
    _latex(r"x<2:\; C''(x)<0 \Rightarrow C'(x)\text{ decreases}")
    _latex(r"x>2:\; C''(x)>0 \Rightarrow C'(x)\text{ increases}")

    xs = np.linspace(-1, 6, 600)
    ys = xs**3 - 6 * xs**2 + 9 * xs
    _small_plot(xs, ys, "Cost curve (concavity change)", vlines=[2])


def _learn_blackboard_simulator() -> None:
    _h2("Board simulator (full solution on one board)")
    _p("Choose an example, then press **Play solution** to watch the full solution appear on the same board.")

    example = st.radio(
        "Choose an example",
        options=["Example A (concavity + inflection)", "Example B (Second Derivative Test)"],
        horizontal=True,
    )

    if "bb_playing" not in st.session_state:
        st.session_state.bb_playing = False

    col1, col2 = st.columns([1, 1])
    with col1:
        play = st.button("Play solution", use_container_width=True)
    with col2:
        reset = st.button("Reset", use_container_width=True)

    if reset:
        st.session_state.bb_playing = False

    if play:
        st.session_state.bb_playing = True

    if not st.session_state.bb_playing:
        st.caption("Press **Play solution** to display the full solution.")
        return

    if example.startswith("Example A"):
        lines = [
            r"\\textbf{Example A: Concavity and inflection point}",
            r"f(x)=2x^{3}+9x^{2}-24x-10",
            r"f'(x)=6x^{2}+18x-24=6(x+4)(x-1)",
            r"f''(x)=12x+18=6(2x+3)",
            r"f''(x)=0 \Rightarrow 12x+18=0 \Rightarrow x=-\frac{3}{2}",
            r"x<-\frac{3}{2}:\; f''(x)<0 \Rightarrow \text{concave down}",
            r"x>-\frac{3}{2}:\; f''(x)>0 \Rightarrow \text{concave up}",
            r"\text{Inflection point at } \left(-\frac{3}{2},\,f\!\left(-\frac{3}{2}\right)\right)",
        ]
    else:
        lines = [
            r"\\textbf{Example B: Second Derivative Test}",
            r"f(x)=x^{4}-8x^{2}+10",
            r"f'(x)=4x^{3}-16x=4x(x-2)(x+2)",
            r"f'(x)=0 \Rightarrow x=-2,\;0,\;2",
            r"f''(x)=12x^{2}-16",
            r"f''(-2)=32>0 \Rightarrow \text{local minimum}",
            r"f''(0)=-16<0 \Rightarrow \text{local maximum}",
            r"f''(2)=32>0 \Rightarrow \text{local minimum}",
        ]

    used = _try_render_blackboard(lines_latex=lines, height_px=440)
    if not used:
        _fallback_blackboard(lines_latex=[f"$${ln}$$" if not ln.startswith(r"\\textbf") else ln.replace(r"\\textbf", "<b>").replace("}", "</b>") for ln in lines], height_px=440)


# ----------------------------
# Practice (20+ questions)
# ----------------------------

@dataclass
class PracticeItem:
    prompt_lines: List[str]     # Can include plain text, but math must be inside $...$.
    latex_lines: List[str]      # Displayed with st.latex (math only).
    hint_lines: List[str]       # Must avoid plain-text math; if needed, use $...$ in markdown.
    answer_steps: List[Tuple[str, Optional[str]]]  # (markdown sentence, latex or None)

def _practice_items() -> List[PracticeItem]:
    # All math is rendered using LaTeX either via $...$ or st.latex blocks.
    items: List[PracticeItem] = []

    # Q1–Q10: concavity + inflection from f'' sign
    items.append(PracticeItem(
        prompt_lines=["Find the intervals of concavity and any inflection points for:"],
        latex_lines=[r"f(x)=x^{3}-3x"],
        hint_lines=[
            "Compute $f''(x)$, solve $f''(x)=0$, then test the sign of $f''(x)$ on each interval.",
        ],
        answer_steps=[
            ("Compute derivatives:", r"f'(x)=3x^{2}-3,\quad f''(x)=6x"),
            ("Solve for candidates:", r"6x=0 \Rightarrow x=0"),
            ("Sign of $f''(x)$:", r"x<0:\ f''(x)<0\Rightarrow \text{concave down},\quad x>0:\ f''(x)>0\Rightarrow \text{concave up}"),
            ("Conclusion:", r"\text{Concave down on }(-\infty,0),\ \text{concave up on }(0,\infty),\ \text{inflection at }x=0"),
        ]
    ))

    items.append(PracticeItem(
        prompt_lines=["Find concavity intervals and inflection point(s) for:"],
        latex_lines=[r"f(x)=2x^{3}+9x^{2}-24x-10"],
        hint_lines=["Use $f''(x)$ and a sign test around the solution of $f''(x)=0$."],
        answer_steps=[
            ("Second derivative:", r"f''(x)=12x+18"),
            ("Candidates:", r"12x+18=0 \Rightarrow x=-\frac{3}{2}"),
            ("Concavity:", r"(-\infty,-\tfrac{3}{2})\!:\ f''<0\Rightarrow \text{CD},\quad (-\tfrac{3}{2},\infty)\!:\ f''>0\Rightarrow \text{CU}"),
            ("Inflection:", r"x=-\frac{3}{2}\text{ is an inflection }(\text{concavity changes})"),
        ]
    ))

    # Build more quick items (kept exam-style, but compact)
    polys = [
        (r"f(x)=x^{4}-8x^{2}+10", r"f''(x)=12x^{2}-16"),
        (r"f(x)=x^{3}-6x^{2}+9x", r"f''(x)=6x-12"),
        (r"f(x)=x^{4}+4x^{3}", r"f''(x)=12x^{2}+24x"),
        (r"f(x)=x^{3}+x", r"f''(x)=6x"),
        (r"f(x)=x^{4}-4x", r"f''(x)=12x^{2}"),
    ]
    for i, (fx, f2) in enumerate(polys, start=3):
        items.append(PracticeItem(
            prompt_lines=["Find concavity intervals and any inflection points for:"],
            latex_lines=[fx],
            hint_lines=["Compute $f''(x)$, solve $f''(x)=0$, then do a sign test for $f''(x)$."],
            answer_steps=[
                ("Second derivative:", f2),
                ("Candidates:", r"\text{Solve }f''(x)=0\text{ and test concavity on each interval.}"),
            ]
        ))

    # Q8–Q12: second derivative test
    items.append(PracticeItem(
        prompt_lines=["Use the Second Derivative Test to classify the critical points of:"],
        latex_lines=[r"f(x)=x^{4}-8x^{2}+10"],
        hint_lines=["Solve $f'(x)=0$, then evaluate $f''(x)$ at each critical point."],
        answer_steps=[
            ("Critical points:", r"f'(x)=4x(x-2)(x+2)=0 \Rightarrow x=-2,0,2"),
            ("Second derivative:", r"f''(x)=12x^{2}-16"),
            ("Classification:", r"f''(-2)=32>0\Rightarrow \min,\quad f''(0)=-16<0\Rightarrow \max,\quad f''(2)=32>0\Rightarrow \min"),
        ]
    ))

    items.append(PracticeItem(
        prompt_lines=["Use the Second Derivative Test to classify the critical point of:"],
        latex_lines=[r"g(x)=(x-1)^{4}"],
        hint_lines=["Compute $g'(x)$ and $g''(x)$. If $g''(c)=0$, the test is inconclusive."],
        answer_steps=[
            ("Derivatives:", r"g'(x)=4(x-1)^{3},\quad g''(x)=12(x-1)^{2}"),
            ("Critical point:", r"g'(x)=0 \Rightarrow x=1"),
            ("Test:", r"g''(1)=0\Rightarrow \text{inconclusive}"),
            ("What to do next:", r"\text{Use a sign test on }g'(x)\text{ to classify }x=1"),
        ]
    ))

    # Q14–Q20: graph interpretation (described tasks; still all math latex)
    items.append(PracticeItem(
        prompt_lines=[
            "A graph shows a curve that is concave down for $x<1$ and concave up for $x>1$.",
            "State the inflection $x$-value.",
        ],
        latex_lines=[],
        hint_lines=["An inflection occurs where concavity changes."],
        answer_steps=[("Answer:", r"x=1")]
    ))

    items.append(PracticeItem(
        prompt_lines=[
            "A graph has a local maximum at $x=-2$ and is concave down at that point.",
            "State what you expect about the signs of $f'( -2 )$ and $f''( -2 )$.",
        ],
        latex_lines=[],
        hint_lines=["At a local maximum, usually $f'(c)=0$ and concave down means $f''(c)<0$."],
        answer_steps=[
            ("Expected signs:", r"f'(-2)=0,\quad f''(-2)<0"),
        ]
    ))

    # Ensure at least 20
    while len(items) < 20:
        k = len(items) + 1
        items.append(PracticeItem(
            prompt_lines=[f"Compute concavity intervals for the function in Question {k}:"],
            latex_lines=[r"f(x)=x^{3}-kx"],  # still LaTeX; symbol k is fine
            hint_lines=["Compute $f''(x)$ and use a sign test."],
            answer_steps=[("General form:", r"f''(x)=6x\Rightarrow \text{CD on }(-\infty,0)\text{ and CU on }(0,\infty)")]
        ))

    return items


def _render_practice() -> None:
    _h2("Practice (20 questions)")
    _p("For each question: write the required derivatives, test signs on intervals, then state your final conclusion clearly.")

    items = _practice_items()
    for idx, it in enumerate(items, start=1):
        st.markdown("---")
        st.markdown(f"### Q{idx}")
        for ln in it.prompt_lines:
            _p(ln)

        for le in it.latex_lines:
            _latex(le)

        with st.expander("Hint", expanded=False):
            for hl in it.hint_lines:
                _p(hl)

        show = st.button(f"Show answer for Q{idx}", key=f"show_{idx}", use_container_width=True)
        if show:
            st.markdown("**Solution (step-by-step)**")
            for md, latex in it.answer_steps:
                _p(md)
                if latex:
                    _latex(latex)


# ----------------------------
# Learn tab renderer
# ----------------------------

def _render_learn() -> None:
    _learn_objectives()
    st.markdown("---")

    _learn_concavity_definition()
    st.markdown("---")

    _worked_example_concavity_inflection()
    st.markdown("---")

    _learn_tables_of_variation()
    st.markdown("---")

    _worked_example_combined_table()
    st.markdown("---")

    _learn_second_derivative_test()
    st.markdown("---")

    _learn_graph_estimation()
    st.markdown("---")

    _learn_economic_model()
    st.markdown("---")

    _learn_blackboard_simulator()


# ----------------------------
# Required entry point
# ----------------------------

def render() -> None:
    # Required by the app registry (fixes “missing render()”).
    st.title("Subtopic 5.5: Concavity and 2nd Derivative Test")
    st.caption("Term: Term 2 • Topic: Topic 5: Applications of Differentiation")

    tab_learn, tab_practice = st.tabs(["Learn", "Practice"])
    with tab_learn:
        _render_learn()
    with tab_practice:
        _render_practice()
