import streamlit as st


def render():
    st.header("Subtopic 5.3: Maximum and Minimum Values")
    st.caption("Status: Added to navigation. Content will be developed next.")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.info(
            "**Coming next:** Full Learn tab covering critical points, closed intervals, and optimisation exam questions.\n\n"
            "All mathematics will be rendered in **humanised LaTeX/KaTeX**."
        )
        st.latex(r"\text{Critical points occur where } f'(x)=0 \text{ or } f'(x)\text{ is undefined.}")

    with tabs[1]:
        st.warning("Practice will be added with 15+ questions (Hint + Show Answer) once this subtopic content is developed.")

