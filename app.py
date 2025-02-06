import streamlit as st
import numpy as np

# Function to allocate study time
def wsm_allocation(math, eng, sci, comp, total_study_time):
    total_score = math + eng + sci + comp
    weights = [(100 - math) / total_score, (100 - eng) / total_score, (100 - sci) / total_score, (100 - comp) / total_score]
    study_times = np.array(weights) * total_study_time
    return {
        "Math": round(study_times[0], 2),
        "English": round(study_times[1], 2),
        "Science": round(study_times[2], 2),
        "Computer": round(study_times[3], 2)
    }

# Google Drive PDF links
pdf_links = {
    "Basics of Computer": "https://drive.google.com/file/d/1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp/preview"
}

# Streamlit UI
st.set_page_config(page_title="Study Time Allocator", layout="wide")

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "home"

# Home Page - User Input
if st.session_state.page == "home":
    st.title("📚 Study Time Allocator Dashboard")

    # User Input Form
    with st.form("user_info"):
        name = st.text_input("👤 Name")
        age = st.number_input("📅 Age", min_value=5, max_value=100, step=1)
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
        student_class = st.text_input("🏫 Class")

        st.subheader("🎯 Enter Your Subject Scores (%)")
        math = st.slider("🧮 Math", 0, 100, 50)
        eng = st.slider("📖 English", 0, 100, 50)
        sci = st.slider("🔬 Science", 0, 100, 50)
        comp = st.slider("💻 Computer", 0, 100, 50)
        study_time = st.number_input("⏳ Daily Study Time (hours)", min_value=1.0, max_value=10.0, step=0.5)

        submitted = st.form_submit_button("📊 Generate Study Plan")

    # Navigate to Dashboard Page
    if submitted:
        st.session_state.page = "dashboard"
        st.session_state.study_plan = wsm_allocation(math, eng, sci, comp, study_time)
        st.experimental_rerun()

# Dashboard Page
elif st.session_state.page == "dashboard":
    st.title("📊 Study Plan Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Study Time Allocation")
        for subject, time in st.session_state.study_plan.items():
            st.write(f"✅ {subject}: **{time} hours**")

    with col2:
        st.subheader("📄 View PDF Notes")
        pdf_option = st.selectbox("📂 Select a PDF", list(pdf_links.keys()))
        
        if pdf_option:
            st.write(f"**📖 {pdf_option} Preview:**")
            pdf_url = pdf_links[pdf_option]
            st.markdown(f'<iframe src="{pdf_url}" width="700" height="600"></iframe>', unsafe_allow_html=True)

    # Add Back Button
    if st.button("🔙 Go Back"):
        st.session_state.page = "home"
        st.experimental_rerun()
