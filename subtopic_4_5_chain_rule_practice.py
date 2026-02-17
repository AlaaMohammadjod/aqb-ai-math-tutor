from __future__ import annotations

import streamlit as st


def _qa(
    *,
    qnum: int,
    problem_md: str,
    expr_latex: str,
    expected_md: str,
    hint_md: str,
    answer_steps_latex: list[str],
    explain_md: str,
    qid: str,
):
    st.markdown("---")
    st.markdown(f"### Question {qnum}")
    st.markdown(f"**Problem:** {problem_md}")
    st.markdown(f"**What you should produce:** {expected_md}")
    st.latex(expr_latex)

    c1, c2 = st.columns([1, 1])
    with c1:
        show_hint = st.button("Hint", key=f"hint_{qid}")
    with c2:
        show_ans = st.button("Show Answer", key=f"ans_{qid}")

    if show_hint:
        st.info(hint_md)

    if show_ans:
        st.markdown("#### Full worked answer (step-by-step)")
        for line in answer_steps_latex:
            st.latex(line)
        st.success(explain_md)


def render_practice():
    st.markdown("## Practice (15 questions)")
    st.caption("Each question includes a hint and a full worked solution.")

    # 1
    _qa(
        qnum=1,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=(x^3-1)^2",
        hint_md="Outside is a square. Differentiate the inside $(x^3-1)$, then multiply.",
        answer_steps_latex=[
            r"u=x^3-1",
            r"f(x)=u^2 \Rightarrow f'(x)=2u\cdot u'",
            r"u'=3x^2",
            r"\boxed{f'(x)=2(x^3-1)\cdot 3x^2=6x^2(x^3-1)}",
        ],
        explain_md="Chain rule: outside derivative × inside derivative.",
        qid="q1",
    )

    # 2
    _qa(
        qnum=2,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=(x^2+2x+1)^2",
        hint_md="Outside is a square; inside derivative is $2x+2$.",
        answer_steps_latex=[
            r"u=x^2+2x+1",
            r"f(x)=u^2 \Rightarrow f'(x)=2u\cdot u'",
            r"u'=2x+2",
            r"\boxed{f'(x)=2(x^2+2x+1)(2x+2)}",
        ],
        explain_md="Differentiate the outside power, then multiply by the inside derivative.",
        qid="q2",
    )

    # 3
    _qa(
        qnum=3,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=(x^2+1)^3",
        hint_md="Outside derivative is $3(x^2+1)^2$; multiply by $2x$.",
        answer_steps_latex=[
            r"u=x^2+1",
            r"f(x)=u^3 \Rightarrow f'(x)=3u^2\cdot u'",
            r"u'=2x",
            r"\boxed{f'(x)=3(x^2+1)^2\cdot 2x=6x(x^2+1)^2}",
        ],
        explain_md="Power rule shortcut: $(u^n)'=nu^{n-1}u'$.",
        qid="q3",
    )

    # 4
    _qa(
        qnum=4,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=(2x+1)^4",
        hint_md="Inside derivative is $2$.",
        answer_steps_latex=[
            r"u=2x+1",
            r"f(x)=u^4 \Rightarrow f'(x)=4u^3\cdot u'",
            r"u'=2",
            r"\boxed{f'(x)=4(2x+1)^3\cdot 2=8(2x+1)^3}",
        ],
        explain_md="The chain rule brings the factor $2$ from the inside.",
        qid="q4",
    )

    # 5
    _qa(
        qnum=5,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=(x^3-x)^3",
        hint_md="Outside is a cube; inside derivative is $3x^2-1$.",
        answer_steps_latex=[
            r"u=x^3-x",
            r"f(x)=u^3 \Rightarrow f'(x)=3u^2\cdot u'",
            r"u'=3x^2-1",
            r"\boxed{f'(x)=3(x^3-x)^2(3x^2-1)}",
        ],
        explain_md="Outside power first, then multiply by the inside derivative.",
        qid="q5",
    )

    # 6
    _qa(
        qnum=6,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=\sqrt{x^2+4}",
        hint_md="Rewrite as $(x^2+4)^{1/2}$ and use the power rule shortcut.",
        answer_steps_latex=[
            r"f(x)=(x^2+4)^{1/2}",
            r"f'(x)=\frac{1}{2}(x^2+4)^{-1/2}\cdot (2x)",
            r"\boxed{f'(x)=\frac{x}{\sqrt{x^2+4}}}",
        ],
        explain_md="Square root is a power; don’t forget the inside derivative $2x$.",
        qid="q6",
    )

    # 7
    _qa(
        qnum=7,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=(x^3+x-1)^4",
        hint_md="Outside: power $4$. Inside derivative: $3x^2+1$.",
        answer_steps_latex=[
            r"u=x^3+x-1",
            r"f'(x)=4u^3\cdot u'",
            r"u'=3x^2+1",
            r"\boxed{f'(x)=4(x^3+x-1)^3(3x^2+1)}",
        ],
        explain_md="Power rule shortcut + inside derivative.",
        qid="q7",
    )

    # 8
    _qa(
        qnum=8,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(x)$.",
        expr_latex=r"f(x)=\sqrt{4x-\frac{1}{x}}",
        hint_md="Rewrite as $(4x-x^{-1})^{1/2}$ and differentiate the inside carefully.",
        answer_steps_latex=[
            r"f(x)=(4x-x^{-1})^{1/2}",
            r"f'(x)=\frac{1}{2}(4x-x^{-1})^{-1/2}\cdot(4+x^{-2})",
            r"\boxed{f'(x)=\frac{4+\frac{1}{x^2}}{2\sqrt{4x-\frac{1}{x}}}}",
        ],
        explain_md="Inside derivative: $\\frac{d}{dx}(4x)=4$ and $\\frac{d}{dx}(-x^{-1})=+x^{-2}$.",
        qid="q8",
    )

    # 9
    _qa(
        qnum=9,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(t)$.",
        expr_latex=r"f(t)=t^5\sqrt{t^3+2}",
        hint_md="Use product rule, then chain rule inside the square root.",
        answer_steps_latex=[
            r"f(t)=t^5(t^3+2)^{1/2}",
            r"f'(t)=5t^4(t^3+2)^{1/2}+t^5\cdot \frac{1}{2}(t^3+2)^{-1/2}\cdot(3t^2)",
            r"\boxed{f'(t)=5t^4\sqrt{t^3+2}+\frac{3t^7}{2\sqrt{t^3+2}}}",
        ],
        explain_md="Product rule creates two terms; the root term needs chain rule.",
        qid="q9",
    )

    # 10
    _qa(
        qnum=10,
        problem_md="Differentiate the function.",
        expected_md="Find $f'(t)$.",
        expr_latex=r"f(t)=(t^3+2)\sqrt{t}",
        hint_md="Product rule. Remember $\\sqrt{t}=t^{1/2}$.",
        answer_steps_latex=[
            r"f(t)=(t^3+2)t^{1/2}",
            r"f'(t)= (3t^2)t^{1/2} + (t^3+2)\cdot \frac{1}{2}t^{-1/2}",
            r"\boxed{f'(t)=3t^{5/2}+\frac{t^3+2}{2\sqrt{t}}}",
        ],
        explain_md="Two factors: derivative of each, then add.",
        qid="q10",
    )

    # 11 (π-based)
    _qa(
        qnum=11,
        problem_md="Differentiate the function and then evaluate the derivative at $x=\\frac{\\pi}{6}$.",
        expected_md="Find $y'$ and the exact value of $y'\\!\\left(\\frac{\\pi}{6}\\right)$.",
        expr_latex=r"y=\sin(3x)",
        hint_md="Chain rule: derivative of $\\sin(u)$ is $\\cos(u)$, then multiply by $u'$.",
        answer_steps_latex=[
            r"u=3x",
            r"y=\sin(u)\Rightarrow y'=\cos(u)\cdot u'",
            r"u'=3",
            r"\boxed{y'=3\cos(3x)}",
            r"y'\\!\\left(\\frac{\\pi}{6}\\right)=3\cos\\left(\\frac{\\pi}{2}\\right)=0",
            r"\boxed{y'\\!\\left(\\frac{\\pi}{6}\\right)=0}",
        ],
        explain_md="Using π-angles keeps trig values exact.",
        qid="q11",
    )

    # 12
    _qa(
        qnum=12,
        problem_md="Differentiate the function and evaluate at $x=\\frac{\\pi}{4}$.",
        expected_md="Find $y'$ and the exact value of $y'\\!\\left(\\frac{\\pi}{4}\\right)$.",
        expr_latex=r"y=\cos(2x)",
        hint_md="Derivative of $\\cos(u)$ is $-\\sin(u)$, then multiply by $u'$.",
        answer_steps_latex=[
            r"u=2x",
            r"y=\cos(u)\Rightarrow y'=-\sin(u)\cdot u'",
            r"u'=2",
            r"\boxed{y'=-2\sin(2x)}",
            r"y'\\!\\left(\\frac{\\pi}{4}\\right)=-2\sin\\left(\\frac{\\pi}{2}\\right)=-2",
            r"\boxed{y'\\!\\left(\\frac{\\pi}{4}\\right)=-2}",
        ],
        explain_md="At $x=\\pi/4$, the inside becomes $\\pi/2$.",
        qid="q12",
    )

    # 13 (existence check)
    _qa(
        qnum=13,
        problem_md="Differentiate the function and evaluate at $x=\\frac{\\pi}{10}$.",
        expected_md="Find $y'$ and decide whether $y'\\!\\left(\\frac{\\pi}{10}\\right)$ exists.",
        expr_latex=r"y=\tan(5x)",
        hint_md="Derivative of $\\tan(u)$ is $\\sec^2(u)$, then multiply by $u'$.",
        answer_steps_latex=[
            r"u=5x",
            r"y=\tan(u)\Rightarrow y'=\sec^2(u)\cdot u'",
            r"u'=5",
            r"\boxed{y'=5\sec^2(5x)}",
            r"y'\\!\\left(\\frac{\\pi}{10}\\right)=5\sec^2\\left(\\frac{\\pi}{2}\\right)",
            r"\text{But }\sec\left(\frac{\pi}{2}\right)\text{ is undefined.}",
            r"\boxed{\text{So }y'\\!\\left(\\frac{\\pi}{10}\\right)\text{ does not exist.}}",
        ],
        explain_md="Domain check: if $\\cos(u)=0$, then $\\sec^2(u)$ is undefined.",
        qid="q13",
    )

    # 14
    _qa(
        qnum=14,
        problem_md="Differentiate the function and evaluate at $x=\\frac{\\pi}{6}$.",
        expected_md="Find $y'$ and the exact value of $y'\\!\\left(\\frac{\\pi}{6}\\right)$.",
        expr_latex=r"y=(\sin(2x))^4",
        hint_md="Power rule + chain rule (and trig has its own inside $2x$).",
        answer_steps_latex=[
            r"y=(\sin(2x))^4",
            r"y'=4(\sin(2x))^3\cdot \frac{d}{dx}(\sin(2x))",
            r"\frac{d}{dx}(\sin(2x))=\cos(2x)\cdot 2",
            r"\boxed{y'=8(\sin(2x))^3\cos(2x)}",
            r"y'\\!\\left(\\frac{\\pi}{6}\\right)=8\left(\sin\left(\frac{\pi}{3}\right)\right)^3\cos\left(\frac{\pi}{3}\right)",
            r"=8\left(\frac{\sqrt{3}}{2}\right)^3\cdot\frac{1}{2}",
            r"\boxed{y'\\!\\left(\\frac{\\pi}{6}\\right)=\frac{3\sqrt{3}}{2}}",
        ],
        explain_md="Double chain rule: power rule, then trig chain rule.",
        qid="q14",
    )

    # 15
    _qa(
        qnum=15,
        problem_md="Differentiate the function and evaluate at $x=\\frac{\\pi}{3}$.",
        expected_md="Find $y'$ and the exact value of $y'\\!\\left(\\frac{\\pi}{3}\\right)$.",
        expr_latex=r"y=e^{\cos x}",
        hint_md="Derivative of $e^{u}$ is $e^{u}u'$. Here $u=\\cos x$.",
        answer_steps_latex=[
            r"u=\cos x",
            r"y=e^{u}\Rightarrow y'=e^{u}\cdot u'",
            r"u'=-\sin x",
            r"\boxed{y'=-e^{\cos x}\sin x}",
            r"y'\\!\\left(\\frac{\\pi}{3}\\right)=-e^{\cos(\pi/3)}\sin(\pi/3)",
            r"=-e^{1/2}\cdot\frac{\sqrt{3}}{2}",
            r"\boxed{y'\\!\\left(\\frac{\\pi}{3}\\right)=-\frac{\sqrt{3}}{2}e^{1/2}}",
        ],
        explain_md="Leave answers exact (in terms of $\\pi$ and exact trig values).",
        qid="q15",
    )

    st.markdown("---")
    st.success("✅ Practice complete.")
