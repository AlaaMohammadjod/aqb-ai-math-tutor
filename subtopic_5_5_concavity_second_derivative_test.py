# ===========================
# File 1 of 2
# subtopic_5_5_concavity_second_derivative_test.py
# ===========================

import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from subtopic_5_5_concavity_second_derivative_test_data import (
    LEARNING_OBJECTIVES,
    WORKED_EXAMPLES,
    PRACTICE_QUESTIONS,
    BOARD_EXAMPLES,
)

# -----------------------------
# Helpers (strict: all math is LaTeX/KaTeX)
# -----------------------------
def _md(s: str) -> None:
    st.markdown(s)

def _latex(expr: str) -> None:
    st.latex(expr)

def _title_math(text_with_math: str) -> None:
    # Use markdown + inline latex, but keep math inside \( \)
    st.markdown(text_with_math)

def _info_box(title: str, body_lines: list[str]) -> None:
    st.markdown(
        f"""
<div style="border-left: 6px solid #1f77b4; background: #f2f7ff; padding: 12px 14px; border-radius: 10px; margin: 8px 0 14px 0;">
  <div style="font-weight: 800; margin-bottom: 8px;">{title}</div>
  <div style="line-height: 1.55;">
    {"".join([f"<div style='margin: 4px 0;'>{line}</div>" for line in body_lines])}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

def _section_header(h: str) -> None:
    st.markdown(f"### {h}")

def _small_plot(fig, max_width_px: int = 680):
    # Smaller + consistent plot sizing (no huge charts)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

def _plot_function_with_marks(
    f,
    x_min: float,
    x_max: float,
    title: str,
    x_marks: list[float] | None = None,
    y_marks: list[float] | None = None,
):
    xs = np.linspace(x_min, x_max, 600)
    ys = f(xs)

    fig = plt.figure(figsize=(7.2, 3.6), dpi=140)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xs, ys)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)

    if x_marks:
        for xm in x_marks:
            ax.axvline(xm, linestyle="--", linewidth=1, alpha=0.8)
    if x_marks and y_marks and len(x_marks) == len(y_marks):
        ax.scatter(x_marks, y_marks)

    _small_plot(fig)

def _render_clean_table(headers: list[str], rows: list[list[str]], title: str | None = None):
    """
    Render a *readable* table using matplotlib (large font, no overlap).
    Note: math in tables is rendered as LaTeX-style text inside the figure.
    """
    fig = plt.figure(figsize=(8.0, 2.6), dpi=170)
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")

    cell_text = rows
    table = ax.table(
        cellText=cell_text,
        colLabels=headers,
        cellLoc="center",
        colLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.15, 1.55)

    if title:
        ax.set_title(title, fontsize=13, pad=10)

    _small_plot(fig)

def _katex_all_math_reminder():
    _info_box(
        "How to write your final answers clearly",
        [
            "Whenever you write a derivative, write it as \\(f'(x)\\) or \\(f''(x)\\).",
            "When you give intervals, write them as \\((a,b)\\), \\([a,b]\\), \\((a,\\infty)\\), or \\(( -\\infty, b)\\).",
            "When you state concavity, use: \\(f''(x)>0\\Rightarrow\\) concave up, and \\(f''(x)<0\\Rightarrow\\) concave down.",
            "An inflection point happens when concavity **changes** (sign change of \\(f''(x)\\)).",
        ],
    )

# -----------------------------
# Blackboard-style auto-solved (no next-step buttons)
# -----------------------------
def _board_play(example_key: str):
    ex = BOARD_EXAMPLES[example_key]

    # Blackboard frame
    st.markdown(
        """
<div style="background:#0b0f14; border:1px solid #1d2a3a; border-radius:14px; padding:18px 18px 14px 18px; margin-top:10px;">
  <div style="color:#d7e7ff; font-weight:800; margin-bottom:8px;">Blackboard</div>
  <div style="color:#a9c7ff; margin-bottom:12px; line-height:1.55;">
    Watch the full solution appear line-by-line on the same board.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # We write into one placeholder (same canvas)
    board = st.empty()

    lines = ex["lines_latex"]  # list[str] with LaTeX (already safe)
    delay = ex.get("delay_s", 0.35)

    # Accumulate and redraw in the SAME place
    rendered = []
    for line in lines:
        rendered.append(line)
        with board.container():
            st.markdown(
                """
<div style="background:#0b0f14; border:1px solid #1d2a3a; border-radius:14px; padding:16px 16px 14px 16px;">
""",
                unsafe_allow_html=True,
            )
            for L in rendered:
                st.latex(L)
            st.markdown("</div>", unsafe_allow_html=True)
        time.sleep(delay)

def _board_ui():
    _section_header("Board simulator (auto-solved examples)")
    _info_box(
        "How to use this",
        [
            "Choose an example, then press the play button to see the **full** solution appear on the same board.",
            "The board shows the derivatives, the sign reasoning for \\(f''(x)\\), then the final concavity and inflection conclusions.",
        ],
    )

    ex_keys = list(BOARD_EXAMPLES.keys())
    labels = [BOARD_EXAMPLES[k]["label"] for k in ex_keys]
    choice = st.radio("Choose an example", labels, index=0, horizontal=True)
    chosen_key = ex_keys[labels.index(choice)]

    c1, c2 = st.columns([1, 1])
    with c1:
        play = st.button("Play solution", use_container_width=True)
    with c2:
        reset = st.button("Reset", use_container_width=True)

    if reset:
        st.session_state["board_last_played"] = None
        st.rerun()

    if play:
        st.session_state["board_last_played"] = chosen_key

    if st.session_state.get("board_last_played") == chosen_key:
        _board_play(chosen_key)

# -----------------------------
# Learn tab content (strictly inside objectives)
# -----------------------------
def _render_objectives():
    _section_header("Learning objectives")
    for obj in LEARNING_OBJECTIVES:
        st.markdown(f"- {obj}")

def _render_concavity_core():
    _section_header("5.5.1 Concavity and inflection points")
    _info_box(
        "Key idea",
        [
            "Concavity describes how the slope \\(f'(x)\\) changes.",
            "If the slopes are getting **larger** as \\(x\\) increases, then \\(f\\) is concave up.",
            "If the slopes are getting **smaller** as \\(x\\) increases, then \\(f\\) is concave down.",
        ],
    )

    st.markdown("Use the second derivative to test concavity:")
    _latex(r"f''(x)>0 \ \Rightarrow\ \text{concave up}")
    _latex(r"f''(x)<0 \ \Rightarrow\ \text{concave down}")

    _info_box(
        "Inflection points",
        [
            "An inflection point is a point where the graph changes concavity.",
            "To find candidates: solve \\(f''(x)=0\\) and also check where \\(f''(x)\\) is undefined (if it happens).",
            "Then you must confirm a sign change of \\(f''(x)\\) across that \\(x\\)-value.",
        ],
    )

def _render_second_derivative_test():
    _section_header("5.5.3 Second derivative test (local maximum / local minimum)")
    _info_box(
        "When you can use it",
        [
            "First, find a critical point by solving \\(f'(c)=0\\).",
            "Then evaluate \\(f''(c)\\).",
        ],
    )
    st.markdown("Classification:")
    _latex(r"f''(c)<0 \ \Rightarrow\ f(c)\ \text{is a local maximum}")
    _latex(r"f''(c)>0 \ \Rightarrow\ f(c)\ \text{is a local minimum}")
    _latex(r"f''(c)=0 \ \Rightarrow\ \text{inconclusive (you must use another method)}")

def _render_tables_of_variation():
    _section_header("5.5.2 Combined tables (variation + concavity)")
    _info_box(
        "What your combined table must include",
        [
            "Interval row split using all critical numbers (from \\(f'(x)=0\\)) and all concavity candidates (from \\(f''(x)=0\\) or where \\(f''(x)\\) is undefined).",
            "A sign row for \\(f'(x)\\) to decide increasing/decreasing.",
            "A sign row for \\(f''(x)\\) to decide concave up/concave down.",
            "A final behavior row summarizing increasing/decreasing and concavity on each interval.",
        ],
    )

    headers = [
        r"Interval",
        r"sign of $f'(x)$",
        r"Behavior",
        r"sign of $f''(x)$",
        r"Concavity",
    ]
    rows = [
        [r"$(-\infty,a)$", r"$+/-$", r"$\text{Inc.}/\text{Dec.}$", r"$+/-$", r"$\text{CU}/\text{CD}$"],
        [r"$(a,b)$", r"$+/-$", r"$\text{Inc.}/\text{Dec.}$", r"$+/-$", r"$\text{CU}/\text{CD}$"],
        [r"$(b,\infty)$", r"$+/-$", r"$\text{Inc.}/\text{Dec.}$", r"$+/-$", r"$\text{CU}/\text{CD}$"],
    ]
    _render_clean_table(headers, rows, title="Combined table template")

def _render_graph_estimation():
    _section_header("5.5.4 Estimating from a graph")
    _info_box(
        "What to look for on a graph",
        [
            "Increasing where the curve rises left-to-right; decreasing where it falls left-to-right.",
            "Concave up where the curve bends like a cup \\((\\cup)\\); concave down where it bends like a cap \\((\\cap)\\).",
            "Inflection point where the bending switches from \\(\\cup\\) to \\(\\cap\\), or from \\(\\cap\\) to \\(\\cup\\).",
        ],
    )

    # Keep chart smaller
    def f(x):
        return 2 * x**3 + 9 * x**2 - 24 * x - 10

    _plot_function_with_marks(
        f,
        x_min=-4.2,
        x_max=4.2,
        title="Example curve for estimating concavity and turning behavior",
        x_marks=[-1.5, 0.0, 2.0],
        y_marks=[f(-1.5), f(0.0), f(2.0)],
    )

def _render_applications():
    _section_header("5.5.5 Applications (economics / production)")
    _info_box(
        "How concavity helps in applications",
        [
            "If \\(C(t)\\) is cost, then \\(C'(t)\\) is the cost rate and \\(C''(t)\\) tells whether that rate is increasing or decreasing.",
            "If \\(C''(t)>0\\), then \\(C'(t)\\) is increasing and the cost rate is rising.",
            "If \\(C''(t)<0\\), then \\(C'(t)\\) is decreasing and the cost rate is falling.",
        ],
    )

    st.markdown("Example (exam format):")
    _info_box(
        "Question",
        [
            r"Let \(C(t)=t^3-6t^2+12t+5\).",
            r"1) Find where \(C\) is concave up and concave down.",
            r"2) Interpret what this means for the behavior of the cost rate \(C'(t)\).",
        ],
    )
    st.markdown("Solution:")
    _latex(r"C'(t)=3t^2-12t+12")
    _latex(r"C''(t)=6t-12=6(t-2)")
    _latex(r"C''(t)=0 \Rightarrow t=2")
    _latex(r"\text{For }t<2,\ C''(t)<0\Rightarrow C\text{ is concave down}")
    _latex(r"\text{For }t>2,\ C''(t)>0\Rightarrow C\text{ is concave up}")
    _latex(r"\text{Interpretation: }t<2,\ C'(t)\text{ decreases; }t>2,\ C'(t)\text{ increases}")

def _render_worked_examples():
    _section_header("Worked examples (exam format)")
    for ex in WORKED_EXAMPLES:
        _info_box("Question", ex["question_lines"])
        st.markdown("Solution:")
        for L in ex["solution_latex_lines"]:
            _latex(L)

def _render_learn():
    st.header("Subtopic 5.5: Concavity and 2nd Derivative Test")

    _render_objectives()
    _katex_all_math_reminder()

    _render_concavity_core()
    _render_second_derivative_test()
    _render_tables_of_variation()
    _render_worked_examples()
    _board_ui()
    _render_graph_estimation()
    _render_applications()

# -----------------------------
# Practice tab (keep structure clean, all math in LaTeX)
# -----------------------------
def _render_practice():
    st.header("Practice")

    _info_box(
        "How to answer",
        [
            r"For each question: compute \(f'(x)\) and/or \(f''(x)\) as required.",
            r"State intervals using correct notation such as \((a,b)\), \((a,\infty)\), or \((-\infty,b)\).",
            r"When asked for inflection points, you must confirm a concavity change (sign change of \(f''(x)\)).",
        ],
    )

    for i, q in enumerate(PRACTICE_QUESTIONS, start=1):
        st.markdown(f"#### Q{i}")
        _info_box("Question", q["question_lines"])

        # Show answer button (no sliders)
        key = f"show_ans_{i}"
        if key not in st.session_state:
            st.session_state[key] = False

        cols = st.columns([1, 3])
        with cols[0]:
            if st.button("Show answer", key=f"btn_{i}", use_container_width=True):
                st.session_state[key] = not st.session_state[key]

        if st.session_state[key]:
            st.markdown("Answer:")
            for L in q["answer_latex_lines"]:
                _latex(L)

# -----------------------------
# Required entry point
# -----------------------------
def render():
    # Must exist for the app registry
    if "board_last_played" not in st.session_state:
        st.session_state["board_last_played"] = None

    tab1, tab2 = st.tabs(["Learn", "Practice"])
    with tab1:
        _render_learn()
    with tab2:
        _render_practice()
