# subtopic_5_2_indeterminate_forms_lhopitals_rule.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

from simulations import BoardStep, render_simulation
import subtopic_5_2_indeterminate_forms_lhopitals_rule_practice as practice_module


# -----------------------------
# Helpers (LaTeX-first + student-friendly)
# -----------------------------
def _step(latex_line: str, explain_md: str) -> BoardStep:
    return BoardStep(latex_line=latex_line, teacher_explain_md=explain_md)


def _callout(kind: str, title: str, body_md: str) -> None:
    styles = {
        "tip": {
            "border": "#2563eb",
            "bg": "#f7fbff",
            "title": "#1d4ed8",
            "text": "#111827",
        },
        "warning": {
            "border": "#f59e0b",
            "bg": "#fffbeb",
            "title": "#b45309",
            "text": "#111827",
        },
        "check": {
            "border": "#16a34a",
            "bg": "#f0fdf4",
            "title": "#166534",
            "text": "#052e16",
        },
    }
    s = styles.get(kind, styles["tip"])
    st.markdown(
        f"""
<div style="border:1px solid {s['border']}33;border-left:6px solid {s['border']};border-radius:12px;padding:12px 14px;background:{s['bg']};margin:10px 0;">
  <div style="font-weight:900;color:{s['title']};margin-bottom:6px;">{title}</div>
  <div style="color:{s['text']};line-height:1.6;">{body_md}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _exam_block(title: str, question_latex: str, tasks_md: str) -> None:
    st.markdown(f"### {title}")
    st.markdown("**Question**")
    st.latex(question_latex)
    st.markdown("**What your answer must include**")
    st.markdown(tasks_md)


def _fig_axes():
    # Smaller graphs (as requested)
    fig = plt.figure(figsize=(4.8, 2.6), dpi=150)
    ax = fig.add_subplot(111)
    ax.grid(True, alpha=0.22)
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.7)
    ax.axvline(0, color="black", linewidth=0.8, alpha=0.7)
    return fig, ax


def _limit_table(xs: list[float], fx: list[float]) -> None:
    rows = []
    for x, y in zip(xs, fx):
        if y is None or (isinstance(y, float) and (math.isnan(y) or math.isinf(y))):
            rows.append((x, "undefined"))
        else:
            rows.append((x, y))
    st.table({"x": [r[0] for r in rows], "f(x)": [r[1] for r in rows]})


def _safe_sin_over_x(x: float) -> float:
    if x == 0:
        return float("nan")
    return math.sin(x) / x


# -----------------------------
# Learn sections (Objectives 5.2.1–5.2.4)
# -----------------------------
def _obj_521():
    st.subheader(
        "Objective 5.2.1 — Recognize indeterminate forms and solve by factoring, conjugate, and linear approximation"
    )

    _callout(
        "tip",
        "What an indeterminate form is",
        "An indeterminate form happens when direct substitution gives a form that does not reveal the limit value. "
        "You must simplify or transform the expression to uncover the true behavior near the point.",
    )

    st.markdown("**Two key indeterminate forms here:**")
    st.latex(r"\frac{0}{0}\qquad\frac{\infty}{\infty}")

    _callout(
        "check",
        "Your first move",
        "Try direct substitution. If you get an indeterminate form, stop and choose the best method: factoring, conjugate, or a known approximation.",
    )

    st.markdown("### A. Factoring to resolve a limit")
    _exam_block(
        "Example 1 (factoring)",
        r"\lim_{x\to 1}\frac{x^2-1}{x-1}",
        "- Factor the numerator fully.\n"
        "- Cancel the common factor.\n"
        "- Substitute to finish.",
    )
    steps = [
        _step(
            r"\lim_{x\to 1}\frac{x^2-1}{x-1}",
            "Direct substitution gives an indeterminate form, so simplify first.",
        ),
        _step(r"x^2-1=(x-1)(x+1)", "Factor the difference of squares."),
        _step(
            r"\lim_{x\to 1}\frac{(x-1)(x+1)}{x-1}=\lim_{x\to 1}(x+1)",
            "Cancel the common factor.",
        ),
        _step(r"\lim_{x\to 1}(x+1)=2", "Substitute to finish."),
    ]
    render_simulation(steps, "5.2.1 — Factoring method (Example 1)")

    st.markdown("### B. Multiplying by the conjugate")
    _exam_block(
        "Example 2 (conjugate)",
        r"\lim_{x\to 0}\frac{\sqrt{1+x}-1}{x}",
        "- Multiply numerator and denominator by the conjugate.\n"
        "- Simplify completely.\n"
        "- Substitute to finish.",
    )
    steps2 = [
        _step(
            r"\lim_{x\to 0}\frac{\sqrt{1+x}-1}{x}",
            "Use the conjugate to remove the square root from the numerator.",
        ),
        _step(
            r"\frac{\sqrt{1+x}-1}{x}\cdot\frac{\sqrt{1+x}+1}{\sqrt{1+x}+1}",
            "Multiply by the conjugate.",
        ),
        _step(
            r"\frac{(1+x)-1}{x\bigl(\sqrt{1+x}+1\bigr)}=\frac{x}{x\bigl(\sqrt{1+x}+1\bigr)}",
            "Simplify the numerator.",
        ),
        _step(r"\frac{1}{\sqrt{1+x}+1}", "Cancel the common factor."),
        _step(r"\lim_{x\to 0}\frac{1}{\sqrt{1+x}+1}=\frac{1}{2}", "Substitute to finish."),
    ]
    render_simulation(steps2, "5.2.1 — Conjugate method (Example 2)")

    st.markdown("### C. Linear approximation for a classic trigonometric limit")
    st.markdown("A powerful fact near the origin is the approximation below.")
    st.latex(r"\sin x\approx x\quad\text{for }x\text{ near }0")
    st.latex(r"\lim_{x\to 0}\frac{\sin x}{x}=1")

    _callout(
        "tip",
        "What you should notice",
        "Near the origin, the sine curve behaves almost like a straight line. The ratio becomes close to a constant.",
    )

    st.markdown("#### Visual: values of the ratio near the origin (table always visible)")
    xs = [-0.5, -0.2, -0.1, -0.05, -0.02, 0.02, 0.05, 0.1, 0.2, 0.5]
    fx = [_safe_sin_over_x(x) for x in xs]
    _limit_table(xs, fx)

    fig, ax = _fig_axes()
    x_plot = np.linspace(-0.7, 0.7, 500)
    y_plot = np.sin(x_plot) / x_plot
    y_plot[np.isclose(x_plot, 0.0)] = np.nan
    ax.plot(x_plot, y_plot, linewidth=2)
    ax.set_title("Behavior of the ratio near the origin")
    ax.set_xlabel("x")
    ax.set_ylabel("ratio")
    ax.set_ylim(0.6, 1.4)
    st.pyplot(fig, use_container_width=True)


def _obj_522():
    st.subheader("Objective 5.2.2 — Apply L’Hôpital’s Rule for the two quotient forms")

    st.markdown("The two quotient forms you are allowed to use with the rule are:")
    st.latex(r"\frac{0}{0}\qquad\frac{\infty}{\infty}")

    _callout(
        "warning",
        "When you are allowed to use the rule",
        "You can apply the rule only when the limit is a quotient and substitution gives one of the two required indeterminate forms. "
        "Both functions must be differentiable near the limit point.",
    )

    st.markdown("**L’Hôpital’s Rule:**")
    st.latex(
        r"\text{If }\lim_{x\to a}\frac{f(x)}{g(x)}\text{ has the form }\frac{0}{0}\text{ or }\frac{\infty}{\infty},"
    )
    st.latex(
        r"\text{then }\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)}\text{ (when the right-hand limit exists).}"
    )

    st.markdown("### Re-solve using the rule")
    _exam_block(
        "Example 1",
        r"\lim_{x\to 0}\frac{1-\cos x}{\sin x}",
        "- Confirm the indeterminate form by substitution.\n"
        "- Apply the rule once.\n"
        "- Substitute to finish.",
    )

    steps = [
        _step(r"\lim_{x\to 0}\frac{1-\cos x}{\sin x}", "Substitution gives the required indeterminate form."),
        _step(
            r"=\lim_{x\to 0}\frac{\frac{d}{dx}(1-\cos x)}{\frac{d}{dx}(\sin x)}",
            "Apply the rule.",
        ),
        _step(r"=\lim_{x\to 0}\frac{\sin x}{\cos x}", "Differentiate numerator and denominator."),
        _step(r"=\frac{0}{1}=0", "Substitute to finish."),
    ]
    render_simulation(steps, "5.2.2 — L’Hôpital once (Example 1)")

    st.markdown("### Another example for the quotient form")
    st.latex(r"\frac{\infty}{\infty}")
    _exam_block(
        "Example 2",
        r"\lim_{x\to\infty}\frac{e^{x}}{x}",
        "- Confirm the form.\n"
        "- Apply the rule once.\n"
        "- Interpret the result.",
    )

    steps2 = [
        _step(r"\lim_{x\to\infty}\frac{e^{x}}{x}", "Both numerator and denominator grow without bound."),
        _step(r"\frac{\infty}{\infty}", "The form matches the rule."),
        _step(r"=\lim_{x\to\infty}\frac{\frac{d}{dx}(e^{x})}{\frac{d}{dx}(x)}", "Apply the rule."),
        _step(r"=\lim_{x\to\infty}\frac{e^{x}}{1}", "Differentiate."),
        _step(r"=\infty", "The exponential growth dominates linear growth."),
    ]
    render_simulation(steps2, "5.2.2 — L’Hôpital (Example 2)")


def _obj_523():
    st.subheader("Objective 5.2.3 — Successive applications, hypothesis checks, and rewriting")

    _callout(
        "tip",
        "A reliable workflow",
        "Confirm the indeterminate form, apply the rule, simplify, and re-check the form. If it is still indeterminate, you may apply the rule again.",
    )

    st.markdown("### A. Multiple successive applications")
    _exam_block(
        "Example 1 (two applications)",
        r"\lim_{x\to\infty}\frac{x^{2}}{e^{x}}",
        "- Confirm the form.\n"
        "- Apply the rule twice.\n"
        "- Conclude the limit.",
    )

    steps = [
        _step(r"\lim_{x\to\infty}\frac{x^{2}}{e^{x}}", "This is a quotient with the required form."),
        _step(r"\frac{\infty}{\infty}", "Both grow without bound."),
        _step(r"=\lim_{x\to\infty}\frac{2x}{e^{x}}", "First application."),
        _step(r"\frac{\infty}{\infty}", "Still indeterminate."),
        _step(r"=\lim_{x\to\infty}\frac{2}{e^{x}}", "Second application."),
        _step(r"=0", "The denominator grows without bound."),
    ]
    render_simulation(steps, "5.2.3 — Two applications (Example 1)")

    st.markdown("### B. Rewrite first when the expression is not a quotient")
    _callout(
        "warning",
        "Mistake to avoid",
        "Do not apply the rule if the expression is not a quotient in the required form. Rewrite first.",
    )

    _exam_block(
        "Example 2",
        r"\lim_{x\to\infty}\frac{1}{x\ln x}",
        "- Rewrite into a quotient with the required form.\n"
        "- Apply the rule once.",
    )

    steps2 = [
        _step(r"\lim_{x\to\infty}\frac{1}{x\ln x}", "Rewrite into a quotient that matches the rule."),
        _step(r"=\lim_{x\to\infty}\frac{\ln x}{x}", "Rewrite."),
        _step(r"\frac{\infty}{\infty}", "Now the form matches."),
        _step(r"=\lim_{x\to\infty}\frac{\frac{1}{x}}{1}=0", "Apply the rule."),
    ]
    render_simulation(steps2, "5.2.3 — Rewrite then apply (Example 2)")

    st.markdown("### C. Apply the rule once and then simplify")
    _exam_block(
        "Example 3",
        r"\lim_{x\to 0^{+}}\frac{\ln x}{\csc x}",
        "- Apply the rule once.\n"
        "- Rewrite using trig identities.\n"
        "- Finish using known limits.",
    )

    steps3 = [
        _step(r"\lim_{x\to 0^{+}}\frac{\ln x}{\csc x}", "This is a quotient with the required form."),
        _step(r"\frac{\infty}{\infty}", "The form matches the rule."),
        _step(r"=\lim_{x\to 0^{+}}\frac{\frac{1}{x}}{-\csc x\cot x}", "Apply the rule."),
        _step(r"=\lim_{x\to 0^{+}}\left(-\frac{\sin x}{x\tan x}\right)", "Rewrite using reciprocal identities."),
        _step(r"=-(1)(1)=-1", "Use the classic trigonometric limits."),
    ]
    render_simulation(steps3, "5.2.3 — Simplify after L’Hôpital (Example 3)")


def _obj_524():
    st.subheader("Objective 5.2.4 — Rewrite other indeterminate forms to use L’Hôpital’s Rule")

    st.markdown("Indeterminate forms to rewrite in this objective:")
    st.latex(r"\infty-\infty\qquad 0\cdot\infty\qquad 1^{\infty}\qquad 0^{0}\qquad \infty^{0}")

    _callout(
        "tip",
        "Core idea",
        "Rewrite until you get a quotient with the required form, then apply the rule.",
    )

    st.markdown("### A. Rewrite the difference form")
    st.latex(r"\infty-\infty")
    _exam_block(
        "Example 1",
        r"\lim_{x\to\infty}\left(\sqrt{x^{2}+x}-x\right)",
        "- Multiply by the conjugate.\n"
        "- Simplify to a quotient.\n"
        "- Evaluate the limit.",
    )

    steps = [
        _step(r"\sqrt{x^{2}+x}-x", "Multiply by the conjugate to remove the radical from the difference."),
        _step(
            r"\left(\sqrt{x^{2}+x}-x\right)\cdot\frac{\sqrt{x^{2}+x}+x}{\sqrt{x^{2}+x}+x}",
            "Conjugate multiplication.",
        ),
        _step(
            r"=\frac{(x^{2}+x)-x^{2}}{\sqrt{x^{2}+x}+x}=\frac{x}{\sqrt{x^{2}+x}+x}",
            "Simplify the numerator.",
        ),
        _step(r"=\frac{1}{\sqrt{1+\frac{1}{x}}+1}", "Divide numerator and denominator by the common factor to simplify."),
        _step(r"\lim_{x\to\infty}\frac{1}{\sqrt{1+\frac{1}{x}}+1}=\frac{1}{2}", "Substitute to finish."),
    ]
    render_simulation(steps, "5.2.4 — Conjugate for difference form (Example 1)")

    st.markdown("### B. Rewrite the product form")
    st.latex(r"0\cdot\infty")
    _exam_block(
        "Example 2",
        r"\lim_{x\to\infty}\frac{1}{x\ln x}",
        "- Rewrite into a quotient.\n"
        "- Apply the rule and evaluate.",
    )

    steps2 = [
        _step(r"\frac{1}{x\ln x}=\frac{\ln x}{x}", "Rewrite into a quotient."),
        _step(r"\frac{\infty}{\infty}", "Now the form matches."),
        _step(r"\lim_{x\to\infty}\frac{\ln x}{x}=\lim_{x\to\infty}\frac{\frac{1}{x}}{1}=0", "Apply the rule."),
    ]
    render_simulation(steps2, "5.2.4 — Rewrite product form to quotient (Example 2)")

    st.markdown("### C. Exponential-type indeterminate forms")
    _callout(
        "tip",
        "The log transform",
        "For an expression with a variable exponent, take the natural logarithm, rewrite the limit into a quotient, apply L’Hôpital’s Rule, then exponentiate back.",
    )

    st.latex(r"y=[f(x)]^{g(x)}\quad\Rightarrow\quad \ln y=g(x)\ln\!\bigl(f(x)\bigr)")

    st.markdown("#### Log transform example 3 (expression shown in LaTeX)")
    st.latex(r"\lim_{x\to 0^{+}}(\sin x)^{x}")
    _exam_block(
        "Example 3",
        r"\lim_{x\to 0^{+}}(\sin x)^{x}",
        "- Use the log transform.\n"
        "- Apply the rule after rewriting to a quotient.\n"
        "- Exponentiate back.",
    )

    steps3 = [
        _step(r"y=(\sin x)^{x}\Rightarrow \ln y=x\ln(\sin x)", "Take the natural logarithm."),
        _step(
            r"\lim_{x\to 0^{+}}\ln y=\lim_{x\to 0^{+}}\frac{\ln(\sin x)}{\frac{1}{x}}",
            "Rewrite as a quotient so the rule can be used.",
        ),
        _step(r"\frac{-\infty}{\infty}", "This is a quotient form where L’Hôpital’s Rule applies."),
        _step(
            r"=\lim_{x\to 0^{+}}\frac{\cot x}{-x^{-2}}=\lim_{x\to 0^{+}}\bigl(-x^{2}\cot x\bigr)=0",
            "Differentiate and simplify.",
        ),
        _step(r"\Rightarrow \lim_{x\to 0^{+}}y=e^{0}=1", "Exponentiate back."),
    ]
    render_simulation(steps3, "5.2.4 — Log transform example 3 (unique)")

    st.markdown("#### Log transform example 4 (expression shown in LaTeX)")
    st.latex(r"\lim_{x\to\infty}(x+1)^{2/x}")
    _exam_block(
        "Example 4",
        r"\lim_{x\to\infty}(x+1)^{2/x}",
        "- Use the log transform.\n"
        "- Apply the rule.\n"
        "- Exponentiate back.",
    )

    steps4 = [
        _step(r"y=(x+1)^{2/x}\Rightarrow \ln y=\frac{2\ln(x+1)}{x}", "Take the natural logarithm."),
        _step(r"\frac{\infty}{\infty}", "Now the form matches the rule."),
        _step(r"\lim_{x\to\infty}\ln y=\lim_{x\to\infty}\frac{\frac{2}{x+1}}{1}=0", "Apply L’Hôpital’s Rule."),
        _step(r"\Rightarrow \lim_{x\to\infty}y=e^{0}=1", "Exponentiate back."),
    ]
    render_simulation(steps4, "5.2.4 — Log transform example 4 (unique)")


# -----------------------------
# Entry point
# -----------------------------
def render():
    st.header("Subtopic 5.2: Indeterminate Forms and L’Hôpital’s Rule")
    st.caption("Student version: fully guided explanations, simulations, and practice (no sliders)")

    learn_tab, practice_tab = st.tabs(["Learn", "Practice"])

    with learn_tab:
        st.markdown("### Learning objectives")
        st.markdown(
            "- 5.2.1 Define the indeterminate forms of limits and solve using factoring, conjugates, and linear approximations."
        )
        st.markdown("- 5.2.2 Apply L’Hôpital’s Rule for the two indeterminate quotient forms.")
        st.markdown(
            "- 5.2.3 Solve problems requiring L’Hôpital’s Rule, including successive applications and correct rewriting."
        )
        st.markdown(
            "- 5.2.4 Rewrite other indeterminate forms so they can be solved using L’Hôpital’s Rule."
        )

        st.divider()
        _obj_521()
        st.divider()
        _obj_522()
        st.divider()
        _obj_523()
        st.divider()
        _obj_524()

    with practice_tab:
        practice_module.render()