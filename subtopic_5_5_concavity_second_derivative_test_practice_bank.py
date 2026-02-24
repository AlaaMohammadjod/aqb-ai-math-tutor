# subtopic_5_5_concavity_second_derivative_test_practice_bank.py
# Practice bank for Subtopic 5.5 (>= 20 questions)
# ALL math is LaTeX/KaTeX.

from __future__ import annotations

from typing import Dict, List


def _in(tex: str) -> str:
    return "\\(" + tex + "\\)"


PRACTICE_BANK: List[Dict] = [
    {
        "prompt_md": "For " + _in("f(x)=x^{3}-3x") + ", find where the graph is concave up / concave down, and identify any inflection point(s).",
        "solution_steps_md": [
            "Compute the second derivative:\n$$f'(x)=3x^{2}-3,\\quad f''(x)=6x$$",
            "Solve:\n$$f''(x)=0\\Rightarrow 6x=0\\Rightarrow x=0$$",
            "Sign test:\n"
            + "$$x<0\\Rightarrow f''(x)<0\\Rightarrow\\text{concave down on }(-\\infty,0)$$\n"
            + "$$x>0\\Rightarrow f''(x)>0\\Rightarrow\\text{concave up on }(0,\\infty)$$",
            "Concavity changes at " + _in("x=0") + ", so inflection point at:\n$$\\bigl(0,f(0)\\bigr)=(0,0)$$",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=2x^{3}+9x^{2}-24x-10") + ", find concavity intervals and the inflection point(s).",
        "solution_steps_md": [
            "$$f'(x)=6x^{2}+18x-24,\\quad f''(x)=12x+18$$",
            "$$f''(x)=0\\Rightarrow 12x+18=0\\Rightarrow x=-\\frac{3}{2}$$",
            "Test:\n"
            + "$$f''(-2)=-6<0\\Rightarrow\\text{concave down on }(-\\infty,-\\frac{3}{2})$$\n"
            + "$$f''(0)=18>0\\Rightarrow\\text{concave up on }(-\\frac{3}{2},\\infty)$$",
            "Concavity changes at " + _in("x=-\\frac{3}{2}") + ", so inflection point at:\n"
            + "$$\\left(-\\frac{3}{2},\\ f\\left(-\\frac{3}{2}\\right)\\right)$$",
        ],
    },
    {
        "prompt_md": "Use the Second Derivative Test for " + _in("f(x)=x^{4}-8x^{2}+10") + " to classify local extrema.",
        "solution_steps_md": [
            "$$f'(x)=4x^{3}-16x=4x(x-2)(x+2)$$",
            "$$f'(x)=0\\Rightarrow x=-2,\\ 0,\\ 2$$",
            "$$f''(x)=12x^{2}-16$$",
            "$$f''(0)=-16<0\\Rightarrow\\text{local maximum at }x=0$$",
            "$$f''(2)=32>0\\Rightarrow\\text{local minimum at }x=2$$",
            "$$f''(-2)=32>0\\Rightarrow\\text{local minimum at }x=-2$$",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=x^{4}") + ", apply the Second Derivative Test at the critical point and state the conclusion.",
        "solution_steps_md": [
            "$$f'(x)=4x^{3}\\Rightarrow f'(x)=0\\Rightarrow x=0$$",
            "$$f''(x)=12x^{2}\\Rightarrow f''(0)=0$$",
            "Because " + _in("f''(0)=0") + ", the Second Derivative Test is **inconclusive**.",
        ],
    },
    {
        "prompt_md": "Find concavity and inflection point(s) for " + _in("f(x)=\\frac{1}{x}") + " on its domain.",
        "solution_steps_md": [
            "$$f'(x)=-\\frac{1}{x^{2}},\\quad f''(x)=\\frac{2}{x^{3}}$$",
            "On the domain " + _in("x\\neq 0") + ":\n"
            + "$$x>0\\Rightarrow f''(x)>0\\Rightarrow\\text{concave up on }(0,\\infty)$$\n"
            + "$$x<0\\Rightarrow f''(x)<0\\Rightarrow\\text{concave down on }(-\\infty,0)$$",
            "No inflection point because " + _in("x=0") + " is not in the domain.",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=x^{3}+x") + ", determine concavity and whether any inflection point exists.",
        "solution_steps_md": [
            "$$f'(x)=3x^{2}+1,\\quad f''(x)=6x$$",
            "$$f''(x)=0\\Rightarrow x=0$$",
            "$$x<0\\Rightarrow\\text{concave down},\\quad x>0\\Rightarrow\\text{concave up}$$",
            "Inflection point at:\n$$\\bigl(0,f(0)\\bigr)=(0,0)$$",
        ],
    },
    {
        "prompt_md": "Use " + _in("f''(x)") + " to find concavity for " + _in("f(x)=\\sin(x)") + " on " + _in("\\left(0,2\\pi\\right)") + ".",
        "solution_steps_md": [
            "$$f'(x)=\\cos(x),\\quad f''(x)=-\\sin(x)$$",
            "$$\\sin(x)>0\\Rightarrow f''(x)<0\\Rightarrow\\text{concave down on }(0,\\pi)$$",
            "$$\\sin(x)<0\\Rightarrow f''(x)>0\\Rightarrow\\text{concave up on }(\\pi,2\\pi)$$",
            "$$f''(x)=0\\Rightarrow x=\\pi$$",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=\\ln(x)") + " on " + _in("(0,\\infty)") + ", state concavity.",
        "solution_steps_md": [
            "$$f'(x)=\\frac{1}{x},\\quad f''(x)=-\\frac{1}{x^{2}}$$",
            "Since " + _in("-\\frac{1}{x^{2}}<0") + " for all " + _in("x>0") + ", concave down on:\n$$ (0,\\infty) $$",
        ],
    },
    {
        "prompt_md": "Use the Second Derivative Test for " + _in("f(x)=x^{3}-6x^{2}+9x") + " to classify its critical points.",
        "solution_steps_md": [
            "$$f'(x)=3(x-1)(x-3)\\Rightarrow x=1,\\ 3$$",
            "$$f''(x)=6x-12$$",
            "$$f''(1)=-6<0\\Rightarrow\\text{local maximum at }x=1$$",
            "$$f''(3)=6>0\\Rightarrow\\text{local minimum at }x=3$$",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=\\frac{25}{x}+x") + ", find concavity on its domain.",
        "solution_steps_md": [
            "$$f'(x)=-\\frac{25}{x^{2}}+1,\\quad f''(x)=\\frac{50}{x^{3}}$$",
            "$$x>0\\Rightarrow\\text{concave up on }(0,\\infty)$$",
            "$$x<0\\Rightarrow\\text{concave down on }(-\\infty,0)$$",
            "No inflection point because " + _in("x=0") + " not in domain.",
        ],
    },
    {
        "prompt_md": "Find concavity and inflection for " + _in("f(x)=x^{4}+x^{2}") + ".",
        "solution_steps_md": [
            "$$f''(x)=12x^{2}+2>0\\ \\forall x$$",
            "Concave up on:\n$$(-\\infty,\\infty)$$",
            "No inflection point.",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=x^{3}-x^{2}") + ", find concavity intervals and inflection point(s).",
        "solution_steps_md": [
            "$$f''(x)=6x-2$$",
            "$$6x-2=0\\Rightarrow x=\\frac{1}{3}$$",
            "$$\\text{concave down on }(-\\infty,\\frac{1}{3}),\\quad \\text{concave up on }(\\frac{1}{3},\\infty)$$",
            "Inflection at:\n$$\\left(\\frac{1}{3},\\ f\\left(\\frac{1}{3}\\right)\\right)$$",
        ],
    },
    {
        "prompt_md": "Second Derivative Test: classify the critical point of " + _in("f(x)=x^{2}") + ".",
        "solution_steps_md": [
            "$$f'(x)=2x\\Rightarrow x=0$$",
            "$$f''(x)=2>0\\Rightarrow\\text{local minimum at }x=0$$",
        ],
    },
    {
        "prompt_md": "For " + _in("C(x)=x^{3}-6x^{2}+12x") + ", state concavity and interpret what it means for " + _in("C'(x)") + ".",
        "solution_steps_md": [
            "$$C''(x)=6(x-2)$$",
            "$$x<2\\Rightarrow\\text{concave down},\\quad x>2\\Rightarrow\\text{concave up}$$",
            _in("C'(x)") + " decreases for " + _in("x<2") + " and increases for " + _in("x>2") + ".",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=(x+2)^{\\frac{1}{5}}+4") + ", identify where " + _in("f'(x)") + " is undefined and what it means.",
        "solution_steps_md": [
            "$$f'(x)=\\frac{1}{5}(x+2)^{-\\frac{4}{5}}$$",
            "$$f'(x)\\text{ undefined at }x=-2$$",
            "This indicates a **vertical tangent** at " + _in("x=-2") + ".",
        ],
    },
    {
        "prompt_md": "Find concavity for " + _in("f(x)=e^{x}") + ".",
        "solution_steps_md": [
            "$$f''(x)=e^{x}>0\\ \\forall x$$",
            "Concave up on:\n$$(-\\infty,\\infty)$$",
        ],
    },
    {
        "prompt_md": "Second Derivative Test: classify critical points of " + _in("f(x)=x^{3}") + ".",
        "solution_steps_md": [
            "$$f'(x)=3x^{2}\\Rightarrow x=0$$",
            "$$f''(0)=0\\Rightarrow\\text{inconclusive}$$",
        ],
    },
    {
        "prompt_md": "Concavity for " + _in("f(x)=\\cos(x)") + " on " + _in("\\left(0,2\\pi\\right)") + ".",
        "solution_steps_md": [
            "$$f''(x)=-\\cos(x)$$",
            "$$\\cos(x)<0\\Rightarrow\\text{concave up on }\\left(\\frac{\\pi}{2},\\frac{3\\pi}{2}\\right)$$",
            "$$\\cos(x)>0\\Rightarrow\\text{concave down on }\\left(0,\\frac{\\pi}{2}\\right)\\cup\\left(\\frac{3\\pi}{2},2\\pi\\right)$$",
        ],
    },
    {
        "prompt_md": "For " + _in("f(x)=x^{4}-4x^{3}") + ", determine concavity intervals using " + _in("f''(x)") + ".",
        "solution_steps_md": [
            "$$f''(x)=12x(x-2)$$",
            "$$\\text{concave up on }(-\\infty,0)\\cup(2,\\infty),\\quad \\text{concave down on }(0,2)$$",
        ],
    },
    {
        "prompt_md": "Second Derivative Test: for " + _in("f(x)=x^{3}-3x^{2}") + ", classify critical points.",
        "solution_steps_md": [
            "$$f'(x)=3x(x-2)\\Rightarrow x=0,\\ 2$$",
            "$$f''(x)=6x-6$$",
            "$$f''(0)=-6<0\\Rightarrow\\text{local maximum at }x=0$$",
            "$$f''(2)=6>0\\Rightarrow\\text{local minimum at }x=2$$",
        ],
    },
]