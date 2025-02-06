import streamlit as st
import numpy as np

# Function to allocate study time using Weighted Score Method (WSM)
def wsm_allocation(math, eng, sci, comp, total_study_time):
    total_score = math + eng + sci + comp
    weights = [(100 - math) / total_score, (100 - eng) / total_score, 
               (100 - sci) / total_score, (100 - comp) / total_score]
    study_times = np.array(weights) * total_study_time
    return {
        "Math": round(study_times[0], 2),
        "English": round(study_times[1], 2),
        "Science": round(study_times[2], 2),
        "Computer": round(study_times[3], 2)
    }

# Function to generate an embeddable Google Drive link
def get_pdf_viewer_link(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview"

# Google Drive PDF file IDs
pdf_drive_links = {
    "Basics of Computer.pdf": "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp",  # Computer PDF
    "10th_Mathematics_English_Medium.pdf": "1Os8nxl_EwyadsKhrAgagmjg3sHTH2Ylc"  # Math PDF
}

# Streamlit UI Setup
st.set_page_config(page_title="Study Planner & PDF Viewer", layout="wide")

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "home"

# 🏠 **Home Page - User Input**
if st.session_state.page == "home":
    st.title("📚 Study Time Allocator & PDF Notes")

    # 📝 User Input Form
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

# 📊 **Dashboard Page**
elif st.session_state.page == "dashboard":
    st.title("📊 Study Plan & Learning Resources")

    col1, col2 = st.columns([1, 2])

    # 📌 **Study Time Allocation**
    with col1:
        st.subheader("📌 Study Time Allocation")
        for subject, time in st.session_state.study_plan.items():
            st.write(f"✅ {subject}: **{time} hours**")

        # 🔙 **Back Button**
        if st.button("🔙 Go Back"):
            st.session_state.page = "home"
            st.experimental_rerun()

    # 📄 **PDF Viewer**
    with col2:
        st.subheader("📖 Study Material (Scrollable PDF)")
        pdf_option = st.selectbox("📂 Select a PDF", list(pdf_drive_links.keys()))

        # Generate PDF Viewer Link
        pdf_viewer_url = get_pdf_viewer_link(pdf_drive_links[pdf_option])

        # Display Embedded PDF (Scrollable)
        st.markdown(f"""
            <iframe src="{pdf_viewer_url}" width="100%" height="600px"></iframe>
        """, unsafe_allow_html=True)
import streamlit as st
import pdfplumber
from PIL import Image
import requests
from io import BytesIO

# Function to fetch PDF from Google Drive (works in a web viewer)
def fetch_pdf_from_drive(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Function to display PDF pages as images in Streamlit
def display_pdf(pdf_url):
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            for page in pdf.pages:
                img = page.to_image().annotated  # Convert page to an image
                st.image(img, use_column_width=True)
    else:
        st.error("Failed to load PDF. Please check the link.")

# Streamlit App Layout
st.title("📄 PDF Viewer in Streamlit")

# Google Drive PDF file IDs
math_pdf_id = "1Os8nxl_EwyadsKhrAgagmjg3sHTH2Ylc"  # Replace with actual Math PDF ID
computer_pdf_id = "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp"  # Replace with actual Computer PDF ID

# Generate direct links
math_pdf_url = fetch_pdf_from_drive(math_pdf_id)
computer_pdf_url = fetch_pdf_from_drive(computer_pdf_id)

# Dropdown to select PDF
pdf_choice = st.selectbox("Select a PDF:", ["Math PDF", "Computer PDF"])

# Display the selected PDF
if pdf_choice == "Math PDF":
    display_pdf(math_pdf_url)
elif pdf_choice == "Computer PDF":
    display_pdf(computer_pdf_url)
