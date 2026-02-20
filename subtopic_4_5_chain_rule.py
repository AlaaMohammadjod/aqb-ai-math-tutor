# aqb-ai-math-tutor/subtopic_4_5_chain_rule.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

from simulations import BoardStep, render_simulation
import subtopic_4_5_chain_rule_practice as practice_module


# -----------------------------
# Helpers (LaTeX-first rendering)
# -----------------------------
def _step(latex_line: str, explain_md: str) -> BoardStep:
    """Create a BoardStep compatible with simulations.py."""
    return BoardStep(latex_line=latex_line, teacher_explain_md=explain_md)


def _note_box(title: str, body_md: str) -> None:
    # Student-facing coaching box (no teacher-only wording)
    st.markdown(
        f"""
<div style="border:1px solid #d9e6ff;border-left:6px solid #2563eb;border-radius:12px;padding:12px 14px;background:#f7fbff;margin:10px 0;">
  <div style="font-weight:800;color:#1d4ed8;margin-bottom:6px;">{title}</div>
  <div style="color:#111827;line-height:1.6;">{body_md}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _checkpoint_box(body_md: str) -> None:
    st.markdown(
        f"""
<div style="border:1px solid #dcfce7;border-left:6px solid #16a34a;border-radius:12px;padding:12px 14px;background:#f0fdf4;margin:10px 0;">
  <div style="font-weight:800;color:#166534;margin-bottom:6px;">Checkpoint</div>
  <div style="color:#052e16;line-height:1.6;">{body_md}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _small_fig():
    fig = plt.figure(figsize=(6.2, 3.4), dpi=140)
    ax = fig.add_subplot(111)
    ax.grid(True, alpha=0.25)
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.7)
    ax.axvline(0, color="black", linewidth=0.8, alpha=0.7)
    return fig, ax


def _exam_intro(title: str, question_latex: str, what_to_do_md: str) -> None:
    st.markdown(f"### {title}")
    st.markdown("**Question**")
    st.latex(question_latex)
    st.markdown("**What your answer should include**")
    st.markdown(what_to_do_md)


def _latex_point_to_float(latex_val: str) -> float:
    """Convert a very small set of LaTeX point labels into numeric values (no eval)."""
    mapping = {
        r"0": 0.0,
        r"\pi": math.pi,
        r"\frac{\pi}{6}": math.pi / 6,
        r"\frac{\pi}{4}": math.pi / 4,
        r"\frac{\pi}{3}": math.pi / 3,
        r"\frac{\pi}{2}": math.pi / 2,
    }
    if latex_val not in mapping:
        # Fallback: treat as 0 to avoid crashing; also show a clear LaTeX output for the student.
        return 0.0
    return mapping[latex_val]


# -----------------------------
# Objective sections
# -----------------------------
def _objective_451():
    st.subheader("Objective 4.5.1 — Chain rule (both notations)")

    _note_box(
        "Big idea",
        "When one function is **inside** another, you are differentiating a **composition**. "
        "The chain rule tells you how the outside change and the inside change multiply together.",
    )

    st.markdown("**The chain rule (two equivalent notations):**")
    st.latex(r"\bigl[f(g(x))\bigr]' = f'\!\bigl(g(x)\bigr)\cdot g'(x)")
    st.latex(r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}\qquad\text{(where }u=g(x)\text{)}")

    _note_box(
        "How to spot it fast",
        r"If you can point to an **inside expression** (call it $u$) that is not just $x$, you likely need the chain rule.",
    )

    st.markdown("### Visual: outside–inside mapping")
    steps = [
        _step(
            r"y=f(g(x))",
            r"Think of $g(x)$ as the **inside** and $f(\cdot)$ as the **outside**.",
        ),
        _step(
            r"u=g(x)",
            r"Rename the inside as $u$ so the structure is obvious.",
        ),
        _step(
            r"y=f(u)",
            r"Now you have a simple two-step process: $x\to u\to y$.",
        ),
        _step(
            r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}",
            r"Total rate of change equals (outside rate) $\times$ (inside rate).",
        ),
    ]
    render_simulation(steps, "Chain Rule — Structure (Obj 4.5.1)")

    _checkpoint_box(
        r"Before you differentiate, write the inside as $u$ and say out loud: "
        r"“Differentiate the outside in terms of $u$, then multiply by $u'$.”"
    )

    # Worked Example: Basic
    _exam_intro(
        "Worked Example 1 (basic)",
        r"y=\sqrt{5x^2+1}",
        "- Identify the outside function and the inside function.\n"
        "- Use the chain rule to find $\dfrac{dy}{dx}$.\n"
        "- Simplify your final answer.",
    )

    ex_steps = [
        _step(
            r"y=\sqrt{5x^2+1}=\bigl(5x^2+1\bigr)^{1/2}",
            "Rewrite the square root as a power so the derivative rule is clear.",
        ),
        _step(
            r"u=5x^2+1\qquad y=u^{1/2}",
            r"Outside is $u^{1/2}$ and inside is $u=5x^2+1$.",
        ),
        _step(
            r"\frac{dy}{du}=\frac{1}{2}u^{-1/2}=\frac{1}{2\sqrt{u}}",
            r"Differentiate the outside with respect to $u$.",
        ),
        _step(
            r"\frac{du}{dx}=10x",
            "Differentiate the inside.",
        ),
        _step(
            r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}=\frac{1}{2\sqrt{5x^2+1}}\cdot 10x",
            "Multiply outside derivative by inside derivative.",
        ),
        _step(
            r"\frac{dy}{dx}=\frac{5x}{\sqrt{5x^2+1}}",
            "Simplify.",
        ),
    ]
    render_simulation(ex_steps, "Worked Example 1 — Chain Rule (Obj 4.5.1)")

    # Worked Example: Medium
    _exam_intro(
        "Worked Example 2 (medium)",
        r"y=\bigl(2x-3\bigr)^{7}",
        "- Differentiate using the chain rule.\n"
        "- Simplify your final answer.",
    )

    ex2_steps = [
        _step(r"y=(2x-3)^7", "This is a power applied to a linear inside function."),
        _step(r"u=2x-3\qquad y=u^7", r"Outside is $u^7$, inside is $u=2x-3$."),
        _step(r"\frac{dy}{du}=7u^6", "Differentiate the outside."),
        _step(r"\frac{du}{dx}=2", "Differentiate the inside."),
        _step(r"\frac{dy}{dx}=7(2x-3)^6\cdot 2", "Multiply."),
        _step(r"\frac{dy}{dx}=14(2x-3)^6", "Simplify."),
    ]
    render_simulation(ex2_steps, "Worked Example 2 — Chain Rule (Obj 4.5.1)")

    # Exam-style Challenge
    _exam_intro(
        "Exam-Style Challenge (composition inside a trig function)",
        r"y=\sin\bigl((x^2+1)^3\bigr)",
        "- Clearly identify the inside function $u$.\n"
        "- Find $\dfrac{dy}{dx}$ and keep your final answer fully in terms of $x$.\n"
        "- Make sure your final derivative shows the two factors: outside derivative $\times$ inside derivative.",
    )

    ch_steps = [
        _step(
            r"y=\sin\bigl((x^2+1)^3\bigr)",
            r"Outside is $\sin(\cdot)$ and inside is $(x^2+1)^3$.",
        ),
        _step(
            r"u=(x^2+1)^3\qquad y=\sin(u)",
            r"Name the inside expression $u$.",
        ),
        _step(
            r"\frac{dy}{du}=\cos(u)",
            r"Derivative of $\sin(u)$ is $\cos(u)$.",
        ),
        _step(
            r"\frac{du}{dx}=3(x^2+1)^2\cdot 2x",
            r"Differentiate $u=(x^2+1)^3$ using the chain rule again.",
        ),
        _step(
            r"\frac{du}{dx}=6x(x^2+1)^2",
            "Simplify the inside derivative.",
        ),
        _step(
            r"\frac{dy}{dx}=\cos\bigl((x^2+1)^3\bigr)\cdot 6x(x^2+1)^2",
            "Multiply the factors and write the answer in terms of $x$.",
        ),
    ]
    render_simulation(ch_steps, "Exam-Style Challenge — Chain Rule (Obj 4.5.1)")


def _objective_452():
    st.subheader("Objective 4.5.2 — General power rule shortcut")

    _note_box(
        "Shortcut you should memorize",
        r"When you see a constant times a power of an inside function, use this fast form:",
    )
    st.latex(r"\frac{d}{dx}\Bigl(a\cdot\bigl(u(x)\bigr)^n\Bigr)=a\cdot n\cdot\bigl(u(x)\bigr)^{n-1}\cdot u'(x)")

    _checkpoint_box(
        r"Treat $u(x)$ as one chunk. Apply the power rule to $u^n$, then multiply by $u'(x)$."
    )

    _exam_intro(
        "Worked Example 1 (basic)",
        r"y=3(1-4x)^5",
        "- Use the shortcut form.\n"
        "- Show the inside derivative $\dfrac{d}{dx}(1-4x)$.\n"
        "- Simplify the final answer.",
    )
    steps = [
        _step(r"y=3(1-4x)^5", "Identify the constant, the power, and the inside."),
        _step(r"a=3,\; n=5,\; u=1-4x", "Match the expression to the shortcut form."),
        _step(r"\frac{dy}{dx}=3\cdot 5\cdot (1-4x)^{4}\cdot \frac{d}{dx}(1-4x)", "Apply the shortcut."),
        _step(r"\frac{d}{dx}(1-4x)=-4", "Differentiate the inside."),
        _step(r"\frac{dy}{dx}=3\cdot 5\cdot (1-4x)^4\cdot (-4)", "Multiply."),
        _step(r"\frac{dy}{dx}=-60(1-4x)^4", "Simplify."),
    ]
    render_simulation(steps, "General Power Rule — Worked Example 1 (Obj 4.5.2)")

    _exam_intro(
        "Worked Example 2 (medium)",
        r"y=\frac{4}{\bigl(2x+1\bigr)^3}",
        "- Rewrite as a power of the inside function.\n"
        "- Differentiate using the power-rule shortcut.\n"
        "- Simplify the final derivative.",
    )
    steps2 = [
        _step(r"y=\frac{4}{(2x+1)^3}=4(2x+1)^{-3}", "Rewrite the quotient as a negative power."),
        _step(r"u=2x+1\qquad y=4u^{-3}", "Outside is $4u^{-3}$, inside is $u=2x+1$."),
        _step(r"\frac{dy}{du}=4\cdot (-3)u^{-4}", "Differentiate the outside with respect to $u$."),
        _step(r"\frac{du}{dx}=2", "Differentiate the inside."),
        _step(r"\frac{dy}{dx}=-12(2x+1)^{-4}\cdot 2", "Multiply."),
        _step(r"\frac{dy}{dx}=-24(2x+1)^{-4}", "Simplify."),
        _step(r"\frac{dy}{dx}=-\frac{24}{(2x+1)^4}", "Rewrite with positive powers if you prefer."),
    ]
    render_simulation(steps2, "General Power Rule — Worked Example 2 (Obj 4.5.2)")

    _exam_intro(
        "Exam-Style Challenge (power + square root)",
        r"y=\bigl(1+\sqrt{x}\bigr)^6",
        "- Let $u=1+\sqrt{x}$.\n"
        "- Differentiate carefully (you will use the chain rule twice).\n"
        "- Simplify your final answer using exponents (no decimals).",
    )
    steps3 = [
        _step(r"y=(1+\sqrt{x})^6", r"Outside is $(\cdot)^6$ and inside is $1+\sqrt{x}$."),
        _step(r"u=1+\sqrt{x}\qquad y=u^6", "Name the inside $u$."),
        _step(r"\frac{dy}{du}=6u^5", "Differentiate the outside."),
        _step(r"\frac{du}{dx}=\frac{d}{dx}\bigl(1+x^{1/2}\bigr)=\frac{1}{2}x^{-1/2}", "Differentiate the inside."),
        _step(r"\frac{du}{dx}=\frac{1}{2\sqrt{x}}", "Rewrite in radical form."),
        _step(r"\frac{dy}{dx}=6(1+\sqrt{x})^5\cdot\frac{1}{2\sqrt{x}}", "Multiply."),
        _step(r"\frac{dy}{dx}=\frac{3(1+\sqrt{x})^5}{\sqrt{x}}", "Simplify."),
    ]
    render_simulation(steps3, "General Power Rule — Exam Challenge (Obj 4.5.2)")


def _objective_453():
    st.subheader("Objective 4.5.3 — Different function types with the chain rule")

    _note_box(
        "Most common chain-rule patterns",
        r"These come up constantly. In each one, $u=u(x)$ is an inside expression.",
    )

    st.markdown("**Core derivatives with an inside function $u(x)$:**")
    st.latex(r"\frac{d}{dx}\bigl(\sin(u)\bigr)=\cos(u)\,u'(x)")
    st.latex(r"\frac{d}{dx}\bigl(\cos(u)\bigr)=-\sin(u)\,u'(x)")
    st.latex(r"\frac{d}{dx}\bigl(e^{u}\bigr)=e^{u}\,u'(x)")
    st.latex(r"\frac{d}{dx}\bigl(\ln(u)\bigr)=\frac{1}{u}\,u'(x)")
    st.latex(r"\frac{d}{dx}\bigl(u^n\bigr)=n\,u^{n-1}\,u'(x)")

    _checkpoint_box(
        r"If you forget the chain rule, your derivative often looks “too small” because it is missing the factor $u'(x)$."
    )

    _exam_intro(
        "Worked Example 1 (trig + evaluation)",
        r"y=\sin(3x)\qquad\text{Find }y'\!\left(\frac{\pi}{6}\right).",
        "- Differentiate using the chain rule.\n"
        "- Substitute $x=\dfrac{\pi}{6}$.\n"
        "- Use exact trig values (keep $\pi$).",
    )

    steps = [
        _step(r"y=\sin(3x)", r"Outside is $\sin$, inside is $3x$."),
        _step(r"y'=\cos(3x)\cdot \frac{d}{dx}(3x)", "Differentiate the outside and multiply by the derivative of the inside."),
        _step(r"y'=3\cos(3x)", "Simplify."),
        _step(r"y'\!\left(\frac{\pi}{6}\right)=3\cos\!\left(3\cdot\frac{\pi}{6}\right)", "Substitute the point."),
        _step(r"y'\!\left(\frac{\pi}{6}\right)=3\cos\!\left(\frac{\pi}{2}\right)=0", "Evaluate using exact trig values."),
    ]
    render_simulation(steps, "Worked Example 1 — Trig + Chain Rule (Obj 4.5.3)")

    _exam_intro(
        "Worked Example 2 (log)",
        r"y=\ln(2x^2+5)",
        "- Differentiate using the chain rule.\n"
        "- Simplify your final answer into a single fraction.",
    )

    steps2 = [
        _step(r"y=\ln(2x^2+5)", r"Outside is $\ln$, inside is $2x^2+5$."),
        _step(r"y'=\frac{1}{2x^2+5}\cdot \frac{d}{dx}(2x^2+5)", r"Derivative of $\ln(u)$ is $\frac{1}{u}$, then multiply by $u'(x)$."),
        _step(r"\frac{d}{dx}(2x^2+5)=4x", "Differentiate the inside."),
        _step(r"y'=\frac{4x}{2x^2+5}", "Simplify."),
    ]
    render_simulation(steps2, "Worked Example 2 — Log + Chain Rule (Obj 4.5.3)")

    _exam_intro(
        "Exam-Style Challenge (exponential + product rule)",
        r"y=x^2\,e^{x^3}",
        "- Find $\dfrac{dy}{dx}$.\n"
        "- Your work must show both: the product rule and the chain rule.\n"
        "- Simplify your final answer by factoring when possible.",
    )

    steps3 = [
        _step(r"y=x^2\,e^{x^3}", r"This is a product: $x^2$ times $e^{x^3}$."),
        _step(r"\frac{dy}{dx}=\frac{d}{dx}(x^2)\cdot e^{x^3}+x^2\cdot\frac{d}{dx}\bigl(e^{x^3}\bigr)", "Apply the product rule."),
        _step(r"\frac{d}{dx}(x^2)=2x", "Differentiate the first factor."),
        _step(r"\frac{d}{dx}\bigl(e^{x^3}\bigr)=e^{x^3}\cdot\frac{d}{dx}(x^3)", "Chain rule for the exponential."),
        _step(r"\frac{d}{dx}(x^3)=3x^2", "Differentiate the inside."),
        _step(r"\frac{dy}{dx}=2x\,e^{x^3}+x^2\cdot e^{x^3}\cdot 3x^2", "Substitute derivatives."),
        _step(r"\frac{dy}{dx}=2x\,e^{x^3}+3x^4e^{x^3}", "Simplify."),
        _step(r"\frac{dy}{dx}=x\,e^{x^3}\bigl(2+3x^3\bigr)", "Factor a common term."),
    ]
    render_simulation(steps3, "Exam-Style Challenge — Mixed Rules (Obj 4.5.3)")


def _objective_454():
    st.subheader("Objective 4.5.4 — Equations of tangent lines using the chain rule")

    _note_box(
        "Tangent-line formula",
        r"At $x=a$, the tangent line is the line through the point $(a,f(a))$ with slope $f'(a)$.",
    )
    st.latex(r"y_{\text{tan}}(x)=f(a)+f'(a)\,(x-a)")

    _checkpoint_box(
        r"Order matters: compute $f(a)$, then compute $f'(x)$, then compute $f'(a)$, then substitute into the formula."
    )

    _exam_intro(
        "Worked Example 1 (exact trig values)",
        r"y=\cos(2x)\qquad\text{Find the tangent line at }x=\frac{\pi}{4}.",
        "- Find the point on the curve at $x=\dfrac{\pi}{4}$.\n"
        "- Find the slope using $y'$, then write $y_{\text{tan}}(x)$.\n"
        "- Keep answers in terms of $\pi$.",
    )

    steps = [
        _step(r"a=\frac{\pi}{4}", "The tangent point is at $x=a$."),
        _step(r"f(a)=\cos\!\left(2\cdot\frac{\pi}{4}\right)=\cos\!\left(\frac{\pi}{2}\right)=0", "Compute the $y$-value."),
        _step(r"y'=-\sin(2x)\cdot 2=-2\sin(2x)", "Differentiate using the chain rule."),
        _step(r"f'(a)=-2\sin\!\left(\frac{\pi}{2}\right)=-2", "Compute the slope at the point."),
        _step(r"y_{\text{tan}}(x)=0+(-2)\left(x-\frac{\pi}{4}\right)", "Substitute into the tangent-line formula."),
        _step(r"y_{\text{tan}}(x)=-2x+\frac{\pi}{2}", "Simplify."),
    ]
    render_simulation(steps, "Worked Example 1 — Tangent Line (Obj 4.5.4)")

    _exam_intro(
        "Worked Example 2 (medium)",
        r"y=\sqrt{x+4}\qquad\text{Find the tangent line at }x=5.",
        "- Compute $f(5)$.\n"
        "- Find $f'(x)$ using the chain rule.\n"
        "- Evaluate $f'(5)$ and write the tangent line equation.",
    )
    steps2 = [
        _step(r"f(5)=\sqrt{5+4}=3", "Compute the point on the curve."),
        _step(r"y=\sqrt{x+4}=(x+4)^{1/2}", "Rewrite as a power."),
        _step(r"y'=\frac{1}{2}(x+4)^{-1/2}\cdot \frac{d}{dx}(x+4)", "Differentiate using the chain rule."),
        _step(r"\frac{d}{dx}(x+4)=1", "Inside derivative."),
        _step(r"y'=\frac{1}{2\sqrt{x+4}}", "Simplify."),
        _step(r"f'(5)=\frac{1}{2\sqrt{9}}=\frac{1}{6}", "Slope at $x=5$."),
        _step(r"y_{\text{tan}}(x)=3+\frac{1}{6}(x-5)", "Tangent-line equation."),
        _step(r"y_{\text{tan}}(x)=\frac{1}{6}x+\frac{13}{6}", "Simplify."),
    ]
    render_simulation(steps2, "Worked Example 2 — Tangent Line (Obj 4.5.4)")

    st.markdown("### Visual check")
    st.markdown(
        "Choose a labeled point, then compare the curve with its tangent line at that point. "
        "Your goal is to **see** that the dashed line touches the curve and has slope $f'(a)$."
    )

    # IMPORTANT: no LaTeX inside widget options (Streamlit cannot render KaTeX there)
    options = [
        ("Point A", r"0"),
        ("Point B", r"\frac{\pi}{6}"),
        ("Point C", r"\frac{\pi}{4}"),
        ("Point D", r"\frac{\pi}{3}"),
    ]
    label = st.radio("Choose a point label", [o[0] for o in options], horizontal=True, key="cr_454_pt_label")
    x_latex = dict(options)[label]
    st.latex(r"a=" + x_latex)

    x0 = _latex_point_to_float(x_latex)
    xs = np.linspace(x0 - 1.2, x0 + 1.2, 300)
    ys = np.cos(2 * xs)
    m = -2 * np.sin(2 * x0)
    y0 = np.cos(2 * x0)
    yt = y0 + m * (xs - x0)

    fig, ax = _small_fig()
    ax.plot(xs, ys, linewidth=2, label="curve")
    ax.plot(xs, yt, linewidth=2, linestyle="--", label="tangent")
    ax.scatter([x0], [y0], s=40)
    ax.set_title("Curve and tangent line")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc="upper right")
    st.pyplot(fig, use_container_width=True)


def _objective_455():
    st.subheader("Objective 4.5.5 — Derivative at a point (slope from a graph)")

    _note_box(
        "Meaning of the derivative",
        r"The derivative at $x=a$ is the slope of the tangent line at that point.",
    )
    st.latex(r"f'(a)=\text{slope of the tangent line to }y=f(x)\text{ at }x=a")

    _exam_intro(
        "Worked Example 1",
        r"y=\sin(3x)\qquad\text{Find }y'\!\left(\frac{\pi}{6}\right).",
        "- Compute the derivative.\n"
        "- Evaluate it at $x=\dfrac{\pi}{6}$.\n"
        "- Use the graph to confirm the tangent slope.",
    )

    steps = [
        _step(r"y=\sin(3x)\Rightarrow y'=3\cos(3x)", "Differentiate using the chain rule."),
        _step(r"y'\!\left(\frac{\pi}{6}\right)=3\cos\!\left(\frac{\pi}{2}\right)=0", "Evaluate exactly."),
        _step(r"\text{A slope of }0\text{ means the tangent line is horizontal.}", "So you should see a flat dashed line on the graph."),
    ]
    render_simulation(steps, "Worked Example 1 — Slope From Graph (Obj 4.5.5)")

    st.markdown("### Graph simulation")
    st.markdown(
        "Pick a point label. The app draws the curve and the tangent line at $x=a$. "
        "Read the slope from the formula and see it match the dashed line."
    )

    pts = [
        ("Point A", r"0"),
        ("Point B", r"\frac{\pi}{6}"),
        ("Point C", r"\frac{\pi}{3}"),
        ("Point D", r"\frac{\pi}{2}"),
    ]
    lab = st.radio("Choose a point label", [p[0] for p in pts], horizontal=True, key="cr_455_pt_label")
    a_latex = dict(pts)[lab]
    st.latex(r"a=" + a_latex)

    a = _latex_point_to_float(a_latex)
    xs = np.linspace(a - 1.1, a + 1.1, 350)
    f = np.sin(3 * xs)
    m = 3 * np.cos(3 * a)
    ya = np.sin(3 * a)
    tan = ya + m * (xs - a)

    fig, ax = _small_fig()
    ax.plot(xs, f, linewidth=2, label="curve")
    ax.plot(xs, tan, linewidth=2, linestyle="--", label="tangent")
    ax.scatter([a], [ya], s=40)
    ax.set_title(r"$y=\sin(3x)$ and its tangent at $x=a$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc="upper right")
    st.pyplot(fig, use_container_width=True)

    st.markdown("Slope at your chosen point:")
    st.latex(r"y'(a)=3\cos(3a)")

    _exam_intro(
        "Exam-Style Challenge (graph + chain rule)",
        r"y=(x^2+1)^3\qquad\text{Find the slope of the tangent line at }x=1.",
        "- Compute $y'$ using the chain rule.\n"
        "- Evaluate $y'(1)$.\n"
        "- Use the graph below to confirm the tangent slope visually.",
    )

    steps2 = [
        _step(r"y=(x^2+1)^3", r"Inside is $x^2+1$, outside is $(\cdot)^3$."),
        _step(r"y'=3(x^2+1)^2\cdot 2x", "Chain rule."),
        _step(r"y'=6x(x^2+1)^2", "Simplify."),
        _step(r"y'(1)=6\cdot 1\cdot (1^2+1)^2=6\cdot 4=24", "Evaluate at $x=1$."),
    ]
    render_simulation(steps2, "Exam-Style Challenge — Slope From Graph (Obj 4.5.5)")

    x0 = 1.0
    xs2 = np.linspace(x0 - 1.2, x0 + 1.2, 350)
    y2 = (xs2**2 + 1) ** 3
    m2 = 6 * x0 * (x0**2 + 1) ** 2
    y0 = (x0**2 + 1) ** 3
    tan2 = y0 + m2 * (xs2 - x0)

    fig2, ax2 = _small_fig()
    ax2.plot(xs2, y2, linewidth=2, label="curve")
    ax2.plot(xs2, tan2, linewidth=2, linestyle="--", label="tangent")
    ax2.scatter([x0], [y0], s=40)
    ax2.set_title(r"$y=(x^2+1)^3$ and its tangent at $x=1$")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.legend(loc="upper left")
    st.pyplot(fig2, use_container_width=True)


def _objective_456():
    st.subheader("Objective 4.5.6 — Higher-order derivatives")

    _note_box(
        "What “higher-order” means",
        r"You can differentiate more than once: first derivative $y'$, second derivative $y''$, third derivative $y^{(3)}$, and so on.",
    )
    st.latex(r"y',\; y'',\; y^{(3)},\;\dots")

    _checkpoint_box(
        r"Every time the inside is not just $x$, use the chain rule. On the second derivative, you might also need the product rule."
    )

    _exam_intro(
        "Worked Example 1 (first and second derivative)",
        r"y=(x^2+1)^5\qquad\text{Find }y'\text{ and }y''.",
        "- Use the chain rule to find $y'$.\n"
        "- Differentiate again to find $y''$ (use the product rule if needed).\n"
        "- Simplify (factoring is a good final step).",
    )

    steps = [
        _step(r"y=(x^2+1)^5", "First derivative: apply the chain rule."),
        _step(r"y'=5(x^2+1)^4\cdot 2x", "Outside derivative times inside derivative."),
        _step(r"y'=10x(x^2+1)^4", "Simplify."),
        _step(r"y''=\frac{d}{dx}\Bigl(10x(x^2+1)^4\Bigr)", "Second derivative: product rule."),
        _step(r"y''=10(x^2+1)^4+10x\cdot 4(x^2+1)^3\cdot 2x", "Product rule + chain rule."),
        _step(r"y''=10(x^2+1)^4+80x^2(x^2+1)^3", "Simplify."),
        _step(r"y''=10(x^2+1)^3(9x^2+1)", "Factor and finish."),
    ]
    render_simulation(steps, "Worked Example 1 — Higher Derivatives (Obj 4.5.6)")

    _exam_intro(
        "Exam-Style Challenge (trig higher derivatives)",
        r"y=\sin(2x)\qquad\text{Find }y'\text{ and }y''.",
        "- Use the chain rule to find $y'$.\n"
        "- Differentiate again to find $y''$.\n"
        "- Keep exact trig functions (no decimals).",
    )

    steps2 = [
        _step(r"y=\sin(2x)", r"Outside is $\sin$, inside is $2x$."),
        _step(r"y'=\cos(2x)\cdot 2", "Chain rule."),
        _step(r"y'=2\cos(2x)", "Simplify."),
        _step(r"y''=\frac{d}{dx}\bigl(2\cos(2x)\bigr)", "Differentiate again."),
        _step(r"y''=2\cdot\bigl(-\sin(2x)\cdot 2\bigr)", "Chain rule again."),
        _step(r"y''=-4\sin(2x)", "Simplify."),
    ]
    render_simulation(steps2, "Exam-Style Challenge — Higher Derivatives (Obj 4.5.6)")


def _objective_457():
    st.subheader("Objective 4.5.7 — Derivative of an inverse function")

    _note_box(
        "Key formula",
        r"If $f$ is one-to-one and differentiable, then for an input value $a$:",
    )
    st.latex(r"\Bigl(f^{-1}\Bigr)'(a)=\frac{1}{f'\!\bigl(f^{-1}(a)\bigr)}")

    _checkpoint_box(
        r"Two steps: (1) solve $f(x)=a$ to find $f^{-1}(a)$, then (2) compute $f'(x)$ and substitute into the formula."
    )

    _exam_intro(
        "Worked Example 1 (basic)",
        r"f(x)=x^3+1\qquad\text{Find }\Bigl(f^{-1}\Bigr)'(2).",
        "- Find $f^{-1}(2)$ by solving $f(x)=2$.\n"
        "- Compute $f'(x)$.\n"
        "- Substitute into $\bigl(f^{-1}\bigr)'(2)=\dfrac{1}{f'(f^{-1}(2))}$.",
    )

    steps = [
        _step(r"\Bigl(f^{-1}\Bigr)'(2)=\frac{1}{f'\!\bigl(f^{-1}(2)\bigr)}", "Start with the formula."),
        _step(r"f^{-1}(2)=x\Longleftrightarrow x^3+1=2", "Solve $f(x)=2$."),
        _step(r"x^3=1\Longrightarrow x=1", "So $f^{-1}(2)=1$."),
        _step(r"f'(x)=3x^2", "Differentiate $f(x)$."),
        _step(r"f'\!\bigl(f^{-1}(2)\bigr)=f'(1)=3", "Evaluate at $x=1$."),
        _step(r"\Bigl(f^{-1}\Bigr)'(2)=\frac{1}{3}", "Final answer."),
    ]
    render_simulation(steps, "Worked Example 1 — Inverse Derivative (Obj 4.5.7)")

    _exam_intro(
        "Exam-Style Challenge (log inverse)",
        r"f(x)=\ln(x-1)\quad(x>1)\qquad\text{Find }\Bigl(f^{-1}\Bigr)'(0).",
        "- First, solve $\ln(x-1)=0$ to find $f^{-1}(0)$.\n"
        "- Then compute $f'(x)$.\n"
        "- Substitute into the inverse-derivative formula and simplify.",
    )

    steps2 = [
        _step(r"\Bigl(f^{-1}\Bigr)'(0)=\frac{1}{f'\!\bigl(f^{-1}(0)\bigr)}", "Use the formula."),
        _step(r"f^{-1}(0)=x\Longleftrightarrow \ln(x-1)=0", "Solve $f(x)=0$."),
        _step(r"x-1=e^{0}=1\Longrightarrow x=2", "So $f^{-1}(0)=2$."),
        _step(r"f'(x)=\frac{1}{x-1}", r"Derivative of $\ln(x-1)$ is $\frac{1}{x-1}\cdot 1$."),
        _step(r"f'\!\bigl(f^{-1}(0)\bigr)=f'(2)=\frac{1}{1}=1", "Evaluate at $x=2$."),
        _step(r"\Bigl(f^{-1}\Bigr)'(0)=\frac{1}{1}=1", "Final answer."),
    ]
    render_simulation(steps2, "Exam-Style Challenge — Inverse Derivative (Obj 4.5.7)")


# -----------------------------
# Public entry point
# -----------------------------
def render():
    st.title("Subtopic 4.5: The Chain Rule")
    st.caption("Term: Term 2 • Topic: Topic 4: Differentiation (Cont’d)")

    learn_tab, practice_tab = st.tabs(["Learn", "Practice"])

    with learn_tab:
        st.markdown("### Learning objectives")
        st.markdown("- 4.5.1 Define and understand the chain rule in both notations.")
        st.markdown("- 4.5.2 Use the chain rule as the general power-rule shortcut.")
        st.markdown("- 4.5.3 Differentiate common function types using the chain rule (and with other rules when needed).")
        st.markdown("- 4.5.4 Find equations of tangent lines using the chain rule.")
        st.markdown("- 4.5.5 Find the derivative at a point given a graph.")
        st.markdown("- 4.5.6 Find higher-order derivatives.")
        st.markdown("- 4.5.7 Compute the derivative of an inverse function.")

        st.divider()
        _objective_451()
        st.divider()
        _objective_452()
        st.divider()
        _objective_453()
        st.divider()
        _objective_454()
        st.divider()
        _objective_455()
        st.divider()
        _objective_456()
        st.divider()
        _objective_457()

    with practice_tab:
        practice_module.render()