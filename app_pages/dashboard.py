import streamlit as st
import plotly.graph_objects as go

def dashboard():
    st.title("AI Technical Interviewer")
    st.markdown("##### Simulate real technical interviews tailored to your resume and target role.")
    st.divider()

    # ── Last Session Results ──────────────────────────────────────────────────
    has_summary = (
        "performance_summary" in st.session_state
        and st.session_state.performance_summary is not None
    )

    if has_summary:
        summary = st.session_state.performance_summary

        st.subheader("Last Session Results")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Overall", f"{summary.overall_score}/10")
        col2.metric("Technical", f"{summary.technical_accuracy}/10")
        col3.metric("Communication", f"{summary.communication_skills}/10")
        col4.metric("Problem Solving", f"{summary.problem_solving}/10")
        col5.metric("Code Quality", f"{summary.code_quality}/10")

        # Mini radar chart
        categories = ["Technical", "Communication", "Problem Solving", "Code Quality"]
        scores = [
            summary.technical_accuracy,
            summary.communication_skills,
            summary.problem_solving,
            summary.code_quality,
        ]
        fig = go.Figure(
            data=go.Scatterpolar(r=scores, theta=categories, fill="toself",
                                 line_color="steelblue")
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            height=320,
            margin=dict(t=20, b=20, l=40, r=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("View Full Report", use_container_width=True, type="secondary"):
                st.session_state.page = "page3"
                st.rerun()
        with btn_col2:
            if st.button("Start New Interview", use_container_width=True, type="primary"):
                # Clear previous session data
                for key in ["messages", "feedbacks", "performance_summary",
                            "current_question_type", "resume", "job_role",
                            "experience", "company_name", "input_id", "autoplay_audio"]:
                    st.session_state.pop(key, None)
                st.session_state.page = "page1"
                st.rerun()

    else:
        # ── First-time / no session state ────────────────────────────────────
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**📄 Resume-Aware**\n\nQuestions tailored to your actual experience and skills.")
        with col2:
            st.info("**🎙️ Voice + Code**\n\nAnswer by typing, speaking, or using the built-in code editor.")
        with col3:
            st.info("**📊 Instant Feedback**\n\nDetailed performance report with radar chart after each session.")

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn, _, _ = st.columns([1, 1, 1])
        with col_btn:
            if st.button("Start Interview", use_container_width=True, type="primary"):
                st.session_state.page = "page1"
                st.rerun()
