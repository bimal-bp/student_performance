import streamlit as st
import numpy as np
import requests
from io import BytesIO

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

# GitHub raw PDF URLs
pdf_urls = {
    "Basics of Computer.pdf": "https://bimal-bp.github.io/student_performance/Basics%20of%20Computer.pdf",
    "10th_Mathematics_English_Medium.pdf": "https://bimal-bp.github.io/student_performance/10th_Mathametics%20English%20Medium_Text_www.tntextbooks.in.pdf"
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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📌 Study Time Allocation")
        for subject, time in st.session_state.study_plan.items():
            st.write(f"✅ {subject}: **{time} hours**")

    with col2:
        st.subheader("📄 View PDF Notes")
        pdf_option = st.selectbox("📂 Select a PDF", list(pdf_urls.keys()))
        if st.button("📖 Open PDF"):
            pdf_url = pdf_urls[pdf_option]
            st.components.v1.iframe(pdf_url, width=700, height=500)

    with col3:
        st.subheader("📝 Quiz Section")
        if st.button("🚀 Start Quiz"):
            st.success("🎉 Quiz Started!")

    # Add Back Button
    if st.button("🔙 Go Back"):
        st.session_state.page = "home"
        st.experimental_rerun()
