# subtopic_4_10_mean_value_theorem.py
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# ------------------------------------------------------------
# Helpers (humanised math everywhere)
# ------------------------------------------------------------
def _latex(expr: str):
    st.latex(expr)


def _md(text: str):
    st.markdown(text)


def _tip_box(title: str, bullets: list[str], kind: str = "info"):
    msg = "**" + title + "**\n\n" + "\n".join([f"- {b}" for b in bullets])
    if kind == "success":
        st.success(msg)
    elif kind == "warning":
        st.warning(msg)
    else:
        st.info(msg)


def _small_plot(fig):
    # Keep graphs visually smaller (no full-width stretch)
    st.pyplot(fig, clear_figure=True, use_container_width=False)


# ------------------------------------------------------------
# Graph utilities (smaller figures)
# ------------------------------------------------------------
def _get_function(choice: str):
    # returns (f, fprime, latex_name)
    if choice == "f(x)=x^2":
        f = lambda x: x**2
        fp = lambda x: 2 * x
        return f, fp, r"f(x)=x^2"
    if choice == "f(x)=x^3-x":
        f = lambda x: x**3 - x
        fp = lambda x: 3 * x**2 - 1
        return f, fp, r"f(x)=x^3-x"
    if choice == r"f(x)=\sin x":
        f = lambda x: np.sin(x)
        fp = lambda x: np.cos(x)
        return f, fp, r"f(x)=\sin x"
    # default e^x
    f = lambda x: np.exp(x)
    fp = lambda x: np.exp(x)
    return f, fp, r"f(x)=e^x"


def _find_c_for_mvt(fp, a: float, b: float, m: float):
    """
    Find c in (a,b) such that fp(c)=m (robust grid + sign-change + bisection).
    """
    xs = np.linspace(a, b, 1400)
    gs = fp(xs) - m

    for i in range(len(xs) - 1):
        if np.isnan(gs[i]) or np.isnan(gs[i + 1]):
            continue
        if gs[i] == 0:
            c = xs[i]
            if a < c < b:
                return float(c)
        if gs[i] * gs[i + 1] < 0:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(70):
                mid = (lo + hi) / 2
                gmid = fp(mid) - m
                glo = fp(lo) - m
                if np.isnan(gmid) or np.isnan(glo):
                    break
                if glo * gmid <= 0:
                    hi = mid
                else:
                    lo = mid
            c = (lo + hi) / 2
            if a < c < b:
                return float(c)

    idx = int(np.nanargmin(np.abs(gs)))
    c = float(xs[idx])
    if c <= a or c >= b:
        c = float((a + b) / 2)
    return c


def _plot_rolle_steps(f, a: float, b: float, c: float, step: int):
    # step 0: curve only
    # step 1: add endpoints
    # step 2: add horizontal tangent at c
    x_min = min(a, b) - 1.0
    x_max = max(a, b) + 1.0
    xs = np.linspace(x_min, x_max, 700)
    ys = f(xs)

    fa = float(f(a))
    fb = float(f(b))
    fc = float(f(c))

    fig = plt.figure(figsize=(5.9, 3.3))
    ax = fig.add_subplot(111)
    ax.plot(xs, ys, label=r"$y=f(x)$")

    if step >= 1:
        ax.scatter([a, b], [fa, fb], s=60)
        ax.plot([a, b], [fa, fb], linestyle="--", linewidth=1.0, label=r"endpoints")

    if step >= 2:
        ax.scatter([c], [fc], s=60)
        ax.plot(xs, np.full_like(xs, fc), linewidth=1.2, label=r"horizontal tangent")

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    ax.set_title("Rolle’s Theorem (graph simulation)")
    ax.legend()
    return fig


def _plot_mvt_steps(f, fp, a: float, b: float, step: int):
    # step 0: curve only
    # step 1: add secant through (a,f(a)), (b,f(b))
    # step 2: add tangent at c where slope matches secant
    if a == b:
        b = a + 1e-6
    if a > b:
        a, b = b, a

    xs = np.linspace(a - 1.0, b + 1.0, 700)
    ys = f(xs)

    fa = float(f(a))
    fb = float(f(b))
    m = (fb - fa) / (b - a)
    c = _find_c_for_mvt(fp, a, b, m)
    fc = float(f(c))

    fig = plt.figure(figsize=(5.9, 3.3))
    ax = fig.add_subplot(111)
    ax.plot(xs, ys, label=r"$y=f(x)$")

    if step >= 1:
        secant_y = fa + m * (xs - a)
        ax.plot(xs, secant_y, linewidth=1.2, label=r"secant line")
        ax.scatter([a, b], [fa, fb], s=60)

    if step >= 2:
        tangent_y = fc + m * (xs - c)
        ax.plot(xs, tangent_y, linewidth=1.2, label=r"tangent at $c$")
        ax.scatter([c], [fc], s=60)

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    ax.set_title("Mean Value Theorem (graph simulation)")
    ax.legend()

    return fig, m, c


def _plot_zero_count_steps(step: int):
    """
    Example: f(x)=x^3-3x+1
    step 0: curve only
    step 1: mark sign-check intervals
    step 2: show derivative critical points x=-1,1 (supports max roots logic)
    """
    f = lambda x: x**3 - 3 * x + 1
    xs = np.linspace(-2.5, 2.5, 800)
    ys = f(xs)

    fig = plt.figure(figsize=(5.9, 3.3))
    ax = fig.add_subplot(111)
    ax.plot(xs, ys, label=r"$f(x)=x^3-3x+1$")
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)

    if step >= 1:
        for xline in [-2, -1, 0, 1, 2]:
            ax.axvline(xline, linestyle="--", linewidth=0.8, alpha=0.6)
        ax.set_title("Zeros (graph simulation): sign-change intervals")
    else:
        ax.set_title("Zeros (graph simulation): curve")

    if step >= 2:
        ax.axvline(-1, linewidth=1.1)
        ax.axvline(1, linewidth=1.1)
        ax.set_title("Zeros (graph simulation): turning points at $x=-1,1$")

    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig


# ------------------------------------------------------------
# Blackboard simulations (ONLY delimiter fixes: use $...$ not \( \) or \[ \])
# ------------------------------------------------------------
def _sim_objective_4101_rolle_statement():
    return [
        BoardStep(
            latex_line=r"\text{Rolle’s Theorem}",
            teacher_explain_md=r"""
Rolle’s Theorem is used when a function starts and ends at the **same height** on an interval.

You will use it to locate at least one point where the tangent is horizontal.
""",
        ),
        BoardStep(
            latex_line=r"\text{If } f \text{ is continuous on } [a,b] \text{ and differentiable on } (a,b) \text{ and } f(a)=f(b),",
            teacher_explain_md=r"""
Before applying the theorem, check:

- Continuity on the closed interval $[a,b]$
- Differentiability on the open interval $(a,b)$
- Endpoint condition $f(a)=f(b)$
""",
        ),
        BoardStep(
            latex_line=r"\text{then there exists } c\in(a,b) \text{ such that } f'(c)=0.",
            teacher_explain_md=r"""
Conclusion:

There is at least one point $c$ inside the interval where the slope is $0$ (a horizontal tangent).
""",
        ),
    ]


def _sim_objective_4101_find_c_poly():
    return [
        BoardStep(
            latex_line=r"\text{Problem: } f(x)=x^2-4x+3 \text{ on } [1,3]. \text{ Find } c \text{ such that } f'(c)=0.",
            teacher_explain_md=r"""
What you should do:

1) Check the Rolle conditions  
2) Differentiate  
3) Solve $f'(c)=0$ and confirm $c\in(1,3)$
""",
        ),
        BoardStep(
            latex_line=r"f(1)=0,\quad f(3)=0 \quad\Rightarrow\quad f(1)=f(3)",
            teacher_explain_md=r"Endpoint condition is satisfied.",
        ),
        BoardStep(
            latex_line=r"f'(x)=2x-4",
            teacher_explain_md=r"Differentiate the function.",
        ),
        BoardStep(
            latex_line=r"2c-4=0 \quad\Rightarrow\quad c=2",
            teacher_explain_md=r"Since $2\in(1,3)$, the value is valid.",
        ),
    ]


def _sim_objective_4101_find_c_trig():
    return [
        BoardStep(
            latex_line=r"\text{Problem: } f(x)=\sin x \text{ on } [0,\pi]. \text{ Find } c \text{ such that } f'(c)=0.",
            teacher_explain_md=r"""
What you should do:

- Verify $f(0)=f(\pi)$
- Compute $f'(x)$
- Solve $f'(c)=0$ in $(0,\pi)$
""",
        ),
        BoardStep(
            latex_line=r"f(0)=0,\quad f(\pi)=0 \quad\Rightarrow\quad f(0)=f(\pi)",
            teacher_explain_md=r"Endpoint condition is satisfied.",
        ),
        BoardStep(
            latex_line=r"f'(x)=\cos x",
            teacher_explain_md=r"Differentiate the function.",
        ),
        BoardStep(
            latex_line=r"\cos c=0 \quad\Rightarrow\quad c=\frac{\pi}{2}",
            teacher_explain_md=r"$\frac{\pi}{2}\in(0,\pi)$, so it is valid.",
        ),
    ]


def _sim_objective_4102_mvt_statement():
    return [
        BoardStep(
            latex_line=r"\text{Mean Value Theorem (MVT)}",
            teacher_explain_md=r"""
The Mean Value Theorem compares:

- the **average rate of change** on $[a,b]$  
with  
- the **instantaneous rate of change** at some interior point.
""",
        ),
        BoardStep(
            latex_line=r"\text{If } f \text{ is continuous on } [a,b] \text{ and differentiable on } (a,b),",
            teacher_explain_md=r"""
Check these two conditions:

- Continuous on $[a,b]$  
- Differentiable on $(a,b)$
""",
        ),
        BoardStep(
            latex_line=r"\text{then there exists } c\in(a,b) \text{ such that } f'(c)=\frac{f(b)-f(a)}{b-a}.",
            teacher_explain_md=r"""
The equality says:

A tangent slope $f'(c)$ matches the secant slope:
$$\frac{f(b)-f(a)}{b-a}.$$
""",
        ),
    ]


def _sim_objective_4102_find_c_example():
    return [
        BoardStep(
            latex_line=r"\text{Problem: } f(x)=x^2 \text{ on } [1,3]. \text{ Find } c \text{ such that } f'(c)=\frac{f(3)-f(1)}{3-1}.",
            teacher_explain_md=r"""
What you should do:

1) Compute the secant slope  
2) Compute the derivative $f'(x)$  
3) Solve $f'(c)=$ secant slope
""",
        ),
        BoardStep(
            latex_line=r"\frac{f(3)-f(1)}{3-1}=\frac{9-1}{2}=4",
            teacher_explain_md=r"Average slope on $[1,3]$.",
        ),
        BoardStep(
            latex_line=r"f'(x)=2x",
            teacher_explain_md=r"Derivative of $x^2$.",
        ),
        BoardStep(
            latex_line=r"2c=4 \quad\Rightarrow\quad c=2",
            teacher_explain_md=r"Since $2\in(1,3)$, it is valid.",
        ),
    ]


def _sim_objective_4103_ivt_and_zeros():
    return [
        BoardStep(
            latex_line=r"\text{Intermediate Value Theorem (IVT) for zeros}",
            teacher_explain_md=r"""
If a function is continuous and changes sign, it must cross the $x$-axis.

This is the main tool for **guaranteeing** a zero exists.
""",
        ),
        BoardStep(
            latex_line=r"\text{If } f \text{ is continuous on } [a,b] \text{ and } f(a)\,f(b)<0,\ \text{then there exists } c\in(a,b) \text{ such that } f(c)=0.",
            teacher_explain_md=r"""
Sign change condition:
$$f(a)\,f(b)<0.$$
Then a root exists between $a$ and $b$.
""",
        ),
        BoardStep(
            latex_line=r"\text{Rolle consequence: if } f(x_1)=0 \text{ and } f(x_2)=0 \text{ with } x_1<x_2,\ \text{then there exists } d\in(x_1,x_2) \text{ such that } f'(d)=0.",
            teacher_explain_md=r"""
Meaning:

Between two distinct roots of $f$, there is at least one point where $f'(x)=0$.

This helps you **limit** how many roots a function can have.
""",
        ),
    ]


def _sim_objective_4103_three_zeros_example():
    return [
        BoardStep(
            latex_line=r"\text{Problem: Determine the number of zeros of } f(x)=x^3-3x+1.",
            teacher_explain_md=r"""
What you should do:

1) Use the derivative to understand the turning points  
2) Use the sign-change idea to confirm zeros exist in specific intervals  
3) Conclude how many zeros there are
""",
        ),
        BoardStep(
            latex_line=r"f'(x)=3x^2-3=3(x-1)(x+1)",
            teacher_explain_md=r"""
Critical points:
$$f'(x)=0 \Rightarrow x=-1,\ 1.$$
So $f$ can change direction only at these points.
""",
        ),
        BoardStep(
            latex_line=r"f(-2)=-1,\quad f(-1)=3 \quad\Rightarrow\quad \exists\,c_1\in(-2,-1)\text{ with } f(c_1)=0",
            teacher_explain_md=r"Sign change $\Rightarrow$ a zero exists in $(-2,-1)$.",
        ),
        BoardStep(
            latex_line=r"f(0)=1,\quad f(1)=-1 \quad\Rightarrow\quad \exists\,c_2\in(0,1)\text{ with } f(c_2)=0",
            teacher_explain_md=r"Sign change $\Rightarrow$ a zero exists in $(0,1)$.",
        ),
        BoardStep(
            latex_line=r"f(1)=-1,\quad f(2)=3 \quad\Rightarrow\quad \exists\,c_3\in(1,2)\text{ with } f(c_3)=0",
            teacher_explain_md=r"Sign change $\Rightarrow$ a zero exists in $(1,2)$.",
        ),
        BoardStep(
            latex_line=r"\text{Conclusion: } f \text{ has at least 3 zeros. Since } f'(x)=0 \text{ at only two points, } f \text{ cannot have more than 3 zeros.}",
            teacher_explain_md=r"""
Why “cannot have more than 3”?

If there were 4 distinct zeros, the Rolle consequence would force at least 3 distinct zeros of $f'$, but $f'$ has only 2.
""",
        ),
        BoardStep(
            latex_line=r"\text{Therefore } f(x)=x^3-3x+1 \text{ has exactly 3 zeros.}",
            teacher_explain_md=r"Final statement.",
        ),
    ]


def _sim_objective_4104_same_derivative_constant():
    return [
        BoardStep(
            latex_line=r"\text{If two functions have the same derivative, they differ by a constant.}",
            teacher_explain_md=r"""
Key idea:

If $f'(x)=g'(x)$ on an open interval $I$, then their graphs have the same slope everywhere on $I$.
So the vertical gap between them stays constant.
""",
        ),
        BoardStep(
            latex_line=r"\text{Let } h(x)=f(x)-g(x). \ \text{Then } h'(x)=f'(x)-g'(x)=0 \ \text{on } I.",
            teacher_explain_md=r"""
Create a new function:
$$h(x)=f(x)-g(x).$$
If the derivatives match, then $h'(x)=0$.
""",
        ),
        BoardStep(
            latex_line=r"\text{For any } a<b \text{ in } I,\ \text{MVT gives } h(b)-h(a)=h'(c)(b-a)=0.",
            teacher_explain_md=r"""
Apply MVT to $h$ on $[a,b]\subset I$:

Since $h'(c)=0$, the change $h(b)-h(a)$ must be $0$.
""",
        ),
        BoardStep(
            latex_line=r"h(b)=h(a)\ \text{for all } a,b\in I \ \Rightarrow\ h(x)=C\ \text{(constant)} \ \Rightarrow\ f(x)-g(x)=C.",
            teacher_explain_md=r"""
So $h$ is constant:
$$f(x)-g(x)=C$$
for all $x\in I$.
""",
        ),
    ]


def _sim_objective_4104_find_function_example():
    return [
        BoardStep(
            latex_line=r"\text{Problem: } f'(x)=2x \text{ and } f(0)=5. \text{ Find } f(x).",
            teacher_explain_md=r"""
What you should do:

- Recognise that any function with derivative $2x$ looks like $x^2+C$
- Use the given point to find $C$
""",
        ),
        BoardStep(
            latex_line=r"\text{Since } \frac{d}{dx}(x^2)=2x,\ \text{we write } f(x)=x^2+C.",
            teacher_explain_md=r"General form.",
        ),
        BoardStep(
            latex_line=r"f(0)=0^2+C=5 \Rightarrow C=5",
            teacher_explain_md=r"Use the condition to identify the constant.",
        ),
        BoardStep(
            latex_line=r"f(x)=x^2+5",
            teacher_explain_md=r"Final answer.",
        ),
    ]


# ------------------------------------------------------------
# Practice bank (KEEP EXACTLY AS IS — DO NOT CHANGE)
# ------------------------------------------------------------
def _practice_questions():
    qs = []

    qs.append({
        "q_latex": r"\text{State the Mean Value Theorem (MVT) including all conditions.}",
        "hint_md": r"Write the continuity condition on $[a,b]$ and differentiability on $(a,b)$, then the conclusion $f'(c)=\dfrac{f(b)-f(a)}{b-a}$.",
        "ans_steps_latex": [
            r"\text{If }f\text{ is continuous on }[a,b]\text{ and differentiable on }(a,b),",
            r"\text{then there exists }c\in(a,b)\text{ such that }f'(c)=\frac{f(b)-f(a)}{b-a}.",
        ],
    })

    qs.append({
        "q_latex": r"\text{Does MVT apply to }f(x)=|x|\text{ on }[-1,1]?\ \text{Explain.}",
        "hint_md": r"Check differentiability on $(-1,1)$. The cusp at $x=0$ is the issue.",
        "ans_steps_latex": [
            r"f(x)=|x|\text{ is continuous on }[-1,1].",
            r"f(x)\text{ is not differentiable at }x=0\ (\text{cusp}).",
            r"\text{So MVT does not apply on }[-1,1].",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find }c\text{ for }f(x)=x^2\text{ on }[1,3].",
        "hint_md": r"Compute secant slope $\dfrac{f(3)-f(1)}{3-1}$ and solve $2c=$ that value.",
        "ans_steps_latex": [
            r"\frac{f(3)-f(1)}{3-1}=\frac{9-1}{2}=4",
            r"f'(x)=2x",
            r"2c=4\Rightarrow c=2",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find }c\text{ for }f(x)=x^3\text{ on }[0,2].",
        "hint_md": r"Secant slope is $\dfrac{8-0}{2}=4$. Set $f'(c)=3c^2=4$.",
        "ans_steps_latex": [
            r"\frac{f(2)-f(0)}{2-0}=\frac{8-0}{2}=4",
            r"f'(x)=3x^2",
            r"3c^2=4\Rightarrow c=\sqrt{\frac{4}{3}}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find }c\text{ for }f(x)=\sin x\text{ on }[0,\pi].",
        "hint_md": r"The secant slope is $0$ because $\sin(0)=\sin(\pi)=0$. Solve $\cos(c)=0$.",
        "ans_steps_latex": [
            r"\frac{f(\pi)-f(0)}{\pi-0}=\frac{0-0}{\pi}=0",
            r"f'(x)=\cos x",
            r"\cos(c)=0\Rightarrow c=\frac{\pi}{2}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Rolle’s Theorem: }f(x)=x^2-4x+3\text{ on }[1,3].\ \text{Find }c.",
        "hint_md": r"Check $f(1)=f(3)$ then solve $f'(c)=0$.",
        "ans_steps_latex": [
            r"f(1)=1-4+3=0,\quad f(3)=9-12+3=0\Rightarrow f(1)=f(3)",
            r"f'(x)=2x-4",
            r"2c-4=0\Rightarrow c=2",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find }c\text{ for }f(x)=\frac{1}{x}\text{ on }[1,4].",
        "hint_md": r"Compute secant slope $\dfrac{\frac14-1}{3}=-\frac14$. Set $-\frac{1}{c^2}=-\frac14$.",
        "ans_steps_latex": [
            r"\frac{f(4)-f(1)}{4-1}=\frac{\frac14-1}{3}=\frac{-\frac34}{3}=-\frac14",
            r"f'(x)=-\frac{1}{x^2}",
            r"-\frac{1}{c^2}=-\frac14\Rightarrow c^2=4\Rightarrow c=2",
        ],
    })

    qs.append({
        "q_latex": r"\text{Does MVT apply to }f(x)=\frac{1}{x-1}\text{ on }[0,2]?\ \text{Explain.}",
        "hint_md": r"Check continuity on $[0,2]$. There is a vertical asymptote at $x=1$.",
        "ans_steps_latex": [
            r"f(x)=\frac{1}{x-1}\text{ is not defined at }x=1",
            r"\text{So it is not continuous on }[0,2]",
            r"\text{Therefore MVT does not apply.}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find }c\text{ for }f(x)=\ln x\text{ on }[1,e].",
        "hint_md": r"Secant slope is $\dfrac{1-0}{e-1}=\dfrac{1}{e-1}$. Set $f'(c)=\dfrac{1}{c}$.",
        "ans_steps_latex": [
            r"\frac{f(e)-f(1)}{e-1}=\frac{1-0}{e-1}=\frac{1}{e-1}",
            r"f'(x)=\frac{1}{x}",
            r"\frac{1}{c}=\frac{1}{e-1}\Rightarrow c=e-1",
        ],
    })

    qs.append({
        "q_latex": r"\text{Use MVT to prove: }|\sin b-\sin a|\le |b-a|.",
        "hint_md": r"Apply MVT to $f(x)=\sin x$ then use $|\cos c|\le 1$.",
        "ans_steps_latex": [
            r"f(x)=\sin x\Rightarrow f'(x)=\cos x",
            r"\sin b-\sin a=\cos(c)(b-a)\ \text{for some }c\in(a,b)",
            r"|\sin b-\sin a|=|\cos(c)|\,|b-a|\le 1\cdot |b-a|=|b-a|",
        ],
    })

    qs.append({
        "q_latex": r"\text{Use MVT to show }e^x\text{ is increasing on }\mathbb{R}.",
        "hint_md": r"Take $a<b$. Use $e^b-e^a=e^c(b-a)$ with $e^c>0$.",
        "ans_steps_latex": [
            r"\text{Let }a<b. \text{ MVT gives } e^b-e^a=e^c(b-a)\text{ for some }c\in(a,b).",
            r"e^c>0\ \text{and }(b-a)>0\Rightarrow e^b-e^a>0",
            r"\Rightarrow e^b>e^a\ \text{so }e^x\text{ is increasing.}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Does MVT apply to }f(x)=\sqrt[3]{x}\text{ on }[-1,1]?\ \text{Explain.}",
        "hint_md": r"Check differentiability on $(-1,1)$. The derivative involves $x^{-2/3}$.",
        "ans_steps_latex": [
            r"f(x)=x^{1/3}\text{ is continuous on }[-1,1].",
            r"f'(x)=\frac{1}{3}x^{-2/3}\text{ is undefined at }x=0.",
            r"\text{So MVT does not apply on }[-1,1].",
        ],
    })

    qs.append({
        "q_latex": r"\text{If }f'(x)=0\text{ for all }x\in(a,b),\text{ show that }f\text{ is constant on }(a,b).",
        "hint_md": r"Use MVT on any interval $[u,v]\subset(a,b)$.",
        "ans_steps_latex": [
            r"\text{Choose any }u<v\text{ in }(a,b).",
            r"\text{MVT gives }f(v)-f(u)=f'(c)(v-u)\text{ for some }c\in(u,v).",
            r"f'(c)=0\Rightarrow f(v)-f(u)=0\Rightarrow f(v)=f(u).",
            r"\text{So }f\text{ is constant on }(a,b).",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find }c\text{ for }f(x)=x^2+1\text{ on }[-1,2].",
        "hint_md": r"Compute secant slope then solve $f'(c)=2c$.",
        "ans_steps_latex": [
            r"f(2)=5,\ f(-1)=2\Rightarrow \frac{f(2)-f(-1)}{2-(-1)}=\frac{3}{3}=1",
            r"f'(x)=2x",
            r"2c=1\Rightarrow c=\frac{1}{2}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Check MVT conditions for }f(x)=\frac{x^2-1}{x-1}\text{ on }[0,2].",
        "hint_md": r"Simplify first, but be careful at $x=1$.",
        "ans_steps_latex": [
            r"\frac{x^2-1}{x-1}=\frac{(x-1)(x+1)}{x-1}=x+1\quad (\text{for }x\ne 1)",
            r"\text{At }x=1,\ f(x)\text{ is undefined, so it is not continuous on }[0,2].",
            r"\text{Therefore MVT does not apply on }[0,2].",
        ],
    })

    return qs


# ------------------------------------------------------------
# Main render (FIX LEARN LATEX RENDERING ONLY; PRACTICE UNCHANGED)
# ------------------------------------------------------------
def render():
    st.header("Subtopic 4.10: The Mean Value Theorem")
    st.caption("Source: Al Diwan Advanced Stream Mathematics – G12 ADV Lesson 3.10 The Mean Value Theorem")

    tabs = st.tabs(["Learn", "Practice"])

    # ---------------------- LEARN (UPDATED: force KaTeX via $...$ and st.latex) ----------------------
    with tabs[0]:
        st.markdown("### Lesson Objectives")
        st.markdown(
            r"""
**4.10.1 Explain and apply the Rolle’s Theorem.**  
- Find the value of $c$ that satisfies the conditions of the theorem  

**4.10.2 Explain and apply Mean Value Theorem.**  
- Find the value of $c$ that satisfies the conditions of the theorem  

**4.10.3 Use the Intermediate Value Theorem and a subsequent theorem from Rolle’s to determine the number of zeros of a given function**  

**4.10.4 Realize that if two non-identical functions have the same derivative on an open interval $I$ then they differ by a constant on the same interval $I$**
"""
        )

        _tip_box(
            "Teacher tips (high impact)",
            [
                r"Students must always check conditions first: continuity on $[a,b]$, differentiability on $(a,b)$.",
                r"Never accept $c=a$ or $c=b$. The point must satisfy $c\in(a,b)$.",
                r"For zero-count problems: IVT guarantees existence; the Rolle consequence limits how many zeros are possible.",
            ],
            kind="info",
        )

        st.markdown("---")
        st.subheader("4.10.1 Rolle’s Theorem")

        _md(
            r"""
**Key idea:** If a function is smooth on an interval and begins and ends at the same height, it must have at least one point in between with a horizontal tangent.

You will do two things:
1) Apply the theorem (check the conditions)  
2) Find the value(s) of $c$ such that $f'(c)=0$
"""
        )

        _md(
            r"""
Before opening the step-by-step board, make sure you can answer these quickly:

- Are you given an interval $[a,b]$?  
- Can you verify $f(a)=f(b)$ using substitution?  
- Can you differentiate $f(x)$ correctly?  
- After solving $f'(c)=0$, can you confirm $c\in(a,b)$?
"""
        )

        render_simulation(_sim_objective_4101_rolle_statement(), "Mini Blackboard — Rolle’s Theorem")

        st.markdown("#### Example 1")
        _md("**Problem:**")
        _latex(r"f(x)=x^2-4x+3 \quad \text{on } [1,3].")
        _md("What you should produce (in your notebook):")
        _md(
            r"""
- Evaluate $f(1)$ and $f(3)$ clearly  
- Write $f'(x)$  
- Solve $f'(c)=0$  
- State the final $c$ value and confirm it lies strictly inside $(1,3)$
"""
        )
        render_simulation(_sim_objective_4101_find_c_poly(), "Mini Blackboard — Find $c$ (polynomial)")

        st.markdown("#### Example 2")
        _md("**Problem:**")
        _latex(r"f(x)=\sin x \quad \text{on } [0,\pi].")
        _md("What you should produce:")
        _md(
            r"""
- Verify $\sin(0)=\sin(\pi)$  
- Differentiate to get $f'(x)=\cos x$  
- Solve $\cos(c)=0$ and keep only values inside $(0,\pi)$
"""
        )
        render_simulation(_sim_objective_4101_find_c_trig(), "Mini Blackboard — Find $c$ (trigonometric)")

        st.markdown("#### Rolle graph simulation (no sliders)")
        _md(
            r"""
This graph simulation shows the idea visually:

- Step 1: the curve  
- Step 2: the endpoints $(a,f(a))$ and $(b,f(b))$  
- Step 3: a horizontal tangent at the guaranteed interior point $c$
"""
        )

        # Widget options cannot render KaTeX, so keep labels text-only and render the chosen math below.
        rolle_choice = st.selectbox(
            "Choose a Rolle example for the graph",
            ["Example A (polynomial)", "Example B (trigonometric)"],
            index=0,
            key="rolle_graph_choice",
        )

        if rolle_choice.startswith("Example A"):
            f_r = lambda x: x**2 - 4 * x + 3
            a_r, b_r = 1.0, 3.0
            c_r = 2.0
            _latex(r"f(x)=x^2-4x+3 \quad \text{on } [1,3]")
        else:
            f_r = lambda x: np.sin(x)
            a_r, b_r = 0.0, float(np.pi)
            c_r = float(np.pi / 2)
            _latex(r"f(x)=\sin x \quad \text{on } [0,\pi]")

        step_key = "rolle_graph_step"
        if step_key not in st.session_state:
            st.session_state[step_key] = 0

        colA, colB, colC = st.columns([1, 1, 1])
        with colA:
            if st.button("Next", key="rolle_next"):
                st.session_state[step_key] = min(2, st.session_state[step_key] + 1)
        with colB:
            if st.button("Back", key="rolle_back"):
                st.session_state[step_key] = max(0, st.session_state[step_key] - 1)
        with colC:
            if st.button("Reset", key="rolle_reset"):
                st.session_state[step_key] = 0

        fig = _plot_rolle_steps(f_r, a_r, b_r, c_r, st.session_state[step_key])
        _small_plot(fig)
        _latex(r"f(a)=f(b)\ \Rightarrow\ \exists\,c\in(a,b)\ \text{such that}\ f'(c)=0")

        st.markdown("---")
        st.subheader("4.10.2 Mean Value Theorem (MVT)")

        _md(
            r"""
**Key idea:** There is at least one point inside $(a,b)$ where the tangent slope equals the average slope from $a$ to $b$.

You will do two things:
1) Apply the theorem (check the conditions)  
2) Find the value(s) of $c$ such that
"""
        )
        _latex(r"f'(c)=\frac{f(b)-f(a)}{b-a}")

        _md(
            r"""
Before opening the step-by-step board, make sure you know exactly what each symbol means:

- $f(b)-f(a)$ is the vertical change (rise)  
- $b-a$ is the horizontal change (run)  
- $\dfrac{f(b)-f(a)}{b-a}$ is the secant slope  
- $f'(c)$ is the tangent slope at an interior point $c$
"""
        )

        render_simulation(_sim_objective_4102_mvt_statement(), "Mini Blackboard — Mean Value Theorem")

        st.markdown("#### Example")
        _md("**Problem:**")
        _latex(r"f(x)=x^2 \quad \text{on } [1,3].")
        _md("What you should produce:")
        _md(
            r"""
- Compute $f(1)$ and $f(3)$  
- Compute the secant slope $\dfrac{f(3)-f(1)}{3-1}$  
- Differentiate to get $f'(x)$  
- Solve $f'(c)=$ (secant slope) and confirm $c\in(1,3)$
"""
        )
        render_simulation(_sim_objective_4102_find_c_example(), "Mini Blackboard — Find $c$ using MVT")

        st.markdown("#### MVT graph simulation (no sliders)")
        _md(
            r"""
This graph simulation shows:

- Step 1: the curve $y=f(x)$  
- Step 2: the secant line through $(a,f(a))$ and $(b,f(b))$  
- Step 3: a tangent line at an interior point $c$ with the same slope
"""
        )

        # Widgets cannot render KaTeX -> use text labels + render math underneath
        f_choice = st.selectbox(
            "Choose a function",
            ["Function A (quadratic)", "Function B (cubic)", "Function C (sine)", "Function D (exponential)"],
            index=0,
            key="mvt_func_choice_v2",
        )
        if f_choice.startswith("Function A"):
            f_m, fp_m, fname_latex = _get_function("f(x)=x^2")
        elif f_choice.startswith("Function B"):
            f_m, fp_m, fname_latex = _get_function("f(x)=x^3-x")
        elif f_choice.startswith("Function C"):
            f_m, fp_m, fname_latex = _get_function(r"f(x)=\sin x")
        else:
            f_m, fp_m, fname_latex = _get_function(r"f(x)=e^x")
        _latex(fname_latex)

        interval_choice = st.selectbox(
            "Choose an interval",
            ["Interval 1", "Interval 2", "Interval 3", "Interval 4"],
            index=0,
            key="mvt_interval_choice",
        )
        if interval_choice == "Interval 1":
            a_m, b_m = (-1.0, 2.0)
            _latex(r"[a,b]=[-1,2]")
        elif interval_choice == "Interval 2":
            a_m, b_m = (0.0, 2.0)
            _latex(r"[a,b]=[0,2]")
        elif interval_choice == "Interval 3":
            a_m, b_m = (1.0, 3.0)
            _latex(r"[a,b]=[1,3]")
        else:
            a_m, b_m = (-2.0, 1.0)
            _latex(r"[a,b]=[-2,1]")

        step_key2 = "mvt_graph_step"
        if step_key2 not in st.session_state:
            st.session_state[step_key2] = 0

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Next", key="mvt_next"):
                st.session_state[step_key2] = min(2, st.session_state[step_key2] + 1)
        with col2:
            if st.button("Back", key="mvt_back"):
                st.session_state[step_key2] = max(0, st.session_state[step_key2] - 1)
        with col3:
            if st.button("Reset", key="mvt_reset"):
                st.session_state[step_key2] = 0

        fig, m, c = _plot_mvt_steps(f_m, fp_m, a_m, b_m, st.session_state[step_key2])
        _small_plot(fig)

        _latex(r"m=\frac{f(b)-f(a)}{b-a}=" + f"{m:.6f}")
        _latex(r"c\in(a,b)\approx " + f"{c:.6f}")
        _latex(r"f'(c)\approx " + f"{float(fp_m(c)):.6f}")

        st.markdown("---")
        st.subheader("4.10.3 Zeros of a function using IVT + a theorem from Rolle’s")

        _md(
            r"""
This objective uses two ideas together:

1) Intermediate Value Theorem (IVT)  
If $f$ is continuous and $f(a)$ and $f(b)$ have opposite signs, then a zero exists between them.

2) A consequence from Rolle’s Theorem  
If $f$ has two distinct zeros, then $f'$ must be zero somewhere between them.

This lets you:
- Guarantee zeros exist (IVT)  
- Limit how many zeros are possible (Rolle consequence)
"""
        )

        _md(
            r"""
Before opening the step-by-step board, keep this structure in mind:

- “At least $n$ zeros”: you must show $n$ different sign-change intervals  
- “At most $n$ zeros”: you must use the Rolle consequence + the number of critical points of $f'$
"""
        )

        render_simulation(_sim_objective_4103_ivt_and_zeros(), "Mini Blackboard — IVT + Rolle consequence")

        st.markdown("#### Example (determine the number of zeros)")
        _md("**Problem:**")
        _latex(r"f(x)=x^3-3x+1")
        _md("What you should produce:")
        _md(
            r"""
- Compute $f'(x)$ and identify where $f'(x)=0$  
- Use sign checks to show zeros exist in multiple intervals  
- Use the Rolle consequence to explain why the function cannot have more zeros than your conclusion
"""
        )
        render_simulation(_sim_objective_4103_three_zeros_example(), "Mini Blackboard — Exactly 3 zeros example")

        st.markdown("#### Graph simulation for zeros (no sliders)")
        _md(
            r"""
- Step 1: the curve  
- Step 2: show the sign-check interval boundaries  
- Step 3: show the turning points at $x=-1$ and $x=1$ (from $f'(x)=0$)
"""
        )

        step_key3 = "zeros_graph_step"
        if step_key3 not in st.session_state:
            st.session_state[step_key3] = 0

        cA, cB, cC = st.columns([1, 1, 1])
        with cA:
            if st.button("Next", key="zeros_next"):
                st.session_state[step_key3] = min(2, st.session_state[step_key3] + 1)
        with cB:
            if st.button("Back", key="zeros_back"):
                st.session_state[step_key3] = max(0, st.session_state[step_key3] - 1)
        with cC:
            if st.button("Reset", key="zeros_reset"):
                st.session_state[step_key3] = 0

        figz = _plot_zero_count_steps(st.session_state[step_key3])
        _small_plot(figz)
        _latex(r"\text{IVT identifies sign-change intervals; the Rolle consequence limits the maximum number of roots.}")

        st.markdown("---")
        st.subheader("4.10.4 Same derivative $\Rightarrow$ differ by a constant on an open interval $I$")

        _md(
            r"""
If two non-identical functions have the same derivative on an open interval $I$, then they differ by a constant on that same interval.

In symbols:
"""
        )
        _latex(r"f'(x)=g'(x)\ \text{on } I \quad\Rightarrow\quad f(x)=g(x)+C \ \text{on } I")

        _md(
            r"""
Before opening the step-by-step board, focus on the one key move:

Define a new function:
"""
        )
        _latex(r"h(x)=f(x)-g(x)")
        _md(
            r"""
If $f'(x)=g'(x)$, then $h'(x)=0$.  
A function with derivative $0$ on an interval must be constant on that interval.
"""
        )

        render_simulation(_sim_objective_4104_same_derivative_constant(), "Mini Blackboard — Why the difference is constant")

        st.markdown("#### Example (find the constant)")
        _md("**Problem:**")
        _latex(r"f'(x)=2x,\quad f(0)=5")
        _md("What you should produce:")
        _md(
            r"""
- Recognise the basic function whose derivative is $2x$, which is $x^2$  
- Add a constant $C$  
- Use the condition $f(0)=5$ to identify $C$
"""
        )
        render_simulation(_sim_objective_4104_find_function_example(), "Mini Blackboard — Find the function from $f'$ and one point")

        _tip_box(
            "Common mistakes to avoid",
            [
                r"Writing $c=a$ or $c=b$. Always keep $c\in(a,b)$.",
                r"Using MVT or Rolle when the function is not differentiable inside the interval (e.g., $|x|$ at $0$).",
                r"For zero-count problems, claiming “exactly $n$” without both: (i) IVT evidence for at least $n$, and (ii) Rolle consequence to cap the maximum.",
            ],
            kind="warning",
        )

    # ---------------------- PRACTICE (UNCHANGED) ----------------------
    with tabs[1]:
        st.subheader("Practice (15+ questions)")
        st.markdown("Each question includes **Hint** and **Show Answer** (full steps at once).")

        questions = _practice_questions()

        for i, q in enumerate(questions, start=1):
            st.markdown("---")
            st.markdown(f"### Question {i}")
            _latex(q["q_latex"])

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Hint", key=f"mvt410_hint_{i}"):
                    st.info("")
                    _md(q["hint_md"])
            with c2:
                if st.button("Show Answer", key=f"mvt410_ans_{i}"):
                    st.success("Solution (step-by-step):")
                    for step in q["ans_steps_latex"]:
                        _latex(step)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
