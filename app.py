import streamlit as st
import numpy as np
import requests
from io import BytesIO

# Function to allocate study time based on scores
def wsm_allocation(math, eng, sci, comp, total_study_time):
    total_score = math + eng + sci + comp
    if total_score == 400:  # Avoid division by zero when all scores are 100%
        weights = [0.25, 0.25, 0.25, 0.25]
    else:
        weights = [(100 - s) / (400 - total_score) for s in [math, eng, sci, comp]]
    
    study_times = np.array(weights) * total_study_time
    return {
        "Math": round(study_times[0], 2),
        "English": round(study_times[1], 2),
        "Science": round(study_times[2], 2),
        "Computer": round(study_times[3], 2)
    }

# GitHub raw PDF URLs
pdf_urls = {
    "Basics of Computer.pdf": "https://raw.githubusercontent.com/bimal-bp/student_performance/main/Basics%20of%20Computer.pdf",
    "10th Mathematics English Medium.pdf": "https://raw.githubusercontent.com/bimal-bp/student_performance/main/10th_Mathametics%20English_Medium_Text_www.tntextbooks.in.pdf"
}

# Fetch PDF from GitHub
def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        st.error("⚠️ Failed to load PDF. Please check the file URL.")
        return None

# Streamlit UI
st.set_page_config(page_title="📚 Study Time Allocator", layout="wide")

# Session State for Navigation
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
        st.rerun()

# Dashboard Page
elif st.session_state.page == "dashboard":
    st.title("📊 Study Plan Dashboard")

    col1, col2, col3 = st.columns(3)

    # Study Time Allocation
    with col1:
        st.subheader("📌 Study Time Allocation")
        for subject, time in st.session_state.study_plan.items():
            st.write(f"✅ {subject}: **{time} hours**")

    # PDF Notes Section
    with col2:
        st.subheader("📄 View PDF Notes")
        pdf_option = st.selectbox("📂 Select a PDF", list(pdf_urls.keys()))
        
        if st.button("📖 Open PDF"):
            pdf_url = pdf_urls[pdf_option]
            st.write(f"**📖 {pdf_option} Preview:**")
            st.components.v1.iframe(pdf_url, height=600)

            # Download Button
            pdf_data = fetch_pdf(pdf_url)
            if pdf_data:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_data,
                    file_name=pdf_option,
                    mime="application/pdf"
                )

    # Quiz Section
    with col3:
        st.subheader("📝 Quiz Section")
        if st.button("🚀 Start Quiz"):
            st.success("🎉 Quiz Started!")

    # Back Button
    if st.button("🔙 Go Back"):
        st.session_state.page = "home"
        st.rerun()
