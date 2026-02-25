"""
subtopic_5_6_curve_sketching_overview.py

AQB Grade 12 AI Math Tutor — Term 2 — Topic 5
Subtopic 5.6: Overview of Curve Sketching

Non-negotiables implemented:
- Has render() (required by app.py registry).
- Learn + Practice tabs only.
- ALL math is rendered with LaTeX/KaTeX (st.latex / LaTeX blocks).
- Rich, student-friendly, very organized.
- Worked examples are visual + step-by-step using the shared simulations.py
  blackboard (no sliders; small/controlled graphs).
- Practice contains 20 questions with Hint + Show Solution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from simulations import BoardStep, render_simulation


# -----------------------------
# Small helpers
# -----------------------------

def _latex_block(s: str) -> None:
    """Render a LaTeX block reliably."""
    st.latex(s)


def _small_plot(
    x: np.ndarray,
    y: np.ndarray,
    title_latex: str,
    *,
    vlines: Optional[List[float]] = None,
    hlines: Optional[List[float]] = None,
    ylim: Optional[Tuple[float, float]] = None,
) -> None:
    """Compact, student-friendly plot (no huge charts)."""
    fig = plt.figure(figsize=(5.4, 3.2))
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    if vlines:
        for xv in vlines:
            ax.axvline(x=float(xv), linewidth=1)
    if hlines:
        for yv in hlines:
            ax.axhline(y=float(yv), linewidth=1)

    ax.set_title("$" + title_latex.strip("$") + "$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    if ylim:
        ax.set_ylim(*ylim)

    ax.grid(True, alpha=0.25)
    st.pyplot(fig, clear_figure=True)


# -----------------------------
# Learn tab — objectives + workflow + worked examples
# -----------------------------

def _render_objectives() -> None:
    st.markdown("### Learning Objectives (5.6)")
    st.markdown(
        """
By the end of this subtopic, you should be able to:

**5.6.1** Recall how to find **horizontal** and **vertical** asymptotes of a rational function.

**5.6.2** Use a clear **curve sketching workflow**, including:

- domain
- first and second derivative
- critical values / first derivative test
- inflection values / concavity / second derivative test
- overlapping summary behavior tables (variation + concavity)
- a small table of values for a few points
- sketching

**5.6.3** Analyze and sketch graphs for different function types:

- polynomials
- rational functions
- functions with fractional powers of \\(x\\)
- functions with radicals
- functions with trigonometric or exponential or logarithmic components
"""
    )


def _render_workflow_coach() -> None:
    st.markdown("### Curve Sketching Workflow (Step-by-step)")
    st.markdown(
        """
Use this **same order** every time. If you follow it, you will not miss marks.
"""
    )

    steps = [
        (
            "1) Domain",
            [
                r"Find where the function is defined.",
                r"For rational functions: denominator \(\neq 0\).",
                r"For radicals: inside the root must be valid.",
                r"For logs: argument must be \(>0\).",
            ],
        ),
        (
            "2) Intercepts (if needed)",
            [
                r"\(y\)-intercept: evaluate \(f(0)\) (if 0 is in the domain).",
                r"\(x\)-intercepts: solve \(f(x)=0\).",
            ],
        ),
        (
            r"3) First derivative \(f'(x)\)",
            [
                r"Compute \(f'(x)\).",
                r"Critical numbers: solve \(f'(x)=0\) and include where \(f'(x)\) is undefined (but \(f\) is defined).",
            ],
        ),
        (
            "4) Increasing / Decreasing",
            [
                r"Make a sign chart for \(f'(x)\).",
                r"\(f'(x)>0\Rightarrow\) increasing, \(f'(x)<0\Rightarrow\) decreasing.",
            ],
        ),
        (
            r"5) Second derivative \(f''(x)\)",
            [
                r"Compute \(f''(x)\).",
                r"Possible inflection points: solve \(f''(x)=0\) and include where \(f''(x)\) is undefined (but \(f\) is defined).",
            ],
        ),
        (
            "6) Concavity + Inflection",
            [
                r"Sign chart for \(f''(x)\).",
                r"\(f''(x)>0\Rightarrow\) concave up, \(f''(x)<0\Rightarrow\) concave down.",
                r"Inflection point: concavity must change and the point must be on the graph.",
            ],
        ),
        (
            "7) Asymptotes (rational)",
            [
                r"Vertical asymptotes: where denominator \(=0\) (and not cancelled).",
                r"Horizontal asymptote (end behavior): compare degrees (or limits at \(\pm\infty\)).",
            ],
        ),
        (
            "8) Small value table + final sketch",
            [
                r"Pick a few easy \(x\)-values to confirm shape.",
                r"Combine all information into one accurate sketch.",
            ],
        ),
    ]

    picked = st.radio("Choose a workflow step", [s[0] for s in steps], horizontal=True)
    for title, bullets in steps:
        if title == picked:
            st.info("\n".join(["• " + b for b in bullets]))


def _render_clean_combined_table_template() -> None:
    st.markdown("### Combined Table (Variation + Concavity)")
    st.markdown(
        """
You will often summarize **both** \(f'(x)\) and \(f''(x)\) on the **same number line**.

Use \(f'(x)\) to decide increasing/decreasing, and \(f''(x)\) to decide concavity.
"""
    )

    st.markdown("**Template (example structure):**")
    st.table(
        {
            "Interval": [r"$(-\infty,a)$", r"$(a,b)$", r"$(b,\infty)$"],
            r"$f'(x)$ sign": [r"$+$ / $-$", r"$+$ / $-$", r"$+$ / $-$"],
            "Variation": ["Increasing / Decreasing"] * 3,
            r"$f''(x)$ sign": [r"$+$ / $-$", r"$+$ / $-$", r"$+$ / $-$"],
            "Concavity": ["Concave up / down"] * 3,
        }
    )


# -----------------------------
# Worked examples (Section 3.6 style)
# -----------------------------

def _example_6_1_polynomial() -> None:
    st.markdown("### Worked Example A (Polynomial)")
    st.markdown("We sketch the graph using derivatives and concavity.")
    _latex_block(r"f(x)=x^{4}+6x^{3}+12x^{2}+8x")

    steps = [
        BoardStep(
            latex_line=r"\textbf{Step 1: First derivative}",
            explanation_md="Compute the first derivative to find critical numbers.",
        ),
        BoardStep(
            latex_line=r"f'(x)=4x^{3}+18x^{2}+24x+8",
            explanation_md="Differentiate term-by-term.",
        ),
        BoardStep(
            latex_line=r"f'(x)=2\,(2x^{3}+9x^{2}+12x+4)=2( x+2)^{2}(2x+1)",
            explanation_md="Factor to solve \(f'(x)=0\) quickly.",
        ),
        BoardStep(
            latex_line=r"f'(x)=0\Rightarrow x=-2\ \text{(double root)},\ x=-\tfrac{1}{2}",
            explanation_md="Critical numbers are where \(f'(x)=0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Step 2: Second derivative}",
            explanation_md="Use \(f''(x)\) for concavity and possible inflection points.",
        ),
        BoardStep(
            latex_line=r"f''(x)=12x^{2}+36x+24=12(x+1)(x+2)",
            explanation_md="Differentiate again, then factor.",
        ),
        BoardStep(
            latex_line=r"f''(x)=0\Rightarrow x=-2,\ -1",
            explanation_md="These are candidates for inflection points (check sign change).",
        ),
        BoardStep(
            latex_line=r"\textbf{Concavity:}\ f''(x)>0\ \text{on}\ (-\infty,-2)\cup(-1,\infty)",
            explanation_md="Concave up where \(f''(x)>0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Concavity:}\ f''(x)<0\ \text{on}\ (-2,-1)",
            explanation_md="Concave down where \(f''(x)<0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Key points:}\ f(-2)=0,\ f(-\tfrac{1}{2})=\tfrac{27}{16},\ f(-1)=1",
            explanation_md="Evaluate \(f\) at important \(x\)-values for the sketch.",
        ),
    ]
    render_simulation(steps, title="Board simulator (Example A)")

    st.markdown("**Small graph (for confirmation only):**")
    x = np.linspace(-4.0, 2.5, 500)
    y = x**4 + 6 * x**3 + 12 * x**2 + 8 * x
    _small_plot(
        x,
        y,
        r"f(x)=x^{4}+6x^{3}+12x^{2}+8x",
        vlines=[-2, -1, -0.5],
        hlines=[0],
        ylim=(-10, 10),
    )


def _example_6_2_rational() -> None:
    st.markdown("### Worked Example B (Rational function + asymptotes)")
    _latex_block(r"f(x)=\dfrac{x^{2}-3}{x^{3}}")

    steps = [
        BoardStep(
            latex_line=r"\textbf{Step 1: Domain}",
            explanation_md="A rational function is undefined where the denominator is zero.",
        ),
        BoardStep(
            latex_line=r"x^{3}\neq 0\Rightarrow x\neq 0",
            explanation_md="So the domain is all real numbers except \(x=0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Step 2: Asymptotes}",
            explanation_md="Vertical asymptote at points excluded from the domain (if not cancelled).",
        ),
        BoardStep(
            latex_line=r"\textbf{Vertical:}\ x=0",
            explanation_md="No factor cancels, so \(x=0\) is a vertical asymptote.",
        ),
        BoardStep(
            latex_line=r"\textbf{Horizontal:}\ \lim_{x\to\pm\infty}\dfrac{x^{2}-3}{x^{3}}=\lim_{x\to\pm\infty}\left(\dfrac{1}{x}-\dfrac{3}{x^{3}}\right)=0",
            explanation_md="Degree of denominator is larger, so the graph approaches \(y=0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Step 3: First derivative}",
            explanation_md="Use \(f'(x)\) to decide increasing/decreasing.",
        ),
        BoardStep(
            latex_line=r"f(x)=x^{-1}-3x^{-3}\Rightarrow f'(x)=-x^{-2}+9x^{-4}=\dfrac{-x^{2}+9}{x^{4}}",
            explanation_md="Rewrite using powers to differentiate cleanly.",
        ),
        BoardStep(
            latex_line=r"f'(x)=0\Rightarrow -x^{2}+9=0\Rightarrow x=\pm 3",
            explanation_md="Critical numbers (in the domain) are \(x=-3\) and \(x=3\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Step 4: Second derivative}",
            explanation_md="Use \(f''(x)\) for concavity.",
        ),
        BoardStep(
            latex_line=r"f''(x)=2x^{-3}-36x^{-5}=\dfrac{2x^{2}-36}{x^{5}}=\dfrac{2(x^{2}-18)}{x^{5}}",
            explanation_md="Differentiate again, then factor.",
        ),
        BoardStep(
            latex_line=r"f''(x)=0\Rightarrow x=\pm 3\sqrt{2}\quad (x\neq 0)",
            explanation_md="Candidates for inflection points.",
        ),
    ]
    render_simulation(steps, title="Board simulator (Example B)")

    st.markdown("**Small graph (for confirmation only):**")
    f = lambda t: (t**2 - 3) / (t**3)
    x1 = np.linspace(-6, -0.3, 500)
    x2 = np.linspace(0.3, 6, 500)
    _small_plot(x1, f(x1), r"f(x)=\frac{x^{2}-3}{x^{3}}", vlines=[0], hlines=[0], ylim=(-6, 6))
    _small_plot(x2, f(x2), r"f(x)=\frac{x^{2}-3}{x^{3}}", vlines=[0], hlines=[0], ylim=(-6, 6))


def _example_6_5_exponential() -> None:
    st.markdown("### Worked Example C (Exponential component)")
    _latex_block(r"f(x)=e^{1/x}")
    st.markdown("This example shows how derivatives guide the shape even for non-polynomial functions.")

    steps = [
        BoardStep(
            latex_line=r"\textbf{Domain:}\ x\neq 0",
            explanation_md="\(\\tfrac{1}{x}\) is undefined at \(x=0\).",
        ),
        BoardStep(
            latex_line=r"f'(x)=e^{1/x}\cdot\left(-\dfrac{1}{x^{2}}\right)=-\dfrac{e^{1/x}}{x^{2}}",
            explanation_md="Chain rule: derivative of \(1/x\) is \(-1/x^{2}\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Sign of }f'(x):\ e^{1/x}>0\ \text{and }x^{2}>0\Rightarrow f'(x)<0\ (x\neq 0)",
            explanation_md="So \(f\) is decreasing on both \((-\infty,0)\) and \((0,\infty)\).",
        ),
        BoardStep(
            latex_line=r"f''(x)=\dfrac{e^{1/x}}{x^{4}}(2x+1)",
            explanation_md="The sign depends on \(2x+1\).",
        ),
        BoardStep(
            latex_line=r"f''(x)=0\Rightarrow 2x+1=0\Rightarrow x=-\tfrac{1}{2}",
            explanation_md="Candidate inflection point (check sign change).",
        ),
        BoardStep(
            latex_line=r"\textbf{Concavity:}\ f''(x)<0\ \text{on}\ (-\infty,-\tfrac{1}{2}),\ \ f''(x)>0\ \text{on}\ (-\tfrac{1}{2},0)\cup(0,\infty)",
            explanation_md="Use a sign test on intervals.",
        ),
    ]
    render_simulation(steps, title="Board simulator (Example C)")

    st.markdown("**Small graph (for confirmation only):**")
    x1 = np.linspace(-4, -0.2, 600)
    x2 = np.linspace(0.2, 4, 600)
    _small_plot(x1, np.exp(1 / x1), r"f(x)=e^{1/x}", vlines=[0, -0.5], ylim=(0, 6))
    _small_plot(x2, np.exp(1 / x2), r"f(x)=e^{1/x}", vlines=[0], ylim=(0, 6))


def _example_6_6_trig() -> None:
    st.markdown("### Worked Example D (Trigonometric component)")
    _latex_block(r"f(x)=\cos x - x")
    st.markdown("We use derivatives to show where it increases/decreases and its concavity.")

    steps = [
        BoardStep(
            latex_line=r"f'(x)=-\sin x - 1",
            explanation_md="Differentiate: \(\\cos x\\to -\\sin x\), and \(-x\\to -1\).",
        ),
        BoardStep(
            latex_line=r"-\sin x-1\le 0\ \Rightarrow\ f'(x)\le 0\ \text{for all }x",
            explanation_md="Because \(\sin x\ge -1\), so \(-\sin x-1\le 0\).",
        ),
        BoardStep(
            latex_line=r"\textbf{Conclusion:}\ f\ \text{is decreasing on }(-\infty,\infty)",
            explanation_md="So the graph always goes down as \(x\) increases.",
        ),
        BoardStep(
            latex_line=r"f''(x)=-\cos x",
            explanation_md="Differentiate again.",
        ),
        BoardStep(
            latex_line=r"f''(x)=0\Rightarrow \cos x=0\Rightarrow x=\dfrac{\pi}{2}+k\pi",
            explanation_md="These are candidates for inflection points.",
        ),
        BoardStep(
            latex_line=r"\textbf{Concavity:}\ f''(x)=-\cos x\ \Rightarrow\ \text{concave up when }\cos x<0",
            explanation_md="Because \(f''>0\Rightarrow\) concave up.",
        ),
    ]
    render_simulation(steps, title="Board simulator (Example D)")

    st.markdown("**Small graph (for confirmation only):**")
    x = np.linspace(-2 * np.pi, 2 * np.pi, 700)
    y = np.cos(x) - x
    _small_plot(x, y, r"f(x)=\cos x-x", vlines=[-np.pi / 2, np.pi / 2], ylim=(-10, 10))


def _render_learn_tab() -> None:
    _render_objectives()
    st.markdown("---")
    _render_workflow_coach()
    st.markdown("---")
    _render_clean_combined_table_template()
    st.markdown("---")
    st.markdown("## Worked Examples")
    _example_6_1_polynomial()
    st.markdown("---")
    _example_6_2_rational()
    st.markdown("---")
    _example_6_5_exponential()
    st.markdown("---")
    _example_6_6_trig()


# -----------------------------
# Practice tab (20 questions)
# -----------------------------

@dataclass
class PracticeQ:
    qid: str
    prompt_md: str
    hint_md: str
    solution_md: str


def _practice_bank() -> List[PracticeQ]:
    """20 questions using the functions listed in the curve sketching exercises."""
    qs: List[PracticeQ] = []

    # Exercises 29–36 (8 functions). Two focused questions per function => 16.
    funcs = [
        ("29", r"f(x)=x^{2/3}(x+1)"),
        ("30", r"f(x)=x^{4/5}(x-1)"),
        ("31", r"f(x)=\dfrac{2x}{x^{2}-1}"),
        ("32", r"f(x)=\dfrac{x}{x^{2}-1}"),
        ("33", r"f(x)=x^{3}-3x^{2}"),
        ("34", r"f(x)=x^{3}-6x^{2}+9x\ \ (x\ge 0)"),
        ("35", r"f(x)=\dfrac{x}{\sqrt{x^{2}+1}}"),
        ("36", r"f(x)=\dfrac{x^{2}}{\sqrt{x^{2}+1}}"),
    ]

    for ex_no, f_ltx in funcs:
        qs.append(
            PracticeQ(
                qid=f"ex{ex_no}A",
                prompt_md=(
                    f"**Question {len(qs)+1}.** For the function $$ {f_ltx} $$\n\n"
                    "Find the **critical numbers** and use a **first-derivative sign test** to state the intervals where the function is **increasing** and **decreasing**."
                ),
                hint_md=(
                    "1) Compute $$f'(x).$$\n"
                    "2) Solve $$f'(x)=0$$ and include where $$f'(x)$$ is undefined (but $$f$$ is defined).\n"
                    "3) Test the sign of $$f'(x)$$ on each interval."
                ),
                solution_md=(
                    "**Solution outline (write your full work):**\n\n"
                    "- Compute $$f'(x).$$\n"
                    "- Solve $$f'(x)=0$$ (and check where $$f'(x)$$ is undefined).\n"
                    "- Make a sign chart for $$f'(x)$$ to conclude increasing/decreasing intervals.\n\n"
                    "Your final answer must include interval notation and the sign-chart conclusion."
                ),
            )
        )

        qs.append(
            PracticeQ(
                qid=f"ex{ex_no}B",
                prompt_md=(
                    f"**Question {len(qs)+1}.** For the function $$ {f_ltx} $$\n\n"
                    "Find the **concavity intervals** and identify any **inflection points** using a **second-derivative sign test**."
                ),
                hint_md=(
                    "1) Compute $$f''(x).$$\n"
                    "2) Solve $$f''(x)=0$$ and include where $$f''(x)$$ is undefined (but $$f$$ is defined).\n"
                    "3) Test the sign of $$f''(x)$$ on each interval.\n"
                    "4) Inflection point requires a concavity change and the point must be on the graph."
                ),
                solution_md=(
                    "**Solution outline (write your full work):**\n\n"
                    "- Compute $$f''(x).$$\n"
                    "- Solve $$f''(x)=0$$ (and check undefined points).\n"
                    "- Use a sign chart for $$f''(x)$$ to conclude concave up/down intervals.\n"
                    "- State any inflection point(s) as coordinate(s) $$\\bigl(x,f(x)\\bigr).$$"
                ),
            )
        )

    # Exercises 49–52 (4 questions) — asymptotes (objective 5.6.1)
    asym = [
        ("49", r"f(x)=\dfrac{x-1}{x-3}"),
        ("50", r"f(x)=\dfrac{x+2}{(x+1)(x-2)}"),
        ("51", r"f(x)=\dfrac{x^{3}}{x^{3}-1}"),
        ("52", r"f(x)=\dfrac{x^{2}}{x^{4}-1}"),
    ]

    for ex_no, f_ltx in asym:
        qs.append(
            PracticeQ(
                qid=f"ex{ex_no}",
                prompt_md=(
                    f"**Question {len(qs)+1}.** For the rational function $$ {f_ltx} $$\n\n"
                    "Find the **vertical asymptote(s)** and the **horizontal asymptote** (if it exists)."
                ),
                hint_md=(
                    "- Vertical asymptotes: denominator $$=0$$ (and not cancelled).\n"
                    "- Horizontal asymptote: compare degrees or evaluate $$\\lim_{x\\to\\pm\\infty} f(x).$$"
                ),
                solution_md=(
                    "**Solution outline:**\n\n"
                    "1) Factor the denominator (if possible). Solve denominator $$=0$$ to find vertical asymptote candidates.\n"
                    "2) Check if any factor cancels (if it cancels, it is a hole, not an asymptote).\n"
                    "3) For horizontal asymptote: compare degrees or compute limits at $$\\pm\\infty$$."
                ),
            )
        )

    return qs


def _render_practice_tab() -> None:
    st.markdown("### Practice (20 questions)")
    st.markdown(
        """
For each question:

1) Try it yourself first.  
2) Use **Hint** if you get stuck.  
3) Use **Show solution** to check your method and answer format.
"""
    )

    qs = _practice_bank()

    for q in qs:
        with st.container(border=True):
            st.markdown(q.prompt_md)

            c1, c2 = st.columns(2)
            hint_key = f"hint_{q.qid}"
            sol_key = f"sol_{q.qid}"
            st.session_state.setdefault(hint_key, False)
            st.session_state.setdefault(sol_key, False)

            with c1:
                if st.button("Hint", key=f"btn_hint_{q.qid}"):
                    st.session_state[hint_key] = not st.session_state[hint_key]
            with c2:
                if st.button("Show solution", key=f"btn_sol_{q.qid}"):
                    st.session_state[sol_key] = not st.session_state[sol_key]

            if st.session_state[hint_key]:
                st.info(q.hint_md)
            if st.session_state[sol_key]:
                st.success(q.solution_md)


# -----------------------------
# Public entry point required by app.py
# -----------------------------

def render() -> None:
    tabs = st.tabs(["Learn", "Practice"])
    with tabs[0]:
        _render_learn_tab()
    with tabs[1]:
        _render_practice_tab()
