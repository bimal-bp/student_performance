import streamlit as st
import numpy as np

# Function to allocate study time using Weighted Score Method (WSM)
def wsm_allocation(math, eng, sci, comp, soc, total_study_time):
    total_score = math + eng + sci + comp + soc
    weights = [(100 - math) / total_score, (100 - eng) / total_score, 
               (100 - sci) / total_score, (100 - comp) / total_score,
               (100 - soc) / total_score]
    study_times = np.array(weights) * total_study_time
    return {
        "Math": round(study_times[0], 2),
        "English": round(study_times[1], 2),
        "Science": round(study_times[2], 2),
        "Computer": round(study_times[3], 2),
        "Social Science": round(study_times[4], 2)
    }

# Function to generate an embeddable Google Drive link
def get_pdf_viewer_link(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview"

# Google Drive PDF file IDs
pdf_drive_links = {
    "Computer ": "1Bbs8U2Vh2c9N9gQkNyoH9ezj2KMh3Bk4",  # Updated Computer PDF
    "Mathematics ": "1KhT3-9RgG8LPLc8BkL5TGnmYRoe8eKrG",  # Updated Math PDF
    "Science ": "1Z5Lh-v0lzHZ6tc-SZFZGJQsbykeCW57P",  # Updated Science PDF
    "English ": "1X2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N",  # Updated English PDF
    "Social Science": "1Q2W3E4R5T6Y7U8I9O0P1A2S3D4F5G6H7J8K"  # Updated Social Science PDF
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
        soc = st.slider("🌍 Social Science", 0, 100, 50)
        study_time = st.number_input("⏳ Daily Study Time (hours)", min_value=1.0, max_value=10.0, step=0.5)

        submitted = st.form_submit_button("📊 Generate Study Plan")

    # Navigate to Dashboard Page
    if submitted:
        st.session_state.page = "dashboard"
        st.session_state.study_plan = wsm_allocation(math, eng, sci, comp, soc, study_time)
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
    
    # 📚 **Quiz Section**
    st.subheader("📝 Quick Quiz")
    
    quiz_questions = {
        "What is the capital of France?": ["Paris", "London", "Berlin", "Madrid"],
        "What is 5 + 3?": ["6", "7", "8", "9"],
        "Which planet is known as the Red Planet?": ["Earth", "Mars", "Jupiter", "Venus"]
    }
    
    answers = {"What is the capital of France?": "Paris", "What is 5 + 3?": "8", "Which planet is known as the Red Planet?": "Mars"}
    
    score = 0
    for question, options in quiz_questions.items():
        user_answer = st.radio(question, options, index=None)
        if user_answer is not None and user_answer == answers[question]:
            score += 1
    
    if st.button("Submit Quiz"):
        st.success(f"🎉 Your Score: {score}/{len(quiz_questions)}")
