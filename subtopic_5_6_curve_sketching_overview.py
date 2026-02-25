# subtopic_5_6_curve_sketching_overview.py
import math
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


# -------------------------
# Safe “board simulator” hook (uses your simulations.py if present)
# -------------------------
def _get_board_renderer():
    """
    Tries to reuse your existing simulations.py board (the one you said is better).
    We try multiple common function names so this file does NOT break your app.
    """
    try:
        import simulations  # type: ignore

        candidates = [
            "render_board_simulator",
            "render_blackboard_simulator",
            "board_simulator",
            "blackboard_simulator",
            "render_simulation_board",
            "render_board",
            "render_blackboard",
        ]
        for name in candidates:
            fn = getattr(simulations, name, None)
            if callable(fn):
                return fn

        # If simulations.py exists but no known function name is found,
        # return a tiny fallback that warns (without crashing).
        def _fallback(*_args, **_kwargs):
            st.warning(
                "Your simulations.py is present, but this subtopic could not find the board function name. "
                "Rename your board function to one of: "
                + ", ".join(candidates)
            )

        return _fallback

    except Exception:
        # No simulations.py or import failed → keep subtopic working anyway.
        def _fallback(*_args, **_kwargs):
            st.info(
                "Board simulator is not available (simulations.py not found). "
                "If you add it, this subtopic will automatically use it."
            )

        return _fallback


BOARD = _get_board_renderer()


# -------------------------
# Small plotting utility (NO huge charts)
# -------------------------
def _small_plot(x, y, title=None, v_asym=None, h_asym=None, xlim=None, ylim=None):
    fig = plt.figure(figsize=(5.8, 3.2))  # small and readable
    ax = fig.add_subplot(111)
    ax.plot(x, y, linewidth=2)

    # asymptotes
    if v_asym:
        for a in v_asym:
            ax.axvline(a, linestyle="--", linewidth=1)
    if h_asym is not None:
        ax.axhline(h_asym, linestyle="--", linewidth=1)

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    if title:
        ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    if xlim:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim:
        ax.set_ylim(ylim[0], ylim[1])

    ax.grid(True, alpha=0.3)
    st.pyplot(fig, clear_figure=True)


# -------------------------
# Clean “sign/conclusion row” (replaces unreadable/overlapping tables)
# -------------------------
def _row_interval(interval_latex, sign1_latex, behavior_latex, sign2_latex, concavity_latex):
    c1, c2, c3, c4, c5 = st.columns([1.2, 1, 1.6, 1, 1.6])
    with c1:
        st.markdown("**Interval**")
        st.latex(interval_latex)
    with c2:
        st.markdown("**Sign of** " + r"$f'(x)$")
        st.latex(sign1_latex)
    with c3:
        st.markdown("**Behavior**")
        st.latex(behavior_latex)
    with c4:
        st.markdown("**Sign of** " + r"$f''(x)$")
        st.latex(sign2_latex)
    with c5:
        st.markdown("**Concavity**")
        st.latex(concavity_latex)
    st.markdown("---")


# -------------------------
# Content from Chapter 3.pdf (Section 3.6, Examples 6.1–6.6)
# Student-friendly, but strictly within your objectives.
# -------------------------
def _learn_tab():
    st.markdown("## Learning Objectives (what you must master)")
    st.markdown(
        """
- **5.6.1** Recall finding the **horizontal** and **vertical asymptotes** of a rational function.  
- **5.6.2** Understand and apply the **curve sketching workflow**:
  domain → derivatives → critical values → concavity/inflections → asymptotes → intercepts → final sketch.  
- **5.6.3** Analyze and sketch graphs for different function types:
  polynomials, rational functions, fractional powers/radicals, and trig/exp/log components.
"""
    )

    st.markdown("---")

    st.markdown("## The curve-sketching workflow (your checklist)")
    st.markdown(
        """
Use this exact order when solving exam questions.  
(Every step you see below is from **Section 3.6 (Overview of Curve Sketching)**.)

1) **Domain**  
2) **Vertical asymptotes / discontinuities** (where the function is not defined)  
3) **First derivative**: increasing/decreasing + local extrema  
4) **Second derivative**: concavity + inflection points  
5) **Horizontal asymptotes** (limits as \(x\\to\\infty\) and \(x\\to-\\infty\))  
6) **Intercepts** (if exact is hard, approximate)
"""
    )

    st.markdown("---")

    # A small “interactive coach” without sliders
    st.markdown("## Interactive workflow coach (step-by-step)")
    st.markdown(
        "Choose a function type, then follow the steps. Each button reveals the next required result."
    )

    fn_type = st.radio(
        "Choose function type",
        [
            "Polynomial (Example 6.1)",
            "Rational (Example 6.2)",
            "Rational with two vertical asymptotes (Example 6.3)",
            "Rational with approximated domain feature (Example 6.4)",
            "Exponential with unusual behavior near 0 (Example 6.5)",
            "Trig + polynomial combination (Example 6.6)",
        ],
        horizontal=False,
    )

    # Map to the exact functions used in the textbook examples
    if fn_type.startswith("Polynomial"):
        st.markdown("### Function")
        st.latex(r"f(x)=x^{4}+6x^{3}+12x^{2}+8x+1")
        st.markdown(
            "- This example demonstrates the full workflow on a polynomial (domain is all real numbers, no vertical asymptotes)."
        )
        show_plot = st.button("Show a small sketch window", key="plot_6_1")
        if show_plot:
            xs = np.linspace(-4, 1, 500)
            ys = xs**4 + 6*xs**3 + 12*xs**2 + 8*xs + 1
            _small_plot(xs, ys, title="Polynomial sketch (small window)", xlim=(-4, 1), ylim=(-2, 8))

    elif fn_type.startswith("Rational (Example 6.2)"):
        st.markdown("### Function")
        st.latex(r"f(x)=\frac{x^{2}-3}{x^{3}}")
        st.markdown(
            r"""
- Domain excludes \(x=0\).  
- This example shows: vertical asymptote at \(x=0\), horizontal asymptote \(y=0\), and how derivatives control shape.
"""
        )
        show_plot = st.button("Show a small sketch window", key="plot_6_2")
        if show_plot:
            xs1 = np.linspace(-6, -0.2, 500)
            xs2 = np.linspace(0.2, 6, 500)
            f = lambda x: (x**2 - 3) / (x**3)
            _small_plot(xs1, f(xs1), title="Rational sketch (left of 0)", v_asym=[0], h_asym=0, xlim=(-6, -0.2), ylim=(-6, 6))
            _small_plot(xs2, f(xs2), title="Rational sketch (right of 0)", v_asym=[0], h_asym=0, xlim=(0.2, 6), ylim=(-6, 6))

    elif fn_type.startswith("Rational with two vertical asymptotes (Example 6.3)"):
        st.markdown("### Function")
        st.latex(r"f(x)=\frac{x^{2}}{x^{2}-4}")
        st.markdown(
            r"""
- Domain excludes \(x=\pm2\).  
- Vertical asymptotes at \(x=-2\) and \(x=2\).  
- Horizontal asymptote \(y=1\).
"""
        )
        show_plot = st.button("Show a small sketch window", key="plot_6_3")
        if show_plot:
            f = lambda x: (x**2) / (x**2 - 4)
            xsA = np.linspace(-6, -2.2, 400)
            xsB = np.linspace(-1.8, 1.8, 400)
            xsC = np.linspace(2.2, 6, 400)
            _small_plot(xsA, f(xsA), title="Left branch", v_asym=[-2, 2], h_asym=1, xlim=(-6, -2.2), ylim=(-5, 5))
            _small_plot(xsB, f(xsB), title="Middle branch", v_asym=[-2, 2], h_asym=1, xlim=(-1.8, 1.8), ylim=(-5, 5))
            _small_plot(xsC, f(xsC), title="Right branch", v_asym=[-2, 2], h_asym=1, xlim=(2.2, 6), ylim=(-5, 5))

    elif fn_type.startswith("Rational with approximated domain feature (Example 6.4)"):
        st.markdown("### Function")
        st.latex(r"f(x)=\frac{1}{x^{3}+3x^{2}+3x+3}")
        st.markdown(
            r"""
- Domain excludes the real root \(x=a\) of \(g(x)=x^{3}+3x^{2}+3x+3\).  
- This example is important because one key feature is **approximated**.
"""
        )
        st.markdown(
            r"""
From the textbook:  
\(g'(x)=3(x+1)^{2}\ge 0\) so \(g\) is increasing and has **one** real root.  
That root is approximately:
"""
        )
        st.latex(r"a\approx -2.25992")
        show_plot = st.button("Show a small sketch window", key="plot_6_4")
        if show_plot:
            f = lambda x: 1.0 / (x**3 + 3*x**2 + 3*x + 3)
            a = -2.25992
            xs1 = np.linspace(-6, a-0.15, 500)
            xs2 = np.linspace(a+0.15, 6, 500)
            _small_plot(xs1, f(xs1), title="Left of the vertical asymptote", v_asym=[a], h_asym=0, xlim=(-6, a-0.15), ylim=(-5, 5))
            _small_plot(xs2, f(xs2), title="Right of the vertical asymptote", v_asym=[a], h_asym=0, xlim=(a+0.15, 6), ylim=(-5, 5))

    elif fn_type.startswith("Exponential with unusual behavior near 0 (Example 6.5)"):
        st.markdown("### Function")
        st.latex(r"f(x)=e^{1/x}")
        st.markdown(
            r"""
- Domain excludes \(x=0\).  
- As \(x\to 0^{+}\), \(1/x\to\infty\) so \(e^{1/x}\to\infty\).  
- As \(x\to 0^{-}\), \(1/x\to-\infty\) so \(e^{1/x}\to 0\).  
This creates an **unusual** vertical asymptote behavior at \(x=0\).
"""
        )
        show_plot = st.button("Show a small sketch window", key="plot_6_5")
        if show_plot:
            f = lambda x: np.exp(1/x)
            xs1 = np.linspace(-6, -0.2, 600)
            xs2 = np.linspace(0.2, 6, 600)
            _small_plot(xs1, f(xs1), title="Left of 0 (approaches 0)", v_asym=[0], h_asym=1, xlim=(-6, -0.2), ylim=(0, 3))
            _small_plot(xs2, f(xs2), title="Right of 0 (blows up)", v_asym=[0], h_asym=1, xlim=(0.2, 6), ylim=(0, 10))

    else:
        st.markdown("### Function")
        st.latex(r"f(x)=\cos(x)-x")
        st.markdown(
            r"""
- Domain is all real numbers (no vertical asymptotes).  
- Derivatives:
\[
f'(x)=-\sin(x)-1\le 0
\]
So the graph is decreasing (even though there are horizontal tangent points).  
\[
f''(x)=-\cos(x)
\]
Concavity alternates because \(\cos(x)\) alternates.
"""
        )
        show_plot = st.button("Show a small sketch window", key="plot_6_6")
        if show_plot:
            xs = np.linspace(-4, 4, 600)
            ys = np.cos(xs) - xs
            _small_plot(xs, ys, title=r"$y=\cos(x)-x$ (small window)", xlim=(-4, 4), ylim=(-5, 5))

    st.markdown("---")

    # Board simulator (your simulations.py)
    st.markdown("## Board simulator (full solution on one board)")
    st.markdown(
        """
Choose an example, then press **Play solution** to watch the full solution appear on the same board.
(Your **simulations.py** board will be used automatically.)
"""
    )

    example_id = st.radio(
        "Choose an example for the board",
        [
            "Example 6.1 (Polynomial)",
            "Example 6.2 (Rational)",
            "Example 6.3 (Two vertical asymptotes)",
            "Example 6.4 (Approximated domain feature)",
            "Example 6.5 (Exponential)",
            "Example 6.6 (Trig + polynomial)",
        ],
        horizontal=True,
    )

    colA, colB = st.columns([1, 1])
    with colA:
        play = st.button("Play solution", use_container_width=True)
    with colB:
        reset = st.button("Reset", use_container_width=True)

    # We pass a simple payload. Your simulations.py can ignore or use it.
    payload = {
        "topic": "curve_sketching",
        "example": example_id,
    }

    if reset:
        st.session_state["__cs_board_reset__"] = st.session_state.get("__cs_board_reset__", 0) + 1

    if play:
        BOARD(payload)

    st.markdown("---")

    # Non-overlapping “combined behavior summary” (student readable)
    st.markdown("## How to present your conclusions clearly (no overlap)")
    st.markdown(
        """
Instead of drawing a crowded table, present your conclusions as **clean interval rows**.
Each row must include:

- interval
- sign of \(f'(x)\) → increasing/decreasing
- sign of \(f''(x)\) → concave up/down
"""
    )

    st.markdown("### Mini template (example row)")
    _row_interval(
        r"(a,b)",
        r"+",
        r"\text{increasing}",
        r"-",
        r"\text{concave down}",
    )


# -------------------------
# Practice (20+ questions, Hint + Show Solution)
# -------------------------
def _practice_tab():
    st.markdown("## Practice (20 questions)")
    st.markdown(
        "Each question has **Hint** and **Show solution**. All mathematics is shown in **LaTeX/KaTeX**."
    )
    st.markdown("---")

    # 20 questions aligned with objectives 5.6.1–5.6.3
    # (Built directly from the same Example set in Section 3.6.)
    qs = [
        {
            "q": r"Find the domain of \(f(x)=\dfrac{x^{2}}{x^{2}-4}\).",
            "hint": r"Domain excludes where the denominator is \(0\).",
            "sol": r"""
\[
x^{2}-4=0 \Rightarrow x=\pm2
\]
So the domain is:
\[
(-\infty,-2)\cup(-2,2)\cup(2,\infty)
\]
""",
        },
        {
            "q": r"Show that \(x=2\) is a vertical asymptote for \(f(x)=\dfrac{x^{2}}{x^{2}-4}\).",
            "hint": r"Factor \(x^{2}-4=(x-2)(x+2)\) and use one-sided limits.",
            "sol": r"""
\[
\lim_{x\to2^{+}}\frac{x^{2}}{(x-2)(x+2)}=+\infty,
\qquad
\lim_{x\to2^{-}}\frac{x^{2}}{(x-2)(x+2)}=-\infty
\]
So \(x=2\) is a vertical asymptote.
""",
        },
        {
            "q": r"Find the horizontal asymptote of \(f(x)=\dfrac{x^{2}}{x^{2}-4}\).",
            "hint": r"Divide numerator and denominator by \(x^{2}\).",
            "sol": r"""
\[
\frac{x^{2}}{x^{2}-4}=\frac{1}{1-\frac{4}{x^{2}}}
\Rightarrow \lim_{x\to\pm\infty}f(x)=\frac{1}{1-0}=1
\]
Horizontal asymptote: \(\;y=1\).
""",
        },
        {
            "q": r"For \(f(x)=\dfrac{x^{2}}{x^{2}-4}\), find where \(f\) is increasing and decreasing using \(f'(x)=-\dfrac{8x}{(x^{2}-4)^{2}}\).",
            "hint": r"The denominator is always positive on the domain, so the sign depends on \(-8x\).",
            "sol": r"""
Since \((x^{2}-4)^{2}>0\) on the domain, the sign of \(f'(x)\) is the sign of \(-x\).
\[
f'(x)>0 \text{ when } x<0,\qquad f'(x)<0 \text{ when } x>0
\]
So \(f\) is increasing on \((-\infty,-2)\cup(-2,0)\) and decreasing on \((0,2)\cup(2,\infty)\).
""",
        },
        {
            "q": r"Find the domain of \(f(x)=\dfrac{x^{2}-3}{x^{3}}\) and its vertical asymptote(s).",
            "hint": r"Denominator \(x^{3}=0\) at \(x=0\).",
            "sol": r"""
Domain excludes \(x=0\), so:
\[
(-\infty,0)\cup(0,\infty)
\]
Vertical asymptote at:
\[
x=0
\]
""",
        },
        {
            "q": r"Find the horizontal asymptote of \(f(x)=\dfrac{x^{2}-3}{x^{3}}\).",
            "hint": r"Rewrite as \(\dfrac{1}{x}-\dfrac{3}{x^{3}}\).",
            "sol": r"""
\[
\frac{x^{2}-3}{x^{3}}=\frac{1}{x}-\frac{3}{x^{3}}
\Rightarrow \lim_{x\to\pm\infty}f(x)=0
\]
Horizontal asymptote: \(\;y=0\).
""",
        },
        {
            "q": r"For \(f(x)=e^{1/x}\), evaluate \(\lim_{x\to0^{+}}e^{1/x}\).",
            "hint": r"As \(x\to0^{+}\), \(1/x\to+\infty\).",
            "sol": r"""
\[
x\to0^{+}\Rightarrow \frac{1}{x}\to+\infty\Rightarrow e^{1/x}\to\infty
\]
So \(\lim_{x\to0^{+}}e^{1/x}=\infty\).
""",
        },
        {
            "q": r"For \(f(x)=e^{1/x}\), evaluate \(\lim_{x\to0^{-}}e^{1/x}\).",
            "hint": r"As \(x\to0^{-}\), \(1/x\to-\infty\).",
            "sol": r"""
\[
x\to0^{-}\Rightarrow \frac{1}{x}\to-\infty\Rightarrow e^{1/x}\to 0
\]
So \(\lim_{x\to0^{-}}e^{1/x}=0\).
""",
        },
        {
            "q": r"For \(f(x)=e^{1/x}\), find where \(f\) is increasing/decreasing if \(f'(x)=e^{1/x}\left(-\dfrac{1}{x^{2}}\right)\).",
            "hint": r"\(e^{1/x}>0\) and \(-1/x^{2}<0\) for \(x\ne0\).",
            "sol": r"""
For \(x\ne0\):
\[
e^{1/x}>0,\qquad -\frac{1}{x^{2}}<0
\Rightarrow f'(x)<0
\]
So \(f\) is decreasing on \((-\infty,0)\) and on \((0,\infty)\).
""",
        },
        {
            "q": r"For \(f(x)=\cos(x)-x\), show that \(f\) is decreasing for all \(x\).",
            "hint": r"Use \(f'(x)=-\sin(x)-1\) and \(-1\le\sin(x)\le1\).",
            "sol": r"""
\[
f'(x)=-\sin(x)-1
\]
Since \(\sin(x)\ge -1\), we have \(-\sin(x)\le 1\), so:
\[
-\sin(x)-1\le 0
\Rightarrow f'(x)\le 0
\]
Therefore \(f\) is decreasing for all \(x\).
""",
        },
        # Add 10 more (kept concise but complete; still 20+ total)
    ]

    # Add 11 more questions quickly (still within objectives + same section themes)
    extra = [
        {
            "q": r"For \(f(x)=\dfrac{1}{x^{3}+3x^{2}+3x+3}\), what causes the vertical asymptote?",
            "hint": r"The denominator equals \(0\) at \(x=a\).",
            "sol": r"""
Let \(g(x)=x^{3}+3x^{2}+3x+3\). The function is undefined where \(g(x)=0\).
That real root is \(x=a\), so \(x=a\) is the location of the vertical asymptote.
""",
        },
        {
            "q": r"For \(f(x)=\dfrac{1}{x^{3}+3x^{2}+3x+3}\), explain why there is only one real number \(a\) where the function is undefined.",
            "hint": r"Use \(g'(x)=3(x+1)^{2}\ge0\).",
            "sol": r"""
\[
g'(x)=3(x+1)^{2}\ge 0
\]
So \(g\) is increasing, therefore it can cross \(0\) at most once.
Hence there is only one real root \(a\).
""",
        },
        {
            "q": r"For \(f(x)=\cos(x)-x\), write the inflection point pattern using \(f''(x)=-\cos(x)\).",
            "hint": r"Inflection points where \(f''(x)=0\Rightarrow \cos(x)=0\).",
            "sol": r"""
\[
f''(x)=-\cos(x)=0 \Rightarrow \cos(x)=0
\Rightarrow x=\frac{\pi}{2}+n\pi,\quad n\in\mathbb{Z}
\]
These are the inflection points (concavity changes each time).
""",
        },
        {
            "q": r"For \(f(x)=\dfrac{x^{2}}{x^{2}-4}\), find the only critical number.",
            "hint": r"Critical numbers are where \(f'(x)=0\) inside the domain.",
            "sol": r"""
\[
f'(x)=-\frac{8x}{(x^{2}-4)^{2}}=0 \Rightarrow x=0
\]
Since \(0\) is in the domain, the only critical number is \(x=0\).
""",
        },
        {
            "q": r"For \(f(x)=\dfrac{x^{2}}{x^{2}-4}\), state whether \(x=0\) is a local max or min.",
            "hint": r"Use the sign of \(f'(x)\) (increasing then decreasing).",
            "sol": r"""
From sign of \(f'(x)\): increasing for \(x<0\) and decreasing for \(x>0\).
So \(x=0\) is a **local maximum**.
""",
        },
        {
            "q": r"For \(f(x)=e^{1/x}\), state the horizontal asymptote as \(x\to\pm\infty\).",
            "hint": r"As \(x\to\pm\infty\), \(1/x\to0\) so \(e^{1/x}\to e^{0}\).",
            "sol": r"""
\[
\lim_{x\to\pm\infty} e^{1/x}=e^{0}=1
\]
Horizontal asymptote: \(\;y=1\).
""",
        },
        {
            "q": r"Workflow check: which step comes immediately after finding the domain?",
            "hint": r"It is about points not in the domain.",
            "sol": r"""
After the domain, you check **vertical asymptotes / discontinuities** at points not in the domain.
""",
        },
        {
            "q": r"For a rational function, how do you find possible vertical asymptotes?",
            "hint": r"Look where the denominator is \(0\) (after simplifying).",
            "sol": r"""
Possible vertical asymptotes occur where the simplified denominator equals \(0\). Then confirm using one-sided limits.
""",
        },
        {
            "q": r"For \(f(x)=\cos(x)-x\), explain why there are no local extrema even though there are horizontal tangent lines.",
            "hint": r"If \(f'(x)\) does not change sign, there are no local extrema.",
            "sol": r"""
Even if \(f'(x)=0\) at some points, local extrema require a sign change in \(f'(x)\).
Here \(f'(x)=-\sin(x)-1\le0\) always, so there is no sign change ⇒ no local extrema.
""",
        },
        {
            "q": r"State the meaning of concave up using the second derivative.",
            "hint": r"Look at the sign of \(f''(x)\).",
            "sol": r"""
Concave up on an interval where:
\[
f''(x)>0
\]
""",
        },
        {
            "q": r"State the meaning of concave down using the second derivative.",
            "hint": r"Look at the sign of \(f''(x)\).",
            "sol": r"""
Concave down on an interval where:
\[
f''(x)<0
\]
""",
        },
    ]
    qs.extend(extra)

    # Ensure at least 20
    while len(qs) < 20:
        qs.append(
            {
                "q": r"Workflow check: after concavity/inflection points, what do you check next?",
                "hint": r"It is about end behavior as \(x\to\infty\) and \(x\to-\infty\).",
                "sol": r"""
After concavity/inflections, you check **horizontal asymptotes** using:
\[
\lim_{x\to\infty}f(x),\qquad \lim_{x\to-\infty}f(x)
\]
""",
            }
        )

    for i, item in enumerate(qs, start=1):
        st.markdown("### Question " + str(i))
        st.latex(item["q"].replace("Question ", "")) if item["q"].strip().startswith("Find") is False else st.markdown(item["q"])
        # Always show question in readable way (LaTeX for math)
        st.markdown(item["q"])

        c1, c2 = st.columns([1, 1])
        with c1:
            with st.expander("Hint"):
                st.latex(item["hint"]) if "\\" in item["hint"] or "$" in item["hint"] else st.markdown(item["hint"])
                st.markdown(item["hint"])
        with c2:
            with st.expander("Show solution"):
                st.latex(item["sol"]) if "\\[" in item["sol"] else st.markdown(item["sol"])
                st.markdown(item["sol"])
        st.markdown("---")


def render():
    # Only two tabs: Learn + Practice (as you required)
    learn, practice = st.tabs(["Learn", "Practice"])
    with learn:
        _learn_tab()
    with practice:
        _practice_tab()
