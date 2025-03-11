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
GEMINI_API_KEY = "AIzaSyDICIQ2Qq0k5yo91hdhWYQeXP__K__OfkU"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_db_connection():
    return psycopg2.connect(DB_URL)


def allocate_study_time(selected_subjects, total_hours, efficiency_level, problem_solving):
    ratings = np.array([subject_ratings[sub] for sub in selected_subjects])
    efficiency_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[efficiency_level]
    problem_solving_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[problem_solving]
    
    weighted_ratings = ratings * efficiency_factor * problem_solving_factor
    normalized_weights = weighted_ratings / np.sum(weighted_ratings)
    
    allocated_times = np.round(normalized_weights * total_hours, 2)
    return dict(zip(selected_subjects, allocated_times))

def generate_content(subjects):
    prompt = f"Generate a detailed study guide for the following subjects: {', '.join(subjects)}. Include key topics, resources, and tips for effective learning."
    response = model.generate_content(prompt)
    return response.text

def student_info():
    st.title("Learn Mate - Student Performance Application")
    st.header("Student Information")

    # Student Information
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    mobile_number = st.text_input("Mobile Number")

    # Branch-wise subject selection
    st.subheader("Select Your Branch")
    branch = st.selectbox(
        "Choose your branch",
        options=[
            "Computer Science",
            "Artificial Intelligence",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Common Subjects"
        ],
        key="branch"
    )

    # Branch-wise subjects
    branch_subjects = {
        "Computer Science": [
            "Programming", "Data Structures & Algorithms", "Operating Systems", "Computer Networks",
            "Database Management Systems", "Software Engineering", "Web Technologies", "Compiler Design",
            "Object-Oriented Programming", "Cryptography & Network Security", "Software Testing",
            "Data Mining & Data Warehousing", "Business Communication & Ethics", "Business Analytics",
            "Digital Marketing"
        ],
        "Artificial Intelligence": [
            "Artificial Intelligence", "Machine Learning", "Deep Learning", "Data Science & Analytics",
            "Natural Language Processing", "Neural Networks", "Reinforcement Learning", "Computer Vision",
            "Linear Algebra for ML", "Data Visualization", "Data Mining & Data Warehousing"
        ],
        "Electrical Engineering": [
            "Circuit Theory", "Digital Logic Design", "Analog & Digital Electronics", "Signals & Systems",
            "Microprocessors & Microcontrollers", "Communication Systems", "VLSI Design",
            "Antennas & Wave Propagation", "Embedded Systems", "Optical Communication",
            "IoT & Wireless Sensor Networks", "Electrical Circuits", "Control Systems", "Power Systems",
            "Electrical Machines", "Power Electronics", "Digital Signal Processing", "High Voltage Engineering",
            "Renewable Energy Systems", "Industrial Automation"
        ],
        "Mechanical Engineering": [
            "Engineering Mechanics", "Strength of Materials", "Thermodynamics", "Fluid Mechanics",
            "Manufacturing Processes", "Heat & Mass Transfer", "Machine Design", "Robotics", "CAD/CAM",
            "Automotive Engineering", "Industrial Engineering"
        ],
        "Civil Engineering": [
            "Structural Analysis", "Surveying", "Fluid Mechanics", "Geotechnical Engineering",
            "Construction Materials", "Transportation Engineering", "Environmental Engineering",
            "Hydrology & Water Resources", "Building Design & Architecture", "Earthquake Engineering"
        ],
        "Common Subjects": [
            "Engineering Mathematics", "Engineering Physics", "Engineering Chemistry",
            "Basic Electrical and Electronical Engineering", "Web Technologies", "Programming",
            "Data Structures & Algorithms", "Operating Systems", "Computer Networks",
            "Cryptography & Network Security", "Big Data Technologies", "Cloud Computing",
            "Cyber Security", "Blockchain Technology", "IoT (Internet of Things)",
            "Introduction to AI & ML", "Data Science & Analytics", "Probability & Statistics",
            "Engineering Drawing", "Engineering Economics & Financial Management"
        ]
    }

    # Subject selection based on branch
    st.subheader("Select Subjects")
    selected_subjects = st.multiselect(
        f"Select up to 10 subjects from {branch}",
        options=branch_subjects[branch],
        default=[],
        key="subjects"
    )

    # Validate that no more than 10 subjects are selected
    if len(selected_subjects) > 10:
        st.error("You can select a maximum of 10 subjects.")
        selected_subjects = selected_subjects[:10]  # Truncate to 10 subjects

    # Efficiency levels
    st.subheader("Efficiency Levels")
    col1, col2 = st.columns(2)

    with col1:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])

    with col2:
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])
        conceptual_understanding = st.selectbox("Conceptual Understanding", ["low", "intermediate", "high"])
        time_management = st.selectbox("Time Management", ["low", "intermediate", "high"])

    # Total study time
    study_time = st.number_input("Total Study Time Per Week (hours)", min_value=1, max_value=168)

    if st.button("Save Information"):
        if not email:
            st.error("Please enter an email.")
        elif len(selected_subjects) > 10:
            st.error("Please select no more than 10 subjects.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                subjects_str = ", ".join(selected_subjects)
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, 
                        problem_solving_efficiency, conceptual_understanding, time_management, selected_subjects, study_time_per_week)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age, 
                        mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency,
                        math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        conceptual_understanding = EXCLUDED.conceptual_understanding,
                        time_management = EXCLUDED.time_management,
                        selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week
                    """),
                    (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, conceptual_understanding, time_management, subjects_str, study_time)
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
            "SELECT name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week FROM students WHERE email = %s",
            (email,),
        )
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student:
            # Display Student Information and Study Time Allocation in two columns
            col1, col2 = st.columns(2)

            with col1:
                st.write("### Student Information")
                st.write(f"**Name:** {student[0]}")
                st.write(f"**Age:** {student[1]}")
                st.write(f"**Email:** {student[2]}")
                st.write(f"**Mobile Number:** {student[3]}")
                st.write(f"**Coding Efficiency:** {student[4]}")
                st.write(f"**Math Efficiency:** {student[5]}")
                st.write(f"**Problem Solving Efficiency:** {student[6]}")
                st.write(f"**Study Time Per Week:** {student[8]} hours")

            with col2:
                st.write("### Study Time Allocation")
                selected_subjects = student[7].split(", ")
                study_time = student[8]
                coding_eff = student[4]
                problem_solving_eff = student[6]
                study_allocation = allocate_study_time(selected_subjects, study_time, coding_eff, problem_solving_eff)

                for subject, hours in study_allocation.items():
                    st.write(f"- **{subject}:** {hours} hours/week")

            # Add three buttons below the columns
            st.markdown("---")
            col3, col4, col5 = st.columns(3)

            with col3:
                if st.button("Predict Future Score 🎯"):
                    st.write("🚧 Feature under construction!")  # Placeholder for future functionality

            with col4:
                if st.button("Take a Quiz 📝"):
                    st.session_state["page"] = "Quiz"
                    st.rerun()

            with col5:
                if st.button("Generate Study Content 📚"):
                    content = generate_content(selected_subjects)
                    st.write("### Generated Study Content")
                    st.write(content)

        else:
            st.warning("No records found for the logged-in user.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

def quiz_section():
    st.header("Quiz Section")

    # Load the questions from the .pkl file
    try:
        with open('questions.pkl', 'rb') as f:
            data = pickle.load(f)
        st.write("Questions loaded successfully!")  # Debug statement
    except FileNotFoundError:
        st.error("The questions file was not found. Please ensure 'questions.pkl' is in the correct directory.")
        return

    # Flatten all questions into a single list
    all_questions = []
    for subject, questions in data.items():
        all_questions.extend(questions)  # Add all questions from each subject to the list

    # Randomly select 30 questions from the flattened list
    if len(all_questions) >= 30:
        selected_questions = random.sample(all_questions, 30)
    else:
        selected_questions = all_questions  # If fewer than 30 questions, use all available

    # Initialize session state for quiz if not already present
    if 'quiz_started' not in st.session_state:
        st.session_state['quiz_started'] = False
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0
    if 'user_answers' not in st.session_state:
        st.session_state['user_answers'] = []
    if 'score' not in st.session_state:
        st.session_state['score'] = 0
    if 'selected_answer' not in st.session_state:
        st.session_state['selected_answer'] = None

    if not st.session_state['quiz_started']:
        if st.button("Start Quiz"):
            st.session_state['quiz_started'] = True

    if st.session_state['quiz_started']:
        if st.session_state['current_question'] < len(selected_questions):
            question = selected_questions[st.session_state['current_question']]
            st.write(f"**Question {st.session_state['current_question'] + 1}:** {question['question']}")
            
            # Display options using st.radio
            options = question['options']
            user_answer = st.radio(
                "Select your answer:",
                options,
                key=f"q{st.session_state['current_question']}",
                index=None if st.session_state['selected_answer'] is None else options.index(st.session_state['selected_answer'])
            )

            # Update the selected answer in session state
            if user_answer is not None:
                st.session_state['selected_answer'] = user_answer

            # Automatically move to the next question when an answer is selected
            if st.session_state['selected_answer'] is not None:
                # Check if the selected answer is correct
                if st.session_state['selected_answer'] == question['answer']:
                    st.session_state['score'] += 1
                # Store the user's answer
                st.session_state['user_answers'].append(st.session_state['selected_answer'])
                # Move to the next question
                st.session_state['current_question'] += 1
                st.session_state['selected_answer'] = None
                st.rerun()  # Refresh the app to show the next question
        else:
            # Quiz ended
            st.write("### Quiz Ended!")
            st.write(f"**Your Score:** {st.session_state['score']}/{len(selected_questions)}")
            
            # Show correct answers and user answers
            st.write("### Review Your Answers:")
            for i, (question, user_answer) in enumerate(zip(selected_questions, st.session_state['user_answers'])):
                st.write(f"**Question {i + 1}:** {question['question']}")
                st.write(f"**Your Answer:** {user_answer}")
                st.write(f"**Correct Answer:** {question['answer']}")
                st.write("---")
            
            # Restart quiz button
            if st.button("Restart Quiz"):
                st.session_state['quiz_started'] = False
                st.session_state['current_question'] = 0
                st.session_state['user_answers'] = []
                st.session_state['score'] = 0
                st.session_state['selected_answer'] = None
                st.rerun()

    # Back to Dashboard button
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

if __name__ == "__main__":
    main()
