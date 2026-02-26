# subtopic_5_6_curve_sketching_overview.py
# AQB Grade 12 AI Math Tutor — Subtopic 5.6: Overview of Curve Sketching
# Style aligned to repo’s “best-looking” subtopic patterns (exam boxes, callouts, small plots),
# while keeping the learning logic and simulations usage unchanged.
#
# NOTE: Does NOT modify app.py or simulations.py.

from __future__ import annotations

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# ----------------------------
# Visual style helpers (match Subtopic 5.5 patterns)
# ----------------------------
def _h2(title: str) -> None:
    st.markdown(f"## {title}")


def _h3(title: str) -> None:
    st.markdown(f"### {title}")


def _p(text: str) -> None:
    st.markdown(text)


def _latex(expr: str) -> None:
    # KaTeX-friendly LaTeX line (humanised)
    st.latex(expr)


def _callout(title: str, body_lines: list[str]) -> None:
    # Same style as Subtopic 5.5: info box with bullet points
    st.info("**" + title + "**\n\n" + "\n".join([f"- {ln}" for ln in body_lines]))


def _exam_box(question_lines: list[str], task_lines: list[str]) -> None:
    # Same “Question / Task” box style as Subtopic 5.5
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


def _small_plot_xy(x: np.ndarray, y: np.ndarray, title: str, vlines: list[float] | None = None, hlines: list[float] | None = None) -> None:
    # Match Subtopic 5.5 plot sizing + dpi (small, crisp)
    fig = plt.figure(figsize=(6.2, 3.2), dpi=140)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    if vlines:
        for xv in vlines:
            ax.axvline(xv, linestyle="--", linewidth=1)

    if hlines:
        for yv in hlines:
            ax.axhline(yv, linestyle="--", linewidth=1)

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)
    st.pyplot(fig, clear_figure=True)


def _small_plot_fig(fig) -> None:
    # For pre-built figs, keep same “small” feel
    st.pyplot(fig, clear_figure=True, use_container_width=False)


# ----------------------------
# Example graphs (small, controlled)
# ----------------------------
def _fig_small(title: str):
    fig = plt.figure(figsize=(6.2, 3.2), dpi=140)
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    return fig, ax


def _plot_polynomial_example():
    # f(x)=x^3-3x
    x = np.linspace(-3.2, 3.2, 800)
    y = x**3 - 3 * x
    fig, ax = _fig_small(r"Polynomial: $f(x)=x^3-3x$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_rational_example():
    # f(x)=(x+1)/(x-2)
    x1 = np.linspace(-6, 1.95, 800)
    x2 = np.linspace(2.05, 6, 800)
    f = lambda t: (t + 1) / (t - 2)

    fig, ax = _fig_small(r"Rational: $f(x)=\dfrac{x+1}{x-2}$")
    ax.plot(x1, f(x1), label=r"$f(x)$")
    ax.plot(x2, f(x2), label=r"$f(x)$")
    ax.axvline(2, linestyle="--", linewidth=1)
    ax.axhline(1, linestyle="--", linewidth=1)
    ax.set_ylim(-6, 6)
    ax.legend(loc="best")
    return fig


def _plot_fractional_power_example():
    # f(x)=x^(2/3)
    x = np.linspace(-8, 8, 1200)
    y = np.sign(x) * (np.abs(x) ** (2 / 3))
    fig, ax = _fig_small(r"Fractional power: $f(x)=x^{2/3}$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_radical_example():
    # f(x)=sqrt(x-1)
    x = np.linspace(1, 10, 600)
    y = np.sqrt(x - 1)
    fig, ax = _fig_small(r"Radical: $f(x)=\sqrt{x-1}$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_trig_exp_log_example():
    # f(x)=ln(x)+sin(x), x>0
    x = np.linspace(0.25, 10, 900)
    y = np.log(x) + np.sin(x)
    fig, ax = _fig_small(r"Components: $f(x)=\ln(x)+\sin(x)$, domain $x>0$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


# ----------------------------
# Simulations (must use simulations.py as-is)
# ----------------------------
def _sim_curve_sketch_rational():
    steps = [
        BoardStep(
            latex_line=r"f(x)=\frac{x+1}{x-2}",
            teacher_explain_md=r"We will **sketch** a rational function by following the curve-sketching workflow step by step.",
        ),
        BoardStep(
            latex_line=r"\textbf{1) Domain: }x\neq 2",
            teacher_explain_md=r"Because the denominator is zero at \(x=2\), the function is **undefined** there.",
        ),
        BoardStep(
            latex_line=r"\textbf{2) Vertical asymptote: }x=2",
            teacher_explain_md=r"Since \((x-2)\) does **not** cancel, \(x=2\) is a **vertical asymptote**.",
        ),
        BoardStep(
            latex_line=r"\textbf{3) Horizontal asymptote: }y=1",
            teacher_explain_md=r"Degrees are equal (1 and 1), so the horizontal asymptote is the ratio of leading coefficients: \(\frac{1}{1}=1\).",
        ),
        BoardStep(
            latex_line=r"\textbf{4) Intercepts: }f(0)=-\frac12,\ \ x\text{-int: }x=-1",
            teacher_explain_md=r"Find intercepts for anchor points: \(y\)-intercept is \(f(0)\). The \(x\)-intercept is where numerator \(x+1=0\Rightarrow x=-1\).",
        ),
        BoardStep(
            latex_line=r"\textbf{5) First derivative: }f'(x)=\frac{-3}{(x-2)^2}",
            teacher_explain_md=r"Differentiate to study **increasing/decreasing**. Here \(f'(x)\) is always negative (except undefined at \(x=2\)).",
        ),
        BoardStep(
            latex_line=r"\textbf{Variation: }f'(x)<0\Rightarrow \text{decreasing on }(-\infty,2)\ \text{and }(2,\infty)",
            teacher_explain_md=r"So there are **no turning points**, but there is a break at the asymptote.",
        ),
        BoardStep(
            latex_line=r"\textbf{6) Second derivative: }f''(x)=\frac{6}{(x-2)^3}",
            teacher_explain_md=r"Use \(f''(x)\) to study **concavity**.",
        ),
        BoardStep(
            latex_line=r"\textbf{Concavity: }f''(x)<0\ (x<2),\quad f''(x)>0\ (x>2)",
            teacher_explain_md=r"The curve is **concave down** to the left of \(x=2\) and **concave up** to the right.",
        ),
        BoardStep(
            latex_line=r"\textbf{7) Table of values (near }x=2\textbf{): }f(1)= -2,\ f(3)=4",
            teacher_explain_md=r"Pick a few points to control the sketch. Near a vertical asymptote, values change quickly.",
        ),
        BoardStep(
            latex_line=r"\textbf{8) Final sketch: two branches approaching }x=2\ \text{and }y=1",
            teacher_explain_md=r"Combine: domain break at \(2\), VA \(x=2\), HA \(y=1\), decreasing on both sides, and opposite concavity on each side.",
        ),
    ]
    render_simulation(steps, title="Simulation A — Full workflow on a rational function")


def _sim_curve_sketch_polynomial():
    steps = [
        BoardStep(
            latex_line=r"f(x)=x^3-3x",
            teacher_explain_md=r"We will sketch a polynomial using derivatives to find turning points and concavity.",
        ),
        BoardStep(
            latex_line=r"\textbf{1) Domain: }\mathbb{R}",
            teacher_explain_md=r"Polynomials are defined for all real \(x\).",
        ),
        BoardStep(
            latex_line=r"\textbf{2) Intercepts: }x(x^2-3)=0\Rightarrow x=0,\ \pm\sqrt3",
            teacher_explain_md=r"Factor to find \(x\)-intercepts. The \(y\)-intercept is \(f(0)=0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{3) First derivative: }f'(x)=3x^2-3=3(x^2-1)",
            teacher_explain_md=r"Critical points happen when \(f'(x)=0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{4) Critical points: }3(x^2-1)=0\Rightarrow x=\pm 1",
            teacher_explain_md=r"Evaluate \(f(x)\) at these \(x\)-values to locate turning points.",
        ),
        BoardStep(
            latex_line=r"f(-1)=2\quad(\text{local max}),\qquad f(1)=-2\quad(\text{local min})",
            teacher_explain_md=r"Use the sign of \(f'(x)\): it changes from \(+\) to \(-\) at \(-1\) (max) and from \(-\) to \(+\) at \(1\) (min).",
        ),
        BoardStep(
            latex_line=r"\textbf{5) Second derivative: }f''(x)=6x",
            teacher_explain_md=r"Inflection points occur when \(f''(x)=0\) **and** concavity changes.",
        ),
        BoardStep(
            latex_line=r"\textbf{6) Inflection: }6x=0\Rightarrow x=0,\ \ f(0)=0",
            teacher_explain_md=r"Concavity: \(f''(x)<0\) for \(x<0\) (concave down) and \(f''(x)>0\) for \(x>0\) (concave up).",
        ),
        BoardStep(
            latex_line=r"\textbf{7) Final sketch: S-shape through }(-\sqrt3,0), (0,0), (\sqrt3,0)",
            teacher_explain_md=r"Combine intercepts, turning points \((-1,2)\) and \((1,-2)\), and inflection \((0,0)\).",
        ),
    ]
    render_simulation(steps, title="Simulation B — Full workflow on a polynomial")


# ----------------------------
# Practice (same logic, clearer + consistent spacing)
# ----------------------------
def _practice_asymptotes():
    _h3("Practice Set 5.6.1 — Asymptotes (Rational Functions)")

    _p(r"**Q1.** For \(f(x)=\dfrac{2x^2-1}{x^2+4}\), what is the horizontal asymptote?")
    ans = st.radio(
        "Choose one:",
        ["A) \(y=0\)", "B) \(y=1\)", "C) \(y=2\)", "D) No horizontal asymptote"],
        index=None,
        key="p561_q1",
    )
    if ans:
        if ans.startswith("C"):
            st.success(r"Correct. Degrees are equal (2 and 2), so HA is \(\frac{2}{1}=2\).")
        else:
            st.error("Not quite. Compare degrees and leading coefficients.")
        with st.expander("Hint + full answer"):
            _p(r"If \(\deg(P)=\deg(Q)\), then \(y=\dfrac{\text{LC}(P)}{\text{LC}(Q)}\). So \(y=2\).")

    st.markdown("---")

    _p(r"**Q2.** For \(g(x)=\dfrac{x+3}{(x-1)(x+2)}\), which values give vertical asymptotes?")
    ans2 = st.radio(
        "Choose one:",
        ["A) \(x=1\) only", "B) \(x=-2\) only", "C) \(x=1\) and \(x=-2\)", "D) No vertical asymptotes"],
        index=None,
        key="p561_q2",
    )
    if ans2:
        if ans2.startswith("C"):
            st.success(r"Correct. Denominator is zero at \(x=1\) and \(x=-2\), and nothing cancels.")
        else:
            st.error("Check where the denominator becomes zero (and whether factors cancel).")
        with st.expander("Hint + full answer"):
            _p(r"VA occur at denominator zeros that do not cancel: \((x-1)(x+2)=0\Rightarrow x=1,-2\).")


def _practice_workflow_steps():
    _h3("Practice Set 5.6.2 — Curve Sketching Steps")

    _p(r"**Q3.** Which option shows the correct order of the core curve-sketching steps?")
    ans3 = st.radio(
        "Choose one:",
        [
            "A) Derivatives → Sketch → Domain → Table → Asymptotes",
            "B) Domain → Derivatives → Critical points → Concavity/Inflection → Table → Sketch",
            "C) Table → Domain → Sketch → Derivatives → Concavity",
            "D) Domain → Table → Sketch only",
        ],
        index=None,
        key="p562_q3",
    )
    if ans3:
        if ans3.startswith("B"):
            st.success("Correct. This matches the workflow in objective 5.6.2.")
        else:
            st.error("Not quite. Start with domain, then derivatives for shape, then small table, then final sketch.")
        with st.expander("Why this order?"):
            _callout(
                "Reliable summary order",
                [
                    "Domain",
                    "First & second derivative",
                    "Critical values / first derivative test",
                    "Inflection / concavity / second derivative test",
                    "Overlap behaviour tables (variation + concavity)",
                    "Small table of values",
                    "Final sketch",
                ],
            )


def _practice_sketching_types():
    _h3("Practice Set 5.6.3 — Sketching Different Function Types")

    _p(r"**Q4.** Which statement is true for \(f(x)=\sqrt{x-4}\)?")
    ans4 = st.radio(
        "Choose one:",
        [
            "A) Domain is all real numbers",
            "B) Domain is \(x\ge 4\)",
            "C) Domain is \(x\le 4\)",
            "D) It has a vertical asymptote at \(x=4\)",
        ],
        index=None,
        key="p563_q4",
    )
    if ans4:
        if ans4.startswith("B"):
            st.success(r"Correct. Need \(x-4\ge 0\Rightarrow x\ge 4\).")
        else:
            st.error(r"Think: for radicals, the inside must be \(\ge 0\).")
        with st.expander("Hint + full answer"):
            _p(r"\(\sqrt{x-4}\) is defined when \(x\ge 4\). At \(x=4\), \(f(4)=0\) (endpoint, not an asymptote).")

    st.markdown("---")

    _p(r"**Q5.** Which feature best describes \(h(x)=x^{2/3}\) at \(x=0\)?")
    ans5 = st.radio(
        "Choose one:",
        [
            "A) A smooth minimum",
            "B) A cusp (sharp point)",
            "C) A vertical asymptote",
            "D) A hole (removable discontinuity)",
        ],
        index=None,
        key="p563_q5",
    )
    if ans5:
        if ans5.startswith("B"):
            st.success(r"Correct. \(x^{2/3}\) is defined but has a sharp point (cusp) at \(0\).")
        else:
            st.error("Look at the shape near \(x=0\): defined but not smooth.")
        with st.expander("Hint + full answer"):
            _p(r"\(x^{2/3}=(\sqrt[3]{x})^2\) is defined for all real \(x\), but not differentiable at \(0\) (cusp).")


# ----------------------------
# Main render()
# ----------------------------
def render():
    st.header("Subtopic 5.6: Overview of Curve Sketching")
    st.caption("Source: Al Diwan – Grade 12 Advanced Stream Mathematics – Lesson 4.6")

    _h2("Learning objectives (5.6)")
    _p("By the end of this subtopic, you should be able to:")

    st.markdown(
        """
- **5.6.1** Recall finding the **horizontal** and **vertical asymptotes** of a rational function.  
- **5.6.2** Discuss and understand the **summary of steps** for curve sketching techniques:
  - domain  
  - first and second derivative  
  - critical values / first derivative test  
  - inflection values / concavity / second derivative test  
  - overlapping summary behavior tables of variation and concavity  
  - table of values for a few points  
  - sketching  
- **5.6.3** Analyze and sketch graphs for different functions:
  - polynomials  
  - rational functions  
  - with fractional powers of \(x\)  
  - with radicals  
  - with trig / exp / log components  
"""
    )

    tabs = st.tabs(["Learn", "Simulations", "Practice"])

    # ---------------------- LEARN ----------------------
    with tabs[0]:
        _h2("5.6.1  Horizontal and vertical asymptotes (rational functions)")

        _callout(
            "Rational function form",
            [
                r"A rational function is \(f(x)=\dfrac{P(x)}{Q(x)}\) where \(P,Q\) are polynomials and \(Q(x)\neq 0\).",
                r"Always start with the **domain**: exclude values where \(Q(x)=0\).",
            ],
        )

        _h3("Vertical asymptotes (VA)")
        _p(
            r"A vertical asymptote happens where the denominator is zero **after simplifying** (no factor cancels):"
        )
        _latex(r"Q(x)=0 \quad \Rightarrow \quad x=\text{(vertical asymptote candidates)}")

        _h3("Horizontal asymptotes (HA)")
        _p("Recall the degree rules:")
        st.markdown(
            r"""
- If \(\deg(P) < \deg(Q)\), then \(y=0\).  
- If \(\deg(P) = \deg(Q)\), then \(y=\dfrac{\text{leading coefficient of }P}{\text{leading coefficient of }Q}\).  
- If \(\deg(P) > \deg(Q)\), then there is **no horizontal asymptote** (in this subtopic we only recall HA/VA).
"""
        )

        with st.expander("Mini example (asymptotes) — open"):
            _exam_box(
                question_lines=[r"Consider \(f(x)=\dfrac{x+1}{x-2}\)."],
                task_lines=[
                    r"State the domain.",
                    r"Find the vertical asymptote.",
                    r"Find the horizontal asymptote.",
                ],
            )
            _step("Solution highlights")
            _p(r"Domain: \(x\neq 2\)")
            _p(r"Vertical asymptote: \(x=2\)")
            _p(r"Horizontal asymptote: degrees equal \(\Rightarrow y=\frac{1}{1}=1\)")

        st.markdown("---")

        _h2("5.6.2  Summary workflow for curve sketching")
        _callout(
            "Use this order every time",
            [
                "1) Domain",
                "2) First and second derivative",
                "3) Critical values / first derivative test",
                "4) Inflection values / concavity / second derivative test",
                "5) Overlap behaviour tables (variation + concavity)",
                "6) Small table of values (few points)",
                "7) Final sketch",
            ],
        )

        _p(
            r"The goal is not to compute lots of points. The goal is to **control the shape** using derivatives and key features."
        )

        cols = st.columns(2)
        with cols[0]:
            _callout(
                "Variation table (from \(f'(x)\))",
                [
                    r"If \(f'(x)>0\), the function is increasing.",
                    r"If \(f'(x)<0\), the function is decreasing.",
                    r"Turning points come from \(f'(x)=0\) (then confirm with sign change).",
                ],
            )
        with cols[1]:
            _callout(
                "Concavity table (from \(f''(x)\))",
                [
                    r"If \(f''(x)>0\), concave up.",
                    r"If \(f''(x)<0\), concave down.",
                    r"Inflection points come from \(f''(x)=0\) (then confirm concavity change).",
                ],
            )

        st.markdown("---")

        _h2("5.6.3  Sketching different function families")
        st.markdown(
            r"""
Different functions need different **first checks**:

- **Polynomials:** domain is \(\mathbb{R}\). Derivatives locate turning points and inflection points.  
- **Rational functions:** domain restrictions + **vertical asymptotes** + possible **horizontal asymptotes**.  
- **Fractional powers** (e.g., \(x^{2/3}\)): can create **sharp points** at key locations.  
- **Radicals** (e.g., \(\sqrt{x-1}\)): domain often begins at an **endpoint**.  
- **Trig / exp / log components:** check domain restrictions (e.g., \(\ln(x)\) needs \(x>0\)) and general shape.
"""
        )

        _h3("Small visual gallery (graphs are intentionally not oversized)")
        g1, g2 = st.columns(2)
        with g1:
            _small_plot_fig(_plot_polynomial_example())
        with g2:
            _small_plot_fig(_plot_rational_example())

        g3, g4 = st.columns(2)
        with g3:
            _small_plot_fig(_plot_fractional_power_example())
        with g4:
            _small_plot_fig(_plot_radical_example())

        _small_plot_fig(_plot_trig_exp_log_example())

        st.markdown("---")

        _h3("Quick analysis card (choose an example)")
        choice = st.selectbox(
            "Choose a function",
            [
                r"Polynomial:  f(x)=x^3-3x",
                r"Rational:    f(x)=(x+1)/(x-2)",
                r"Fractional:  f(x)=x^{2/3}",
                r"Radical:     f(x)=\sqrt{x-1}",
                r"Components:  f(x)=\ln(x)+\sin(x)",
            ],
            index=1,
            key="cs_choice_56",
        )

        if "Polynomial" in choice:
            _callout(
                "Key sketch checkpoints",
                [
                    r"Domain: \(\mathbb{R}\).",
                    r"Critical points from \(f'(x)=0\).",
                    r"Concavity + inflection from \(f''(x)\).",
                ],
            )
            _latex(r"f'(x)=3x^2-3=3(x^2-1)\Rightarrow x=\pm 1")
            _latex(r"f''(x)=6x\Rightarrow \text{inflection at }x=0\ (\text{concavity changes})")

        elif "Rational" in choice:
            _callout(
                "Key sketch checkpoints",
                [
                    r"Start with domain + vertical asymptotes.",
                    r"Then recall horizontal asymptote rule (degree comparison).",
                    r"Use \(f'(x)\) and \(f''(x)\) to control shape on each interval.",
                ],
            )
            _latex(r"\text{Domain: }x\neq 2")
            _latex(r"\text{VA: }x=2 \qquad \text{HA: }y=1")

        elif "Fractional" in choice:
            _callout(
                "Key sketch checkpoint",
                [
                    r"\(x^{2/3}\) is defined for all real \(x\), but has a **cusp** at \(x=0\).",
                    r"That affects how the curve meets the origin (sharp point).",
                ],
            )

        elif "Radical" in choice:
            _callout(
                "Key sketch checkpoint",
                [
                    r"For \(\sqrt{x-1}\), require \(x-1\ge 0\Rightarrow x\ge 1\).",
                    r"The curve begins at an endpoint \((1,0)\).",
                ],
            )

        else:
            _callout(
                "Key sketch checkpoint",
                [
                    r"Domain is controlled by \(\ln(x)\Rightarrow x>0\).",
                    r"\(\sin(x)\) adds oscillation around the slow growth of \(\ln(x)\).",
                ],
            )

    # ------------------- SIMULATIONS -------------------
    with tabs[1]:
        _h2("Blackboard simulations (step-by-step)")
        _p(
            r"Use **Start solving** to animate the board. The explanation panel tells you exactly **why** each step matters."
        )
        _sim_curve_sketch_rational()
        st.markdown("---")
        _sim_curve_sketch_polynomial()

    # -------------------- PRACTICE ---------------------
    with tabs[2]:
        _practice_asymptotes()
        st.markdown("---")
        _practice_workflow_steps()
        st.markdown("---")
        _practice_sketching_types()
