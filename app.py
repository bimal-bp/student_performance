import streamlit as st
import pandas as pd
import psycopg2
import google.generativeai as genai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini API Setup
genai.configure(api_key="AIzaSyCNV_-fekzYdly2JoVBZ8wa-k3J-ZMbLbs")

# Database connection
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Function to create tables if they don't exist
def create_tables():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Student Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                phone TEXT UNIQUE,
                email TEXT UNIQUE,
                coding TEXT,
                mathematics TEXT,
                problem_solving TEXT,
                study_time INTEGER,
                subjects TEXT
            )
        """)

        # MCDM Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mcdm_techniques (
                id SERIAL PRIMARY KEY,
                technique_name TEXT UNIQUE,
                description TEXT
            )
        """)

        conn.commit()
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to insert student data
def insert_student(name, age, gender, phone, email, coding, math, problem_solving, study_time, subjects):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        subjects_str = ", ".join(subjects)  # Convert list to string
        
        cur.execute("""
            INSERT INTO students (name, age, gender, phone, email, coding, mathematics, problem_solving, study_time, subjects)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (phone) DO UPDATE SET
            name = EXCLUDED.name, age = EXCLUDED.age, gender = EXCLUDED.gender, email = EXCLUDED.email,
            coding = EXCLUDED.coding, mathematics = EXCLUDED.mathematics, problem_solving = EXCLUDED.problem_solving,
            study_time = EXCLUDED.study_time, subjects = EXCLUDED.subjects
        """, (name, age, gender, phone, email, coding, math, problem_solving, study_time, subjects_str))

        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting student data: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to fetch student data
def fetch_student(phone):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE phone = %s", (phone,))
        student = cur.fetchone()
        return student
    except Exception as e:
        logger.error(f"Error fetching student data: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to fetch all students
def fetch_all_students():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, gender, phone, email, study_time FROM students")
        students = cur.fetchall()
        return students
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to fetch MCDM techniques
def fetch_mcdm_techniques():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM mcdm_techniques")
        techniques = cur.fetchall()
        return techniques
    except Exception as e:
        logger.error(f"Error fetching MCDM techniques: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to generate AI-based quiz using Gemini API
def generate_quiz(question):
    try:
        response = genai.chat(prompt=f"Create a multiple-choice quiz question with 4 options for {question}. Provide the correct answer.")
        return response.text
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        return "Failed to generate quiz."

# Create tables on startup
create_tables()

# Session Management
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if st.session_state["page"] == "login":
    st.title("Student Login")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")

    st.write("### Select Your Proficiencies")
    coding = st.selectbox("Coding Proficiency", ["Beginner", "Intermediate", "Expert"])
    mathematics = st.selectbox("Mathematics Proficiency", ["Beginner", "Intermediate", "Expert"])
    problem_solving = st.selectbox("Problem Solving Proficiency", ["Beginner", "Intermediate", "Expert"])
    study_time = st.slider("Study Time per Week (hrs)", 0, 50, 10)

    subjects = ["Data Structures", "Operating Systems", "DBMS", "Python", "ML", "AI"]
    selected_subjects = st.multiselect("Select Subjects", subjects, max_selections=10)

    if st.button("Save Details"):
        insert_student(name, age, gender, phone, email, coding, mathematics, problem_solving, study_time, selected_subjects)
        st.success("Student data saved successfully!")

    if st.button("Go to Dashboard") and phone:
        st.session_state["student_phone"] = phone
        st.session_state["page"] = "dashboard"

elif st.session_state["page"] == "dashboard":
    st.title("📊 Student Dashboard")
    
    students = fetch_all_students()
    if students:
        df = pd.DataFrame(students, columns=["ID", "Name", "Age", "Gender", "Phone", "Email", "Study Time"])
        st.dataframe(df)

    st.subheader("🔍 MCDM Techniques")
    techniques = fetch_mcdm_techniques()
    if techniques:
        df_mcdm = pd.DataFrame(techniques, columns=["ID", "Technique", "Description"])
        st.dataframe(df_mcdm)
    else:
        st.write("No MCDM techniques found.")

    if st.button("Back to Login"):
        st.session_state["page"] = "login"
