# subtopic_5_6_curve_sketching_overview.py
# AQB Grade 12 AI Math Tutor — Term 2 — Topic 5
# Subtopic 5.6: Overview of Curve Sketching
#
# NON-NEGOTIABLES satisfied:
# - render() provided
# - No sliders
# - All math is LaTeX/KaTeX (every formula/expression/notation)
# - Learn + Practice tabs only
# - Graphs kept small and readable
# - Content aligned to objectives 5.6.1–5.6.3 and Chapter 3 (Section 3.6) exercises/examples

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


# -----------------------------
# Small helpers (LaTeX everywhere)
# -----------------------------
def _md(s: str) -> None:
    st.markdown(s)


def _latex(s: str) -> None:
    # Always pass raw LaTeX without wrapping $$ to avoid double-wrapping mistakes.
    st.latex(s)


def _inline_math(text: str) -> str:
    # Convenience when building markdown lines that include inline LaTeX.
    return text


def _small_plot(
    f: Callable[[np.ndarray], np.ndarray],
    x_min: float,
    x_max: float,
    title_latex: str,
    *,
    y_clip: float | None = None,
    vlines: List[float] | None = None,
    hlines: List[float] | None = None,
) -> None:
    x = np.linspace(x_min, x_max, 800)
    with np.errstate(all="ignore"):
        y = f(x)

    if y_clip is not None:
        y = np.clip(y, -y_clip, y_clip)

    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    # Axes lines
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    if vlines:
        for xv in vlines:
            ax.axvline(xv, linestyle="--", linewidth=1)
    if hlines:
        for yv in hlines:
            ax.axhline(yv, linestyle="--", linewidth=1)

    ax.set_title("")  # keep clean; title shown via LaTeX above
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)
    st.write(_inline_math(title_latex))
    st.pyplot(fig, clear_figure=True)


def _safe_button(label: str, key: str) -> bool:
    return st.button(label, key=key, use_container_width=True)


def _katex_text_block(lines_latex: List[str], *, box_title: str | None = None) -> None:
    """
    A clean "board-like" box that renders math line-by-line using st.latex (KaTeX).
    """
    st.markdown(
        """
<style>
.aqb-board{
  background:#0f1216;
  border:1px solid rgba(255,255,255,0.10);
  border-radius:14px;
  padding:16px 16px 10px 16px;
}
.aqb-board h4{
  margin:0 0 12px 0;
  color:#e8eefc;
  font-weight:700;
  font-size:16px;
}
</style>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="aqb-board">', unsafe_allow_html=True)
    if box_title:
        st.markdown(f"<h4>{box_title}</h4>", unsafe_allow_html=True)
    for line in lines_latex:
        _latex(line)
    st.markdown("</div>", unsafe_allow_html=True)


def _sign_table(
    intervals_latex: List[str],
    sign_fprime_latex: List[str],
    behavior_latex: List[str],
    sign_f2_latex: List[str],
    concavity_latex: List[str],
) -> None:
    """
    Readable table (no overlap): rendered row-by-row with Streamlit columns.
    Every cell is LaTeX.
    """
    st.markdown(
        """
<style>
.aqb-table-head{
  font-weight:700;
  padding:8px 10px;
  border-radius:10px;
  background: rgba(30, 80, 170, 0.08);
  border: 1px solid rgba(30, 80, 170, 0.18);
  margin-bottom:6px;
}
.aqb-table-row{
  padding:10px 8px;
  border-bottom:1px solid rgba(0,0,0,0.08);
}
</style>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns([1.2, 1.0, 1.2, 1.0, 1.3])
    with c1:
        st.markdown('<div class="aqb-table-head">Interval</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="aqb-table-head">$f\'(x)$ sign</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="aqb-table-head">Behavior</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="aqb-table-head">$f\'\'(x)$ sign</div>', unsafe_allow_html=True)
    with c5:
        st.markdown('<div class="aqb-table-head">Concavity</div>', unsafe_allow_html=True)

    n = len(intervals_latex)
    for i in range(n):
        r1, r2, r3, r4, r5 = st.columns([1.2, 1.0, 1.2, 1.0, 1.3])
        with r1:
            _latex(intervals_latex[i])
        with r2:
            _latex(sign_fprime_latex[i])
        with r3:
            _latex(behavior_latex[i])
        with r4:
            _latex(sign_f2_latex[i])
        with r5:
            _latex(concavity_latex[i])


# -----------------------------
# Content models
# -----------------------------
@dataclass
class WorkedExample:
    title: str
    question_lines_md: List[str]
    solution_lines_latex: List[str]
    plot_fn: Callable[[np.ndarray], np.ndarray]
    plot_window: Tuple[float, float]
    plot_title_latex: str
    plot_yclip: float | None = None
    vlines: List[float] | None = None
    hlines: List[float] | None = None


@dataclass
class PracticeItem:
    q_latex: str
    hint_lines_latex: List[str]
    sol_lines_latex: List[str]
    # Optional small plot
    plot_fn: Callable[[np.ndarray], np.ndarray] | None = None
    plot_window: Tuple[float, float] | None = None
    plot_title_latex: str | None = None
    plot_yclip: float | None = None
    vlines: List[float] | None = None
    hlines: List[float] | None = None


# -----------------------------
# Chapter 3 (Section 3.6) aligned examples
# (Exercises 3.6 include these exact functions)
# -----------------------------
def _examples() -> List[WorkedExample]:
    # Example A (polynomial) — Exercise 3.6 #1
    def f1(x: np.ndarray) -> np.ndarray:
        return x**3 - 3 * x**2 + 3 * x

    ex1 = WorkedExample(
        title="Example 1 — Polynomial (complete discussion)",
        question_lines_md=[
            "**Question.** Consider the function $f(x)=x^{3}-3x^{2}+3x$.",
            "**Task.**",
            "1. Find the critical numbers (solve $f'(x)=0$ and include where $f'(x)$ is undefined if it happens).",
            "2. Determine intervals of increase/decrease using the sign of $f'(x)$.",
            "3. Find possible inflection $x$-values (solve $f''(x)=0$ and include where $f''(x)$ is undefined if it happens).",
            "4. Determine concavity and any inflection point(s) using the sign of $f''(x)$.",
            "5. Sketch a representative graph using the information above.",
        ],
        solution_lines_latex=[
            r"f(x)=x^{3}-3x^{2}+3x",
            r"f'(x)=3x^{2}-6x+3=3(x^{2}-2x+1)=3(x-1)^{2}",
            r"f'(x)=0 \;\Rightarrow\; x=1",
            r"\text{Since }(x-1)^{2}\ge 0,\;\; f'(x)=3(x-1)^{2}\ge 0\text{ for all }x",
            r"\text{So }f\text{ is increasing on }(-\infty,\infty)\text{ (no decreasing interval).}",
            r"f''(x)=6x-6=6(x-1)",
            r"f''(x)=0\;\Rightarrow\; x=1",
            r"\text{If }x<1,\; f''(x)<0\Rightarrow \text{concave down.}\qquad \text{If }x>1,\; f''(x)>0\Rightarrow \text{concave up.}",
            r"\text{Therefore, }x=1\text{ is an inflection point.}",
            r"f(1)=1-3+3=1\;\Rightarrow\;\text{Inflection point }(1,1).",
        ],
        plot_fn=f1,
        plot_window=(-2.5, 4.5),
        plot_title_latex=r"$f(x)=x^{3}-3x^{2}+3x$",
        plot_yclip=25,
        vlines=[1.0],
    )

    # Example B (rational) — Exercise 3.6 #9 (shows vertical/horizontal asymptotes)
    def f9(x: np.ndarray) -> np.ndarray:
        return (2 * x) / (x**2 - 1)

    ex2 = WorkedExample(
        title="Example 2 — Rational (asymptotes + derivatives)",
        question_lines_md=[
            "**Question.** Consider the function $f(x)=\\dfrac{2x}{x^{2}-1}$.",
            "**Task.**",
            "1. Find the domain and any vertical asymptote(s).",
            "2. Determine the horizontal asymptote (if it exists).",
            "3. Find $f'(x)$ and use it to decide increase/decrease.",
            "4. Find $f''(x)$ and use it to decide concavity (optional check with a small sketch).",
        ],
        solution_lines_latex=[
            r"f(x)=\dfrac{2x}{x^{2}-1}",
            r"\text{Domain: }x^{2}-1\ne 0\Rightarrow x\ne -1,\;x\ne 1",
            r"\text{Vertical asymptotes: }x=-1,\;x=1",
            r"\text{Since }\deg(\text{numerator})<\deg(\text{denominator}),\;\;\lim_{x\to\pm\infty}f(x)=0\Rightarrow \text{horizontal asymptote }y=0",
            r"f'(x)=\dfrac{2(x^{2}-1)-2x(2x)}{(x^{2}-1)^{2}}=\dfrac{-2x^{2}-2}{(x^{2}-1)^{2}}=-\dfrac{2(x^{2}+1)}{(x^{2}-1)^{2}}",
            r"\text{Because }x^{2}+1>0\text{ and }(x^{2}-1)^{2}>0\text{ on the domain, we have }f'(x)<0",
            r"\Rightarrow\; f\text{ is decreasing on }(-\infty,-1),\;(-1,1),\;(1,\infty).",
        ],
        plot_fn=f9,
        plot_window=(-4.0, 4.0),
        plot_title_latex=r"$f(x)=\dfrac{2x}{x^{2}-1}$",
        plot_yclip=8,
        vlines=[-1.0, 1.0],
        hlines=[0.0],
    )

    # Example C (radical) — Exercise 3.6 #16
    def f16(x: np.ndarray) -> np.ndarray:
        # sqrt(2x - 1), domain x >= 1/2
        y = np.where(2 * x - 1 >= 0, np.sqrt(2 * x - 1), np.nan)
        return y

    ex3 = WorkedExample(
        title="Example 3 — Radical (domain + shape)",
        question_lines_md=[
            "**Question.** Consider the function $f(x)=\\sqrt{2x-1}$.",
            "**Task.**",
            "1. Find the domain.",
            "2. Find $f'(x)$ (where it exists) and describe where the function increases/decreases.",
            "3. Sketch a representative graph.",
        ],
        solution_lines_latex=[
            r"f(x)=\sqrt{2x-1}",
            r"\text{Domain: }2x-1\ge 0\Rightarrow x\ge \dfrac12",
            r"f'(x)=\dfrac{1}{2\sqrt{2x-1}}\cdot 2=\dfrac{1}{\sqrt{2x-1}}",
            r"\text{For }x>\dfrac12,\;\sqrt{2x-1}>0\Rightarrow f'(x)>0\Rightarrow \text{increasing on }\left(\dfrac12,\infty\right)",
            r"\text{At }x=\dfrac12,\;f\left(\dfrac12\right)=0\text{ and the graph starts there.}",
        ],
        plot_fn=f16,
        plot_window=(0.0, 6.0),
        plot_title_latex=r"$f(x)=\sqrt{2x-1}$",
        plot_yclip=None,
        vlines=[0.5],
    )

    # Example D (fractional powers) — Exercise 3.6 #19
    def f19(x: np.ndarray) -> np.ndarray:
        # x^(5/3) - 5 x^(2/3). Use real cube root handling:
        # x^(2/3) = (|x|^(2/3)), x^(5/3) = x*|x|^(2/3)
        a = np.abs(x) ** (2.0 / 3.0)
        return x * a - 5 * a

    ex4 = WorkedExample(
        title="Example 4 — Fractional powers (shape + key points)",
        question_lines_md=[
            "**Question.** Consider the function $f(x)=x^{5/3}-5x^{2/3}$.",
            "**Task.**",
            "1. State the domain.",
            "2. Compute $f'(x)$ (where it exists) and find critical numbers.",
            "3. Use sign testing to describe increase/decrease.",
            "4. Sketch a representative graph.",
        ],
        solution_lines_latex=[
            r"f(x)=x^{5/3}-5x^{2/3}",
            r"\text{Domain: }x^{2/3}\text{ is defined for all real }x\Rightarrow (-\infty,\infty)",
            r"f'(x)=\dfrac{5}{3}x^{2/3}-5\cdot\dfrac{2}{3}x^{-1/3}=\dfrac{5}{3}x^{2/3}-\dfrac{10}{3}x^{-1/3}",
            r"\text{Critical numbers come from }f'(x)=0\text{ or }f'(x)\text{ undefined.}",
            r"f'(x)\text{ is undefined at }x=0\text{ (because }x^{-1/3}\text{).}",
            r"f'(x)=0\Rightarrow \dfrac{5}{3}x^{2/3}=\dfrac{10}{3}x^{-1/3}\Rightarrow x^{2/3}\cdot x^{1/3}=2\Rightarrow x=2",
            r"\text{So test intervals }(-\infty,0),\;(0,2),\;(2,\infty)\text{ using the sign of }f'(x).",
        ],
        plot_fn=f19,
        plot_window=(-6.0, 6.0),
        plot_title_latex=r"$f(x)=x^{5/3}-5x^{2/3}$",
        plot_yclip=30,
        vlines=[0.0, 2.0],
    )

    # Example E (trig + linear) — Exercise 3.6 #11
    def f11(x: np.ndarray) -> np.ndarray:
        return x + np.sin(x)

    ex5 = WorkedExample(
        title="Example 5 — Trig component (derivative controls shape)",
        question_lines_md=[
            "**Question.** Consider the function $f(x)=x+\\sin x$.",
            "**Task.**",
            "1. Compute $f'(x)$ and explain why the function increases on all real numbers.",
            "2. Compute $f''(x)$ and describe concavity intervals.",
            "3. Sketch a representative graph.",
        ],
        solution_lines_latex=[
            r"f(x)=x+\sin x",
            r"f'(x)=1+\cos x",
            r"\text{Since }-1\le \cos x\le 1,\;\;0\le 1+\cos x\le 2\Rightarrow f'(x)\ge 0",
            r"\Rightarrow\; f\text{ is increasing on }(-\infty,\infty)",
            r"f''(x)=-\sin x",
            r"\text{Concave up when }-\sin x>0\Rightarrow \sin x<0,\;\;\text{concave down when }\sin x>0.",
        ],
        plot_fn=f11,
        plot_window=(-8.0, 8.0),
        plot_title_latex=r"$f(x)=x+\sin x$",
        plot_yclip=15,
        vlines=None,
    )

    return [ex1, ex2, ex3, ex4, ex5]


# -----------------------------
# Practice bank (Exercises 3.6, #1–#22)
# At least 20 items, each with Hint + Solution
# -----------------------------
def _practice_items() -> List[PracticeItem]:
    items: List[PracticeItem] = []

    # For consistency, each hint references the workflow (domain, asymptotes if rational,
    # f'(x), critical numbers, sign chart, f''(x), inflection, sketch).
    def hint_workflow(extra: List[str] | None = None) -> List[str]:
        base = [
            r"\text{Use the workflow: domain } \rightarrow \text{ intercepts } \rightarrow f'(x) \rightarrow \text{ critical numbers } \rightarrow \text{ sign chart } \rightarrow f''(x) \rightarrow \text{ concavity } \rightarrow \text{ sketch.}",
        ]
        return base + (extra or [])

    # 1) x^3 - 3x^2 + 3x
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q1. } f(x)=x^{3}-3x^{2}+3x",
            hint_lines_latex=hint_workflow([r"\text{Compute }f'(x)\text{ and notice a perfect square.}"]),
            sol_lines_latex=[
                r"f'(x)=3(x-1)^{2}\Rightarrow f'(x)\ge 0\Rightarrow \text{increasing on }(-\infty,\infty)",
                r"f''(x)=6(x-1)\Rightarrow \text{inflection at }x=1,\;\;f(1)=1\Rightarrow (1,1).",
            ],
        )
    )

    # 2) x^4 - 3x^2 + 2
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q2. } f(x)=x^{4}-3x^{2}+2",
            hint_lines_latex=hint_workflow([r"\text{Factor }f'(x)\text{ and use symmetry (even function).}"]),
            sol_lines_latex=[
                r"f'(x)=4x^{3}-6x=2x(2x^{2}-3)\Rightarrow x=0,\;x=\pm \sqrt{\dfrac{3}{2}}",
                r"f''(x)=12x^{2}-6=6(2x^{2}-1)\Rightarrow x=\pm \dfrac{1}{\sqrt{2}} \text{ candidates for inflection.}",
            ],
        )
    )

    # 3) x^5 - 2x^3 + 1
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q3. } f(x)=x^{5}-2x^{3}+1",
            hint_lines_latex=hint_workflow([r"\text{Factor }f'(x)=x^{2}(\cdots).}"]),
            sol_lines_latex=[
                r"f'(x)=5x^{4}-6x^{2}=x^{2}(5x^{2}-6)\Rightarrow x=0,\;x=\pm \sqrt{\dfrac{6}{5}}",
                r"f''(x)=20x^{3}-12x=4x(5x^{2}-3)\Rightarrow x=0,\;x=\pm \sqrt{\dfrac{3}{5}}",
            ],
        )
    )

    # 4) x^4 + 4x^3 - 1
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q4. } f(x)=x^{4}+4x^{3}-1",
            hint_lines_latex=hint_workflow([r"\text{Factor }f'(x)=4x^{2}(\cdots).}"]),
            sol_lines_latex=[
                r"f'(x)=4x^{3}+12x^{2}=4x^{2}(x+3)\Rightarrow x=0,\;x=-3",
                r"f''(x)=12x^{2}+24x=12x(x+2)\Rightarrow x=0,\;x=-2",
            ],
        )
    )

    # 5) (x+4)/x
    def f5(x: np.ndarray) -> np.ndarray:
        return (x + 4) / x

    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q5. } f(x)=\dfrac{x+4}{x}",
            hint_lines_latex=hint_workflow([r"\text{Domain excludes }x=0.\;\;\text{Rewrite }f(x)=1+\dfrac{4}{x}."]),
            sol_lines_latex=[
                r"f(x)=1+\dfrac{4}{x}\Rightarrow x=0\text{ is a vertical asymptote, }y=1\text{ is a horizontal asymptote.}",
                r"f'(x)=-\dfrac{4}{x^{2}}<0\Rightarrow \text{decreasing on }(-\infty,0)\text{ and }(0,\infty).",
            ],
            plot_fn=f5,
            plot_window=(-6.0, 6.0),
            plot_title_latex=r"$f(x)=\dfrac{x+4}{x}$",
            plot_yclip=10,
            vlines=[0.0],
            hlines=[1.0],
        )
    )

    # 6) (x^2-1)/x
    def f6(x: np.ndarray) -> np.ndarray:
        return (x**2 - 1) / x

    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q6. } f(x)=\dfrac{x^{2}-1}{x}",
            hint_lines_latex=hint_workflow([r"\text{Rewrite }f(x)=x-\dfrac{1}{x}\text{ and use }x\ne 0."]),
            sol_lines_latex=[
                r"f(x)=x-\dfrac{1}{x}\Rightarrow x=0\text{ is a vertical asymptote (no horizontal asymptote here).}",
                r"f'(x)=1+\dfrac{1}{x^{2}}>0\Rightarrow \text{increasing on }(-\infty,0)\text{ and }(0,\infty).",
            ],
            plot_fn=f6,
            plot_window=(-6.0, 6.0),
            plot_title_latex=r"$f(x)=\dfrac{x^{2}-1}{x}$",
            plot_yclip=12,
            vlines=[0.0],
        )
    )

    # 7) (x^2+4)/x^3
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q7. } f(x)=\dfrac{x^{2}+4}{x^{3}}",
            hint_lines_latex=hint_workflow([r"\text{Rewrite }f(x)=\dfrac{1}{x}+\dfrac{4}{x^{3}}."]),
            sol_lines_latex=[
                r"\text{Domain: }x\ne 0\Rightarrow \text{vertical asymptote }x=0,\;\;\text{horizontal asymptote }y=0.",
                r"f'(x)=-\dfrac{1}{x^{2}}-\dfrac{12}{x^{4}}=-\dfrac{x^{2}+12}{x^{4}}<0\Rightarrow \text{decreasing on each side of }0.",
            ],
        )
    )

    # 8) (x-4)/x^3
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q8. } f(x)=\dfrac{x-4}{x^{3}}",
            hint_lines_latex=hint_workflow([r"\text{Domain }x\ne 0.\;\;\text{Rewrite }f(x)=\dfrac{1}{x^{2}}-\dfrac{4}{x^{3}}."]),
            sol_lines_latex=[
                r"\text{Vertical asymptote: }x=0,\;\;\text{horizontal asymptote: }y=0.",
                r"f'(x)=-\dfrac{2}{x^{3}}+\dfrac{12}{x^{4}}=\dfrac{-2x+12}{x^{4}}=\dfrac{2(6-x)}{x^{4}}.",
            ],
        )
    )

    # 9) 2x/(x^2-1)
    def f9(x: np.ndarray) -> np.ndarray:
        return (2 * x) / (x**2 - 1)

    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q9. } f(x)=\dfrac{2x}{x^{2}-1}",
            hint_lines_latex=hint_workflow([r"\text{Find vertical asymptotes from }x^{2}-1=0\text{ and horizontal asymptote from degrees.}"]),
            sol_lines_latex=[
                r"x=\pm 1\text{ are vertical asymptotes, }y=0\text{ is horizontal.}",
                r"f'(x)=-\dfrac{2(x^{2}+1)}{(x^{2}-1)^{2}}<0\Rightarrow \text{decreasing on each domain interval.}",
            ],
            plot_fn=f9,
            plot_window=(-4.0, 4.0),
            plot_title_latex=r"$f(x)=\dfrac{2x}{x^{2}-1}$",
            plot_yclip=8,
            vlines=[-1.0, 1.0],
            hlines=[0.0],
        )
    )

    # 10) 3x^2/(x^2+1)
    def f10(x: np.ndarray) -> np.ndarray:
        return (3 * x**2) / (x**2 + 1)

    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q10. } f(x)=\dfrac{3x^{2}}{x^{2}+1}",
            hint_lines_latex=hint_workflow([r"\text{No vertical asymptotes since }x^{2}+1\ne 0\text{ for real }x.}"]),
            sol_lines_latex=[
                r"\text{Domain: }(-\infty,\infty)\text{ and no vertical asymptotes.}",
                r"\lim_{x\to\pm\infty}\dfrac{3x^{2}}{x^{2}+1}=3\Rightarrow \text{horizontal asymptote }y=3.",
                r"f'(x)=\dfrac{6x(x^{2}+1)-3x^{2}(2x)}{(x^{2}+1)^{2}}=\dfrac{6x}{(x^{2}+1)^{2}}.",
            ],
            plot_fn=f10,
            plot_window=(-6.0, 6.0),
            plot_title_latex=r"$f(x)=\dfrac{3x^{2}}{x^{2}+1}$",
            plot_yclip=4,
            hlines=[3.0],
        )
    )

    # 11) x + sin x
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q11. } f(x)=x+\sin x",
            hint_lines_latex=hint_workflow([r"\text{Use }-1\le \cos x\le 1\text{ for }f'(x)=1+\cos x.}"]),
            sol_lines_latex=[
                r"f'(x)=1+\cos x\ge 0\Rightarrow \text{increasing on }(-\infty,\infty).",
                r"f''(x)=-\sin x\Rightarrow \text{concavity depends on the sign of }\sin x.",
            ],
        )
    )

    # 12) sin x - cos x
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q12. } f(x)=\sin x-\cos x",
            hint_lines_latex=hint_workflow([r"\text{Compute }f'(x)=\cos x+\sin x\text{ and solve }f'(x)=0.}"]),
            sol_lines_latex=[
                r"f'(x)=\cos x+\sin x=\sqrt{2}\sin\left(x+\dfrac{\pi}{4}\right)",
                r"f'(x)=0\Rightarrow x+\dfrac{\pi}{4}=k\pi\Rightarrow x=k\pi-\dfrac{\pi}{4}",
                r"f''(x)=-\sin x+\cos x=\sqrt{2}\cos\left(x+\dfrac{\pi}{4}\right).",
            ],
        )
    )

    # 13) x ln x
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q13. } f(x)=x\ln x",
            hint_lines_latex=hint_workflow([r"\text{Domain: }x>0.\;\;\text{Use product rule.}"]),
            sol_lines_latex=[
                r"f'(x)=\ln x+1,\;\; f'(x)=0\Rightarrow \ln x=-1\Rightarrow x=e^{-1}",
                r"f''(x)=\dfrac{1}{x}>0\text{ for }x>0\Rightarrow \text{concave up on }(0,\infty).",
            ],
        )
    )

    # 14) x ln(x^2)
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q14. } f(x)=x\ln(x^{2})",
            hint_lines_latex=hint_workflow([r"\text{Domain: }x\ne 0\text{ because }\ln(x^{2})=\ln(|x|^{2}).}"]),
            sol_lines_latex=[
                r"\ln(x^{2})=2\ln|x|\Rightarrow f(x)=2x\ln|x|,\;\;x\ne 0",
                r"f'(x)=2\ln|x|+2,\;\; f'(x)=0\Rightarrow \ln|x|=-1\Rightarrow |x|=e^{-1}",
            ],
        )
    )

    # 15) sqrt(x^2+1)
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q15. } f(x)=\sqrt{x^{2}+1}",
            hint_lines_latex=hint_workflow([r"\text{Differentiate }(x^{2}+1)^{1/2}\text{ using chain rule.}"]),
            sol_lines_latex=[
                r"f'(x)=\dfrac{x}{\sqrt{x^{2}+1}},\;\; f'(x)=0\Rightarrow x=0",
                r"f''(x)=\dfrac{1}{(x^{2}+1)^{3/2}}>0\Rightarrow \text{concave up everywhere.}",
            ],
        )
    )

    # 16) sqrt(2x-1)
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q16. } f(x)=\sqrt{2x-1}",
            hint_lines_latex=hint_workflow([r"\text{Domain: }x\ge \dfrac12.\;\;f'(x)=\dfrac{1}{\sqrt{2x-1}}."]),
            sol_lines_latex=[
                r"f'(x)=\dfrac{1}{\sqrt{2x-1}}>0\Rightarrow \text{increasing on }\left(\dfrac12,\infty\right)",
                r"f''(x)=-\dfrac{1}{(2x-1)^{3/2}}<0\Rightarrow \text{concave down on }\left(\dfrac12,\infty\right)",
            ],
        )
    )

    # 17) cube root of x^3 - 3x^2 + 2x
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q17. } f(x)=\sqrt[3]{x^{3}-3x^{2}+2x}",
            hint_lines_latex=hint_workflow([r"\text{Write }f(x)=(x^{3}-3x^{2}+2x)^{1/3}\text{ and use chain rule.}"]),
            sol_lines_latex=[
                r"f'(x)=\dfrac{1}{3}(x^{3}-3x^{2}+2x)^{-2/3}\cdot (3x^{2}-6x+2)",
                r"\text{Critical numbers: }3x^{2}-6x+2=0\text{ or }x^{3}-3x^{2}+2x=0.",
            ],
        )
    )

    # 18) sqrt(x^3 - 3x^2 + 2x)
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q18. } f(x)=\sqrt{x^{3}-3x^{2}+2x}",
            hint_lines_latex=hint_workflow([r"\text{First find domain from }x^{3}-3x^{2}+2x\ge 0.}"]),
            sol_lines_latex=[
                r"x^{3}-3x^{2}+2x=x(x-1)(x-2)",
                r"\text{Domain: }x(x-1)(x-2)\ge 0\Rightarrow x\in[0,1]\cup[2,\infty).",
                r"f'(x)=\dfrac{3x^{2}-6x+2}{2\sqrt{x^{3}-3x^{2}+2x}}\quad \text{(on the domain where denominator }\ne 0\text{).}",
            ],
        )
    )

    # 19) x^(5/3) - 5 x^(2/3)
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q19. } f(x)=x^{5/3}-5x^{2/3}",
            hint_lines_latex=hint_workflow([r"\text{Include where }f'(x)\text{ is undefined (at }x=0\text{).}"]),
            sol_lines_latex=[
                r"f'(x)=\dfrac{5}{3}x^{2/3}-\dfrac{10}{3}x^{-1/3}",
                r"f'(x)=0\Rightarrow x=2,\;\; f'(x)\text{ undefined at }x=0.",
            ],
        )
    )

    # 20) x^3 - 3/400 x
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q20. } f(x)=x^{3}-\dfrac{3}{400}x",
            hint_lines_latex=hint_workflow([r"\text{Factor }f'(x)\text{ and find critical numbers.}"]),
            sol_lines_latex=[
                r"f'(x)=3x^{2}-\dfrac{3}{400}=3\left(x^{2}-\dfrac{1}{400}\right)\Rightarrow x=\pm \dfrac{1}{20}",
                r"f''(x)=6x\Rightarrow \text{inflection at }x=0.",
            ],
        )
    )

    # 21) e^{-2/x}
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q21. } f(x)=e^{-2/x}",
            hint_lines_latex=hint_workflow([r"\text{Domain: }x\ne 0.\;\;\text{Use chain rule for }e^{u(x)}."]),
            sol_lines_latex=[
                r"u(x)=-\dfrac{2}{x}\Rightarrow u'(x)=\dfrac{2}{x^{2}}",
                r"f'(x)=e^{-2/x}\cdot\dfrac{2}{x^{2}}=\dfrac{2e^{-2/x}}{x^{2}}>0\Rightarrow \text{increasing on each side of }0.",
                r"\lim_{x\to\pm\infty}e^{-2/x}=e^{0}=1\Rightarrow \text{horizontal asymptote }y=1.",
            ],
        )
    )

    # 22) e^{1/x^2}
    items.append(
        PracticeItem(
            q_latex=r"\textbf{Q22. } f(x)=e^{1/x^{2}}",
            hint_lines_latex=hint_workflow([r"\text{Domain: }x\ne 0.\;\;\text{Use chain rule with }u(x)=x^{-2}."]),
            sol_lines_latex=[
                r"u(x)=\dfrac{1}{x^{2}}\Rightarrow u'(x)=-\dfrac{2}{x^{3}}",
                r"f'(x)=e^{1/x^{2}}\left(-\dfrac{2}{x^{3}}\right)=-\dfrac{2e^{1/x^{2}}}{x^{3}}",
                r"\text{So }f'(x)>0\text{ for }x<0\text{ and }f'(x)<0\text{ for }x>0.",
                r"\lim_{x\to\pm\infty}e^{1/x^{2}}=1\Rightarrow \text{horizontal asymptote }y=1.",
            ],
        )
    )

    # Ensure at least 20; we have 22.
    return items


# -----------------------------
# Learn tab: interactive “workflow board”
# -----------------------------
def _workflow_board() -> None:
    _md("### Curve sketching workflow (step-by-step)")
    _md(
        "- Use this every time you are asked to **“discuss the graph completely”**.\n"
        "- You will build the sketch using a fixed order of steps.\n"
        "- Press **Next step** to reveal the solution progressively."
    )

    # Pick from the exact Chapter 3 (Exercises 3.6) list
    choices: Dict[str, Dict[str, object]] = {
        r"$f(x)=x^{4}-3x^{2}+2$": {
            "f": lambda x: x**4 - 3 * x**2 + 2,
            "window": (-3.2, 3.2),
            "yclip": 10,
            "steps": [
                [r"f(x)=x^{4}-3x^{2}+2", r"\text{Domain: }(-\infty,\infty)"],
                [r"\text{Intercepts: }f(0)=2\Rightarrow (0,2)", r"\text{Solve }x^{4}-3x^{2}+2=0\Rightarrow (x^{2}-1)(x^{2}-2)=0"],
                [r"\Rightarrow x=\pm 1,\;\;x=\pm \sqrt{2}\;\;\Rightarrow\text{ x-intercepts at }(\pm 1,0),(\pm\sqrt{2},0)"],
                [r"f'(x)=4x^{3}-6x=2x(2x^{2}-3)", r"f'(x)=0\Rightarrow x=0,\;\;x=\pm\sqrt{\dfrac{3}{2}}"],
                [r"f''(x)=12x^{2}-6=6(2x^{2}-1)", r"f''(x)=0\Rightarrow x=\pm \dfrac{1}{\sqrt{2}}\;\;\text{(possible inflection)}"],
                [r"\text{Now create sign charts for }f'(x)\text{ and }f''(x)\text{ to decide increase/decrease and concavity.}"],
                [r"\text{Finish with a representative sketch using: intercepts, critical points, inflection points, and end behavior.}"],
            ],
            "vlines": [0.0, math.sqrt(3 / 2), -math.sqrt(3 / 2), 1 / math.sqrt(2), -1 / math.sqrt(2)],
            "hlines": [0.0],
        },
        r"$f(x)=\dfrac{2x}{x^{2}-1}$": {
            "f": lambda x: (2 * x) / (x**2 - 1),
            "window": (-4.0, 4.0),
            "yclip": 8,
            "steps": [
                [r"f(x)=\dfrac{2x}{x^{2}-1}", r"\text{Domain: }x\ne -1,\;x\ne 1"],
                [r"\text{Vertical asymptotes: }x=-1,\;x=1", r"\text{Horizontal asymptote: }y=0"],
                [r"f'(x)=-\dfrac{2(x^{2}+1)}{(x^{2}-1)^{2}}<0\Rightarrow \text{decreasing on each domain interval.}"],
                [r"\text{Use }f''(x)\text{ (optional) to decide concavity on }(-\infty,-1),(-1,1),(1,\infty)."],
                [r"\text{Sketch: show asymptotes and monotonic behavior on each interval.}"],
            ],
            "vlines": [-1.0, 1.0],
            "hlines": [0.0],
        },
        r"$f(x)=\sqrt{2x-1}$": {
            "f": lambda x: np.where(2 * x - 1 >= 0, np.sqrt(2 * x - 1), np.nan),
            "window": (0.0, 7.0),
            "yclip": None,
            "steps": [
                [r"f(x)=\sqrt{2x-1}", r"\text{Domain: }x\ge \dfrac{1}{2}"],
                [r"f'(x)=\dfrac{1}{\sqrt{2x-1}}>0\Rightarrow \text{increasing on }\left(\dfrac12,\infty\right)"],
                [r"f''(x)=-\dfrac{1}{(2x-1)^{3/2}}<0\Rightarrow \text{concave down on }\left(\dfrac12,\infty\right)"],
                [r"\text{Sketch: start at }\left(\dfrac12,0\right)\text{ and curve upward while bending down.}"],
            ],
            "vlines": [0.5],
            "hlines": [0.0],
        },
    }

    sel = st.selectbox("Choose a function", list(choices.keys()), key="cs56_workflow_choice")
    cfg = choices[sel]

    if "cs56_step" not in st.session_state:
        st.session_state.cs56_step = 0

    cA, cB = st.columns([1, 1])
    with cA:
        if _safe_button("Next step", "cs56_next_step"):
            st.session_state.cs56_step = min(st.session_state.cs56_step + 1, len(cfg["steps"]))  # type: ignore[index]
    with cB:
        if _safe_button("Reset steps", "cs56_reset_step"):
            st.session_state.cs56_step = 0

    # Show current steps on a board
    lines: List[str] = []
    for k in range(st.session_state.cs56_step):
        for line in cfg["steps"][k]:  # type: ignore[index]
            lines.append(line)

    if st.session_state.cs56_step == 0:
        _katex_text_block(
            [r"\text{Press }\textbf{Next step}\text{ to reveal the workflow solution line-by-line.}"],
            box_title="Solution board",
        )
    else:
        _katex_text_block(lines, box_title="Solution board")

    # Small plot
    _small_plot(
        cfg["f"],  # type: ignore[arg-type]
        cfg["window"][0],  # type: ignore[index]
        cfg["window"][1],  # type: ignore[index]
        f"Graph: {sel}",
        y_clip=cfg.get("yclip", None),  # type: ignore[arg-type]
        vlines=cfg.get("vlines", None),  # type: ignore[arg-type]
        hlines=cfg.get("hlines", None),  # type: ignore[arg-type]
    )


# -----------------------------
# Learn tab: objectives + explanations + worked examples
# -----------------------------
def _render_learn() -> None:
    _md("## Learning objectives (Subtopic 5.6)")
    _md(
        "- **5.6.1** Recall finding the **horizontal** and **vertical** asymptotes of a rational function.\n"
        "- **5.6.2** Use a clear **summary of steps** for curve sketching: domain, first and second derivatives, critical values, inflection values, summary tables, a few values, and the final sketch.\n"
        "- **5.6.3** Analyze and sketch graphs for different function types: polynomials, rational functions, fractional powers, radicals, and functions with trigonometric / exponential / logarithmic components."
    )

    st.divider()

    # 5.6.1
    _md("### 5.6.1 Vertical and horizontal asymptotes (rational functions)")
    _md(
        "- A **vertical asymptote** happens where the function is not defined and the graph shoots up/down.\n"
        "- A **horizontal asymptote** describes the end behavior as $x\\to\\infty$ or $x\\to-\\infty$."
    )
    _md("**How to find vertical asymptotes**")
    _md("- For $f(x)=\\dfrac{p(x)}{q(x)}$, solve $q(x)=0$ (and keep only values that do not cancel).")

    _md("**How to find a horizontal asymptote**")
    _md(
        "- Compare degrees of $p(x)$ and $q(x)$:\n"
        "  - If $\\deg(p)<\\deg(q)$ then $\\displaystyle \\lim_{x\\to\\pm\\infty}f(x)=0$ so $y=0$.\n"
        "  - If $\\deg(p)=\\deg(q)$ then the limit is the ratio of leading coefficients.\n"
        "  - If $\\deg(p)>\\deg(q)$ then there is **no horizontal asymptote**."
    )

    # Short aligned micro-example (from Exercise list)
    with st.expander(_inline_math("Worked example (rational asymptotes): $f(x)=\\dfrac{x+4}{x}$"), expanded=True):
        _katex_text_block(
            [
                r"f(x)=\dfrac{x+4}{x}=1+\dfrac{4}{x}",
                r"\text{Vertical asymptote: }x=0",
                r"\lim_{x\to\pm\infty}\left(1+\dfrac{4}{x}\right)=1\Rightarrow \text{Horizontal asymptote: }y=1",
            ],
            box_title="Solution board",
        )
        _small_plot(
            lambda x: (x + 4) / x,
            -6.0,
            6.0,
            r"$f(x)=\dfrac{x+4}{x}$ (small view)",
            y_clip=10,
            vlines=[0.0],
            hlines=[1.0],
        )

    st.divider()

    # 5.6.2 workflow
    _md("### 5.6.2 Summary steps for curve sketching")
    _md(
        "When you are asked to **“discuss the graph completely”**, use this exact order:\n\n"
        "1. **Domain** (where the function is defined).\n"
        "2. **Intercepts**: $x$-intercepts (solve $f(x)=0$) and $y$-intercept (evaluate $f(0)$ if it exists).\n"
        "3. **First derivative** $f'(x)$.\n"
        "4. **Critical values**: solve $f'(x)=0$ and include where $f'(x)$ is undefined (but $f$ is defined).\n"
        "5. **Sign chart for $f'(x)$** to decide increasing/decreasing.\n"
        "6. **Second derivative** $f''(x)$.\n"
        "7. **Inflection values**: solve $f''(x)=0$ and include where $f''(x)$ is undefined (but $f$ is defined).\n"
        "8. **Sign chart for $f''(x)$** to decide concavity.\n"
        "9. **Asymptotes** (for rational functions: vertical and horizontal).\n"
        "10. **Table of values** for a few points only when needed.\n"
        "11. **Final sketch** that matches all results."
    )

    _workflow_board()

    st.divider()

    # 5.6.3 worked examples (from Section 3.6 list)
    _md("### 5.6.3 Worked examples (from Section 3.6 function list)")
    exs = _examples()

    for ex in exs:
        with st.expander(ex.title, expanded=False):
            st.markdown(
                """
<style>
.aqb-question{
  padding:14px 14px 10px 14px;
  border-radius:12px;
  border:1px solid rgba(30,80,170,0.18);
  background: rgba(30,80,170,0.06);
}
</style>
""",
                unsafe_allow_html=True,
            )
            st.markdown('<div class="aqb-question">', unsafe_allow_html=True)
            for line in ex.question_lines_md:
                _md(line)
            st.markdown("</div>", unsafe_allow_html=True)

            _katex_text_block(ex.solution_lines_latex, box_title="Step-by-step solution")

            _small_plot(
                ex.plot_fn,
                ex.plot_window[0],
                ex.plot_window[1],
                ex.plot_title_latex,
                y_clip=ex.plot_yclip,
                vlines=ex.vlines,
                hlines=ex.hlines,
            )

    st.divider()

    # A clean, readable combined sign/concavity table (no overlap)
    _md("### Combined summary table (example format)")
    _md(
        "Sometimes you will summarize **increase/decrease** and **concavity** together.\n"
        "Below is a **readable** table layout you can copy in exams."
    )
    _sign_table(
        intervals_latex=[r"(-\infty,a)", r"(a,b)", r"(b,\infty)"],
        sign_fprime_latex=[r"+", r"-", r"+"],
        behavior_latex=[r"\text{increasing}", r"\text{decreasing}", r"\text{increasing}"],
        sign_f2_latex=[r"-", r"+", r"+"],
        concavity_latex=[r"\text{concave down}", r"\text{concave up}", r"\text{concave up}"],
    )


# -----------------------------
# Practice tab
# -----------------------------
def _render_practice() -> None:
    _md("## Practice (at least 20 questions)")
    _md(
        "For each question:\n"
        "- Press **Hint** if you want a small push.\n"
        "- Press **Show solution** to reveal a guided solution outline.\n"
        "- Keep your work organized using the workflow from the Learn tab."
    )

    items = _practice_items()

    # Session state for per-question toggles
    if "cs56_hint" not in st.session_state:
        st.session_state.cs56_hint = {}
    if "cs56_sol" not in st.session_state:
        st.session_state.cs56_sol = {}

    for i, it in enumerate(items, start=1):
        st.markdown("---")
        _latex(it.q_latex)

        c1, c2 = st.columns([1, 1])
        with c1:
            if _safe_button("Hint", f"cs56_hint_btn_{i}"):
                st.session_state.cs56_hint[str(i)] = True
        with c2:
            if _safe_button("Show solution", f"cs56_sol_btn_{i}"):
                st.session_state.cs56_sol[str(i)] = True

        if st.session_state.cs56_hint.get(str(i), False):
            _katex_text_block(it.hint_lines_latex, box_title="Hint")

        if st.session_state.cs56_sol.get(str(i), False):
            _katex_text_block(it.sol_lines_latex, box_title="Solution outline")

            if it.plot_fn is not None and it.plot_window is not None and it.plot_title_latex is not None:
                _small_plot(
                    it.plot_fn,
                    it.plot_window[0],
                    it.plot_window[1],
                    it.plot_title_latex,
                    y_clip=it.plot_yclip,
                    vlines=it.vlines,
                    hlines=it.hlines,
                )


# -----------------------------
# Entry point required by the app
# -----------------------------
def render() -> None:
    # Keep the top clean (no duplicate headers, no placeholders).
    st.subheader("Subtopic 5.6: Overview of Curve Sketching")

    tab_learn, tab_practice = st.tabs(["Learn", "Practice"])

    with tab_learn:
        _render_learn()

    with tab_practice:
        _render_practice()
