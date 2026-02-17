# subtopic_5_1_linear_approximations_newton.py

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from simulations import BoardStep, render_simulation


# -----------------------------
# KaTeX-only helpers (humanized math everywhere)
# -----------------------------
def _katex(expr: str):
    st.latex(expr)


def _pyplot_small(fig, *, width_mode: str = "content"):
    """Smaller graphs; Streamlit width-safe."""
    try:
        st.pyplot(fig, clear_figure=True, width=width_mode)
    except TypeError:
        st.pyplot(fig, clear_figure=True, use_container_width=(width_mode == "stretch"))


def _hr():
    st.markdown("<hr style='margin: 0.6rem 0; opacity: .18;'>", unsafe_allow_html=True)


# -----------------------------
# Graph simulations (NO sliders)
# -----------------------------
@dataclass
class LinearApproxExample:
    name: str
    f: Callable[[np.ndarray], np.ndarray]
    fp: Callable[[float], float]
    a: float
    x1: float
    x_domain: Tuple[float, float]
    y_label: str
    f_latex: str
    a_latex: str
    x1_latex: str
    target_latex: str


def _linear_examples() -> List[LinearApproxExample]:
    # ✅ Trig example uses x1 in terms of π (no "1 rad")
    return [
        LinearApproxExample(
            name="Approximate  cos(3π/10)  using  f(x)=cos x  at  a=π/3",
            f=lambda x: np.cos(x),
            fp=lambda x: -math.sin(x),
            a=math.pi / 3,
            x1=3 * math.pi / 10,
            x_domain=(0.0, math.pi),
            y_label=r"$y$",
            f_latex=r"f(x)=\cos x",
            a_latex=r"a=\frac{\pi}{3}",
            x1_latex=r"x_1=\frac{3\pi}{10}",
            target_latex=r"\cos\!\left(\frac{3\pi}{10}\right)",
        ),
        LinearApproxExample(
            name="Approximate  ∛(8.15)  using  f(x)=x^{1/3}  at  a=8",
            f=lambda x: np.cbrt(x),
            fp=lambda x: 1.0 / (3.0 * (x ** (2.0 / 3.0))),
            a=8.0,
            x1=8.15,
            x_domain=(6.5, 9.5),
            y_label=r"$y$",
            f_latex=r"f(x)=x^{1/3}",
            a_latex=r"a=8",
            x1_latex=r"x_1=8.15",
            target_latex=r"\sqrt[3]{8.15}",
        ),
    ]


def _render_linear_graph_simulation():
    st.subheader("Graph simulation — Linear approximation (no sliders)")
    st.write(
        "You will **step through** the idea visually: curve → point at "
        r"$x=a$ → tangent line at $a$ → predicted value at the nearby $x_1$."
    )

    ex_list = _linear_examples()
    ex = st.selectbox(
        "Choose a linear-approximation example",
        ex_list,
        format_func=lambda e: e.name,
        key="la_ex_choice",
    )

    step_key = f"la_step_{ex.name}"
    if step_key not in st.session_state:
        st.session_state[step_key] = 1

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back", key=f"la_back_{ex.name}", use_container_width=True):
            st.session_state[step_key] = max(1, st.session_state[step_key] - 1)
    with c2:
        if st.button("Next", key=f"la_next_{ex.name}", use_container_width=True):
            st.session_state[step_key] = min(4, st.session_state[step_key] + 1)

    step = st.session_state[step_key]

    a = ex.a
    x1 = ex.x1
    fa = float(ex.f(np.array([a]))[0])
    fpa = float(ex.fp(a))
    Lx1 = fa + fpa * (x1 - a)
    fx1 = float(ex.f(np.array([x1]))[0])
    err = fx1 - Lx1

    # Explain step BEFORE plot
    if step == 1:
        st.markdown("**Step 1:** Look at the function curve.")
        _katex(ex.f_latex)
    elif step == 2:
        st.markdown("**Step 2:** Mark the anchor point at the approximation center.")
        _katex(rf"\text{{Anchor: }} {ex.a_latex},\quad f(a)")
    elif step == 3:
        st.markdown("**Step 3:** Draw the tangent line at the anchor point (this becomes the linear model).")
        _katex(r"L(x)=f(a)+f'(a)(x-a)")
    else:
        st.markdown("**Step 4:** Use the tangent line to **predict** the nearby value.")
        _katex(ex.x1_latex)
        _katex(rf"{ex.target_latex}\approx L(x_1)\quad \text{{when }}x_1\text{{ is close to }}a")
        st.markdown(
            f"Prediction: **L(x₁) ≈ {Lx1:.6f}** "
            f"(true value ≈ **{fx1:.6f}**, error ≈ **{err:.6f}**)."
        )

    # Smaller plot
    x = np.linspace(ex.x_domain[0], ex.x_domain[1], 600)
    y = ex.f(x)

    fig = plt.figure(figsize=(4.8, 2.8))
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    if step >= 2:
        ax.scatter([a], [fa])
        ax.annotate("  (a, f(a))", (a, fa), fontsize=9)

    if step >= 3:
        xt = np.linspace(max(ex.x_domain[0], a - 1.2), min(ex.x_domain[1], a + 1.2), 200)
        yt = fa + fpa * (xt - a)
        ax.plot(xt, yt)

    if step >= 4:
        ax.scatter([x1], [Lx1])
        ax.annotate("  (x₁, L(x₁))", (x1, Lx1), fontsize=9)
        ax.plot([x1, x1], [min(Lx1, fx1), max(Lx1, fx1)], linestyle="--", linewidth=1)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(ex.y_label)
    ax.set_title("Linear approximation (step view)")
    ax.grid(True, alpha=0.25)

    _pyplot_small(fig, width_mode="content")

    st.markdown("**What to notice:**")
    st.markdown(
        "- If \(x_1\) is **close** to \(a\), the tangent line stays very close to the curve.\n"
        "- If \(x_1\) is far from \(a\), the tangent line can drift away (accuracy drops)."
    )


def _render_newton_graph_simulation():
    st.subheader("Graph simulation — Newton’s method (no sliders)")
    st.write(
        "You will step through Newton’s method visually: curve → initial guess "
        r"$x_0$ → tangent line → new guess $x_1$ → repeat."
    )

    examples = [
        {
            "name": "Solve  x^3 − 7 = 0  (approximates  ∛7)",
            "f": lambda x: x**3 - 7,
            "fp": lambda x: 3 * x**2,
            "x0": 2.0,
            "x_domain": (0.0, 3.0),
            "f_latex": r"f(x)=x^3-7",
        },
        {
            "name": "Solve  x^5 − x + 1 = 0  (one real root near −1.17)",
            "f": lambda x: x**5 - x + 1,
            "fp": lambda x: 5 * x**4 - 1,
            "x0": -1.0,
            "x_domain": (-2.2, 0.6),
            "f_latex": r"f(x)=x^5-x+1",
        },
    ]

    choice = st.selectbox("Choose a Newton example", examples, format_func=lambda e: e["name"], key="nm_ex_choice")

    step_key = f"nm_step_{choice['name']}"
    if step_key not in st.session_state:
        st.session_state[step_key] = 0

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Back", key=f"nm_back_{choice['name']}", use_container_width=True):
            st.session_state[step_key] = max(0, st.session_state[step_key] - 1)
    with c2:
        if st.button("Next", key=f"nm_next_{choice['name']}", use_container_width=True):
            st.session_state[step_key] = min(3, st.session_state[step_key] + 1)

    iters_to_show = st.session_state[step_key]

    _katex(choice["f_latex"])
    _katex(r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}")

    xs = [float(choice["x0"])]
    for _ in range(3):
        x = xs[-1]
        fx = float(choice["f"](x))
        fpx = float(choice["fp"](x))
        if abs(fpx) < 1e-12:
            break
        xs.append(x - fx / fpx)

    st.markdown("**What you should do each iteration:**")
    st.markdown(
        "1. Evaluate **\(f(x_n)\)**.\n"
        "2. Evaluate **\(f'(x_n)\)**.\n"
        "3. Compute **\(x_{n+1}\)** using the update.\n"
        "4. Stop when \(x_{n+1}\approx x_n\) and \(|f(x_n)|\) is tiny."
    )

    xd0, xd1 = choice["x_domain"]
    xgrid = np.linspace(xd0, xd1, 700)
    ygrid = choice["f"](xgrid)

    fig = plt.figure(figsize=(4.8, 2.8))
    ax = fig.add_subplot(111)
    ax.plot(xgrid, ygrid)
    ax.axhline(0, linewidth=1)

    for n in range(min(iters_to_show + 1, len(xs))):
        x_n = xs[n]
        y_n = float(choice["f"](x_n))
        ax.scatter([x_n], [y_n])
        ax.annotate(f"  x{n}", (x_n, y_n), fontsize=9)

        if n < iters_to_show and n + 1 < len(xs):
            slope = float(choice["fp"](x_n))
            xt = np.linspace(max(xd0, x_n - 0.6), min(xd1, x_n + 0.6), 80)
            yt = y_n + slope * (xt - x_n)
            ax.plot(xt, yt)

            x_next = xs[n + 1]
            ax.scatter([x_next], [0.0])
            ax.annotate(f"  x{n+1}", (x_next, 0.0), fontsize=9)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title("Newton’s method (step view)")
    ax.grid(True, alpha=0.25)
    _pyplot_small(fig, width_mode="content")

    st.markdown("**Current iteration values (rounded):**")
    rows = []
    for i, xv in enumerate(xs[: iters_to_show + 2]):
        rows.append((i, xv, float(choice["f"](xv))))
    st.table([{"n": n, "x_n": f"{xv:.10f}", "f(x_n)": f"{fxv:.3e}"} for (n, xv, fxv) in rows])


# -----------------------------
# Blackboard simulations (step-by-step)
# -----------------------------
def _sim_linear_cos_pi():
    # ✅ Updated: target is cos(3π/10) (pi form)
    steps = [
        BoardStep(r"f(x)=\cos x,\quad a=\frac{\pi}{3}", r"Goal: build the tangent-line model at \(x=a\), then use it to estimate a nearby value."),
        BoardStep(r"\text{Estimate }\cos\!\left(\frac{3\pi}{10}\right)", r"The target input is written in terms of \(\pi\)."),
        BoardStep(r"f(a)=\cos\!\left(\frac{\pi}{3}\right)=\frac12", r"This is the anchor value at the center point \(a\)."),
        BoardStep(r"f'(x)=-\sin x", r"Differentiate \( \cos x \)."),
        BoardStep(r"f'(a)=-\sin\!\left(\frac{\pi}{3}\right)=-\frac{\sqrt3}{2}", r"This is the tangent slope at the anchor point."),
        BoardStep(r"L(x)=f(a)+f'(a)(x-a)", r"Linear approximation (tangent-line model)."),
        BoardStep(r"L(x)=\frac12-\frac{\sqrt3}{2}\left(x-\frac{\pi}{3}\right)", r"Substitute the anchor values into the model."),
        BoardStep(
            r"L\!\left(\frac{3\pi}{10}\right)=\frac12-\frac{\sqrt3}{2}\left(\frac{3\pi}{10}-\frac{\pi}{3}\right)\approx 0.5907",
            r"Evaluate at \(x=\frac{3\pi}{10}\)."
        ),
        BoardStep(
            r"\cos\!\left(\frac{3\pi}{10}\right)\approx L\!\left(\frac{3\pi}{10}\right)\approx 0.5907",
            r"Conclusion: since \(\frac{3\pi}{10}\) is close to \(\frac{\pi}{3}\), the tangent-line prediction is accurate."
        ),
    ]
    render_simulation(steps, "Mini Blackboard — Linear approximation (cos example in π form)")


def _sim_differentials_cuberoot():
    steps = [
        BoardStep(r"f(x)=x^{1/3},\quad a=8,\quad x=8.15", r"We estimate \(f(8.15)\) using differentials near \(a=8\)."),
        BoardStep(r"f(8)=\sqrt[3]{8}=2", r"The anchor value is exact."),
        BoardStep(r"f'(x)=\frac{1}{3x^{2/3}}", r"Differentiate \(x^{1/3}\)."),
        BoardStep(r"f'(8)=\frac{1}{3\cdot 8^{2/3}}=\frac{1}{12}", r"Compute the slope at the anchor point."),
        BoardStep(r"dx=x-a=8.15-8=0.15", r"Small input change."),
        BoardStep(r"dy=f'(a)\,dx=\frac{1}{12}(0.15)=0.0125", r"Differential estimate of the output change."),
        BoardStep(r"f(8.15)\approx f(8)+dy=2+0.0125=2.0125", r"Final estimate using \(f(a)+dy\)."),
    ]
    render_simulation(steps, "Mini Blackboard — Differentials (cube root example)")


def _sim_newton_cuberoot7():
    steps = [
        BoardStep(r"\text{Solve }x^3-7=0\quad(\text{this gives }\sqrt[3]{7})", r"Turn the root problem into \(f(x)=0\)."),
        BoardStep(r"f(x)=x^3-7,\quad f'(x)=3x^2", r"Newton needs \(f\) and \(f'\)."),
        BoardStep(r"x_0=2", r"Choose an initial guess near the root (because \(2^3=8\) is close to \(7\))."),
        BoardStep(r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}", r"Newton update formula."),
        BoardStep(r"x_1=2-\frac{2^3-7}{3\cdot 2^2}=2-\frac{1}{12}=\frac{23}{12}\approx 1.9166667", r"First refinement."),
        BoardStep(r"x_2\approx 1.9129384583", r"Second refinement (already very close)."),
        BoardStep(r"x_3\approx 1.9129311828", r"Third refinement (typically enough)."),
        BoardStep(r"\sqrt[3]{7}\approx 1.9129311828", r"Conclusion: the root is the cube root."),
    ]
    render_simulation(steps, "Mini Blackboard — Newton’s method (cube root of 7)")


# -----------------------------
# Practice (15 questions, Hint + Show Answer)
# -----------------------------
@dataclass
class PracticeQ:
    title: str
    prompt_lines: List[str]
    prompt_math: List[str]
    hint_lines: List[str]
    hint_math: List[str]
    answer_lines: List[str]
    answer_math: List[str]


def _practice_questions() -> List[PracticeQ]:
    return [
        PracticeQ(
            title="Q1 — Linear approximation (square root)",
            prompt_lines=["Estimate the value using a linear approximation at the given anchor point."],
            prompt_math=[r"\text{Use }f(x)=\sqrt{x}\text{ at }a=4\text{ to estimate }\sqrt{3.9}."],
            hint_lines=["Use the tangent line model at a: compute f(a) and f'(a)."],
            hint_math=[r"L(x)=f(a)+f'(a)(x-a),\quad f'(x)=\frac{1}{2\sqrt{x}}."],
            answer_lines=["Compute anchor values, build L(x), then evaluate at x=3.9."],
            answer_math=[
                r"f(4)=2,\quad f'(4)=\frac{1}{2\cdot 2}=\frac14.",
                r"L(x)=2+\frac14(x-4).",
                r"\sqrt{3.9}\approx L(3.9)=2+\frac14(-0.1)=1.975."
            ],
        ),
        PracticeQ(
            title="Q2 — Linear approximation (trig, π form)",
            prompt_lines=["Estimate the value using a linear approximation at the given anchor point."],
            prompt_math=[
                r"\text{Use }f(x)=\cos x\text{ at }a=\frac{\pi}{3}\text{ to estimate }\cos\!\left(\frac{3\pi}{10}\right)."
            ],
            hint_lines=["Differentiate cos(x), then plug into the tangent-line model."],
            hint_math=[r"f'(x)=-\sin x,\quad L(x)=f(a)+f'(a)(x-a)."],
            answer_lines=["Use the tangent line at a=π/3."],
            answer_math=[
                r"f(a)=\cos\!\left(\frac{\pi}{3}\right)=\frac12,\quad f'(a)=-\sin\!\left(\frac{\pi}{3}\right)=-\frac{\sqrt3}{2}.",
                r"L(x)=\frac12-\frac{\sqrt3}{2}\left(x-\frac{\pi}{3}\right).",
                r"\cos\!\left(\frac{3\pi}{10}\right)\approx L\!\left(\frac{3\pi}{10}\right)\approx 0.5907."
            ],
        ),
        PracticeQ(
            title="Q3 — Differentials (small change)",
            prompt_lines=["Estimate the change in the function using differentials."],
            prompt_math=[r"y=x^3,\quad x=2,\quad dx=0.01.\ \text{Estimate }dy\text{ and }y(2.01)."],
            hint_lines=["Compute dy = f'(a) dx at a=2."],
            hint_math=[r"f'(x)=3x^2,\quad dy=f'(2)\,dx."],
            answer_lines=["Use the derivative at x=2 to estimate the change."],
            answer_math=[
                r"f'(2)=3(2)^2=12.",
                r"dy\approx 12(0.01)=0.12.",
                r"y(2.01)\approx 8+0.12=8.12."
            ],
        ),
        PracticeQ(
            title="Q4 — Differentials (cube root)",
            prompt_lines=["Estimate the value using differentials near the anchor point."],
            prompt_math=[r"\text{Use }f(x)=x^{1/3}\text{ at }a=8\text{ to estimate }\sqrt[3]{8.07}."],
            hint_lines=["Compute f(8), f'(8), dx=8.07−8, then f(8)+dy."],
            hint_math=[r"f'(x)=\frac{1}{3x^{2/3}},\quad dy=f'(a)\,dx."],
            answer_lines=["Use the differential estimate dy."],
            answer_math=[
                r"f(8)=2,\quad f'(8)=\frac{1}{12}.",
                r"dx=0.07,\quad dy\approx \frac{1}{12}(0.07)\approx 0.0058333.",
                r"\sqrt[3]{8.07}\approx 2.0058333."
            ],
        ),
        PracticeQ(
            title="Q5 — Linear approximation (small-angle, π form)",
            prompt_lines=["Use a linear approximation near the anchor point."],
            prompt_math=[r"\text{Use the linear approximation of }\sin x\text{ near }0\text{ to estimate }\sin\!\left(\frac{\pi}{40}\right)."],
            hint_lines=["Near 0, sin x is very close to its tangent line."],
            hint_math=[r"\sin x\approx x\quad \text{for }x\text{ close to }0."],
            answer_lines=["Apply the standard small-angle linear approximation."],
            answer_math=[r"\sin\!\left(\frac{\pi}{40}\right)\approx \frac{\pi}{40}."],
        ),
        PracticeQ(
            title="Q6 — Newton’s method (one iteration)",
            prompt_lines=["Use Newton’s method to produce one improved approximation."],
            prompt_math=[r"f(x)=x^3-7,\quad x_0=2.\ \text{Find }x_1."],
            hint_lines=["Use the Newton update formula."],
            hint_math=[r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)},\quad f'(x)=3x^2."],
            answer_lines=["Compute f(2), f'(2), then update."],
            answer_math=[
                r"f(2)=1,\quad f'(2)=12.",
                r"x_1=2-\frac{1}{12}=\frac{23}{12}\approx 1.9166667."
            ],
        ),
        PracticeQ(
            title="Q7 — Newton’s method (two iterations)",
            prompt_lines=["Continue Newton’s method for one more step."],
            prompt_math=[r"f(x)=x^3-7,\quad x_0=2.\ \text{Find }x_2\text{ (use }x_1\text{ from Q6)}."],
            hint_lines=["Substitute x1 into the update formula."],
            hint_math=[r"x_2=x_1-\frac{x_1^3-7}{3x_1^2}."],
            answer_lines=["Use x1 ≈ 1.9166667."],
            answer_math=[r"x_2\approx 1.9129384583."],
        ),
        PracticeQ(
            title="Q8 — Newton’s method (set up from a root statement)",
            prompt_lines=["Rewrite the statement as f(x)=0, then write the Newton iteration."],
            prompt_math=[r"\text{Use Newton’s method to approximate }\sqrt[4]{5}."],
            hint_lines=["Let x be the root and rewrite as an equation."],
            hint_math=[r"x=\sqrt[4]{5}\iff x^4-5=0."],
            answer_lines=["Create f and f′, then write the update."],
            answer_math=[
                r"f(x)=x^4-5,\quad f'(x)=4x^3.",
                r"x_{n+1}=x_n-\frac{x_n^4-5}{4x_n^3}."
            ],
        ),
        PracticeQ(
            title="Q9 — Linear approximation (exponential near 0)",
            prompt_lines=["Estimate the value using the tangent-line approximation at a=0."],
            prompt_math=[r"\text{Use }f(x)=e^x\text{ at }a=0\text{ to estimate }e^{0.05}."],
            hint_lines=["Compute f(0) and f'(0)."],
            hint_math=[r"f(0)=1,\quad f'(0)=1."],
            answer_lines=["Build L(x) at 0."],
            answer_math=[r"L(x)=1+x,\quad e^{0.05}\approx 1.05."],
        ),
        PracticeQ(
            title="Q10 — Differentials (square root)",
            prompt_lines=["Estimate the change in y using differentials."],
            prompt_math=[r"y=\sqrt{x},\quad x=9,\quad dx=-0.12.\ \text{Estimate }dy\text{ and }\sqrt{8.88}."],
            hint_lines=["Use dy=f'(a)dx at a=9."],
            hint_math=[r"f'(x)=\frac{1}{2\sqrt{x}}."],
            answer_lines=["Compute the derivative at 9 and apply dx."],
            answer_math=[
                r"f(9)=3,\quad f'(9)=\frac{1}{6}.",
                r"dy\approx \frac{1}{6}(-0.12)=-0.02.",
                r"\sqrt{8.88}\approx 2.98."
            ],
        ),
        PracticeQ(
            title="Q11 — Linear approximation (log)",
            prompt_lines=["Write the linear approximation function L(x) at x=a."],
            prompt_math=[r"f(x)=\ln x,\quad a=1.\ \text{Write }L(x)\text{ and estimate }\ln(1.03)."],
            hint_lines=["Compute f(1) and f'(1)."],
            hint_math=[r"f(1)=0,\quad f'(1)=1."],
            answer_lines=["Build L(x) and evaluate at 1.03."],
            answer_math=[r"L(x)=x-1,\quad \ln(1.03)\approx 0.03."],
        ),
        PracticeQ(
            title="Q12 — Newton’s method (trig, π form)",
            prompt_lines=["Write f(x)=0 and perform one Newton step."],
            prompt_math=[r"\text{Solve }\sin x=\frac12\text{ using Newton’s method with }x_0=\frac{\pi}{5}.\ \text{Find }x_1."],
            hint_lines=["Rewrite as f(x)=sin x − 1/2. Then f'(x)=cos x."],
            hint_math=[r"x_1=x_0-\frac{\sin x_0-\frac12}{\cos x_0}."],
            answer_lines=["Substitute x0=π/5."],
            answer_math=[
                r"f(x)=\sin x-\frac12,\quad f'(x)=\cos x.",
                r"x_1=\frac{\pi}{5}-\frac{\sin\!\left(\frac{\pi}{5}\right)-\frac12}{\cos\!\left(\frac{\pi}{5}\right)}."
            ],
        ),
        PracticeQ(
            title="Q13 — Newton’s method (why it can fail)",
            prompt_lines=["Explain (briefly) why Newton’s method fails if f'(x0)=0."],
            prompt_math=[r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}"],
            hint_lines=["Look at the denominator and the geometry of the tangent line."],
            hint_math=[r"f'(x_0)=0\Rightarrow \text{horizontal tangent and division by }0."],
            answer_lines=["The update is undefined (division by 0), and a horizontal tangent may not cross the x-axis."],
            answer_math=[],
        ),
        PracticeQ(
            title="Q14 — When linear approximation is accurate",
            prompt_lines=["State when a linear approximation is expected to be accurate."],
            prompt_math=[r"f(x)\approx f(a)+f'(a)(x-a)"],
            hint_lines=["Think: “nearby” and “smooth curve”."],
            hint_math=[],
            answer_lines=["It is accurate when x is close to a and the function is smooth (not rapidly changing curvature)."],
            answer_math=[],
        ),
        PracticeQ(
            title="Q15 — Newton stopping check",
            prompt_lines=["You computed x3 using Newton’s method. What two quick checks confirm it is acceptable?"],
            prompt_math=[],
            hint_lines=["One check is about how much xn changes; the other is about f(xn)."],
            hint_math=[],
            answer_lines=[
                "1) Successive values stop changing much (xₙ₊₁ ≈ xₙ).",
                "2) The function value is extremely close to zero (|f(xₙ)| is tiny).",
            ],
            answer_math=[],
        ),
    ]


def _render_practice():
    st.subheader("Practice (15 questions)")
    st.write("Each question has **Hint** and **Show answer**. The full solution appears all at once when you click **Show answer**.")

    qs = _practice_questions()
    for i, q in enumerate(qs, start=1):
        with st.expander(f"{q.title}", expanded=False):
            for line in q.prompt_lines:
                st.write(line)
            for m in q.prompt_math:
                _katex(m)

            k_hint = f"p51_hint_{i}"
            k_ans = f"p51_ans_{i}"
            if k_hint not in st.session_state:
                st.session_state[k_hint] = False
            if k_ans not in st.session_state:
                st.session_state[k_ans] = False

            b1, b2 = st.columns([1, 1])
            with b1:
                if st.button("Hint", key=f"btn_hint_{i}", use_container_width=True):
                    st.session_state[k_hint] = True
            with b2:
                if st.button("Show answer", key=f"btn_ans_{i}", use_container_width=True):
                    st.session_state[k_ans] = True

            if st.session_state[k_hint]:
                st.markdown("**Hint:**")
                for line in q.hint_lines:
                    st.write(line)
                for m in q.hint_math:
                    _katex(m)

            if st.session_state[k_ans]:
                st.markdown("**Answer (full solution):**")
                for line in q.answer_lines:
                    st.write(line)
                for m in q.answer_math:
                    _katex(m)


# -----------------------------
# Main render()
# -----------------------------
def render():
    st.markdown("## Subtopic 5.1: Linear Approximations and Newton’s Method")

    st.markdown("### Lesson Objectives")
    st.write("By the end of this lesson, you should be able to:")

    st.markdown("- **5.1.1** Use the tangent line (linear approximation) at an anchor point to estimate nearby function values.")
    _katex(r"L(x)=f(a)+f'(a)(x-a),\qquad f(x)\approx L(x)\ \text{when }x\text{ is close to }a.")
    st.markdown("- **5.1.2** Use increments and differentials to estimate small changes.")
    _katex(r"\Delta x=x-a,\qquad \Delta y=f(x)-f(a),\qquad \Delta y\approx dy=f'(a)\,dx.")
    st.markdown("- **5.1.3** Apply Newton’s method to approximate solutions of equations.")
    _katex(r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)},\qquad (n=0,1,2,\ldots).")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.markdown("### ✅ Lesson Roadmap (teacher replacement)")
        st.markdown(
            "- Build the **tangent-line model** and use it for fast estimation.\n"
            "- Use **differentials** to estimate small changes.\n"
            "- Use **Newton’s method** to approximate roots efficiently."
        )

        _hr()

        st.markdown("## 5.1.1 Linear approximation (tangent line idea)")
        st.write("When \(x\) is close to \(a\), the curve behaves almost like its tangent line.")
        st.markdown("**Core model:**")
        _katex(r"L(x)=f(a)+f'(a)(x-a)")
        st.markdown("**Meaning:**")
        _katex(r"f(x)\approx L(x)\quad \text{when }x\text{ is close to }a")

        st.info(
            "Teacher tip: say out loud **“replace the curve with its tangent line near the anchor.”**"
        )

        _render_linear_graph_simulation()

        st.markdown("### Example (step-by-step)")
        st.markdown("**Problem:** Use the tangent-line approximation of the cosine function at the anchor point to estimate the value.")
        _katex(r"\text{Approximate }\cos\!\left(\frac{3\pi}{10}\right)\text{ using }f(x)=\cos x\text{ at }a=\frac{\pi}{3}.")
        st.markdown("**What you should produce:**")
        st.markdown("- Compute \(f(a)\).")
        st.markdown("- Compute \(f'(a)\).")
        st.markdown("- Build \(L(x)\).")
        st.markdown(r"- Evaluate \(L\!\left(\frac{3\pi}{10}\right)\).")
        _sim_linear_cos_pi()

        _hr()

        st.markdown("## 5.1.2 Increments and differentials (estimating small changes)")
        st.write("Differentials give a fast estimate of how much the output changes when the input changes a little.")
        _katex(r"\Delta x=x-a,\qquad \Delta y=f(x)-f(a)")
        _katex(r"dy=f'(a)\,dx\quad\text{and we use }\Delta y\approx dy")

        st.warning(
            "Teacher tip: don’t mix up **Δy** (exact change) with **dy** (tangent-line estimate)."
        )

        st.markdown("### Example (step-by-step)")
        st.markdown("**Problem:** Estimate a cube root near an anchor value using differentials.")
        _katex(r"\text{Estimate }\sqrt[3]{8.15}\text{ using }f(x)=x^{1/3}\text{ at }a=8.")
        st.markdown("**What you should produce:**")
        st.markdown("- Compute \(f(8)\).")
        st.markdown("- Compute \(f'(8)\).")
        st.markdown("- Compute \(dx\).")
        st.markdown("- Compute \(dy=f'(8)\,dx\).")
        st.markdown("- Estimate \(f(8.15)\approx f(8)+dy\).")
        _sim_differentials_cuberoot()

        _hr()

        st.markdown("## 5.1.3 Newton’s method (root-finding by tangent lines)")
        st.write("Newton’s method repeatedly uses tangent lines to jump closer to a root.")
        _katex(r"x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}")

        st.info(
            "Teacher tip: stop when **both** are true: \(x_{n+1}\approx x_n\) and \(|f(x_n)|\) is tiny."
        )

        _render_newton_graph_simulation()

        st.markdown("### Example (step-by-step)")
        st.markdown("**Problem:** Use Newton’s method to approximate a cube root.")
        _katex(r"\text{Approximate }\sqrt[3]{7}\text{ by solving }x^3-7=0.")
        st.markdown("**What you should produce:**")
        st.markdown("- Define \(f(x)\) and \(f'(x)\).")
        st.markdown("- Choose \(x_0\).")
        st.markdown("- Compute \(x_1,x_2,x_3\).")
        st.markdown("- Confirm \(|f(x_3)|\) is close to 0.")
        _sim_newton_cuberoot7()

    with tabs[1]:
        _render_practice()
