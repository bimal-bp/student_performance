import streamlit as st
import pandas as pd
import numpy as np

def login_page():
    st.title("Student Login")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    number = st.text_input("Phone Number")
    mail = st.text_input("Email")
    study_time = st.slider("Study Time per Week (hrs)", 0, 50, 10)
    
    subjects = [
        "Data Structures and Algorithms", "Operating Systems", "Database Management Systems",
        "Computer Networks", "Software Engineering", "Python", "Object-Oriented Programming (Java/C/C++)",
        "Web Technologies", "Theory of Computation", "Compiler Design", "Artificial Intelligence",
        "Machine Learning", "Cloud Computing", "Cybersecurity", "Distributed Systems",
        "Deep Learning", "Data Mining", "Big Data Analytics", "Natural Language Processing",
        "Reinforcement Learning", "Data Visualization", "Business Intelligence"
    ]
    selected_subjects = st.multiselect("Select 10 Subjects", subjects, max_selections=10)
    
    if st.button("Go to Dashboard") and len(selected_subjects) == 10:
        st.session_state["student_info"] = {
            "name": name, "age": age, "gender": gender,
            "number": number, "mail": mail, "study_time": study_time,
            "selected_subjects": selected_subjects
        }
        st.session_state["page"] = "dashboard"

def dashboard_page():
    st.title("Student Dashboard")
    student_info = st.session_state.get("student_info", {})
    
    st.markdown("""
        <style>
        .small-box {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .medium-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        </style>
    
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])  # Adjust column widths to give more space to the table
    
    with col1:
        st.markdown('<div class="small-box">', unsafe_allow_html=True)
        st.subheader("Student Info")
        st.write(f"**Name:** {student_info.get('name', '')}")
        st.write(f"**Age:** {student_info.get('age', '')}")
        st.write(f"**Gender:** {student_info.get('gender', '')}")
        st.write(f"**Email:** {student_info.get('mail', '')}")
        st.write(f"**Contact Number:** {student_info.get('number', '')}")
        st.write(f"**Weekly Study Time:** {student_info.get('study_time', '')} hrs")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="small-box">', unsafe_allow_html=True)
        st.subheader("Study Time Allocation")
        study_time = student_info.get("study_time", 10)
        subjects = student_info.get("selected_subjects", [])
        
        if subjects:
            weights = np.random.dirichlet(np.ones(len(subjects)), size=1)[0] * study_time
            df = pd.DataFrame({"Subject": subjects, "Allocated Time (hrs)": weights})
            st.dataframe(df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="medium-box">', unsafe_allow_html=True)
    st.subheader("Reading Content")
    st.write("(Placeholder for study materials and resources)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("Predict Your Future Score"):
            st.write("(Placeholder for prediction logic)")
    
    with col4:
        if st.button("Quiz Section"):
            st.session_state["page"] = "quiz"
def quiz_page():
    st.title("Quiz Section")
    st.write("(Placeholder for quiz questions based on selected subjects)")
    
    if st.button("Back to Dashboard"):
        st.session_state["page"] = "dashboard"

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if st.session_state["page"] == "login":
    login_page()
elif st.session_state["page"] == "dashboard":
    dashboard_page()
elif st.session_state["page"] == "quiz":
    quiz_page()
