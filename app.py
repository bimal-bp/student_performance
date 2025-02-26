import streamlit as st
import psycopg2
from psycopg2 import sql

# Database connection
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

# AHP (Analytic Hierarchy Process) for time allocation
def ahp_time_allocation(subjects, coding_eff, math_eff, problem_solving_eff, study_time):
    # Define weights for efficiency levels
    efficiency_weights = {
        'low': 1,
        'intermediate': 2,
        'high': 3
    }

    # Assign weights based on efficiency levels
    coding_weight = efficiency_weights[coding_eff]
    math_weight = efficiency_weights[math_eff]
    problem_solving_weight = efficiency_weights[problem_solving_eff]

    # Normalize weights
    total_weight = coding_weight + math_weight + problem_solving_weight
    coding_weight_normalized = coding_weight / total_weight
    math_weight_normalized = math_weight / total_weight
    problem_solving_weight_normalized = problem_solving_weight / total_weight

    # Assign time to subjects based on their ratings and weights
    subject_ratings = {subject: rating for subject, rating in subjects.items()}
    total_rating = sum(subject_ratings.values())
    time_allocation = {
        subject: (rating / total_rating) * study_time * coding_weight_normalized  # Prioritize coding
        for subject, rating in subject_ratings.items()
    }

    return time_allocation

# Login and Student Info Page
def login_and_student_info():
    st.title("Student Performance Web Application")
    st.header("Login and Student Information")

    # Use columns to display input fields side by side
    col1, col2 = st.columns(2)

    with col1:
        # Input fields
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        email = st.text_input("Email")
        mobile_number = st.text_input("Mobile Number")

    with col2:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])

    # Subject selection
    subjects = {
        "Data Structures and Algorithms": 10,
        "Operating Systems": 9,
        "Database Management Systems (DBMS)": 9,
        "Computer Networks": 8,
        "Software Engineering": 7,
        "Python": 10,
        "Object-Oriented Programming (Java/C/C++)": 10,
        "Web Technologies": 7,
        "Theory of Computation": 8,
        "Compiler Design": 7,
        "Artificial Intelligence": 9,
        "Machine Learning": 9,
        "Cloud Computing": 8,
        "Cybersecurity": 8,
        "Distributed Systems": 7
    }
    selected_subjects = st.multiselect("Select 10 Subjects", list(subjects.keys()), default=list(subjects.keys())[:10])

    # Study time input
    study_time = st.number_input("Study Time Per Week (hours)", min_value=1, max_value=168)

    # Save to database
    if st.button("Save Information"):
        if len(selected_subjects) != 10:
            st.error("Please select exactly 10 subjects.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """),
                    (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, selected_subjects, study_time)
                )
                conn.commit()
                st.success("Student information saved successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                cur.close()
                conn.close()

# Dashboard Page
def dashboard():
    st.title("Dashboard")
    st.header("Student Information and Time Allocation")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    conn.close()

    if not students:
        st.warning("No student data found.")
        return

    # Display student information
    for student in students:
        st.subheader(f"Student: {student[1]}")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"Age: {student[2]}")
            st.write(f"Email: {student[3]}")
            st.write(f"Mobile Number: {student[4]}")
            st.write(f"Coding Efficiency: {student[5]}")
            st.write(f"Math Efficiency: {student[6]}")
            st.write(f"Problem Solving Efficiency: {student[7]}")
            st.write(f"Selected Subjects: {', '.join(student[8])}")
            st.write(f"Study Time Per Week: {student[9]} hours")

        with col2:
            # Calculate time allocation using AHP
            subjects_with_ratings = {subject: subjects[subject] for subject in student[8]}
            time_allocation = ahp_time_allocation(subjects_with_ratings, student[5], student[6], student[7], student[9])

            st.subheader("Time Allocation for Subjects")
            for subject, time in time_allocation.items():
                st.write(f"{subject}: {round(time, 2)} hours")

        st.write("---")

# Main App
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login and Student Info", "Dashboard"])

    if page == "Login and Student Info":
        login_and_student_info()
    elif page == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
