# subtopic_5_6_curve_sketching_overview.py
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# ------------------------------------------------------------
# Helpers (humanised math everywhere)
# ------------------------------------------------------------
def _md_math(md: str):
    """
    Render Markdown that may include inline math \( \) and display math $$ $$.
    (Streamlit renders these with KaTeX.)
    """
    st.markdown(md)


def _small_plot(fig):
    """Keep graphs readable and not oversized."""
    st.pyplot(fig, clear_figure=True, use_container_width=False)


def _section(title: str, body_md: str):
    st.subheader(title)
    _md_math(body_md)


def _pill(title: str, text_md: str, kind: str = "info"):
    if kind == "success":
        st.success(f"**{title}**\n\n{text_md}")
    elif kind == "warning":
        st.warning(f"**{title}**\n\n{text_md}")
    else:
        st.info(f"**{title}**\n\n{text_md}")


# ------------------------------------------------------------
# Example functions (pre-selected; no sympy needed)
# ------------------------------------------------------------
def _plot_function(ax, x, y, label):
    ax.plot(x, y, label=label)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)


def _fig_small(title: str):
    fig = plt.figure(figsize=(6.0, 3.3))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    return fig, ax


def _plot_polynomial_example():
    # f(x)=x^3-3x
    x = np.linspace(-3.2, 3.2, 800)
    y = x**3 - 3 * x
    fig, ax = _fig_small(r"Polynomial example: $f(x)=x^3-3x$")
    _plot_function(ax, x, y, r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_rational_example():
    # f(x)=(x+1)/(x-2)
    x1 = np.linspace(-6, 1.95, 800)
    x2 = np.linspace(2.05, 6, 800)
    f = lambda t: (t + 1) / (t - 2)
    fig, ax = _fig_small(r"Rational example: $f(x)=\dfrac{x+1}{x-2}$")
    _plot_function(ax, x1, f(x1), r"$f(x)$")
    _plot_function(ax, x2, f(x2), r"$f(x)$")
    ax.axvline(2, linestyle="--", linewidth=1.0)
    ax.axhline(1, linestyle="--", linewidth=1.0)
    ax.set_ylim(-6, 6)
    ax.legend(loc="best")
    return fig


def _plot_fractional_power_example():
    # f(x)=x^(2/3)
    x = np.linspace(-8, 8, 1200)
    y = np.sign(x) * (np.abs(x) ** (2 / 3))
    fig, ax = _fig_small(r"Fractional power: $f(x)=x^{2/3}$")
    _plot_function(ax, x, y, r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_radical_example():
    # f(x)=sqrt(x-1)
    x = np.linspace(1, 10, 600)
    y = np.sqrt(x - 1)
    fig, ax = _fig_small(r"Radical: $f(x)=\sqrt{x-1}$")
    _plot_function(ax, x, y, r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_trig_exp_log_example():
    # f(x)=ln(x)+sin(x), x>0
    x = np.linspace(0.25, 10, 900)
    y = np.log(x) + np.sin(x)
    fig, ax = _fig_small(r"Components: $f(x)=\ln(x)+\sin(x)$ (domain $x>0$)")
    _plot_function(ax, x, y, r"$f(x)$")
    ax.legend(loc="best")
    return fig


# ------------------------------------------------------------
# Simulations (blackboard) — uses simulations.py as-is
# ------------------------------------------------------------
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
            teacher_explain_md=r"So there are **no turning points** (no sign change), but there is a break at the asymptote.",
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


# ------------------------------------------------------------
# Practice (clear, guided, aligned to objectives only)
# ------------------------------------------------------------
def _practice_asymptotes():
    st.markdown("### Practice Set 5.6.1 — Asymptotes (Rational Functions)")

    _md_math(r"""
**Q1.** For \(f(x)=\dfrac{2x^2-1}{x^2+4}\), what is the horizontal asymptote?

- A) \(y=0\)  
- B) \(y=1\)  
- C) \(y=2\)  
- D) No horizontal asymptote
""")
    ans = st.radio("Your answer (Q1)", ["A", "B", "C", "D"], index=None, key="p561_q1")
    if ans:
        if ans == "C":
            st.success(r"Correct. Degrees are equal (2 and 2), so HA is \(\frac{2}{1}=2\).")
        else:
            st.error("Not quite. Compare degrees and leading coefficients.")
        with st.expander("Hint + full answer"):
            _md_math(r"""
If \(\deg(P)=\deg(Q)\), then
$$
y=\frac{\text{leading coefficient of }P}{\text{leading coefficient of }Q}.
$$
So \(y=2\).
""")

    _md_math(r"""
**Q2.** For \(g(x)=\dfrac{x+3}{(x-1)(x+2)}\), which values give vertical asymptotes?

- A) \(x=1\) only  
- B) \(x=-2\) only  
- C) \(x=1\) and \(x=-2\)  
- D) No vertical asymptotes
""")
    ans2 = st.radio("Your answer (Q2)", ["A", "B", "C", "D"], index=None, key="p561_q2")
    if ans2:
        if ans2 == "C":
            st.success(r"Correct. Denominator is zero at \(x=1\) and \(x=-2\), and nothing cancels.")
        else:
            st.error("Check where the denominator becomes zero (and whether factors cancel).")
        with st.expander("Hint + full answer"):
            _md_math(r"""
Vertical asymptotes occur at zeros of the denominator **that do not cancel**:
\((x-1)(x+2)=0\Rightarrow x=1,\,-2\).
""")


def _practice_workflow_steps():
    st.markdown("### Practice Set 5.6.2 — Curve Sketching Steps")

    _md_math(r"""
**Q3.** Which option shows the correct order of the *core* curve-sketching steps?

- A) Derivatives → Sketch → Domain → Table → Asymptotes  
- B) Domain → Derivatives → Critical points → Concavity/Inflection → Table → Sketch  
- C) Table → Domain → Sketch → Derivatives → Concavity  
- D) Domain → Table → Sketch only
""")
    ans3 = st.radio("Your answer (Q3)", ["A", "B", "C", "D"], index=None, key="p562_q3")
    if ans3:
        if ans3 == "B":
            st.success("Correct. This matches the workflow in objective 5.6.2.")
        else:
            st.error("Not quite. Use domain first, then derivatives to control shape, then a small value table, then final sketch.")
        with st.expander("Why this order?"):
            _md_math(r"""
A reliable summary:

1) **Domain**  
2) **First & second derivative**  
3) **Critical values / first derivative test**  
4) **Inflection / concavity / second derivative test**  
5) **Overlap behaviour tables**  
6) **Table of values (few points)**  
7) **Sketch**
""")


def _practice_sketching_types():
    st.markdown("### Practice Set 5.6.3 — Sketching Different Function Types")

    _md_math(r"""
**Q4.** Which statement is true for \(f(x)=\sqrt{x-4}\)?

- A) Domain is all real numbers  
- B) Domain is \(x\ge 4\)  
- C) Domain is \(x\le 4\)  
- D) It has a vertical asymptote at \(x=4\)
""")
    ans4 = st.radio("Your answer (Q4)", ["A", "B", "C", "D"], index=None, key="p563_q4")
    if ans4:
        if ans4 == "B":
            st.success(r"Correct. \(\sqrt{x-4}\) needs \(x-4\ge 0\Rightarrow x\ge 4\).")
        else:
            st.error(r"Think: for radicals, the inside must be \(\ge 0\).")
        with st.expander("Hint + full answer"):
            _md_math(r"""
\(\sqrt{x-4}\) is defined when \(x-4\ge 0\Rightarrow x\ge 4\).  
At \(x=4\), \(f(4)=0\) (endpoint, not an asymptote).
""")

    _md_math(r"""
**Q5.** Which feature best describes \(h(x)=x^{2/3}\) at \(x=0\)?

- A) A smooth minimum  
- B) A cusp (sharp point)  
- C) A vertical asymptote  
- D) A hole (removable discontinuity)
""")
    ans5 = st.radio("Your answer (Q5)", ["A", "B", "C", "D"], index=None, key="p563_q5")
    if ans5:
        if ans5 == "B":
            st.success(r"Correct. \(x^{2/3}\) has a sharp point (cusp) at \(0\).")
        else:
            st.error("Look at the shape near \(x=0\): defined but not smooth.")
        with st.expander("Hint + full answer"):
            _md_math(r"""
\(x^{2/3}=(\sqrt[3]{x})^2\) is defined for all real \(x\), but near \(0\) the curve has a **cusp**.
""")


# ------------------------------------------------------------
# Main render()
# ------------------------------------------------------------
def render():
    st.header("Subtopic 5.6: Overview of Curve Sketching")
    st.caption("Source: Al Diwan – Grade 12 Advanced Stream Mathematics (Lesson 4.6)")

    st.markdown("### Lesson Objectives")
    _md_math(r"""
By the end of this subtopic, you should be able to:

- **5.6.1** Recall finding the **horizontal** and **vertical asymptotes** of a rational function.
- **5.6.2** Discuss and understand the **summary of steps** for curve sketching techniques:
  - domain  
  - first and second derivative  
  - critical values / first derivative test  
  - inflection values / concavity / second derivative test  
  - overlapping summary behaviour tables (variation + concavity)  
  - table of values for a few points  
  - sketching
- **5.6.3** Analyze and sketch graphs for different functions:
  - polynomials  
  - rational functions  
  - fractional powers of \(x\)  
  - radicals  
  - trig / exponential / logarithmic components
""")

    tabs = st.tabs(["Learn", "Simulations", "Practice"])

    # ---------------------- LEARN ----------------------
    with tabs[0]:
        _section(
            "5.6.1  Horizontal and vertical asymptotes (rational functions)",
            r"""
A **rational function** has the form
$$
f(x)=\frac{P(x)}{Q(x)}
$$
where \(P(x)\) and \(Q(x)\) are polynomials and \(Q(x)\neq 0\).

**Vertical asymptotes (VA)**  
A vertical asymptote occurs where the denominator is zero **and does not cancel**:
$$
Q(x)=0 \quad \text{(after simplifying)}
$$

**Horizontal asymptotes (HA)**  
Compare degrees:

- If \(\deg(P) < \deg(Q)\), then \(y=0\).
- If \(\deg(P) = \deg(Q)\), then
  $$
  y=\frac{\text{leading coefficient of }P}{\text{leading coefficient of }Q}.
  $$
- If \(\deg(P) > \deg(Q)\), then there is **no horizontal asymptote** (in this subtopic we only *recall* HA/VA).
""",
        )

        with st.expander("Mini example (asymptotes) — click to open"):
            _md_math(r"""
Let
$$
f(x)=\frac{x+1}{x-2}.
$$
- VA: \(x-2=0\Rightarrow x=2\) (no factor cancels)  
- HA: degrees equal \((1=1)\Rightarrow y=\frac{1}{1}=1\)
""")

        _section(
            "5.6.2  Curve sketching summary workflow",
            r"""
A curve sketch is a **controlled drawing**. The aim is to use quick analysis to predict the shape without plotting hundreds of points.

Use this workflow:

1) **Domain** (where can the function exist?)  
2) **First and second derivatives** (shape tools)  
3) **Critical values + first derivative test** (turning points + increasing/decreasing)  
4) **Inflection values + concavity + second derivative test**  
5) **Overlay behaviour tables**: variation + concavity together  
6) **Small table of values** for a few anchor points  
7) **Final sketch**
""",
        )

        cols = st.columns([1.15, 1])
        with cols[0]:
            _pill(
                "A simple ‘behaviour table’ idea",
                r"""
Make two short sign summaries:

- **Variation table** from \(f'(x)\) (increasing \(+\) / decreasing \(-\))  
- **Concavity table** from \(f''(x)\) (concave up \(+\) / concave down \(-\))

Then overlap them on the same intervals to know how the curve bends while it rises/falls.
""",
                kind="info",
            )
        with cols[1]:
            _pill(
                "What to write in your sketch notes",
                r"""
Always label:

- intercepts (where possible)
- turning points (from \(f'(x)=0\) and sign change)
- inflection points (from \(f''(x)=0\) and concavity change)
- asymptotes / domain breaks
""",
                kind="success",
            )

        _section(
            "5.6.3  Sketching different function families",
            r"""
Different functions require different **first checks**:

- **Polynomials:** domain is \(\mathbb{R}\). Shape controlled by degree and turning points.  
- **Rational:** check **domain**, **vertical asymptotes**, and end behaviour (horizontal asymptote when it exists).  
- **Fractional powers** (like \(x^{2/3}\)): can create **sharp points** (not smooth).  
- **Radicals** (like \(\sqrt{x-1}\)): domain often starts at an **endpoint**.  
- **Trig/exp/log components:** domain restrictions (e.g. \(\ln(x)\) needs \(x>0\)), and periodic behaviour for trig.
""",
        )

        st.markdown("#### Visual gallery (small, readable graphs)")
        gcols = st.columns(2)
        with gcols[0]:
            _small_plot(_plot_polynomial_example())
        with gcols[1]:
            _small_plot(_plot_rational_example())

        gcols2 = st.columns(2)
        with gcols2[0]:
            _small_plot(_plot_fractional_power_example())
        with gcols2[1]:
            _small_plot(_plot_radical_example())

        gcols3 = st.columns(1)
        with gcols3[0]:
            _small_plot(_plot_trig_exp_log_example())

        st.markdown("#### Quick ‘analysis card’ (choose an example)")
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
            _md_math(r"""
**Domain:** \(\mathbb{R}\)

**Key points (from derivatives):**  
\(f'(x)=3(x^2-1)\Rightarrow x=\pm 1\)  
Turning points: \((-1,2)\) (local max), \((1,-2)\) (local min)

**Concavity:** \(f''(x)=6x\Rightarrow\) inflection at \(x=0\) and concavity changes there.
""")
        elif "Rational" in choice:
            _md_math(r"""
**Domain:** \(x\neq 2\)

**Asymptotes:**  
Vertical: \(x=2\)  
Horizontal: degrees equal \(\Rightarrow y=1\)

**Derivatives:**  
\(f'(x)=\dfrac{-3}{(x-2)^2}<0\Rightarrow\) decreasing on both sides of \(2\).  
\(f''(x)=\dfrac{6}{(x-2)^3}\Rightarrow\) concave down for \(x<2\), concave up for \(x>2\).
""")
        elif "Fractional" in choice:
            _md_math(r"""
**Domain:** \(\mathbb{R}\)

**Key sketch feature:**  
\(f(x)=x^{2/3}\) is defined for all real \(x\), but it has a **sharp point (cusp)** at \(x=0\).  
That affects how you sketch near the origin.
""")
        elif "Radical" in choice:
            _md_math(r"""
**Domain:** for \(f(x)=\sqrt{x-1}\), require \(x-1\ge 0\Rightarrow x\ge 1\).

**Key sketch feature:**  
The graph **starts** at the endpoint \((1,0)\) and increases slowly.
""")
        else:
            _md_math(r"""
**Domain:** \(\ln(x)\) requires \(x>0\), so the whole function has domain \(x>0\).

**Key sketch feature:**  
\(\ln(x)\) grows slowly, while \(\sin(x)\) adds a small oscillation.  
Your sketch should show an overall rising trend with gentle waves.
""")

    # ------------------- SIMULATIONS -------------------
    with tabs[1]:
        st.markdown("### Blackboard simulations (step-by-step)")
        _md_math(r"""
Use **Start solving** to animate the board. The explanations on the right tell you exactly *why* each step matters.
""")
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
