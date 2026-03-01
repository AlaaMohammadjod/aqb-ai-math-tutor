# subtopic_5_6_curve_sketching_overview.py
# AQB Grade 12 AI Math Tutor — Subtopic 5.6: Overview of Curve Sketching
#
# GUARANTEES:
# - All math is rendered ONLY using st.latex() (KaTeX).
# - No math appears inside widget labels/options (letters-only radios).
# - Simulations are inside the Learn tab.
# - Mini worked example is shown by default.
# - Practice tab includes 24 questions (>=20).
# - Does NOT modify app.py or simulations.py.

from __future__ import annotations

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from simulations import BoardStep, render_simulation


# -----------------------------
# Strict KaTeX helpers
# -----------------------------
def _m(expr: str) -> None:
    """Render math ONLY via KaTeX."""
    st.latex(expr)


def _t(text: str) -> None:
    """Plain text only (no math here)."""
    st.markdown(text)


def _h2(title: str) -> None:
    st.markdown(f"## {title}")


def _h3(title: str) -> None:
    st.markdown(f"### {title}")


def _box(title: str, accent: str = "#1f77b4", bg: str = "#f3f8ff") -> None:
    st.markdown(
        f"""
<div style="border-left:6px solid {accent};background:{bg};padding:14px;border-radius:12px;margin:10px 0;">
<div style="font-weight:700;margin-bottom:6px;">{title}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _small_fig(title: str):
    fig = plt.figure(figsize=(6.0, 3.1), dpi=140)
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    return fig, ax


def _show(fig) -> None:
    st.pyplot(fig, clear_figure=True, use_container_width=False)


# -----------------------------
# Small plots (5.6.3)
# -----------------------------
def _plot_poly():
    x = np.linspace(-3.2, 3.2, 800)
    y = x**3 - 3 * x
    fig, ax = _small_fig(r"Polynomial: $f(x)=x^3-3x$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_rat():
    x1 = np.linspace(-6, 1.95, 800)
    x2 = np.linspace(2.05, 6, 800)

    def f(t):
        return (t + 1) / (t - 2)

    fig, ax = _small_fig(r"Rational: $f(x)=\dfrac{x+1}{x-2}$")
    ax.plot(x1, f(x1), label=r"$f(x)$")
    ax.plot(x2, f(x2), label=r"$f(x)$")
    ax.axvline(2, linestyle="--", linewidth=1)
    ax.axhline(1, linestyle="--", linewidth=1)
    ax.set_ylim(-6, 6)
    ax.legend(loc="best")
    return fig


def _plot_frac():
    x = np.linspace(-8, 8, 1200)
    y = np.sign(x) * (np.abs(x) ** (2 / 3))
    fig, ax = _small_fig(r"Fractional power: $f(x)=x^{2/3}$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_rad():
    x = np.linspace(1, 10, 600)
    y = np.sqrt(x - 1)
    fig, ax = _small_fig(r"Radical: $f(x)=\sqrt{x-1}$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


def _plot_mix():
    x = np.linspace(0.25, 10, 900)
    y = np.log(x) + np.sin(x)
    fig, ax = _small_fig(r"Components: $f(x)=\ln(x)+\sin(x)$")
    ax.plot(x, y, label=r"$f(x)$")
    ax.legend(loc="best")
    return fig


# -----------------------------
# Simulations (Learn tab only)
# -----------------------------
def _sim_rational():
    steps = [
        BoardStep(latex_line=r"f(x)=\frac{x+1}{x-2}", teacher_explain_md=r"Follow the curve-sketching workflow."),
        BoardStep(latex_line=r"\textbf{1) Domain: }x\neq 2", teacher_explain_md=r"Denominator is zero at \(x=2\)."),
        BoardStep(latex_line=r"\textbf{2) Vertical asymptote: }x=2", teacher_explain_md=r"No factor cancels."),
        BoardStep(latex_line=r"\textbf{3) Horizontal asymptote: }y=1", teacher_explain_md=r"Degrees equal; ratio of leading coefficients."),
        BoardStep(latex_line=r"\textbf{4) Intercepts: }f(0)=-\frac12,\ x=-1", teacher_explain_md=r"Anchor points."),
        BoardStep(latex_line=r"\textbf{5) }f'(x)=\frac{-3}{(x-2)^2}", teacher_explain_md=r"Always negative for \(x\neq 2\)."),
        BoardStep(latex_line=r"\textbf{Variation: decreasing on }(-\infty,2)\ \text{and }(2,\infty)", teacher_explain_md=r"No turning points."),
        BoardStep(latex_line=r"\textbf{6) }f''(x)=\frac{6}{(x-2)^3}", teacher_explain_md=r"Concavity changes across \(x=2\)."),
        BoardStep(latex_line=r"\textbf{Concavity: }x<2\Rightarrow f''(x)<0,\ x>2\Rightarrow f''(x)>0", teacher_explain_md=r"Left down, right up."),
        BoardStep(latex_line=r"\textbf{7) Values: }f(1)=-2,\ f(3)=4", teacher_explain_md=r"Few points."),
        BoardStep(latex_line=r"\textbf{8) Final sketch using all features}", teacher_explain_md=r"Combine everything."),
    ]
    render_simulation(steps, title="Simulation — Full workflow (rational)")


def _sim_polynomial():
    steps = [
        BoardStep(latex_line=r"f(x)=x^3-3x", teacher_explain_md=r"Sketch a polynomial using derivatives."),
        BoardStep(latex_line=r"\textbf{1) Domain: }\mathbb{R}", teacher_explain_md=r"Defined for all real \(x\)."),
        BoardStep(latex_line=r"\textbf{2) Zeros: }x(x^2-3)=0\Rightarrow x=0,\pm\sqrt3", teacher_explain_md=r"Intercepts."),
        BoardStep(latex_line=r"\textbf{3) }f'(x)=3x^2-3", teacher_explain_md=r"Critical points from \(f'(x)=0\)."),
        BoardStep(latex_line=r"f'(x)=0\Rightarrow x=\pm 1", teacher_explain_md=r"Critical values."),
        BoardStep(latex_line=r"f(-1)=2,\ f(1)=-2", teacher_explain_md=r"Turning points."),
        BoardStep(latex_line=r"\textbf{4) }f''(x)=6x", teacher_explain_md=r"Concavity / inflection."),
        BoardStep(latex_line=r"f''(x)=0\Rightarrow x=0,\ f(0)=0", teacher_explain_md=r"Inflection point."),
        BoardStep(latex_line=r"\textbf{Final sketch using intercepts + turning points + inflection}", teacher_explain_md=r"Controlled sketch."),
    ]
    render_simulation(steps, title="Simulation — Full workflow (polynomial)")


# -----------------------------
# KaTeX-safe MCQ (letters-only radio)
# -----------------------------
def _mcq(
    qid: str,
    stem_text: list[str],
    stem_math: list[str],
    opt_text: list[str],
    opt_math: list[str],
    correct: str,
    explain_text: list[str],
    explain_math: list[str],
    hint_text: list[str],
    hint_math: list[str],
) -> None:
    _box(f"Question {qid}")
    for s in stem_text:
        _t(s)
    for e in stem_math:
        _m(e)

    letters = ["A", "B", "C", "D"]

    _t("Options:")
    for i in range(4):
        st.markdown(f"- **{letters[i]}.** {opt_text[i]}")
        if opt_math[i]:
            _m(opt_math[i])

    pick = st.radio("Choose:", letters, index=None, key=f"q_{qid}")

    if pick is not None:
        if pick == correct:
            st.success("✅ Correct")
        else:
            st.error("❌ Not correct")

        with st.expander("Explanation"):
            for s in explain_text:
                _t(s)
            for e in explain_math:
                _m(e)

        with st.expander("Hint"):
            for s in hint_text:
                _t(s)
            for e in hint_math:
                _m(e)

    st.markdown("---")


# -----------------------------
# Learn content (full coverage, not beyond)
# -----------------------------
def _learn():
    _h2("5.6.1  Recall: horizontal and vertical asymptotes of a rational function")

    _box("Rational function form", accent="#2ca02c", bg="#f3fff6")
    _t("A rational function is a ratio of polynomials.")
    _m(r"f(x)=\frac{P(x)}{Q(x)},\qquad Q(x)\neq 0")

    _box("Vertical asymptotes (VA)", accent="#ff7f0e", bg="#fff6ee")
    _t("Find denominator zeros after simplifying. These are domain breaks and possible vertical asymptotes.")
    _m(r"Q(x)=0\ \Rightarrow\ x=\text{VA candidates}")

    _box("Horizontal asymptotes (HA) — recall rules", accent="#9467bd", bg="#f7f2ff")
    _t("Compare degrees of numerator and denominator.")
    _m(r"\deg(P)<\deg(Q)\Rightarrow y=0")
    _m(r"\deg(P)=\deg(Q)\Rightarrow y=\frac{\text{leading coeff of }P}{\text{leading coeff of }Q}")
    _m(r"\deg(P)>\deg(Q)\Rightarrow \text{no horizontal asymptote (recall)}")

    _h3("Mini worked example (shown by default)")
    _box("Example A", accent="#1f77b4", bg="#f3f8ff")
    _m(r"f(x)=\frac{x+1}{x-2}")
    _t("Domain restriction:")
    _m(r"x-2=0\Rightarrow x=2")
    _m(r"x\in\mathbb{R},\ x\neq 2")
    _t("Vertical asymptote:")
    _m(r"x=2")
    _t("Horizontal asymptote (degrees equal):")
    _m(r"y=\frac{1}{1}=1")

    _box("Example B (HA by degree comparison)", accent="#2ca02c", bg="#f3fff6")
    _m(r"g(x)=\frac{4x^2-7}{2x^2+5x+1}")
    _m(r"y=\frac{4}{2}=2")

    _box("Example C (two VA)", accent="#ff7f0e", bg="#fff6ee")
    _m(r"h(x)=\frac{x+3}{(x-1)(x+2)}")
    _m(r"(x-1)(x+2)=0\Rightarrow x=1,\ x=-2")
    _m(r"x=1,\quad x=-2")

    st.markdown("---")

    _h2("5.6.2  Summary of steps for curve sketching techniques")

    _box("Required workflow (exactly as objective 5.6.2)", accent="#2ca02c", bg="#f3fff6")
    _t("Use this sequence every time:")
    st.markdown("- Domain")
    st.markdown("- First and second derivative")
    st.markdown("- Critical values / first derivative test")
    st.markdown("- Inflection values / concavity / second derivative test")
    st.markdown("- Overlapping summary behaviour tables of variation and concavity")
    st.markdown("- Table of values for a few points")
    st.markdown("- Sketching")

    _box("Derivative meaning (needed for the workflow)", accent="#9467bd", bg="#f7f2ff")
    _m(r"f'(x)>0\Rightarrow \text{increasing},\qquad f'(x)<0\Rightarrow \text{decreasing}")
    _m(r"f''(x)>0\Rightarrow \text{concave up},\qquad f''(x)<0\Rightarrow \text{concave down}")

    _box("Worked workflow checkpoint (variation + concavity tables)", accent="#1f77b4", bg="#f3f8ff")
    _m(r"f(x)=\frac{x+1}{x-2}")
    _t("First derivative and sign:")
    _m(r"f'(x)=\frac{-3}{(x-2)^2}")
    _m(r"f'(x)<0\ \text{for}\ x\neq 2")
    _t("Second derivative and sign:")
    _m(r"f''(x)=\frac{6}{(x-2)^3}")
    _m(r"x<2\Rightarrow f''(x)<0,\qquad x>2\Rightarrow f''(x)>0")

    st.markdown("---")

    _h2("5.6.3  Analyze and sketch graphs for different functions")

    _box("What to check first (exactly within objective 5.6.3)", accent="#ff7f0e", bg="#fff6ee")
    st.markdown("- Polynomials: domain is all real numbers; use derivatives for turning points and concavity.")
    st.markdown("- Rational functions: domain restrictions and asymptotes; then derivatives.")
    st.markdown("- Fractional powers of \(x\): check for sharp points and behavior near key points.")
    st.markdown("- Radicals: domain begins at an endpoint where the inside becomes zero.")
    st.markdown("- Trig/exp/log components: check domain restrictions (especially log) and basic shape.")

    _box("Small visual gallery (graphs are intentionally small)", accent="#1f77b4", bg="#f3f8ff")
    c1, c2 = st.columns(2)
    with c1:
        _show(_plot_poly())
    with c2:
        _show(_plot_rat())
    c3, c4 = st.columns(2)
    with c3:
        _show(_plot_frac())
    with c4:
        _show(_plot_rad())
    _show(_plot_mix())

    st.markdown("---")

    _h2("Simulations (inside Learn tab)")
    _t("These simulations follow the workflow in objective 5.6.2.")
    _sim_rational()
    st.markdown("---")
    _sim_polynomial()


# -----------------------------
# Practice: 24 questions (>=20)
# -----------------------------
def _practice():
    _h2("Practice (24 questions)")
    _t("All questions stay within objectives 5.6.1–5.6.3.")

    _h3("5.6.1  Asymptotes (Q1–Q10)")

    _mcq("1",
         ["Find the horizontal asymptote."],
         [r"f(x)=\frac{2x^2-1}{x^2+4}"],
         ["", "", "", "No horizontal asymptote"],
         [r"y=0", r"y=1", r"y=2", ""],
         "C",
         ["Degrees are equal, so use ratio of leading coefficients."],
         [r"y=\frac{2}{1}=2"],
         ["Compare degrees of numerator and denominator."],
         [r"\deg(P)=\deg(Q)"])

    _mcq("2",
         ["Find the vertical asymptotes."],
         [r"g(x)=\frac{x+3}{(x-1)(x+2)}"],
         ["", "", "", "No vertical asymptotes"],
         [r"x=1", r"x=-2", r"x=1,\ x=-2", ""],
         "C",
         ["Set denominator equal to zero (no cancellation)."],
         [r"(x-1)(x+2)=0\Rightarrow x=1,\ x=-2"],
         ["Solve the denominator equation."],
         [r"(x-1)(x+2)=0"])

    _mcq("3",
         ["Horizontal asymptote rule when numerator degree is smaller:"],
         [r"\deg(P)<\deg(Q)"],
         ["", "", "", ""],
         [r"y=0", r"y=1", r"x=0", r"\text{no horizontal asymptote}"],
         "A",
         ["A proper rational function tends to zero as the denominator grows faster."],
         [r"y=0"],
         ["Use degree comparison."],
         [r"\deg(P)<\deg(Q)"])

    _mcq("4",
         ["Find the horizontal asymptote."],
         [r"f(x)=\frac{5x-1}{2x+7}"],
         ["", "", "", ""],
         [r"y=\frac{5}{2}", r"y=\frac{2}{5}", r"y=0", r"\text{no horizontal asymptote}"],
         "A",
         ["Degrees equal, so ratio of leading coefficients."],
         [r"y=\frac{5}{2}"],
         ["Use leading coefficients."],
         [r"\frac{5x}{2x}\to\frac{5}{2}"])

    _mcq("5",
         ["Find the vertical asymptote."],
         [r"f(x)=\frac{x^2+1}{x-3}"],
         ["", "", "", "No vertical asymptote"],
         [r"x=0", r"x=1", r"x=3", ""],
         "C",
         ["Denominator is zero at the vertical asymptote."],
         [r"x-3=0\Rightarrow x=3"],
         ["Set the denominator equal to zero."],
         [r"x-3=0"])

    _mcq("6",
         ["Find the vertical asymptote."],
         [r"f(x)=\frac{3}{x^2}"],
         ["", "", "", "No vertical asymptote"],
         [r"x=0", r"y=0", r"y=3", ""],
         "A",
         ["Denominator is zero when the function is undefined."],
         [r"x^2=0\Rightarrow x=0"],
         ["Solve the denominator equation."],
         [r"x^2=0"])

    _mcq("7",
         ["Find the horizontal asymptote."],
         [r"f(x)=\frac{x^3}{x^4+1}"],
         ["", "", "", ""],
         [r"y=0", r"y=1", r"y=x", r"\text{no horizontal asymptote}"],
         "A",
         ["Degree on top is smaller."],
         [r"3<4\Rightarrow y=0"],
         ["Compare degrees."],
         [r"3<4"])

    _mcq("8",
         ["Find the horizontal asymptote."],
         [r"f(x)=\frac{7x^4-2}{x^4+9}"],
         ["", "", "", ""],
         [r"y=0", r"y=7", r"y=\frac{1}{7}", r"\text{no horizontal asymptote}"],
         "B",
         ["Degrees equal; ratio of leading coefficients."],
         [r"y=\frac{7}{1}=7"],
         ["Use leading coefficients."],
         [r"\frac{7x^4}{x^4}\to 7"])

    _mcq("9",
         ["Find the vertical asymptotes."],
         [r"f(x)=\frac{1}{(x+5)(x-2)}"],
         ["", "", "", "No vertical asymptote"],
         [r"x=-5", r"x=2", r"x=-5,\ x=2", ""],
         "C",
         ["Denominator zeros give vertical asymptotes."],
         [r"(x+5)(x-2)=0\Rightarrow x=-5,\ x=2"],
         ["Set denominator equal to zero."],
         [r"(x+5)(x-2)=0"])

    _mcq("10",
         ["If a rational function is undefined at a value, that value is always:"],
         [r"Q(a)=0"],
         ["A domain restriction (may be a VA)", "", "", ""],
         ["", r"\text{always a VA}", r"\text{always a HA}", r"\text{always an intercept}"],
         "A",
         ["It must be excluded from the domain; VA depends on cancellation."],
         [r"x=a\Rightarrow x\neq a"],
         ["Domain comes before classification."],
         [r"f(a)\ \text{undefined}"])

    _h3("5.6.2  Steps (Q11–Q18)")

    _mcq("11", ["First step in curve sketching:"], [], ["Find the domain", "", "", ""], ["", r"f'(x)", r"f''(x)", r"\text{table of many values}"],
         "A",
         ["Domain tells where the function exists."], [],
         ["Start by identifying restrictions."], [])

    _mcq("12", ["Critical values for turning points come from:"], [], ["", "", "", ""], [r"f(x)=0", r"f'(x)=0", r"f''(x)=0", r"f(x)=1"],
         "B",
         ["Turning points are linked to slope being zero."], [r"f'(x)=0"],
         ["Slope is the first derivative."], [r"f'(x)"])

    _mcq("13", ["First derivative test decides:"], [], ["", "", "", ""],
         [r"\text{increasing/decreasing and local max/min}", r"\text{domain only}", r"\text{HA only}", r"\text{intercepts only}"],
         "A",
         ["Use sign of first derivative."], [r"f'(x)>0,\ f'(x)<0"],
         ["Positive means increasing."], [r"f'(x)>0"])

    _mcq("14", ["Concavity is decided using:"], [], ["", "", "", ""],
         [r"f(x)", r"f'(x)", r"f''(x)", r"\text{domain}"],
         "C",
         ["Second derivative controls concavity."], [r"f''(x)>0,\ f''(x)<0"],
         ["Concavity comes from the second derivative."], [r"f''(x)"])

    _mcq("15", ["Inflection point requires:"], [], ["", "", "", ""],
         [r"f'(x)=0", r"f''(x)=0\ \text{and concavity changes}", r"Q(x)=0", r"\text{HA exists}"],
         "B",
         ["Inflection is a change in concavity."], [r"f''(x)=0\ \text{and sign change}"],
         ["Check concavity on both sides."], [])

    _mcq("16", ["Overlapping behaviour tables combine:"], [], ["", "", "", ""],
         [r"\text{domain and intercepts}", r"f'(x)\ \text{and}\ f''(x)", r"f(x)\ \text{and}\ f'(x)", r"f(x)\ \text{and}\ f''(x)"],
         "B",
         ["Variation from first derivative; concavity from second derivative."], [r"f'(x),\ f''(x)"],
         ["Rise/fall + bend direction."], [])

    _mcq("17", ["A small table of values is used to:"], [], ["Anchor the sketch", "Replace derivatives", "Remove asymptotes", "Find the domain"], ["", "", "", ""],
         "A",
         ["A few points place the curve correctly."], [],
         ["Only a few anchors are needed."], [])

    _mcq("18", ["Final sketch should be drawn after:"], [], ["", "", "", ""],
         [r"\text{domain + derivative behaviour + a few points}", r"\text{many values only}", r"\text{intercepts only}", r"\text{HA only}"],
         "A",
         ["Sketch is controlled by combining all features."], [],
         ["Follow the full workflow."], [])

    _h3("5.6.3  Function types (Q19–Q24)")

    _mcq("19", ["Domain of a polynomial:"], [], ["", "", "", ""], [r"\mathbb{R}", r"x>0", r"x\neq 0", r"x\ge 0"],
         "A",
         ["Polynomials are defined for all real numbers."], [r"\mathbb{R}"],
         ["No denominators/radicals/logs."], [])

    _mcq("20", ["Radical domain condition for:"], [r"f(x)=\sqrt{x-4}"], ["", "", "", ""], [r"x-4\ge 0", r"x-4\le 0", r"x-4>0", r"x-4<0"],
         "A",
         ["Square root requires nonnegative input."], [r"x\ge 4"],
         ["Inside the root must be nonnegative."], [])

    _mcq("21", ["Log domain restriction for:"], [r"f(x)=\ln(x)+\sin(x)"], ["", "", "", ""], [r"x>0", r"x\ge 0", r"x\neq 0", r"\mathbb{R}"],
         "A",
         ["Natural log requires positive input."], [r"x>0"],
         ["Log controls the domain."], [])

    _mcq("22", ["Key feature at the origin for:"], [r"f(x)=x^{2/3}"], ["", "", "", ""],
         [r"\text{cusp at }x=0", r"\text{VA at }x=0", r"\text{hole at }x=0", r"\text{HA}"],
         "A",
         ["Defined but not smooth at the origin, giving a cusp."], [r"x^{2/3}\ \text{cusp at }x=0"],
         ["Not smooth does not mean undefined."], [])

    _mcq("23", ["For rational functions, start with:"], [], ["", "", "", ""],
         [r"\text{domain restrictions and asymptotes}", r"\text{only intercepts}", r"\text{only }f''(x)", r"\text{many values}"],
         "A",
         ["Asymptotes and breaks control the shape."], [],
         ["Find denominator zeros first."], [])

    _mcq("24", ["Purpose of the second derivative in sketching:"], [], ["", "", "", ""],
         [r"\text{concavity and inflection points}", r"\text{HA}", r"\text{domain only}", r"\text{intercepts only}"],
         "A",
         ["Second derivative tells concavity and helps identify inflection points."], [r"f''(x)>0,\ f''(x)<0"],
         ["Concavity comes from }f''(x)"], [])


def render():
    st.header("Subtopic 5.6: Overview of Curve Sketching")
    st.caption("Source: Al Diwan – Grade 12 Advanced Stream Mathematics – Lesson 4.6")

    _h2("Lesson objectives")
    _t("By the end of this subtopic, you should be able to:")
    st.markdown("- 5.6.1 Recall horizontal and vertical asymptotes of a rational function.")
    st.markdown("- 5.6.2 Understand the curve sketching workflow steps listed in the syllabus.")
    st.markdown("- 5.6.3 Sketch polynomials, rational functions, fractional powers, radicals, and trig/exp/log components.")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        _learn()

    with tabs[1]:
        _practice()