import streamlit as st


def render():
    st.header("Subtopic 5.5: Concavity and 2nd Derivative Test")
    st.caption("Status: Added to navigation. Content will be developed next.")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.info(
            "**Coming next:** Full Learn tab with concavity intervals, inflection points, and the second derivative test.\n\n"
            "All mathematics will be rendered in **humanised LaTeX/KaTeX**."
        )
        st.latex(r"f''(x)>0\Rightarrow \text{concave up}\qquad f''(x)<0\Rightarrow \text{concave down}")
        st.latex(r"f'(c)=0,\ f''(c)>0\Rightarrow \text{local min}\qquad f'(c)=0,\ f''(c)<0\Rightarrow \text{local max}")

    with tabs[1]:
        st.warning("Practice will be added with 15+ questions (Hint + Show Answer) once this subtopic content is developed.")

