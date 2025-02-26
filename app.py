import streamlit as st
import psycopg2
from psycopg2 import sql

DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def home():
    st.title("Welcome to the Student Performance Web Application")
    st.write("Navigate to different sections using the sidebar.")

def student_info():
    st.title("Student Performance Web Application")
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
    
    subjects = [
        "Data Structures and Algorithms", "Operating Systems", "Database Management Systems (DBMS)", "Computer Networks",
        "Software Engineering", "Python", "Object-Oriented Programming (Java/C/C++)", "Web Technologies",
        "Theory of Computation", "Compiler Design", "Artificial Intelligence", "Machine Learning",
        "Cloud Computing", "Cybersecurity", "Distributed Systems", "Electrical Machines", "Power Systems",
        "Control Systems", "Electrical Circuit Analysis", "Power Electronics", "Analog Electronics",
        "Digital Electronics", "Electromagnetic Field Theory", "Microprocessors and Microcontrollers",
        "Renewable Energy Systems", "Electrical Measurements and Instrumentation", "Analog and Digital Communication",
        "Signals and Systems", "Digital Signal Processing (DSP)", "VLSI Design", "Optical Communication",
        "Embedded Systems", "Wireless Communication", "Antenna and Wave Propagation", "Structural Analysis",
        "Fluid Mechanics", "Engineering Mechanics", "Geotechnical Engineering", "Construction Materials and Techniques",
        "Surveying", "Reinforced Concrete Structures", "Steel Structures", "Transportation Engineering",
        "Environmental Engineering", "Hydrology and Water Resources Engineering", "Foundation Engineering"
    ]
    
    selected_subjects = st.multiselect(
        "Select up to 10 subjects",
        options=subjects,
        default=[],
        key="subject_selection"
    )
    
    study_time = st.number_input("Study Time Per Week (hours)", min_value=1, max_value=168)
    
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

def dashboard():
    st.header("Student Dashboard")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, email, mobile_number, selected_subjects FROM students ORDER BY id DESC LIMIT 10;")
        students = cur.fetchall()
        cur.close()
        conn.close()
        
        if students:
            st.write("### Recent Students:")
            for student in students:
                st.write(f"**{student[1]}**, Age: {student[2]}, Email: {student[3]}, Mobile: {student[4]}")
                st.write("Selected Subjects:")
                for subject in student[5]:
                    st.write(f"- {subject}")
                if st.button(f"Update {student[1]}", key=f"update_{student[0]}"):
                    update_student(student[0])
        else:
            st.write("No student data available.")
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

def update_student(student_id):
    st.header("Update Student Information")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    
    if student:
        name = st.text_input("Name", value=student[1])
        age = st.number_input("Age", min_value=1, max_value=100, value=student[2])
        email = st.text_input("Email", value=student[3])
        mobile_number = st.text_input("Mobile Number", value=student[4])
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"], index=["low", "intermediate", "high"].index(student[5]))
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"], index=["low", "intermediate", "high"].index(student[6]))
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"], index=["low", "intermediate", "high"].index(student[7]))
        
        subjects = [
            "Data Structures and Algorithms", "Operating Systems", "Database Management Systems (DBMS)", "Computer Networks",
            "Software Engineering", "Python", "Object-Oriented Programming (Java/C/C++)", "Web Technologies",
            "Theory of Computation", "Compiler Design", "Artificial Intelligence", "Machine Learning",
            "Cloud Computing", "Cybersecurity", "Distributed Systems", "Electrical Machines", "Power Systems",
            "Control Systems", "Electrical Circuit Analysis", "Power Electronics", "Analog Electronics",
            "Digital Electronics", "Electromagnetic Field Theory", "Microprocessors and Microcontrollers",
            "Renewable Energy Systems", "Electrical Measurements and Instrumentation", "Analog and Digital Communication",
            "Signals and Systems", "Digital Signal Processing (DSP)", "VLSI Design", "Optical Communication",
            "Embedded Systems", "Wireless Communication", "Antenna and Wave Propagation", "Structural Analysis",
            "Fluid Mechanics", "Engineering Mechanics", "Geotechnical Engineering", "Construction Materials and Techniques",
            "Surveying", "Reinforced Concrete Structures", "Steel Structures", "Transportation Engineering",
            "Environmental Engineering", "Hydrology and Water Resources Engineering", "Foundation Engineering"
        ]
        
        selected_subjects = st.multiselect(
            "Select up to 10 subjects",
            options=subjects,
            default=student[8],
            key=f"subject_selection_{student_id}"
        )
        
        study_time = st.number_input("Study Time Per Week (hours)", min_value=1, max_value=168, value=student[9])
        
        if st.button("Update Information"):
            if len(selected_subjects) != 10:
                st.error("Please select exactly 10 subjects.")
            else:
                conn = get_db_connection()
                cur = conn.cursor()
                try:
                    cur.execute(
                        sql.SQL("""
                            UPDATE students
                            SET name = %s, age = %s, email = %s, mobile_number = %s, coding_efficiency = %s, math_efficiency = %s, problem_solving_efficiency = %s, selected_subjects = %s, study_time_per_week = %s
                            WHERE id = %s
                        """),
                        (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, selected_subjects, study_time, student_id)
                    )
                    conn.commit()
                    st.success("Student information updated successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    cur.close()
                    conn.close()

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Student Info", "Dashboard"])
    
    if selection == "Home":
        home()
    elif selection == "Student Info":
        student_info()
    elif selection == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
