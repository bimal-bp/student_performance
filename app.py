import streamlit as st
import numpy as np
import random

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

# Sample Quiz Questions (10 Questions)
quiz_questions = [
    ("What is 5 + 3?", ["6", "7", "8", "9"], "8"),
    ("Which planet is known as the Red Planet?", ["Earth", "Mars", "Jupiter", "Venus"], "Mars"),
    ("Who wrote 'Hamlet'?", ["Shakespeare", "Dickens", "Austen", "Hemingway"], "Shakespeare"),
    ("What is the capital of France?", ["London", "Berlin", "Paris", "Madrid"], "Paris"),
    ("What is H2O?", ["Oxygen", "Water", "Hydrogen", "Helium"], "Water"),
    ("What is the square root of 64?", ["6", "7", "8", "9"], "8"),
    ("Which gas do plants absorb from the atmosphere?", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "Carbon Dioxide"),
    ("What is the largest mammal?", ["Elephant", "Whale", "Giraffe", "Hippo"], "Whale"),
    ("Who discovered gravity?", ["Newton", "Einstein", "Galileo", "Edison"], "Newton"),
    ("What is the boiling point of water?", ["50°C", "75°C", "100°C", "150°C"], "100°C")
]

# Streamlit UI Setup
st.set_page_config(page_title="Study Planner", layout="wide")

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# 🏠 **Home Page - User Input**
if st.session_state.page == "home":
    st.title("📚 Study Time Allocator")

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
    st.title("📊 Study Plan")

    st.subheader("📌 Study Time Allocation")
    for subject, time in st.session_state.study_plan.items():
        st.write(f"✅ {subject}: **{time} hours**")

    st.subheader("📝 Quiz Section")
    if not st.session_state.quiz_started:
        if st.button("🚀 Start Quiz"):
            st.session_state.quiz_started = True
            st.experimental_rerun()
    else:
        st.write("🧠 Answer the following questions:")
        correct_answers = 0

        # Display Questions
        for i, (question, options, correct_answer) in enumerate(quiz_questions):
            user_answer = st.radio(f"**{i+1}. {question}**", options, key=f"q{i}")
            st.session_state.quiz_answers[i] = user_answer
            if user_answer == correct_answer:
                correct_answers += 1

        # Submit Quiz Button
        if st.button("📊 Submit Quiz"):
            st.success(f"🎉 You scored {correct_answers}/10!")
            st.session_state.quiz_started = False

    # 🔙 **Back Button**
    if st.button("🔙 Go Back"):
        st.session_state.page = "home"
        st.experimental_rerun()
