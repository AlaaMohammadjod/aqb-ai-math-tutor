import os
import base64
import streamlit as st
import streamlit.components.v1 as components


def _img_to_base64(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_banner():
    """
    FIX: render banner via components.html so NO HTML ever leaks as visible text.
    """
    logo_path = os.path.join("assets", "ats_logo.png")
    logo_b64 = _img_to_base64(logo_path)

    if logo_b64:
        logo_html = f"""
          <img src="data:image/png;base64,{logo_b64}"
               style="height:96px; width:auto; object-fit:contain;
                      filter: drop-shadow(0 4px 10px rgba(0,0,0,0.22));" />
        """
    else:
        logo_html = """
          <div style="
                padding:10px 12px;
                border-radius:12px;
                background: rgba(255,255,255,0.18);
                border: 1px solid rgba(255,255,255,0.22);
                color:#ffffff;
                font-size:12px;
                font-weight:700;">
            ATS logo missing: assets/ats_logo.png
          </div>
        """

    html_block = f"""
    <div style="padding-top: 10px;"></div>

    <div style="
        margin: 8px 0 14px 0;
        padding: 18px 18px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0b3d91 0%, #0a66c2 55%, #1b8cff 100%);
        box-shadow: 0 10px 24px rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.18);
        overflow: hidden;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    ">
      <div style="display:flex; gap:18px; align-items:center; justify-content:space-between;">
        <div style="flex: 1 1 auto; min-width: 0;">
          <div style="font-size: 30px; font-weight: 900; color: #ffffff; line-height: 1.12;">
            AQB Grade 12 AI Math Tutor
          </div>
          <div style="font-size: 15px; font-weight: 700; color: rgba(255,255,255,0.92); margin-top: 6px;">
            Applied Technology School – Al Ain (Al Aqabiya)
          </div>
          <div style="font-size: 13px; color: rgba(255,255,255,0.92); margin-top: 8px;">
            Term 2 • Support & inquiries: <span style="font-weight:900;">Alaa.Mohammad@actvet.gov.ae</span>
          </div>
        </div>

        <div style="flex: 0 0 240px; display:flex; justify-content:flex-end; align-items:center;">
          {logo_html}
        </div>
      </div>
    </div>
    """

    components.html(html_block, height=160, scrolling=False)
