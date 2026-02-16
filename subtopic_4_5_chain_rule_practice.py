from __future__ import annotations

import streamlit as st


def _qa(question_latex: str, hint_md: str, answer_steps_latex: list[str], explain_md: str, qid: str):
    st.markdown("---")
    st.markdown("### Question")
    st.latex(question_latex)

    c1, c2 = st.columns([1, 1])
    with c1:
        show_hint = st.button("Hint", key=f"hint_{qid}")
    with c2:
        show_ans = st.button("Show Answer", key=f"ans_{qid}")

    if show_hint:
        st.info(hint_md)

    if show_ans:
        st.markdown("#### Step-by-step answer")
        for line in answer_steps_latex:
            st.latex(line)
        st.success(explain_md)


def render_practice():
    st.markdown("## Practice (15 questions)")
    st.caption("Hints and full worked answers are available. Questions are aligned to Section 2.5 Chain Rule exercises.")

    # Q1
    _qa(
        question_latex=r"f(x)=(x^3-1)^2",
        hint_md="Use the power rule on the outside, then multiply by the derivative of the inside.",
        answer_steps_latex=[
            r"u=x^3-1",
            r"f(x)=u^2 \Rightarrow f'(x)=2u\cdot u'",
            r"u'=3x^2",
            r"\boxed{f'(x)=2(x^3-1)\cdot 3x^2=6x^2(x^3-1)}",
        ],
        explain_md="Outside: square → multiply by inside derivative.",
        qid="q1",
    )

    # Q2
    _qa(
        question_latex=r"f(x)=(x^2+2x+1)^2",
        hint_md="It’s a square of a polynomial. Differentiate inside as usual.",
        answer_steps_latex=[
            r"u=x^2+2x+1",
            r"f(x)=u^2 \Rightarrow f'(x)=2u\cdot u'",
            r"u'=2x+2",
            r"\boxed{f'(x)=2(x^2+2x+1)(2x+2)}",
        ],
        explain_md="Chain rule: derivative of outside power × derivative of inside polynomial.",
        qid="q2",
    )

    # Q3
    _qa(
        question_latex=r"f(x)=(x^2+1)^3",
        hint_md="Power rule outside (3), then inside derivative (2x).",
        answer_steps_latex=[
            r"u=x^2+1",
            r"f(x)=u^3 \Rightarrow f'(x)=3u^2\cdot u'",
            r"u'=2x",
            r"\boxed{f'(x)=3(x^2+1)^2\cdot 2x=6x(x^2+1)^2}",
        ],
        explain_md="Outside: cube → multiply by inside derivative.",
        qid="q3",
    )

    # Q4
    _qa(
        question_latex=r"f(x)=(2x+1)^4",
        hint_md="Derivative of (2x+1) is 2.",
        answer_steps_latex=[
            r"u=2x+1",
            r"f(x)=u^4 \Rightarrow f'(x)=4u^3\cdot u'",
            r"u'=2",
            r"\boxed{f'(x)=4(2x+1)^3\cdot 2=8(2x+1)^3}",
        ],
        explain_md="The inside derivative contributes the factor 2.",
        qid="q4",
    )

    # Q5a
    _qa(
        question_latex=r"f(x)=(x^3-x)^3",
        hint_md="Outside is cube; inside derivative is (3x^2-1).",
        answer_steps_latex=[
            r"u=x^3-x",
            r"f(x)=u^3 \Rightarrow f'(x)=3u^2\cdot u'",
            r"u'=3x^2-1",
            r"\boxed{f'(x)=3(x^3-x)^2(3x^2-1)}",
        ],
        explain_md="Classic chain rule: power outside, polynomial inside.",
        qid="q5a",
    )

    # Q5b
    _qa(
        question_latex=r"f(x)=\sqrt{x^2+4}",
        hint_md="Rewrite as (x^2+4)^(1/2).",
        answer_steps_latex=[
            r"f(x)=(x^2+4)^{1/2}",
            r"f'(x)=\frac{1}{2}(x^2+4)^{-1/2}\cdot (2x)",
            r"\boxed{f'(x)=\frac{x}{\sqrt{x^2+4}}}",
        ],
        explain_md="Square root is a power of 1/2; don’t forget the inner derivative 2x.",
        qid="q5b",
    )

    # Q6a
    _qa(
        question_latex=r"f(x)=(x^3+x-1)^4",
        hint_md="Outside: power 4. Inside derivative: 3x^2+1.",
        answer_steps_latex=[
            r"u=x^3+x-1",
            r"f'(x)=4u^3\cdot u'",
            r"u'=3x^2+1",
            r"\boxed{f'(x)=4(x^3+x-1)^3(3x^2+1)}",
        ],
        explain_md="Power rule + inside derivative.",
        qid="q6a",
    )

    # Q6b (as shown in extracted text: sqrt(4x - 1/x))
    _qa(
        question_latex=r"f(x)=\sqrt{4x-\frac{1}{x}}",
        hint_md="Rewrite as (4x - 1/x)^(1/2). Differentiate inside carefully.",
        answer_steps_latex=[
            r"f(x)=(4x-x^{-1})^{1/2}",
            r"f'(x)=\frac{1}{2}(4x-x^{-1})^{-1/2}\cdot(4+x^{-2})",
            r"\boxed{f'(x)=\frac{4+\frac{1}{x^2}}{2\sqrt{4x-\frac{1}{x}}}}",
        ],
        explain_md="Inside derivative: d/dx(4x)=4 and d/dx(-x^{-1})=+x^{-2}.",
        qid="q6b",
    )

    # Q7a
    _qa(
        question_latex=r"f(t)=t^5\sqrt{t^3+2}",
        hint_md="Product rule first (two factors), then chain rule inside the square root.",
        answer_steps_latex=[
            r"f(t)=t^5(t^3+2)^{1/2}",
            r"f'(t)=5t^4(t^3+2)^{1/2}+t^5\cdot \frac{1}{2}(t^3+2)^{-1/2}\cdot(3t^2)",
            r"\boxed{f'(t)=5t^4\sqrt{t^3+2}+\frac{3t^7}{2\sqrt{t^3+2}}}",
        ],
        explain_md="This mixes product rule + chain rule (inside the root).",
        qid="q7a",
    )

    # Q7b
    _qa(
        question_latex=r"f(t)=(t^3+2)\sqrt{t}",
        hint_md="Product rule. √t is t^(1/2).",
        answer_steps_latex=[
            r"f(t)=(t^3+2)t^{1/2}",
            r"f'(t)= (3t^2)t^{1/2} + (t^3+2)\cdot \frac{1}{2}t^{-1/2}",
            r"\boxed{f'(t)=3t^{5/2}+\frac{t^3+2}{2\sqrt{t}}}",
        ],
        explain_md="Two factors: derivative of each, then add.",
        qid="q7b",
    )

    # Q8a
    _qa(
        question_latex=r"f(t)=(t^4+2)\sqrt{t^2+1}",
        hint_md="Product rule. Then chain rule inside √(t^2+1).",
        answer_steps_latex=[
            r"f(t)=(t^4+2)(t^2+1)^{1/2}",
            r"f'(t)=4t^3\sqrt{t^2+1}+(t^4+2)\cdot \frac{1}{2}(t^2+1)^{-1/2}\cdot(2t)",
            r"\boxed{f'(t)=4t^3\sqrt{t^2+1}+\frac{t(t^4+2)}{\sqrt{t^2+1}}}",
        ],
        explain_md="Product rule first; the root requires chain rule.",
        qid="q8a",
    )

    # Q8b (from text: sqrt(t)(t^(4/3)+3))
    _qa(
        question_latex=r"f(t)=\sqrt{t}\,(t^{4/3}+3)",
        hint_md="Product rule: t^(1/2) times (t^(4/3)+3).",
        answer_steps_latex=[
            r"f(t)=t^{1/2}(t^{4/3}+3)",
            r"f'(t)=\frac{1}{2}t^{-1/2}(t^{4/3}+3)+t^{1/2}\left(\frac{4}{3}t^{1/3}\right)",
            r"\boxed{f'(t)=\frac{t^{4/3}+3}{2\sqrt{t}}+\frac{4}{3}t^{5/6}}",
        ],
        explain_md="No chain rule inside here, but still careful with fractional powers.",
        qid="q8b",
    )

    # Q9a
    _qa(
        question_latex=r"f(u)=\frac{u^2+1}{u+4}",
        hint_md="Quotient rule first. (No deep chain rule, but still composite-looking.)",
        answer_steps_latex=[
            r"f(u)=\frac{u^2+1}{u+4}",
            r"f'(u)=\frac{(2u)(u+4)-(u^2+1)(1)}{(u+4)^2}",
            r"\boxed{f'(u)=\frac{2u(u+4)-(u^2+1)}{(u+4)^2}}",
        ],
        explain_md="This one is mainly quotient rule; simplify if needed.",
        qid="q9a",
    )

    # Q9b
    _qa(
        question_latex=r"f(u)=\frac{u^3}{(u^2+4)^2}",
        hint_md="Rewrite as u^3 (u^2+4)^(-2) then product rule (or quotient). Chain rule inside (u^2+4).",
        answer_steps_latex=[
            r"f(u)=u^3(u^2+4)^{-2}",
            r"f'(u)=3u^2(u^2+4)^{-2}+u^3\cdot(-2)(u^2+4)^{-3}\cdot(2u)",
            r"\boxed{f'(u)=3u^2(u^2+4)^{-2}-4u^4(u^2+4)^{-3}}",
        ],
        explain_md="Chain rule appears in the derivative of (u^2+4)^(-2).",
        qid="q9b",
    )

    # Q10a
    _qa(
        question_latex=r"f(v)=\frac{v^2-1}{v^2+1}",
        hint_md="Quotient rule; both numerator and denominator are polynomials.",
        answer_steps_latex=[
            r"f(v)=\frac{v^2-1}{v^2+1}",
            r"f'(v)=\frac{(2v)(v^2+1)-(v^2-1)(2v)}{(v^2+1)^2}",
            r"\boxed{f'(v)=\frac{2v(v^2+1)-2v(v^2-1)}{(v^2+1)^2}}",
            r"\boxed{f'(v)=\frac{4v}{(v^2+1)^2}",
        ],
        explain_md="The middle terms cancel nicely here.",
        qid="q10a",
    )

    st.markdown("---")
    st.success("✅ Practice complete. In the next messages, we can build Subtopics 4.6–4.9 fully.")

