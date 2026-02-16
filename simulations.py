# simulations.py
from __future__ import annotations

from dataclasses import dataclass
import json
import hashlib
import streamlit as st
import streamlit.components.v1 as components


@dataclass
class BoardStep:
    latex_line: str
    teacher_explain_md: str  # Markdown text that may include \(..\), $$..$$, etc.


def _stable_id(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:10]


def render_simulation(steps: list[BoardStep], title: str):
    """
    Renders a blackboard simulation with a virtual pen and a teacher explanation panel.

    IMPORTANT:
    - Blackboard draws in humanized KaTeX immediately (no raw LaTeX flashes).
    - Teacher explanation renders math with KaTeX as well (no backslashes shown).
    - No components.html(key=...) (prevents crash).
    """
    if not steps:
        st.info("No simulation steps provided yet.")
        return

    sim_id = _stable_id(title)
    run_key = f"sim_run_token_{sim_id}"
    reset_key = f"sim_reset_token_{sim_id}"

    if run_key not in st.session_state:
        st.session_state[run_key] = 0
    if reset_key not in st.session_state:
        st.session_state[reset_key] = 0

    st.subheader(title)

    # Controls row (keep consistent with your existing UI)
    c1, c2, c3 = st.columns([5, 1.2, 1.2])
    with c1:
        speed_label = st.selectbox(
            "Speed",
            ["0.5x", "1x", "1.5x", "2x"],
            index=1,
            key=f"sim_speed_{sim_id}",
        )
    with c2:
        if st.button("Start solving", key=f"sim_start_{sim_id}"):
            st.session_state[run_key] += 1
    with c3:
        if st.button("Reset board", key=f"sim_reset_{sim_id}"):
            st.session_state[reset_key] += 1

    speed_map = {"0.5x": 0.5, "1x": 1.0, "1.5x": 1.5, "2x": 2.0}
    speed = float(speed_map.get(speed_label, 1.0))

    payload = {
        "title": title,
        "steps": [{"latex": s.latex_line, "explain": s.teacher_explain_md} for s in steps],
        "speed": speed,
        "runToken": st.session_state[run_key],
        "resetToken": st.session_state[reset_key],
    }

    html = _SIM_HTML.replace("__PAYLOAD_JSON__", json.dumps(payload))

    # Important: no key=... argument here (fixes your crash)
    components.html(html, height=640, scrolling=False)


def _SIM_HTML() -> str:
    return ""


# HTML template (kept in a single constant for reliability)
_SIM_HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- KaTeX -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

  <style>
    :root{
      --card-border: rgba(40, 83, 160, 0.18);
      --card-bg: #f7fbff;
      --card-shadow: 0 10px 30px rgba(0,0,0,.08);
    }
    body{
      margin:0;
      padding:0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: transparent;
      overflow: hidden;
    }

    .wrap{
      display:flex;
      gap:18px;
      align-items:stretch;
    }

    /* Blackboard */
    .boardWrap{
      flex: 1 1 58%;
      border-radius: 16px;
      background:#000;
      box-shadow: var(--card-shadow);
      position:relative;
      overflow:hidden;
      height: 560px;
    }
    .boardLabel{
      position:absolute;
      top:12px;
      right:14px;
      color:rgba(255,255,255,.65);
      font-weight:700;
      font-size:18px;
      letter-spacing:.3px;
      z-index:5;
    }
    .board{
      position:absolute;
      inset: 0;
      padding: 26px 26px 26px 26px;
      box-sizing:border-box;
      /* IMPORTANT: keep board stable; no iframe scroll jumps */
      overflow:hidden;
    }

    .line{
      position:relative;
      margin: 10px 0;
      color:#fff;
      font-weight:800;
      /* Keep this consistent with your "perfect board" look */
      font-size: 34px;
      line-height: 1.35;
      white-space: nowrap;
    }

    /* Reveal mask: we render full KaTeX immediately but reveal width grows */
    .reveal{
      display:inline-block;
      overflow:hidden;
      width:0px;
      vertical-align:top;
    }

    /* Pen */
    .pen{
      position:absolute;
      width: 20px;
      height: 60px;
      transform: rotate(-12deg);
      z-index: 10;
      pointer-events:none;
      opacity: 0;
      transition: opacity .15s ease;
    }

    /* Teacher panel */
    .teacher{
      flex: 1 1 42%;
      border-radius: 16px;
      background: #fff;
      box-shadow: var(--card-shadow);
      border: 1px solid var(--card-border);
      height: 560px;
      overflow:hidden;
      display:flex;
      flex-direction:column;
    }
    .teacherHeader{
      padding: 14px 16px;
      border-bottom: 1px solid rgba(40, 83, 160, 0.18);
      color: #1f4f9c;
      font-weight: 900;
      font-size: 22px;
    }
    .teacherBody{
      padding: 14px 14px 18px 14px;
      overflow:auto;
      background: #ffffff;
    }
    .stepCard{
      border: 2px solid rgba(40,83,160,.18);
      background: var(--card-bg);
      border-radius: 14px;
      padding: 14px 14px;
      margin-bottom: 12px;
    }
    .stepTitle{
      font-weight: 900;
      font-size: 18px;
      margin: 0 0 8px 0;
      color:#123a7a;
    }
    .md{
      color:#1b1f2a;
      font-size: 16px;
      line-height: 1.55;
    }
    .md p{ margin: 8px 0; }
    .md ul{ margin: 8px 0 8px 22px; }
    .md li{ margin: 6px 0; }
    .katex-display{ margin: 10px 0; }
    .katex { font-size: 1.05em; }

    /* Make sure teacher math never gets cut off */
    .teacherBody *{
      max-width: 100%;
      box-sizing: border-box;
      overflow-wrap: anywhere;
    }
  </style>
</head>

<body>
  <div class="wrap">
    <div class="boardWrap">
      <div class="boardLabel">Blackboard</div>
      <div id="board" class="board"></div>

      <!-- Pen SVG (looks like a pen, not a dot) -->
      <svg id="pen" class="pen" viewBox="0 0 64 160" aria-hidden="true">
        <defs>
          <linearGradient id="penBody" x1="0" x2="1">
            <stop offset="0" stop-color="#2aa7ff"/>
            <stop offset="1" stop-color="#0a63c7"/>
          </linearGradient>
        </defs>
        <!-- body -->
        <rect x="18" y="22" width="28" height="92" rx="10" fill="url(#penBody)" />
        <!-- grip -->
        <rect x="18" y="92" width="28" height="20" rx="10" fill="#0b3f86" opacity="0.55"/>
        <!-- tip -->
        <path d="M32 112 L44 132 L20 132 Z" fill="#e9eef6"/>
        <path d="M32 132 L36 150 L28 150 Z" fill="#ffffff"/>
        <!-- tiny nib -->
        <circle cx="32" cy="152" r="3" fill="#ffffff"/>
      </svg>
    </div>

    <div class="teacher">
      <div class="teacherHeader">Teacher explanation (adds under each step)</div>
      <div id="teacherBody" class="teacherBody"></div>
    </div>
  </div>

<script>
  const PAYLOAD = __PAYLOAD_JSON__;

  function escHtml(s){
    return String(s)
      .replaceAll('&','&amp;')
      .replaceAll('<','&lt;')
      .replaceAll('>','&gt;');
  }

  // Very small markdown -> HTML (keeps your existing teacher text style)
  // Then KaTeX renders math in that HTML.
  function mdToHtml(md){
    const raw = String(md || "");

    // Split into lines and build paragraphs/lists
    const lines = raw.replace(/\r\n/g, "\n").split("\n");
    let html = "";
    let inList = false;

    function closeList(){
      if(inList){ html += "</ul>"; inList = false; }
    }

    for(const line of lines){
      const t = line.trim();

      if(t === ""){
        closeList();
        continue;
      }

      // bullet list
      if(t.startsWith("- ") || t.startsWith("• ")){
        if(!inList){ html += "<ul>"; inList = true; }
        const item = t.replace(/^(- |• )/, "");
        html += "<li>" + inlineBold(escHtml(item)) + "</li>";
        continue;
      }

      closeList();

      // headings like "Start" or "Rewrite in base (e)" if provided as plain lines
      // We'll keep them as paragraphs but bold if written like **...**
      html += "<p>" + inlineBold(escHtml(line)) + "</p>";
    }
    closeList();

    return "<div class='md'>" + html + "</div>";
  }

  function inlineBold(s){
    // **bold**
    return s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  }

  function renderMathIn(elem){
    // Render \( \), \[ \], $$ $$, and $ $
    renderMathInElement(elem, {
      delimiters: [
        {left: "$$", right: "$$", display: true},
        {left: "\\[", right: "\\]", display: true},
        {left: "\\(", right: "\\)", display: false},
        {left: "$", right: "$", display: false}
      ],
      throwOnError: false
    });
  }

  function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

  const board = document.getElementById("board");
  const teacherBody = document.getElementById("teacherBody");
  const pen = document.getElementById("pen");

  function clearAll(){
    board.innerHTML = "";
    teacherBody.innerHTML = "";
    pen.style.opacity = 0;
  }

  // Reveal animation: full KaTeX rendered immediately, but clipped width grows
  async function writeLineKaTeX(latex, speed){
    const line = document.createElement("div");
    line.className = "line";

    const reveal = document.createElement("span");
    reveal.className = "reveal";

    const inner = document.createElement("span");
    reveal.appendChild(inner);
    line.appendChild(reveal);

    board.appendChild(line);

    // Render full KaTeX immediately (so students NEVER see raw LaTeX)
    try{
      katex.render(latex, inner, {throwOnError:false, displayMode:false});
    }catch(e){
      inner.textContent = latex; // fallback
    }

    // Measure full width after render
    await sleep(0);
    const fullW = inner.getBoundingClientRect().width;

    // Reveal animation duration proportional to latex length
    const base = Math.max(400, latex.length * 28); // ms
    const duration = base / speed;

    // Position pen at the left start of the line
    const lineRect = line.getBoundingClientRect();
    const boardRect = board.getBoundingClientRect();

    pen.style.opacity = 1;

    const startX = 0;
    const startY = (lineRect.top - boardRect.top) + 6;

    const t0 = performance.now();
    return new Promise(resolve => {
      function frame(t){
        const p = Math.min(1, (t - t0) / duration);
        const w = fullW * p;
        reveal.style.width = w + "px";

        // Pen follows reveal edge, aligned to text baseline
        const px = 26 + startX + w + 6; // 26 = board padding left
        const py = 26 + startY - 6;
        pen.style.left = px + "px";
        pen.style.top = py + "px";

        if(p < 1){
          requestAnimationFrame(frame);
        }else{
          resolve();
        }
      }
      requestAnimationFrame(frame);
    });
  }

  function addTeacherCard(stepIndex, md){
    const card = document.createElement("div");
    card.className = "stepCard";

    const title = document.createElement("div");
    title.className = "stepTitle";
    title.textContent = "Step " + (stepIndex+1) + ":";

    const body = document.createElement("div");
    body.innerHTML = mdToHtml(md);

    card.appendChild(title);
    card.appendChild(body);

    teacherBody.appendChild(card);

    // Render all math INSIDE teacher explanation as KaTeX (humanized)
    renderMathIn(card);

    // Keep teacher panel readable (no cut-off)
    teacherBody.scrollTop = teacherBody.scrollHeight;
  }

  async function run(){
    // If not started yet, do nothing
    if(!PAYLOAD.runToken || PAYLOAD.runToken === 0){
      return;
    }

    clearAll();

    const steps = PAYLOAD.steps || [];
    for(let i=0; i<steps.length; i++){
      const latex = String(steps[i].latex || "").trim();
      const explain = String(steps[i].explain || "").trim();

      if(latex){
        await writeLineKaTeX(latex, PAYLOAD.speed || 1.0);
        await sleep(120);
      }
      if(explain){
        addTeacherCard(i, explain);
      }
      await sleep(120);
    }

    // Hide pen after finishing
    pen.style.opacity = 0;
  }

  // Reset handling
  if(PAYLOAD.resetToken && PAYLOAD.resetToken > 0){
    clearAll();
  }

  // Wait until KaTeX is available, then run
  const waitKatex = setInterval(() => {
    if(window.katex && window.renderMathInElement){
      clearInterval(waitKatex);
      run();
    }
  }, 30);
</script>
</body>
</html>
"""
