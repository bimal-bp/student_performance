import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np
import pickle
import random

# Database Connection String
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

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
    # Define efficiency and problem-solving factors
    efficiency_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[efficiency_level]
    problem_solving_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[problem_solving]
    
    # Get ratings for selected subjects (default to 5 if not found)
    ratings = np.array([subject_ratings.get(sub, 5) for sub in selected_subjects])
    
    # Calculate weighted ratings
    weighted_ratings = ratings * efficiency_factor * problem_solving_factor
    
    # Normalize weights
    normalized_weights = weighted_ratings / np.sum(weighted_ratings)
    
    # Allocate time in hours
    allocated_times_hours = normalized_weights * total_hours
    
    # Convert decimal hours to hours and minutes
    allocated_times = {}
    for subject, time_hours in zip(selected_subjects, allocated_times_hours):
        hours = int(time_hours)
        minutes = int((time_hours - hours) * 60)
        allocated_times[subject] = f"{hours}h {minutes}m"
    
    return allocated_times

def sign_in():
    st.title("Learn Mate - Student Performance Application")
    st.header("Sign In")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    mobile_number = st.text_input("Mobile Number")

    if st.button("Sign In"):
        if not email:
            st.error("Please enter an email.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name, age = EXCLUDED.age, mobile_number = EXCLUDED.mobile_number
                    """),
                    (name, age, email, mobile_number)
                )
                conn.commit()
                st.success("✅ Signed in successfully!")
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
        st.warning("Please sign in to view your dashboard.")
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

            with col2:
                st.write("### Branch Selection")
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
                                (student[0], student[1], student[2], student[3], coding_eff, math_eff, problem_solving_eff, conceptual_understanding, time_management, subjects_str, study_time, branch)
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

            st.markdown("---")
            st.write("### Study Time Allocation")
            if student[7] and student[8]:
                selected_subjects = student[7].split(", ")
                study_time = student[8]
                coding_eff = student[4]
                problem_solving_eff = student[6]
                study_allocation = allocate_study_time(selected_subjects, study_time, coding_eff, problem_solving_eff)
                for subject, hours in study_allocation.items():
                    st.write(f"- **{subject}:** {hours} h/w")

            if st.button("Change Subjects"):
                st.session_state["page"] = "Change Subjects"
                st.rerun()

        else:
            st.warning("No records found for the logged-in user.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

def change_subjects():
    st.header("Change Subjects")

    if "email" not in st.session_state:
        st.warning("Please sign in to change subjects.")
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
            st.write("### Current Subjects")
            st.write(f"**Selected Subjects:** {student[7]}")
            st.write(f"**Study Time Per Week:** {student[8]} h/w")
            st.write(f"**Branch:** {student[9]}")

            st.write("### Update Subjects")
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

            study_time = st.number_input
