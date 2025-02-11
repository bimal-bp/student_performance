import streamlit as st
import numpy as np
import requests

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
    "10th_Computer": "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp",
    "10th_Mathematics": "1g83nbaDLFtUYBW46uWqZSxF6kKGCnoEk",
    "10th_Science": "1Z5Lh-v0lzHZ6tc-SZFZGJQsbykeCW57P",
    "10th_English": "1qYkk7srJSnfzSQahhdcSGFbZ48uptr_d",
    "10th_Social Science": "1fqQlgUs6f8V4CMEEkFxM6lDLHi3FePpq"
}

# Function to get quiz questions
def get_advanced_quiz():
    api_url = "https://gemi-api-url.com/generate-quiz"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('quiz_questions', [])
    else:
        return ["Unable to fetch advanced quiz."]

# Streamlit UI Setup
st.set_page_config(page_title="Study Planner & PDF Viewer", layout="wide")

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "login"

# 🏠 Login Page
if st.session_state.page == "login":
    st.title("📚 Study Time Allocator & PDF Notes - Login")
    with st.form("login_form"):
        name = st.text_input("👤 Name")
        password = st.text_input("🔑 Password", type="password")
        submitted = st.form_submit_button("🚪 Login")
    
    if submitted and password == "student123":
        st.session_state.page = "dashboard"
        st.experimental_rerun()
    elif submitted:
        st.error("❌ Incorrect Password!")

# 📊 Dashboard Page
elif st.session_state.page == "dashboard":
    st.title("📊 Study Plan & Learning Resources")
    with st.form("user_info"):
        st.subheader("🎯 Enter Your Subject Scores (%)")
        math = st.slider("🧮 Math", 0, 100, 50)
        eng = st.slider("📖 English", 0, 100, 50)
        sci = st.slider("🔬 Science", 0, 100, 50)
        comp = st.slider("💻 Computer", 0, 100, 50)
        soc = st.slider("🌍 Social Science", 0, 100, 50)
        study_time = st.number_input("⏳ Daily Study Time (hours)", min_value=1.0, max_value=10.0, step=0.5)
        submitted = st.form_submit_button("📊 Generate Study Plan")
    
    if submitted:
        st.session_state.study_plan = wsm_allocation(math, eng, sci, comp, soc, study_time)
        st.experimental_rerun()
    
    if "study_plan" in st.session_state:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("📌 Study Time Allocation")
            for subject, time in st.session_state.study_plan.items():
                st.write(f"✅ {subject}: *{time} hours*")
        
        with col2:
            st.subheader("📖 Study Material (Scrollable PDF)")
            pdf_option = st.selectbox("📂 Select a PDF", list(pdf_drive_links.keys()))
            pdf_viewer_url = get_pdf_viewer_link(pdf_drive_links[pdf_option])
            st.markdown(f"<iframe src='{pdf_viewer_url}' width='100%' height='600px'></iframe>", unsafe_allow_html=True)
    
    if st.button("📝 Start Quiz"):
        st.session_state.page = "quiz"
        st.experimental_rerun()

# 📝 Quiz Page
elif st.session_state.page == "quiz":
    st.title("📝 Quiz Section")
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
    
    if st.button("💡 Generate Advanced Quiz"):
        advanced_quiz = get_advanced_quiz()
        for question in advanced_quiz:
            st.write(question)
    
    if st.button("🔙 Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.experimental_rerun()
