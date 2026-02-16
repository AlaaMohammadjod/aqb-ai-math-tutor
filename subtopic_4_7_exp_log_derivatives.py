# subtopic_4_7_exp_log_derivatives.py
import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


def _latex_block(expr: str):
    """Render a single LaTeX display block (humanised)."""
    st.latex(expr)


def _md_math(text: str):
    """
    Markdown with KaTeX blocks.
    Use $$ ... $$ for display math to avoid showing raw backslashes.
    """
    st.markdown(text)


def _small_graph(fig):
    """Standardised smaller graph sizing for Streamlit."""
    st.pyplot(fig, clear_figure=True, use_container_width=False)


def _plot_exp_base_a(a: float = 2.0):
    x = np.linspace(-2, 2, 400)
    y = a**x
    yp = (a**x) * math.log(a)

    fig = plt.figure(figsize=(6.2, 3.6))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label=r"$y=a^x$")
    ax.plot(x, yp, label=r"$y' = a^x\ln(a)$")
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_title(f"Graph — $y={a:g}^x$ and its derivative")
    ax.legend()
    ax.grid(True, alpha=0.25)
    return fig


def _plot_log_base_a(a: float = 5.0):
    x = np.linspace(0.15, 6, 500)
    y = np.log(x) / math.log(a)
    yp = 1.0 / (x * math.log(a))

    fig = plt.figure(figsize=(6.2, 3.6))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label=r"$y=\log_a(x)$")
    ax.plot(x, yp, label=r"$y'=\frac{1}{x\ln(a)}$")
    ax.axhline(0, linewidth=0.8)
    ax.set_title(f"Graph — $y=\\log_{{{a:g}}}(x)$ and its derivative")
    ax.legend()
    ax.grid(True, alpha=0.25)
    return fig


def _plot_ln_and_exp():
    x1 = np.linspace(0.15, 6, 400)
    ln = np.log(x1)
    ln_p = 1 / x1

    x2 = np.linspace(-2, 2, 400)
    ex = np.exp(x2)
    ex_p = np.exp(x2)

    fig = plt.figure(figsize=(6.2, 4.6))
    ax1 = fig.add_subplot(211)
    ax1.plot(x1, ln, label=r"$y=\ln(x)$")
    ax1.plot(x1, ln_p, label=r"$y'=\frac{1}{x}$")
    ax1.axhline(0, linewidth=0.8)
    ax1.set_title(r"$\ln(x)$ and its derivative")
    ax1.legend()
    ax1.grid(True, alpha=0.25)

    ax2 = fig.add_subplot(212)
    ax2.plot(x2, ex, label=r"$y=e^x$")
    ax2.plot(x2, ex_p, label=r"$y'=e^x$")
    ax2.axhline(0, linewidth=0.8)
    ax2.axvline(0, linewidth=0.8)
    ax2.set_title(r"$e^x$ and its derivative")
    ax2.legend()
    ax2.grid(True, alpha=0.25)

    fig.tight_layout()
    return fig


def _plot_tangent_on_exp_u(x0: float):
    x = np.linspace(-1, 5, 600)
    y = np.exp(x**2 - 4*x)

    y0 = math.exp(x0**2 - 4*x0)
    m = y0 * (2*x0 - 4)
    tan = m * (x - x0) + y0

    fig = plt.figure(figsize=(6.4, 3.7))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label=r"$y=e^{x^2-4x}$")
    ax.plot(x, tan, label=r"Tangent at $x=a$")
    ax.scatter([x0], [y0])
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_title(r"Tangent line at a chosen point $a$")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig, y0, m


def _plot_tangent_normal_on_log(a_base: float, x0: float):
    x = np.linspace(0.2, 6, 600)
    y = np.log(x) / math.log(a_base)

    y0 = math.log(x0) / math.log(a_base)
    m_tan = 1.0 / (x0 * math.log(a_base))
    m_norm = -1.0 / m_tan

    tan = m_tan * (x - x0) + y0
    norm = m_norm * (x - x0) + y0

    fig = plt.figure(figsize=(6.4, 3.7))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label=rf"$y=\log_{{{a_base:g}}}(x)$")
    ax.plot(x, tan, label="Tangent")
    ax.plot(x, norm, label="Normal")
    ax.scatter([x0], [y0])
    ax.axhline(0, linewidth=0.8)
    ax.set_title(r"Tangent & normal at a chosen point")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig, y0, m_tan, m_norm


def _classify_slope(m: float, eps: float = 1e-9) -> str:
    if abs(m) <= eps:
        return "flat"
    return "increasing" if m > 0 else "decreasing"


def _prediction_ui(block_key: str, prompt_md: str):
    st.markdown(prompt_md)
    choice = st.radio(
        "Your prediction",
        ["Increasing", "Decreasing", "Flat"],
        horizontal=True,
        key=f"{block_key}_choice",
    )
    return choice


def _prediction_feedback(block_key: str, predicted: str, actual: str):
    pred_norm = predicted.lower()
    if pred_norm == "increasing":
        pred_norm = "increasing"
    elif pred_norm == "decreasing":
        pred_norm = "decreasing"
    else:
        pred_norm = "flat"

    if pred_norm == actual:
        st.success("✅ Correct! Your prediction matches the slope sign at this point.")
    else:
        if actual == "flat":
            st.warning("Not quite — the tangent is horizontal here (slope = 0).")
        else:
            st.warning(f"Not quite — here the function is **{actual}** (based on the sign of the slope).")


def _reflection_box(text_md: str):
    st.info(text_md)


# -------------------------
# Blackboard sims (UNCHANGED)
# -------------------------
def _sim_convert_to_base_e_steps():
    steps = [
        BoardStep(
            latex_line=r"2^x = e^{x\ln 2}",
            teacher_explain_md=(
                "Start with the key idea:\n\n"
                "- Any exponential with base \(a\) can be rewritten using \(e\).\n"
                "- We use the identity:\n\n"
                "$$a^x = e^{x\ln(a)}$$\n\n"
                "So for \(2^x\):\n\n"
                "$$2^x = e^{x\ln 2}$$"
            ),
        ),
        BoardStep(
            latex_line=r"a^x = e^{x\ln a}",
            teacher_explain_md=(
                "General base \(a\):\n\n"
                "- This works for any \(a>0\), \(a\\neq 1\).\n\n"
                "$$a^x = e^{x\\ln(a)}$$\n\n"
                "This form is powerful because differentiating \(e^{u}\) is straightforward."
            ),
        ),
        BoardStep(
            latex_line=r"\log_5(x)=\frac{\ln(x)}{\ln(5)}",
            teacher_explain_md=(
                "Change of base for logarithms:\n\n"
                "$$\\log_a(x)=\\frac{\\ln(x)}{\\ln(a)}$$\n\n"
                "So:\n\n"
                "$$\\log_5(x)=\\frac{\\ln(x)}{\\ln(5)}$$"
            ),
        ),
    ]
    return steps


def _sim_derive_d_dx_a_pow_x_steps():
    steps = [
        BoardStep(
            latex_line=r"y=a^x",
            teacher_explain_md=(
                "Goal: find \\(\\frac{dy}{dx}\\) when the base is not \(e\).\n\n"
                "We will rewrite \(a^x\) in \(e\)-form first."
            ),
        ),
        BoardStep(
            latex_line=r"a^x = e^{x\ln(a)}",
            teacher_explain_md=(
                "Rewrite in base \(e\):\n\n"
                "$$a^x = e^{x\\ln(a)}$$\n\n"
                "Now the exponent is \(x\\ln(a)\)."
            ),
        ),
        BoardStep(
            latex_line=r"y = e^{x\ln(a)}",
            teacher_explain_md=(
                "So the function becomes:\n\n"
                "$$y = e^{x\\ln(a)}$$\n\n"
                "Now apply the chain rule."
            ),
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=e^{x\ln(a)}\cdot\frac{d}{dx}(x\ln(a))",
            teacher_explain_md=(
                "Derivative of \(e^{u}\) is \(e^{u}\\cdot u'\).\n\n"
                "Here \(u=x\\ln(a)\), so:\n\n"
                "$$\\frac{dy}{dx}=e^{x\\ln(a)}\\cdot\\frac{d}{dx}(x\\ln(a))$$"
            ),
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(x\ln(a))=\ln(a)",
            teacher_explain_md=(
                "Because \\(\\ln(a)\\) is a constant (since \(a\) is constant):\n\n"
                "$$\\frac{d}{dx}(x\\ln(a))=\\ln(a)$$"
            ),
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=e^{x\ln(a)}\ln(a)=a^x\ln(a)",
            teacher_explain_md=(
                "Substitute back \(e^{x\\ln(a)}=a^x\):\n\n"
                "$$\\frac{dy}{dx}=a^x\\ln(a)$$\n\n"
                "This is the standard rule for \(a^x\)."
            ),
        ),
    ]
    return steps


def _sim_derive_log_a_steps():
    steps = [
        BoardStep(
            latex_line=r"y=\log_a(x)",
            teacher_explain_md=(
                "We will differentiate \\(\\log_a(x)\\) using change of base.\n\n"
                "Key identity:\n\n"
                "$$\\log_a(x)=\\frac{\\ln(x)}{\\ln(a)}$$"
            ),
        ),
        BoardStep(
            latex_line=r"y=\frac{\ln(x)}{\ln(a)}",
            teacher_explain_md=(
                "Rewrite using natural log:\n\n"
                "$$y=\\frac{\\ln(x)}{\\ln(a)}$$\n\n"
                "Here \\(\\ln(a)\\) is a constant."
            ),
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=\frac{1}{\ln(a)}\cdot\frac{d}{dx}(\ln x)",
            teacher_explain_md=(
                "Pull out the constant:\n\n"
                "$$\\frac{dy}{dx}=\\frac{1}{\\ln(a)}\\cdot\\frac{d}{dx}(\\ln x)$$"
            ),
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(\ln x)=\frac{1}{x}",
            teacher_explain_md=(
                "Derivative of \\(\\ln x\\) is:\n\n"
                "$$\\frac{d}{dx}(\\ln x)=\\frac{1}{x}$$"
            ),
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=\frac{1}{x\ln(a)}",
            teacher_explain_md=(
                "Final result:\n\n"
                "$$\\frac{d}{dx}(\\log_a(x))=\\frac{1}{x\\ln(a)}$$"
            ),
        ),
    ]
    return steps


def _sim_chain_rule_exp_steps():
    steps = [
        BoardStep(
            latex_line=r"y=e^{x^2-4x}",
            teacher_explain_md=(
                "Composite function: \(e^{u}\) where \(u=x^2-4x\).\n\n"
                "We will use:\n\n"
                "$$\\frac{d}{dx}(e^{u}) = e^{u}\\cdot u'$$"
            ),
        ),
        BoardStep(
            latex_line=r"u=x^2-4x",
            teacher_explain_md=(
                "Let the inside be:\n\n"
                "$$u=x^2-4x$$\n\n"
                "Now compute \(u'\)."
            ),
        ),
        BoardStep(
            latex_line=r"\frac{du}{dx}=2x-4",
            teacher_explain_md=(
                "Differentiate the inside:\n\n"
                "$$\\frac{du}{dx}=2x-4$$"
            ),
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=e^{x^2-4x}(2x-4)",
            teacher_explain_md=(
                "Chain rule result:\n\n"
                "$$\\frac{dy}{dx}=e^{x^2-4x}(2x-4)$$\n\n"
                "Notice: \(e^{x^2-4x}>0\), so the sign of the derivative depends on \(2x-4\)."
            ),
        ),
    ]
    return steps


def _sim_chain_rule_log_steps():
    steps = [
        BoardStep(
            latex_line=r"y=\ln(5x^2+1)",
            teacher_explain_md=(
                "Composite function: \\(\\ln(u)\\) where \\(u=5x^2+1\\).\n\n"
                "We use:\n\n"
                "$$\\frac{d}{dx}(\\ln u)=\\frac{u'}{u}$$"
            ),
        ),
        BoardStep(
            latex_line=r"u=5x^2+1",
            teacher_explain_md=(
                "Let:\n\n"
                "$$u=5x^2+1$$\n\n"
                "Compute \(u'\)."
            ),
        ),
        BoardStep(
            latex_line=r"\frac{du}{dx}=10x",
            teacher_explain_md=(
                "Differentiate the inside:\n\n"
                "$$\\frac{du}{dx}=10x$$"
            ),
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=\frac{10x}{5x^2+1}",
            teacher_explain_md=(
                "Apply the rule:\n\n"
                "$$\\frac{dy}{dx}=\\frac{u'}{u}=\\frac{10x}{5x^2+1}$$"
            ),
        ),
    ]
    return steps


def _practice_questions():
    # (UNCHANGED) — kept exactly as before in your version
    qs = []

    qs.append({
        "q_latex": r"\text{Convert to base }e:\quad 3^x",
        "hint_md": "Use the identity: $$a^x = e^{x\\ln(a)}$$",
        "ans_steps_latex": [r"3^x = e^{x\ln(3)}"]
    })

    qs.append({
        "q_latex": r"\text{Convert to base }e:\quad 7^{2x}",
        "hint_md": "Rewrite as $$7^{2x}=(7^2)^x$$ or apply identity directly.",
        "ans_steps_latex": [r"7^{2x} = e^{2x\ln 7}"]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(2^x\right)",
        "hint_md": "Rule: $$\\frac{d}{dx}(a^x)=a^x\\ln(a)$$",
        "ans_steps_latex": [r"\frac{d}{dx}(2^x)=2^x\ln(2)"]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(5^{x^2}\right)",
        "hint_md": "Use chain rule with $$u=x^2$$ and $$\\frac{d}{dx}(a^u)=a^u\\ln(a)\cdot u'$$",
        "ans_steps_latex": [
            r"y=5^{x^2}",
            r"\frac{dy}{dx}=5^{x^2}\ln(5)\cdot \frac{d}{dx}(x^2)",
            r"\frac{dy}{dx}=5^{x^2}\ln(5)\cdot 2x",
            r"\frac{dy}{dx}=2x\,5^{x^2}\ln(5)"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(e^{3x-1}\right)",
        "hint_md": "For $$e^u$$, derivative is $$e^u\\cdot u'$$.",
        "ans_steps_latex": [
            r"y=e^{3x-1}",
            r"\frac{dy}{dx}=e^{3x-1}\cdot \frac{d}{dx}(3x-1)",
            r"\frac{dy}{dx}=e^{3x-1}\cdot 3",
            r"\frac{dy}{dx}=3e^{3x-1}"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(\ln x\right)",
        "hint_md": "Basic rule: $$\\frac{d}{dx}(\\ln x)=\\frac{1}{x}$$",
        "ans_steps_latex": [r"\frac{d}{dx}(\ln x)=\frac{1}{x}"]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(\log_4 x\right)",
        "hint_md": "Use change of base: $$\\log_a x=\\frac{\\ln x}{\\ln a}$$",
        "ans_steps_latex": [
            r"y=\log_4(x)=\frac{\ln x}{\ln 4}",
            r"\frac{dy}{dx}=\frac{1}{\ln 4}\cdot\frac{1}{x}",
            r"\frac{dy}{dx}=\frac{1}{x\ln 4}"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(\ln(5x^2+1)\right)",
        "hint_md": "For $$\\ln(u)$$: $$\\frac{d}{dx}(\\ln u)=\\frac{u'}{u}$$",
        "ans_steps_latex": [
            r"y=\ln(5x^2+1)",
            r"u=5x^2+1,\quad u'=10x",
            r"\frac{dy}{dx}=\frac{u'}{u}=\frac{10x}{5x^2+1}"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(\log_3(2x-1)\right)",
        "hint_md": "Combine: $$\\frac{d}{dx}(\\log_a u)=\\frac{u'}{u\\ln a}$$",
        "ans_steps_latex": [
            r"y=\log_3(2x-1)",
            r"u=2x-1,\quad u'=2",
            r"\frac{dy}{dx}=\frac{u'}{u\ln 3}=\frac{2}{(2x-1)\ln 3}"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(e^{x^2-4x}\right)",
        "hint_md": "Use $$\\frac{d}{dx}(e^u)=e^u u'$$ with $$u=x^2-4x$$.",
        "ans_steps_latex": [
            r"y=e^{x^2-4x}",
            r"u=x^2-4x,\quad u'=2x-4",
            r"\frac{dy}{dx}=e^{x^2-4x}(2x-4)"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(2^{3x}\right)",
        "hint_md": "Treat it as $$a^{u}$$: derivative $$a^u\\ln(a)u'$$",
        "ans_steps_latex": [
            r"y=2^{3x}",
            r"\frac{dy}{dx}=2^{3x}\ln(2)\cdot \frac{d}{dx}(3x)",
            r"\frac{dy}{dx}=2^{3x}\ln(2)\cdot 3",
            r"\frac{dy}{dx}=3\ln(2)\,2^{3x}"
        ]
    })

    qs.append({
        "q_latex": r"\frac{d}{dx}\left(\ln(e^{2x}+1)\right)",
        "hint_md": "Outer: ln(u). Inner: u=e^{2x}+1.",
        "ans_steps_latex": [
            r"y=\ln(e^{2x}+1)",
            r"u=e^{2x}+1,\quad u'=2e^{2x}",
            r"\frac{dy}{dx}=\frac{u'}{u}=\frac{2e^{2x}}{e^{2x}+1}"
        ]
    })

    qs.append({
        "q_latex": r"\text{Find where } y=e^{x^2-4x} \text{ has a horizontal tangent.}",
        "hint_md": "Horizontal tangent means $$y'=0$$.",
        "ans_steps_latex": [
            r"y=e^{x^2-4x}",
            r"y'=e^{x^2-4x}(2x-4)",
            r"y'=0 \Rightarrow e^{x^2-4x}(2x-4)=0",
            r"e^{x^2-4x}>0\ \text{for all }x,\ \Rightarrow 2x-4=0",
            r"x=2"
        ]
    })

    qs.append({
        "q_latex": r"\text{Find the tangent line to } y=\ln x \text{ at } x=1.",
        "hint_md": "Use $$y-y_1=m(x-x_1)$$ with $$m=y'(1)$$.",
        "ans_steps_latex": [
            r"y=\ln x \Rightarrow y'=\frac{1}{x}",
            r"m=y'(1)=1",
            r"y(1)=\ln(1)=0",
            r"y-0=1(x-1)",
            r"y=x-1"
        ]
    })

    qs.append({
        "q_latex": r"\text{Find the normal line to } y=\log_2 x \text{ at } x=2.",
        "hint_md": "Normal slope = negative reciprocal of tangent slope.",
        "ans_steps_latex": [
            r"y=\log_2 x=\frac{\ln x}{\ln 2}",
            r"y'=\frac{1}{x\ln 2}",
            r"m_{\text{tan}}=y'(2)=\frac{1}{2\ln 2}",
            r"m_{\text{norm}}=-\frac{1}{m_{\text{tan}}}=-2\ln 2",
            r"y(2)=\log_2 2=1",
            r"y-1=-2\ln 2\,(x-2)"
        ]
    })

    qs.append({
        "q_latex": r"\text{Use logarithmic differentiation: } y=x^x",
        "hint_md": "Take ln both sides: $$\\ln y = x\\ln x$$ then differentiate.",
        "ans_steps_latex": [
            r"y=x^x",
            r"\ln y = x\ln x",
            r"\frac{1}{y}y' = \ln x + 1",
            r"y' = y(\ln x + 1)",
            r"y' = x^x(\ln x + 1)"
        ]
    })

    return qs


def render():
    st.header("Subtopic 4.7: Derivatives of Exponential and Logarithmic Functions")

    # Lesson objectives at the top
    st.markdown("### Lesson Objectives")

    # 4.7.1–4.7.3 in ONE markdown+KaTeX block
    _md_math(
        r"""
By the end of this lesson, you should be able to:

- **4.7.1** Convert exponential and logarithmic functions with general bases into natural base \(e\) form:
  $$a^x=e^{x\ln(a)},\qquad \log_b(x)=\frac{\ln(x)}{\ln(b)} \quad (a,b>0,\ a\neq 1,\ b\neq 1)$$
  and review exponent/log properties (product, quotient, power).

- **4.7.2** Differentiate exponential functions:
  $$\frac{d}{dx}(a^x)=a^x\ln(a),\qquad \frac{d}{dx}(e^x)=e^x.$$

- **4.7.3** Differentiate logarithmic functions:
  $$\frac{d}{dx}(\log_b x)=\frac{1}{x\ln(b)},\qquad \frac{d}{dx}(\ln x)=\frac{1}{x}.$$

- **4.7.4** Differentiate functions involving exponentials using the chain rule:
"""
    )

    # 4.7.4 MUST be rendered with st.latex (not inside _md_math)
    st.latex(r"\frac{d}{dx}\bigl(c\,e^{U(x)}\bigr)=c\,e^{U(x)}\,U'(x)")
    st.latex(r"\frac{d}{dx}\bigl(c\,a^{U(x)}\bigr)=c\,a^{U(x)}\,U'(x)\,\ln(a)")

    # 4.7.5–4.7.9 continue in a SECOND markdown+KaTeX block
    _md_math(
        r"""
- **4.7.5** Differentiate functions involving logarithms using the chain rule:
  $$\frac{d}{dx}\bigl(c\,\ln(U(x))\bigr)=c\,\frac{U'(x)}{U(x)} \quad (U(x)>0).$$

- **4.7.6** Find equations of **tangent** and **normal** lines to exponential/logarithmic graphs.

- **4.7.7** Find the value(s) of \(x\) where a function has a **horizontal tangent**:
  $$y'(x)=0.$$

- **4.7.8** Find derivatives using **logarithmic differentiation** (when it helps).

- **4.7.9** Use derivatives of exponential/log functions in real-life applications (growth/decay, concentration change), and interpret the derivative as an instant rate of change.
"""
    )

    tabs = st.tabs(["Learn", "Practice"])

    # -------------------------
    # LEARN
    # -------------------------
    with tabs[0]:
        st.subheader("4.7.1 Convert to base $e$ (key identities)")
        _md_math("We rewrite general bases into forms that differentiate cleanly.\n\n**Core identities (memorize):**")
        _latex_block(r"a^x = e^{x\ln(a)} \quad (a>0,\ a\neq 1)")
        _latex_block(r"\log_a(x)=\frac{\ln(x)}{\ln(a)} \quad (a>0,\ a\neq 1)")

        st.markdown("---")
        st.markdown("### Blackboard simulation — Convert to base $e$ / $\\ln$")
        st.markdown("**Problem (what the student should do):** Convert each expression to base $e$ or $\\ln$.")
        render_simulation(_sim_convert_to_base_e_steps(), "Mini Blackboard — Convert to base $e$ / $\\ln$")

        st.markdown("---")
        st.subheader("4.7.2 Derivative of exponential functions (including general base)")
        st.markdown("**Natural base:**")
        _latex_block(r"\frac{d}{dx}\left(e^x\right)=e^x")
        st.markdown("**General base:**")
        _latex_block(r"\frac{d}{dx}\left(a^x\right)=a^x\ln(a)")

        st.markdown("---")
        st.markdown("### Blackboard simulation — Why the rule for $a^x$ works")
        st.markdown("**Problem (what the student should do):** Rewrite $a^x$ using base $e$, then differentiate.")
        st.markdown("**Target rule:**")
        _latex_block(r"\frac{d}{dx}(a^x)=a^x\ln(a)")
        render_simulation(_sim_derive_d_dx_a_pow_x_steps(), "Derive the rule (using base e)")

        st.markdown("---")
        st.subheader("4.7.3 Derivative of logarithmic functions")
        _latex_block(r"\frac{d}{dx}(\ln x)=\frac{1}{x}")
        _latex_block(r"\frac{d}{dx}(\log_a x)=\frac{1}{x\ln(a)}")

        st.markdown("---")
        st.markdown("### Blackboard simulation — Derivative of $\\log_a(x)$")
        st.markdown("**Problem:** Differentiate $\\log_a(x)$ using change of base.")
        st.markdown("**Target rule:**")
        _latex_block(r"\frac{d}{dx}(\log_a x)=\frac{1}{x\ln(a)}")
        render_simulation(_sim_derive_log_a_steps(), "Differentiate log base a (change of base)")

        st.markdown("---")
        st.subheader("4.7.4–4.7.5 Chain rule with exponential & logarithmic functions")
        st.markdown("**Generalised (must know):**")
        _latex_block(r"\frac{d}{dx}\left(c\,e^{U(x)}\right)=c\,e^{U(x)}\cdot U'(x)")
        _latex_block(r"\frac{d}{dx}\left(c\,a^{U(x)}\right)=c\,a^{U(x)}\ln(a)\cdot U'(x)")
        _latex_block(r"\frac{d}{dx}\left(c\,\ln(U(x))\right)=c\,\frac{U'(x)}{U(x)}")

        st.markdown("---")
        st.markdown("### Blackboard simulation — Chain rule with $e^{x^2-4x}$")
        st.markdown("**Problem:** Differentiate $y=e^{x^2-4x}$.")
        render_simulation(_sim_chain_rule_exp_steps(), "Example — Chain rule with exponential")

        st.markdown("---")
        st.markdown("### Blackboard simulation — Chain rule with $\\ln(5x^2+1)$")
        st.markdown("**Problem:** Differentiate $y=\\ln(5x^2+1)$.")
        render_simulation(_sim_chain_rule_log_steps(), "Example — Chain rule with logarithm")

        st.markdown("---")
        st.subheader("4.7.6 Tangent & normal lines for exp/log graphs")

        st.markdown("**Step A — Get the tangent slope**")
        _latex_block(r"m_{\text{tan}} = y'(a)")
        st.markdown("**Step B — Tangent line equation (point-slope form)**")
        _latex_block(r"y-y(a)=y'(a)\,(x-a)")
        st.markdown("**Step C — Normal line slope (perpendicular line)**")
        _latex_block(r"m_{\perp}=-\frac{1}{y'(a)}")

        st.markdown("#### Check your prediction → Reveal → Next point")
        st.caption("Predict the behaviour at the given point, then reveal the tangent to check your understanding.")

        base_a = st.selectbox("Choose base $a$ for the graph", [2.0, 3.0, 5.0, 10.0], index=0, key="log_base_sim_47_6")
        x_positions = [0.5, 1.0, 2.0, 3.0, 5.0]

        state_key = f"idx_log_sim_{base_a}"
        reveal_key = f"reveal_log_sim_{base_a}"

        if state_key not in st.session_state:
            st.session_state[state_key] = 2
        if reveal_key not in st.session_state:
            st.session_state[reveal_key] = False

        idx = st.session_state[state_key]
        x0 = x_positions[idx]

        predicted = _prediction_ui(
            block_key=f"pred_log_{base_a}",
            prompt_md=f"**At** $$x={x0:g}$$ **on** $$y=\\log_{{{base_a:g}}}(x),$$ **is the function increasing, decreasing, or flat?**",
        )

        cA, cB, cC = st.columns([1.2, 1.2, 2])
        with cA:
            if st.button("Reveal", key=f"reveal_btn_log_{base_a}"):
                st.session_state[reveal_key] = True
        with cB:
            if st.button("Next point ▶", key=f"next_btn_log_{base_a}"):
                st.session_state[state_key] = min(len(x_positions) - 1, st.session_state[state_key] + 1)
                st.session_state[reveal_key] = False
                st.rerun()

        if st.session_state[reveal_key]:
            fig_ln, y0, m_tan, m_norm = _plot_tangent_normal_on_log(base_a, x0)
            _small_graph(fig_ln)

            actual = _classify_slope(m_tan)
            _prediction_feedback(f"pred_log_{base_a}", predicted, actual)
            _reflection_box(r"Reflection: What did the sign of $$y'$$ tell you about the curve at this point?")

            st.markdown("**At the chosen point:**")
            _latex_block(r"a=" + f"{base_a:g}" + r",\quad x_0=" + f"{x0:g}")
            _latex_block(
                r"m_{\text{tan}}=\frac{1}{x_0\ln(a)}=\frac{1}{"
                + f"{x0:g}"
                + r"\ln("
                + f"{base_a:g}"
                + r")}"
            )
            _latex_block(r"m_{\perp}=-\frac{1}{m_{\text{tan}}}")
        else:
            st.info("Choose your prediction, then click **Reveal**.")

        st.markdown("---")
        st.subheader("4.7.7 Horizontal tangents")
        st.markdown("A horizontal tangent means the slope is zero, so:")
        _latex_block(r"y'(x)=0")

        st.markdown("#### Check your prediction → Reveal → Next point")
        st.caption("Predict the behaviour at the given point, then reveal the tangent to check your understanding.")

        x_positions_exp = [0.0, 1.0, 2.0, 3.0, 4.0]
        exp_key = "idx_exp_sim_47_7"
        exp_reveal_key = "reveal_exp_sim_47_7"

        if exp_key not in st.session_state:
            st.session_state[exp_key] = 2
        if exp_reveal_key not in st.session_state:
            st.session_state[exp_reveal_key] = False

        x0e = x_positions_exp[st.session_state[exp_key]]

        predicted2 = _prediction_ui(
            block_key="pred_exp_47_7",
            prompt_md=f"**For** $$y=e^{{x^2-4x}}$$ **at** $$x={x0e:g},$$ **is the function increasing, decreasing, or flat?**",
        )

        d1, d2, d3 = st.columns([1.2, 1.2, 2])
        with d1:
            if st.button("Reveal", key="reveal_btn_exp_47_7"):
                st.session_state[exp_reveal_key] = True
        with d2:
            if st.button("Next point ▶", key="next_btn_exp_47_7"):
                st.session_state[exp_key] = min(len(x_positions_exp) - 1, st.session_state[exp_key] + 1)
                st.session_state[exp_reveal_key] = False
                st.rerun()

        if st.session_state[exp_reveal_key]:
            fig_te, y0e, me = _plot_tangent_on_exp_u(x0e)
            _small_graph(fig_te)

            actual2 = _classify_slope(me)
            _prediction_feedback("pred_exp_47_7", predicted2, actual2)
            _reflection_box(r"Reflection: What does $$y'=0$$ mean about the tangent line at that point?")

            st.markdown("**At the chosen point:**")
            _latex_block(r"x_0=" + f"{x0e:g}")
            _latex_block(r"y'(x)=e^{x^2-4x}(2x-4)")
        else:
            st.info("Choose your prediction, then click **Reveal**.")

        st.markdown("---")
        st.subheader("4.7.8 Logarithmic differentiation (when it helps)")
        st.markdown(
            "We use logarithmic differentiation when the function has a variable both in the base and exponent (like \(x^x\)), "
            "or when taking natural logs makes products/quotients with powers much easier."
        )
        st.markdown("**Key idea:** take natural log on both sides, then differentiate.")
        _latex_block(r"\ln(y)=\ln(f(x))")
        _latex_block(r"\frac{1}{y}\frac{dy}{dx}=\frac{d}{dx}\left[\ln(f(x))\right]")

        st.markdown("#### Worked example: $y=x^x$")
        _latex_block(r"y=x^x")
        _latex_block(r"\ln(y)=x\ln(x)")
        _latex_block(r"\frac{1}{y}y'=\ln(x)+1")
        _latex_block(r"y'=x^x(\ln(x)+1)")

        st.markdown("---")
        st.subheader("Graphs — seeing what the derivative means")
        st.markdown(
            "These graphs help you *see* the meaning of the derivative:\n\n"
            "- The curve \(y\) shows the function.\n"
            "- The curve \(y'\) shows the slope at each \(x\).\n\n"
            "If \(y'>0\) the function is increasing; if \(y'<0\) it is decreasing."
        )
        st.markdown("#### Graph 1 — $y=a^x$ and $y' = a^x\\ln(a)$")
        _small_graph(_plot_exp_base_a(a=2.0))

        st.markdown("#### Graph 2 — $y=\\log_a(x)$ and $y' = \\dfrac{1}{x\\ln(a)}$")
        _small_graph(_plot_log_base_a(a=5.0))

        st.markdown("#### Graph 3 — $\\ln(x)$ and $e^x$")
        _small_graph(_plot_ln_and_exp())

        st.markdown("---")
        st.subheader("4.7.9 Real-life applications")
        _md_math(
            """
Exponential and logarithmic models appear in population growth/decay and chemical concentration change.
The derivative tells us the **instant rate of change** at that moment.

**A) Growth / decay model**
If a quantity grows (or decays) proportionally to its current size:
$$P(t)=P_0e^{kt}$$
then
$$\\frac{dP}{dt}=kP_0e^{kt}=kP(t).$$

- If $$k>0$$, then $$\\frac{dP}{dt}>0$$ and the quantity is **increasing**.
- If $$k<0$$, then $$\\frac{dP}{dt}<0$$ and the quantity is **decreasing**.
- The size of $$\\left|\\frac{dP}{dt}\\right|$$ tells you **how fast** the change is happening at time $$t$$.

**B) Concentration change (first-order decay)**
A common model for a decreasing concentration is:
$$C(t)=C_0e^{-kt} \\quad (k>0).$$
Then:
$$\\frac{dC}{dt}=-kC(t).$$
This means the concentration is always decreasing, and the rate of decrease is proportional to the current concentration.

**C) Using a derivative to interpret “rate right now”**
If you know $$P(t_1)$$ and $$\\frac{dP}{dt}(t_1)$$:
- $$P(t_1)$$ is the amount **now**,
- $$\\frac{dP}{dt}(t_1)$$ is the change **per unit time now** (units matter).

**D) Logarithms help measure multiplicative change**
If $$P(t)>0$$, then:
$$\\frac{d}{dt}\\bigl(\\ln(P(t))\\bigr)=\\frac{P'(t)}{P(t)}.$$
So $$\\frac{P'(t)}{P(t)}$$ is the **relative growth rate** (growth per unit of what you already have).
"""
        )

    # -------------------------
    # PRACTICE (UNCHANGED)
    # -------------------------
    with tabs[1]:
        st.subheader("Practice (15+ questions)")
        st.markdown("Click **Hint** if you get stuck. Click **Show Answer** to see the full solution (all steps at once).")

        questions = _practice_questions()

        for i, q in enumerate(questions, start=1):
            st.markdown("---")
            st.markdown(f"### Question {i}")
            _latex_block(q["q_latex"])

            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Hint", key=f"q47_hint_{i}"):
                    st.info("")
                    _md_math(q["hint_md"])
            with c2:
                if st.button("Show Answer", key=f"q47_ans_{i}"):
                    st.success("Solution (step-by-step):")
                    for step in q["ans_steps_latex"]:
                        _latex_block(step)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
