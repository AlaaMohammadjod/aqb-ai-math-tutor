import math
import time
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


# -----------------------------
# Helpers (math-first rendering)
# -----------------------------


def _md(s: str) -> None:
    """Markdown with LaTeX support. Use $...$ / $$...$$ for all math."""
    st.markdown(s)


def _latex(s: str) -> None:
    st.latex(s)


def _callout(kind: str, title: str, body_md: str) -> None:
    """Student-facing colored callouts."""
    icon = {
        "tip": "💡",
        "rule": "📌",
        "warning": "⚠️",
        "check": "✅",
        "exam": "📝",
    }.get(kind, "💬")

    if kind == "warning":
        st.warning(f"{icon} **{title}**\n\n{body_md}")
    elif kind == "check":
        st.success(f"{icon} **{title}**\n\n{body_md}")
    else:
        st.info(f"{icon} **{title}**\n\n{body_md}")


def _center_pyplot(fig, width_col_ratio=(1, 2, 1)) -> None:
    """Center a matplotlib figure (keeps graphs readable + stable)."""
    c1, c2, c3 = st.columns(list(width_col_ratio))
    with c2:
        st.pyplot(fig, clear_figure=True, use_container_width=False)


# -----------------------------
# Example bank
# -----------------------------


@dataclass
class SignChartExample:
    name: str
    f_latex: str
    fp_latex: str
    fp_factor_latex: str
    critical_points: list[float]
    intervals: list[tuple[float, float]]
    test_points: list[float]
    fp_signs: list[int]  # +1 or -1 per interval
    f: callable


def _example_bank() -> list[SignChartExample]:
    # Scenario A: Polynomial
    def fA(x: float) -> float:
        return x**3 - 3 * x

    # Scenario B: Rational
    def fB(x: float) -> float:
        return (x + 1) / (x - 2)

    # Scenario C: Trig
    def fC(x: float) -> float:
        return math.sin(x)

    return [
        SignChartExample(
            name="Scenario A (Polynomial)",
            f_latex=r"f(x)=x^3-3x",
            fp_latex=r"f'(x)=3x^2-3",
            fp_factor_latex=r"f'(x)=3(x^2-1)=3(x-1)(x+1)",
            critical_points=[-1.0, 1.0],
            intervals=[(-np.inf, -1.0), (-1.0, 1.0), (1.0, np.inf)],
            test_points=[-2.0, 0.0, 2.0],
            fp_signs=[+1, -1, +1],
            f=fA,
        ),
        SignChartExample(
            name="Scenario B (Rational function)",
            f_latex=r"f(x)=\dfrac{x+1}{x-2}",
            fp_latex=r"f'(x)=\dfrac{(x-2)\cdot 1-(x+1)\cdot 1}{(x-2)^2}",
            fp_factor_latex=r"f'(x)=\dfrac{-3}{(x-2)^2}",
            critical_points=[2.0],
            intervals=[(-np.inf, 2.0), (2.0, np.inf)],
            test_points=[0.0, 3.0],
            fp_signs=[-1, -1],
            f=fB,
        ),
        SignChartExample(
            name=r"Scenario C (Trig on $[0,2\pi]$)",
            f_latex=r"f(x)=\sin(x)\ \text{on }[0,2\pi]",
            fp_latex=r"f'(x)=\cos(x)",
            fp_factor_latex=r"\cos(x)=0\Rightarrow x=\dfrac{\pi}{2},\ \dfrac{3\pi}{2}",
            critical_points=[math.pi / 2, 3 * math.pi / 2],
            intervals=[(0.0, math.pi / 2), (math.pi / 2, 3 * math.pi / 2), (3 * math.pi / 2, 2 * math.pi)],
            test_points=[math.pi / 4, math.pi, 7 * math.pi / 4],
            fp_signs=[+1, -1, +1],
            f=fC,
        ),
    ]


# -----------------------------
# Board-style simulator (no sliders, no Next-step)
# -----------------------------


def _sign_chart_figure(example: SignChartExample, stage: int) -> plt.Figure:
    """Stages:
    0: number line
    1: mark critical points
    2: add interval labels
    3: add signs
    4: add conclusion
    """

    fig = plt.figure(figsize=(7.2, 2.6), dpi=140)
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    # Window for drawing
    cps = [c for c in example.critical_points if np.isfinite(c)]
    if len(cps) == 0:
        xmin, xmax = -3.0, 3.0
    else:
        xmin, xmax = min(cps) - 2.6, max(cps) + 2.6
    xmin, xmax = min(xmin, -3.2), max(xmax, 3.2)

    y0 = 0.0
    ax.plot([xmin, xmax], [y0, y0], linewidth=2)
    ax.annotate("", xy=(xmax, y0), xytext=(xmax - 0.25, y0), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("", xy=(xmin, y0), xytext=(xmin + 0.25, y0), arrowprops=dict(arrowstyle="<-", lw=2))

    ax.text((xmin + xmax) / 2, 0.9, r"Sign chart for $f'(x)$", ha="center", va="center", fontsize=14)
    ax.text((xmin + xmax) / 2, 0.55, f"${example.f_latex}$", ha="center", va="center", fontsize=12)

    # mark points
    if stage >= 1:
        for c in example.critical_points:
            if not np.isfinite(c):
                continue
            ax.plot([c, c], [y0 - 0.12, y0 + 0.12], linewidth=3)
            if example.name.startswith("Scenario C"):
                if abs(c - math.pi / 2) < 1e-9:
                    lab = r"$\dfrac{\pi}{2}$"
                elif abs(c - 3 * math.pi / 2) < 1e-9:
                    lab = r"$\dfrac{3\pi}{2}$"
                else:
                    lab = rf"${c:g}$"
            else:
                lab = rf"${c:g}$"
            ax.text(c, y0 - 0.35, lab, ha="center", va="center", fontsize=12)

        if example.name.startswith("Scenario B"):
            ax.text(2.0, y0 + 0.35, r"$x=2$ (undefined)", ha="center", va="center", fontsize=11)

    # interval labels
    if stage >= 2:
        for (a, b) in example.intervals:
            if np.isinf(a) and np.isfinite(b):
                xmid = b - 1.2
                lab = rf"$(-\infty,{b:g})$"
            elif np.isfinite(a) and np.isinf(b):
                xmid = a + 1.2
                lab = rf"$({a:g},\infty)$"
            else:
                xmid = (a + b) / 2
                if example.name.startswith("Scenario C"):

                    def _pi(xv: float) -> str:
                        if abs(xv - 0.0) < 1e-9:
                            return r"0"
                        if abs(xv - math.pi / 2) < 1e-9:
                            return r"\dfrac{\pi}{2}"
                        if abs(xv - math.pi) < 1e-9:
                            return r"\pi"
                        if abs(xv - 3 * math.pi / 2) < 1e-9:
                            return r"\dfrac{3\pi}{2}"
                        if abs(xv - 2 * math.pi) < 1e-9:
                            return r"2\pi"
                        return f"{xv:g}"

                    lab = rf"$({ _pi(a) },{ _pi(b) })$"
                else:
                    lab = rf"$({a:g},{b:g})$"

            ax.text(xmid, y0 - 0.65, lab, ha="center", va="center", fontsize=11, alpha=0.9)

    # signs
    if stage >= 3:
        for (a, b), sgn in zip(example.intervals, example.fp_signs):
            if np.isinf(a) and np.isfinite(b):
                xmid = b - 1.2
            elif np.isfinite(a) and np.isinf(b):
                xmid = a + 1.2
            else:
                xmid = (a + b) / 2

            symbol = r"+" if sgn > 0 else r"-"
            ax.text(xmid, y0 + 0.25, rf"$\mathbf{{{symbol}}}$", ha="center", va="center", fontsize=18)

    # conclusion
    if stage >= 4:
        inc_parts, dec_parts = [], []
        for (a, b), sgn in zip(example.intervals, example.fp_signs):
            if example.name.startswith("Scenario C"):

                def _pi(xv: float) -> str:
                    if abs(xv - 0.0) < 1e-9:
                        return r"0"
                    if abs(xv - math.pi / 2) < 1e-9:
                        return r"\dfrac{\pi}{2}"
                    if abs(xv - math.pi) < 1e-9:
                        return r"\pi"
                    if abs(xv - 3 * math.pi / 2) < 1e-9:
                        return r"\dfrac{3\pi}{2}"
                    if abs(xv - 2 * math.pi) < 1e-9:
                        return r"2\pi"
                    return f"{xv:g}"

                seg = rf"({ _pi(a) },{ _pi(b) })"
            else:
                if np.isinf(a):
                    seg = rf"(-\infty,{b:g})"
                elif np.isinf(b):
                    seg = rf"({a:g},\infty)"
                else:
                    seg = rf"({a:g},{b:g})"

            (inc_parts if sgn > 0 else dec_parts).append(seg)

        def _join(parts: list[str]) -> str:
            if len(parts) == 0:
                return r"\varnothing"
            if len(parts) == 1:
                return parts[0]
            return r"\cup".join(parts)

        inc = _join(inc_parts)
        dec = _join(dec_parts)
        ax.text(
            (xmin + xmax) / 2,
            -1.05,
            rf"$f\ \text{{increasing on }}{inc}\qquad f\ \text{{decreasing on }}{dec}$",
            ha="center",
            va="center",
            fontsize=12,
        )

    ax.set_xlim(xmin - 0.2, xmax + 0.2)
    ax.set_ylim(-1.35, 1.05)
    return fig


def _function_with_arrows_figure(example: SignChartExample, stage: int) -> plt.Figure:
    """Stage 0: curve only; then adds arrows interval-by-interval."""

    fig = plt.figure(figsize=(7.2, 3.2), dpi=140)
    ax = fig.add_subplot(111)

    if example.name.startswith("Scenario C"):
        xs = np.linspace(0, 2 * math.pi, 600)
        xticks = [0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi]
        xtlabels = [r"$0$", r"$\dfrac{\pi}{2}$", r"$\pi$", r"$\dfrac{3\pi}{2}$", r"$2\pi$"]
    else:
        xs = np.linspace(-4, 4, 700)
        xticks = [-4, -2, -1, 0, 1, 2, 4]
        xtlabels = [rf"${t:g}$" for t in xticks]

    ys = np.array([example.f(float(x)) for x in xs])

    if example.name.startswith("Scenario B"):
        ys = np.clip(ys, -8, 8)
        ax.axvline(2, linestyle="--", linewidth=1.5)

    ax.plot(xs, ys, linewidth=2)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.set_title(r"Function sketch with rise/fall arrows", fontsize=13)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtlabels)

    intervals = example.intervals
    for k in range(min(stage, len(intervals))):
        a, b = intervals[k]
        sgn = example.fp_signs[k]

        if np.isinf(a) and np.isfinite(b):
            x0 = b - 2.0
        elif np.isfinite(a) and np.isinf(b):
            x0 = a + 2.0
        else:
            x0 = (a + b) / 2

        x0 = float(np.clip(x0, xs.min() + 0.2, xs.max() - 0.2))
        y0 = float(example.f(x0))
        y0 = float(np.clip(y0, ys.min() + 0.4, ys.max() - 0.4))

        dx = 0.6
        dy = 1.0 if sgn > 0 else -1.0

        ax.annotate(
            "",
            xy=(x0 + dx, y0 + dy),
            xytext=(x0 - dx, y0 - dy),
            arrowprops=dict(arrowstyle="->", lw=2),
        )
        ax.text(
            x0,
            y0 + (1.25 if sgn > 0 else -1.25),
            r"$\nearrow$" if sgn > 0 else r"$\searrow$",
            ha="center",
            va="center",
            fontsize=14,
        )

    ax.set_ylim(ys.min() - 1.0, ys.max() + 1.0)
    return fig


def _board_simulator(example: SignChartExample) -> None:
    _callout(
        "rule",
        "Board simulator (watch the whole solution happen)",
        "Press **Start** and the board will build the solution automatically.",
    )

    cols = st.columns([1, 1, 1])
    with cols[0]:
        start = st.button("Start", key=f"sim_start_{example.name}")
    with cols[1]:
        speed = st.selectbox(
            "Speed",
            options=["1×", "1.5×", "2×"],
            index=0,
            key=f"sim_speed_{example.name}",
        )
    with cols[2]:
        st.write("")

    delay = {"1×": 0.85, "1.5×": 0.55, "2×": 0.35}[speed]

    # Fixed placeholders (prevents content "dropping" when the page updates)
    sign_ph = st.empty()
    func_ph = st.empty()
    steps_ph = st.empty()

    # Always show full worked steps (no hidden buttons)
    with steps_ph.container():
        st.subheader("Worked steps (fully solved)")
        _latex(example.f_latex)
        _latex(example.fp_latex)
        _latex(example.fp_factor_latex)

        if example.name.startswith("Scenario C"):
            _latex(r"\text{Critical numbers on }[0,2\pi]:\ \dfrac{\pi}{2},\ \dfrac{3\pi}{2}.")
        elif example.name.startswith("Scenario B"):
            _latex(r"\text{Domain note: }x=2\text{ is not allowed, so it splits the number line.}")
        else:
            _latex(r"f'(x)=0\Rightarrow x=-1,\ x=1.")

        _latex(r"\text{Choose a test value in each interval to find the sign of }f'(x).")
        for tp, sgn in zip(example.test_points, example.fp_signs):
            sign_symbol = r">0" if sgn > 0 else r"<0"
            if example.name.startswith("Scenario C"):
                if abs(tp - math.pi / 4) < 1e-9:
                    _latex(r"x=\dfrac{\pi}{4}:\ \cos\left(\dfrac{\pi}{4}\right)=\dfrac{\sqrt{2}}{2}>0")
                elif abs(tp - math.pi) < 1e-9:
                    _latex(r"x=\pi:\ \cos(\pi)=-1<0")
                else:
                    _latex(r"x=\dfrac{7\pi}{4}:\ \cos\left(\dfrac{7\pi}{4}\right)=\dfrac{\sqrt{2}}{2}>0")
            else:
                _latex(rf"x={tp:g}:\ f'({tp:g})\ {sign_symbol}.")

        _latex(r"f'(x)>0\Rightarrow f\text{ increasing}\qquad f'(x)<0\Rightarrow f\text{ decreasing.}")

    if not start:
        # Preview final state (readable + centered)
        fig_sc = _sign_chart_figure(example, stage=4)
        fig_fn = _function_with_arrows_figure(example, stage=len(example.intervals))
        with sign_ph.container():
            _center_pyplot(fig_sc)
        with func_ph.container():
            _center_pyplot(fig_fn)
        return

    # Animate sign chart
    for s in range(0, 5):
        fig_sc = _sign_chart_figure(example, stage=s)
        with sign_ph.container():
            _center_pyplot(fig_sc)
        time.sleep(delay)

    # Animate function arrows
    for s in range(0, len(example.intervals) + 1):
        fig_fn = _function_with_arrows_figure(example, stage=s)
        with func_ph.container():
            _center_pyplot(fig_fn)
        time.sleep(delay)


# -----------------------------
# Learn tab (EXPANDED ONLY)
# -----------------------------


def _learn_tab() -> None:
    st.subheader("Learning objectives")
    _md(
        "- **5.4.1** Define increasing/decreasing regions using graphs, real-life meaning, and the formal two-point definition.\n"
        "- **5.4.2** Find intervals where a function is increasing/decreasing and identify any local extrema (using $f(x)$, $f'(x)$, or the graph of $f'(x)$).\n"
        "- **5.4.3** Sketch a graph of $f(x)$ from information about $f$ and $f'$."
    )

    st.divider()

    # -----------------------
    # 5.4.1 (expanded)
    # -----------------------
    st.subheader(r"5.4.1 — Increasing/decreasing (definition + graph reading)")

    _callout(
        "rule",
        "Formal definition (two points)",
        "A function $f$ is **increasing** on an interval if whenever $x_1<x_2$ (both in the interval), then $f(x_1)<f(x_2)$.\n\n"
        "A function $f$ is **decreasing** on an interval if whenever $x_1<x_2$ (both in the interval), then $f(x_1)>f(x_2)$.",
    )

    _callout(
        "tip",
        "Real-life meaning",
        "- Increasing: when the input grows, the output grows (example: total cost vs number of items).\n"
        "- Decreasing: when the input grows, the output falls (example: remaining battery vs time).\n"
        "- Constant: output does not change as input changes.",
    )

    _callout(
        "tip",
        "How to read a graph (exactly what to look for)",
        "- Horizontal axis is $x$ and vertical axis is $y=f(x)$.\n"
        "- Move left-to-right: curve goes **up** $\Rightarrow$ $f$ increasing; curve goes **down** $\Rightarrow$ $f$ decreasing.\n"
        "- A **flat** part means slope is near $0$.\n"
        "- A sharp corner or vertical tangent often means $f'(x)$ is undefined there.",
    )

    _callout(
        "check",
        "Micro-check (graph reading)",
        "If the curve rises from left to right on $(a,b)$, then you must write:\n\n"
        "- $f$ is increasing on $(a,b)$.\n\n"
        "If it falls, then:\n\n"
        "- $f$ is decreasing on $(a,b)$.",
    )

    st.markdown("### Connecting graphs to derivatives (very important)")
    _callout(
        "rule",
        "Derivative connection",
        "The derivative $f'(x)$ measures slope.\n\n"
        "- $f'(x)>0$ means slope is positive $\Rightarrow$ $f$ increasing.\n"
        "- $f'(x)<0$ means slope is negative $\Rightarrow$ $f$ decreasing.\n"
        "- $f'(x)=0$ means slope is flat (horizontal tangent).\n"
        "- $f'(x)$ undefined means corner/vertical tangent (possible turning behavior).",
    )

    st.divider()

    # -----------------------
    # 5.4.2 (expanded)
    # -----------------------
    st.subheader(r"5.4.2 — Intervals + local extrema (sign chart method)")

    _callout(
        "rule",
        "Exam method (you must show these steps)",
        "1) Find (or read) $f'(x)$.\n"
        "2) Solve $f'(x)=0$ and note where $f'(x)$ is undefined **while $f(x)$ is defined**.\n"
        "3) Split the number line into intervals.\n"
        "4) Choose one test value per interval to determine the sign of $f'(x)$.\n"
        "5) Translate signs into increasing/decreasing for $f$.\n"
        "6) Local extrema: $+\to-$ gives a local maximum; $-\to+$ gives a local minimum.",
    )

    _callout(
        "tip",
        "How to choose test points fast",
        "Pick easy numbers inside each interval:\n"
        "- Between $(-\infty,-1)$ choose $-2$.\n"
        "- Between $(-1,1)$ choose $0$.\n"
        "- Between $(1,\infty)$ choose $2$.\n\n"
        "Your goal is only the sign of $f'(x)$, not the exact value.",
    )

    _callout(
        "warning",
        "Common mistake",
        "Do **not** say “increasing at a point.”\n\n"
        "You must say “increasing on an interval,” like $(1,\infty)$ or $(0,\pi)$.",
    )

    st.markdown("### Worked example 1 — Full board solution")
    _callout(
        "exam",
        "Question",
        "Find where $f(x)=x^3-3x$ is increasing/decreasing and identify any local extrema.",
    )
    exA = _example_bank()[0]
    _board_simulator(exA)

    st.markdown("### Worked example 2 — Using $f'(x)$ directly (no need for $f(x)$)")
    _callout(
        "exam",
        "Question",
        "A derivative is given by $f'(x)=(x-2)(x+1)$. Find where $f$ is increasing/decreasing and identify any local extrema.",
    )

    _latex(r"f'(x)=(x-2)(x+1)")
    _latex(r"f'(x)=0\Rightarrow x=-1,\ 2")
    _latex(r"\text{Intervals: }(-\infty,-1),\ (-1,2),\ (2,\infty)")
    _latex(r"\text{Sign of }(x-2)(x+1):\ (+),\ (-),\ (+)")
    _latex(r"\boxed{\text{Increasing: }(-\infty,-1)\cup(2,\infty)}")
    _latex(r"\boxed{\text{Decreasing: }(-1,2)}")
    _latex(r"(+\to-)\Rightarrow \text{local maximum at }x=-1\qquad(-\to+)\Rightarrow \text{local minimum at }x=2")

    _callout(
        "tip",
        "Why this works",
        "To decide increasing/decreasing, you only need the **sign** of $f'(x)$.\n\n"
        "You do not need the full equation of $f(x)$ unless the question asks for values of $f$.",
    )

    st.markdown("### Worked example 3 — Domain matters (rational)")
    _callout(
        "exam",
        "Question",
        "Find where $f(x)=\dfrac{x+1}{x-2}$ is increasing/decreasing.",
    )
    exB = _example_bank()[1]
    _board_simulator(exB)

    _callout(
        "warning",
        "Domain rule you must remember",
        "If $f(x)$ is not defined at a point, you cannot include that point in an interval.\n\n"
        "That point breaks the number line into separate intervals.",
    )

    st.markdown(r"### Worked example 4 — Trig on a closed interval (use $\pi$)")
    _callout(
        "exam",
        "Question",
        "On $[0,2\pi]$, find where $f(x)=\sin(x)$ is increasing/decreasing and identify any local extrema inside the interval.",
    )
    exC = _example_bank()[2]
    _board_simulator(exC)

    _callout(
        "tip",
        r"Trig memory trick",
        r"On $[0,2\pi]$:\n\n"
        r"- $\cos(x)>0$ on $\left(0,\dfrac{\pi}{2}\right)\cup\left(\dfrac{3\pi}{2},2\pi\right)$\n"
        r"- $\cos(x)<0$ on $\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)$",
    )

    st.divider()

    # -----------------------
    # NEW: Tables of variation (worked examples)
    # -----------------------
    st.subheader(r"Tables of variation (a teacher-style way to present your sign chart)")
    _callout(
        "rule",
        "What a table of variation shows",
        "A table of variation is a compact summary:\n\n"
        "- critical numbers on the $x$-line,\n"
        "- the sign of $f'(x)$ on each interval,\n"
        "- arrows showing $f$ increasing ($\nearrow$) or decreasing ($\searrow$),\n"
        "- and where local maxima/minima happen (from sign change).",
    )

    _callout(
        "tip",
        "How to convert sign to arrows",
        r"$f'(x)>0\Rightarrow f$ goes up $\Rightarrow \nearrow$"
        "\n\n"
        r"$f'(x)<0\Rightarrow f$ goes down $\Rightarrow \searrow$",
    )

    st.markdown("### Variation example V1 (polynomial)")
    _callout(
        "exam",
        "Question",
        r"For $f(x)=x^3-3x$, create a table of variation and state increasing/decreasing intervals and local extrema.",
    )
    _latex(r"f'(x)=3(x-1)(x+1)")
    _latex(r"f'(x)=0\Rightarrow x=-1,\ 1")

    _md(
        r"""
**Table of variation (summary):**

| $x$ | $(-\infty,-1)$ | $-1$ | $(-1,1)$ | $1$ | $(1,\infty)$ |
|---|---:|:---:|---:|:---:|---:|
| $f'(x)$ | $+$ | $0$ | $-$ | $0$ | $+$ |
| $f$ | $\nearrow$ |  | $\searrow$ |  | $\nearrow$ |

**Conclusion:**
- Increasing on $(-\infty,-1)\cup(1,\infty)$  
- Decreasing on $(-1,1)$  
- $+\to-$ at $x=-1$ $\Rightarrow$ local maximum  
- $-\to+$ at $x=1$ $\Rightarrow$ local minimum
"""
    )

    st.markdown("### Variation example V2 (rational — domain breaks the table)")
    _callout(
        "exam",
        "Question",
        r"For $f(x)=\dfrac{x+1}{x-2}$, use a variation table idea to describe monotonicity.",
    )
    _latex(r"f'(x)=\dfrac{-3}{(x-2)^2}<0\ \text{for }x\ne 2")
    _md(
        r"""
Because $x=2$ is not in the domain, the “table” must split:

| $x$ | $(-\infty,2)$ | $2$ | $(2,\infty)$ |
|---|---:|:---:|---:|
| $f'(x)$ | $-$ | undefined | $-$ |
| $f$ | $\searrow$ |  | $\searrow$ |

**Conclusion:** decreasing on $(-\infty,2)\cup(2,\infty)$.
"""
    )

    st.markdown(r"### Variation example V3 (trig on $[0,2\pi]$ — use $\pi$)")
    _callout(
        "exam",
        "Question",
        r"For $f(x)=\sin(x)$ on $[0,2\pi]$, produce the variation idea and intervals.",
    )
    _latex(r"f'(x)=\cos(x)")
    _latex(r"\cos(x)=0\Rightarrow x=\dfrac{\pi}{2},\ \dfrac{3\pi}{2}")
    _md(
        r"""
| $x$ | $(0,\frac{\pi}{2})$ | $\frac{\pi}{2}$ | $(\frac{\pi}{2},\frac{3\pi}{2})$ | $\frac{3\pi}{2}$ | $(\frac{3\pi}{2},2\pi)$ |
|---|---:|:---:|---:|:---:|---:|
| $\cos(x)$ | $+$ | $0$ | $-$ | $0$ | $+$ |
| $\sin(x)$ | $\nearrow$ |  | $\searrow$ |  | $\nearrow$ |

**Conclusion:** increasing on $\left(0,\dfrac{\pi}{2}\right)\cup\left(\dfrac{3\pi}{2},2\pi\right)$ and decreasing on $\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)$.
"""
    )

    st.divider()

    # -----------------------
    # NEW: Cases where f'(x) is undefined (corner / vertical tangent)
    # -----------------------
    st.subheader(r"When $f'(x)$ is undefined (corners and vertical tangents)")
    _callout(
        "rule",
        "Critical numbers include undefined derivatives",
        r"A number $c$ is a critical number if:"
        "\n\n"
        r"- $f'(c)=0$, **or**"
        "\n"
        r"- $f'(c)$ is undefined **and** $f(c)$ is defined.",
    )

    st.markdown("### Undefined derivative example U1 (corner)")
    _callout(
        "exam",
        "Question",
        r"Consider $f(x)=|x|$. Describe increasing/decreasing and the extremum.",
    )
    _latex(r"f(x)=|x|=\begin{cases}-x,&x<0\\x,&x\ge 0\end{cases}")
    _latex(r"f'(x)=\begin{cases}-1,&x<0\\1,&x>0\end{cases}\qquad \text{and }f'(0)\text{ is undefined (corner).}")
    _md(
        r"""
- On $(-\infty,0)$, $f'(x)=-1<0$ so $f$ is decreasing.  
- On $(0,\infty)$, $f'(x)=1>0$ so $f$ is increasing.  

Sign change is $(-\to+)$ at $x=0$, so $x=0$ is a **local minimum** (and also the absolute minimum).
"""
    )

    st.markdown("### Undefined derivative example U2 (vertical tangent)")
    _callout(
        "exam",
        "Question",
        r"Consider $f(x)=x^{1/3}$. Explain why $f'(0)$ is undefined and what happens to increasing/decreasing.",
    )
    _latex(r"f(x)=x^{1/3}")
    _latex(r"f'(x)=\dfrac{1}{3}x^{-2/3}=\dfrac{1}{3\sqrt[3]{x^2}}")
    _latex(r"f'(0)\text{ is undefined (vertical tangent), but }f(0)\text{ exists.}")
    _md(
        r"""
For $x\ne 0$, we have $\sqrt[3]{x^2}>0$, so
\[
f'(x)=\dfrac{1}{3\sqrt[3]{x^2}}>0
\]
on both sides of $0$.

**Conclusion:**
- $f$ is increasing on $(-\infty,0)$ and on $(0,\infty)$ (and in fact increasing overall).
- Because the sign does **not** change, there is **no** local maximum/minimum at $x=0$.
- The point $x=0$ is still a critical number because the derivative is undefined there.
"""
    )

    _callout(
        "warning",
        "Key exam sentence",
        r"“$f'(c)$ is undefined” does **not** automatically mean “turning point.” You must check the sign before and after $c$.",
    )

    st.divider()

    # -----------------------
    # Reading a derivative graph (already in your version)
    # -----------------------
    st.subheader(r"Reading the graph of $f'(x)$ (when $f'(x)$ is given as a graph)")
    _callout(
        "rule",
        "How to use a derivative graph",
        "If you are given the graph of $f'(x)$:\n\n"
        "- Where the graph is **above** the $x$-axis, $f'(x)>0$ so $f$ is increasing.\n"
        "- Where the graph is **below** the $x$-axis, $f'(x)<0$ so $f$ is decreasing.\n"
        "- Where it crosses the $x$-axis, $f'(x)=0$ (critical number).\n\n"
        "Then you use sign changes to decide local maxima/minima of $f$.",
    )

    _callout(
        "check",
        "Mini example (no calculations)",
        "If the graph of $f'(x)$ is positive on $(-\infty,-2)$, negative on $(-2,1)$, and positive on $(1,\infty)$, then:\n\n"
        "- $f$ increases, then decreases, then increases.\n"
        "- $x=-2$ is a local maximum.\n"
        "- $x=1$ is a local minimum.",
    )

    st.divider()

    # -----------------------
    # 5.4.3 (expanded) — sketching
    # -----------------------
    st.subheader(r"5.4.3 — Sketching $f$ from $f'$ information")

    _callout(
        "tip",
        "Sketch checklist (do this every time)",
        "- Step 1: Mark critical numbers where $f'(x)=0$ or undefined.\n"
        "- Step 2: Use the sign of $f'(x)$ to decide where $f$ rises/falls.\n"
        "- Step 3: Put turning points where the sign changes.\n"
        "- Step 4: Draw a smooth curve that matches that behavior.\n\n"
        "You are drawing a **behavior sketch**, not a perfect scale graph.",
    )

    _callout(
        "rule",
        "Turning point rule",
        "- If $f'(x)$ changes $+\to-$ at $x=c$, then $f$ has a local maximum at $x=c$.\n"
        "- If $f'(x)$ changes $-\to+$ at $x=c$, then $f$ has a local minimum at $x=c$.\n"
        "- If there is no sign change, there is no local maximum/minimum.",
    )

    _callout(
        "tip",
        "What to write in words (strong answers)",
        "A complete answer includes:\n\n"
        "- the critical numbers,\n"
        "- the test intervals,\n"
        "- the sign of $f'(x)$ on each interval,\n"
        "- the final increasing/decreasing intervals,\n"
        "- and any local extrema with sign-change justification.",
    )

    _callout(
        "rule",
        "Sketch scenario (guided)",
        "If $f'(x)>0$ on $(-\infty,-2)$, $f'(x)<0$ on $(-2,1)$, and $f'(x)>0$ on $(1,\infty)$:\n\n"
        "1) Write increasing/decreasing intervals.\n"
        "2) Identify the local maximum and local minimum.\n"
        "3) Sketch a curve that rises, then falls, then rises.",
    )

    # Representative sketch (clear, centered)
    fig = plt.figure(figsize=(7.2, 3.2), dpi=140)
    ax = fig.add_subplot(111)
    xs = np.linspace(-4, 4, 700)
    ys = (xs**3) / 3 + (xs**2) / 2 - 2 * xs  # derivative sign pattern: (x+2)(x-1)
    ax.plot(xs, ys, linewidth=2)
    ax.axvline(-2, linewidth=1)
    ax.axvline(1, linewidth=1)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_title(r"Representative sketch from $f'(x)$ sign information", fontsize=13)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    _center_pyplot(fig)

    _callout(
        "check",
        "Conclusion (model answer style)",
        "$f$ is increasing on $(-\infty,-2)\cup(1,\infty)$ and decreasing on $(-2,1)$.\n\n"
        "Therefore, there is a local maximum at $x=-2$ and a local minimum at $x=1$.",
    )

    st.divider()

    # -----------------------
    # NEW: Link to 5.3 extrema (connection section)
    # -----------------------
    st.subheader(r"Connection to 5.3 (Maximum/Minimum values) — how topics connect")
    _callout(
        "rule",
        "Local vs absolute (5.3 and 5.4 together)",
        "In **5.4**, you decide **where the function rises/falls** using the sign of $f'(x)$.\n\n"
        "In **5.3**, you decide **max/min values** (local and absolute). The workflow connects like this:\n\n"
        "1) Use **5.4** to find critical numbers and monotonic intervals.\n"
        "2) Use sign change to label **local maxima/minima**.\n"
        "3) For **absolute extrema on a closed interval** $[a,b]$, you must also check **endpoints** $a$ and $b$ (5.3 / EVT idea).",
    )

    _callout(
        "tip",
        "Absolute extrema on $[a,b]$ (fast exam checklist)",
        r"To find absolute max/min on a closed interval $[a,b]$:"
        "\n\n"
        r"- Find critical numbers in $(a,b)$ where $f'(x)=0$ or $f'(x)$ is undefined,"
        "\n"
        r"- Evaluate $f$ at those critical numbers,"
        "\n"
        r"- Evaluate $f(a)$ and $f(b)$,"
        "\n"
        r"- Compare all values: largest is absolute maximum, smallest is absolute minimum.",
    )

    _callout(
        "warning",
        "What students often miss",
        r"A local maximum is not always an absolute maximum. On a closed interval, endpoints can beat the interior turning points."
        "\n\n"
        r"That is exactly why 5.3 (absolute extrema) needs the endpoint check.",
    )

    _callout(
        "warning",
        "Final common errors to avoid",
        "- Do not include a point where $f$ is undefined inside an interval.\n"
        "- Do not mix up the graph of $f$ with the graph of $f'(x)$.\n"
        "- Always write answers as intervals using parentheses: $(a,b)$.\n"
        "- Use $\pi$-form answers when trig is involved (for example, $\dfrac{\pi}{2}$).",
    )


# -----------------------------
# Practice tab (UNCHANGED)
# -----------------------------


def _qa(q_title: str, question_md: str, hint_md: str, solution_latex_lines: list[str]) -> None:
    st.markdown(f"#### {q_title}")
    _callout("exam", "Question", question_md)
    c1, c2 = st.columns([1, 1])
    with c1:
        with st.expander("Hint"):
            _md(hint_md)
    with c2:
        with st.expander("Show answer"):
            for line in solution_latex_lines:
                _latex(line)


def _practice_tab() -> None:
    st.subheader("Practice (20 questions)")
    _callout(
        "tip",
        "How to use this",
        "Solve first. Open **Hint** only if needed. Then open **Show answer** to compare with a full solution.",
    )

    st.divider()

    _qa(
        "Q1",
        "Use the two-point definition: If $f$ is increasing, what inequality connects $f(x_1)$ and $f(x_2)$ when $x_1<x_2$?",
        "Increasing means outputs get bigger when inputs get bigger.",
        [
            r"\text{If }x_1<x_2\text{ and }f\text{ is increasing, then }f(x_1)<f(x_2).",
        ],
    )

    _qa(
        "Q2",
        "A graph goes down as you move left-to-right on $(2,5)$. What does that mean about $f$ on $(2,5)$?",
        "Downward left-to-right means values decrease.",
        [
            r"\boxed{f\text{ is decreasing on }(2,5).}",
        ],
    )

    _qa(
        "Q3",
        "If $f'(x)>0$ for every $x$ in $(-3,4)$, what can you conclude about $f$?",
        "Derivative positive means rising.",
        [
            r"f'(x)>0\Rightarrow f\text{ increasing.}",
            r"\boxed{f\text{ is increasing on }(-3,4).}",
        ],
    )

    _qa(
        "Q4",
        "If $f'(x)<0$ for every $x$ in $(0,\pi)$, what can you conclude about $f$?",
        "Derivative negative means falling.",
        [
            r"f'(x)<0\Rightarrow f\text{ decreasing.}",
            r"\boxed{f\text{ is decreasing on }(0,\pi).}",
        ],
    )

    _qa(
        "Q5",
        "$f'(2)=0$ and $f'(x)$ changes from $+$ to $-$ at $x=2$. Identify the extremum.",
        "Sign change $+\to-$ means rise then fall.",
        [
            r"(+\to-)\Rightarrow \text{local maximum.}",
            r"\boxed{\text{Local maximum at }x=2.}",
        ],
    )

    _qa(
        "Q6",
        "For $f(x)=x^3-3x$, find increasing/decreasing intervals.",
        "Compute $f'(x)$ and build a sign chart.",
        [
            r"f'(x)=3x^2-3=3(x-1)(x+1)",
            r"f'(x)=0\Rightarrow x=-1,\ 1",
            r"\text{Signs: }(+),(-),(+)\text{ on }(-\infty,-1),(-1,1),(1,\infty)",
            r"\boxed{\text{Increasing: }(-\infty,-1)\cup(1,\infty)}",
            r"\boxed{\text{Decreasing: }(-1,1)}",
        ],
    )

    _qa(
        "Q7",
        "For $f(x)=x^4-4x^2$, find where $f$ is increasing/decreasing.",
        "Factor $f'(x)$ and use a sign chart.",
        [
            r"f'(x)=4x^3-8x=4x(x^2-2)=4x(x-\sqrt{2})(x+\sqrt{2})",
            r"\text{Critical numbers: }x=-\sqrt{2},\ 0,\ \sqrt{2}",
            r"\boxed{\text{Increasing: }(-\sqrt{2},0)\cup(\sqrt{2},\infty)}",
            r"\boxed{\text{Decreasing: }(-\infty,-\sqrt{2})\cup(0,\sqrt{2})}",
        ],
    )

    _qa(
        "Q8",
        "For $f(x)=\dfrac{x+1}{x-2}$, find where $f$ is increasing/decreasing.",
        "Differentiate; remember $x\ne 2$.",
        [
            r"f'(x)=\dfrac{-3}{(x-2)^2}<0\text{ for }x\ne 2",
            r"\boxed{\text{Decreasing on }(-\infty,2)\cup(2,\infty)}",
            r"\boxed{\text{Increasing: }\varnothing}",
        ],
    )

    _qa(
        "Q9",
        "On $[0,2\pi]$, for $f(x)=\sin(x)$ find increasing/decreasing intervals.",
        "Use $f'(x)=\cos(x)$ and cosine sign.",
        [
            r"f'(x)=\cos(x)",
            r"\cos(x)=0\Rightarrow x=\dfrac{\pi}{2},\ \dfrac{3\pi}{2}",
            r"\boxed{\text{Increasing: }\left(0,\dfrac{\pi}{2}\right)\cup\left(\dfrac{3\pi}{2},2\pi\right)}",
            r"\boxed{\text{Decreasing: }\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)}",
        ],
    )

    _qa(
        "Q10",
        "Given $f'(x)=(x+3)(x-1)^2$, find where $f$ is increasing/decreasing.",
        "Squared factor does not change sign.",
        [
            r"(x-1)^2\ge 0\text{ so sign depends on }(x+3)",
            r"\boxed{\text{Decreasing: }(-\infty,-3)}",
            r"\boxed{\text{Increasing: }(-3,1)\cup(1,\infty)}",
        ],
    )

    _qa(
        "Q11",
        "For $f(x)=\sqrt{x}$, find where $f$ is increasing/decreasing on its domain.",
        "Domain: $x\ge 0$. Derivative is positive for $x>0$.",
        [
            r"f'(x)=\dfrac{1}{2\sqrt{x}}>0\text{ for }x>0",
            r"\boxed{\text{Increasing on }(0,\infty)\text{ (and increasing on }[0,\infty)\text{ by the graph).}}",
            r"\boxed{\text{Decreasing: }\varnothing}",
        ],
    )

    _qa(
        "Q12",
        "$f'(x)$ is undefined at $x=0$ but $f(0)$ exists. Why is $0$ a critical number?",
        "Critical numbers: $f'(c)=0$ or undefined (with $f(c)$ defined).",
        [
            r"\text{Because }f\text{ is defined at }0\text{ and }f'(0)\text{ is undefined, }0\text{ is a critical number.}",
        ],
    )

    _qa(
        "Q13",
        "Suppose $f'(x)>0$ on $(-\infty,-2)$, $f'(x)<0$ on $(-2,1)$, and $f'(x)>0$ on $(1,\infty)$. State intervals and extrema.",
        "Translate sign to motion; sign change gives extrema.",
        [
            r"\boxed{\text{Increasing: }(-\infty,-2)\cup(1,\infty)}",
            r"\boxed{\text{Decreasing: }(-2,1)}",
            r"(+\to-)\Rightarrow \text{local maximum at }x=-2",
            r"(-\to+)\Rightarrow \text{local minimum at }x=1",
        ],
    )

    _qa(
        "Q14",
        "A derivative graph lies below the $x$-axis on $(-5,5)$. What does that mean for $f$ on $(-5,5)$?",
        "Below axis means negative derivative.",
        [
            r"f'(x)<0\Rightarrow f\text{ decreasing.}",
            r"\boxed{f\text{ is decreasing on }(-5,5).}",
        ],
    )

    _qa(
        "Q15",
        "$f'(3)=0$ but $f'(x)>0$ on both sides of $3$. What happens at $x=3$?",
        "No sign change means no local max/min.",
        [
            r"\text{No sign change }\Rightarrow \text{no local extremum at }x=3.",
        ],
    )

    _qa(
        "Q16",
        "Why are increasing/decreasing intervals written as open intervals even when the domain is closed like $[a,b]$?",
        "Monotonicity is described on intervals between critical numbers.",
        [
            r"\text{You report monotonic intervals between critical numbers as open intervals, e.g. }(a,c),(c,b).",
            r"\text{Endpoints matter for absolute extrema, but monotonic intervals are written open.}",
        ],
    )

    _qa(
        "Q17",
        "Find intervals of increase/decrease for $f(x)=x-\ln(x)$ on $(0,\infty)$.",
        "Compute $f'(x)=1-1/x$.",
        [
            r"f'(x)=1-\dfrac{1}{x}=\dfrac{x-1}{x}",
            r"\boxed{\text{Decreasing: }(0,1)}",
            r"\boxed{\text{Increasing: }(1,\infty)}",
        ],
    )

    _qa(
        "Q18",
        "$f'(x)=\dfrac{x}{\sqrt{1-x^2}}$ on $(-1,1)$. Find increasing/decreasing.",
        "Denominator positive on $(-1,1)$.",
        [
            r"\text{Sign matches }x\text{ on }(-1,1)",
            r"\boxed{\text{Decreasing: }(-1,0)}",
            r"\boxed{\text{Increasing: }(0,1)}",
        ],
    )

    _qa(
        "Q19",
        "Given $f'(x)=-(x-2)(x+4)$, find intervals and local extrema.",
        "Negative sign flips the sign chart.",
        [
            r"f'(x)=0\Rightarrow x=-4,\ 2",
            r"\boxed{\text{Increasing: }(-4,2)}",
            r"\boxed{\text{Decreasing: }(-\infty,-4)\cup(2,\infty)}",
            r"(-\to+)\Rightarrow \text{local minimum at }x=-4\qquad(+\to-)\Rightarrow \text{local maximum at }x=2",
        ],
    )

    _qa(
        "Q20",
        "Sketch-only: $f'(x)$ is positive, then zero at $x=1$, then negative, then zero at $x=4$, then positive again. Describe the shape of $f$.",
        "Translate $+\to 0\to -\to 0\to +$.",
        [
            r"\text{Rises until }x=1\text{ (local maximum at }x=1).",
            r"\text{Falls from }x=1\text{ to }x=4\text{ (local minimum at }x=4).",
            r"\text{Rises again for }x>4.",
        ],
    )


def render() -> None:
    st.header("Subtopic 5.4: Increasing and Decreasing Functions")
    st.caption("Topic 5 • Applications of Differentiation")

    tabs = st.tabs(["Learn", "Practice"])
    with tabs[0]:
        _learn_tab()
    with tabs[1]:
        _practice_tab()