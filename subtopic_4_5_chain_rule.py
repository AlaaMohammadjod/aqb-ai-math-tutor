import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation
from subtopic_4_5_chain_rule_practice import render_practice


# ----------------------------
# Graph helpers (clear + sized)
# ----------------------------
def _plot_with_tangent(ax, x, y, x0, y0, m, title):
    tangent = y0 + m * (x - x0)
    ax.plot(x, y, label="y")
    ax.plot(x, tangent, linestyle="--", label="tangent at x=a")
    ax.scatter([x0], [y0], s=55, zorder=5)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    ax.legend()


def _graph_polynomial_chain():
    st.markdown("### Graph A — Why chain rule creates big slopes")
    st.markdown(
        "**Teacher explanation (simple words):**  \n"
        "- When you have a power like $(3x^2+1)^5$, the slope becomes large because:  \n"
        "  1) the outside power derivative creates a big factor, and  \n"
        "  2) the inside derivative multiplies it (chain rule)."
    )
    st.latex(r"y=(3x^2+1)^5")
    st.latex(r"y' = 5(3x^2+1)^4 \cdot 6x = 30x(3x^2+1)^4")

    x = np.linspace(-1.2, 1.2, 900)
    y = (3 * x**2 + 1) ** 5
    yp = 30 * x * (3 * x**2 + 1) ** 4

    fig = plt.figure(figsize=(11.5, 5.4))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label="y")
    ax.plot(x, yp, label="y'")
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_title(r"$y=(3x^2+1)^5$ and $y'=30x(3x^2+1)^4$")
    ax.grid(True, alpha=0.25)
    ax.legend()
    st.pyplot(fig, use_container_width=True)

    st.markdown(
        "**How to read this (teacher guide):**  \n"
        "- Where $y'$ is large positive → the function rises steeply.  \n"
        "- Where $y'$ is large negative → the function falls steeply.  \n"
        "- Where $y'=0$ → the curve is flat (horizontal tangent).  \n"
        "- Chain rule explains *why* the derivative becomes huge: the inside derivative multiplies the outside derivative."
    )


def _graph_explorer_sin():
    st.markdown("### Graph B (Interactive) — Tangent slope for $y=\\sin(2x^3)$")
    st.markdown(
        "**Goal:** You will *see* that the derivative is the slope of the tangent line, and that chain rule makes slope larger away from 0."
    )
    st.latex(r"y=\sin(2x^3)")
    st.latex(r"y' = 6x^2\cos(2x^3)")

    x0 = st.slider("Choose the point $x=a$:", -2.0, 2.0, 0.6, 0.05)

    x = np.linspace(-2.0, 2.0, 1400)
    y = np.sin(2 * x**3)
    y0 = float(np.sin(2 * x0**3))
    m = float(6 * x0**2 * np.cos(2 * x0**3))

    fig = plt.figure(figsize=(11.5, 5.4))
    ax = fig.add_subplot(111)
    _plot_with_tangent(
        ax,
        x,
        y,
        x0,
        y0,
        m,
        r"Tangent line on $y=\sin(2x^3)$ at $x=a$ (slope = $y'(a)$)",
    )
    st.pyplot(fig, use_container_width=True)

    st.markdown("**Teacher explanation (very friendly):**")
    st.markdown(
        "- The dot is your point $(a, y(a))$.  \n"
        "- The dashed line is the tangent line — this is the line that touches the curve and shows how steep it is *right now*.  \n"
        "- The slope of the tangent is exactly the derivative value $y'(a)$.  \n"
        "- Notice: the factor $6x^2$ grows when $|x|$ grows → slopes can get larger away from 0. That is chain rule in action."
    )
    st.latex(r"(a, y(a)) = (%.2f, \sin(2(%.2f)^3))" % (x0, x0))
    st.latex(r"y'(a)=6a^2\cos(2a^3)\approx %.3f" % m)


def _graph_explorer_exp_sign():
    st.markdown("### Graph C (Interactive) — Increasing / decreasing for $y=e^{x^2-4x}$")
    st.markdown(
        "**Goal:** Understand that the sign of the derivative tells you whether the curve goes up or down."
    )
    st.latex(r"y=e^{x^2-4x}")
    st.latex(r"y'=(2x-4)e^{x^2-4x}")

    x0 = st.slider("Choose the point $x=a$:", -1.0, 4.0, 1.0, 0.05)

    x = np.linspace(-1.0, 4.0, 1400)

    # SAFE python: ** for powers, * for multiplication
    expo = x**2 - 4 * x
    y = np.exp(expo)
    yp = (2 * x - 4) * np.exp(expo)

    y0 = float(np.exp(x0**2 - 4 * x0))
    m = float((2 * x0 - 4) * np.exp(x0**2 - 4 * x0))

    fig = plt.figure(figsize=(11.5, 5.4))
    ax = fig.add_subplot(111)
    ax.plot(x, y, label="y")
    ax.plot(x, yp, label="y'")
    ax.axvline(2, linestyle=":", linewidth=2, label="x=2 (slope=0)")
    ax.scatter([x0], [y0], s=55, zorder=5)
    ax.axhline(0, linewidth=1)
    ax.set_title(r"$y=e^{x^2-4x}$ and $y'=(2x-4)e^{x^2-4x}$")
    ax.grid(True, alpha=0.25)
    ax.legend()
    st.pyplot(fig, use_container_width=True)

    st.markdown("**Teacher explanation (simple and powerful):**")
    st.markdown(
        "- The exponential part $e^{x^2-4x}$ is always **positive**.  \n"
        "- So the sign of $y'$ comes from $(2x-4)$:  \n"
        "  - if $x<2$ → $(2x-4)<0$ → derivative negative → curve goes **down**  \n"
        "  - if $x>2$ → $(2x-4)>0$ → derivative positive → curve goes **up**  \n"
        "  - at $x=2$ → derivative is 0 → curve is **flat** there (horizontal tangent)"
    )
    st.latex(r"y'(a)\approx %.3f" % m)


# ----------------------------
# Objective simulations
# ----------------------------
def _sim_tangent_line_objective_4554():
    st.markdown("### Objective 4.5.4 — Tangent line using chain rule (FULL simulation)")
    st.markdown(
        "**We will find the tangent line to** $y=(3x^2+1)^5$ **at** $x=1$."
    )

    steps = [
        BoardStep(r"y=(3x^2+1)^5", r"We want a tangent line at \(x=1\). We need slope \(y'(1)\) and point \((1,y(1))\)."),
        BoardStep(r"y' = 30x(3x^2+1)^4", r"Differentiate using chain rule (from Example A). This gives the slope function."),
        BoardStep(r"y(1)=(3\cdot 1^2+1)^5 = 4^5 = 1024", r"Substitute \(x=1\) to get the point on the curve."),
        BoardStep(r"y'(1)=30(1)(3\cdot 1^2+1)^4 = 30\cdot 4^4 = 30\cdot 256 = 7680", r"Substitute \(x=1\) in the derivative to get the slope."),
        BoardStep(r"y-y_1=m(x-x_1)", r"Use point-slope form for the tangent line."),
        BoardStep(r"y-1024 = 7680(x-1)", r"Final tangent line equation."),
    ]
    render_simulation(steps, "Tangent Line — Pen Writing (Objective 4.5.4)")


def _sim_derivative_from_graph_objective_4555():
    st.markdown("### Objective 4.5.5 — Derivative at a point from a graph (slope meaning)")

    st.markdown(
        "Teacher idea: **The derivative at a point is the slope of the tangent line at that point.**"
    )
    st.latex(r"y'(a)=\text{slope of tangent line at }x=a")

    st.markdown("Pick a point. The tangent slope shown is exactly the derivative value.")

    x0 = st.slider("Choose a point for this objective:", -2.0, 2.0, 0.5, 0.05, key="obj4555")

    x = np.linspace(-2.0, 2.0, 1400)
    y = np.sin(2 * x**3)
    y0 = float(np.sin(2 * x0**3))
    m = float(6 * x0**2 * np.cos(2 * x0**3))

    fig = plt.figure(figsize=(11.5, 5.4))
    ax = fig.add_subplot(111)
    _plot_with_tangent(ax, x, y, x0, y0, m, r"Tangent slope = derivative value")
    st.pyplot(fig, use_container_width=True)

    st.markdown("**Teacher explanation (very simple):**")
    st.markdown(
        "- If the tangent tilts upward → slope positive → derivative positive.  \n"
        "- If it tilts downward → slope negative → derivative negative.  \n"
        "- If it looks flat → slope 0 → derivative is 0.  \n"
        "- This is how graphs communicate derivatives without algebra."
    )
    st.latex(r"y'(a)\approx %.3f" % m)


def _sim_higher_order_objective_4556():
    st.markdown("### Objective 4.5.6 — Higher order derivatives (2nd derivative)")

    st.markdown(
        "**Example:** Find $y'$ and $y''$ for $y=(x^2+1)^3$ and explain meaning."
    )

    steps = [
        BoardStep(r"y=(x^2+1)^3", r"First derivative uses chain rule because this is a power of an inside expression."),
        BoardStep(r"y' = 3(x^2+1)^2 \cdot (2x)", r"Outside derivative: \(3(\cdot)^2\). Inside derivative: \(2x\). Multiply."),
        BoardStep(r"y' = 6x(x^2+1)^2", r"Simplify the first derivative."),
        BoardStep(r"y''=\frac{d}{dx}\left(6x(x^2+1)^2\right)", r"Now differentiate again (this needs product rule + chain rule)."),
        BoardStep(r"y''=6(x^2+1)^2 + 6x\cdot 2(x^2+1)\cdot (2x)", r"Product rule: derivative of \(6x\) plus \(6x\) times derivative of \((x^2+1)^2\)."),
        BoardStep(r"y''=6(x^2+1)^2 + 24x^2(x^2+1)", r"Simplify."),
        BoardStep(r"y''=6(x^2+1)\left((x^2+1)+4x^2\right)=6(x^2+1)(5x^2+1)", r"Factor for a clean final form."),
    ]
    render_simulation(steps, "Higher Derivatives — Pen Writing (Objective 4.5.6)")

    st.markdown("**Meaning (teacher words):**")
    st.markdown(
        "- $y'$ tells you **slope** (how fast the function is increasing/decreasing).  \n"
        "- $y''$ tells you **how the slope changes**:  \n"
        "  - If $y''>0$ the curve is bending upward (concave up).  \n"
        "  - If $y''<0$ the curve is bending downward (concave down)."
    )


def _sim_inverse_derivative_objective_4557():
    st.markdown("### Objective 4.5.7 — Derivative of an inverse function (teacher explanation + simulation)")

    st.markdown(
        "Teacher rule (very important): if $y=f(x)$ has an inverse, then the inverse derivative is:"
    )
    st.latex(r"(f^{-1})'(x)=\frac{1}{f'(f^{-1}(x))}")

    st.markdown(
        "**Simple meaning:** The inverse slope is the **reciprocal** of the original slope (but evaluated at matching inverse points)."
    )

    st.markdown("**Example:** If $f(x)=x^3$, then $f^{-1}(x)=\sqrt[3]{x}$.")

    steps = [
        BoardStep(r"f(x)=x^3", r"We know the inverse is \(f^{-1}(x)=\sqrt[3]{x}\)."),
        BoardStep(r"f'(x)=3x^2", r"Differentiate the original function."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{f'(f^{-1}(x))}", r"Use the inverse derivative formula."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{3(f^{-1}(x))^2}", r"Substitute \(f^{-1}(x)\) into \(f'(x)=3x^2\)."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{3(\sqrt[3]{x})^2}", r"Replace \(f^{-1}(x)\) with \(\sqrt[3]{x}\)."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{3x^{2/3}}", r"Final simplified answer."),
    ]
    render_simulation(steps, "Inverse Derivative — Pen Writing (Objective 4.5.7)")

    st.markdown(
        "**Teacher note:** In many exam questions, you can also use the reciprocal slope idea:"
    )
    st.latex(r"(f^{-1})'(a)=\frac{1}{f'(b)} \quad \text{where } b=f^{-1}(a)\ \text{and } f(b)=a")


# ----------------------------
# Main render
# ----------------------------
def render():
    st.markdown("## Subtopic 4.5: The Chain Rule")

    learn_tab, practice_tab = st.tabs(["Learn", "Practice"])

    with learn_tab:
        st.markdown("### ✅ Lesson Roadmap (Teacher replaces explanation)")
        st.markdown(
            "- We will learn chain rule in **two notations**.\n"
            "- We will use the **power shortcut**.\n"
            "- We will practice different function types (polynomial, trig, exponential, log).\n"
            "- We will apply chain rule to **tangent lines**.\n"
            "- We will understand derivatives **from graphs**.\n"
            "- We will learn **2nd derivative** idea.\n"
            "- We will learn **inverse derivative** rule."
        )

        st.divider()

        # 4.5.1
        st.markdown("## Objective 4.5.1 — Chain rule in BOTH notations (teacher explanation)")
        st.markdown(
            "When a function is inside another function, we differentiate the outside, then multiply by the derivative of the inside."
        )
        st.markdown("**Function notation:**")
        st.latex(r"[f(g(x))]'=f'(g(x))\cdot g'(x)")
        st.markdown("**Leibniz notation (step-by-step meaning):**")
        st.latex(r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}")
        st.markdown(
            "- Think: derivative of outside with respect to inside, then multiply by derivative of inside with respect to x."
        )

        st.divider()

        # 4.5.2
        st.markdown("## Objective 4.5.2 — General Power Rule Shortcut (super important)")
        st.markdown(
            "If you see a power of something (like $(\\,\text{inside}\\,)^{n}$), use this shortcut:"
        )
        st.latex(r"(u^n)'=nu^{n-1}u'")
        st.markdown(
            "This is chain rule + power rule combined. It saves time and avoids mistakes."
        )

        st.divider()

        # 4.5.3 — multiple types
        st.markdown("## Objective 4.5.3 — Different function types (with simulations)")
        st.markdown("We will cover: polynomial-inside, trig-inside, exponential/log-inside.")

        st.markdown("### Example A — Polynomial inside: $y=(3x^2+1)^5$")
        steps_a = [
            BoardStep(r"y=(3x^2+1)^5", r"Composite: inside \(u=3x^2+1\), outside \(u^5\)."),
            BoardStep(r"u=3x^2+1 \Rightarrow y=u^5", r"Let \(u\) be the inside."),
            BoardStep(r"\frac{dy}{du}=5u^4", r"Outside derivative."),
            BoardStep(r"\frac{du}{dx}=6x", r"Inside derivative."),
            BoardStep(r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}=5u^4\cdot 6x", r"Chain rule multiply."),
            BoardStep(r"\frac{dy}{dx}=30x(3x^2+1)^4", r"Substitute back. Final answer."),
        ]
        render_simulation(steps_a, "Example A — Chain Rule (Polynomial inside)")

        st.markdown("### Example B — Trig inside: $y=\\sin(2x^3)$")
        steps_b = [
            BoardStep(r"y=\sin(2x^3)", r"Outside is \(\sin(u)\), inside is \(u=2x^3\)."),
            BoardStep(r"u=2x^3 \Rightarrow y=\sin(u)", r"Define \(u\)."),
            BoardStep(r"\frac{dy}{du}=\cos(u)", r"Outside derivative."),
            BoardStep(r"\frac{du}{dx}=6x^2", r"Inside derivative."),
            BoardStep(r"\frac{dy}{dx}=6x^2\cos(u)", r"Multiply."),
            BoardStep(r"\frac{dy}{dx}=6x^2\cos(2x^3)", r"Substitute back."),
        ]
        render_simulation(steps_b, "Example B — Chain Rule (Trig inside)")

        st.markdown("### Example C — Exponential inside: $y=e^{x^2-4x}$")
        steps_c = [
            BoardStep(r"y=e^{x^2-4x}", r"Outside \(e^u\), inside \(u=x^2-4x\)."),
            BoardStep(r"u=x^2-4x \Rightarrow y=e^u", r"Define \(u\)."),
            BoardStep(r"\frac{dy}{du}=e^u", r"Outside derivative."),
            BoardStep(r"\frac{du}{dx}=2x-4", r"Inside derivative."),
            BoardStep(r"\frac{dy}{dx}=e^u(2x-4)", r"Multiply."),
            BoardStep(r"\frac{dy}{dx}=(2x-4)e^{x^2-4x}", r"Substitute back."),
        ]
        render_simulation(steps_c, "Example C — Chain Rule (Exponential)")

        st.markdown("### Example D — Log inside: $y=\\ln(5x^2+1)$")
        steps_d = [
            BoardStep(r"y=\ln(5x^2+1)", r"Outside is \(\ln(u)\), inside is \(u=5x^2+1\)."),
            BoardStep(r"u=5x^2+1 \Rightarrow y=\ln(u)", r"Define \(u\)."),
            BoardStep(r"\frac{dy}{du}=\frac{1}{u}", r"Derivative of \(\ln(u)\) is \(1/u\)."),
            BoardStep(r"\frac{du}{dx}=10x", r"Derivative of \(5x^2+1\) is \(10x\)."),
            BoardStep(r"\frac{dy}{dx}=\frac{1}{u}\cdot 10x", r"Multiply (chain rule)."),
            BoardStep(r"\frac{dy}{dx}=\frac{10x}{5x^2+1}", r"Substitute back. Final answer."),
        ]
        render_simulation(steps_d, "Example D — Chain Rule (Logarithm)")

        st.divider()

        # Common mistakes
        st.markdown("## Common Mistakes (teacher warning)")
        st.markdown(
            "- Forgetting to multiply by the inside derivative.  \n"
            "- Differentiating inside incorrectly.  \n"
            "- Treating $(u^n)'$ as $nu^{n-1}$ only and forgetting $u'$.  \n"
            "- For trig/log/exp: forgetting the correct outside derivative (e.g., $(\ln u)'=1/u$)."
        )

        st.divider()

        # 4.5.4
        _sim_tangent_line_objective_4554()
        st.divider()

        # 4.5.5
        _sim_derivative_from_graph_objective_4555()
        st.divider()

        # 4.5.6
        _sim_higher_order_objective_4556()
        st.divider()

        # 4.5.7
        _sim_inverse_derivative_objective_4557()
        st.divider()

        # Graphs section
        st.markdown("## Graphs — Proper size + clear explanation + interactive")
        _graph_polynomial_chain()
        st.divider()
        _graph_explorer_sin()
        st.divider()
        _graph_explorer_exp_sign()

    with practice_tab:
        # Practice stays exactly as you approved
        render_practice()
