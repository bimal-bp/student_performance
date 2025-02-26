import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np

DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def allocate_study_time(subject_ratings, total_hours, efficiency_factor):
    weights = np.array(subject_ratings) / sum(subject_ratings)
    allocated_time = np.round(weights * total_hours * efficiency_factor, 2)
    return allocated_time

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
    
    efficiency_map = {"low": 0.8, "intermediate": 1.0, "high": 1.2}
    efficiency_factor = np.mean([
        efficiency_map[coding_eff], 
        efficiency_map[math_eff], 
        efficiency_map[problem_solving_eff]
    ])
    
    subjects = [
        "Data Structures and Algorithms", "Operating Systems", "Database Management Systems (DBMS)", "Computer Networks",
        "Software Engineering", "Python", "Object-Oriented Programming (Java/C/C++)", "Web Technologies",
        "Theory of Computation", "Compiler Design", "Artificial Intelligence", "Machine Learning",
        "Cloud Computing", "Cybersecurity", "Distributed Systems",
        "Machine Learning", "Artificial Intelligence", "Deep Learning", "Data Mining", "Big Data Analytics",
        "Natural Language Processing", "Reinforcement Learning", "Data Visualization", "Business Intelligence",
        "Neural Networks", "Computer Vision", "Pattern Recognition",
        "Business Strategy and Analytics", "Financial and Management Accounting", "Business Process Management", "Enterprise Systems"
    ]
    
    selected_subjects = st.multiselect("Select up to 10 subjects", options=subjects, default=[], key="subject_selection")
    if len(selected_subjects) > 10:
        st.error("Please select a maximum of 10 subjects.")
        return
    
    subject_ratings = [st.slider(f"Rate proficiency in {subject}", 1, 10, 5) for subject in selected_subjects]
    study_time = st.number_input("Total Study Time Per Week (hours)", min_value=1, max_value=168)
    
    if st.button("Save Information"):
        allocated_times = allocate_study_time(subject_ratings, study_time, efficiency_factor)
        study_allocation = dict(zip(selected_subjects, allocated_times))
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                sql.SQL("""
                    INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week, study_allocation)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO UPDATE 
                    SET age = EXCLUDED.age,
                        mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency,
                        math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week,
                        study_allocation = EXCLUDED.study_allocation
                """),
                (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, ", ".join(selected_subjects), study_time, str(study_allocation))
            )
            conn.commit()
            st.success("Student information saved successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cur.close()
            conn.close()

def dashboard():
    st.header("Student Dashboard")
    email_filter = st.text_input("Enter Email to Filter")
    
    if email_filter:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT name, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week, study_allocation FROM students WHERE email = %s", (email_filter,))
            student = cur.fetchone()
            cur.close()
            conn.close()
            
            if student:
                st.write(f"**Name:** {student[0]}")
                st.write(f"**Email:** {student[1]}")
                st.write(f"**Mobile Number:** {student[2]}")
                st.write(f"**Coding Efficiency:** {student[3]}")
                st.write(f"**Math Efficiency:** {student[4]}")
                st.write(f"**Problem Solving Efficiency:** {student[5]}")
                st.write(f"**Selected Subjects:** {student[6]}")
                st.write(f"**Study Time Per Week:** {student[7]} hours")
                st.write(f"**Study Allocation:** {student[8]}")
            else:
                st.write("No records found for this email.")
        except Exception as e:
            st.error(f"Error loading dashboard: {e}")

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Student Info", "Dashboard"])
    
    if selection == "Student Info":
        student_info()
    elif selection == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
