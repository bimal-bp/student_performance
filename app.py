import streamlit as st
import numpy as np

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

# Streamlit UI
st.title("Dashboard - Study Time Allocator")

# User Input Form
with st.form("user_info"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    student_class = st.text_input("Class")
    
    st.subheader("Enter your subject scores (%)")
    math = st.slider("Math", 0, 100, 50)
    eng = st.slider("English", 0, 100, 50)
    sci = st.slider("Science", 0, 100, 50)
    comp = st.slider("Computer", 0, 100, 50)
    study_time = st.number_input("Daily Study Time (hours)", min_value=1.0, max_value=10.0, step=0.5)
    
    submitted = st.form_submit_button("Calculate Study Plan")

if submitted:
    study_plan = wsm_allocation(math, eng, sci, comp, study_time)
    
    st.subheader("Study Plan")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Study Time Allocation")
        for subject, time in study_plan.items():
            st.write(f"{subject}: {time} hours")
    
    with col2:
        st.subheader("View PDF")
        pdf_option = st.selectbox("Select a PDF", ["Basics of Computer.pdf", "10th_Mathematics_English_Medium.pdf"])
        if st.button("Open PDF"):
            st.write(f"Opening: {pdf_option}")
    
    with col3:
        st.subheader("Quiz Section")
        if st.button("Start Quiz"):
            st.write("Quiz Started!")
