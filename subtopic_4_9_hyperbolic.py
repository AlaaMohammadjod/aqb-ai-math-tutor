# subtopic_4_9_hyperbolic.py
import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# ------------------------------------------------------------
# Helpers (consistent with Subtopic 4.8 style)
# ------------------------------------------------------------
def _latex_block(expr: str):
    """Render a single LaTeX display block (humanised)."""
    st.latex(expr)


def _md_math(text: str):
    """
    Markdown with KaTeX blocks.
    Use $...$ for inline and $$...$$ for display.
    """
    st.markdown(text)


def _small_graph(fig):
    """Standardised smaller graph sizing for Streamlit."""
    st.pyplot(fig, clear_figure=True, use_container_width=False)


def _tip_box(title: str, bullets: list[str], kind: str = "info"):
    msg = "**" + title + "**\n\n" + "\n".join([f"- {b}" for b in bullets])
    if kind == "success":
        st.success(msg)
    elif kind == "warning":
        st.warning(msg)
    else:
        st.info(msg)


# ------------------------------------------------------------
# Graph utilities
# ------------------------------------------------------------
def _hyperbolic_values(which: str, x: np.ndarray):
    if which == "sinh":
        return np.sinh(x)
    if which == "cosh":
        return np.cosh(x)
    if which == "tanh":
        return np.tanh(x)
    if which == "sech":
        return 1 / np.cosh(x)
    if which == "csch":
        # avoid division by zero
        y = np.sinh(x)
        y = np.where(np.abs(y) < 1e-12, np.nan, y)
        return 1 / y
    if which == "coth":
        y = np.tanh(x)
        y = np.where(np.abs(y) < 1e-12, np.nan, y)
        return 1 / y
    return np.sinh(x)


def _plot_hyperbolic(which: str, show_derivative: bool, x_min: float, x_max: float):
    x = np.linspace(x_min, x_max, 800)
    y = _hyperbolic_values(which, x)

    fig = plt.figure(figsize=(6.6, 3.8))
    ax = fig.add_subplot(111)

    label_map = {
        "sinh": r"$y=\sinh(x)$",
        "cosh": r"$y=\cosh(x)$",
        "tanh": r"$y=\tanh(x)$",
        "sech": r"$y=\operatorname{sech}(x)$",
        "csch": r"$y=\operatorname{csch}(x)$",
        "coth": r"$y=\operatorname{coth}(x)$",
    }
    ax.plot(x, y, label=label_map.get(which, r"$y$"))

    if show_derivative:
        if which == "sinh":
            yp = np.cosh(x)
            ax.plot(x, yp, label=r"$y'=\cosh(x)$")
        elif which == "cosh":
            yp = np.sinh(x)
            ax.plot(x, yp, label=r"$y'=\sinh(x)$")
        elif which == "tanh":
            yp = (1 / np.cosh(x)) ** 2
            ax.plot(x, yp, label=r"$y'=\operatorname{sech}^2(x)$")
        elif which == "sech":
            yp = -(1 / np.cosh(x)) * np.tanh(x)
            ax.plot(x, yp, label=r"$y'=-\operatorname{sech}(x)\tanh(x)$")
        elif which == "csch":
            y_sinh = np.sinh(x)
            y_sinh = np.where(np.abs(y_sinh) < 1e-12, np.nan, y_sinh)
            yp = -(1 / y_sinh) * (1 / np.tanh(x))  # -csch*coth
            ax.plot(x, yp, label=r"$y'=-\operatorname{csch}(x)\operatorname{coth}(x)$")
        elif which == "coth":
            y_sinh = np.sinh(x)
            y_sinh = np.where(np.abs(y_sinh) < 1e-12, np.nan, y_sinh)
            yp = -(1 / y_sinh) ** 2  # -csch^2
            ax.plot(x, yp, label=r"$y'=-\operatorname{csch}^2(x)$")

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    ax.set_title("Hyperbolic function (and optional derivative)")
    ax.legend()
    return fig


def _plot_hyperbola_param(t: float):
    """Show the unit hyperbola x^2 - y^2 = 1 and the point (cosh t, sinh t)."""
    x = np.linspace(1.0, 3.2, 500)
    y = np.sqrt(np.clip(x * x - 1, 0, None))

    x0 = math.cosh(t)
    y0 = math.sinh(t)

    fig = plt.figure(figsize=(6.6, 3.8))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label=r"$x^2-y^2=1$ (upper right branch)")
    ax.plot(x, -y, label=r"$x^2-y^2=1$ (lower right branch)")
    ax.scatter([x0], [y0], s=60)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Hyperbola parameterisation with cosh and sinh")
    ax.legend()
    return fig, x0, y0


def _plot_catenary(a: float):
    x = np.linspace(-6, 6, 700)
    y = a * np.cosh(x / a)

    fig = plt.figure(figsize=(6.6, 3.8))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label=r"$y=a\cosh\!\left(\frac{x}{a}\right)$")
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    ax.set_title("Catenary (hanging cable) model")
    ax.legend()
    return fig


# ------------------------------------------------------------
# Blackboard simulations (step-by-step)
# ------------------------------------------------------------
def _sim_definitions_steps():
    return [
        BoardStep(
            latex_line=r"\sinh x=\frac{e^x-e^{-x}}{2},\qquad \cosh x=\frac{e^x+e^{-x}}{2}",
            teacher_explain_md=r"""
**Key idea:** Hyperbolic functions are **built from exponentials**.

**Student task:** Memorise these two definitions first.  
Everything else (identities and derivatives) follows quickly.
""",
        ),
        BoardStep(
            latex_line=r"\tanh x=\frac{\sinh x}{\cosh x},\qquad \operatorname{sech}x=\frac{1}{\cosh x}",
            teacher_explain_md=r"""
Define the remaining functions using ratios/reciprocals.

**Student note:** \(\tanh x\) behaves like a “bounded” S-curve (approaches \(\pm1\)).
""",
        ),
        BoardStep(
            latex_line=r"\operatorname{csch}x=\frac{1}{\sinh x},\qquad \operatorname{coth}x=\frac{\cosh x}{\sinh x}",
            teacher_explain_md=r"""
These are less common but still appear in exams.

**Domain warning:** \(\sinh x=0\) at \(x=0\), so \(\operatorname{csch}x\) and \(\operatorname{coth}x\) are undefined at \(x=0\).
""",
        ),
    ]


def _sim_identity_steps():
    return [
        BoardStep(
            latex_line=r"\text{Prove: }\cosh^2x-\sinh^2x=1",
            teacher_explain_md=r"""
**Exam-style task:** Prove the hyperbolic identity using the exponential definitions.

Strategy:
1) Substitute definitions of \(\cosh x\) and \(\sinh x\).  
2) Expand squares carefully.  
3) Subtract and simplify.
""",
        ),
        BoardStep(
            latex_line=r"\cosh^2x-\sinh^2x=\left(\frac{e^x+e^{-x}}{2}\right)^2-\left(\frac{e^x-e^{-x}}{2}\right)^2",
            teacher_explain_md=r"Substitute the definitions.",
        ),
        BoardStep(
            latex_line=r"=\frac{(e^x+e^{-x})^2-(e^x-e^{-x})^2}{4}",
            teacher_explain_md=r"Put over a common denominator \(4\).",
        ),
        BoardStep(
            latex_line=r"=\frac{\left(e^{2x}+2+e^{-2x}\right)-\left(e^{2x}-2+e^{-2x}\right)}{4}",
            teacher_explain_md=r"Expand both squares.",
        ),
        BoardStep(
            latex_line=r"=\frac{4}{4}=1",
            teacher_explain_md=r"Cancel terms: the exponentials vanish and only the constants remain.",
        ),
    ]


def _sim_derivative_sinh_steps():
    return [
        BoardStep(
            latex_line=r"y=\sinh x=\frac{e^x-e^{-x}}{2}",
            teacher_explain_md=r"""
**Exam-style task:** Derive \(\dfrac{d}{dx}(\sinh x)\) from the definition.

This is a quick “definition → differentiate” proof.
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{1}{2}\left(\frac{d}{dx}(e^x)-\frac{d}{dx}(e^{-x})\right)",
            teacher_explain_md=r"Differentiate term-by-term.",
        ),
        BoardStep(
            latex_line=r"y'=\frac{1}{2}\left(e^x-(-e^{-x})\right)=\frac{e^x+e^{-x}}{2}",
            teacher_explain_md=r"""
Chain rule: \(\dfrac{d}{dx}(e^{-x})=e^{-x}\cdot(-1)=-e^{-x}\).

So the minus becomes a plus.
""",
        ),
        BoardStep(
            latex_line=r"y'=\cosh x",
            teacher_explain_md=r"Recognise the definition of \(\cosh x\).",
        ),
    ]


def _sim_derivative_tanh_steps():
    return [
        BoardStep(
            latex_line=r"y=\tanh x=\frac{\sinh x}{\cosh x}",
            teacher_explain_md=r"""
**Exam-style task:** Show that \(\dfrac{d}{dx}(\tanh x)=\operatorname{sech}^2x\).

We use the quotient rule plus the identity:
$$
\cosh^2x-\sinh^2x=1.
$$
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{(\cosh x)(\cosh x)-(\sinh x)(\sinh x)}{\cosh^2x}",
            teacher_explain_md=r"""
Quotient rule:
$$
\left(\frac{u}{v}\right)'=\frac{u'v-uv'}{v^2},
$$
with \(u=\sinh x\), \(u'=\cosh x\), \(v=\cosh x\), \(v'=\sinh x\).
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{\cosh^2x-\sinh^2x}{\cosh^2x}=\frac{1}{\cosh^2x}",
            teacher_explain_md=r"Use \(\cosh^2x-\sinh^2x=1\).",
        ),
        BoardStep(
            latex_line=r"y'=\operatorname{sech}^2x",
            teacher_explain_md=r"Since \(\operatorname{sech}x=\dfrac{1}{\cosh x}\).",
        ),
    ]


def _sim_example_9_1_steps():
    return [
        BoardStep(
            latex_line=r"\text{Differentiate: } f(x)=\sinh^2(3x)",
            teacher_explain_md=r"""
**Exam-style question:** Differentiate \(f(x)=\sinh^2(3x)\).

Expected approach:
- Rewrite as \([\sinh(3x)]^2\)
- Outer power rule, then chain rule.
""",
        ),
        BoardStep(
            latex_line=r"f(x)=[\sinh(3x)]^2",
            teacher_explain_md=r"Rewrite to make the outer function clear.",
        ),
        BoardStep(
            latex_line=r"f'(x)=2\sinh(3x)\cdot \frac{d}{dx}(\sinh(3x))",
            teacher_explain_md=r"Outer power rule: \(\dfrac{d}{dx}(g^2)=2g\cdot g'\).",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(\sinh(3x))=\cosh(3x)\cdot 3",
            teacher_explain_md=r"Chain rule: \(\dfrac{d}{dx}(\sinh u)=\cosh u\cdot u'\) with \(u=3x\).",
        ),
        BoardStep(
            latex_line=r"f'(x)=2\sinh(3x)\cdot (3\cosh(3x))=6\sinh(3x)\cosh(3x)",
            teacher_explain_md=r"Multiply constants and simplify.",
        ),
    ]


def _sim_inverse_def_steps():
    return [
        BoardStep(
            latex_line=r"y=\sinh^{-1}(x)\quad \Longleftrightarrow\quad \sinh y=x",
            teacher_explain_md=r"""
**Definition:** Inverse hyperbolic sine is defined by:
$$
y=\sinh^{-1}(x)\iff \sinh y=x.
$$

**Domain note:** \(\sinh x\) is one-to-one on \(\mathbb{R}\), so this inverse exists for all real \(x\).
""",
        ),
        BoardStep(
            latex_line=r"\text{Differentiate: }\sinh y=x",
            teacher_explain_md=r"""
**Exam-style task:** Find \(\dfrac{d}{dx}(\sinh^{-1}x)\) by implicit differentiation.
""",
        ),
        BoardStep(
            latex_line=r"\cosh(y)\,y'=1",
            teacher_explain_md=r"""
Differentiate both sides:
$$
\frac{d}{dx}(\sinh y)=\cosh(y)\,y'
$$
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{1}{\cosh(y)}",
            teacher_explain_md=r"Isolate \(y'\).",
        ),
        BoardStep(
            latex_line=r"\cosh^2(y)-\sinh^2(y)=1\Rightarrow \cosh(y)=\sqrt{1+\sinh^2(y)}=\sqrt{1+x^2}",
            teacher_explain_md=r"""
Convert to \(x\) using the identity:
$$
\cosh^2y-\sinh^2y=1.
$$
Since \(\sinh y=x\), we get \(\cosh y=\sqrt{1+x^2}\) (always positive).
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}\left(\sinh^{-1}x\right)=\frac{1}{\sqrt{1+x^2}}",
            teacher_explain_md=r"Final derivative rule.",
        ),
    ]


def _sim_example_9_2_steps():
    return [
        BoardStep(
            latex_line=r"\text{Find an explicit formula for }\sinh^{-1}(x)",
            teacher_explain_md=r"""
**Exam-style (Example 9.2 idea):** Express \(\sinh^{-1}(x)\) using logarithms.

Goal:
$$
\sinh^{-1}(x)=\ln(\,\cdots\,)
$$
""",
        ),
        BoardStep(
            latex_line=r"y=\sinh^{-1}(x)\iff \sinh y=x",
            teacher_explain_md=r"Start from the inverse definition.",
        ),
        BoardStep(
            latex_line=r"x=\sinh y=\frac{e^y-e^{-y}}{2}",
            teacher_explain_md=r"Use the definition of \(\sinh y\).",
        ),
        BoardStep(
            latex_line=r"2x=e^y-e^{-y}\quad \Rightarrow\quad 2xe^y=e^{2y}-1",
            teacher_explain_md=r"Multiply both sides by \(e^y\) to eliminate \(e^{-y}\).",
        ),
        BoardStep(
            latex_line=r"e^{2y}-2xe^y-1=0",
            teacher_explain_md=r"Treat this as a quadratic in \(e^y\).",
        ),
        BoardStep(
            latex_line=r"e^y=x+\sqrt{x^2+1}",
            teacher_explain_md=r"""
Solve the quadratic:
$$
(e^y)^2-2x(e^y)-1=0
$$
Take the positive root because \(e^y>0\).
""",
        ),
        BoardStep(
            latex_line=r"y=\ln\!\left(x+\sqrt{x^2+1}\right)",
            teacher_explain_md=r"""
Therefore:
$$
\sinh^{-1}(x)=\ln\!\left(x+\sqrt{x^2+1}\right).
$$
""",
        ),
    ]


# ------------------------------------------------------------
# Practice bank (15+)
# ------------------------------------------------------------
def _practice_questions():
    qs = []

    qs.append({
        "q_latex": r"\text{Write }\sinh x\text{ and }\cosh x\text{ in terms of exponentials.}",
        "hint_md": r"Use the definitions: $$\sinh x=\frac{e^x-e^{-x}}{2},\quad \cosh x=\frac{e^x+e^{-x}}{2}.$$",
        "ans_steps_latex": [
            r"\sinh x=\frac{e^x-e^{-x}}{2}",
            r"\cosh x=\frac{e^x+e^{-x}}{2}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Prove the identity } \cosh^2x-\sinh^2x=1.",
        "hint_md": r"Substitute the exponential definitions and expand: $$\left(\frac{e^x+e^{-x}}{2}\right)^2-\left(\frac{e^x-e^{-x}}{2}\right)^2.$$",
        "ans_steps_latex": [
            r"\cosh^2x-\sinh^2x=\left(\frac{e^x+e^{-x}}{2}\right)^2-\left(\frac{e^x-e^{-x}}{2}\right)^2",
            r"=\frac{(e^x+e^{-x})^2-(e^x-e^{-x})^2}{4}",
            r"=\frac{(e^{2x}+2+e^{-2x})-(e^{2x}-2+e^{-2x})}{4}",
            r"=\frac{4}{4}=1",
        ],
    })

    qs.append({
        "q_latex": r"\text{Evaluate: }\sinh(0),\ \cosh(0),\ \tanh(0).",
        "hint_md": r"Use definitions or known values: $$e^0=1.$$",
        "ans_steps_latex": [
            r"\sinh(0)=\frac{1-1}{2}=0",
            r"\cosh(0)=\frac{1+1}{2}=1",
            r"\tanh(0)=\frac{\sinh(0)}{\cosh(0)}=0",
        ],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\sinh x.",
        "hint_md": r"Use the rule: $$\frac{d}{dx}(\sinh x)=\cosh x.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\sinh x)=\cosh x"],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\cosh x.",
        "hint_md": r"Use the rule: $$\frac{d}{dx}(\cosh x)=\sinh x.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\cosh x)=\sinh x"],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\tanh x.",
        "hint_md": r"Use the rule: $$\frac{d}{dx}(\tanh x)=\operatorname{sech}^2x.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\tanh x)=\operatorname{sech}^2x"],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\operatorname{sech}x.",
        "hint_md": r"Use the rule: $$\frac{d}{dx}(\operatorname{sech}x)=-\operatorname{sech}x\,\tanh x.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\operatorname{sech}x)=-\operatorname{sech}x\,\tanh x"],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\operatorname{coth}x.",
        "hint_md": r"Use the rule: $$\frac{d}{dx}(\operatorname{coth}x)=-\operatorname{csch}^2x.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\operatorname{coth}x)=-\operatorname{csch}^2x"],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\operatorname{csch}x.",
        "hint_md": r"Use the rule: $$\frac{d}{dx}(\operatorname{csch}x)=-\operatorname{csch}x\,\operatorname{coth}x.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\operatorname{csch}x)=-\operatorname{csch}x\,\operatorname{coth}x"],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } f(x)=\sinh^2(3x).",
        "hint_md": r"Write it as $$[\sinh(3x)]^2$$ then use power rule + chain rule.",
        "ans_steps_latex": [
            r"f(x)=[\sinh(3x)]^2",
            r"f'(x)=2\sinh(3x)\cdot \frac{d}{dx}(\sinh(3x))",
            r"\frac{d}{dx}(\sinh(3x))=\cosh(3x)\cdot 3",
            r"f'(x)=2\sinh(3x)\cdot 3\cosh(3x)=6\sinh(3x)\cosh(3x)",
        ],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\cosh(5x^2).",
        "hint_md": r"Chain rule: $$\frac{d}{dx}(\cosh u)=\sinh u\cdot u',$$ with \(u=5x^2\).",
        "ans_steps_latex": [
            r"u=5x^2\Rightarrow u'=10x",
            r"y'=\sinh(5x^2)\cdot 10x",
            r"y'=10x\,\sinh(5x^2)",
        ],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\tanh(\sqrt{x}).",
        "hint_md": r"Use $$\frac{d}{dx}(\tanh u)=\operatorname{sech}^2(u)\,u'$$ and \(u=\sqrt{x}\).",
        "ans_steps_latex": [
            r"u=\sqrt{x}\Rightarrow u'=\frac{1}{2\sqrt{x}}",
            r"y'=\operatorname{sech}^2(\sqrt{x})\cdot \frac{1}{2\sqrt{x}}",
            r"y'=\frac{\operatorname{sech}^2(\sqrt{x})}{2\sqrt{x}}",
        ],
    })

    qs.append({
        "q_latex": r"\text{Simplify: } 1-\tanh^2x.",
        "hint_md": r"Use the identity: $$1-\tanh^2x=\operatorname{sech}^2x.$$",
        "ans_steps_latex": [r"1-\tanh^2x=\operatorname{sech}^2x"],
    })

    qs.append({
        "q_latex": r"\text{Find } \displaystyle\int \operatorname{sech}^2x\,dx.",
        "hint_md": r"Recognise a derivative: $$\frac{d}{dx}(\tanh x)=\operatorname{sech}^2x.$$",
        "ans_steps_latex": [r"\int \operatorname{sech}^2x\,dx=\tanh x+C"],
    })

    qs.append({
        "q_latex": r"\text{Show that }\cosh(-x)=\cosh x\text{ and }\sinh(-x)=-\sinh x.",
        "hint_md": r"Use exponential definitions and replace \(x\) by \(-x\).",
        "ans_steps_latex": [
            r"\cosh(-x)=\frac{e^{-x}+e^{x}}{2}=\frac{e^{x}+e^{-x}}{2}=\cosh x",
            r"\sinh(-x)=\frac{e^{-x}-e^{x}}{2}=-\frac{e^{x}-e^{-x}}{2}=-\sinh x",
        ],
    })

    qs.append({
        "q_latex": r"\text{Find } \displaystyle\lim_{x\to\infty}\tanh x.",
        "hint_md": r"Rewrite: $$\tanh x=\frac{e^x-e^{-x}}{e^x+e^{-x}}=\frac{1-e^{-2x}}{1+e^{-2x}}.$$",
        "ans_steps_latex": [
            r"\tanh x=\frac{1-e^{-2x}}{1+e^{-2x}}",
            r"\lim_{x\to\infty}\tanh x=\frac{1-0}{1+0}=1",
        ],
    })

    qs.append({
        "q_latex": r"\text{Differentiate: } y=\sinh^{-1}(x).",
        "hint_md": r"Use: $$\frac{d}{dx}(\sinh^{-1}x)=\frac{1}{\sqrt{1+x^2}}.$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\sinh^{-1}x)=\frac{1}{\sqrt{1+x^2}}"],
    })

    qs.append({
        "q_latex": r"\text{Find an explicit formula for } \sinh^{-1}(x).",
        "hint_md": r"Start from \(x=\sinh y=\frac{e^y-e^{-y}}{2}\) and solve for \(y\).",
        "ans_steps_latex": [
            r"y=\sinh^{-1}(x)\iff x=\frac{e^y-e^{-y}}{2}",
            r"2x=e^y-e^{-y}\Rightarrow 2xe^y=e^{2y}-1",
            r"e^{2y}-2xe^y-1=0",
            r"e^y=x+\sqrt{x^2+1}",
            r"y=\ln\!\left(x+\sqrt{x^2+1}\right)",
            r"\sinh^{-1}(x)=\ln\!\left(x+\sqrt{x^2+1}\right)",
        ],
    })

    qs.append({
        "q_latex": r"\text{Catenary model: } y=a\cosh\!\left(\frac{x}{a}\right). \ \text{Find } y'.",
        "hint_md": r"Chain rule: $$\frac{d}{dx}\big(\cosh u\big)=\sinh u\cdot u',$$ with \(u=\frac{x}{a}\).",
        "ans_steps_latex": [
            r"y=a\cosh\!\left(\frac{x}{a}\right)",
            r"u=\frac{x}{a}\Rightarrow u'=\frac{1}{a}",
            r"y'=a\cdot \sinh\!\left(\frac{x}{a}\right)\cdot \frac{1}{a}",
            r"y'=\sinh\!\left(\frac{x}{a}\right)",
        ],
    })

    return qs


# ------------------------------------------------------------
# Main render()
# ------------------------------------------------------------
def render():
    st.header("Subtopic 4.9: The Hyperbolic Functions")
    st.caption("Coverage aligned to Chapter 2 (Section 2.9 Hyperbolic Functions)")

    tabs = st.tabs(["Learn", "Practice"])

    # ---------------------- LEARN ----------------------
    with tabs[0]:
        st.markdown("### Learning goals")
        st.markdown(
            r"""
- Define the six hyperbolic functions using exponentials: $\sinh x$, $\cosh x$, $\tanh x$, $\operatorname{sech}x$, $\operatorname{csch}x$, $\operatorname{coth}x$.
- Use the fundamental identity: $$\cosh^2x-\sinh^2x=1.$$
- Differentiate hyperbolic functions and apply chain rule to composites.
- Connect $\cosh$ and $\sinh$ to the unit hyperbola and the catenary model.
- Understand inverse hyperbolic functions (existence, derivatives, and explicit formulas).
"""
        )

        _tip_box(
            "Teacher tips (high impact)",
            [
                r"Tell students: “Hyperbolic is like trig, but the key identity uses a **minus sign**: $\cosh^2x-\sinh^2x=1$.”",
                r"For derivatives: $\sinh$ and $\cosh$ behave like a swap: $(\sinh)'=\cosh$, $(\cosh)'=\sinh$.",
                r"Always check domains when inverses appear (e.g., $\cosh^{-1}x$ needs $x\ge 1$).",
            ],
            kind="info",
        )

        st.markdown("---")
        st.subheader("1) Definitions (built from exponentials)")
        st.markdown(
            r"""
**Exam-format prompt:** *State the definitions of $\sinh x$ and $\cosh x$, then define the remaining hyperbolic functions.*

**What you should be able to do:**
- Write each function exactly in terms of $e^x$ and $e^{-x}$ (or as ratios/reciprocals of $\sinh$ and $\cosh$).
"""
        )
        render_simulation(_sim_definitions_steps(), "Mini Blackboard — Definitions of hyperbolic functions")

        st.markdown("---")
        st.subheader("2) The fundamental identity (hyperbolic Pythagorean)")
        st.markdown(
            r"""
**Exam-format prompt:** *Prove the identity $$\cosh^2x-\sinh^2x=1$$ using exponential definitions.*

**What is expected:**
- Substitute definitions.
- Expand correctly.
- Simplify cleanly to get exactly $1$.
"""
        )
        render_simulation(_sim_identity_steps(), "Mini Blackboard — Prove the identity")

        st.markdown("---")
        st.subheader("3) Derivatives (from definitions + rules)")
        st.markdown(r"**Key derivative rules (must be memorised):**")
        st.latex(
            r"""
\begin{aligned}
\frac{d}{dx}(\sinh x)&=\cosh x\\
\frac{d}{dx}(\cosh x)&=\sinh x\\
\frac{d}{dx}(\tanh x)&=\operatorname{sech}^2x\\
\frac{d}{dx}(\operatorname{coth}x)&=-\operatorname{csch}^2x\\
\frac{d}{dx}(\operatorname{sech}x)&=-\operatorname{sech}x\,\tanh x\\
\frac{d}{dx}(\operatorname{csch}x)&=-\operatorname{csch}x\,\operatorname{coth}x
\end{aligned}
"""
        )

        st.markdown("### Derivation (sinh) — show you can prove one rule")
        render_simulation(_sim_derivative_sinh_steps(), "Mini Blackboard — Derive d/dx(sinh x)")

        st.markdown("### Derivation (tanh) — quotient rule + identity")
        render_simulation(_sim_derivative_tanh_steps(), "Mini Blackboard — Derive d/dx(tanh x)")

        st.markdown("---")
        st.subheader("4) Visual graphs (function + optional derivative)")
        st.markdown(
            r"""
**Student task:** Use the graph to explain key behaviour:
- Which functions are even/odd?
- Which have horizontal asymptotes?
- Where is the function undefined?
"""
        )

        c1, c2, c3 = st.columns([1.2, 1, 1])
        with c1:
            which = st.selectbox(
                "Choose a hyperbolic function",
                ["sinh", "cosh", "tanh", "sech", "csch", "coth"],
                index=0,
                key="hyp_plot_pick",
            )
        with c2:
            show_d = st.checkbox("Show derivative curve", value=True, key="hyp_plot_showd")
        with c3:
            x_span = st.selectbox("x-range", ["-3 to 3", "-5 to 5", "-8 to 8"], index=1, key="hyp_plot_span")

        x_min, x_max = (-5, 5)
        if x_span == "-3 to 3":
            x_min, x_max = (-3, 3)
        elif x_span == "-8 to 8":
            x_min, x_max = (-8, 8)

        _small_graph(_plot_hyperbolic(which, show_d, x_min, x_max))

        _tip_box(
            "Graph-reading checklist (students should say these aloud)",
            [
                r"$\cosh x$ is even and always $\ge 1$.",
                r"$\sinh x$ is odd and crosses the origin.",
                r"$\tanh x$ has horizontal asymptotes at $y=\pm 1$.",
                r"$\operatorname{csch}x$ and $\operatorname{coth}x$ are undefined at $x=0$.",
            ],
            kind="success",
        )

        st.markdown("---")
        st.subheader("5) Hyperbola connection: why cosh and sinh matter")
        st.markdown(
            r"""
**Core idea:** The identity
$$
\cosh^2t-\sinh^2t=1
$$
means the point
$$
(\cosh t,\ \sinh t)
$$
lies on the unit hyperbola $x^2-y^2=1$.

**Student task:** Move the slider and verify that $x_0^2-y_0^2=1$.
"""
        )
        t = st.slider("Choose parameter $t$", -2.0, 2.0, 1.0, 0.05, key="hyp_t_param")
        fig, x0, y0 = _plot_hyperbola_param(t)
        _small_graph(fig)
        st.latex(r"x_0=\cosh t=" + f"{x0:.4f}")
        st.latex(r"y_0=\sinh t=" + f"{y0:.4f}")
        st.latex(r"x_0^2-y_0^2=" + f"{(x0*x0 - y0*y0):.6f}")

        st.markdown("---")
        st.subheader("6) Chain rule example (from the chapter)")
        st.markdown(
            r"""
**Exam-format question:** Differentiate
$$
f(x)=\sinh^2(3x).
$$

**Expected work:**
- Outer power rule
- Chain rule on $\sinh(3x)$
"""
        )
        render_simulation(_sim_example_9_1_steps(), "Mini Blackboard — Example: differentiate sinh²(3x)")

        st.markdown("---")
        st.subheader("7) Catenary model (real-life application)")
        st.markdown(
            r"""
A hanging cable often forms a **catenary**:
$$
y=a\cosh\!\left(\frac{x}{a}\right).
$$

**Exam-format question:** *Find $y'$ and interpret the slope as $x$ changes.*
"""
        )
        a = st.slider("Choose parameter $a$", 0.5, 5.0, 2.0, 0.1, key="cat_a")
        _small_graph(_plot_catenary(a))
        st.latex(r"y=a\cosh\!\left(\frac{x}{a}\right)\quad\Rightarrow\quad y'=\sinh\!\left(\frac{x}{a}\right)")
        st.markdown(
            r"""
**Interpretation (student-friendly):**
- At $x=0$, slope is $y'(0)=\sinh(0)=0$ (lowest point is flat).
- As $|x|$ increases, $|\sinh(x/a)|$ increases quickly → the curve gets steeper.
"""
        )

        st.markdown("---")
        st.subheader("8) Inverse hyperbolic functions (definitions, derivatives, explicit formula)")
        st.markdown(
            r"""
From the graphs, $\sinh x$ and $\tanh x$ are one-to-one on $\mathbb{R}$, and $\cosh x$ is one-to-one on $x\ge 0$.

So we can define:
$$
y=\sinh^{-1}(x)\iff \sinh y=x,\qquad
y=\cosh^{-1}(x)\iff \cosh y=x\ (y\ge 0),\qquad
y=\tanh^{-1}(x)\iff \tanh y=x.
$$
"""
        )

        st.markdown("### Derivative of $\\sinh^{-1}(x)$ via implicit differentiation")
        render_simulation(_sim_inverse_def_steps(), "Mini Blackboard — Derive d/dx(sinh⁻¹ x)")

        st.markdown("### Explicit formula (log form)")
        render_simulation(_sim_example_9_2_steps(), "Mini Blackboard — Find a formula for sinh⁻¹(x)")

        st.markdown("### Summary: inverse hyperbolic derivative rules")
        st.latex(
            r"""
\begin{aligned}
\frac{d}{dx}\left(\sinh^{-1}x\right)&=\frac{1}{\sqrt{1+x^2}}\\
\frac{d}{dx}\left(\cosh^{-1}x\right)&=\frac{1}{\sqrt{x^2-1}}\qquad (x>1)\\
\frac{d}{dx}\left(\tanh^{-1}x\right)&=\frac{1}{1-x^2}\qquad (|x|<1)
\end{aligned}
"""
        )

        _tip_box(
            "Domain restrictions (non-negotiable in exams)",
            [
                r"$\cosh^{-1}x$ requires $x\ge 1$ (and $\sqrt{x^2-1}$ requires $|x|\ge 1$).",
                r"$\tanh^{-1}x$ requires $|x|<1$ because $\tanh x$ outputs values between $-1$ and $1$.",
                r"For log forms (like $\sinh^{-1}x=\ln(x+\sqrt{x^2+1})$), check the inside of $\ln$ is positive.",
            ],
            kind="warning",
        )

    # ---------------------- PRACTICE ----------------------
    with tabs[1]:
        st.subheader("Practice (15+ questions)")
        st.markdown(
            r"""
Click **Hint** if you get stuck. Click **Show Answer** to reveal the full solution (all steps at once).
"""
        )

        questions = _practice_questions()

        for i, q in enumerate(questions, start=1):
            st.markdown("---")
            st.markdown(f"### Question {i}")
            _latex_block(q["q_latex"])

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Hint", key=f"q49_hint_{i}"):
                    st.info("")
                    _md_math(q["hint_md"])
            with c2:
                if st.button("Show Answer", key=f"q49_ans_{i}"):
                    st.success("Solution (step-by-step):")
                    for step in q["ans_steps_latex"]:
                        _latex_block(step)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
