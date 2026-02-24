# subtopic_5_5_concavity_second_derivative_test.py
import streamlit as st

# Optional: use the shared simulator from simulations.py if it exists in your project.
# (If not found, this file falls back to an internal board simulator.)
try:
    from simulations import render_blackboard_simulator  # type: ignore
    _HAS_SHARED_BOARD = True
except Exception:
    render_blackboard_simulator = None  # type: ignore
    _HAS_SHARED_BOARD = False

from subtopic_5_5_concavity_second_derivative_test_practice import render_practice


# -----------------------------
# Helpers (NO plain-text math)
# -----------------------------
def _H(txt: str) -> None:
    st.markdown(f"### {txt}")


def _P(txt: str) -> None:
    st.markdown(txt)


def _L(latex: str) -> None:
    # Always LaTeX/KaTeX for any math
    st.latex(latex)


def _card(title: str, body_md: str) -> None:
    st.markdown(
        f"""
<div style="border:1px solid #E6EEF8; background:#F7FBFF; padding:14px 14px; border-radius:12px;">
  <div style="font-weight:700; color:#1F4B8F; margin-bottom:6px;">{title}</div>
  <div style="color:#1F2937; line-height:1.55;">{body_md}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _rule() -> None:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)


# -----------------------------
# Internal board simulator (fallback)
# Auto-writes FULL solution (no next-step buttons)
# -----------------------------
def _internal_board_simulator() -> None:
    import streamlit.components.v1 as components

    st.markdown("#### Board simulator")

    _P(
        "Choose an example, then press the button to watch the full solution appear on the same board."
    )

    example = st.radio(
        "Choose an example",
        ["Example A (concavity + inflection)", "Example B (second derivative test)"],
        horizontal=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        play = st.button("Play solution", use_container_width=True)
    with col2:
        reset = st.button("Reset", use_container_width=True)

    # Example content (ALL math is LaTeX strings)
    if example.startswith("Example A"):
        lines = [
            r"\textbf{Example A: Concavity and inflection points}",
            r"\text{Given } f(x)=2x^3+9x^2-24x-10.",
            r"\text{Goal: Find concavity intervals and any inflection point(s).}",
            r"f'(x)=6x^2+18x-24=6(x^2+3x-4)=6(x+4)(x-1).",
            r"f''(x)=12x+18=6(2x+3).",
            r"f''(x)=0 \Rightarrow 12x+18=0 \Rightarrow x=-\frac{3}{2}.",
            r"\text{Test an }x\text{ in }(-\infty,-\frac{3}{2})\text{ e.g. }x=-2:",
            r"f''(-2)=12(-2)+18=-6<0 \Rightarrow \text{concave down on }(-\infty,-\frac{3}{2}).",
            r"\text{Test an }x\text{ in }(-\frac{3}{2},\infty)\text{ e.g. }x=0:",
            r"f''(0)=18>0 \Rightarrow \text{concave up on }(-\frac{3}{2},\infty).",
            r"\text{Concavity changes at }x=-\frac{3}{2}\Rightarrow \text{inflection point at }x=-\frac{3}{2}.",
            r"\text{Compute the }y\text{-value: } f\!\left(-\frac{3}{2}\right)=2\left(-\frac{3}{2}\right)^3+9\left(-\frac{3}{2}\right)^2-24\left(-\frac{3}{2}\right)-10.",
            r"f\!\left(-\frac{3}{2}\right)=-\frac{27}{4}+\frac{81}{4}+36-10=\frac{54}{4}+26=\frac{27}{2}+26=\frac{79}{2}.",
            r"\textbf{Answer: } \text{concave down on }(-\infty,-\frac{3}{2}),\ \text{concave up on }(-\frac{3}{2},\infty),\ \text{inflection at }\left(-\frac{3}{2},\frac{79}{2}\right).",
        ]
    else:
        lines = [
            r"\textbf{Example B: Second Derivative Test}",
            r"\text{Given } f(x)=x^3-3x.",
            r"\text{Goal: Classify stationary points using the second derivative test.}",
            r"f'(x)=3x^2-3=3(x^2-1)=3(x-1)(x+1).",
            r"f'(x)=0 \Rightarrow x=-1,\ 1.",
            r"f''(x)=6x.",
            r"\text{At }x=-1:\ f''(-1)=-6<0 \Rightarrow \text{local maximum at }x=-1.",
            r"\text{At }x=1:\ f''(1)=6>0 \Rightarrow \text{local minimum at }x=1.",
            r"\text{Compute the }y\text{-values: } f(-1)=2,\ f(1)=-2.",
            r"\textbf{Answer: } \text{local max at }(-1,2)\ \text{and local min at }(1,-2).",
            r"\textbf{If }f''(c)=0\text{ (or undefined), the test is inconclusive and you must use another method.}",
        ]

    # HTML board (KaTeX rendering inside)
    # No sliders, no next-step buttons: auto-writes the FULL solution once "Play solution" is pressed.
    # Reset clears the board.
    payload = {
        "play": bool(play),
        "reset": bool(reset),
        "lines": lines,
    }

    html = r"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"></script>
  <style>
    body { margin:0; padding:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; }
    .wrap { border:1px solid #1f2937; border-radius:14px; overflow:hidden; }
    .hdr { background:#0b1220; color:#e5e7eb; padding:10px 12px; font-weight:700; }
    .board { background:#05070c; color:#e5e7eb; min-height:420px; padding:14px 16px; }
    .line { margin: 10px 0; font-size: 18px; }
    .muted { color:#94a3b8; font-weight:600; font-size: 13px; margin-top:10px;}
  </style>
</head>
<body>
<div class="wrap">
  <div class="hdr">Blackboard</div>
  <div class="board" id="board">
    <div class="muted">Press “Play solution” to watch the full solution appear here.</div>
  </div>
</div>

<script>
  const payload = __PAYLOAD__;
  const board = document.getElementById("board");

  function clearBoard(){
    board.innerHTML = '<div class="muted">Press “Play solution” to watch the full solution appear here.</div>';
  }

  function addLine(latex){
    const div = document.createElement("div");
    div.className = "line";
    try{
      katex.render(latex, div, {throwOnError:false, displayMode:true});
    } catch(e){
      div.textContent = latex;
    }
    board.appendChild(div);
  }

  function writeAll(lines){
    board.innerHTML = "";
    let i = 0;
    const timer = setInterval(() => {
      if (i >= lines.length){
        clearInterval(timer);
        return;
      }
      addLine(lines[i]);
      i++;
      // keep last lines visible
      board.scrollTop = board.scrollHeight;
    }, 650);
  }

  if(payload.reset){
    clearBoard();
  } else if(payload.play){
    writeAll(payload.lines || []);
  }
</script>
</body>
</html>
"""
    html = html.replace("__PAYLOAD__", str(payload).replace("'", '"'))
    components.html(html, height=470, scrolling=True)


# -----------------------------
# Learn tab content
# -----------------------------
def _render_learn() -> None:
    _H("Learning Objectives")
    _card(
        "By the end of this subtopic, you should be able to:",
        """
<ul style="margin:0; padding-left:18px;">
  <li>Find intervals where a graph is concave up or concave down and identify any inflection point(s).</li>
  <li>Build a combined table (variation + concavity) that summarizes behavior using derivatives.</li>
  <li>Use the second derivative test to classify stationary points, and recognise when it is inconclusive.</li>
  <li>Estimate increasing/decreasing, extrema, concavity, and inflection points from a graph.</li>
  <li>Apply concavity and the second derivative ideas to economic-style functions (sales, cost, efficiency, etc.).</li>
</ul>
""",
    )

    _rule()

    # 5.5.1 Concavity + inflection points
    _H("Concavity and inflection points")

    _card(
        "Key idea",
        """
Concavity describes how the slope changes:
<ul style="margin:0; padding-left:18px;">
  <li>Concave up: slopes increase as you move left to right.</li>
  <li>Concave down: slopes decrease as you move left to right.</li>
</ul>
""",
    )

    _L(r"f''(x)>0 \Rightarrow \text{concave up}")
    _L(r"f''(x)<0 \Rightarrow \text{concave down}")

    _card(
        "Inflection point",
        """
An inflection point is where concavity changes.
You must confirm a sign change of the second derivative (or a change in concavity from the graph).
""",
    )
    _L(r"\text{Inflection at }x=c \text{ if concavity changes at }c.")

    _rule()

    _H("Worked example 1")
    _card(
        "Question",
        """
Find where the function is concave up and concave down, and identify any inflection point(s).
""",
    )
    _L(r"f(x)=2x^3+9x^2-24x-10")

    _card(
        "What you must do",
        """
<ol style="margin:0; padding-left:18px;">
  <li>Find <span style="font-weight:700;">the second derivative</span>.</li>
  <li>Solve <span style="font-weight:700;">\(f''(x)=0\)</span> (and include where \(f''(x)\) is undefined if it happens).</li>
  <li>Use a sign test to confirm concavity on each interval.</li>
  <li>State concavity intervals clearly and give the inflection point if concavity changes.</li>
</ol>
""",
    )

    _L(r"f'(x)=6x^2+18x-24=6(x+4)(x-1)")
    _L(r"f''(x)=12x+18=6(2x+3)")
    _L(r"f''(x)=0 \Rightarrow 12x+18=0 \Rightarrow x=-\frac{3}{2}")

    _card(
        "Sign test (concavity)",
        "Choose a test value in each interval and evaluate the sign of the second derivative.",
    )
    _L(r"\text{For }x=-2:\ f''(-2)=-6<0 \Rightarrow \text{concave down on }(-\infty,-\frac{3}{2}).")
    _L(r"\text{For }x=0:\ f''(0)=18>0 \Rightarrow \text{concave up on }(-\frac{3}{2},\infty).")
    _L(r"\text{Concavity changes at }x=-\frac{3}{2}\Rightarrow \text{inflection at }x=-\frac{3}{2}.")
    _L(
        r"f\!\left(-\frac{3}{2}\right)=-\frac{27}{4}+\frac{81}{4}+36-10=\frac{79}{2}"
    )
    _L(
        r"\textbf{Answer: concave down }(-\infty,-\frac{3}{2}),\ \textbf{concave up }(-\frac{3}{2},\infty),\ \textbf{inflection } \left(-\frac{3}{2},\frac{79}{2}\right)."
    )

    _rule()

    # Graph (smaller)
    _H("Graph (for shape understanding)")
    _P("This graph is a visual support to connect concavity and turning behavior.")
    try:
        import numpy as np
        import matplotlib.pyplot as plt

        xs = np.linspace(-4, 4, 500)
        ys = 2 * xs**3 + 9 * xs**2 - 24 * xs - 10

        fig = plt.figure(figsize=(6.0, 3.2))
        ax = fig.add_subplot(111)
        ax.plot(xs, ys)
        ax.axhline(0)
        ax.axvline(0)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        st.pyplot(fig, use_container_width=False)
    except Exception:
        _card("Graph note", "The graph could not be rendered in this environment.")

    _rule()

    # 5.5.2 Tables of concavity + variation (NO overlap)
    _H("Combined table (variation + concavity)")

    _card(
        "What the combined table must include",
        """
<ul style="margin:0; padding-left:18px;">
  <li>Critical numbers from <span style="font-weight:700;">\(f'(x)=0\)</span> and where <span style="font-weight:700;">\(f'(x)\)</span> is undefined (if any).</li>
  <li>Candidate inflection values from <span style="font-weight:700;">\(f''(x)=0\)</span> and where <span style="font-weight:700;">\(f''(x)\)</span> is undefined (if any).</li>
  <li>Intervals split by all those values.</li>
  <li>Sign of <span style="font-weight:700;">\(f'(x)\)</span>, then increasing/decreasing.</li>
  <li>Sign of <span style="font-weight:700;">\(f''(x)\)</span>, then concave up/down.</li>
</ul>
""",
    )

    _card(
        "Template (readable)",
        "Use a table like the one below and fill it using sign tests.",
    )
    # Use LaTeX array so it is readable and NOT overlapping (and fully KaTeX)
    _L(
        r"""
\begin{array}{c|c|c|c|c}
\text{Interval} & \text{sign of } f'(x) & \text{Behavior} & \text{sign of } f''(x) & \text{Concavity}\\
\hline
(-\infty,a) & +\ \text{or}\ - & \text{increasing/decreasing} & +\ \text{or}\ - & \text{up/down}\\
(a,b) & +\ \text{or}\ - & \text{increasing/decreasing} & +\ \text{or}\ - & \text{up/down}\\
(b,\infty) & +\ \text{or}\ - & \text{increasing/decreasing} & +\ \text{or}\ - & \text{up/down}
\end{array}
"""
    )

    _rule()

    _H("Worked example 2 (combined table)")
    _card(
        "Question",
        """
Build one combined table summarising increasing/decreasing and concavity.
Identify any local extrema and inflection point(s).
""",
    )
    _L(r"f(x)=x^4-8x^2+10")

    _card(
        "Step-by-step solution",
        """
Follow the steps in order:
<ol style="margin:0; padding-left:18px;">
  <li
