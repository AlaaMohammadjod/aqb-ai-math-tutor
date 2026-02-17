import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO

from simulations import BoardStep, render_simulation
from subtopic_4_5_chain_rule_practice import render_practice


# ---------------------------------
# Plot rendering (small + consistent)
# ---------------------------------
def _show_fig(fig, width_px: int = 720):
    """Render a Matplotlib figure as a reasonably-sized image (no full-width stretching)."""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    st.image(buf.getvalue(), width=width_px)


def _plot_with_tangent(ax, x, y, x0, y0, m, title):
    tangent = y0 + m * (x - x0)
    ax.plot(x, y, label=r"$y$")
    ax.plot(x, tangent, linestyle="--", label=r"tangent at $x=a$")
    ax.scatter([x0], [y0], s=45, zorder=5)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    ax.legend()


# ---------------------------------
# Small "no-slider" graph simulators
# ---------------------------------
def _stepper(key: str, n_steps: int):
    """Return step index controlled by Back/Next buttons (no sliders)."""
    if key not in st.session_state:
        st.session_state[key] = 0

    c_back, c_spacer, c_next = st.columns([1, 6, 1])
    with c_back:
        back = st.button("Back", key=f"{key}_back")
    with c_next:
        nxt = st.button("Next", key=f"{key}_next")

    if back:
        st.session_state[key] = max(0, st.session_state[key] - 1)
    if nxt:
        st.session_state[key] = min(n_steps - 1, st.session_state[key] + 1)

    return st.session_state[key]


def _choose_pi_point(label: str, key: str):
    """
    IMPORTANT:
    Streamlit selectbox options CANNOT render KaTeX.
    So we show human-readable π text in the dropdown (no backslashes),
    then render the selected value in KaTeX UNDER the dropdown using st.latex.
    """
    options = [
        ("a = −π/2", r"-\frac{\pi}{2}", -np.pi / 2),
        ("a = −π/3", r"-\frac{\pi}{3}", -np.pi / 3),
        ("a = −π/6", r"-\frac{\pi}{6}", -np.pi / 6),
        ("a = 0", r"0", 0.0),
        ("a = π/6", r"\frac{\pi}{6}", np.pi / 6),
        ("a = π/3", r"\frac{\pi}{3}", np.pi / 3),
        ("a = π/2", r"\frac{\pi}{2}", np.pi / 2),
    ]

    display = [opt[0] for opt in options]
    idx = st.selectbox(label, list(range(len(display))), format_func=lambda i: display[i], key=key)

    latex_a = options[idx][1]
    a_val = float(options[idx][2])

    # KaTeX “humanised” rendering of the selected value
    st.latex(rf"a = {latex_a}")

    return a_val, latex_a


def _graph_sim_sin3x_tangent():
    st.markdown("### Graph Simulation 1 — Tangent slope (π-based) for a chain-rule trig function")

    st.markdown("You will *see* the derivative as a tangent slope for a function that requires the chain rule.")
    st.latex(r"y=\sin(3x)")
    st.latex(r"y'=3\cos(3x)")

    st.markdown("Choose the point using π-values (so trig values stay exact). Then step through the graph.")
    a_val, a_tex = _choose_pi_point("Choose the point x = a:", key="sin3x_a")

    step = _stepper("sin3x_step", n_steps=3)

    x = np.linspace(-np.pi, np.pi, 1200)
    y = np.sin(3 * x)

    y0 = float(np.sin(3 * a_val))
    m = float(3 * np.cos(3 * a_val))

    fig = plt.figure(figsize=(6.6, 3.6))
    ax = fig.add_subplot(111)

    if step == 0:
        ax.plot(x, y, label=r"$y=\sin(3x)$")
        ax.set_title("Step 1: The curve")
    elif step == 1:
        ax.plot(x, y, label=r"$y=\sin(3x)$")
        ax.scatter([a_val], [y0], s=45, zorder=5, label=r"point $(a, y(a))$")
        ax.set_title("Step 2: Mark the point on the curve")
    else:
        _plot_with_tangent(ax, x, y, a_val, y0, m, "Step 3: Tangent line (slope = derivative)")

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, alpha=0.25)
    ax.legend()

    _show_fig(fig, width_px=740)

    st.markdown("**Read the result (teacher explanation):**")
    st.markdown("- The dashed line shows the tangent line at the chosen point.")
    st.markdown("- The derivative value is exactly the slope of that tangent line.")
    st.markdown("- Using π-points keeps trig values exact.")

    st.latex(rf"(a, y(a))=\left({a_tex},\ \sin\left(3\cdot {a_tex}\right)\right)")
    st.latex(rf"y'(a)=3\cos\left(3\cdot {a_tex}\right)")
    st.latex(rf"y'(a)\approx {m:.4f}")


def _graph_polynomial_chain_small():
    st.markdown("### Graph Simulation 2 — Why chain rule can create large slopes (no sliders)")
    st.markdown("This visual compares the function and its derivative to show where the curve is steep or flat.")
    st.latex(r"y=(3x^2+1)^5")
    st.latex(r"y' = 30x(3x^2+1)^4")

    x = np.linspace(-1.2, 1.2, 900)
    y = (3 * x**2 + 1) ** 5
    yp = 30 * x * (3 * x**2 + 1) ** 4

    step = _stepper("poly_step", n_steps=2)

    fig = plt.figure(figsize=(6.6, 3.6))
    ax = fig.add_subplot(111)

    if step == 0:
        ax.plot(x, y, label=r"$y$")
        ax.set_title("Step 1: The function")
    else:
        ax.plot(x, y, label=r"$y$")
        ax.plot(x, yp, label=r"$y'$")
        ax.set_title("Step 2: Add the derivative")

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, alpha=0.25)
    ax.legend()

    _show_fig(fig, width_px=740)

    st.markdown("**What students should notice:**")
    st.markdown("- Where $y'$ is large and positive, the curve rises steeply.")
    st.markdown("- Where $y'$ is large and negative, the curve falls steeply.")
    st.markdown("- Where $y'=0$, the tangent is horizontal (flat).")


def _graph_exp_sign_small():
    st.markdown("### Graph Simulation 3 — Increasing / decreasing from the sign of $y'$ (no sliders)")
    st.latex(r"y=e^{x^2-4x}")
    st.latex(r"y'=(2x-4)e^{x^2-4x}")

    a_options = [r"-1", r"0", r"1", r"2", r"3", r"4"]
    a_vals = [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
    idx = st.selectbox(
        "Choose the point x = a:",
        list(range(len(a_options))),
        format_func=lambda i: f"a = {a_options[i]}",
        key="exp_a",
    )
    a = a_vals[idx]
    st.latex(rf"a={a_options[idx]}")

    x = np.linspace(-1.0, 4.0, 1200)
    expo = x**2 - 4 * x
    y = np.exp(expo)
    yp = (2 * x - 4) * np.exp(expo)

    y0 = float(np.exp(a**2 - 4 * a))
    m = float((2 * a - 4) * np.exp(a**2 - 4 * a))

    step = _stepper("exp_step", n_steps=3)

    fig = plt.figure(figsize=(6.6, 3.6))
    ax = fig.add_subplot(111)

    if step == 0:
        ax.plot(x, y, label=r"$y$")
        ax.set_title("Step 1: The function")
    elif step == 1:
        ax.plot(x, y, label=r"$y$")
        ax.plot(x, yp, label=r"$y'$")
        ax.set_title("Step 2: Add the derivative")
    else:
        ax.plot(x, y, label=r"$y$")
        ax.plot(x, yp, label=r"$y'$")
        ax.scatter([a], [y0], s=45, zorder=5, label=r"point $(a,y(a))$")
        ax.axvline(2, linestyle=":", linewidth=2, label=r"$x=2$ (where $y'=0$)")
        ax.set_title("Step 3: Mark a point and interpret the slope")

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, alpha=0.25)
    ax.legend()

    _show_fig(fig, width_px=740)

    st.markdown("**Teacher explanation:**")
    st.markdown("- The factor $e^{x^2-4x}$ is always positive.")
    st.markdown("- So the sign of $y'$ comes from $(2x-4)$.")
    st.latex(r"y'(a)\approx %.4f" % m)


# ---------------------------------
# Objective simulations (blackboard)
# ---------------------------------
def _sim_tangent_line_objective_4554():
    st.markdown("### Objective 4.5.4 — Tangent line using chain rule (step-by-step)")
    st.markdown("**Problem:** Find the equation of the tangent line to the curve at the given point.")
    st.latex(r"y=(3x^2+1)^5\quad\text{at }x=1")

    steps = [
        BoardStep(r"y=(3x^2+1)^5", r"We need the slope at \(x=1\), which is \(y'(1)\), and the point \((1,y(1))\)."),
        BoardStep(r"y' = 30x(3x^2+1)^4", r"Differentiate using chain rule."),
        BoardStep(r"y(1)=(3\cdot 1^2+1)^5 = 4^5 = 1024", r"Compute the point on the curve."),
        BoardStep(r"y'(1)=30(1)(3\cdot 1^2+1)^4 = 30\cdot 4^4 = 7680", r"Compute the slope at \(x=1\)."),
        BoardStep(r"y-y_1=m(x-x_1)", r"Use point-slope form."),
        BoardStep(r"\boxed{y-1024 = 7680(x-1)}", r"Final tangent line equation."),
    ]
    render_simulation(steps, "Tangent Line — Blackboard (Objective 4.5.4)")


def _sim_derivative_from_graph_objective_4555():
    st.markdown("### Objective 4.5.5 — Derivative at a point from a graph")
    st.markdown("In a graph question, you often don’t need to differentiate algebraically. You read the slope of the tangent.")
    st.latex(r"f'(a)=\text{slope of the tangent line to }y=f(x)\text{ at }x=a")

    st.markdown("Use the simulation below to practice the idea with π-based points.")
    _graph_sim_sin3x_tangent()

    st.markdown("**Exam tip:** If the tangent looks horizontal, then $f'(a)=0$. If it is steep downward, then $f'(a)$ is negative.")


def _sim_higher_order_objective_4556():
    st.markdown("### Objective 4.5.6 — Higher order derivatives (finding $y''$)")
    st.markdown("**Problem:** Find $y'$ and $y''$ for the function.")
    st.latex(r"y=(x^2+1)^3")

    steps = [
        BoardStep(r"y=(x^2+1)^3", r"First derivative uses chain rule (power of an inside expression)."),
        BoardStep(r"y' = 3(x^2+1)^2 \cdot (2x)", r"Outside derivative: \(3(\cdot)^2\). Inside derivative: \(2x\). Multiply."),
        BoardStep(r"\boxed{y' = 6x(x^2+1)^2}", r"Simplify the first derivative."),
        BoardStep(r"y''=\frac{d}{dx}\left(6x(x^2+1)^2\right)", r"Now differentiate again (product rule + chain rule)."),
        BoardStep(r"y''=6(x^2+1)^2 + 6x\cdot 2(x^2+1)\cdot (2x)", r"Product rule, then chain rule on \((x^2+1)^2\)."),
        BoardStep(r"\boxed{y''=6(x^2+1)^2 + 24x^2(x^2+1)}", r"Simplify."),
        BoardStep(r"\boxed{y''=6(x^2+1)(5x^2+1)}", r"Factor to a clean final form."),
    ]
    render_simulation(steps, "Higher Derivatives — Blackboard (Objective 4.5.6)")

    st.markdown("**Meaning:**")
    st.markdown("- $y'$ tells you the slope (increase/decrease).")
    st.markdown("- $y''$ tells you how the slope is changing (concavity).")


def _sim_inverse_derivative_objective_4557():
    st.markdown("### Objective 4.5.7 — Derivative of an inverse function")
    st.markdown("**Key rule (must memorize):**")
    st.latex(r"(f^{-1})'(x)=\frac{1}{f'(f^{-1}(x))}")

    st.markdown("**Problem:** Use the rule to find the derivative of the inverse function.")
    st.latex(r"f(x)=x^3\quad\Rightarrow\quad f^{-1}(x)=\sqrt[3]{x}")

    steps = [
        BoardStep(r"f(x)=x^3", r"The inverse is \(f^{-1}(x)=\sqrt[3]{x}\)."),
        BoardStep(r"f'(x)=3x^2", r"Differentiate the original function."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{f'(f^{-1}(x))}", r"Apply the inverse derivative formula."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{3(f^{-1}(x))^2}", r"Substitute \(f^{-1}(x)\) into \(f'(x)=3x^2\)."),
        BoardStep(r"(f^{-1})'(x)=\frac{1}{3(\sqrt[3]{x})^2}", r"Replace \(f^{-1}(x)\) with \(\sqrt[3]{x}\)."),
        BoardStep(r"\boxed{(f^{-1})'(x)=\frac{1}{3x^{2/3}}}", r"Final simplified answer."),
    ]
    render_simulation(steps, "Inverse Derivative — Blackboard (Objective 4.5.7)")

    st.markdown("**Exam tip:** If you know a matching point pair $(b,a)$ where $f(b)=a$, then:")
    st.latex(r"(f^{-1})'(a)=\frac{1}{f'(b)}")


# ---------------------------------
# Main render
# ---------------------------------
def render():
    st.markdown("## Subtopic 4.5: The Chain Rule")

    learn_tab, practice_tab = st.tabs(["Learn", "Practice"])

    with learn_tab:
        st.markdown("### ✅ Lesson Roadmap (Teacher replaces explanation)")
        st.markdown(
            """
- We learn chain rule in **two notations**.
- We use the **general power rule shortcut**.
- We practice chain rule with polynomial, trig, exponential, and logarithmic examples.
- We apply chain rule to **tangent line** questions.
- We connect derivatives to **graphs** (slope meaning).
- We find **higher order derivatives**.
- We use the **inverse derivative** rule.
            """
        )

        st.divider()

        # 4.5.1
        st.markdown("## Objective 4.5.1 — Chain rule in BOTH notations")
        st.markdown("When one function is inside another function:")
        st.latex(r"[f(g(x))]'=f'(g(x))\cdot g'(x)")
        st.markdown("Leibniz notation (shows the 'multiply the rates' idea):")
        st.latex(r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}")

        st.markdown("**Teacher tip:** Say out loud: “Differentiate the outside, then multiply by the inside derivative.”")

        st.divider()

        # 4.5.2
        st.markdown("## Objective 4.5.2 — General Power Rule Shortcut")
        st.markdown("If the outside is a power, use this shortcut (chain rule built-in):")
        st.latex(r"(u^n)'=nu^{n-1}u'")

        st.markdown("**Mini example:**")
        st.latex(r"y=(5x-1)^6")
        st.latex(r"y'=6(5x-1)^5\cdot 5=30(5x-1)^5")

        st.divider()

        # 4.5.3
        st.markdown("## Objective 4.5.3 — Chain rule with different function types")

        st.markdown("### Example A — Polynomial inside")
        st.markdown("**Problem:** Differentiate the function.")
        st.latex(r"y=(3x^2+1)^5")
        steps_a = [
            BoardStep(r"y=(3x^2+1)^5", r"Composite: inside \(u=3x^2+1\), outside \(u^5\)."),
            BoardStep(r"u=3x^2+1\Rightarrow y=u^5", r"Let \(u\) be the inside."),
            BoardStep(r"\frac{dy}{du}=5u^4", r"Outside derivative."),
            BoardStep(r"\frac{du}{dx}=6x", r"Inside derivative."),
            BoardStep(r"\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}=5u^4\cdot 6x", r"Multiply (chain rule)."),
            BoardStep(r"\boxed{\frac{dy}{dx}=30x(3x^2+1)^4}", r"Substitute back. Final answer."),
        ]
        render_simulation(steps_a, "Example A — Chain Rule (Polynomial inside)")

        st.markdown("### Example B — Trigonometric inside (π-friendly evaluation)")
        st.markdown("**Problem:** Differentiate and evaluate the derivative at a π-point.")
        st.latex(r"y=\sin(3x)\quad\text{and evaluate }y'\!\left(\frac{\pi}{6}\right)")
        steps_b = [
            BoardStep(r"y=\sin(3x)", r"Outside is \(\sin(u)\); inside is \(u=3x\)."),
            BoardStep(r"u=3x\Rightarrow y=\sin(u)", r"Define the inside."),
            BoardStep(r"\frac{dy}{du}=\cos(u)", r"Outside derivative."),
            BoardStep(r"\frac{du}{dx}=3", r"Inside derivative."),
            BoardStep(r"\boxed{y'=3\cos(3x)}", r"Substitute back."),
            BoardStep(r"y'\!\left(\frac{\pi}{6}\right)=3\cos\left(\frac{\pi}{2}\right)=0", r"Exact trig evaluation using π."),
        ]
        render_simulation(steps_b, "Example B — Chain Rule (Trig inside, π evaluation)")

        st.divider()

        st.markdown("## High-impact teacher tips")
        st.markdown("- Always identify the **inside** function first.")
        st.markdown("- Write the inside derivative immediately (so you don’t forget it).")
        st.markdown("- If you evaluate at trig angles, keep answers exact using π-values.")

        st.divider()

        _sim_tangent_line_objective_4554()
        st.divider()

        _sim_derivative_from_graph_objective_4555()
        st.divider()

        _sim_higher_order_objective_4556()
        st.divider()

        _sim_inverse_derivative_objective_4557()
        st.divider()

        st.markdown("## Graph section (proper size, simulated, no sliders)")
        _graph_polynomial_chain_small()
        st.divider()
        _graph_exp_sign_small()

    with practice_tab:
        render_practice()
