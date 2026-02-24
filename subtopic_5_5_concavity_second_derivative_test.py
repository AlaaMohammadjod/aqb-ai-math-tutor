# subtopic_5_5_concavity_second_derivative_test.py
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple


# =========================================================
# NON-NEGOTIABLE COMPLIANCE
# - NO sliders
# - ALL math must be LaTeX/KaTeX (use st.latex, or $...$ only if needed)
# - Must expose render()
# - Practice content stays as-is (your feedback: practice is perfect)
# - Board simulator must use simulations.py (no iframe hack)
# =========================================================


# -----------------------------
# Small helpers (KaTeX-safe)
# -----------------------------
def _latex(tex: str) -> None:
    st.latex(tex)


def _title(text: str) -> None:
    st.markdown(f"### {text}")


def _p(text: str) -> None:
    # prose ONLY (no math inside this string)
    st.markdown(text)


def _box(title: str, bullets: List[str]) -> None:
    # bullets can contain LaTeX ONLY via st.latex per line (to guarantee “all math is LaTeX”)
    with st.container(border=True):
        st.markdown(f"**{title}**")
        for b in bullets:
            if b.strip().startswith(r"\(") or b.strip().startswith(r"\[") or b.strip().startswith(r"$") or "\\" in b:
                # If user accidentally passes math here, force it to LaTeX line.
                _latex(b.replace(r"\(", "").replace(r"\)", "").replace("$", ""))
            else:
                st.markdown(f"- {b}")


def _latex_bullets(lines: List[str]) -> None:
    for ln in lines:
        _latex(ln)


def _small_plot(
    f: Callable[[np.ndarray], np.ndarray],
    x_min: float,
    x_max: float,
    title: str,
) -> None:
    xs = np.linspace(x_min, x_max, 800)
    ys = f(xs)

    plt.figure(figsize=(6.0, 3.2), dpi=160)
    ax = plt.gca()
    ax.plot(xs, ys)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    st.pyplot(plt.gcf(), clear_figure=True)


def _render_blackboard_from_simulations() -> None:
    """Use the board simulator from simulations.py (no iframe)."""
    try:
        import simulations  # type: ignore
    except Exception as e:
        st.error("Could not import `simulations.py`.")
        st.exception(e)
        return

    candidates = [
        "render_blackboard_simulator",
        "render_board_simulator",
        "render_blackboard",
        "board_simulator",
    ]
    for name in candidates:
        fn = getattr(simulations, name, None)
        if callable(fn):
            try:
                fn()
                return
            except Exception as e:
                st.error("A blackboard simulator function was found, but it raised an error.")
                st.exception(e)
                return

    st.error("No supported blackboard simulator function name was found inside `simulations.py`.")


# -----------------------------
# Worked examples (Exam format)
# -----------------------------
@dataclass
class WorkedExample:
    title: str
    question_tex: str
    tasks_tex: List[str]
    steps_tex: List[str]
    plot_func: Optional[Callable[[np.ndarray], np.ndarray]] = None
    plot_domain: Tuple[float, float] = (-4, 4)
    plot_title: Optional[str] = None


def _worked_examples_bank() -> List[WorkedExample]:
    # Keep tightly within objectives 5.5.1–5.5.5 and aligned to Chapter 3 style:
    # - exam question
    # - clear tasks
    # - full teacher-like solution

    ex1 = WorkedExample(
        title="Example 1: Concavity and inflection point",
        question_tex=r"f(x)=2x^3+9x^2-24x-10",
        tasks_tex=[
            r"\text{(i) Find the intervals where }f\text{ is concave up and concave down.}",
            r"\text{(ii) Identify the inflection point(s).}",
        ],
        steps_tex=[
            r"\textbf{Step 1. Compute the second derivative.}",
            r"f'(x)=6x^2+18x-24",
            r"f''(x)=12x+18=6(2x+3)",
            r"\textbf{Step 2. Find candidates for inflection.}",
            r"f''(x)=0\;\Rightarrow\;12x+18=0\;\Rightarrow\;x=-\frac{3}{2}",
            r"\textbf{Step 3. Sign test for }f''(x)\textbf{ on each interval.}",
            r"\text{Pick }x=-2:\;f''(-2)=12(-2)+18=-6<0\;\Rightarrow\;\text{concave down on }\left(-\infty,-\frac{3}{2}\right)",
            r"\text{Pick }x=0:\;f''(0)=18>0\;\Rightarrow\;\text{concave up on }\left(-\frac{3}{2},\infty\right)",
            r"\textbf{Step 4. Inflection point (concavity change).}",
            r"\text{Concavity changes at }x=-\frac{3}{2}\;\Rightarrow\;\text{inflection at }x=-\frac{3}{2}",
            r"f\!\left(-\frac{3}{2}\right)=\frac{47}{2}",
            r"\textbf{Answer: }\;\text{concave down on }\left(-\infty,-\frac{3}{2}\right),\;\text{concave up on }\left(-\frac{3}{2},\infty\right),\;\text{inflection point }\left(-\frac{3}{2},\frac{47}{2}\right)",
        ],
        plot_func=lambda x: 2 * x**3 + 9 * x**2 - 24 * x - 10,
        plot_domain=(-4, 4),
        plot_title="Concavity change (supporting graph)",
    )

    ex2 = WorkedExample(
        title="Example 2: Second Derivative Test (local extrema)",
        question_tex=r"f(x)=x^4-8x^2+10",
        tasks_tex=[
            r"\text{Find the critical numbers.}",
            r"\text{Use the Second Derivative Test to classify each critical number.}",
        ],
        steps_tex=[
            r"\textbf{Step 1. Find critical numbers from }f'(x)=0.",
            r"f'(x)=4x^3-16x=4x(x^2-4)=4x(x-2)(x+2)",
            r"f'(x)=0\;\Rightarrow\;x=-2,\;0,\;2",
            r"\textbf{Step 2. Use }f''(x)\textbf{ at each critical number.}",
            r"f''(x)=12x^2-16",
            r"f''(-2)=12(4)-16=32>0\;\Rightarrow\;\text{local minimum at }x=-2",
            r"f''(0)=-16<0\;\Rightarrow\;\text{local maximum at }x=0",
            r"f''(2)=32>0\;\Rightarrow\;\text{local minimum at }x=2",
        ],
        plot_func=lambda x: x**4 - 8 * x**2 + 10,
        plot_domain=(-4, 4),
        plot_title="Extrema (supporting graph)",
    )

    ex3 = WorkedExample(
        title="Example 3: When the Second Derivative Test is inconclusive",
        question_tex=r"f(x)=x^4",
        tasks_tex=[
            r"\text{Find the critical number(s).}",
            r"\text{Apply the Second Derivative Test and state what happens.}",
            r"\text{Decide the correct classification.}",
        ],
        steps_tex=[
            r"\textbf{Step 1. Critical numbers from }f'(x)=0.",
            r"f'(x)=4x^3",
            r"4x^3=0\;\Rightarrow\;x=0",
            r"\textbf{Step 2. Second Derivative Test.}",
            r"f''(x)=12x^2",
            r"f''(0)=0\;\Rightarrow\;\text{inconclusive}",
            r"\textbf{Step 3. Correct classification (within objective 5.5.3).}",
            r"x^4\ge 0\;\text{for all }x\;\Rightarrow\;x=0\text{ is a local minimum}",
        ],
    )

    ex4 = WorkedExample(
        title="Example 4: Concavity where }f''(x)\text{ is undefined (corner case)",
        question_tex=r"f(x)=|x|",
        tasks_tex=[
            r"\text{Explain why concavity is not defined at }x=0.",
            r"\text{State what happens on }(-\infty,0)\text{ and }(0,\infty).",
        ],
        steps_tex=[
            r"|x|=\begin{cases}-x,&x<0\\x,&x\ge 0\end{cases}",
            r"f'(x)=\begin{cases}-1,&x<0\\1,&x>0\end{cases}\;\text{and }f'(0)\text{ does not exist (corner)}",
            r"\text{Because }f'(0)\text{ does not exist, }f''(0)\text{ is undefined}",
            r"\textbf{Conclusion: }\text{concavity is not defined at }x=0\text{ (corner)}",
        ],
        plot_func=lambda x: np.abs(x),
        plot_domain=(-4, 4),
        plot_title="Corner example (supporting graph)",
    )

    # Objective 5.5.5 (economic/production) — keep strictly within: interpret concavity via second derivative.
    ex5 = WorkedExample(
        title="Example 5: Economic interpretation (cost / revenue concavity)",
        question_tex=r"\text{Suppose }C(x)\text{ is a cost function and }C''(x)>0\text{ on an interval.}",
        tasks_tex=[
            r"\text{State what concavity means for }C(x)\text{ on that interval.}",
            r"\text{Interpret what happens to }C'(x)\text{ (marginal cost).}",
        ],
        steps_tex=[
            r"C''(x)>0\;\Rightarrow\;C(x)\text{ is concave up on that interval}",
            r"\text{Concave up means slopes increase } \Rightarrow\; C'(x)\text{ is increasing}",
            r"\textbf{Interpretation: }\text{marginal cost increases as production increases on that interval}",
        ],
    )

    return [ex1, ex2, ex3, ex4, ex5]


def _render_worked_examples() -> None:
    bank = _worked_examples_bank()
    title = st.radio("Choose a worked example", [b.title for b in bank], horizontal=False)
    ex = next(b for b in bank if b.title == title)

    _title("Question")
    _latex(ex.question_tex)

    _title("Task")
    _latex_bullets(ex.tasks_tex)

    _title("Solution (step-by-step)")
    _latex_bullets(ex.steps_tex)

    if ex.plot_func is not None and ex.plot_title is not None:
        _title("Supporting graph")
        _small_plot(ex.plot_func, ex.plot_domain[0], ex.plot_domain[1], ex.plot_title)


# -----------------------------
# Learn tab (FULL, organized, objective-by-objective)
# -----------------------------
def _render_objectives() -> None:
    _title("Learning objectives (5.5)")
    _p("This subtopic focuses only on the following outcomes.")
    _latex_bullets(
        [
            r"\textbf{5.5.1}\;\text{Find intervals where a function is concave up/down and identify inflection points.}",
            r"\textbf{5.5.2}\;\text{Build combined tables (tables of variation) summarizing behavior and concavity.}",
            r"\textbf{5.5.3}\;\text{Use the Second Derivative Test to classify local extrema and know when it is inconclusive.}",
            r"\textbf{5.5.4}\;\text{Estimate increase/decrease, extrema, concavity, and inflection points from a graph.}",
            r"\textbf{5.5.5}\;\text{Apply concavity ideas to economic/production contexts (sales, efficiency, cost).}",
        ]
    )


def _render_551() -> None:
    _title("5.5.1 Concavity and inflection points")
    _box(
        "Meaning (in student-friendly words)",
        [
            "Concavity tells you how the slope is changing as you move left to right.",
            "You will decide concavity using the sign of the second derivative.",
        ],
    )

    _latex(r"f''(x)>0\;\Rightarrow\;f\text{ is concave up}")
    _latex(r"f''(x)<0\;\Rightarrow\;f\text{ is concave down}")

    _box(
        "How to find inflection points (exact method)",
        [
            "Find candidates where the second derivative becomes zero or undefined.",
            "Do a sign test for the second derivative on the intervals around each candidate.",
            "You have an inflection point only if the concavity changes.",
        ],
    )
    _latex_bullets(
        [
            r"\text{Candidates: }f''(x)=0\;\text{ or }f''(x)\text{ is undefined}",
            r"\text{Confirm: sign change of }f''(x)\text{ across the candidate}",
        ]
    )

    _title("Mini example (fully solved)")
    _latex(r"f(x)=x^3-3x")
    _latex(r"f'(x)=3x^2-3")
    _latex(r"f''(x)=6x")
    _latex(r"f''(x)=0\;\Rightarrow\;x=0")
    _latex(r"f''(x)<0\text{ on }(-\infty,0)\;\Rightarrow\;\text{concave down}")
    _latex(r"f''(x)>0\text{ on }(0,\infty)\;\Rightarrow\;\text{concave up}")
    _latex(r"\text{Inflection point: }(0,f(0))=(0,0)")

    _small_plot(lambda x: x**3 - 3 * x, -4, 4, "Concavity change (supporting graph)")


def _render_552() -> None:
    _title("5.5.2 Combined table (table of variation)")
    _box(
        "What your combined table must include",
        [
            "Critical numbers from the first derivative.",
            "Inflection candidates from the second derivative.",
            "Intervals on one number line using all split points together.",
            "Signs of the first derivative (increasing / decreasing).",
            "Signs of the second derivative (concave up / concave down).",
        ],
    )

    _title("Clean template (KaTeX — no overlap)")
    # Use st.latex array to avoid overlap and guarantee math rendering
    _latex(
        r"""
\begin{array}{|c|c|c|c|c|}
\hline
\text{Interval} & \text{sign of }f'(x) & \text{Behavior} & \text{sign of }f''(x) & \text{Concavity}\\
\hline
(-\infty,a) & +\;/\;- & \text{Inc.}\;/\;\text{Dec.} & +\;/\;- & \text{CU}\;/\;\text{CD}\\
\hline
(a,b) & +\;/\;- & \text{Inc.}\;/\;\text{Dec.} & +\;/\;- & \text{CU}\;/\;\text{CD}\\
\hline
(b,\infty) & +\;/\;- & \text{Inc.}\;/\;\text{Dec.} & +\;/\;- & \text{CU}\;/\;\text{CD}\\
\hline
\end{array}
"""
    )
    _latex(r"\text{Legend: }\;\text{CU}=\text{concave up},\;\text{CD}=\text{concave down},\;\text{Inc.}=\text{increasing},\;\text{Dec.}=\text{decreasing}")


def _render_553() -> None:
    _title("5.5.3 Second Derivative Test (local extrema)")
    _box(
        "Second Derivative Test (use only at a critical number)",
        [
            "First, find a critical number c where the first derivative is zero.",
            "Then evaluate the second derivative at that point.",
            "If the second derivative is positive, the point is a local minimum.",
            "If the second derivative is negative, the point is a local maximum.",
            "If the second derivative is zero or undefined, the test is inconclusive.",
        ],
    )

    _latex(r"\text{If }f'(c)=0\text{ and }f''(c)>0\;\Rightarrow\;\text{local minimum at }x=c")
    _latex(r"\text{If }f'(c)=0\text{ and }f''(c)<0\;\Rightarrow\;\text{local maximum at }x=c")
    _latex(r"\text{If }f'(c)=0\text{ and }f''(c)=0\;\Rightarrow\;\text{inconclusive}")

    _title("Mini example (inconclusive case)")
    _latex(r"f(x)=x^4")
    _latex(r"f'(x)=4x^3=0\;\Rightarrow\;x=0")
    _latex(r"f''(x)=12x^2\;\Rightarrow\;f''(0)=0\;\Rightarrow\;\text{inconclusive}")
    _latex(r"x^4\ge 0\text{ for all }x\;\Rightarrow\;\text{local minimum at }x=0")


def _render_554() -> None:
    _title("5.5.4 Estimating from a graph")
    _box(
        "What to look for on the curve",
        [
            "Increasing where the curve rises from left to right.",
            "Decreasing where the curve falls from left to right.",
            "Concave up where slopes are getting larger (more positive).",
            "Concave down where slopes are getting smaller (less positive).",
            "Inflection where the curve switches concavity.",
        ],
    )

    _latex(r"\text{Concave up: slopes increase}\;\Rightarrow\;f''(x)>0")
    _latex(r"\text{Concave down: slopes decrease}\;\Rightarrow\;f''(x)<0")

    _title("Short visual example (smaller graph)")
    g = lambda x: x**3 - 3 * x
    _small_plot(g, -4, 4, "Example curve for estimating concavity and turning behavior")


def _render_555() -> None:
    _title("5.5.5 Economic / production interpretation")
    _box(
        "How to interpret the sign of a second derivative",
        [
            "If a quantity is concave up, its rate of change is increasing.",
            "If a quantity is concave down, its rate of change is decreasing.",
        ],
    )

    _latex(r"C''(x)>0\;\Rightarrow\;C(x)\text{ concave up}\;\Rightarrow\;C'(x)\text{ increasing (marginal cost rises)}")
    _latex(r"R''(x)<0\;\Rightarrow\;R(x)\text{ concave down}\;\Rightarrow\;R'(x)\text{ decreasing (marginal revenue falls)}")


def _render_learn() -> None:
    _render_objectives()
    st.divider()
    _render_551()
    st.divider()
    _render_552()
    st.divider()
    _render_553()
    st.divider()
    _render_554()
    st.divider()
    _render_555()


# -----------------------------
# Practice (KEEP AS-IS)
# -----------------------------
@dataclass
class PracticeQ:
    q_latex: str
    answer_steps_latex: List[str]


def _practice_bank() -> List[PracticeQ]:
    # EXACT same practice content as before (your feedback: practice is perfect)
    qs: List[PracticeQ] = []

    def add(q: str, steps: List[str]):
        qs.append(PracticeQ(q_latex=q, answer_steps_latex=steps))

    add(
        r"\textbf{Q1.}\; f(x)=x^3-3x.\; \text{Find concavity intervals and inflection points.}",
        [
            r"f''(x)=6x.",
            r"6x=0\Rightarrow x=0.",
            r"f''(x)<0\text{ on }(-\infty,0)\Rightarrow \text{concave down}.",
            r"f''(x)>0\text{ on }(0,\infty)\Rightarrow \text{concave up}.",
            r"\text{Inflection at }x=0\Rightarrow (0,f(0))=(0,0).",
        ],
    )
    add(
        r"\textbf{Q2.}\; f(x)=2x^3+9x^2-24x-10.\; \text{Find concavity and inflection point.}",
        [
            r"f''(x)=12x+18.",
            r"12x+18=0\Rightarrow x=-\frac{3}{2}.",
            r"f''(x)<0\text{ on }(-\infty,-\tfrac{3}{2}),\; f''(x)>0\text{ on }(-\tfrac{3}{2},\infty).",
            r"\text{Inflection at }\left(-\frac{3}{2},\frac{47}{2}\right).",
        ],
    )
    add(
        r"\textbf{Q3.}\; f(x)=x^4-6x^2.\; \text{Find concavity and inflection points.}",
        [
            r"f''(x)=12x^2-12=12(x^2-1).",
            r"f''(x)=0\Rightarrow x=\pm 1.",
            r"f''(x)>0\text{ on }(-\infty,-1)\cup(1,\infty)\Rightarrow \text{concave up}.",
            r"f''(x)<0\text{ on }(-1,1)\Rightarrow \text{concave down}.",
            r"\text{Inflection at }(-1,f(-1))=(-1,-5)\text{ and }(1,f(1))=(1,-5).",
        ],
    )
    add(
        r"\textbf{Q4.}\; f(x)=\ln(x).\; \text{Find concavity on its domain.}",
        [
            r"f''(x)=-\frac{1}{x^2}.",
            r"f''(x)<0\text{ for }x>0\Rightarrow \text{concave down on }(0,\infty).",
        ],
    )
    add(
        r"\textbf{Q5.}\; f(x)=e^x.\; \text{Find concavity on }(-\infty,\infty).",
        [
            r"f''(x)=e^x>0\Rightarrow \text{concave up on }(-\infty,\infty).",
        ],
    )
    add(
        r"\textbf{Q6.}\; f(x)=\frac{1}{x}.\; \text{Find concavity on its domain.}",
        [
            r"f''(x)=\frac{2}{x^3}.",
            r"f''(x)<0\text{ on }(-\infty,0)\Rightarrow \text{concave down}.",
            r"f''(x)>0\text{ on }(0,\infty)\Rightarrow \text{concave up}.",
            r"\text{No inflection point because }x=0\text{ is not in the domain.}",
        ],
    )
    add(
        r"\textbf{Q7.}\; f(x)=x^{1/3}.\; \text{Discuss concavity where }f''(x)\text{ exists.}",
        [
            r"f'(x)=\frac{1}{3}x^{-2/3}.",
            r"f''(x)=-\frac{2}{9}x^{-5/3}.",
            r"f''(x)>0\text{ on }(-\infty,0)\Rightarrow \text{concave up}.",
            r"f''(x)<0\text{ on }(0,\infty)\Rightarrow \text{concave down}.",
            r"\text{Here }f''(0)\text{ is undefined; concavity changes across }0\Rightarrow \text{inflection at }(0,0).",
        ],
    )
    add(
        r"\textbf{Q8.}\; f(x)=\sqrt{x}.\; \text{Find concavity on its domain.}",
        [
            r"f''(x)=-\frac{1}{4}x^{-3/2}<0\text{ for }x>0\Rightarrow \text{concave down on }(0,\infty).",
        ],
    )
    add(
        r"\textbf{Q9.}\; f(x)=x^4-8x^2+10.\; \text{Classify local extrema using }f''(x).",
        [
            r"f'(x)=4x(x-2)(x+2)\Rightarrow x=-2,0,2.",
            r"f''(x)=12x^2-16.",
            r"f''(-2)=32>0\Rightarrow \text{local min at }x=-2.",
            r"f''(0)=-16<0\Rightarrow \text{local max at }x=0.",
            r"f''(2)=32>0\Rightarrow \text{local min at }x=2.",
        ],
    )
    add(
        r"\textbf{Q10.}\; f(x)=x^3.\; \text{Apply the Second Derivative Test at the critical point.}",
        [
            r"f'(x)=3x^2=0\Rightarrow x=0.",
            r"f''(x)=6x\Rightarrow f''(0)=0\Rightarrow \text{inconclusive}.",
            r"\text{Use sign of }f'(x):\; f'(x)>0\text{ for }x\neq 0\Rightarrow \text{no max/min at }0.",
        ],
    )
    add(
        r"\textbf{Q11.}\; f(x)=\sin(x)\text{ on }(0,2\pi).\; \text{Use }f''(x)\text{ at critical points.}",
        [
            r"f'(x)=\cos(x)=0\Rightarrow x=\frac{\pi}{2},\frac{3\pi}{2}.",
            r"f''(x)=-\sin(x).",
            r"f''(\tfrac{\pi}{2})=-1<0\Rightarrow \text{local max at }x=\tfrac{\pi}{2}.",
            r"f''(\tfrac{3\pi}{2})=1>0\Rightarrow \text{local min at }x=\tfrac{3\pi}{2}.",
        ],
    )
    add(
        r"\textbf{Q12.}\; f(x)=x^2.\; \text{Use }f''(x)\text{ to classify the extremum.}",
        [
            r"f'(x)=2x=0\Rightarrow x=0.",
            r"f''(x)=2>0\Rightarrow \text{local min at }x=0.",
        ],
    )
    add(
        r"\textbf{Q13.}\; f(x)=-x^2.\; \text{Use }f''(x)\text{ to classify the extremum.}",
        [
            r"f'(x)=-2x=0\Rightarrow x=0.",
            r"f''(x)=-2<0\Rightarrow \text{local max at }x=0.",
        ],
    )
    add(
        r"\textbf{Q14.}\; f(x)=x^4.\; \text{Apply the Second Derivative Test at }x=0.",
        [
            r"f'(x)=4x^3=0\Rightarrow x=0.",
            r"f''(x)=12x^2\Rightarrow f''(0)=0\Rightarrow \text{inconclusive}.",
            r"\text{But }x=0\text{ is a local min (since }x^4\ge 0\text{)}.",
        ],
    )
    add(
        r"\textbf{Q15.}\; f(x)=x^4-6x^2.\; \text{Build a combined table using }f'(x)\text{ and }f''(x).",
        [
            r"f'(x)=4x^3-12x=4x(x^2-3)\Rightarrow x=0,\pm\sqrt{3}.",
            r"f''(x)=12x^2-12=12(x^2-1)\Rightarrow x=\pm 1.",
            r"\text{Split intervals at }-\sqrt{3},-1,0,1,\sqrt{3}\text{ and test signs of }f',f''.",
        ],
    )
    add(
        r"\textbf{Q16.}\; f(x)=\ln(x).\; \text{State increasing/decreasing and concavity on }(0,\infty).",
        [
            r"f'(x)=\frac{1}{x}>0\Rightarrow \text{increasing on }(0,\infty).",
            r"f''(x)=-\frac{1}{x^2}<0\Rightarrow \text{concave down on }(0,\infty).",
        ],
    )
    add(
        r"\textbf{Q17.}\; f(x)=e^{-x}.\; \text{State concavity and monotonicity.}",
        [
            r"f'(x)=-e^{-x}<0\Rightarrow \text{decreasing on }(-\infty,\infty).",
            r"f''(x)=e^{-x}>0\Rightarrow \text{concave up on }(-\infty,\infty).",
        ],
    )
    add(
        r"\textbf{Q18.}\; f(x)=\frac{1}{x}.\; \text{Build a combined sign description on }(-\infty,0)\cup(0,\infty).",
        [
            r"f'(x)=-\frac{1}{x^2}<0\Rightarrow \text{decreasing on each interval.}",
            r"f''(x)=\frac{2}{x^3}\Rightarrow \text{concave down on }(-\infty,0),\;\text{concave up on }(0,\infty).",
        ],
    )
    add(
        r"\textbf{Q19.}\; \text{If }C''(x)>0\text{ for all }x,\text{ what does that mean about }C(x)\text{?}",
        [
            r"C''(x)>0\Rightarrow C(x)\text{ is concave up}.",
            r"\text{So }C'(x)\text{ is increasing: marginal cost rises as production increases}.",
        ],
    )
    add(
        r"\textbf{Q20.}\; \text{If }R''(x)<0\text{ for all }x,\text{ what does that mean about }R(x)\text{?}",
        [
            r"R''(x)<0\Rightarrow R(x)\text{ is concave down}.",
            r"\text{So }R'(x)\text{ is decreasing: marginal revenue falls as production increases}.",
        ],
    )

    return qs


def _render_practice() -> None:
    _title("Practice (exam style)")
    _box(
        "How to use this practice",
        [
            "For each question, write your answer clearly and include the calculus steps.",
            "Then open the answer to compare with your work.",
        ],
    )

    qs = _practice_bank()
    for i, q in enumerate(qs, start=1):
        with st.expander(f"Q{i}", expanded=False):
            _latex(q.q_latex)
            if st.button(f"Show answer for Q{i}", key=f"show_ans_{i}"):
                for s in q.answer_steps_latex:
                    _latex(s)


# -----------------------------
# Main render()
# -----------------------------
def render() -> None:
    st.header("Subtopic 5.5: Concavity and 2nd Derivative Test")

    tabs = st.tabs(["Learn", "Worked examples", "Board simulator", "Practice"])

    with tabs[0]:
        _render_learn()

    with tabs[1]:
        _render_worked_examples()

    with tabs[2]:
        _title("Board simulator")
        _p("Choose an example and watch the full solution appear on the same board.")
        _render_blackboard_from_simulations()

    with tabs[3]:
        _render_practice()
