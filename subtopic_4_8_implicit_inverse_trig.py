# subtopic_4_8_implicit_inverse_trig.py
import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# ------------------------------------------------------------
# Helpers (match your Subtopic 4.7 style)
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
# Visualisations (clear + student-friendly)
# ------------------------------------------------------------
def _plot_circle_and_tangent(x0: float, branch: str = "upper"):
    """
    Implicit curve: x^2 + y^2 = 25 (circle radius 5)
    y = ±sqrt(25 - x^2)
    dy/dx = -x/y
    """
    r2 = 25.0
    if abs(x0) >= 5:
        x0 = 4.999

    y0 = math.sqrt(r2 - x0 * x0)
    if branch == "lower":
        y0 = -y0

    m = -x0 / y0  # dy/dx

    x = np.linspace(-5.2, 5.2, 600)
    y_up = np.sqrt(np.clip(r2 - x * x, 0, None))
    y_dn = -y_up

    y_tan = m * (x - x0) + y0

    fig = plt.figure(figsize=(6.6, 3.8))
    ax = fig.add_subplot(111)
    ax.plot(x, y_up, label=r"$x^2+y^2=25$ (upper)")
    ax.plot(x, y_dn, label=r"$x^2+y^2=25$ (lower)")
    ax.plot(x, y_tan, label="Tangent line at chosen point")
    ax.scatter([x0], [y0], s=50)
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Implicit curve + tangent line (visual)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig, x0, y0, m


def _plot_inverse_trig_family(which: str):
    """Plot an inverse trig function and its derivative (two curves)."""
    fig = plt.figure(figsize=(6.6, 3.8))
    ax = fig.add_subplot(111)

    if which == "arcsin":
        x = np.linspace(-0.999, 0.999, 600)
        y = np.arcsin(x)
        yp = 1 / np.sqrt(1 - x * x)
        ax.plot(x, y, label=r"$y=\arcsin(x)$")
        ax.plot(x, yp, label=r"$y'=\frac{1}{\sqrt{1-x^2}}$")
        ax.set_title(r"$\arcsin(x)$ and its derivative (domain matters!)")

    elif which == "arccos":
        x = np.linspace(-0.999, 0.999, 600)
        y = np.arccos(x)
        yp = -1 / np.sqrt(1 - x * x)
        ax.plot(x, y, label=r"$y=\arccos(x)$")
        ax.plot(x, yp, label=r"$y'=-\frac{1}{\sqrt{1-x^2}}$")
        ax.set_title(r"$\arccos(x)$ and its derivative (domain matters!)")

    else:  # arctan
        x = np.linspace(-6, 6, 600)
        y = np.arctan(x)
        yp = 1 / (1 + x * x)
        ax.plot(x, y, label=r"$y=\arctan(x)$")
        ax.plot(x, yp, label=r"$y'=\frac{1}{1+x^2}$")
        ax.set_title(r"$\arctan(x)$ and its derivative")

    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig


# ------------------------------------------------------------
# Blackboard simulations (use your unchanged simulations.py)
# ------------------------------------------------------------
def _sim_implicit_circle_steps():
    steps = [
        BoardStep(
            latex_line=r"x^2+y^2=25",
            teacher_explain_md=r"""
We have an **implicit equation** ( $y$ is not isolated ).

**Student task:** Differentiate both sides w.r.t. $x$ and isolate $y'$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(x^2)+\frac{d}{dx}(y^2)=\frac{d}{dx}(25)",
            teacher_explain_md=r"""
Differentiate term-by-term.

- $\frac{d}{dx}(x^2)=2x$
- $\frac{d}{dx}(25)=0$
- $\frac{d}{dx}(y^2)$ needs **chain rule** because $y=y(x)$.
""",
        ),
        BoardStep(
            latex_line=r"2x+2y\frac{dy}{dx}=0",
            teacher_explain_md=r"""
Key chain rule moment:
$$
\frac{d}{dx}(y^2)=2y\cdot \frac{dy}{dx}
$$
This is the #1 step students forget.
""",
        ),
        BoardStep(
            latex_line=r"2y\frac{dy}{dx}=-2x",
            teacher_explain_md=r"Now isolate the $dy/dx$ term on one side.",
        ),
        BoardStep(
            latex_line=r"\frac{dy}{dx}=-\frac{x}{y}",
            teacher_explain_md=r"""
Divide both sides by $2y$:
$$
\frac{dy}{dx}=-\frac{x}{y}
$$
""",
        ),
    ]
    return steps


def _sim_example_8_1_tangent_steps():
    steps = [
        BoardStep(
            latex_line=r"x^2+y^3-2y=3",
            teacher_explain_md=r"""
**Student task:** Find $y'$ implicitly, then find the tangent line at $(2,1)$.

This equation is hard to solve for $y$, so implicit differentiation is the clean method.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(x^2)+\frac{d}{dx}(y^3)-\frac{d}{dx}(2y)=\frac{d}{dx}(3)",
            teacher_explain_md=r"""
Differentiate both sides w.r.t. $x$.

Remember:
- $\frac{d}{dx}(y^3)=3y^2y'$ (chain rule)
- $\frac{d}{dx}(2y)=2y'$
""",
        ),
        BoardStep(
            latex_line=r"2x+3y^2y'-2y'=0",
            teacher_explain_md=r"Now collect all terms with $y'$ together.",
        ),
        BoardStep(
            latex_line=r"(3y^2-2)\,y'=-2x",
            teacher_explain_md=r"Factor out $y'$.",
        ),
        BoardStep(
            latex_line=r"y'=-\frac{2x}{3y^2-2}",
            teacher_explain_md=r"""
Final derivative:
$$
y'=-\frac{2x}{3y^2-2}
$$
Now substitute $(2,1)$ to get the slope.
""",
        ),
        BoardStep(
            latex_line=r"m=y'(2,1)=-\frac{4}{3(1)^2-2}=-4",
            teacher_explain_md=r"""
Slope at $(2,1)$ is $m=-4$.

Now write the tangent line using point-slope form.
""",
        ),
        BoardStep(
            latex_line=r"y-1=-4(x-2)",
            teacher_explain_md=r"That is the tangent line at $(2,1)$.",
        ),
    ]
    return steps


def _sim_example_8_2_tangent_steps():
    steps = [
        BoardStep(
            latex_line=r"x^2y^2-2x=4-4y",
            teacher_explain_md=r"""
**Student task:** Find $y'$ and then the tangent line at $(2,-2)$.

Notice: $x^2y^2$ is a **product** of $x^2$ and $y^2$ → we need product rule + chain rule.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(x^2y^2)-\frac{d}{dx}(2x)=\frac{d}{dx}(4-4y)",
            teacher_explain_md=r"""
Differentiate both sides.
- LHS first term needs **product rule**
- RHS has $-4y$ → derivative is $-4y'$
""",
        ),
        BoardStep(
            latex_line=r"2xy^2+x^2(2y)y'-2=-4y'",
            teacher_explain_md=r"""
Product rule result:
$$
\frac{d}{dx}(x^2y^2)=(2x)y^2+x^2(2y)y'
$$
""",
        ),
        BoardStep(
            latex_line=r"(2x^2y+4)y'=2-2xy^2",
            teacher_explain_md=r"""
Collect all $y'$ terms on one side, everything else on the other side.
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{2-2xy^2}{2x^2y+4}",
            teacher_explain_md=r"Now substitute $(2,-2)$ to get the slope.",
        ),
        BoardStep(
            latex_line=r"m=y'(2,-2)=\frac{2-16}{-16+4}=\frac{7}{6}",
            teacher_explain_md=r"""
So the slope is $m=\frac{7}{6}$.

Now write the tangent line using point-slope form at $(2,-2)$.
""",
        ),
        BoardStep(
            latex_line=r"y+2=\frac{7}{6}(x-2)",
            teacher_explain_md=r"That is the tangent line at $(2,-2)$.",
        ),
    ]
    return steps


def _sim_radical_implicit_steps():
    steps = [
        BoardStep(
            latex_line=r"\sqrt{x}+\sqrt{y}=10",
            teacher_explain_md=r"""
**Student task:** Differentiate implicitly and isolate $y'$.

This is a **radical case**. The chain rule is needed for $\sqrt{y}=y^{1/2}$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{1}{2\sqrt{x}}+\frac{1}{2\sqrt{y}}\,y'=0",
            teacher_explain_md=r"""
Differentiate:
$$
\frac{d}{dx}(\sqrt{x})=\frac{1}{2\sqrt{x}},\qquad
\frac{d}{dx}(\sqrt{y})=\frac{1}{2\sqrt{y}}\,y'
$$
""",
        ),
        BoardStep(
            latex_line=r"\frac{1}{2\sqrt{y}}\,y'=-\frac{1}{2\sqrt{x}}",
            teacher_explain_md=r"Now isolate the $y'$ term.",
        ),
        BoardStep(
            latex_line=r"y'=-\frac{\sqrt{y}}{\sqrt{x}}",
            teacher_explain_md=r"""
Final derivative:
$$
y'=-\frac{\sqrt{y}}{\sqrt{x}}
$$
""",
        ),
    ]
    return steps


def _sim_log_implicit_steps():
    steps = [
        BoardStep(
            latex_line=r"\ln(xy)=y",
            teacher_explain_md=r"""
**Student task:** Differentiate implicitly and isolate $y'$.

This is a **logarithmic case**.
You must use:
$$
\frac{d}{dx}(\ln u)=\frac{u'}{u}
$$
with $u=xy$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{(xy)'}{xy}=y'",
            teacher_explain_md=r"""
Differentiate both sides:
$$
\frac{d}{dx}\ln(xy)=\frac{(xy)'}{xy}
$$
Right side: $\frac{d}{dx}(y)=y'$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{x y'+y}{xy}=y'",
            teacher_explain_md=r"""
Use product rule:
$$
(xy)'=xy'+y
$$
""",
        ),
        BoardStep(
            latex_line=r"x y'+y=xy\,y'",
            teacher_explain_md=r"Multiply both sides by $xy$.",
        ),
        BoardStep(
            latex_line=r"y=x y'(y-1)",
            teacher_explain_md=r"Collect $y'$ terms and factor.",
        ),
        BoardStep(
            latex_line=r"y'=\frac{y}{x(y-1)}",
            teacher_explain_md=r"""
Final derivative:
$$
y'=\frac{y}{x(y-1)}
$$
""",
        ),
    ]
    return steps


def _sim_second_derivative_exp_steps():
    steps = [
        BoardStep(
            latex_line=r"y^2+2e^{-xy}=6",
            teacher_explain_md=r"""
**Student task:** Find $y''$ implicitly, then evaluate at $(0,2)$.

We will keep work organised and evaluate smartly at the point to avoid messy algebra.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(y^2)+\frac{d}{dx}(2e^{-xy})=0",
            teacher_explain_md=r"""
Differentiate both sides w.r.t. $x$. RHS is $0$.
""",
        ),
        BoardStep(
            latex_line=r"2yy'+2e^{-xy}(-y-xy')=0",
            teacher_explain_md=r"""
Chain rule:
- $\frac{d}{dx}(y^2)=2yy'$
- $\frac{d}{dx}(e^{-xy})=e^{-xy}\cdot \frac{d}{dx}(-xy)=e^{-xy}(-y-xy')$
""",
        ),
        BoardStep(
            latex_line=r"(y-xe^{-xy})y'=e^{-xy}y",
            teacher_explain_md=r"""
Rearrange to a useful form (collect $y'$ terms):
$$
yy' - xe^{-xy}y' = e^{-xy}y
\Rightarrow (y-xe^{-xy})y'=e^{-xy}y
$$
""",
        ),
        BoardStep(
            latex_line=r"\text{At }(0,2):\ e^{0}=1,\ (y-xe^{-xy})=2 \Rightarrow y'(0)=1",
            teacher_explain_md=r"""
Evaluate $y'$ at the point:

At $(0,2)$: $e^{-xy}=e^0=1$

So:
$$
(2-0)\,y'(0)=1\cdot 2 \Rightarrow y'(0)=1
$$
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}\Big[(y-xe^{-xy})y'\Big]=\frac{d}{dx}\Big[e^{-xy}y\Big]",
            teacher_explain_md=r"""
Differentiate the rearranged equation again to get $y''$.
""",
        ),
        BoardStep(
            latex_line=r"(y-xe^{-xy})y''+\Big(\frac{d}{dx}(y-xe^{-xy})\Big)y'=\frac{d}{dx}(e^{-xy}y)",
            teacher_explain_md=r"""
Product rule on the left:
$$
\frac{d}{dx}(AB)=A'B+AB'
$$
Here $A=(y-xe^{-xy})$ and $B=y'$.
""",
        ),
        BoardStep(
            latex_line=r"\text{At }(0,2):\ \frac{d}{dx}(y-xe^{-xy})=0,\ \frac{d}{dx}(e^{-xy}y)=-3",
            teacher_explain_md=r"""
Now evaluate **at the point** $(0,2)$ using $y'(0)=1$:

At $x=0$: $e^{-xy}=1$.

- $\frac{d}{dx}(y-xe^{-xy}) = y' - e^{-xy} + x(\cdots)$.
At $x=0$: $y' - 1 = 1-1=0$.

- $\frac{d}{dx}(e^{-xy}y)=e^{-xy}(-y-xy')y+e^{-xy}y'$.
At $x=0, y=2, y'=1$:
$$
(-2)\cdot 2 + 1 = -4+1=-3
$$
""",
        ),
        BoardStep(
            latex_line=r"2y''=-3 \Rightarrow y''(0)=-\frac{3}{2}",
            teacher_explain_md=r"""
At $(0,2)$: $(y-xe^{-xy})=2$, and the middle term is $0$, so:

$$
2y''=-3 \Rightarrow y''(0)=-\frac{3}{2}
$$
""",
        ),
    ]
    return steps


def _sim_derive_arcsin_steps():
    steps = [
        BoardStep(
            latex_line=r"y=\arcsin(x)\quad\Rightarrow\quad \sin(y)=x",
            teacher_explain_md=r"""
**Student task:** Derive $\frac{d}{dx}(\arcsin x)$ using implicit differentiation.

Rewrite inverse trig as a normal trig equation.
""",
        ),
        BoardStep(
            latex_line=r"\cos(y)\,y'=1",
            teacher_explain_md=r"""
Differentiate:
$$
\frac{d}{dx}(\sin y)=\cos(y)\,y'
$$
and $\frac{d}{dx}(x)=1$.
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{1}{\cos(y)}",
            teacher_explain_md=r"Isolate $y'$.",
        ),
        BoardStep(
            latex_line=r"\cos(y)=\sqrt{1-\sin^2(y)}=\sqrt{1-x^2}",
            teacher_explain_md=r"""
Rewrite in terms of $x$.
Since $\sin(y)=x$:
$$
\cos(y)=\sqrt{1-x^2}
$$
(Principal range for arcsin makes cosine nonnegative.)
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(\arcsin x)=\frac{1}{\sqrt{1-x^2}}",
            teacher_explain_md=r"Final rule.",
        ),
    ]
    return steps


def _sim_derive_arctan_steps():
    steps = [
        BoardStep(
            latex_line=r"y=\arctan(x)\quad\Rightarrow\quad \tan(y)=x",
            teacher_explain_md=r"Rewrite inverse trig as a normal trig equation.",
        ),
        BoardStep(
            latex_line=r"\sec^2(y)\,y'=1",
            teacher_explain_md=r"""
Differentiate:
$$
\frac{d}{dx}(\tan y)=\sec^2(y)\,y'
$$
""",
        ),
        BoardStep(
            latex_line=r"y'=\frac{1}{\sec^2(y)}",
            teacher_explain_md=r"Isolate $y'$.",
        ),
        BoardStep(
            latex_line=r"\sec^2(y)=1+\tan^2(y)=1+x^2",
            teacher_explain_md=r"""
Use identity:
$$
\sec^2(y)=1+\tan^2(y)
$$
Since $\tan(y)=x$, we get $\sec^2(y)=1+x^2$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(\arctan x)=\frac{1}{1+x^2}",
            teacher_explain_md=r"Final rule.",
        ),
    ]
    return steps


def _sim_chain_rule_arccos_steps():
    steps = [
        BoardStep(
            latex_line=r"y=\arccos(3x^2)",
            teacher_explain_md=r"""
**Student task:** Differentiate using chain rule.

Template:
$$
\frac{d}{dx}(\arccos u)=-\frac{u'}{\sqrt{1-u^2}}
$$
""",
        ),
        BoardStep(
            latex_line=r"u=3x^2\Rightarrow u'=6x",
            teacher_explain_md=r"Identify inner function $u$ and its derivative.",
        ),
        BoardStep(
            latex_line=r"y'=-\frac{6x}{\sqrt{1-(3x^2)^2}}=-\frac{6x}{\sqrt{1-9x^4}}",
            teacher_explain_md=r"Substitute into the chain rule formula and simplify.",
        ),
    ]
    return steps


def _sim_chain_rule_arcsec_squared_steps():
    steps = [
        BoardStep(
            latex_line=r"y=(\operatorname{arcsec}x)^2",
            teacher_explain_md=r"""
**Student task:** Differentiate.

This is a **power of a function** → outer power rule + chain rule.
Also: arcsec derivative includes $|x|$.
""",
        ),
        BoardStep(
            latex_line=r"y'=2(\operatorname{arcsec}x)\cdot \frac{d}{dx}(\operatorname{arcsec}x)",
            teacher_explain_md=r"Differentiate the outer square first.",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dx}(\operatorname{arcsec}x)=\frac{1}{|x|\sqrt{x^2-1}}",
            teacher_explain_md=r"Use the inverse trig derivative rule (with domain restriction $|x|>1$).",
        ),
        BoardStep(
            latex_line=r"y'=\frac{2\operatorname{arcsec}x}{|x|\sqrt{x^2-1}}",
            teacher_explain_md=r"Multiply and simplify.",
        ),
    ]
    return steps


def _sim_chain_rule_arctan_x3_steps():
    steps = [
        BoardStep(
            latex_line=r"y=\arctan(x^3)",
            teacher_explain_md=r"""
**Student task:** Differentiate using chain rule.

Template:
$$
\frac{d}{dx}(\arctan u)=\frac{u'}{1+u^2}
$$
""",
        ),
        BoardStep(
            latex_line=r"u=x^3\Rightarrow u'=3x^2",
            teacher_explain_md=r"Compute inner derivative.",
        ),
        BoardStep(
            latex_line=r"y'=\frac{3x^2}{1+(x^3)^2}=\frac{3x^2}{1+x^6}",
            teacher_explain_md=r"Substitute and simplify.",
        ),
    ]
    return steps


def _sim_vdw_steps():
    steps = [
        BoardStep(
            latex_line=r"\left(P+\frac{5}{V^2}\right)(V-0.03)=9.7",
            teacher_explain_md=r"""
**Real-life application (Objective 4.8.8):** Pressure–volume relationship.

Assume $V$ depends on $P$ (so $V=V(P)$).  
**Student task:** Differentiate implicitly and find $\frac{dV}{dP}$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d}{dP}\left[\left(P+5V^{-2}\right)(V-0.03)\right]=0",
            teacher_explain_md=r"""
Differentiate both sides w.r.t. $P$.  
Right side derivative is $0$.
""",
        ),
        BoardStep(
            latex_line=r"\left(1-10V^{-3}\frac{dV}{dP}\right)(V-0.03)+\left(P+5V^{-2}\right)\frac{dV}{dP}=0",
            teacher_explain_md=r"""
Product rule + chain rule.

- $\frac{d}{dP}(P)=1$
- $\frac{d}{dP}(5V^{-2})=5(-2)V^{-3}\frac{dV}{dP}=-10V^{-3}\frac{dV}{dP}$
- $\frac{d}{dP}(V-0.03)=\frac{dV}{dP}$
""",
        ),
        BoardStep(
            latex_line=r"\Big[-10V^{-3}(V-0.03)+P+5V^{-2}\Big]\frac{dV}{dP}=0.03-V",
            teacher_explain_md=r"""
Collect all $\frac{dV}{dP}$ terms on one side.

Everything else moves to the other side.
""",
        ),
        BoardStep(
            latex_line=r"\frac{dV}{dP}=\frac{0.03-V}{-10V^{-3}(V-0.03)+P+5V^{-2}}",
            teacher_explain_md=r"""
Final derivative:
$$
\frac{dV}{dP}=\frac{0.03-V}{-10V^{-3}(V-0.03)+P+5V^{-2}}
$$
""",
        ),
    ]
    return steps


def _sim_ballplayer_gaze_steps():
    steps = [
        BoardStep(
            latex_line=r"\tan(\theta)=\frac{d}{2}",
            teacher_explain_md=r"""
**Real-life application (Objective 4.8.8):** Ballplayer’s gaze.

Batter is $2$ ft from home plate.  
Ball is $d$ ft from home plate (changing with time).

**Student task:** Find $\frac{d\theta}{dt}$ when the ball crosses home plate ($d=0$) given $\frac{dd}{dt}=-130$ ft/s.
""",
        ),
        BoardStep(
            latex_line=r"\theta=\arctan\left(\frac{d}{2}\right)",
            teacher_explain_md=r"""
Convert to inverse trig form so we can differentiate:
$$
\theta=\arctan\left(\frac{d}{2}\right)
$$
""",
        ),
        BoardStep(
            latex_line=r"\frac{d\theta}{dt}=\frac{1}{1+\left(\frac{d}{2}\right)^2}\cdot \frac{d}{dt}\left(\frac{d}{2}\right)",
            teacher_explain_md=r"""
Chain rule:
$$
\frac{d}{dt}(\arctan u)=\frac{u'}{1+u^2}
$$
where $u=\frac{d}{2}$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d\theta}{dt}=\frac{1}{1+\left(\frac{d}{2}\right)^2}\cdot \frac{1}{2}\frac{dd}{dt}",
            teacher_explain_md=r"""
Since $u=\frac{d}{2}$, then $u'=\frac{1}{2}\frac{dd}{dt}$.
""",
        ),
        BoardStep(
            latex_line=r"\frac{d\theta}{dt}=\frac{2\,\frac{dd}{dt}}{4+d^2}",
            teacher_explain_md=r"""
Simplify:
$$
\frac{1}{1+(d/2)^2}\cdot \frac{1}{2}
=\frac{2}{4+d^2}
$$
So:
$$
\frac{d\theta}{dt}=\frac{2\,\frac{dd}{dt}}{4+d^2}
$$
""",
        ),
        BoardStep(
            latex_line=r"\text{At }d=0,\ \frac{dd}{dt}=-130:\ \frac{d\theta}{dt}=\frac{2(-130)}{4}=-65\ \text{rad/s}",
            teacher_explain_md=r"Substitute $d=0$ (crossing home plate) and $\frac{dd}{dt}=-130$.",
        ),
    ]
    return steps


# ------------------------------------------------------------
# Practice bank (15+ questions) — KEEP UNCHANGED
# ------------------------------------------------------------
def _practice_questions():
    qs = []

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } x^2+y^2=25.",
            "hint_md": r"Differentiate both sides. Remember: \[\frac{d}{dx}(y^2)=2y\,y'\]",
            "ans_steps_latex": [
                r"x^2+y^2=25",
                r"\frac{d}{dx}(x^2)+\frac{d}{dx}(y^2)=\frac{d}{dx}(25)",
                r"2x+2y\,y'=0",
                r"2y\,y'=-2x",
                r"y'=-\frac{x}{y}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } x^3+y^3=6.",
            "hint_md": r"Chain rule: \[\frac{d}{dx}(y^3)=3y^2y'\]",
            "ans_steps_latex": [
                r"x^3+y^3=6",
                r"3x^2+3y^2y'=0",
                r"3y^2y'=-3x^2",
                r"y'=-\frac{x^2}{y^2}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } xy=10.",
            "hint_md": r"Product rule: \[\frac{d}{dx}(xy)=x y' + y\]",
            "ans_steps_latex": [
                r"xy=10",
                r"\frac{d}{dx}(xy)=\frac{d}{dx}(10)",
                r"x y' + y = 0",
                r"xy'=-y",
                r"y'=-\frac{y}{x}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } xy+\sin(y)=x^2.",
            "hint_md": r"Product rule for \(xy\) and chain rule for \(\sin(y)\).",
            "ans_steps_latex": [
                r"xy+\sin(y)=x^2",
                r"\frac{d}{dx}(xy)+\frac{d}{dx}(\sin y)=\frac{d}{dx}(x^2)",
                r"(x y' + y)+\cos(y)\,y'=2x",
                r"(x+\cos y)y'=2x-y",
                r"y'=\frac{2x-y}{x+\cos y}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } \ln(x)+\ln(y)=3.",
            "hint_md": r"Differentiate: \[\frac{d}{dx}(\ln y)=\frac{y'}{y}\]",
            "ans_steps_latex": [
                r"\ln(x)+\ln(y)=3",
                r"\frac{1}{x}+\frac{y'}{y}=0",
                r"\frac{y'}{y}=-\frac{1}{x}",
                r"y'=-\frac{y}{x}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{For } x^2+y^2=25,\ \text{find the slope at }(3,4).",
            "hint_md": r"First find \(y'\), then substitute the point.",
            "ans_steps_latex": [
                r"x^2+y^2=25 \Rightarrow y'=-\frac{x}{y}",
                r"m=y'(3,4)=-\frac{3}{4}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find the tangent line to }x^2+y^2=25\text{ at }(3,4).",
            "hint_md": r"Use \(y-y_1=m(x-x_1)\) with \(m=-x/y\).",
            "ans_steps_latex": [
                r"y'=-\frac{x}{y}",
                r"m=-\frac{3}{4}",
                r"y-4=-\frac{3}{4}(x-3)",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{For }x^2+y^2=25,\ \text{find } \frac{d^2y}{dx^2}\text{ in terms of }x,y.",
            "hint_md": r"Start with \(y'=-x/y\). Differentiate using product rule on \(-x\,y^{-1}\).",
            "ans_steps_latex": [
                r"y'=-\frac{x}{y}=-x\,y^{-1}",
                r"y''=\frac{d}{dx}(-x\,y^{-1})",
                r"y''=-(1)\cdot y^{-1}-x\cdot(-1)y^{-2}\cdot y'",
                r"y''=-\frac{1}{y}+\frac{x\,y'}{y^2}",
                r"y''=-\frac{1}{y}+\frac{x}{y^2}\left(-\frac{x}{y}\right)",
                r"y''=-\frac{1}{y}-\frac{x^2}{y^3}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\frac{d}{dx}\left(\arcsin(x)\right)",
            "hint_md": r"Memorise: \[\frac{d}{dx}(\arcsin x)=\frac{1}{\sqrt{1-x^2}}\]",
            "ans_steps_latex": [r"\frac{d}{dx}(\arcsin x)=\frac{1}{\sqrt{1-x^2}}"],
        }
    )

    qs.append(
        {
            "q_latex": r"\frac{d}{dx}\left(\arccos(x)\right)",
            "hint_md": r"Same denominator as arcsin, but negative sign.",
            "ans_steps_latex": [r"\frac{d}{dx}(\arccos x)=-\frac{1}{\sqrt{1-x^2}}"],
        }
    )

    qs.append(
        {
            "q_latex": r"\frac{d}{dx}\left(\arctan(x)\right)",
            "hint_md": r"Memorise: \[\frac{d}{dx}(\arctan x)=\frac{1}{1+x^2}\]",
            "ans_steps_latex": [r"\frac{d}{dx}(\arctan x)=\frac{1}{1+x^2}"],
        }
    )

    qs.append(
        {
            "q_latex": r"\frac{d}{dx}\left(\arcsin(3x)\right)",
            "hint_md": r"Chain rule: \[\frac{d}{dx}(\arcsin u)=\frac{u'}{\sqrt{1-u^2}}\]",
            "ans_steps_latex": [
                r"y=\arcsin(3x)",
                r"u=3x\Rightarrow u'=3",
                r"y'=\frac{u'}{\sqrt{1-u^2}}=\frac{3}{\sqrt{1-(3x)^2}}",
                r"y'=\frac{3}{\sqrt{1-9x^2}}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\frac{d}{dx}\left(\arctan(x^2)\right)",
            "hint_md": r"Chain rule: \[\frac{d}{dx}(\arctan u)=\frac{u'}{1+u^2}\]",
            "ans_steps_latex": [
                r"y=\arctan(x^2)",
                r"u=x^2\Rightarrow u'=2x",
                r"y'=\frac{2x}{1+(x^2)^2}",
                r"y'=\frac{2x}{1+x^4}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\frac{d}{dx}\left(x\,\arcsin(x)\right)",
            "hint_md": r"Product rule and \(\frac{d}{dx}(\arcsin x)=\frac{1}{\sqrt{1-x^2}}\).",
            "ans_steps_latex": [
                r"y=x\,\arcsin(x)",
                r"y' = 1\cdot\arcsin(x)+x\cdot\frac{1}{\sqrt{1-x^2}}",
                r"y'=\arcsin(x)+\frac{x}{\sqrt{1-x^2}}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } \arcsin(y)=x.",
            "hint_md": r"Take sine of both sides: \(\sin(\arcsin(y))=\sin(x)\).",
            "ans_steps_latex": [
                r"\arcsin(y)=x",
                r"\sin(\arcsin(y))=\sin(x)\Rightarrow y=\sin(x)",
                r"y'=\cos(x)",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } \arctan(y)=x^2.",
            "hint_md": r"Take tangent: \(y=\tan(x^2)\), then chain rule.",
            "ans_steps_latex": [
                r"\arctan(y)=x^2",
                r"\tan(\arctan(y))=\tan(x^2)\Rightarrow y=\tan(x^2)",
                r"y'=\sec^2(x^2)\cdot 2x",
                r"y'=2x\sec^2(x^2)",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Find } \frac{dy}{dx}\text{ if } \sin(xy)=x.",
            "hint_md": r"Differentiate: \(\frac{d}{dx}(\sin u)=\cos(u)\,u'\) with \(u=xy\).",
            "ans_steps_latex": [
                r"\sin(xy)=x",
                r"\cos(xy)\cdot\frac{d}{dx}(xy)=1",
                r"\cos(xy)\cdot(xy'+y)=1",
                r"x y' + y = \frac{1}{\cos(xy)}=\sec(xy)",
                r"xy'=\sec(xy)-y",
                r"y'=\frac{\sec(xy)-y}{x}",
            ],
        }
    )

    qs.append(
        {
            "q_latex": r"\text{Differentiate: } y=\arccos(2x-1).",
            "hint_md": r"Chain rule: \(\frac{d}{dx}(\arccos u)=-\frac{u'}{\sqrt{1-u^2}}\).",
            "ans_steps_latex": [
                r"y=\arccos(2x-1)",
                r"u=2x-1\Rightarrow u'=2",
                r"y'=-\frac{2}{\sqrt{1-(2x-1)^2}}",
            ],
        }
    )

    return qs


# ------------------------------------------------------------
# Main render()
# ------------------------------------------------------------
def render():
    st.header("Subtopic 4.8: Implicit Differentiation and Inverse Trigonometric Functions")
    st.caption("Source: Al Diwan Advanced Stream Mathematics – G12 ADV Lesson 3.8")

    # -------------------------
    # LEARN (FIXED: all math humanised)
    # -------------------------
    st.markdown("### Lesson Objectives (as required)")
    st.markdown("**4.8.1** Differentiate between an explicitly and implicitly defined function.")
    st.markdown(
        "**4.8.2** Find derivatives implicitly: break down the sequence of steps needed to isolate $y'$.  \n"
        "*Include cases involving trigonometric, radical, exponential, and logarithmic elements.*"
    )
    st.markdown("**4.8.3** Show examples of finding the second derivative $y''$, implicitly.")
    st.markdown("**4.8.4** Find the slope and equation of a tangent line by using implicit differentiation.")
    st.markdown(
        "**4.8.5** Find the derivative for any rational exponent — explain the proof as an application of implicit differentiation."
    )
    st.markdown("**4.8.6** Paying attention to the domain restrictions: Find the derivatives of the six inverse-trigonometric functions.")
    st.latex(
        r"""
\begin{aligned}
\frac{d}{dx}\left(\arcsin x\right)&=\frac{1}{\sqrt{1-x^2}},\quad -1<x<1\\
\frac{d}{dx}\left(\arccos x\right)&=-\frac{1}{\sqrt{1-x^2}},\quad -1<x<1\\
\frac{d}{dx}\left(\arctan x\right)&=\frac{1}{1+x^2},\quad x\in\mathbb{R}\\
\frac{d}{dx}\left(\operatorname{arccot} x\right)&=-\frac{1}{1+x^2},\quad x\in\mathbb{R}\\
\frac{d}{dx}\left(\operatorname{arcsec} x\right)&=\frac{1}{|x|\sqrt{x^2-1}},\quad |x|>1\\
\frac{d}{dx}\left(\operatorname{arccsc} x\right)&=-\frac{1}{|x|\sqrt{x^2-1}},\quad |x|>1
\end{aligned}
"""
    )
    st.markdown(
        "**4.8.7** Apply the formulas to find derivatives of composition of functions that include inverse-trigonometric components "
        "(chain rule and other rules involved)."
    )
    st.markdown(
        "**4.8.8** Use inverse and implicit differentiation to solve real life applications such as change in a ballplayer’s gaze, "
        "volume change with respect to pressure, etc."
    )

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.subheader("4.8.1 Explicit vs implicit (very clear)")
        st.markdown(
            r"""
**Explicit function:** $y$ is already isolated: $y=f(x)$.  
Example: $y=3x^2-5$.

**Implicit function:** $x$ and $y$ are mixed in one equation.  
Example: $x^2+y^2=25$.

**Why implicit differentiation matters:**  
Even if you cannot (or should not) solve for $y$, you can still find the slope $y'$ and tangent lines directly.
"""
        )

        _tip_box(
            "Teacher tips (high impact)",
            [
                "Say out loud before differentiating: **“$y$ is a function of $x$”**.",
                "Every time you differentiate something with $y$, immediately attach a $y'$. Example: $\\frac{d}{dx}(y^2)=2y\\,y'$.",
                "After solving for $y'$, scan the final answer: do you see **exactly one $y'$** (not many)?",
            ],
            kind="info",
        )

        st.markdown("---")
        st.subheader("4.8.2 Implicit derivatives (trig / radical / exponential / logarithmic)")

        st.markdown("### Example A — Implicit differentiation (circle)")
        st.markdown(
            r"""
**Student Task (what you do):**
- Differentiate $x^2+y^2=25$ with respect to $x$.
- Use chain rule correctly on $y^2$.
- Isolate $y'$.

**Expected final form:** $y'=\text{(expression in }x\text{ and }y)$.
"""
        )
        render_simulation(_sim_implicit_circle_steps(), "Mini Blackboard — Implicit differentiation (circle)")

        st.markdown("---")
        st.markdown("### Example B — Tangent line by implicit differentiation (Example 8.1)")
        st.markdown(
            r"""
**Student Task (what you do):**
1) Find $y'$ for $x^2+y^3-2y=3$.  
2) Evaluate slope at $(2,1)$.  
3) Write the tangent line equation.

**Expected final outputs:**
- $y'=\dots$ (general formula)
- slope $m$ at the point
- tangent line in point-slope form
"""
        )
        render_simulation(_sim_example_8_1_tangent_steps(), "Mini Blackboard — Tangent line (Example 8.1)")

        st.markdown("---")
        st.markdown("### Example C — Product rule + implicit tangent (Example 8.2)")
        st.markdown(
            r"""
**Student Task (what you do):**
1) Differentiate $x^2y^2-2x=4-4y$ implicitly.  
2) Solve for $y'$.  
3) Evaluate the slope at $(2,-2)$.  
4) Write the tangent line equation.

**Big warning:** This is where students forget product rule OR forget the $y'$ on $y^2$.
"""
        )
        render_simulation(_sim_example_8_2_tangent_steps(), "Mini Blackboard — Tangent line (Example 8.2)")

        st.markdown("---")
        st.markdown("### Example D — Radical implicit differentiation")
        st.markdown(
            r"""
**Student Task:** Differentiate $\sqrt{x}+\sqrt{y}=10$ and isolate $y'$.

**Expected final output:** a simplified $y'$ using radicals.
"""
        )
        render_simulation(_sim_radical_implicit_steps(), "Mini Blackboard — Radicals (implicit)")

        st.markdown("---")
        st.markdown("### Example E — Logarithmic implicit differentiation")
        st.markdown(
            r"""
**Student Task:** Differentiate $\ln(xy)=y$ and isolate $y'$.

**Expected final output:** $y'=\dfrac{y}{x(y-1)}$.
"""
        )
        render_simulation(_sim_log_implicit_steps(), "Mini Blackboard — Logarithms (implicit)")

        st.markdown("---")
        st.subheader("4.8.3 Second derivative implicitly (exponential case — Example 8.4)")
        st.markdown(
            r"""
This example is important because it shows:
- You can find $y''$ **without ever solving for $y$** explicitly.
- Evaluating at a point early can keep the algebra clean.

**Student Task:** Find $y''$ for $y^2+2e^{-xy}=6$, then compute $y''(0)$ at $(0,2)$.
"""
        )
        render_simulation(_sim_second_derivative_exp_steps(), "Mini Blackboard — Second derivative (Example 8.4)")

        st.markdown("---")
        st.subheader("4.8.4 Slope + tangent line (visual reinforcement)")
        st.markdown("Once you have $y'$, the **slope at a point** $(x_0,y_0)$ is:")
        st.latex(r"m=y'(x_0,y_0)")
        st.markdown("Then the tangent line is:")
        st.latex(r"y-y_0=m(x-x_0)")

        st.markdown("#### Visual: circle $x^2+y^2=25$ + tangent line at a chosen point")
        colA, colB = st.columns([1, 1])
        with colA:
            x0 = st.slider("Choose x-coordinate", -4.5, 4.5, 3.0, 0.1, key="imp_circle_x0")
        with colB:
            branch = st.selectbox("Choose branch", ["upper", "lower"], index=0, key="imp_circle_branch")

        fig, x0v, y0v, m = _plot_circle_and_tangent(x0, branch=branch)
        _small_graph(fig)

        st.markdown("**At the selected point:**")
        st.latex(r"x_0=" + f"{x0v:.2f}" + r"\quad,\quad y_0=" + f"{y0v:.2f}")
        st.latex(r"\frac{dy}{dx}=-\frac{x}{y}")
        st.latex(r"m=-\frac{x_0}{y_0}=" + f"{m:.4f}")
        st.latex(r"\text{Tangent line:}\quad y-y_0=m(x-x_0)")

        _tip_box(
            "Quick sign check (helps students self-correct)",
            [
                "Upper branch: $y>0$. If $x>0$, then $-x/y<0$ (tangent slopes down).",
                "Lower branch: $y<0$. If $x>0$, then $-x/y>0$ (tangent slopes up).",
            ],
            kind="success",
        )

        st.markdown("---")
        st.subheader("4.8.5 Rational exponents (proof idea using implicit differentiation)")
        st.markdown("Let $y=x^{p/q}$ where $p,q$ are integers ($q\\neq 0$). Raise both sides to power $q$:")
        st.latex(r"y^q=x^p")
        st.markdown("Differentiate implicitly:")
        st.latex(r"q y^{q-1}y' = p x^{p-1}")
        st.markdown("Solve for $y'$:")
        st.latex(r"y'=\frac{p x^{p-1}}{q y^{q-1}}")
        st.markdown("Then substitute $y=x^{p/q}$ back to express the derivative in terms of $x$ only.")

        _tip_box(
            "Teacher tip",
            [
                "This proof is exactly what justifies the power rule for rational exponents.",
                "Students should clearly show where chain rule creates the $y'$.",
            ],
            kind="info",
        )

        st.markdown("---")
        st.subheader("4.8.6 The six inverse trig derivatives (with domain restrictions)")
        st.latex(
            r"""
\begin{aligned}
\frac{d}{dx}\left(\arcsin x\right)&=\frac{1}{\sqrt{1-x^2}},\quad -1<x<1\\
\frac{d}{dx}\left(\arccos x\right)&=-\frac{1}{\sqrt{1-x^2}},\quad -1<x<1\\
\frac{d}{dx}\left(\arctan x\right)&=\frac{1}{1+x^2},\quad x\in\mathbb{R}\\
\frac{d}{dx}\left(\operatorname{arccot} x\right)&=-\frac{1}{1+x^2},\quad x\in\mathbb{R}\\
\frac{d}{dx}\left(\operatorname{arcsec} x\right)&=\frac{1}{|x|\sqrt{x^2-1}},\quad |x|>1\\
\frac{d}{dx}\left(\operatorname{arccsc} x\right)&=-\frac{1}{|x|\sqrt{x^2-1}},\quad |x|>1
\end{aligned}
"""
        )

        _tip_box(
            "Common exam mistakes (warn students explicitly)",
            [
                "For $\\arccos x$, students often forget the negative sign.",
                "For $\\operatorname{arcsec}x$ and $\\operatorname{arccsc}x$, students often forget the **absolute value** $|x|$.",
                "Domain matters: $\\sqrt{1-x^2}$ requires $-1<x<1$.",
            ],
            kind="warning",
        )

        st.markdown("#### Visual: inverse trig function + its derivative")
        which = st.selectbox(
            "Choose a function to visualise",
            ["arcsin", "arccos", "arctan"],
            index=0,
            key="inv_trig_plot_pick",
        )
        _small_graph(_plot_inverse_trig_family(which))

        st.markdown("---")
        st.subheader("4.8.7 Derive the key formulas (so students trust the rules)")

        st.markdown("### Derivation 1 — $\\dfrac{d}{dx}(\\arcsin x)$")
        render_simulation(_sim_derive_arcsin_steps(), "Mini Blackboard — Derive d/dx(arcsin x)")

        st.markdown("### Derivation 2 — $\\dfrac{d}{dx}(\\arctan x)$")
        render_simulation(_sim_derive_arctan_steps(), "Mini Blackboard — Derive d/dx(arctan x)")

        st.markdown("---")
        st.subheader("4.8.7 Chain rule with inverse trig (Example 8.5 style)")

        st.markdown("### Example 8.5(a) — Differentiate $\\arccos(3x^2)$")
        render_simulation(_sim_chain_rule_arccos_steps(), "Mini Blackboard — Chain rule (arccos)")

        st.markdown("### Example 8.5(b) — Differentiate $(\\operatorname{arcsec}x)^2$")
        render_simulation(_sim_chain_rule_arcsec_squared_steps(), "Mini Blackboard — Chain rule (arcsec squared)")

        st.markdown("### Example 8.5(c) — Differentiate $\\arctan(x^3)$")
        render_simulation(_sim_chain_rule_arctan_x3_steps(), "Mini Blackboard — Chain rule (arctan)")

        st.markdown("---")
        st.subheader("4.8.8 Real-life applications (explicitly required)")

        st.markdown("### Application 1 — Volume change with respect to pressure (Example 8.3)")
        st.markdown(
            r"""
**Student Task (what you do):**
- Treat $V$ as a function of $P$: $V=V(P)$.
- Differentiate the equation implicitly with respect to $P$.
- Solve for $\frac{dV}{dP}$.
"""
        )
        render_simulation(_sim_vdw_steps(), "Mini Blackboard — van der Waals (Example 8.3)")

        st.markdown("#### Quick evaluation (numeric substitution)")
        P = st.slider("Choose $P$", 0.0, 10.0, 5.0, 0.1, key="vdw_P")
        V = st.slider("Choose $V$", 0.2, 3.0, 1.0, 0.01, key="vdw_V")

        denom = (-10 * (V ** -3) * (V - 0.03)) + P + (5 * (V ** -2))
        dVdP = (0.03 - V) / denom
        st.latex(r"\frac{dV}{dP}=" + f"{dVdP:.6f}")

        _tip_box(
            "Interpretation (students must say this in words)",
            [
                "If the value is negative, increasing pressure causes volume to decrease (typical gas behaviour).",
                "The derivative is a rate: “volume units per pressure unit.”",
            ],
            kind="info",
        )

        st.markdown("---")
        st.markdown("### Application 2 — Ballplayer’s gaze (Example 8.6)")
        st.markdown(
            r"""
**Student Task (what you do):**
- Write $\theta$ in inverse trig form.
- Differentiate with respect to time $t$.
- Substitute $d=0$ and $\frac{dd}{dt}=-130$ ft/s.

**Key idea:** the angle changes because the distance changes.
"""
        )
        render_simulation(_sim_ballplayer_gaze_steps(), "Mini Blackboard — Ballplayer gaze (Example 8.6)")

        st.markdown("#### Interactive: change $d$ and $\\frac{dd}{dt}$ and see $\\frac{d\\theta}{dt}$")
        d = st.slider("Distance $d$ (ft)", 0.0, 60.0, 0.0, 0.5, key="gaze_d")
        dd_dt = st.slider("Velocity $\\frac{dd}{dt}$ (ft/s)", -200.0, 50.0, -130.0, 1.0, key="gaze_dddt")

        dtheta_dt = (2 * dd_dt) / (4 + d * d)
        st.latex(r"\frac{d\theta}{dt}=" + f"{dtheta_dt:.6f}" + r"\ \text{rad/s}")

        _tip_box(
            "Why this shocks students (important concept message)",
            [
                r"At $d=0$, the rate becomes $\frac{2\,dd/dt}{4}$, which can be large in magnitude.",
                "This explains why “keeping your eye on the ball” near the plate is physically difficult.",
            ],
            kind="warning",
        )

    # -------------------------
    # PRACTICE (KEEP UNCHANGED)
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
                if st.button("Hint", key=f"q48_hint_{i}"):
                    st.info("")
                    _md_math(q["hint_md"])
            with c2:
                if st.button("Show Answer", key=f"q48_ans_{i}"):
                    st.success("Solution (step-by-step):")
                    for step in q["ans_steps_latex"]:
                        _latex_block(step)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
