# app.py
import streamlit as st

from banner import render_banner
from ai_helper import render_sidebar_ai_helper

import subtopic_4_5_chain_rule as st_4_5
import subtopic_4_6_trig_derivatives as st_4_6
import subtopic_4_7_exp_log_derivatives as st_4_7
import subtopic_4_8_implicit_inverse_trig as st_4_8
import subtopic_4_9_hyperbolic as st_4_9
import subtopic_4_10_mean_value_theorem as st_4_10  # ✅ NEW

# ✅ NEW: Topic 5 subtopics
import subtopic_5_1_linear_approximations_newtons_method as st_5_1
import subtopic_5_2_indeterminate_forms_lhopitals_rule as st_5_2
import subtopic_5_3_maximum_minimum_values as st_5_3
import subtopic_5_4_increasing_decreasing_functions as st_5_4
import subtopic_5_5_concavity_second_derivative_test as st_5_5
import subtopic_5_6_curve_sketching_overview as st_5_6


def build_registry():
    # Robust, never-break registry (dict-of-dicts, no mixed indexing)
    return {
        "Term 2": {
            "Topic 4: Differentiation (Cont’d)": {
                "Subtopic 4.5: The Chain Rule": {
                    "module": st_4_5,
                    "key": "4_5_chain_rule",
                },
                "Subtopic 4.6: Trig Derivatives": {
                    "module": st_4_6,
                    "key": "4_6_trig_derivatives",
                },
                "Subtopic 4.7: Exponential & Log Derivatives": {
                    "module": st_4_7,
                    "key": "4_7_exp_log_derivatives",
                },
                "Subtopic 4.8: Implicit & Inverse Trig": {
                    "module": st_4_8,
                    "key": "4_8_'implicit_inverse_trig",
                },
                "Subtopic 4.9: Hyperbolic": {
                    "module": st_4_9,
                    "key": "4_9_hyperbolic",
                },
                # ✅ NEW (as per attached table)
                "Subtopic 4.10: The Mean Value Theorem": {
                    "module": st_4_10,
                    "key": "4_10_mean_value_theorem",
                },
            },

            # ✅ NEW: Topic 5 (Applications of Differentiation) + all subtopics
            "Topic 5: Applications of Differentiation": {
                "Subtopic 5.1: Linear Approximations and Newton’s Method": {
                    "module": st_5_1,
                    "key": "5_1_linear_approximations_newtons_method",
                },
                "Subtopic 5.2: Indeterminate Forms and Hospital’s Rule": {
                    "module": st_5_2,
                    "key": "5_2_indeterminate_forms_lhopitals_rule",
                },
                "Subtopic 5.3: Maximum and Minimum Values": {
                    "module": st_5_3,
                    "key": "5_3_maximum_minimum_values",
                },
                "Subtopic 5.4: Increasing and Decreasing Functions": {
                    "module": st_5_4,
                    "key": "5_4_increasing_decreasing_functions",
                },
                "Subtopic 5.5: Concavity and 2nd Derivative Test": {
                    "module": st_5_5,
                    "key": "5_5_concavity_second_derivative_test",
                },
                "Subtopic 5.6: Overview of Curve Sketching": {
                    "module": st_5_6,
                    "key": "5_6_curve_sketching_overview",
                },
            },
        }
    }


def main():
    st.set_page_config(
        page_title="AQB Grade 12 AI Math Tutor",
        page_icon="📘",
        layout="wide",
    )

    registry = build_registry()

    # Banner
    render_banner()

    # Sidebar navigation
    st.sidebar.markdown("## Navigation")

    terms = list(registry.keys())
    selected_term = st.sidebar.selectbox("Term", terms, index=0)

    topics = list(registry[selected_term].keys())
    selected_topic = st.sidebar.selectbox("Topic", topics, index=0)

    subtopics = list(registry[selected_term][selected_topic].keys())
    selected_subtopic = st.sidebar.selectbox("Subtopic", subtopics, index=0)

    # Sidebar AI Helper (PDFs)
    st.sidebar.markdown("---")
    render_sidebar_ai_helper(selected_term, selected_topic, selected_subtopic)

    # Main content
    subtopic_info = registry[selected_term][selected_topic][selected_subtopic]
    module = subtopic_info["module"]

    st.markdown(
        f"### {selected_subtopic}\n"
        f"<div style='color:#5b6b7a;'>Term: <b>{selected_term}</b> • Topic: <b>{selected_topic}</b></div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Each subtopic module must expose render()
    if hasattr(module, "render"):
        module.render()
    else:
        st.error("This subtopic module is missing a required render() function.")


if __name__ == "__main__":
    main()
