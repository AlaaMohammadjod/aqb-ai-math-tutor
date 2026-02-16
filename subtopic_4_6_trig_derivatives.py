import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# ---------------------------
# Helpers (graphs + styling)
# ---------------------------

def _plot_pair(x, y, yp, title, xlim=None, ylim=None):
    """
    Smaller graph size (per request), still readable.
    """
    fig = plt.figure(figsize=(4.6, 2.55), dpi=135)  # smaller than before
    ax = fig.add_subplot(111)

    ax.plot(x, y, label=r"$y$")
    ax.plot(x, yp, label=r"$y'$")
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)

    ax.grid(True, alpha=0.25)
    ax.set_title(title, fontsize=11)
    ax.legend(fontsize=9)
    st.pyplot(fig, clear_figure=True)


def _teacher_graph_explain_sin():
    st.markdown("### What the graph is teaching you (simple + detailed)")
    st.markdown(
        r"""
**We are comparing the function and its derivative:**

- The function is:  $y=\sin x$
- The derivative is:  $y'=\cos x$

**How to read the graph (the “teacher way”):**
1. Wherever $y'=\cos x$ is **positive**, the function $\sin x$ is **increasing**.
2. Wherever $y'=\cos x$ is **negative**, the function $\sin x$ is **decreasing**.
3. Wherever $y'=\cos x=0$, the function $\sin x$ has a **horizontal tangent** (flat moment).  
   That happens at $x=\frac{\pi}{2}, \frac{3\pi}{2}, \dots$

✅ So the derivative graph $y'$ is like a “slope detector” for the function graph $y$.
"""
    )


def _teacher_graph_explain_chain_trig():
    st.markdown("### What the chain rule changes in trig graphs (simple + detailed)")
    st.markdown(
        r"""
Compare these:

- $y=\sin x \;\Rightarrow\; y'=\cos x$
- $y=\sin(2x^3) \;\Rightarrow\; y'=6x^2\cos(2x^3)$

**What’s new in the second derivative?**  
There are **two factors**:
- $\cos(2x^3)$ controls the **direction** (positive slope / negative slope).
- $6x^2$ controls the **magnitude** (how steep).

**Meaning:**
- Near $x=0$, $6x^2$ is tiny $\Rightarrow$ slopes are small $\Rightarrow$ curve changes gently.
- As $|x|$ grows, $6x^2$ grows $\Rightarrow$ slopes become big $\Rightarrow$ curve becomes steeper.

✅ This is exactly the “inside derivative multiplier” from the chain rule.
"""
    )


# ---------------------------
# Content: Objectives 4.6.1–4.6.5
# ---------------------------

def _section_objectives():
    st.markdown("## Subtopic 4.6 — Derivatives of Trigonometric Functions")
    st.markdown("### Learning objectives (we will cover ALL of them):")
    st.markdown(
        r"""
**4.6.1** Find the derivatives of the six trigonometric functions  
**4.6.2** Differentiate trig functions using chain rule + other rules  
**4.6.3** Find equations of tangent / normal lines to trig graphs  
**4.6.4** Find higher order derivatives  
**4.6.5** Apply trig derivatives to a real-life model (spring–mass)
"""
    )


def _section_core_rules():
    st.markdown("## 1) The six basic trig derivatives — objective 4.6.1")

    st.markdown("### The derivative table (memorize + understand)")
    st.latex(r"\frac{d}{dx}(\sin x)=\cos x")
    st.latex(r"\frac{d}{dx}(\cos x)=-\sin x")
    st.latex(r"\frac{d}{dx}(\tan x)=\sec^2 x")
    st.latex(r"\frac{d}{dx}(\cot x)=-\csc^2 x")
    st.latex(r"\frac{d}{dx}(\sec x)=\sec x \tan x")
    st.latex(r"\frac{d}{dx}(\csc x)=-\csc x \cot x")

    st.info(
        "Teacher note: Once you know sin and cos, the rest are built using identities + quotient rule."
    )

    st.markdown("### A proof-style explanation (simple, not heavy) — objective 4.6.1")
    st.markdown(
        r"""
Your book shows the derivative of $\sin x$ from the **limit definition**.
We do not need every algebra line in class, but we need the idea:
"""
    )
    st.latex(r"\frac{d}{dx}(\sin x)=\lim_{h\to 0}\frac{\sin(x+h)-\sin x}{h}")
    st.markdown("Then we use:")
    st.latex(r"\sin(x+h)=\sin x \cos h + \cos x \sin h")
    st.markdown("After rearranging, the limit becomes:")
    st.latex(
        r"(\sin x)\lim_{h\to 0}\frac{\cos h-1}{h}+(\cos x)\lim_{h\to 0}\frac{\sin h}{h}"
    )
    st.markdown("And the key limits are:")
    st.latex(r"\lim_{h\to 0}\frac{\sin h}{h}=1,\qquad \lim_{h\to 0}\frac{\cos h-1}{h}=0")
    st.markdown("So:")
    st.latex(r"\frac{d}{dx}(\sin x)=0\cdot \sin x + 1\cdot \cos x = \cos x")
    st.success("✅ This is why the result is true (not just memorized).")

    st.markdown("### Mini blackboard simulation: proving the idea (teacher-style)")
    steps = [
        BoardStep(
            latex_line=r"\frac{d}{dx}(\sin x)=\lim_{h\to 0}\frac{\sin(x+h)-\sin x}{h}",
            teacher_explain_md=r"Start from the **limit definition** of derivative. This is the foundation.",
        ),
        BoardStep(
            latex_line=r"\sin(x+h)=\sin x\cos h+\cos x\sin h",
            teacher_explain_md=r"Use the trig identity for $\sin(\alpha+\beta)$.",
        ),
        BoardStep(
            latex_line=r"\frac{\sin(x+h)-\sin x}{h}=\sin x\cdot\frac{\cos h-1}{h}+\cos x\cdot\frac{\sin h}{h}",
            teacher_explain_md=r"Substitute the identity and group terms carefully.",
        ),
        BoardStep(
            latex_line=r"\lim_{h\to 0}\frac{\sin h}{h}=1,\quad \lim_{h\to 0}\frac{\cos h-1}{h}=0",
            teacher_explain_md=r"These are the two standard trig limits your book uses.",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(\sin x)=\sin x\cdot 0+\cos x\cdot 1=\cos x",
            teacher_explain_md=r"So the derivative of $\sin x$ is $\cos x$.",
        ),
    ]
    render_simulation(steps, "Mini Proof Simulation — Why  d/dx(sin x) = cos x")


def _section_rule_combos():
    st.markdown("## 2) Differentiating trig expressions using other rules — objective 4.6.2")

    st.markdown("### Example 1 (Product Rule):")
    st.latex(r"f(x)=x^5\cos x")
    steps = [
        BoardStep(
            latex_line=r"f(x)=x^5\cos x",
            teacher_explain_md=r"This is a **product**: $x^5$ times $\cos x$. Use the product rule.",
        ),
        BoardStep(
            latex_line=r"f'(x)=\frac{d}{dx}(x^5)\cos x + x^5\frac{d}{dx}(\cos x)",
            teacher_explain_md=r"Product rule: $(uv)'=u'v+uv'$.",
        ),
        BoardStep(
            latex_line=r"f'(x)=5x^4\cos x + x^5(-\sin x)",
            teacher_explain_md=r"Derivative: $\frac{d}{dx}(x^5)=5x^4$, and $\frac{d}{dx}(\cos x)=-\sin x$.",
        ),
        BoardStep(
            latex_line=r"f'(x)=5x^4\cos x - x^5\sin x",
            teacher_explain_md=r"Final simplified derivative.",
        ),
    ]
    render_simulation(steps, "Example — Product Rule with Trig")

    st.markdown("### Example 2 (Chain Rule):")
    st.latex(r"g(x)=(\cos x)^3")
    steps2 = [
        BoardStep(
            latex_line=r"g(x)=(\cos x)^3",
            teacher_explain_md=r"This is a **power of a trig function**. Treat $\cos x$ as the inside.",
        ),
        BoardStep(
            latex_line=r"u=\cos x \quad\Rightarrow\quad g=u^3",
            teacher_explain_md=r"Let $u$ represent the inside. This makes the chain rule structure clear.",
        ),
        BoardStep(
            latex_line=r"\frac{dg}{du}=3u^2",
            teacher_explain_md=r"Differentiate the outside: $\frac{d}{du}(u^3)=3u^2$.",
        ),
        BoardStep(
            latex_line=r"\frac{du}{dx}=-\sin x",
            teacher_explain_md=r"Differentiate the inside: $\frac{d}{dx}(\cos x)=-\sin x$.",
        ),
        BoardStep(
            latex_line=r"g'(x)=\frac{dg}{du}\cdot\frac{du}{dx}=3(\cos x)^2(-\sin x)",
            teacher_explain_md=r"Multiply by chain rule.",
        ),
        BoardStep(
            latex_line=r"g'(x)=-3\sin x\cos^2 x",
            teacher_explain_md=r"Final simplified answer.",
        ),
    ]
    render_simulation(steps2, "Example — Chain Rule with Trig Power")

    st.markdown("### Example 3 (Chain Rule inside angle):")
    st.latex(r"h(x)=\cos(3x)")
    steps3 = [
        BoardStep(
            latex_line=r"h(x)=\cos(3x)",
            teacher_explain_md=r"Composite function: outside is $\cos(\cdot)$, inside is $3x$.",
        ),
        BoardStep(
            latex_line=r"u=3x \quad\Rightarrow\quad h=\cos u",
            teacher_explain_md=r"Let $u$ be the inside.",
        ),
        BoardStep(
            latex_line=r"\frac{dh}{du}=-\sin u",
            teacher_explain_md=r"Derivative of $\cos u$ is $-\sin u$.",
        ),
        BoardStep(
            latex_line=r"\frac{du}{dx}=3",
            teacher_explain_md=r"Derivative of $3x$ is $3$.",
        ),
        BoardStep(
            latex_line=r"h'(x)=(-\sin(3x))\cdot 3=-3\sin(3x)",
            teacher_explain_md=r"Multiply by chain rule and substitute back.",
        ),
    ]
    render_simulation(steps3, "Example — Chain Rule for cos(3x)")


def _section_tangent_normal():
    st.markdown("## 3) Tangent & normal lines to trig graphs — objective 4.6.3")

    st.markdown("### Key idea:")
    st.latex(r"\text{Slope of tangent at }x=a \text{ is } y'(a)")
    st.latex(r"\text{Normal slope} = -\frac{1}{y'(a)} \quad (y'(a)\neq 0)")

    st.markdown("### Example (tangent + normal):")
    st.latex(r"y=\sin x \quad \text{at } x=\frac{\pi}{6}")

    steps = [
        BoardStep(
            latex_line=r"y=\sin x,\quad a=\frac{\pi}{6}",
            teacher_explain_md=r"We want the tangent and normal lines at $x=a$. We need **point** and **slope**.",
        ),
        BoardStep(
            latex_line=r"y'=\cos x",
            teacher_explain_md=r"Derivative gives the slope function.",
        ),
        BoardStep(
            latex_line=r"m_{\text{tan}}=y'(a)=\cos\left(\frac{\pi}{6}\right)=\frac{\sqrt{3}}{2}",
            teacher_explain_md=r"Tangent slope is $\cos(\pi/6)=\sqrt{3}/2$.",
        ),
        BoardStep(
            latex_line=r"y(a)=\sin\left(\frac{\pi}{6}\right)=\frac{1}{2}",
            teacher_explain_md=r"Point on the curve: $\left(\frac{\pi}{6},\frac12\right)$.",
        ),
        BoardStep(
            latex_line=r"y-\frac12=\frac{\sqrt3}{2}\left(x-\frac{\pi}{6}\right)",
            teacher_explain_md=r"Point–slope form of tangent line.",
        ),
        BoardStep(
            latex_line=r"m_{\text{norm}}=-\frac{1}{m_{\text{tan}}}=-\frac{2}{\sqrt3}",
            teacher_explain_md=r"Normal slope is the negative reciprocal.",
        ),
        BoardStep(
            latex_line=r"y-\frac12=-\frac{2}{\sqrt3}\left(x-\frac{\pi}{6}\right)",
            teacher_explain_md=r"Point–slope form of normal line.",
        ),
    ]
    render_simulation(steps, "Example — Tangent & Normal Lines (Trig)")


def _section_higher_order():
    st.markdown("## 4) Higher order derivatives — objective 4.6.4")

    st.markdown("### Example:")
    st.latex(r"y=\sin x")

    steps = [
        BoardStep(
            latex_line=r"y=\sin x",
            teacher_explain_md=r"We differentiate repeatedly. Each derivative tells a new “rate of change”.",
        ),
        BoardStep(
            latex_line=r"y'=\cos x",
            teacher_explain_md=r"First derivative: slope of the curve.",
        ),
        BoardStep(
            latex_line=r"y''=-\sin x",
            teacher_explain_md=r"Second derivative: tells us about concavity (curving up/down).",
        ),
        BoardStep(
            latex_line=r"y'''=-\cos x",
            teacher_explain_md=r"Third derivative: rate of change of concavity.",
        ),
        BoardStep(
            latex_line=r"y^{(4)}=\sin x",
            teacher_explain_md=r"Notice the cycle: derivatives repeat every 4 steps for $\sin x$.",
        ),
    ]
    render_simulation(steps, "Higher Derivatives — sin x cycles every 4")


def _section_application():
    st.markdown("## 5) Real-life application: spring–mass model — objective 4.6.5")

    st.markdown("A common physics model for vertical displacement of a spring–mass system is:")
    st.latex(r"u(t)=a\cos(\omega t)+b\sin(\omega t)")

    st.markdown(
        r"""
- $u(t)$ is displacement  
- $t$ is time  
- $\omega$ is angular frequency  
- $a,b$ are constants depending on initial conditions  

**Velocity** is the derivative $u'(t)$.  
"""
    )

    steps = [
        BoardStep(
            latex_line=r"u(t)=a\cos(\omega t)+b\sin(\omega t)",
            teacher_explain_md=r"We differentiate with respect to $t$.",
        ),
        BoardStep(
            latex_line=r"u'(t)=a\frac{d}{dt}(\cos(\omega t))+b\frac{d}{dt}(\sin(\omega t))",
            teacher_explain_md=r"Differentiate each term separately (sum rule).",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dt}(\cos(\omega t))=-\sin(\omega t)\cdot \omega",
            teacher_explain_md=r"Chain rule: inside derivative is $\omega$.",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dt}(\sin(\omega t))=\cos(\omega t)\cdot \omega",
            teacher_explain_md=r"Again chain rule.",
        ),
        BoardStep(
            latex_line=r"u'(t)=-a\omega\sin(\omega t)+b\omega\cos(\omega t)",
            teacher_explain_md=r"Combine results. This is the velocity function.",
        ),
    ]
    render_simulation(steps, "Application — Velocity in a Spring–Mass Model")


def _section_graphs():
    st.markdown("## Visual understanding with graphs (teacher-level explanation)")

    # Graph 1: sin and cos
    st.markdown(r"### Graph 1 —  $y=\sin x$  and  $y'=\cos x$")
    x = np.linspace(-2 * math.pi, 2 * math.pi, 900)
    y = np.sin(x)
    yp = np.cos(x)
    _plot_pair(x, y, yp, r"Graph 1 — $y=\sin x$ and $y'=\cos x$", xlim=(-2*math.pi, 2*math.pi))
    _teacher_graph_explain_sin()

    st.divider()

    # Graph 2: sin(2x^3) and derivative
    st.markdown(r"### Graph 2 —  $y=\sin(2x^3)$  and  $y'=6x^2\cos(2x^3)$")
    x2 = np.linspace(-2.0, 2.0, 900)
    y2 = np.sin(2 * x2**3)
    yp2 = 6 * x2**2 * np.cos(2 * x2**3)
    _plot_pair(x2, y2, yp2, r"Graph 2 — $y=\sin(2x^3)$ and $y'=6x^2\cos(2x^3)$", xlim=(-2, 2))
    _teacher_graph_explain_chain_trig()

    st.divider()

    st.markdown("### Mini Simulation: How the derivative predicts the graph behavior")
    sim = [
        BoardStep(
            latex_line=r"y=\sin x \quad\Rightarrow\quad y'=\cos x",
            teacher_explain_md=r"Derivative is the slope function.",
        ),
        BoardStep(
            latex_line=r"\cos x>0 \Rightarrow \sin x \text{ increasing}",
            teacher_explain_md=r"If slope is positive, the curve rises.",
        ),
        BoardStep(
            latex_line=r"\cos x<0 \Rightarrow \sin x \text{ decreasing}",
            teacher_explain_md=r"If slope is negative, the curve falls.",
        ),
        BoardStep(
            latex_line=r"\cos x=0 \Rightarrow \text{horizontal tangent}",
            teacher_explain_md=r"Slope zero means the curve is momentarily flat.",
        ),
    ]
    render_simulation(sim, "Graph Simulation — Using y′ to predict the shape of y")


# ---------------------------
# PRACTICE (15+ questions)
# ---------------------------

def _latex_aligned_block(lines: list[str]) -> str:
    """
    Combine multiple LaTeX lines into ONE aligned block shown all at once.
    Each input line should be LaTeX (no $...$ wrappers).
    """
    safe_lines = [ln.strip() for ln in lines if ln and ln.strip()]
    body = r" \\ ".join(safe_lines)
    return r"\begin{aligned}" + body + r"\end{aligned}"


def _practice_block(qid: str, question_latex: str, hint_md: str, answer_steps_latex: list[str], answer_explain_md: str):
    st.markdown("---")
    st.markdown("### Practice question")
    st.latex(question_latex)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Hint", key=f"hint_{qid}"):
            st.info(hint_md)
    with col2:
        if st.button("Show answer", key=f"ans_{qid}"):
            st.markdown("**Full step-by-step solution (shown all at once):**")
            st.latex(_latex_aligned_block(answer_steps_latex))
            st.success(answer_explain_md)


def _practice():
    st.markdown("## Practice — Derivatives of Trigonometric Functions")
    st.markdown(
        r"""
Do these like an exam student:
1) Identify the rule(s): basic trig / chain / product / quotient  
2) Differentiate cleanly  
3) Simplify  
"""
    )

    _practice_block(
        "p1",
        r"\frac{d}{dx}(\sin x)",
        "Use the basic trig rule.",
        [r"\frac{d}{dx}(\sin x)=\cos x"],
        r"This is a fundamental result: $\frac{d}{dx}(\sin x)=\cos x$.",
    )

    _practice_block(
        "p2",
        r"\frac{d}{dx}(\cos x)",
        "Use the basic trig rule.",
        [r"\frac{d}{dx}(\cos x)=-\sin x"],
        r"Remember cosine differentiates to negative sine.",
    )

    _practice_block(
        "p3",
        r"\frac{d}{dx}(\tan x)",
        "Use the basic trig rule.",
        [r"\frac{d}{dx}(\tan x)=\sec^2 x"],
        r"This is a standard identity-based derivative.",
    )

    _practice_block(
        "p4",
        r"\frac{d}{dx}(\sec x)",
        "Use the basic trig rule for sec.",
        [r"\frac{d}{dx}(\sec x)=\sec x\tan x"],
        r"Sec derivative returns sec again times tan.",
    )

    _practice_block(
        "p5",
        r"\frac{d}{dx}\big(\sin(5x)\big)",
        "Chain rule: outside is sin, inside is 5x.",
        [
            r"y=\sin(5x)",
            r"y'=\cos(5x)\cdot 5",
            r"y'=5\cos(5x)",
        ],
        r"Chain rule multiplies by the derivative of the inside, which is $5$.",
    )

    _practice_block(
        "p6",
        r"\frac{d}{dx}\big(\cos(3x^2)\big)",
        "Chain rule: outside cos → -sin, inside 3x^2.",
        [
            r"y=\cos(3x^2)",
            r"y'=-\sin(3x^2)\cdot \frac{d}{dx}(3x^2)",
            r"y'=-\sin(3x^2)\cdot 6x",
            r"y'=-6x\sin(3x^2)",
        ],
        r"Derivative of inside $3x^2$ is $6x$.",
    )

    _practice_block(
        "p7",
        r"\frac{d}{dx}\big((\sin x)^4\big)",
        "Treat sin x as inside u, and u^4 outside.",
        [
            r"y=(\sin x)^4",
            r"u=\sin x\Rightarrow y=u^4",
            r"\frac{dy}{du}=4u^3",
            r"\frac{du}{dx}=\cos x",
            r"y'=4(\sin x)^3\cos x",
        ],
        r"Power rule + chain rule.",
    )

    _practice_block(
        "p8",
        r"\frac{d}{dx}\big(x^3\sin x\big)",
        "Product rule: u=x^3, v=sin x.",
        [
            r"y=x^3\sin x",
            r"y'=3x^2\sin x + x^3\cos x",
        ],
        r"Product rule: $(uv)'=u'v+uv'$.",
    )

    _practice_block(
        "p9",
        r"\frac{d}{dx}\left(\frac{\sin x}{x}\right)",
        "Quotient rule: (u/v)'=(u'v-uv')/v^2.",
        [
            r"y=\frac{\sin x}{x}",
            r"y'=\frac{(\cos x)\cdot x-(\sin x)\cdot 1}{x^2}",
            r"y'=\frac{x\cos x-\sin x}{x^2}",
        ],
        r"Careful: denominator becomes squared.",
    )

    _practice_block(
        "p10",
        r"\frac{d}{dx}\big(\tan(2x)\big)",
        "Outside derivative: sec^2(inside). Multiply by inside derivative 2.",
        [
            r"y=\tan(2x)",
            r"y'=\sec^2(2x)\cdot 2",
            r"y'=2\sec^2(2x)",
        ],
        r"Chain rule multiplier is $2$.",
    )

    _practice_block(
        "p11",
        r"\frac{d}{dx}\big(\sin(x^2+1)\big)",
        "Outside: sin → cos. Inside: x^2+1 → 2x.",
        [
            r"y=\sin(x^2+1)",
            r"y'=\cos(x^2+1)\cdot 2x",
            r"y'=2x\cos(x^2+1)",
        ],
        r"Chain rule is direct here.",
    )

    _practice_block(
        "p12",
        r"\frac{d}{dx}\big(\cos x\big)^3",
        "Same structure as in lesson: u=cos x, y=u^3.",
        [
            r"y=(\cos x)^3",
            r"u=\cos x\Rightarrow y=u^3",
            r"y'=3u^2\cdot(-\sin x)",
            r"y'=-3\sin x\cos^2 x",
        ],
        r"Do not forget the negative from $\frac{d}{dx}(\cos x)$.",
    )

    _practice_block(
        "p13",
        r"\text{Find the tangent line to }y=\sin x\text{ at }x=\frac{\pi}{3}",
        "Compute slope y'(a)=cos(a) and point y(a)=sin(a).",
        [
            r"y'=\cos x",
            r"m=\cos\left(\frac{\pi}{3}\right)=\frac12",
            r"y\left(\frac{\pi}{3}\right)=\sin\left(\frac{\pi}{3}\right)=\frac{\sqrt3}{2}",
            r"y-\frac{\sqrt3}{2}=\frac12\left(x-\frac{\pi}{3}\right)",
        ],
        r"Tangent line uses point–slope form.",
    )

    _practice_block(
        "p14",
        r"\text{Find }y''\text{ if }y=\cos x",
        "Differentiate twice.",
        [
            r"y=\cos x",
            r"y'=-\sin x",
            r"y''=-\cos x",
        ],
        r"Second derivative of $\cos x$ is $-\cos x$.",
    )

    _practice_block(
        "p15",
        r"\text{If }u(t)=a\cos(\omega t)+b\sin(\omega t),\text{ find }u'(t)",
        "Differentiate each term and multiply by inside derivative ω.",
        [
            r"u(t)=a\cos(\omega t)+b\sin(\omega t)",
            r"u'(t)=a\cdot(-\sin(\omega t))\cdot\omega + b\cdot(\cos(\omega t))\cdot\omega",
            r"u'(t)=-a\omega\sin(\omega t)+b\omega\cos(\omega t)",
        ],
        r"This is the velocity function in the spring–mass model.",
    )


# ---------------------------
# Main entry required by app.py
# ---------------------------

def render():
    """
    Required by app.py registry: subtopic module must expose render().
    """
    _section_objectives()

    learn_tab, practice_tab = st.tabs(["📘 Learn", "📝 Practice"])

    with learn_tab:
        _section_core_rules()
        st.divider()
        _section_rule_combos()
        st.divider()
        _section_tangent_normal()
        st.divider()
        _section_higher_order()
        st.divider()
        _section_application()
        st.divider()
        _section_graphs()

    with practice_tab:
        _practice()
