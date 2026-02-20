# aqb-ai-math-tutor/subtopic_4_5_chain_rule_practice.py
import streamlit as st


def _q_block(num: int, prompt_md: str, expr_latex: str, hint_md: str, solution_steps_latex: list[str], *, key_prefix: str) -> None:
    st.markdown(f"### Q{num}")
    st.markdown("**Problem**")
    st.markdown(prompt_md)
    if expr_latex:
        st.latex(expr_latex)

    c1, c2 = st.columns([1, 1])
    with c1:
        with st.expander("Hint", expanded=False):
            st.markdown(hint_md)
    with c2:
        with st.expander("Solution", expanded=False):
            st.markdown("**Solution (step-by-step)**")
            for s in solution_steps_latex:
                st.latex(s)


def render():
    st.header("Practice")

    st.markdown(
        "Work through the questions below. Use the hint only if you get stuck, then open the solution to check your steps."
    )

    # 15 questions, mixed difficulty, all math rendered via st.latex
    questions = [
        dict(
            prompt="Differentiate the function.",
            expr=r"y=(5x-1)^6",
            hint="Label the inside as $u=5x-1$. Apply the power rule to $u^6$, then multiply by $u'(x)$.",
            sol=[
                r"u=5x-1",
                r"\frac{dy}{dx}=6u^5\cdot \frac{du}{dx}",
                r"\frac{du}{dx}=5",
                r"\frac{dy}{dx}=6(5x-1)^5\cdot 5=30(5x-1)^5",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=\sqrt{3x^2+1}=(3x^2+1)^{1/2}",
            hint="Rewrite the root as a power. Use $u=3x^2+1$.",
            sol=[
                r"u=3x^2+1",
                r"\frac{dy}{dx}=\frac{1}{2}u^{-1/2}\cdot u'",
                r"u'=6x",
                r"\frac{dy}{dx}=\frac{6x}{2\sqrt{3x^2+1}}=\frac{3x}{\sqrt{3x^2+1}}",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=(2x-3)^7",
            hint="Outside is $(\cdot)^7$, inside is $2x-3$.",
            sol=[
                r"u=2x-3",
                r"\frac{dy}{dx}=7u^6\cdot u'",
                r"u'=2",
                r"\frac{dy}{dx}=14(2x-3)^6",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=3(1-4x)^5",
            hint="Use the shortcut: $a\cdot (u)^n \mapsto a\cdot n\cdot u^{n-1}\cdot u'$.",
            sol=[
                r"u=1-4x,\quad u'=-4",
                r"\frac{dy}{dx}=3\cdot 5\cdot (1-4x)^4\cdot (-4)",
                r"\frac{dy}{dx}=-60(1-4x)^4",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=\sin(3x)",
            hint="Derivative of $\sin(u)$ is $\cos(u)\,u'$.",
            sol=[
                r"u=3x,\quad u'=3",
                r"\frac{dy}{dx}=\cos(3x)\cdot 3",
                r"\frac{dy}{dx}=3\cos(3x)",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=\cos(2x)",
            hint="Derivative of $\cos(u)$ is $-\sin(u)\,u'$.",
            sol=[
                r"u=2x,\quad u'=2",
                r"\frac{dy}{dx}=-\sin(2x)\cdot 2",
                r"\frac{dy}{dx}=-2\sin(2x)",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=e^{x^2+1}",
            hint="Derivative of $e^{u}$ is $e^{u}\,u'$.",
            sol=[
                r"u=x^2+1,\quad u'=2x",
                r"\frac{dy}{dx}=e^{x^2+1}\cdot 2x",
                r"\frac{dy}{dx}=2x\,e^{x^2+1}",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=\ln(2x^2+5)",
            hint="Derivative of $\ln(u)$ is $\frac{1}{u}\,u'$.",
            sol=[
                r"u=2x^2+5,\quad u'=4x",
                r"\frac{dy}{dx}=\frac{1}{2x^2+5}\cdot 4x",
                r"\frac{dy}{dx}=\frac{4x}{2x^2+5}",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=(x^2+1)^5",
            hint="Use chain rule, then simplify.",
            sol=[
                r"u=x^2+1,\quad u'=2x",
                r"\frac{dy}{dx}=5u^4\cdot u'",
                r"\frac{dy}{dx}=5(x^2+1)^4\cdot 2x",
                r"\frac{dy}{dx}=10x(x^2+1)^4",
            ],
        ),
        dict(
            prompt="Find the tangent line at the given point.",
            expr=r"y=\cos(2x)\quad\text{at}\quad x=\frac{\pi}{4}",
            hint="Compute $f(a)$ and $f'(a)$, then use $y=f(a)+f'(a)(x-a)$.",
            sol=[
                r"a=\frac{\pi}{4}",
                r"f(a)=\cos\!\left(2\cdot\frac{\pi}{4}\right)=\cos\!\left(\frac{\pi}{2}\right)=0",
                r"f'(x)=-2\sin(2x)",
                r"f'(a)=-2\sin\!\left(\frac{\pi}{2}\right)=-2",
                r"y=0+(-2)\left(x-\frac{\pi}{4}\right)=-2x+\frac{\pi}{2}",
            ],
        ),
        dict(
            prompt="Evaluate the derivative at the given point.",
            expr=r"y=\sin(3x)\quad\text{Find}\quad y'\!\left(\frac{\pi}{6}\right)",
            hint="Differentiate first, then substitute the value of $x$.",
            sol=[
                r"y'=3\cos(3x)",
                r"y'\!\left(\frac{\pi}{6}\right)=3\cos\!\left(3\cdot\frac{\pi}{6}\right)=3\cos\!\left(\frac{\pi}{2}\right)=0",
            ],
        ),
        dict(
            prompt="Find the second derivative.",
            expr=r"y=(x^2+1)^5",
            hint="First find $y'$, then apply product rule on $10x(x^2+1)^4$.",
            sol=[
                r"y'=10x(x^2+1)^4",
                r"y''=10(x^2+1)^4+10x\cdot 4(x^2+1)^3\cdot 2x",
                r"y''=10(x^2+1)^4+80x^2(x^2+1)^3",
                r"y''=10(x^2+1)^3(9x^2+1)",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=\bigl(\sin x\bigr)^4",
            hint="Treat it as $y=(u)^4$ where $u=\sin x$.",
            sol=[
                r"u=\sin x,\quad u'=\cos x",
                r"\frac{dy}{dx}=4u^3\cdot u'",
                r"\frac{dy}{dx}=4(\sin x)^3\cos x",
            ],
        ),
        dict(
            prompt="Differentiate the function.",
            expr=r"y=\sqrt{1+\cos x}=(1+\cos x)^{1/2}",
            hint="Use $u=1+\cos x$. Remember $(\cos x)'=-\sin x$.",
            sol=[
                r"u=1+\cos x,\quad u'=-\sin x",
                r"\frac{dy}{dx}=\frac{1}{2}u^{-1/2}\cdot u'",
                r"\frac{dy}{dx}=\frac{-\sin x}{2\sqrt{1+\cos x}}",
            ],
        ),
        dict(
            prompt="Compute the derivative of the inverse at the given value.",
            expr=r"f(x)=x^3+1\quad\text{Find}\quad \Bigl(f^{-1}\Bigr)'(2)",
            hint="First solve $x^3+1=2$ to get $f^{-1}(2)$, then use $(f^{-1})'(a)=\frac{1}{f'(f^{-1}(a))}$.",
            sol=[
                r"f^{-1}(2)=x\Longleftrightarrow x^3+1=2\Longleftrightarrow x^3=1\Longrightarrow x=1",
                r"f'(x)=3x^2",
                r"\Bigl(f^{-1}\Bigr)'(2)=\frac{1}{f'(1)}=\frac{1}{3}",
            ],
        ),
    ]

    for i, q in enumerate(questions, start=1):
        _q_block(
            i,
            q["prompt"],
            q["expr"],
            q["hint"],
            q["sol"],
            key_prefix=f"cr_pr_{i}",
        )