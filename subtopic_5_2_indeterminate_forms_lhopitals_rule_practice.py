# subtopic_5_2_indeterminate_forms_lhopitals_rule_practice.py

import streamlit as st


def _callout(kind: str, title: str, body_md: str) -> None:
    styles = {
        "check": {
            "border": "#16a34a",
            "bg": "#f0fdf4",
            "title": "#166534",
            "text": "#052e16",
        }
    }
    s = styles.get(kind, styles["check"])
    st.markdown(
        f"""
<div style="border:1px solid {s['border']}33;border-left:6px solid {s['border']};border-radius:12px;padding:12px 14px;background:{s['bg']};margin:10px 0;">
  <div style="font-weight:900;color:{s['title']};margin-bottom:6px;">{title}</div>
  <div style="color:{s['text']};line-height:1.6;">{body_md}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _q_block(num: int, problem_latex: str, hint_md: str, solution_steps_latex: list[str]) -> None:
    st.markdown(f"### Q{num}")
    st.markdown("**Problem**")
    st.latex(problem_latex)
    c1, c2 = st.columns([1, 1])
    with c1:
        with st.expander("Hint", expanded=False):
            st.markdown(hint_md)
    with c2:
        with st.expander("Show full solution", expanded=False):
            st.markdown("**Solution (all steps)**")
            for s in solution_steps_latex:
                st.latex(s)


def render():
    st.header("Practice")

    _callout(
        "check",
        "How to use this practice",
        "Attempt each question first. Use the hint only if needed. Then open the full solution to compare every step.",
    )

    qs: list[tuple[str, str, list[str]]] = []

    qs.append(
        (
            r"\lim_{x\to 1}\frac{x^{2}-1}{x-1}",
            "Factor the numerator and cancel.",
            [
                r"x^{2}-1=(x-1)(x+1)",
                r"\lim_{x\to 1}\frac{(x-1)(x+1)}{x-1}=\lim_{x\to 1}(x+1)=2",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 2}\frac{x^{2}-4}{x-2}",
            "Factor the numerator as a difference of squares.",
            [
                r"x^{2}-4=(x-2)(x+2)",
                r"\lim_{x\to 2}(x+2)=4",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 0}\frac{\sqrt{1+x}-1}{x}",
            "Multiply by the conjugate.",
            [
                r"\frac{\sqrt{1+x}-1}{x}\cdot\frac{\sqrt{1+x}+1}{\sqrt{1+x}+1}",
                r"=\frac{(1+x)-1}{x(\sqrt{1+x}+1)}=\frac{1}{\sqrt{1+x}+1}",
                r"\Rightarrow \frac{1}{2}",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 0}\frac{\sin x}{x}",
            "Use the basic trigonometric limit result.",
            [
                r"\lim_{x\to 0}\frac{\sin x}{x}=1",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 0}\frac{1-\cos x}{\sin x}",
            "Apply L’Hôpital’s Rule once.",
            [
                r"\frac{0}{0}",
                r"\lim_{x\to 0}\frac{1-\cos x}{\sin x}=\lim_{x\to 0}\frac{\sin x}{\cos x}=0",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}\frac{e^{x}}{x}",
            "Apply L’Hôpital’s Rule once.",
            [
                r"\frac{\infty}{\infty}",
                r"\lim_{x\to\infty}\frac{e^{x}}{x}=\lim_{x\to\infty}\frac{e^{x}}{1}=\infty",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}\frac{x^{2}}{e^{x}}",
            "Apply the rule twice.",
            [
                r"\frac{\infty}{\infty}",
                r"\lim_{x\to\infty}\frac{x^{2}}{e^{x}}=\lim_{x\to\infty}\frac{2x}{e^{x}}",
                r"\frac{\infty}{\infty}",
                r"=\lim_{x\to\infty}\frac{2}{e^{x}}=0",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 0^{+}}\frac{\ln x}{\csc x}",
            "Apply the rule once, then rewrite using identities.",
            [
                r"\frac{\infty}{\infty}",
                r"\lim_{x\to 0^{+}}\frac{\ln x}{\csc x}=\lim_{x\to 0^{+}}\frac{\frac{1}{x}}{-\csc x\cot x}",
                r"=\lim_{x\to 0^{+}}\left(-\frac{\sin x}{x\tan x}\right)=-(1)(1)=-1",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}\frac{1}{x\ln x}",
            "Rewrite into a quotient first.",
            [
                r"\lim_{x\to\infty}\frac{1}{x\ln x}=\lim_{x\to\infty}\frac{\ln x}{x}",
                r"\frac{\infty}{\infty}",
                r"=\lim_{x\to\infty}\frac{\frac{1}{x}}{1}=0",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}\left(\sqrt{x^{2}+x}-x\right)",
            "Multiply by the conjugate.",
            [
                r"\sqrt{x^{2}+x}-x=\frac{x}{\sqrt{x^{2}+x}+x}",
                r"=\frac{1}{\sqrt{1+\frac{1}{x}}+1}\Rightarrow \frac{1}{2}",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 0^{+}}(\sin x)^{x}",
            "Use the log transform.",
            [
                r"y=(\sin x)^{x}\Rightarrow \ln y=x\ln(\sin x)",
                r"\lim_{x\to 0^{+}}\ln y=\lim_{x\to 0^{+}}\frac{\ln(\sin x)}{\frac{1}{x}}",
                r"=\lim_{x\to 0^{+}}\frac{\cot x}{-x^{-2}}=\lim_{x\to 0^{+}}\bigl(-x^{2}\cot x\bigr)=0",
                r"\Rightarrow \lim_{x\to 0^{+}}y=e^{0}=1",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}(x+1)^{2/x}",
            "Use the log transform and apply the rule on the quotient.",
            [
                r"y=(x+1)^{2/x}\Rightarrow \ln y=\frac{2\ln(x+1)}{x}",
                r"\frac{\infty}{\infty}",
                r"\lim_{x\to\infty}\ln y=\lim_{x\to\infty}\frac{\frac{2}{x+1}}{1}=0",
                r"\Rightarrow \lim_{x\to\infty}y=e^{0}=1",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}\left(1+\frac{1}{x}\right)^{x}",
            "Use the log transform and L’Hôpital’s Rule.",
            [
                r"y=\left(1+\frac{1}{x}\right)^{x}\Rightarrow \ln y=x\ln\left(1+\frac{1}{x}\right)",
                r"\lim_{x\to\infty}\ln y=\lim_{x\to\infty}\frac{\ln\left(1+\frac{1}{x}\right)}{\frac{1}{x}}",
                r"\frac{0}{0}",
                r"=\lim_{x\to\infty}\frac{\frac{-1}{x^{2}+x}}{-x^{-2}}=\lim_{x\to\infty}\frac{x^{2}}{x^{2}+x}=1",
                r"\Rightarrow \lim_{x\to\infty}y=e^{1}=e",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to 0}\frac{e^{x}-1}{x}",
            "Apply L’Hôpital’s Rule once.",
            [
                r"\frac{0}{0}",
                r"\lim_{x\to 0}\frac{e^{x}-1}{x}=\lim_{x\to 0}\frac{e^{x}}{1}=1",
            ],
        )
    )

    qs.append(
        (
            r"\lim_{x\to\infty}\frac{\ln x}{x^{1/2}}",
            "Apply L’Hôpital’s Rule after identifying the form.",
            [
                r"\frac{\infty}{\infty}",
                r"\lim_{x\to\infty}\frac{\ln x}{x^{1/2}}=\lim_{x\to\infty}\frac{\frac{1}{x}}{\frac{1}{2}x^{-1/2}}",
                r"=\lim_{x\to\infty}2x^{-1/2}=0",
            ],
        )
    )

    for i, (prob, hint, sol) in enumerate(qs, start=1):
        _q_block(i, prob, hint, sol)