import streamlit as st


def render():
    st.header("Subtopic 5.2: Indeterminate Forms and Hospital’s Rule")
    st.caption("Status: Added to navigation. Content will be developed next.")

    tabs = st.tabs(["Learn", "Practice"])

    with tabs[0]:
        st.info(
            "**Coming next:** Full Learn tab with limit forms, step-by-step L’Hospital applications, and graphs.\n\n"
            "All mathematics will be rendered in **humanised LaTeX/KaTeX**."
        )
        st.latex(r"\text{Indeterminate forms: } \frac{0}{0},\ \frac{\infty}{\infty},\ 0\cdot\infty,\ \infty-\infty,\ 0^0,\ 1^\infty,\ \infty^0")
        st.latex(r"\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)}\quad\text{(when applicable)}")

    with tabs[1]:
        st.warning("Practice will be added with 15+ questions (Hint + Show Answer) once this subtopic content is developed.")

