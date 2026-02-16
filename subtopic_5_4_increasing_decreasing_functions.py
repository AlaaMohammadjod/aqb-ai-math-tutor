import streamlit as st


def render():
    st.header("Subtopic 5.4: Increasing and Decreasing Functions")
    st.caption("Status: Added to navigation. Content will be developed next.")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.info(
            "**Coming next:** Full Learn tab with sign charts, intervals, and graph interpretation.\n\n"
            "All mathematics will be rendered in **humanised LaTeX/KaTeX**."
        )
        st.latex(r"f'(x)>0\Rightarrow f(x)\text{ increasing}\qquad f'(x)<0\Rightarrow f(x)\text{ decreasing}")

    with tabs[1]:
        st.warning("Practice will be added with 15+ questions (Hint + Show Answer) once this subtopic content is developed.")

