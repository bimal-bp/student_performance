import streamlit as st
import numpy as np
import requests
import pdfplumber
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

# Google Drive File IDs (Extracted from links)
pdf_drive_links = {
    "Basics of Computer.pdf": "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp",  # Computer PDF
    "10th_Mathematics_English_Medium.pdf": "1Os8nxl_EwyadsKhrAgagmjg3sHTH2Ylc"  # Math PDF
}

# Fetch PDF from Google Drive
def fetch_pdf_from_drive(file_id):
    drive_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(drive_url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        st.error("⚠️ Failed to load PDF. Please check the file URL.")
        return None

# Display PDF using pdfplumber
def display_pdf(pdf_data):
    with pdfplumber.open(pdf_data) as pdf:
        for page in pdf.pages:
            st.image(page.to_image())

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
        pdf_option = st.selectbox("📂 Select a PDF", list(pdf_drive_links.keys()))
        if st.button("📖 Open PDF"):
            pdf_data = fetch_pdf_from_drive(pdf_drive_links[pdf_option])
            if pdf_data:
                st.write(f"**📖 {pdf_option} Preview:**")
                display_pdf(pdf_data)

    with col3:
        st.subheader("📝 Quiz Section")
        if st.button("🚀 Start Quiz"):
            st.success("🎉 Quiz Started!")

    # Add Back Button
    if st.button("🔙 Go Back"):
        st.session_state.page = "home"
        st.experimental_rerun()
