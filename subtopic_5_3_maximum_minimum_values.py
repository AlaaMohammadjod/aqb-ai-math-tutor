import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

from simulations import BoardStep, render_simulation


# -----------------------------
# Helpers (LaTeX-first, student-friendly, no sliders)
# -----------------------------
def _step(latex_line: str, explain_md: str) -> BoardStep:
    return BoardStep(latex_line=latex_line, teacher_explain_md=explain_md)


def _callout(kind: str, title: str, body_md: str = "", latex_lines: list[str] | None = None) -> None:
    """
    Uses Streamlit's native callouts so KaTeX renders correctly.
    (HTML divs break KaTeX rendering, so we avoid them completely.)
    """
    if latex_lines is None:
        latex_lines = []

    header = f"**{title}**"
    if body_md.strip():
        msg = header + "\n\n" + body_md
    else:
        msg = header

    if kind == "warning":
        st.warning(msg)
    elif kind == "check":
        st.success(msg)
    elif kind == "note":
        st.info(msg)
    elif kind == "answer":
        st.success(msg)
    else:
        st.info(msg)

    for ln in latex_lines:
        st.latex(ln)


def _exam_block(title: str, question_latex: str, tasks_md: str) -> None:
    st.markdown(f"### {title}")
    st.markdown("**Question**")
    st.latex(question_latex)
    st.markdown("**What your answer must include**")
    st.markdown(tasks_md)


def _fig_axes():
    # Centered + slightly bigger (but still compact)
    fig = plt.figure(figsize=(3.2, 1.8), dpi=220)
    ax = fig.add_subplot(111)
    ax.grid(True, alpha=0.22)
    ax.axhline(0, color="black", linewidth=0.65, alpha=0.65)
    ax.axvline(0, color="black", linewidth=0.65, alpha=0.65)
    return fig, ax


def _plot_function(ax, x, y, title: str, xlabel: str = "x", ylabel: str = "y"):
    ax.plot(x, y, linewidth=1.7)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.tick_params(axis="both", labelsize=8)


def _mark_points(ax, pts):
    for (x0, y0, label) in pts:
        ax.scatter([x0], [y0], s=18)
        ax.annotate(label, (x0, y0), textcoords="offset points", xytext=(4, 3), fontsize=7)


def _q_block(num: int, problem_latex: str, hint_md: str, solution_steps_latex: list[str]) -> None:
    st.markdown(f"### Q{num}")
    st.markdown("**Problem**")
    st.latex(problem_latex)
    c1, c2 = st.columns([1, 1])
    with c1:
        with st.expander("Hint", expanded=False):
            st.markdown(hint_md)
    with c2:
        with st.expander("Show full solution", expanded=False):
            st.markdown("**Solution (all steps)**")
            for s in solution_steps_latex:
                st.latex(s)


def _simulation_graph_reading(
    title: str,
    fx_latex: str,
    key_prefix: str,
    xlim: tuple[float, float],
    f_callable,
    conclusion_latex: str,
    candidates_latex: list[str],
):
    """
    Button-based mini-simulation:
    - No sliders
    - ALL math is rendered via st.latex or KaTeX inline ($...$) inside Streamlit native callouts
    - Graphs are centered and slightly bigger
    - Conclusion is ALWAYS visible
    """
    st.markdown(f"#### {title}")
    st.markdown("**Function:**")
    st.latex(fx_latex)

    _callout(
        "note",
        "How to read the graph (exactly what to look for)",
        "1) The horizontal axis is $x$ and the vertical axis is $y=f(x)$.\n"
        "2) A point higher on the curve means a larger value of $f(x)$.\n"
        "3) A point lower on the curve means a smaller value of $f(x)$.\n"
        "4) On a closed interval $[a,b]$, check endpoints and critical numbers.\n"
        "5) A turning point often appears where $f'(x)=0$ (horizontal tangent).",
    )

    a, b = xlim
    sample = [a, (2 * a + b) / 3.0, (a + b) / 2.0, (a + 2 * b) / 3.0, b]

    stage_key = f"{key_prefix}_stage"
    if stage_key not in st.session_state:
        st.session_state[stage_key] = 0

    cols = st.columns([1, 1, 1, 1])
    with cols[0]:
        if st.button("Start", key=f"{key_prefix}_start"):
            st.session_state[stage_key] = 0
    with cols[1]:
        if st.button("Next step", key=f"{key_prefix}_next"):
            st.session_state[stage_key] = min(st.session_state[stage_key] + 1, 3)
    with cols[2]:
        if st.button("Back", key=f"{key_prefix}_back"):
            st.session_state[stage_key] = max(st.session_state[stage_key] - 1, 0)
    with cols[3]:
        if st.button("Jump to compare", key=f"{key_prefix}_compare"):
            st.session_state[stage_key] = 3

    stage = st.session_state[stage_key]

    x = np.linspace(a - 0.2 * (b - a), b + 0.2 * (b - a), 620)
    y = np.array([f_callable(float(t)) for t in x])

    fig, ax = _fig_axes()
    _plot_function(ax, x, y, "Graph")
    ax.set_xlim(a - 0.2 * (b - a), b + 0.2 * (b - a))

    if stage == 0:
        _callout(
            "tip",
            "Step 0 — Before marking anything",
            "First, check: are you working on an open interval $(a,b)$ or a closed interval $[a,b]$?\n"
            "If it is closed, endpoints are included. If it is open, endpoints are not included.",
        )

    if stage >= 1:
        ya = f_callable(a)
        yb = f_callable(b)
        _mark_points(ax, [(a, ya, "end"), (b, yb, "end")])
        _callout(
            "tip",
            "Step 1 — Mark endpoints (if included)",
            "For a closed interval $[a,b]$, endpoints are always candidates for absolute extrema.",
            latex_lines=[r"\text{Endpoint candidates: }x=a,\;x=b"],
        )

    if stage >= 2:
        ys = [f_callable(t) for t in sample]
        imin = int(np.argmin(ys))
        imax = int(np.argmax(ys))
        _mark_points(ax, [(sample[imin], ys[imin], "low?"), (sample[imax], ys[imax], "high?")])
        _callout(
            "tip",
            "Step 2 — Look inside for turning",
            "Scan the curve. If it changes from increasing to decreasing, it suggests a local maximum.\n"
            "If it changes from decreasing to increasing, it suggests a local minimum.",
            latex_lines=[r"\text{Turning points often occur where }f'(x)=0."],
        )

    if stage >= 3:
        _callout(
            "check",
            "Step 3 — Compare candidate values",
            "Compare the function values at every candidate point.\n"
            "Largest value $\Rightarrow$ absolute maximum. Smallest value $\Rightarrow$ absolute minimum.",
        )
        for c in candidates_latex:
            st.latex(c)

    # Center graph (no full-width stretch)
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        st.pyplot(fig, use_container_width=False)

    _callout("answer", "Conclusion (always visible)")
    st.latex(conclusion_latex)


# -----------------------------
# Learn: Objectives 5.3.1–5.3.9
# -----------------------------
def _obj_531():
    st.subheader("Objective 5.3.1 — Identify absolute extrema and use graphs to locate them")

    _callout(
        "tip",
        "Absolute extrema (meaning)",
        "An absolute maximum is the greatest value of the function on the given set.\n"
        "An absolute minimum is the least value of the function on the given set.",
    )

    st.latex(r"\text{Absolute maximum at }c\in S:\; f(c)\ge f(x)\;\text{for all }x\in S")
    st.latex(r"\text{Absolute minimum at }c\in S:\; f(c)\le f(x)\;\text{for all }x\in S")

    st.markdown("### Visual: same function, different intervals")
    st.latex(r"f(x)=x^{2}-9")

    choice = st.radio(
        "Choose the interval",
        ["(−∞,∞)", r"(-3,3)", r"[-3,3]"],
        key="s53_531_interval",
    )

    def f(t: float) -> float:
        return t * t - 9.0

    if choice == "(−∞,∞)":
        _simulation_graph_reading(
            "Graph simulation: unbounded interval idea",
            r"f(x)=x^{2}-9",
            "s53_531_a",
            (-3.0, 3.0),
            f,
            r"\max f \text{ does not exist on }(-\infty,\infty)\quad\text{and}\quad \min f=-9\text{ at }x=0.",
            [r"f(0)=-9", r"\text{As }|x|\to\infty,\;f(x)\to\infty"],
        )
    elif choice == r"(-3,3)":
        _simulation_graph_reading(
            "Graph simulation: open interval (endpoints not included)",
            r"f(x)=x^{2}-9",
            "s53_531_b",
            (-3.0, 3.0),
            f,
            r"\max f \text{ does not exist on }(-3,3)\quad\text{and}\quad \min f=-9\text{ at }x=0.",
            [r"f(0)=-9", r"\text{The value }0\text{ is approached near }x=\pm 3\text{ but not reached.}"],
        )
    else:
        _simulation_graph_reading(
            "Graph simulation: closed interval (endpoints included)",
            r"f(x)=x^{2}-9",
            "s53_531_c",
            (-3.0, 3.0),
            f,
            r"\max f=0\text{ at }x=-3\text{ and }x=3\quad\text{and}\quad \min f=-9\text{ at }x=0.",
            [r"f(-3)=0", r"f(0)=-9", r"f(3)=0"],
        )


def _obj_532():
    st.subheader("Objective 5.3.2 — Functions with no absolute extrema")

    _callout(
        "warning",
        "Why extrema may not exist",
        "Absolute extrema can fail to exist if the function is unbounded, or if the interval is open and the best value is never reached.",
    )

    st.latex(r"f(x)=x^{2}-9\quad\text{on }(-3,3)")

    _simulation_graph_reading(
        "Graph simulation: why no absolute maximum on an open interval",
        r"f(x)=x^{2}-9",
        "s53_532",
        (-3.0, 3.0),
        lambda t: t * t - 9.0,
        r"\max f \text{ does not exist on }(-3,3)\quad\text{because the endpoints are not included.}",
        [r"\text{Candidates do not include }x=\pm 3", r"\text{So the top value is never attained.}"],
    )


def _obj_533_534_536():
    st.subheader("Objectives 5.3.3, 5.3.4, 5.3.6 — EVT + critical numbers + tangent behavior")

    _callout(
        "check",
        "Extreme Value Theorem (EVT)",
        "If $f$ is continuous on a closed interval $[a,b]$, then $f$ must have an absolute maximum and an absolute minimum on $[a,b]$.",
        latex_lines=[
            r"\text{If }f\text{ is continuous on }[a,b],\text{ then }f\text{ attains an absolute maximum and minimum on }[a,b]."
        ],
    )

    st.markdown("### Critical numbers")
    st.latex(
        r"\text{A critical number }c\text{ satisfies }f'(c)=0\;\text{or }f'(c)\text{ is undefined, and }c\text{ is in the domain of }f."
    )

    st.markdown("### Tangent behavior")
    st.latex(r"f'(c)=0\Rightarrow\text{horizontal tangent at }x=c")
    st.latex(r"f'(c)\text{ undefined }\Rightarrow\text{vertical tangent or corner at }x=c")

    _callout(
        "tip",
        "Closed-interval method",
        "1) Find critical numbers in $(a,b)$.\n"
        "2) Evaluate $f$ at critical numbers and endpoints.\n"
        "3) Largest value is the absolute maximum; smallest value is the absolute minimum.",
    )

    _exam_block(
        "Worked example (EVT procedure)",
        r"\text{Find the absolute extrema of }f(x)=2x^{3}-3x^{2}-12x+5\text{ on }[-2,4].",
        "- Find $f'(x)$.\n"
        "- Solve $f'(x)=0$.\n"
        "- Evaluate at endpoints and critical numbers.\n"
        "- Compare values to decide absolute maximum/minimum.",
    )

    steps = [
        _step(
            r"f(x)=2x^{3}-3x^{2}-12x+5",
            "This polynomial is continuous on the closed interval, so EVT guarantees absolute extrema exist.",
        ),
        _step(r"f'(x)=6x^{2}-6x-12", "Differentiate."),
        _step(r"6x^{2}-6x-12=0\Rightarrow x^{2}-x-2=0", "Set derivative equal to zero and simplify."),
        _step(r"(x-2)(x+1)=0\Rightarrow x=2\;\text{or}\;x=-1", "Solve for critical numbers."),
        _step(r"\text{Candidates: }x=-2,\,-1,\,2,\,4", "Endpoints and critical numbers."),
        _step(r"f(-2)=1,\;f(-1)=12,\;f(2)=-15,\;f(4)=37", "Evaluate the function at each candidate."),
        _step(r"\text{Absolute maximum: }37\text{ at }x=4", "Largest value."),
        _step(r"\text{Absolute minimum: }-15\text{ at }x=2", "Smallest value."),
    ]
    render_simulation(steps, "5.3.3 — EVT procedure (unique title)")

    def fpoly(t: float) -> float:
        return 2 * t**3 - 3 * t**2 - 12 * t + 5

    _simulation_graph_reading(
        "Graph simulation: EVT candidates on a closed interval",
        r"f(x)=2x^{3}-3x^{2}-12x+5",
        "s53_evt_graph",
        (-2.0, 4.0),
        fpoly,
        r"\max f=37\text{ at }x=4\quad\text{and}\quad \min f=-15\text{ at }x=2.",
        [r"f(-2)=1", r"f(-1)=12", r"f(2)=-15", r"f(4)=37"],
    )


def _obj_535():
    st.subheader("Objective 5.3.5 — Relative (local) extrema")

    _callout(
        "tip",
        "Local vs absolute",
        "A local maximum/minimum is the highest/lowest value only in a small neighborhood around the point.",
    )

    st.latex(r"\text{Local maximum at }c:\; f(c)\ge f(x)\;\text{for }x\text{ near }c")
    st.latex(r"\text{Local minimum at }c:\; f(c)\le f(x)\;\text{for }x\text{ near }c")

    st.markdown("### Visual: local maximum")
    st.latex(r"f(x)=9-x^{2}")

    _simulation_graph_reading(
        "Graph simulation: spotting a local maximum",
        r"f(x)=9-x^{2}",
        "s53_localmax",
        (-3.0, 3.0),
        lambda t: 9.0 - t * t,
        r"\text{Local maximum at }x=0\text{ with }f(0)=9.",
        [r"f'(x)=-2x", r"f'(0)=0"],
    )


def _obj_537():
    st.subheader("Objective 5.3.7 — Fermat’s Theorem (and the warning)")

    _callout(
        "check",
        "Fermat’s Theorem",
        "If $f$ has a local extremum at an interior point $c$ and $f'(c)$ exists, then $f'(c)=0$.",
        latex_lines=[r"\text{If }f\text{ has a local extremum at }c\text{ and }f'(c)\text{ exists, then }f'(c)=0."],
    )

    _callout(
        "warning",
        "Important warning",
        "A critical number does not guarantee a local extremum.",
    )

    st.markdown("### Example 1: critical but no local extremum")
    st.latex(r"f(x)=x^{3}\qquad f'(x)=3x^{2}\Rightarrow f'(0)=0")
    _simulation_graph_reading(
        "Graph simulation: flat point (no turning)",
        r"f(x)=x^{3}",
        "s53_flatpoint",
        (-2.0, 2.0),
        lambda t: t**3,
        r"\text{No local extremum at }x=0\text{ even though }f'(0)=0.",
        [r"f'(x)=3x^{2}", r"f'(0)=0"],
    )

    st.markdown("### Example 2: vertical tangent critical number")
    st.latex(r"f(x)=x^{1/3}\qquad f'(x)=\frac{1}{3}x^{-2/3}\text{ undefined at }x=0")
    _simulation_graph_reading(
        "Graph simulation: vertical tangent (still no turning)",
        r"f(x)=x^{1/3}",
        "s53_verticaltangent",
        (-2.0, 2.0),
        lambda t: float(np.cbrt(t)),
        r"\text{No local extremum at }x=0\text{ even though }f'(0)\text{ is undefined.}",
        [r"f'(x)=\frac{1}{3}x^{-2/3}", r"\text{undefined at }x=0"],
    )


def _obj_538():
    st.subheader("Objective 5.3.8 — Find critical numbers and local extrema (many function types)")

    _callout(
        "tip",
        "Standard method",
        "1) Find the domain.\n"
        "2) Compute $f'(x)$.\n"
        "3) Solve $f'(x)=0$ and include points where $f'(x)$ is undefined (but $f$ is defined).\n"
        "4) Use turning/sign change to classify local maxima/minima.",
    )

    st.markdown("### A) Polynomial example")
    _exam_block(
        "Example 1",
        r"\text{Find critical numbers and local extrema for }f(x)=x^{2}+5x-1.",
        "- Compute $f'(x)$.\n"
        "- Solve $f'(x)=0$.\n"
        "- Classify the extremum.",
    )
    steps = [
        _step(r"f(x)=x^{2}+5x-1", "Parabola opens upward."),
        _step(r"f'(x)=2x+5", "Differentiate."),
        _step(r"2x+5=0\Rightarrow x=-\frac{5}{2}", "Critical number."),
        _step(r"\text{Local minimum at }x=-\frac{5}{2}", "Upward parabola means the vertex is a minimum."),
    ]
    render_simulation(steps, "5.3.8 — Polynomial local extremum (unique)")

    _simulation_graph_reading(
        "Graph simulation: local minimum (polynomial)",
        r"f(x)=x^{2}+5x-1",
        "s53_poly_min_graph",
        (-5.0, 2.0),
        lambda t: t * t + 5 * t - 1,
        r"\text{Local minimum at }x=-\frac{5}{2}.",
        [r"f'(x)=2x+5", r"x=-\frac{5}{2}"],
    )

    st.markdown("### B) Fractional exponent example")
    _exam_block(
        "Example 2",
        r"\text{Find the critical numbers for }f(x)=(3x+1)^{2/3}.",
        "- Compute $f'(x)$.\n"
        "- Find where $f'(x)$ is undefined.\n"
        "- Confirm the point is in the domain.",
    )

    steps2 = [
        _step(r"f(x)=(3x+1)^{2/3}", "The function is defined for all real $x$."),
        _step(r"f'(x)=\frac{2}{(3x+1)^{1/3}}", "Differentiate (chain rule)."),
        _step(r"3x+1=0\Rightarrow x=-\frac{1}{3}", "Derivative undefined but function defined."),
        _step(r"\Rightarrow x=-\frac{1}{3}\text{ is a critical number.}", "Must be checked for extrema."),
    ]
    render_simulation(steps2, "5.3.8 — Fractional exponent critical number (unique)")

    st.markdown("### C) Rational function example")
    _exam_block(
        "Example 3",
        r"\text{Find critical numbers of }f(x)=\frac{x}{x^{2}+1}\text{ and identify any local extrema.}",
        "- Find the domain.\n"
        "- Compute $f'(x)$.\n"
        "- Solve $f'(x)=0$.\n"
        "- Use sign changes to classify.",
    )
    steps3 = [
        _step(r"f(x)=\frac{x}{x^{2}+1}", r"\text{Domain: all real }x\text{ because }x^{2}+1\ne 0."),
        _step(r"f'(x)=\frac{(x^{2}+1)-x(2x)}{(x^{2}+1)^{2}}", "Quotient rule."),
        _step(r"f'(x)=\frac{1-x^{2}}{(x^{2}+1)^{2}}", "Simplify."),
        _step(r"1-x^{2}=0\Rightarrow x=\pm 1", "Critical numbers."),
        _step(r"\text{Local minimum at }x=-1,\;\text{local maximum at }x=1", "Sign changes of $f'(x)$."),
    ]
    render_simulation(steps3, "5.3.8 — Rational function critical numbers (unique)")


def _obj_539():
    st.subheader("Objective 5.3.9 — Absolute extrema on a closed interval (answers in terms of $\\pi$)")

    _callout(
        "check",
        "Closed interval checklist",
        "On $[a,b]$, compare values at endpoints and critical numbers inside the interval.",
    )

    st.markdown("### Trigonometric example (answers in terms of $\\pi$)")
    st.latex(r"f(x)=\sin x+\cos x\quad\text{on }\left[0,2\pi\right]")

    _exam_block(
        "Example 1",
        r"\text{Find absolute maximum and minimum of }f(x)=\sin x+\cos x\text{ on }\left[0,2\pi\right].",
        "- Find $f'(x)$.\n"
        "- Solve $f'(x)=0$ in the interval.\n"
        "- Evaluate at endpoints and critical points.\n"
        "- Decide absolute maximum/minimum.",
    )

    steps = [
        _step(r"f'(x)=\cos x-\sin x", "Differentiate."),
        _step(r"\cos x-\sin x=0\Rightarrow \tan x=1", "Set derivative equal to zero."),
        _step(r"x=\frac{\pi}{4},\;\frac{5\pi}{4}", "Solutions in $[0,2\pi]$."),
        _step(r"f(0)=1,\;f(2\pi)=1", "Endpoints."),
        _step(r"f\left(\frac{\pi}{4}\right)=\sqrt{2},\;f\left(\frac{5\pi}{4}\right)=-\sqrt{2}", "Critical points."),
        _step(r"\text{Absolute maximum: }\sqrt{2}\text{ at }x=\frac{\pi}{4}", "Largest value."),
        _step(r"\text{Absolute minimum: }-\sqrt{2}\text{ at }x=\frac{5\pi}{4}", "Smallest value."),
    ]
    render_simulation(steps, "5.3.9 — Trig absolute extrema (unique)")

    _simulation_graph_reading(
        "Graph simulation: trig on a closed interval",
        r"f(x)=\sin x+\cos x",
        "s53_trig_interval_graph",
        (0.0, 2.0 * math.pi),
        lambda t: math.sin(t) + math.cos(t),
        r"\max f=\sqrt{2}\text{ at }x=\frac{\pi}{4}\qquad \min f=-\sqrt{2}\text{ at }x=\frac{5\pi}{4}.",
        [r"x=\frac{\pi}{4}", r"x=\frac{5\pi}{4}"],
    )


# -----------------------------
# Practice (20 questions, Hint + Show full solution)
# -----------------------------
def _practice():
    st.subheader("Practice (20 questions)")

    _callout(
        "check",
        "Practice rule",
        "Each problem includes a Hint and a Show full solution section. "
        "When you open Show full solution, you will see the complete steps all at once.",
    )

    questions = []

    questions.append(
        (
            r"\text{On }(-\infty,\infty),\text{ find absolute extrema of }f(x)=x^{2}-9.",
            "Check whether the parabola is bounded above or below.",
            [
                r"f'(x)=2x\Rightarrow f'(x)=0\text{ at }x=0.",
                r"f(0)=-9\Rightarrow \min f=-9\text{ at }x=0.",
                r"\max f\text{ does not exist because }f(x)\to\infty\text{ as }|x|\to\infty.",
            ],
        )
    )

    questions.append(
        (
            r"\text{On }(-3,3),\text{ find absolute extrema of }f(x)=x^{2}-9.",
            "Open interval means endpoints are not included.",
            [
                r"f'(x)=2x=0\Rightarrow x=0.",
                r"f(0)=-9\Rightarrow \min f=-9.",
                r"\max f\text{ does not exist on }(-3,3).",
            ],
        )
    )

    questions.append(
        (
            r"\text{On }[-3,3],\text{ find absolute extrema of }f(x)=x^{2}-9.",
            "Endpoints and critical numbers must be checked.",
            [
                r"f'(x)=2x=0\Rightarrow x=0.",
                r"f(-3)=0,\;f(0)=-9,\;f(3)=0.",
                r"\min f=-9\text{ at }x=0.",
                r"\max f=0\text{ at }x=-3\text{ and }x=3.",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find critical numbers of }f(x)=|x|.",
            "Look for corners.",
            [
                r"f'(0)\text{ is undefined and }0\text{ is in the domain.}",
                r"\Rightarrow x=0\text{ is a critical number.}",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find the local extrema of }f(x)=9-x^{2}.",
            "Downward parabola: vertex is a local maximum.",
            [
                r"f'(x)=-2x\Rightarrow f'(0)=0.",
                r"\Rightarrow \text{local maximum at }x=0\text{ with }f(0)=9.",
            ],
        )
    )

    questions.append(
        (
            r"\text{For }f(x)=x^{3},\text{ decide whether }x=0\text{ is a local extremum.}",
            "A critical number does not always mean an extremum.",
            [
                r"f'(x)=3x^{2}\Rightarrow f'(0)=0\Rightarrow x=0\text{ is critical.}",
                r"f\text{ increases through }0\Rightarrow \text{no local extremum at }x=0.",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find critical numbers of }f(x)=x^{1/3}.",
            "Derivative is undefined at $x=0$.",
            [
                r"f'(x)=\frac{1}{3}x^{-2/3}\text{ is undefined at }x=0.",
                r"f(0)\text{ exists }\Rightarrow x=0\text{ is a critical number.}",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find absolute extrema of }f(x)=2x^{3}-3x^{2}-12x+5\text{ on }[-2,4].",
            "Use EVT method: endpoints + critical numbers.",
            [
                r"f'(x)=6x^{2}-6x-12=6(x-2)(x+1)\Rightarrow x=-1,2.",
                r"f(-2)=1,\;f(-1)=12,\;f(2)=-15,\;f(4)=37.",
                r"\max f=37\text{ at }x=4,\quad \min f=-15\text{ at }x=2.",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find critical numbers for }f(x)=x^{2}+5x-1\text{ and classify the extremum.}",
            "Solve $f'(x)=0$ and use parabola shape.",
            [
                r"f'(x)=2x+5=0\Rightarrow x=-\frac{5}{2}.",
                r"\text{Local minimum at }x=-\frac{5}{2}.",
            ],
        )
    )

    questions.append(
        (
            r"\text{On }\left[0,2\pi\right],\text{ find absolute extrema of }f(x)=\sin x+\cos x.",
            r"Solve $f'(x)=0$ and keep answers in terms of $\pi$.",
            [
                r"f'(x)=\cos x-\sin x=0\Rightarrow \tan x=1.",
                r"x=\frac{\pi}{4},\;\frac{5\pi}{4}.",
                r"f\left(\frac{\pi}{4}\right)=\sqrt{2},\;f\left(\frac{5\pi}{4}\right)=-\sqrt{2},\;f(0)=f(2\pi)=1.",
                r"\max f=\sqrt{2}\text{ at }x=\frac{\pi}{4},\quad \min f=-\sqrt{2}\text{ at }x=\frac{5\pi}{4}.",
            ],
        )
    )

    questions.append(
        (
            r"\text{On }\left[\frac{\pi}{2},\pi\right],\text{ find absolute extrema of }f(x)=\sin x+\cos x.",
            r"If no critical point lies inside, check endpoints only.",
            [
                r"f'(x)=0\Rightarrow x=\frac{\pi}{4},\;\frac{5\pi}{4}\notin\left[\frac{\pi}{2},\pi\right].",
                r"f\left(\frac{\pi}{2}\right)=1,\;f(\pi)=-1.",
                r"\max f=1\text{ at }x=\frac{\pi}{2},\quad \min f=-1\text{ at }x=\pi.",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find critical numbers of }f(x)=\sin x\cos x\text{ on }\left[0,2\pi\right].",
            r"Use }f(x)=\frac{1}{2}\sin(2x).",
            [
                r"f(x)=\frac{1}{2}\sin(2x)\Rightarrow f'(x)=\cos(2x).",
                r"\cos(2x)=0\Rightarrow 2x=\frac{\pi}{2}+k\pi\Rightarrow x=\frac{\pi}{4}+\frac{k\pi}{2}.",
                r"x\in\left\{\frac{\pi}{4},\frac{3\pi}{4},\frac{5\pi}{4},\frac{7\pi}{4}\right\}\text{ on }\left[0,2\pi\right].",
            ],
        )
    )

    questions.append(
        (
            r"\text{On }[0,4],\text{ find critical numbers for }f(x)=4x^{5/4}-8x^{1/4}.",
            "Include points where $f'(x)$ is undefined if $f$ is defined.",
            [
                r"f'(x)=5x^{1/4}-2x^{-3/4}=\frac{5x-2}{x^{3/4}}.",
                r"f'(x)=0\Rightarrow 5x-2=0\Rightarrow x=\frac{2}{5}.",
                r"f'(x)\text{ undefined at }x=0\text{ and }f(0)\text{ exists.}",
                r"\Rightarrow x=0,\;\frac{2}{5}\text{ are critical numbers.}",
            ],
        )
    )

    questions.append(
        (
            r"\text{Explain why EVT guarantees absolute extrema for any polynomial on }[a,b].",
            "Use continuity + closed interval.",
            [
                r"\text{Polynomials are continuous for all }x.",
                r"\text{A continuous function on }[a,b]\text{ attains an absolute maximum and minimum (EVT).}",
            ],
        )
    )

    questions.append(
        (
            r"\text{A function has a local maximum at an interior point }c\text{ and }f'(c)\text{ exists. What must be true?}",
            "Use Fermat’s Theorem.",
            [
                r"\text{By Fermat’s Theorem, }f'(c)=0.",
            ],
        )
    )

    questions.append(
        (
            r"\text{Decide whether the critical point is caused by a corner or a vertical tangent for }f(x)=|x|\text{ and }g(x)=x^{1/3}\text{ at }x=0.",
            r"Corner has a sharp turn; vertical tangent has infinite slope.",
            [
                r"f(x)=|x|\Rightarrow \text{corner at }x=0\Rightarrow f'(0)\text{ undefined due to a corner.}",
                r"g(x)=x^{1/3}\Rightarrow g'(x)=\frac{1}{3}x^{-2/3}\Rightarrow \text{undefined at }x=0\Rightarrow \text{vertical tangent.}",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find critical numbers of }f(x)=\frac{x}{x^{2}+1}\text{ and classify them as local max/min or neither.}",
            r"Use the sign of $f'(x)$ around $x=\pm 1$.",
            [
                r"f'(x)=\frac{1-x^{2}}{(x^{2}+1)^{2}}.",
                r"1-x^{2}=0\Rightarrow x=\pm 1.",
                r"\text{For }|x|<1,\;f'(x)>0\text{ and for }|x|>1,\;f'(x)<0.",
                r"\Rightarrow \text{local minimum at }x=-1\text{ and local maximum at }x=1.",
            ],
        )
    )

    questions.append(
        (
            r"\text{Does EVT guarantee absolute extrema for a continuous function on }(a,b)?\text{ Explain.}",
            r"EVT requires a closed interval.",
            [
                r"\text{No. EVT requires continuity on }[a,b].",
                r"\text{On }(a,b),\text{ a function can approach a best value without attaining it.}",
            ],
        )
    )

    questions.append(
        (
            r"\text{A function has a local maximum at }x=c.\text{ Must it be an absolute maximum? Explain.}",
            r"Local compares nearby values; absolute compares the whole set.",
            [
                r"\text{No. A local maximum is only the largest nearby value.}",
                r"\text{An absolute maximum must be largest on the entire domain/interval.}",
            ],
        )
    )

    questions.append(
        (
            r"\text{Find all critical numbers of }f(x)=\sin x+\cos x\text{ on }\left[0,2\pi\right]\text{ and state which gives max/min.}",
            r"Solve $f'(x)=0\Rightarrow \tan x=1$.",
            [
                r"f'(x)=\cos x-\sin x=0\Rightarrow \tan x=1.",
                r"x=\frac{\pi}{4},\;\frac{5\pi}{4}.",
                r"\max f=\sqrt{2}\text{ at }x=\frac{\pi}{4},\quad \min f=-\sqrt{2}\text{ at }x=\frac{5\pi}{4}.",
            ],
        )
    )

    for i, (prob, hint, sol) in enumerate(questions, start=1):
        _q_block(i, prob, hint, sol)


# -----------------------------
# Entry point
# -----------------------------
def render():
    st.header("Subtopic 5.3: Maximum and Minimum Values")
    st.caption("Student version: fully guided explanations, simulations, and practice (no sliders)")

    learn_tab, practice_tab = st.tabs(["Learn", "Practice"])

    with learn_tab:
        st.markdown("### Learning objectives")
        st.markdown("- 5.3.1 Identify the absolute extrema of a function and use graphs to locate them.")
        st.markdown("- 5.3.2 Showcase functions with no absolute extrema.")
        st.markdown("- 5.3.3 Identify and apply the Extreme Value Theorem to find absolute extrema on closed intervals.")
        st.markdown("- 5.3.4 Define the critical value $c$ of functions: $f'(c)=0$ or $f'(c)$ is undefined.")
        st.markdown("- 5.3.5 Define relative (local) extrema (minimum and maximum).")
        st.markdown("- 5.3.6 Recall tangent behavior when $f'(c)=0$ or $f'(c)$ is undefined.")
        st.markdown("- 5.3.7 Demonstrate Fermat’s Theorem and its limitation.")
        st.markdown(
            "- 5.3.8 Find critical number(s) and local extrema for polynomials, fractional exponents, rational functions, and basic trigonometric functions."
        )
        st.markdown(
            "- 5.3.9 Find absolute extrema on a closed interval for polynomials, fractional exponents, rational functions, and basic trigonometric functions."
        )
        st.latex(r"f'(c)=0\quad\text{or}\quad f'(c)\text{ is undefined}")

        st.divider()
        _obj_531()
        st.divider()
        _obj_532()
        st.divider()
        _obj_533_534_536()
        st.divider()
        _obj_535()
        st.divider()
        _obj_537()
        st.divider()
        _obj_538()
        st.divider()
        _obj_539()

    with practice_tab:
        _practice()