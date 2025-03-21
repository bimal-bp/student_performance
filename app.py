import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np
import pickle
import random
import hashlib

# Database Connection Strings
AUTH_DB_URL = "postgresql://neondb_owner:npg_P0wyolC1KBLW@ep-holy-mud-a5su2ghw-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
APP_DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_auth_db_connection():
    return psycopg2.connect(AUTH_DB_URL)

def get_app_db_connection():
    return psycopg2.connect(APP_DB_URL)

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign-Up Page
def sign_up():
    st.title("Sign Up")
    st.write("Create a new account to access the application.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            conn = get_auth_db_connection()
            cur = conn.cursor()
            try:
                # Check if the user already exists
                cur.execute("SELECT email FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    st.error("❌ User already exists. Please log in.")
                else:
                    hashed_password = hash_password(password)
                    cur.execute(
                        sql.SQL("""
                            INSERT INTO users (email, password)
                            VALUES (%s, %s)
                        """),
                        (email, hashed_password)
                    )
                    conn.commit()
                    st.success("✅ Account created successfully! Please log in.")
                    # Set a flag in session state to indicate successful sign-up
                    st.session_state["signup_success"] = True
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cur.close()
                conn.close()

    # Check if sign-up was successful and show the "Go to Login" button
    if st.session_state.get("signup_success", False):
        if st.button("Go to Login"):
            st.session_state["page"] = "Login"
            # Clear the signup success flag
            del st.session_state["signup_success"]
            st.rerun()

# Login Page
def login():
    st.title("Login")
    st.write("Log in to access the application.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_auth_db_connection()
        cur = conn.cursor()
        try:
            hashed_password = hash_password(password)
            cur.execute(
                "SELECT email FROM users WHERE email = %s AND password = %s",
                (email, hashed_password)
            )
            user = cur.fetchone()
            if user:
                st.success("✅ Login successful!")
                st.session_state["email"] = email
                st.session_state["page"] = "Student Info"
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cur.close()
            conn.close()

# Student Info Page
def student_info():
    st.title("Learn Mate - Student Performance Application")
    st.header("Student Information")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email", value=st.session_state.get("email", ""), disabled=True)
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
        "Computer Science": [
            "Advanced Programming", "Database Management Systems", "Software Engineering",
            "Machine Learning", "Artificial Intelligence", "Computer Architecture",
            "Programming", "Data Structures & Algorithms", "Operating Systems",
            "Computer Networks", "Web Technologies", "Compiler Design",
            "Object-Oriented Programming", "Cryptography & Network Security",
            "Software Testing", "Data Mining & Data Warehousing",
            "Business Communication & Ethics", "Business Analytics", "Digital Marketing"
        ],
        "Artificial Intelligence": [
            "Deep Learning", "Natural Language Processing", "Computer Vision",
            "Reinforcement Learning", "AI Ethics", "Robotics", "Artificial Intelligence",
            "Machine Learning", "Data Science & Analytics", "Neural Networks",
            "Linear Algebra for ML", "Data Visualization"
        ],
        "Electrical Engineering": [
            "Circuit Theory", "Power Systems", "Control Systems", "Signal Processing",
            "Microelectronics", "Renewable Energy Systems", "Digital Logic Design",
            "Analog & Digital Electronics", "Signals & Systems", "Microprocessors & Microcontrollers",
            "Communication Systems", "VLSI Design", "Antennas & Wave Propagation",
            "Embedded Systems", "Optical Communication", "IoT & Wireless Sensor Networks",
            "Electrical Circuits", "Electrical Machines", "Power Electronics",
            "Digital Signal Processing", "High Voltage Engineering", "Industrial Automation"
        ],
        "Mechanical Engineering": [
            "Thermodynamics", "Fluid Mechanics", "Solid Mechanics", "Manufacturing Processes",
            "Heat Transfer", "Machine Design", "Engineering Mechanics", "Strength of Materials",
            "Heat & Mass Transfer", "Robotics", "CAD/CAM", "Automotive Engineering",
            "Industrial Engineering"
        ],
        "Civil Engineering": [
            "Structural Analysis", "Geotechnical Engineering", "Transportation Engineering",
            "Environmental Engineering", "Construction Management", "Hydrology",
            "Surveying", "Construction Materials", "Hydrology & Water Resources",
            "Building Design & Architecture", "Earthquake Engineering"
        ]
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
            conn = get_app_db_connection()
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

# Dashboard Page
def dashboard():
    st.header("Student Dashboard")

    if "email" not in st.session_state:
        st.warning("Please log in to view your dashboard.")
        return

    email = st.session_state["email"]
    try:
        conn = get_app_db_connection()
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
                if st.button("Study Content 📚"):
                    st.session_state["page"] = "Study Content"
                    st.rerun()
        else:
            st.warning("No records found for the logged-in user.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

# Predict Future Score Page
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

# Quiz Section
def quiz_section():
    st.header("Quiz Section")
    
    try:
        with open('quiz_data.pkl', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        st.error("The questions file was not found. Please ensure 'quiz_data.pkl' is in the correct directory.")
        return

    # Allow the user to select a branch
    branch = st.selectbox("Choose a branch for the quiz:", list(data.keys()))
    
    if 'quiz_started' not in st.session_state:
        st.session_state.update({
            'quiz_started': False,
            'current_question': 0,
            'user_answers': [],
            'score': 0,
            'selected_answer': None,
            'selected_branch': None
        })

    if not st.session_state['quiz_started']:
        if st.button("Start Quiz"):
            st.session_state['quiz_started'] = True
            st.session_state['selected_branch'] = branch
            st.session_state['selected_questions'] = random.sample(data[branch], min(30, len(data[branch])))  # Select up to 30 questions

    if st.session_state['quiz_started']:
        selected_questions = st.session_state['selected_questions']
        if st.session_state['current_question'] < len(selected_questions):
            question = selected_questions[st.session_state['current_question']]
            st.write(f"**Question {st.session_state['current_question'] + 1}:** {question['question']}")
            user_answer = st.radio("Select your answer:", question['options'], key=f"q{st.session_state['current_question']}", index=None)
            
            if st.button("Submit Answer"):
                if user_answer is not None:
                    st.session_state['selected_answer'] = user_answer
                    if user_answer[0] == question['answer']:  # Compare the first character (e.g., "A", "B")
                        st.session_state['score'] += 1
                    st.session_state['user_answers'].append(user_answer)
                    st.session_state['current_question'] += 1
                    st.session_state['selected_answer'] = None
                    st.rerun()
                else:
                    st.warning("Please select an answer before submitting.")
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
                    'selected_answer': None,
                    'selected_branch': None
                })
                st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def landing_page():
    st.title("Welcome to Learn Mate")
    st.write("Please choose an option to get started.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up"):
            st.session_state["page"] = "Sign Up"
            st.rerun()
    with col2:
        if st.button("Login"):
            st.session_state["page"] = "Login"
            st.rerun()

# Main Function
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Landing Page"

    if st.session_state["page"] == "Landing Page":
        landing_page()
    elif st.session_state["page"] == "Sign Up":
        sign_up()
    elif st.session_state["page"] == "Login":
        login()
    elif st.session_state["page"] == "Student Info":
        student_info()
    elif st.session_state["page"] == "Dashboard":
        dashboard()


if __name__ == "__main__":
    main()
       
