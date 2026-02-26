# subtopic_5_6_curve_sketching_overview.py
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# IMPORTANT: do NOT change simulations.py — we USE it exactly as-is
import simulations
from simulations import BoardStep


# =========================
# Helpers (LaTeX everywhere)
# =========================
def _md_math(md: str):
    """
    Student-friendly markdown renderer that supports LaTeX.
    Use \( ... \) for inline, $$ ... $$ for display.
    """
    st.markdown(md, unsafe_allow_html=False)


def _latex(s: str):
    """Display LaTeX block."""
    st.latex(s)


def _katex_inline(s: str) -> str:
    """Return inline LaTeX wrapped for markdown."""
    return rf"\({s}\)"


def _katex_block(s: str) -> str:
    """Return display LaTeX wrapped for markdown."""
    return rf"$$ {s} $$"


def _small_plot_xy(x, y, title=None, xlabel="x", ylabel="y"):
    """
    Small default plot (NOT huge) and visible by default.
    Breaks curve on discontinuities.
    """
    fig = plt.figure(figsize=(4.6, 3.1), dpi=150)
    ax = fig.add_subplot(111)

    # Break at huge jumps / inf / nan
    y = np.array(y, dtype=float)
    x = np.array(x, dtype=float)

    mask = np.isfinite(y)
    x2 = x[mask]
    y2 = y[mask]

    if len(x2) > 2:
        jumps = np.abs(np.diff(y2))
        cut = np.where(jumps > np.nanpercentile(jumps, 95))[0]
        if len(cut) > 0:
            # split into segments
            start = 0
            for c in cut[:8]:  # keep it stable
                ax.plot(x2[start:c + 1], y2[start:c + 1])
                start = c + 1
            ax.plot(x2[start:], y2[start:])
        else:
            ax.plot(x2, y2)
    else:
        ax.plot(x2, y2)

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    ax.grid(True, alpha=0.25)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)


def _plot_function(func, segments, title):
    """
    segments = list of (xmin, xmax)
    """
    for (a, b) in segments:
        x = np.linspace(a, b, 600)
        y = func(x)
        _small_plot_xy(x, y, title=title)


def _interval_rows_template():
    """
    Clear, student-readable “combined conclusions” layout (no messy tables).
    Uses columns instead of st.table because st.table does not render LaTeX.
    """
    st.markdown("### Present your conclusions clearly (easy to read)")
    _md_math(
        """
Instead of drawing a crowded table, write your conclusions as **clean interval rows**.
Each row includes:

- the interval for \(x\)
- the sign of \(f'(x)\) → increasing / decreasing
- the sign of \(f''(x)\) → concave up / concave down
"""
    )

    st.markdown("**Example row (template):**")
    c1, c2, c3, c4, c5 = st.columns([1.2, 1.2, 1.4, 1.2, 1.6])
    with c1:
        st.markdown("**Interval**")
        st.markdown(_katex_block(r"(a,b)"))
    with c2:
        st.markdown("**Sign of** " + _katex_inline(r"f'(x)"))
        st.markdown(_katex_block(r"+"))
    with c3:
        st.markdown("**Behavior**")
        st.markdown("increasing")
    with c4:
        st.markdown("**Sign of** " + _katex_inline(r"f''(x)"))
        st.markdown(_katex_block(r"-"))
    with c5:
        st.markdown("**Concavity**")
        st.markdown("concave down")


# =====================================
# Examples (from Chapter 3.pdf section)
# =====================================
# NOTE: The functions match what appears in the Chapter 3.pdf pages you uploaded
# (EXAMPLE 6.1 to EXAMPLE 6.6 in the curve sketching overview).
EXAMPLES = {
    "Example 6.1 (Polynomial)": {
        "f_latex": r"f(x)=x^{3}-3x^{2}+1",
        "plot_segments": [(-4, 4)],
        "f_np": lambda x: x**3 - 3*x**2 + 1,
        "steps": [
            BoardStep(
                latex_line=r"\textbf{Example 6.1: } f(x)=x^{3}-3x^{2}+1",
                teacher_explain_md="We will sketch by finding key features: turning points, concavity, and intercepts."
            ),
            BoardStep(
                latex_line=r"f'(x)=3x^{2}-6x=3x(x-2)",
                teacher_explain_md="Compute the first derivative and factor it to find critical numbers."
            ),
            BoardStep(
                latex_line=r"f'(x)=0 \Rightarrow 3x(x-2)=0 \Rightarrow x=0,\;x=2",
                teacher_explain_md="Critical numbers are where \(f'(x)=0\)."
            ),
            BoardStep(
                latex_line=r"f''(x)=6x-6=6(x-1)",
                teacher_explain_md="Compute \(f''(x)\) to study concavity and possible inflection points."
            ),
            BoardStep(
                latex_line=r"f''(x)=0 \Rightarrow 6(x-1)=0 \Rightarrow x=1",
                teacher_explain_md="Candidate inflection point is where \(f''(x)=0\)."
            ),
            BoardStep(
                latex_line=r"f(0)=1,\quad f(2)=8-12+1=-3,\quad f(1)=1-3+1=-1",
                teacher_explain_md="Evaluate \(f(x)\) at important \(x\)-values to plot key points."
            ),
            BoardStep(
                latex_line=r"\text{Increasing/decreasing from } f'(x)=3x(x-2)",
                teacher_explain_md=r"""
Check the sign of \(f'(x)\) on intervals \((-\infty,0)\), \((0,2)\), \((2,\infty)\).
- \(f'(x)>0\) → increasing
- \(f'(x)<0\) → decreasing
"""
            ),
            BoardStep(
                latex_line=r"\text{Concavity from } f''(x)=6(x-1)",
                teacher_explain_md=r"""
Check the sign of \(f''(x)\) on \((-\infty,1)\) and \((1,\infty)\).
- \(f''(x)>0\) → concave up
- \(f''(x)<0\) → concave down
"""
            ),
            BoardStep(
                latex_line=r"\text{Inflection point at } x=1 \Rightarrow (1,-1)",
                teacher_explain_md="Because concavity changes at \(x=1\), \((1,-1)\) is an inflection point."
            ),
            BoardStep(
                latex_line=r"\text{Final sketch: plot key points and shape from signs}",
                teacher_explain_md="Use the turning point(s), inflection point, and end behavior to draw a correct sketch."
            ),
        ],
    },

    "Example 6.2 (Rational)": {
        "f_latex": r"f(x)=\frac{x^{2}-3}{x^{3}}",
        "plot_segments": [(-4, -0.3), (0.3, 4)],
        "f_np": lambda x: (x**2 - 3) / (x**3),
        "steps": [
            BoardStep(
                latex_line=r"\textbf{Example 6.2: } f(x)=\frac{x^{2}-3}{x^{3}}",
                teacher_explain_md="For a rational function, start with the domain and asymptotes."
            ),
            BoardStep(
                latex_line=r"\text{Domain: } x\neq 0",
                teacher_explain_md="The denominator is zero at \(x=0\), so \(x=0\) is excluded from the domain."
            ),
            BoardStep(
                latex_line=r"\text{Vertical asymptote: } x=0",
                teacher_explain_md="A non-cancelled zero of the denominator gives a vertical asymptote."
            ),
            BoardStep(
                latex_line=r"\text{Horizontal asymptote: } y=0 \; (\deg\text{ numerator } < \deg\text{ denominator})",
                teacher_explain_md="Here degree(2) < degree(3), so \(y=0\) is a horizontal asymptote."
            ),
            BoardStep(
                latex_line=r"f'(x)=\frac{(2x)x^{3}-(x^{2}-3)(3x^{2})}{x^{6}}=\frac{-x^{2}+9}{x^{4}}",
                teacher_explain_md="Differentiate carefully using the quotient rule (or rewrite as powers)."
            ),
            BoardStep(
                latex_line=r"f'(x)=0 \Rightarrow -x^{2}+9=0 \Rightarrow x=\pm 3",
                teacher_explain_md="Critical numbers occur where \(f'(x)=0\) (and where \(f'(x)\) is undefined inside the domain)."
            ),
            BoardStep(
                latex_line=r"f''(x)=\frac{2(x^{2}-18)}{x^{5}}",
                teacher_explain_md="Now use \(f''(x)\) for concavity and possible inflection points."
            ),
            BoardStep(
                latex_line=r"f''(x)=0 \Rightarrow x^{2}-18=0 \Rightarrow x=\pm 3\sqrt{2}",
                teacher_explain_md="Candidates for inflection points: where \(f''(x)=0\) (and discontinuities)."
            ),
            BoardStep(
                latex_line=r"\text{Final sketch uses: asymptotes } (x=0,\;y=0) \text{ + signs of } f', f''",
                teacher_explain_md="Combine intercepts/critical points/concavity and the asymptotes to sketch accurately."
            ),
        ],
    },

    "Example 6.3 (Two vertical asymptotes)": {
        "f_latex": r"f(x)=\frac{x^{2}}{x^{2}-4}",
        "plot_segments": [(-6, -2.2), (-1.8, 1.8), (2.2, 6)],
        "f_np": lambda x: (x**2) / (x**2 - 4),
        "steps": [
            BoardStep(
                latex_line=r"\textbf{Example 6.3: } f(x)=\frac{x^{2}}{x^{2}-4}",
                teacher_explain_md="Start with domain and asymptotes, then use derivatives for shape."
            ),
            BoardStep(
                latex_line=r"\text{Domain: } x\neq \pm 2",
                teacher_explain_md="Denominator is zero at \(x=\pm 2\), so these are excluded."
            ),
            BoardStep(
                latex_line=r"\text{Vertical asymptotes: } x=-2,\;x=2",
                teacher_explain_md="Non-cancelled denominator zeros give vertical asymptotes."
            ),
            BoardStep(
                latex_line=r"\text{Horizontal asymptote: } y=1",
                teacher_explain_md="Degrees are equal; ratio of leading coefficients is \(1/1=1\)."
            ),
            BoardStep(
                latex_line=r"f'(x)=\frac{-8x}{(x^{2}-4)^{2}}",
                teacher_explain_md="Differentiate and simplify; keep the denominator factored/structured."
            ),
            BoardStep(
                latex_line=r"f'(x)=0 \Rightarrow -8x=0 \Rightarrow x=0",
                teacher_explain_md="Only critical number from numerator is \(x=0\) (within the domain)."
            ),
            BoardStep(
                latex_line=r"f''(x)=\frac{8(3x^{2}+4)}{(x^{2}-4)^{3}}",
                teacher_explain_md="Use \(f''(x)\) to decide concavity on each interval split by \(\pm 2\)."
            ),
            BoardStep(
                latex_line=r"\text{Final sketch uses: } x=\pm2,\; y=1,\; \text{and sign tests for } f',f''",
                teacher_explain_md="Sketch each branch separately on \((-\infty,-2),(-2,2),(2,\infty)\)."
            ),
        ],
    },

    "Example 6.4 (Approximated domain feature)": {
        "f_latex": r"f(x)=\sqrt{x-1}+\frac{1}{x-2}",
        "plot_segments": [(1.05, 1.95), (2.05, 6)],
        "f_np": lambda x: np.sqrt(x - 1) + 1/(x - 2),
        "steps": [
            BoardStep(
                latex_line=r"\textbf{Example 6.4: } f(x)=\sqrt{x-1}+\frac{1}{x-2}",
                teacher_explain_md="This function mixes a radical and a rational term, so domain is essential."
            ),
            BoardStep(
                latex_line=r"\text{Domain: } x\ge 1,\; x\neq 2",
                teacher_explain_md=r"""
\(\sqrt{x-1}\) needs \(x-1\ge 0\Rightarrow x\ge 1\).
\(\frac{1}{x-2}\) needs \(x\ne 2\).
"""
            ),
            BoardStep(
                latex_line=r"\text{Vertical asymptote: } x=2",
                teacher_explain_md="The term \(\frac{1}{x-2}\) blows up at \(x=2\), so there is a vertical asymptote."
            ),
            BoardStep(
                latex_line=r"f'(x)=\frac{1}{2\sqrt{x-1}}-\frac{1}{(x-2)^{2}}",
                teacher_explain_md="Differentiate each part: radical derivative + rational derivative."
            ),
            BoardStep(
                latex_line=r"f''(x)=-\frac{1}{4(x-1)^{3/2}}+\frac{2}{(x-2)^{3}}",
                teacher_explain_md="Use \(f''(x)\) to study concavity on \((1,2)\) and \((2,\infty)\)."
            ),
            BoardStep(
                latex_line=r"\text{Final sketch: domain split } (1,2) \text{ and } (2,\infty) \text{ + asymptote } x=2",
                teacher_explain_md="Sketch each side separately and use sign tests for shape."
            ),
        ],
    },

    "Example 6.5 (Exponential)": {
        "f_latex": r"f(x)=e^{x}-x",
        "plot_segments": [(-3, 3)],
        "f_np": lambda x: np.exp(x) - x,
        "steps": [
            BoardStep(
                latex_line=r"\textbf{Example 6.5: } f(x)=e^{x}-x",
                teacher_explain_md="Exponential functions are smooth everywhere, so the domain is all real numbers."
            ),
            BoardStep(
                latex_line=r"\text{Domain: } (-\infty,\infty)",
                teacher_explain_md="No restrictions for \(e^{x}\) or \(-x\)."
            ),
            BoardStep(
                latex_line=r"f'(x)=e^{x}-1",
                teacher_explain_md="Turning behavior comes from the sign of \(f'(x)\)."
            ),
            BoardStep(
                latex_line=r"f'(x)=0 \Rightarrow e^{x}-1=0 \Rightarrow x=0",
                teacher_explain_md="There is one critical number at \(x=0\)."
            ),
            BoardStep(
                latex_line=r"f''(x)=e^{x} \;>\;0 \text{ for all }x",
                teacher_explain_md="Since \(f''(x)\) is always positive, the curve is always concave up."
            ),
            BoardStep(
                latex_line=r"\text{At } x=0:\; f(0)=1 \Rightarrow (0,1)",
                teacher_explain_md="Plot the key point and use increasing + concave up to sketch."
            ),
        ],
    },

    "Example 6.6 (Trig + polynomial)": {
        "f_latex": r"f(x)=x^{2}+\sin x",
        "plot_segments": [(-6, 6)],
        "f_np": lambda x: x**2 + np.sin(x),
        "steps": [
            BoardStep(
                latex_line=r"\textbf{Example 6.6: } f(x)=x^{2}+\sin x",
                teacher_explain_md="This is defined for all real \(x\). Use derivatives to understand the shape."
            ),
            BoardStep(
                latex_line=r"f'(x)=2x+\cos x",
                teacher_explain_md="Critical numbers solve \(2x+\cos x=0\). This may require approximation."
            ),
            BoardStep(
                latex_line=r"f''(x)=2-\sin x",
                teacher_explain_md="Concavity depends on the sign of \(2-\sin x\)."
            ),
            BoardStep(
                latex_line=r"2-\sin x \ge 1 \Rightarrow f''(x) > 0 \text{ for all }x",
                teacher_explain_md="Since \(\sin x\in[-1,1]\), we have \(2-\sin x\in[1,3]\), always positive → always concave up."
            ),
            BoardStep(
                latex_line=r"\text{Final sketch: always concave up, turning points from } 2x+\cos x=0",
                teacher_explain_md="Use a numerical estimate if needed and then sketch using the concave-up shape."
            ),
        ],
    },
}


# =========================
# Practice bank (20 Qs)
# =========================
def _practice_questions():
    # All prompts/hints/solutions are LaTeX-rendered (no raw \dfrac text)
    return [
        {
            "q": r"Find the vertical asymptote(s) of \(f(x)=\frac{x^{2}}{x^{2}-4}\).",
            "hint": r"Set the denominator equal to zero and check that nothing cancels.",
            "sol": r"Vertical asymptotes occur where \(x^{2}-4=0\Rightarrow x=\pm 2\). Nothing cancels, so \(x=-2\) and \(x=2\) are vertical asymptotes.",
        },
        {
            "q": r"Find the horizontal asymptote of \(f(x)=\frac{x^{2}}{x^{2}-4}\).",
            "hint": r"Compare degrees of numerator and denominator.",
            "sol": r"Degrees are equal, so the horizontal asymptote is the ratio of leading coefficients: \(y=\frac{1}{1}=1\).",
        },
        {
            "q": r"State the domain of \(f(x)=\frac{x^{2}}{x^{2}-4}\).",
            "hint": r"Exclude values that make the denominator zero.",
            "sol": r"Exclude \(x=\pm 2\). Domain: \((-\infty,-2)\cup(-2,2)\cup(2,\infty)\).",
        },
        {
            "q": r"For \(f(x)=x^{3}-3x^{2}+1\), compute \(f'(x)\).",
            "hint": r"Differentiate term by term.",
            "sol": r"\(f'(x)=3x^{2}-6x=3x(x-2)\).",
        },
        {
            "q": r"For \(f(x)=x^{3}-3x^{2}+1\), find critical numbers.",
            "hint": r"Solve \(f'(x)=0\).",
            "sol": r"\(3x(x-2)=0\Rightarrow x=0,\;2\).",
        },
        {
            "q": r"For \(f(x)=x^{3}-3x^{2}+1\), compute \(f''(x)\).",
            "hint": r"Differentiate \(f'(x)\).",
            "sol": r"\(f''(x)=6x-6=6(x-1)\).",
        },
        {
            "q": r"For \(f(x)=x^{3}-3x^{2}+1\), find the inflection point.",
            "hint": r"Solve \(f''(x)=0\) and confirm concavity changes.",
            "sol": r"\(6(x-1)=0\Rightarrow x=1\). Then \(f(1)=-1\). Inflection point: \((1,-1)\).",
        },
        {
            "q": r"For \(f(x)=e^{x}-x\), find the critical number.",
            "hint": r"Solve \(f'(x)=0\).",
            "sol": r"\(f'(x)=e^{x}-1\). So \(e^{x}=1\Rightarrow x=0\).",
        },
        {
            "q": r"For \(f(x)=e^{x}-x\), decide concavity.",
            "hint": r"Compute \(f''(x)\).",
            "sol": r"\(f''(x)=e^{x}>0\) for all \(x\). So the curve is concave up everywhere.",
        },
        {
            "q": r"State the domain of \(f(x)=\sqrt{x-1}+\frac{1}{x-2}\).",
            "hint": r"Radical requires \(x-1\ge 0\) and denominator requires \(x\ne 2\).",
            "sol": r"Domain: \([1,2)\cup(2,\infty)\).",
        },
        {
            "q": r"Identify the vertical asymptote of \(f(x)=\sqrt{x-1}+\frac{1}{x-2}\).",
            "hint": r"Look at the rational term.",
            "sol": r"The term \(\frac{1}{x-2}\) blows up at \(x=2\), so \(x=2\) is a vertical asymptote.",
        },
        {
            "q": r"For \(f(x)=\frac{x^{2}-3}{x^{3}}\), identify the vertical asymptote and horizontal asymptote.",
            "hint": r"Vertical: denominator zero. Horizontal: compare degrees.",
            "sol": r"Vertical asymptote: \(x=0\). Since \(\deg(2)<\deg(3)\), horizontal asymptote: \(y=0\).",
        },
        {
            "q": r"For \(f(x)=\frac{x^{2}-3}{x^{3}}\), compute \(f'(x)\) (simplified).",
            "hint": r"Differentiate or rewrite as powers.",
            "sol": r"\(f'(x)=\frac{-x^{2}+9}{x^{4}}\).",
        },
        {
            "q": r"For \(f(x)=\frac{x^{2}-3}{x^{3}}\), solve \(f'(x)=0\).",
            "hint": r"Set the numerator equal to zero.",
            "sol": r"\(-x^{2}+9=0\Rightarrow x=\pm 3\).",
        },
        {
            "q": r"For \(f(x)=x^{2}+\sin x\), compute \(f'(x)\) and \(f''(x)\).",
            "hint": r"Derivative of \(\sin x\) is \(\cos x\).",
            "sol": r"\(f'(x)=2x+\cos x\), and \(f''(x)=2-\sin x\).",
        },
        {
            "q": r"Show that \(f(x)=x^{2}+\sin x\) is concave up for all \(x\).",
            "hint": r"Use \(\sin x\in[-1,1]\).",
            "sol": r"Since \(\sin x\in[-1,1]\), \(2-\sin x\in[1,3]\), so \(f''(x)=2-\sin x>0\) for all \(x\).",
        },
        {
            "q": r"For \(f(x)=\frac{x^{2}}{x^{2}-4}\), compute \(f'(x)\).",
            "hint": r"Quotient rule and simplify.",
            "sol": r"\(f'(x)=\frac{-8x}{(x^{2}-4)^{2}}\).",
        },
        {
            "q": r"For \(f(x)=\frac{x^{2}}{x^{2}-4}\), find the critical number in the domain.",
            "hint": r"Solve \(f'(x)=0\).",
            "sol": r"\(-8x=0\Rightarrow x=0\). This is allowed since \(0\ne \pm 2\).",
        },
        {
            "q": r"Sketch-planning: list the correct order of steps to sketch a curve using derivatives.",
            "hint": r"Use: domain → intercepts → \(f'\) → \(f''\) → asymptotes → final sketch.",
            "sol": r"1) Domain  2) Intercepts  3) \(f'(x)\) sign → increasing/decreasing  4) \(f''(x)\) sign → concavity/inflection  5) Asymptotes (if any)  6) Final sketch.",
        },
        {
            "q": r"For a rational function \(\frac{p(x)}{q(x)}\), when does a vertical asymptote occur?",
            "hint": r"Think denominator zeros that do not cancel.",
            "sol": r"A vertical asymptote occurs at \(x=a\) when \(q(a)=0\) and the factor \((x-a)\) does not cancel with the numerator.",
        },
    ]


# =========================
# Render
# =========================
def render():
    # Tabs as requested: ONLY Learn + Practice
    tab_learn, tab_practice = st.tabs(["Learn", "Practice"])

    # ----------------
    # LEARN
    # ----------------
    with tab_learn:
        st.markdown("## Subtopic 5.6: Overview of Curve Sketching")

        _md_math(
            """
### Learning objectives (what you will master here)
You will be able to:

1. **Recall horizontal and vertical asymptotes** for a rational function.  
2. **Use a clear step-by-step workflow** for curve sketching:
   - domain  
   - first and second derivative  
   - critical values / first derivative test  
   - inflection values / concavity / second derivative test  
   - combine conclusions (in a readable format)  
   - a few key values  
   - final sketch  
3. **Analyze and sketch graphs** of:
   - polynomials  
   - rational functions  
   - functions with fractional powers / radicals  
   - functions with trig / exponential / logarithmic parts  
"""
        )

        st.markdown("---")

        _md_math(
            """
### Curve sketching workflow (the exact order to follow)
Use this checklist every time:

1. **Domain**: where the function is defined  
2. **Intercepts** (when needed): \(x\)-intercepts and \(y\)-intercept  
3. **First derivative** \(f'(x)\): critical numbers and increasing/decreasing  
4. **Second derivative** \(f''(x)\): concavity and inflection points  
5. **Asymptotes** (mainly for rational / mixed forms): vertical and horizontal  
6. **A few key points** (evaluate \(f(x)\) at important \(x\)-values)  
7. **Final sketch**: combine all results consistently
"""
        )

        st.markdown("---")

        st.markdown("### Asymptotes (quick recall for rational functions)")
        _md_math(
            """
**Vertical asymptote** at \(x=a\):  
- happens when \(q(a)=0\) in \(\frac{p(x)}{q(x)}\) **and the factor does not cancel**.

**Horizontal asymptote** for \(\frac{p(x)}{q(x)}\):  
- If \(\deg(p)<\deg(q)\): \(y=0\)  
- If \(\deg(p)=\deg(q)\): \(y=\frac{\text{leading coefficient of }p}{\text{leading coefficient of }q}\)
"""
        )

        st.markdown("---")
        _interval_rows_template()

        st.markdown("---")

        # Board simulator (fully working using simulations.render_simulation)
        st.markdown("## Board simulator (full solution on one board)")
        _md_math(
            """
Choose an example, then press **Play solution** to watch the full solution appear on the same board.
All steps are shown using **LaTeX math**, and the graph is shown **small and visible by default**.
"""
        )

        ex_names = list(EXAMPLES.keys())
        selected = st.radio("Choose an example for the board", ex_names, index=0, horizontal=True)

        c_left, c_right = st.columns([1.4, 1.0])

        with c_right:
            st.markdown("### Small graph (visible by default)")
            ex = EXAMPLES[selected]
            _plot_function(ex["f_np"], ex["plot_segments"], title=selected)

            st.markdown("**Function:**")
            st.markdown(_katex_block(ex["f_latex"].replace("f(x)=", "")))

        with c_left:
            play = st.button("Play solution", use_container_width=True)
            reset = st.button("Reset", use_container_width=True)

            # Board area
            if reset:
                st.session_state.pop(f"board_play_{selected}", None)

            if play:
                st.session_state[f"board_play_{selected}"] = True

            if st.session_state.get(f"board_play_{selected}", False):
                simulations.render_simulation(
                    EXAMPLES[selected]["steps"],
                    title=selected
                )
            else:
                st.info("Press **Play solution** to start the full step-by-step solution.")

        st.markdown("---")

        st.markdown("## Worked examples (quick access)")
        _md_math(
            """
Use the board simulator above to study each example.  
You should be able to answer:

- What is the **domain**?
- Where is the function **increasing/decreasing** (from \(f'(x)\))?
- Where is it **concave up/down** (from \(f''(x)\))?
- What are **vertical/horizontal asymptotes** (if rational / mixed)?
- What are the key points needed for the **final sketch**?
"""
        )

    # ----------------
    # PRACTICE
    # ----------------
    with tab_practice:
        st.markdown("## Practice (20 questions)")
        _md_math(
            """
Instructions:
- Open **Hint** only if needed.
- Then open **Show solution** to check your work.
- Every question uses **LaTeX math** (no raw code-looking expressions).
"""
        )
        st.markdown("---")

        qs = _practice_questions()

        for i, item in enumerate(qs, start=1):
            st.markdown(f"### Question {i}")
            _md_math(item["q"])

            c1, c2 = st.columns([1, 1])
            with c1:
                with st.expander("Hint"):
                    _md_math(item["hint"])
            with c2:
                with st.expander("Show solution"):
                    _md_math(item["sol"])

            st.markdown("---")
