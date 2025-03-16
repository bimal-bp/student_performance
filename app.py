import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np
import google.generativeai as genai
import pickle
import random

# Database Connection String
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyDWd-ZOM4dy5yLwconHJV6cVkNIoIbWC7g"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')

def get_db_connection():
    return psycopg2.connect(DB_URL)

# Subject importance ratings
subject_ratings = {
    # Computer Science
    "Programming": 10, "Data Structures & Algorithms": 10, "Operating Systems": 9,
    "Computer Networks": 9, "Database Management Systems": 9, "Software Engineering": 8,
    "Web Technologies": 8, "Compiler Design": 7, "Object-Oriented Programming": 9,
    "Cryptography & Network Security": 8, "Software Testing": 7, "Data Mining & Data Warehousing": 8,
    "Business Communication & Ethics": 6, "Business Analytics": 7, "Digital Marketing": 7,

    # Artificial Intelligence
    "Artificial Intelligence": 10, "Machine Learning": 10, "Deep Learning": 9,
    "Data Science & Analytics": 9, "Natural Language Processing": 8, "Neural Networks": 9,
    "Reinforcement Learning": 8, "Computer Vision": 8, "Linear Algebra for ML": 9,
    "Data Visualization": 9,

    # Electrical Engineering
    "Circuit Theory": 8, "Digital Logic Design": 9, "Analog & Digital Electronics": 9,
    "Signals & Systems": 8, "Microprocessors & Microcontrollers": 9, "Communication Systems": 8,
    "VLSI Design": 7, "Antennas & Wave Propagation": 7, "Embedded Systems": 9,
    "Optical Communication": 7, "IoT & Wireless Sensor Networks": 8, "Electrical Circuits": 8,
    "Control Systems": 9, "Power Systems": 8, "Electrical Machines": 8, "Power Electronics": 9,
    "Digital Signal Processing": 9, "High Voltage Engineering": 7, "Renewable Energy Systems": 8,
    "Industrial Automation": 8,

    # Mechanical Engineering
    "Engineering Mechanics": 9, "Strength of Materials": 9, "Thermodynamics": 9,
    "Fluid Mechanics": 8, "Manufacturing Processes": 8, "Heat & Mass Transfer": 9,
    "Machine Design": 9, "Robotics": 8, "CAD/CAM": 9, "Automotive Engineering": 7,
    "Industrial Engineering": 8,

    # Civil Engineering
    "Structural Analysis": 9, "Surveying": 8, "Geotechnical Engineering": 9,
    "Construction Materials": 8, "Transportation Engineering": 8, "Environmental Engineering": 8,
    "Hydrology & Water Resources": 7, "Building Design & Architecture": 8, "Earthquake Engineering": 8,

    # Common subjects
    "Engineering Mathematics": 10, "Engineering Physics": 8, "Engineering Chemistry": 6,
    "Basic Electrical and Electronical Engineering": 7, "Big Data Technologies": 8,
    "Cloud Computing": 8, "Cyber Security": 8, "Blockchain Technology": 7, "IoT (Internet of Things)": 7,
    "Introduction to AI & ML": 8, "Probability & Statistics": 10, "Engineering Drawing": 7,
}

def allocate_study_time(selected_subjects, total_hours, efficiency_level, problem_solving):
    efficiency_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[efficiency_level]
    problem_solving_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[problem_solving]
    ratings = np.array([subject_ratings.get(sub, 5) for sub in selected_subjects])
    weighted_ratings = ratings * efficiency_factor * problem_solving_factor
    normalized_weights = weighted_ratings / np.sum(weighted_ratings)
    allocated_times = np.round(normalized_weights * total_hours, 2)
    return dict(zip(selected_subjects, allocated_times))

def student_info():
    st.title("Learn Mate - Student Performance Application")
    st.header("Student Information")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    mobile_number = st.text_input("Mobile Number")

    st.subheader("Select Your Branch")
    branch = st.selectbox(
        "Choose your branch",
        options=["Computer Science", "Artificial Intelligence", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering"],
        key="branch"
    )

    common_subjects = [
        "Engineering Mathematics", "Engineering Physics", "Engineering Chemistry",
        "Basic Electrical and Electronical Engineering", "Web Technologies", "Programming",
        "Data Structures & Algorithms", "Operating Systems", "Computer Networks",
        "Cryptography & Network Security", "Big Data Technologies", "Cloud Computing",
        "Cyber Security", "Blockchain Technology", "IoT (Internet of Things)",
        "Introduction to AI & ML", "Data Science & Analytics", "Probability & Statistics",
        "Engineering Drawing"
    ]

    branch_subjects = {
        "Computer Science": ["Advanced Programming", "Database Management Systems", "Software Engineering", "Machine Learning", "Artificial Intelligence", "Computer Architecture"],
        "Artificial Intelligence": ["Deep Learning", "Natural Language Processing", "Computer Vision", "Reinforcement Learning", "AI Ethics", "Robotics"],
        "Electrical Engineering": ["Circuit Theory", "Power Systems", "Control Systems", "Signal Processing", "Microelectronics", "Renewable Energy Systems"],
        "Mechanical Engineering": ["Thermodynamics", "Fluid Mechanics", "Solid Mechanics", "Manufacturing Processes", "Heat Transfer", "Machine Design"],
        "Civil Engineering": ["Structural Analysis", "Geotechnical Engineering", "Transportation Engineering", "Environmental Engineering", "Construction Management", "Hydrology"]
    }

    all_subjects = common_subjects + branch_subjects.get(branch, [])
    selected_subjects = st.multiselect("Choose your subjects (select up to 10)", options=all_subjects, default=all_subjects[:10], key="subjects")

    st.subheader("Efficiency Levels")
    col1, col2 = st.columns(2)
    with col1:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])
    with col2:
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])
        conceptual_understanding = st.selectbox("Conceptual Understanding", ["low", "intermediate", "high"])
        time_management = st.selectbox("Time Management", ["low", "intermediate", "high"])

    study_time = st.number_input("Total Study Time Per Week (hours)", min_value=1, max_value=168)

    if st.button("Save Information"):
        if not email:
            st.error("Please enter an email.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                subjects_str = ", ".join(selected_subjects)
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, 
                        problem_solving_efficiency, conceptual_understanding, time_management, selected_subjects, study_time_per_week, branch)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name, age = EXCLUDED.age, mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency, math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        conceptual_understanding = EXCLUDED.conceptual_understanding,
                        time_management = EXCLUDED.time_management, selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week, branch = EXCLUDED.branch
                    """),
                    (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, conceptual_understanding, time_management, subjects_str, study_time, branch)
                )
                conn.commit()
                st.success("✅ Student information saved successfully!")
                st.session_state["email"] = email
                st.session_state["page"] = "Dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cur.close()
                conn.close()

def dashboard():
    st.header("Student Dashboard")

    if "email" not in st.session_state:
        st.warning("Please log in to view your dashboard.")
        return

    email = st.session_state["email"]
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week, branch FROM students WHERE email = %s",
            (email,),
        )
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student:
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Student Information")
                st.write(f"**Name:** {student[0]}")
                st.write(f"**Age:** {student[1]}")
                st.write(f"**Email:** {student[2]}")
                st.write(f"**Mobile Number:** {student[3]}")
                st.write(f"**Study Time Per Week:** {student[8]} h/w")
                st.write(f"**Branch:** {student[9]}")

            with col2:
                st.write("### Study Time Allocation")
                selected_subjects = student[7].split(", ")
                study_time = student[8]
                coding_eff = student[4]
                problem_solving_eff = student[6]
                study_allocation = allocate_study_time(selected_subjects, study_time, coding_eff, problem_solving_eff)
                for subject, hours in study_allocation.items():
                    st.write(f"- **{subject}:** {hours} h/w")

            st.markdown("---")
            col3, col4, col5 = st.columns(3)
            with col3:
                if st.button("Predict Future Score 🎯"):
                    st.session_state["page"] = "Predict Future Score"
                    st.rerun()
            with col4:
                if st.button("Take a Quiz 📝"):
                    st.session_state["page"] = "Quiz"
                    st.rerun()
            with col5:
                if st.button("Ask Questions 🤖"):
                    st.session_state["page"] = "Ask Questions"
                    st.rerun()
            with col5:
                if st.button("Add Study Content 📚"):
                    st.session_state["page"] = "Add Study Content"
                    st.rerun()
        else:
            st.warning("No records found for the logged-in user.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

def predict_future_score():
    st.header("Predict Future Score 🎯")
    st.write("Please provide additional details to predict your future score.")

    age = st.number_input("Age", min_value=1, max_value=100, value=st.session_state.get("age", 20))
    study_time_weekly = st.number_input("Study Time Per Week (hours)", min_value=1, max_value=168, value=st.session_state.get("study_time_per_week", 20))
    absences = st.number_input("Number of Absences", min_value=0, max_value=100, value=0)
    tutoring = st.selectbox("Do you receive tutoring?", ["No", "Yes"])
    extracurricular = st.selectbox("Do you participate in extracurricular activities?", ["No", "Yes"])
    sports = st.selectbox("Do you participate in sports?", ["No", "Yes"])
    music = st.selectbox("Do you participate in music activities?", ["No", "Yes"])
    volunteering = st.selectbox("Do you volunteer?", ["No", "Yes"])

    if st.button("Predict Grade"):
        # Prepare input data for the model
        tutoring = 1 if tutoring == "Yes" else 0
        extracurricular = 1 if extracurricular == "Yes" else 0
        sports = 1 if sports == "Yes" else 0
        music = 1 if music == "Yes" else 0
        volunteering = 1 if volunteering == "Yes" else 0

        user_data = [age, study_time_weekly, absences, tutoring, extracurricular, sports, music, volunteering]

        # Load the trained model
        with open('model (6).pkl', 'rb') as file:
            model = pickle.load(file)

        # Make a prediction
        predicted_grade = model.predict([user_data])

        # Display the result
        st.write(f"**Predicted Grade:** {predicted_grade[0]}")

        # Provide suggestions based on the predicted grade
        if predicted_grade[0] == 1:
            st.success("You are doing great! Keep up the good work.")
        elif predicted_grade[0] == 2:
            st.warning("You are doing well, but there is room for improvement. Consider increasing your study time or seeking tutoring.")
        else:
            st.error("You may need to make significant changes to improve your performance. Consider seeking tutoring, reducing absences, and increasing study time.")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def quiz_section():
    st.header("Quiz Section")
    try:
        with open('questions.pkl', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        st.error("The questions file was not found. Please ensure 'questions.pkl' is in the correct directory.")
        return

    all_questions = [q for subject in data.values() for q in subject]
    selected_questions = random.sample(all_questions, min(30, len(all_questions)))

    if 'quiz_started' not in st.session_state:
        st.session_state.update({
            'quiz_started': False,
            'current_question': 0,
            'user_answers': [],
            'score': 0,
            'selected_answer': None
        })

    if not st.session_state['quiz_started']:
        if st.button("Start Quiz"):
            st.session_state['quiz_started'] = True

    if st.session_state['quiz_started']:
        if st.session_state['current_question'] < len(selected_questions):
            question = selected_questions[st.session_state['current_question']]
            st.write(f"**Question {st.session_state['current_question'] + 1}:** {question['question']}")
            user_answer = st.radio("Select your answer:", question['options'], key=f"q{st.session_state['current_question']}", index=None)
            if user_answer is not None:
                st.session_state['selected_answer'] = user_answer
                if user_answer == question['answer']:
                    st.session_state['score'] += 1
                st.session_state['user_answers'].append(user_answer)
                st.session_state['current_question'] += 1
                st.session_state['selected_answer'] = None
                st.rerun()
        else:
            st.write("### Quiz Ended!")
            st.write(f"**Your Score:** {st.session_state['score']}/{len(selected_questions)}")
            st.write("### Review Your Answers:")
            for i, (question, user_answer) in enumerate(zip(selected_questions, st.session_state['user_answers'])):
                st.write(f"**Question {i + 1}:** {question['question']}")
                st.write(f"**Your Answer:** {user_answer}")
                st.write(f"**Correct Answer:** {question['answer']}")
                st.write("---")
            if st.button("Restart Quiz"):
                st.session_state.update({
                    'quiz_started': False,
                    'current_question': 0,
                    'user_answers': [],
                    'score': 0,
                    'selected_answer': None
                })
                st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def ask_questions():
    st.header("Ask Questions 🤖")
    st.write("You can ask any questions related to your subjects here.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please check your API key and ensure the Generative AI API is enabled.")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def add_study_content():
    st.header("Add Study Content 📚")
    st.write("Add links to study materials here.")

    if "study_links" not in st.session_state:
        st.session_state.study_links = []

    link = st.text_input("Enter a link to a study resource")
    if st.button("Add Link"):
        if link:
            st.session_state.study_links.append(link)
            st.success("Link added successfully!")
        else:
            st.error("Please enter a valid link.")

    st.write("### Study Links")
    for i, link in enumerate(st.session_state.study_links):
        st.write(f"{i + 1}. {link}")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Student Info"

    if st.session_state["page"] == "Student Info":
        student_info()
    elif st.session_state["page"] == "Dashboard":
        dashboard()
    elif st.session_state["page"] == "Quiz":
        quiz_section()
    elif st.session_state["page"] == "Ask Questions":
        ask_questions()
    elif st.session_state["page"] == "Add Study Content":
        add_study_content()
    elif st.session_state["page"] == "Predict Future Score":
        predict_future_score()

if __name__ == "__main__":
    main()
