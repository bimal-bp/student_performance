import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np

# Database Connection String
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

# Predefined subject ratings (updated with new subjects)
subject_ratings = {
    # Existing subjects
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
    "Distributed Systems": 7,
    "Deep Learning": 9,
    "Data Mining": 9,
    "Big Data Analytics": 9,
    "Natural Language Processing": 9,
    "Reinforcement Learning": 9,
    "Data Visualization": 8,
    "Business Intelligence": 8,
    "Neural Networks": 9,
    "Computer Vision": 9,
    "Pattern Recognition": 8,
    "Business Strategy and Analytics": 9,
    "Financial and Management Accounting": 8,
    "Business Process Management": 8,
    "Enterprise Systems": 8,
    # New subjects (Electrical and Electronics Engineering)
    "Electrical Machines": 10,
    "Power Systems": 9,
    "Control Systems": 9,
    "Electrical Circuit Analysis": 10,
    "Power Electronics": 9,
    "Analog Electronics": 8,
    "Digital Electronics": 8,
    "Electromagnetic Field Theory": 7,
    "Microprocessors and Microcontrollers": 8,
    "Renewable Energy Systems": 7,
    "Electrical Measurements and Instrumentation": 8,
    # New subjects (Electronics and Communication Engineering)
    "Analog and Digital Communication": 10,
    "Signals and Systems": 9,
    "Digital Signal Processing (DSP)": 9,
    "VLSI Design": 9,
    "Optical Communication": 7,
    "Embedded Systems": 9,
    "Wireless Communication": 9,
    "Antenna and Wave Propagation": 7,
}

def allocate_study_time(selected_subjects, total_hours, efficiency_level, problem_solving):
    ratings = np.array([subject_ratings[sub] for sub in selected_subjects])
    efficiency_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[efficiency_level]
    problem_solving_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[problem_solving]
    
    weighted_ratings = ratings * efficiency_factor * problem_solving_factor
    normalized_weights = weighted_ratings / np.sum(weighted_ratings)
    
    allocated_times = np.round(normalized_weights * total_hours, 2)
    return dict(zip(selected_subjects, allocated_times))

def student_info():
    st.title("Learn Mate - Student Performance Application")
    st.header("Student Information")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        email = st.text_input("Email")
        mobile_number = st.text_input("Mobile Number")

    with col2:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])

    # Multiselect with a maximum of 10 subjects
    selected_subjects = st.multiselect(
        "Select subjects (max 10)", 
        options=list(subject_ratings.keys()), 
        default=[],
        key="subjects"
    )

    # Validate that no more than 10 subjects are selected
    if len(selected_subjects) > 10:
        st.error("You can select a maximum of 10 subjects.")
        selected_subjects = selected_subjects[:10]  # Truncate to 10 subjects

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
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age, 
                        mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency,
                        math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week
                    """),
                    (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, subjects_str, study_time)
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
        else:
            st.warning("No records found for the logged-in user.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Student Info"

    if st.session_state["page"] == "Student Info":
        student_info()
    elif st.session_state["page"] == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
