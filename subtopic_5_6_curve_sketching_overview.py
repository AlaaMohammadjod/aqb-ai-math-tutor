import streamlit as st


def render():
    st.header("Subtopic 5.6: Overview of Curve Sketching")
    st.caption("Status: Added to navigation. Content will be developed next.")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.info(
            "**Coming next:** Full Learn tab with a curve sketching workflow, summary boards, and rich graphs.\n\n"
            "All mathematics will be rendered in **humanised LaTeX/KaTeX**."
        )
        st.latex(r"\text{Workflow: domain }\rightarrow \text{ intercepts }\rightarrow f'(x)\text{ sign chart }\rightarrow f''(x)\text{ concavity }\rightarrow \text{asymptotes }\rightarrow \text{final sketch}")

    with tabs[1]:
        st.warning("Practice will be added with 15+ questions (Hint + Show Answer) once this subtopic content is developed.")

